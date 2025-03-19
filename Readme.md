
# Documentación Microservicio de FastAPI en Python

## 1. Introducción

¡Bienvenido a la **Plantilla de Microservicio** construida con FastAPI! Esta plantilla incluye:

- **Estructura básica del proyecto**: Separación clara de responsabilidades (punto de entrada principal, endpoints, configuraciones y seguridad).
- **Autenticación**: Un ejemplo usando tokens JWT.
- **Llamadas a APIs externas**: Demostración de solicitudes a servicios internos o de terceros.
- **Registro de logs**: Configuración básica de logging para eventos de inicio y apagado.
- **Configuración**: Fácil gestión de variables de entorno para distintos entornos (desarrollo, producción, etc.).

Esta documentación te guiará a través de la estructura del proyecto, cómo se manejan las solicitudes y cómo funciona la autenticación/autorización.

---

## 2. Arquitectura a simple vista

```
my_microservice/
│
├── main.py                   # Punto de entrada de la aplicación
├── app/
│   ├── config.py             # Configuración central (variables de entorno, etc.)
│   ├── logging_conf.py       # Configuración de logging
│   ├── middleware.py         # Configuración del middleware para logging
│   ├── security.py           # Funciones y dependencias relacionadas con JWT         
│   ├── models/
│   │   ├── __init__.py
│   │   ├── auth.py           # Modelos Pydantic relacionados con autenticación
│   │   ├── user.py           # Modelos Pydantic relacionados con usuarios
│   │   └── external.py       # Modelos Pydantic para servicios externos
│   └── endpoints/
│       ├── __init__.py
│       ├── public.py         # Endpoints públicos sin autenticación
│       ├── private.py        # Endpoints que requieren autenticación con JWT
│       ├── auth.py           # Endpoints de inicio de sesión y generación de tokens
│       └── external.py       # Demostración de llamadas HTTP a una API externa
└── requirements.txt          # Dependencias de Python
```

### Principios clave

- **Separación de responsabilidades**: Cada grupo de endpoints (público, privado, auth, externo) está en su propio archivo dentro de `app/endpoints`.
- **Módulos reutilizables**: Utilidades de seguridad, configuración de logging y configuración de entorno en módulos dedicados.
- **Modelos Pydantic**: Uso de Pydantic para validación de entradas y salidas, asegurando estructuras de datos predecibles y documentación OpenAPI automática.

---

## 3. Instalación y Configuración

### Clonar el repositorio:

```bash
git clone https://github.com/your-org/my_microservice.git
cd my_microservice
```

### Crear y activar un entorno virtual (recomendado):

```bash
python -m venv venv
source venv/bin/activate  # En Linux/Mac
# Usuarios de Windows:
venv\Scripts\activate
```

### Instalar dependencias:

```bash
pip install -r requirements.txt
```

### Ejecutar la aplicación:

```bash
uvicorn main:app --reload
```

Esto iniciará el servidor en modo desarrollo en [http://127.0.0.1:8000](http://127.0.0.1:8000).

### Documentación OpenAPI:

Una vez que el servidor esté en ejecución, navega a [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) para ver la documentación interactiva generada automáticamente.

---

## 4. Punto de entrada principal de la aplicación (`main.py`)

### Explicación:

- `app = FastAPI(...)`: Inicializa la aplicación FastAPI.
- **Routers**: Cada router (público, privado, auth, externo) se define en un archivo Python separado y se incluye aquí con un prefijo único (`/api/v1/...`).
- **Logging**: En el inicio y apagado, el servicio registra mensajes indicando el entorno o cualquier otra información relevante.
- **CORS**: Permite solicitudes de origen cruzado; ajústalo según tu política de seguridad en producción.

---

## 5. Configuración (`app/config.py`)

### Puntos clave:

- `BaseSettings` de Pydantic lee automáticamente las variables de entorno y los valores del archivo `.env`.
- `settings` es una instancia que puedes importar en toda la aplicación (`settings.ENVIRONMENT`, etc.).

---

## 6. Configuración de Logging (`app/logging_conf.py`)

---

## 7. Seguridad (JWT) (`app/security/jwt.py`)

La seguridad en este microservicio se maneja a través de **JSON Web Tokens (JWT)**, lo que permite autenticar y autorizar a los usuarios de manera segura. Se usa **OAuth2 con flujo de contraseña** para obtener tokens de acceso.

### ¿Por qué usar JWT?

- **Sin estado**: No es necesario almacenar sesiones en el servidor, ya que el token contiene toda la información de autenticación.
- **Seguro**: Firmado digitalmente con una clave secreta, evitando manipulaciones maliciosas.
- **Flexible**: Se puede usar en múltiples servicios y plataformas sin necesidad de compartir sesiones.

### Generación de tokens

Para autenticar a un usuario, se genera un token JWT con una fecha de expiración. Este token incluye la información del usuario y se firma digitalmente para garantizar su integridad.

```python
def create_access_token(data: dict, expires_delta: Union[int, None] = None):
    """
    Genera un JWT token con expiración.
    """
    return encoded_jwt
```

### Validación y Decodificación de Tokens

Cada vez que un usuario realiza una solicitud protegida, el token se valida y se extrae la información de autenticación. Si el token ha expirado o ha sido modificado, la solicitud se rechaza.

```python
def decode_access_token(token: str):
    """
    Decodifica y verifica un JWT token.
    """
```

### Protección de Endpoints

Los endpoints protegidos requieren que el usuario envíe su token en la cabecera de autorización. FastAPI se encarga de verificar la validez del token antes de conceder acceso.

```python
@router.get("/", response_model=dict)
def private_endpoint(current_user: User = Depends(get_current_user)):
    """
    Enpoint privado que requiere JWT válido.
    """
    return {"message": f"Hello, {current_user.username}. This is a private endpoint."}

```

---

## 8. Modelos (`app/models/*`)

### Ejemplo: `user.py`

```python
from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    username: str
    email: Optional[str] = None
```

### ¿Por qué usar Pydantic?

- Garantiza que la estructura de datos se valide según el esquema esperado.
- Genera automáticamente la documentación OpenAPI (visible en `/docs`).

---

## 9. Implementación de Endpoints (`app/endpoints/*`)

Cada archivo define una instancia de `APIRouter` separada que se monta en `main.py`. La estructura de los endpoints es la siguiente:

- **Endpoints Públicos**: Accesibles sin autenticación, como un mensaje de bienvenida o información de usuario pública.
- **Endpoints Privados**: Requieren autenticación basada en JWT y permiten acciones específicas de usuario.
- **Endpoints de Autenticación**: Manejan el inicio de sesión y la generación de tokens para el control de acceso.
- **Llamadas a API Externas**: Demuestra cómo hacer solicitudes HTTP a servicios de terceros con manejo de errores y validación de respuestas.

### Consideraciones clave:

- **Seguridad**: Los endpoints privados usan inyección de dependencias para validar tokens JWT antes de conceder acceso.
- **Diseño estructurado de la API**: Cada tipo de endpoint está organizado en archivos separados para facilitar el mantenimiento.
- **Manejo de errores**: Excepciones adecuadas garantizan que se devuelvan errores HTTP cuando las solicitudes externas fallen.

### Ejemplo de implementación

#### `app/endpoints/public.py`
```python
from fastapi import APIRouter

router = APIRouter()

@router.get("/", response_model=dict)
def root_public_endpoint():
    """
    Endpoint público sin autenticación requerida.
    """
    return {"message": "¡Bienvenido al endpoint público!"}
```

