## Estilo de Código: PEP 8 y Flake8

### ¿Qué es PEP 8?

[PEP 8](https://peps.python.org/pep-0008/) es el estándar oficial de estilo para el lenguaje de programación Python. Define un conjunto de convenciones sobre cómo escribir código Python de forma clara, legible y coherente, lo cual es fundamental para mantener la calidad del software, facilitar la colaboración entre desarrolladores y asegurar la mantenibilidad del microservicio a largo plazo.

### Principales Reglas de PEP 8

A continuación, se resumen las recomendaciones más relevantes:

- **Indentación**: Se deben usar 4 espacios por nivel de indentación.
- **Longitud de línea**: No debe exceder los 79 caracteres.
- **Espaciado**:
  - Usa espacios alrededor de los operadores (`=`, `+`, etc.).
  - Evita espacios innecesarios dentro de paréntesis, corchetes o llaves.
- **Nomenclatura**:
  - Variables y funciones: `snake_case`
  - Clases: `CamelCase`
  - Constantes: `MAYÚSCULAS_CON_GUIONES`
- **Estructura de imports**:
  1. Módulos estándar
  2. Módulos de terceros
  3. Módulos del proyecto
  - Separados por una línea en blanco y orden alfabético dentro de cada bloque.
- **Líneas en blanco**:
  - Dos líneas en blanco entre funciones o clases a nivel superior.
  - Una línea en blanco entre métodos de una clase.

Aplicar PEP 8 garantiza un código más limpio, comprensible y estandarizado, independientemente del desarrollador que lo escriba o lea.

---

### Validación automática con Flake8

[Flake8](https://flake8.pycqa.org/en/latest/) es una herramienta de análisis estático que ayuda a verificar que el código cumple con las reglas definidas en PEP 8. Además, detecta errores comunes, código redundante y estructuras mal formateadas.

#### Instalación

```bash
pip install flake8
```

#### Uso básico

Para analizar todo el código del proyecto:

```bash
flake8 .
```

También se puede ejecutar sobre archivos específicos:

```bash
flake8 src/app.py
```

#### ⚙️ Configuración recomendada

Se recomienda incluir un archivo de configuración `.flake8` o agregar las reglas en `setup.cfg` o `pyproject.toml`. Ejemplo de `.flake8`:

```ini
[flake8]
max-line-length = 88
exclude =
    .git,
    __pycache__,
    venv,
    migrations
```

---

### Recomendación

Para mantener la calidad del código de este microservicio:

- Todo nuevo código debe respetar el estándar PEP 8.
- Se debe integrar **flake8** como parte del flujo de desarrollo, ya sea en pre-commits o como paso en la integración continua (CI).
- Se recomienda el uso de herramientas complementarias como **Black** (formateador automático) o **isort** (ordenador de imports), en conjunto con Flake8.

