# app/utilities/logging_conf.py
import logging
import ecs_logging
import os
import re
from typing import Union, Dict, Any
from ..config import settings  # Asegúrate de que config.py está actualizado

class CustomLogger:
    def __init__(self, name, log_type='functional'):
        self.logger = logging.getLogger(name)
        self.log_type = log_type

        # Niveles de logging (con defaults y variables de entorno)
        self.root_level = os.environ.get('ROOT_LOGGER_LEVEL', 'ERROR')
        self.technical_level = os.environ.get('TECHNICAL_LOGGER_LEVEL', 'INFO')
        self.functional_level = os.environ.get('FUNCTIONAL_LOGGER_LEVEL', 'DEBUG')

        # Establecer nivel según tipo de log
        if log_type == 'root':
            level = self.root_level
        elif log_type == 'technical':
            level = self.technical_level
        else:  # Default: functional
            level = self.functional_level
        self.logger.setLevel(getattr(logging, level))


        # Usar ecs_logging.StdlibFormatter()
        handler = logging.StreamHandler()
        formatter = ecs_logging.StdlibFormatter()
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)



    def _anonymize(self, message: Union[str, Dict[str, Any]]) -> Union[str, Dict[str, Any]]:
        """Anonimiza el mensaje según la configuración."""

        if not settings.LOGS_IGNORE_ACTIVE:
            return message

        if isinstance(message, dict):
            for key, value in message.items():
                if key in settings.REQUEST_BODY_FIELDS and self.log_type == "activity":
                    message[key] = "****"
                if key in settings.REQUEST_HEADER_FIELDS and self.log_type == "activity":
                    message[key] = "****"
                # Añade response fields
                if key in settings.RESPONSE_BODY_FIELDS and self.log_type == "activity":
                    message[key] = "****"
                if key in settings.RESPONSE_HEADER_FIELDS and self.log_type == "activity":
                    message[key] = "****"

        elif isinstance(message, str):
            for regex_pattern in settings.LOGS_REGEX:
                try:
                    message = re.sub(regex_pattern, r'"\1": "****"', message, flags=re.MULTILINE)
                except (TypeError, re.error) as e:
                    self.logger.error(f"Error en regex: {e}")
        return message


    def _log(self, level, msg, *args, log_type_override=None, **kwargs):
        """Método interno para centralizar el logging."""
        if self.logger.isEnabledFor(level):
            if args:
                msg = msg.format(*args)
            # Anonimiza DESPUÉS del formateo con *args
            msg = self._anonymize(msg)

            extra_data = {
                "log_type": log_type_override if log_type_override else self.log_type,
                "service.name": settings.PROJECT_NAME  # Añade el nombre del servicio
            }
            #Añade a extra si hay kwargs
            if kwargs:
                extra_data.update(kwargs)
            
            # Pasa 'extra' al logger
            self.logger.log(level, msg, extra=extra_data)

    def debug(self, msg, *args, **kwargs):
        self._log(logging.DEBUG, msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self._log(logging.INFO, msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self._log(logging.WARNING, msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self._log(logging.ERROR, msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self._log(logging.CRITICAL, msg, *args, **kwargs)

    def exception(self, msg, *args, **kwargs):
        """Log an exception with traceback.  Usar exc_info=True."""
        self._log(logging.ERROR, msg, *args, exc_info=True, **kwargs)



    def activity(self, request, response):
        """Log de actividad (entrada/salida de peticiones)."""
        request_data = {
            'http.request.method': request.method,
            'url.full': str(request.url),
            'http.request.headers': dict(request.headers), # type: ignore
            'url.query': request.url.query,
             'client.address': request.client.host if request.client else None, # type: ignore
            'client.port': request.client.port if request.client else None # type: ignore
        }
        try:
            request_data['http.request.body.content'] = request.json() # type: ignore
        except:
            request_data['http.request.body.content'] = None

        response_data = {
            'http.response.status_code': response.status_code,
            'http.response.headers': dict(response.headers), # type: ignore
        }

        try:
             response_data['http.response.body.content'] = response.json() # type: ignore

        except:
            response_data['http.response.body.content'] = None

        self._log(logging.INFO, "Request", log_type_override="activity", **request_data)
        self._log(logging.INFO, "Response", log_type_override="activity", **response_data)

    def audit(self, msg, *args, **kwargs):
        """Log de auditoría (para mediciones)."""
        self._log(logging.INFO, msg, *args, log_type_override="audit", **kwargs)


# Funciones para obtener loggers específicos
def get_logger(name="microservicio_python"):
    return CustomLogger(name, 'functional')

def get_technical_logger(name="microservicio_python"):
    return CustomLogger(name, 'technical')

def get_root_logger(name="microservicio_python"):
    return CustomLogger(name, 'root')