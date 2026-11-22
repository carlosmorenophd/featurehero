# Data Model: Distribución pública de Feature Hero

Esta feature no agrega datos de negocio. Las entidades siguientes describen los
artefactos y estados de publicación que deben validarse.

## Distribución pública

- **Purpose**: Paquete instalable desde PyPI.
- **Fields**: nombre `featurehero`, versión, metadata, requisitos de Python,
  dependencias, entry point, wheel y source distribution.
- **Validation**: nombre y versión coinciden con `pyproject.toml`; ambos artefactos
  pasan validación y contienen el paquete `featurehero`.

## Versión publicada

- **Purpose**: Identificador único del código y artefactos aprobados.
- **Fields**: versión del proyecto, commit, tag, fecha, estado de publicación y
  URL de PyPI.
- **Lifecycle**: preparada → validada → publicada → instalada/verificada; una
  versión rechazada no se declara disponible.
- **Validation**: la versión instalada y `featurehero version` coinciden con la
  versión publicada.

## Proceso de publicación

- **Purpose**: Secuencia reproducible de build, validación, autorización, carga y release.
- **Fields**: workflow, evento de release, permisos, artefactos, resultado y logs.
- **Relationships**: produce una Distribución pública y actualiza una Versión publicada.
- **Security**: las credenciales se obtienen mediante una identidad de publicación
  protegida y no forman parte del código ni de los artefactos.

## Instalación pública

- **Purpose**: Estado verificable de un entorno sin el repositorio fuente.
- **Fields**: plataforma, versión Python, comando de instalación, versión instalada,
  resultado de `featurehero --help` y `featurehero version`.
- **Validation**: debe instalar dependencias y exponer el entry point sin pasos
  manuales adicionales fuera de la activación del entorno.

## Ruta documental

- **Purpose**: Instrucciones para usuarios finales y colaboradores.
- **Fields**: idioma, ruta pública, ruta desde fuente, ruta Poetry, requisitos,
  verificación, troubleshooting y enlaces.
- **Validation**: README y guía contienen las rutas equivalentes en español e inglés
  y no presentan la instalación desde fuente como requisito para usuarios finales.
