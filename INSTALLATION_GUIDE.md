# Feature Hero — Installation and Usage Guide

> **Español** | [English](#english)

This guide is written for people who are new to command-line tools. It complements
the complete bilingual [README](README.md): use the guide for a step-by-step path
and the README for the full technical reference.

<a id="espanol"></a>

## Español

### Índice

- [Antes de comenzar](#es-antes-de-comenzar)
- [Windows](#es-windows)
- [macOS](#es-macos)
- [Ubuntu/Debian](#es-ubuntudebian)
- [Otras distribuciones Linux](#es-otras-distribuciones-linux)
- [Inicio rápido](#es-inicio-rápido)
- [Solución de problemas](#es-solución-de-problemas)
- [Desarrollo con Poetry](#es-desarrollo-con-poetry)
- [Referencia técnica](#es-referencia-técnica)
- [English](#english)
- [README en español](README.md#feature-hero)

### <a id="es-antes-de-comenzar"></a>Antes de comenzar

La ruta principal para usuarios finales es PyPI; no necesitas descargar el
repositorio. Necesitas:

- Python `>=3.12,<4.0`.
- Acceso a Internet para descargar el paquete y sus dependencias.
- Un terminal: PowerShell o CMD en Windows, Terminal en macOS, o una terminal
  compatible en Linux.

Instalación pública:

```bash
python -m pip install featurehero
featurehero --help
featurehero version
```

La ruta desde el repositorio y Poetry que aparece más abajo es únicamente para
desarrollo y contribución.

### <a id="es-windows"></a>Windows

#### Instalación pública desde PyPI

```powershell
py -3.12 -m pip install featurehero
featurehero --help
featurehero version
```

#### 1. Descargar el repositorio

Instala Git si aún no lo tienes y ejecuta en PowerShell o CMD:

```text
git clone https://github.com/carlosmorenophd/featurehero.git
cd featurehero
```

También puedes descargar el repositorio como ZIP, descomprimirlo y abrir el
terminal dentro de la carpeta que contiene `pyproject.toml`.

#### 2. Comprobar Python

En PowerShell o CMD:

```text
py -3.12 --version
```

Debes ver Python 3.12 o una versión compatible dentro de `>=3.12,<4.0`.

#### 3. Crear y activar el entorno virtual

En PowerShell:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Si PowerShell bloquea la activación, consulta [Solución de problemas](#es-solución-de-problemas).

En CMD:

```bat
py -3.12 -m venv .venv
.venv\Scripts\activate.bat
```

Cuando el entorno está activo, normalmente aparece `(.venv)` al principio de
la línea del terminal.

#### 4. Instalar Feature Hero

Desde la raíz del repositorio y con el entorno activo:

```text
python -m pip install .
```

La instalación termina correctamente cuando pip no muestra un error.

#### 5. Verificar la instalación

```text
featurehero --help
featurehero version
```

Debes ver la ayuda del CLI y la versión instalada.

### <a id="es-macos"></a>macOS

Con Homebrew instalado, ejecuta `brew install libomp` antes de usar
Feature Hero. XGBoost necesita esta biblioteca en macOS. Comprueba
la instalación con `brew list --versions libomp`.

#### Instalación pública desde PyPI

```bash
python3 -m pip install featurehero
featurehero --help
featurehero version
```

#### 1. Descargar el repositorio

```bash
git clone https://github.com/carlosmorenophd/featurehero.git
cd featurehero
```

También puedes descargar y descomprimir el ZIP del repositorio.

#### 2. Comprobar Python

```bash
python3 --version
```

Instala Python 3.12 o una versión compatible si el comando no existe o muestra
una versión anterior.

#### 3. Crear y activar el entorno virtual

```bash
python3 -m venv .venv
source .venv/bin/activate
```

El terminal normalmente muestra `(.venv)` mientras el entorno está activo.

#### 4. Instalar y verificar

```bash
python -m pip install .
featurehero --help
featurehero version
```

### <a id="es-ubuntudebian"></a>Ubuntu/Debian

#### Instalación pública desde PyPI

```bash
python3 -m pip install featurehero
featurehero --help
featurehero version
```

#### 1. Instalar requisitos del sistema

Actualiza los índices e instala Python, el entorno virtual y Git:

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip git
```

Comprueba que Python cumple `>=3.12,<4.0`:

```bash
python3 --version
```

#### 2. Descargar, instalar y verificar

```bash
git clone https://github.com/carlosmorenophd/featurehero.git
cd featurehero
python3 -m venv .venv
source .venv/bin/activate
python -m pip install .
featurehero --help
featurehero version
```

### <a id="es-otras-distribuciones-linux"></a>Otras distribuciones Linux

La ruta validada paso a paso es Ubuntu/Debian. En otra distribución debes
instalar Python `>=3.12,<4.0`, el módulo de entornos virtuales, pip y Git con el
gestor de paquetes de tu distribución. Después utiliza:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install .
featurehero --help
featurehero version
```

Estas instrucciones son orientación general y no certifican una distribución
que no haya sido registrada en [validation-evidence.md](specs/002-guia-instalacion-uso/validation-evidence.md).

### <a id="es-inicio-rápido"></a>Inicio rápido

Con el entorno activo, crea un archivo llamado `data.csv` con este contenido:

```csv
feature,feature2,target
1,20,10
2,19,20
3,18,30
4,17,40
5,16,50
6,15,60
7,14,70
8,13,80
9,12,90
10,11,100
11,10,110
12,9,120
13,8,130
14,7,140
15,6,150
16,5,160
17,4,170
18,3,180
19,2,190
20,1,200
```

Prueba primero una transformación sencilla:

```bash
featurehero transform --file data.csv --type log1p --columns feature --out processed.csv
```

Debes encontrar `processed.csv` en la carpeta actual.

Para ejecutar la optimización con un ejemplo pequeño:

En PowerShell:

```powershell
featurehero run --file data.csv --column target --params '{\"number_generation\": 10, \"number_population\": 10, \"machines\": [\"lasso_regression\"]}'
```

En CMD:

```cmd
featurehero run --file data.csv --column target --params "{\"number_generation\": 10, \"number_population\": 10, \"machines\": [\"lasso_regression\"]}"
```

En macOS o Linux:

```text
featurehero run --file data.csv --column target --params '{"number_generation": 10, "number_population": 10, "machines": ["lasso_regression"]}'
```

El comando debe aceptar el dataset, mostrar progreso o finalización y crear el
workspace documentado junto al archivo de entrada. Si el JSON produce un error
de comillas, comprueba que estés usando la variante correspondiente a tu shell
o ejecuta primero `featurehero run --help`.

Consulta el [README en español](README.md#optimizacion) para formatos, modelos,
métricas, análisis de resultados y jobs.

### <a id="es-solución-de-problemas"></a>Solución de problemas

#### `python`, `python3` o `py` no se reconoce

Instala Python 3.12 o agrega Python al PATH. En Windows prueba `py -3.12`; en
macOS y Linux prueba `python3`.

#### `featurehero` no se reconoce

Confirma que el entorno virtual está activo, vuelve a ejecutar `python -m pip install .`
desde la raíz del repositorio y prueba `featurehero --help`.

#### PowerShell bloquea `Activate.ps1`

Usa CMD con `.venv\Scripts\activate.bat`, o revisa la política de ejecución de
PowerShell de tu equipo antes de volver a ejecutar:

```powershell
.\.venv\Scripts\Activate.ps1
```

#### No tienes permisos para instalar

Trabaja en una carpeta de usuario, no dentro de una carpeta protegida del
sistema. No uses `sudo pip install` para instalar el paquete en el entorno virtual.

#### El archivo o la columna no existe

Comprueba la ruta desde la carpeta actual, el nombre exacto del archivo y el
nombre exacto de la columna. Usa comillas si una ruta o columna contiene espacios.

#### El dataset no es válido

`run` necesita un target numérico mayor que cero y columnas predictoras numéricas.
Los formatos aceptados son `.csv`, `.xls`, `.xlsx` y `.numbers`.

#### Necesitas más ayuda

Guarda el comando ejecutado, el mensaje completo, tu sistema operativo y la
versión mostrada por `featurehero version`. Después consulta el [README en
español](README.md#referencia-tecnica) y reporta el problema con esa información.

### <a id="es-desarrollo-con-poetry"></a>Desarrollo con Poetry

Poetry es opcional y está destinado al desarrollo del proyecto:

```bash
poetry install
poetry run featurehero --help
poetry run pytest
poetry build
```

No necesitas Poetry para seguir la instalación básica con `pip install .`.

### <a id="es-referencia-técnica"></a>Referencia técnica

El [README en español](README.md#feature-hero) contiene la referencia completa
de comandos, transformaciones, optimización, análisis de resultados, jobs,
artefactos, desarrollo y release. Usa sus índices para saltar directamente a la
sección que necesitas.

## English

### Table of contents

- [Before you start](#en-before-you-start)
- [Windows](#en-windows)
- [macOS](#en-macos)
- [Ubuntu/Debian](#en-ubuntudebian)
- [Other Linux distributions](#en-other-linux-distributions)
- [Quickstart](#en-quickstart)
- [Troubleshooting](#en-troubleshooting)
- [Development with Poetry](#en-development-with-poetry)
- [Technical reference](#en-technical-reference)
- [Español](#espanol)
- [English README](README.md#english)

### <a id="en-before-you-start"></a>Before you start

End users should install Feature Hero from PyPI; downloading the repository is
only required for development. You need:

- Python `>=3.12,<4.0`.
- Internet access to download the package and dependencies.
- A terminal: PowerShell or CMD on Windows, Terminal on macOS, or a compatible
  terminal on Linux.

Public installation:

```bash
python -m pip install featurehero
featurehero --help
featurehero version
```

The repository and Poetry route below is for development and contribution only.

### <a id="en-windows"></a>Windows

#### Public installation from PyPI

```powershell
py -3.12 -m pip install featurehero
featurehero --help
featurehero version
```

#### 1. Download the repository

Install Git if needed and run in PowerShell or CMD:

```text
git clone https://github.com/carlosmorenophd/featurehero.git
cd featurehero
```

You can also download the repository as a ZIP, extract it, and open the terminal
inside the folder containing `pyproject.toml`.

#### 2. Check Python

```text
py -3.12 --version
```

The output must show Python 3.12 or another version compatible with `>=3.12,<4.0`.

#### 3. Create and activate the virtual environment

PowerShell:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

CMD:

```bat
py -3.12 -m venv .venv
.venv\Scripts\activate.bat
```

When the environment is active, `(.venv)` usually appears at the beginning of
the terminal line.

#### 4. Install Feature Hero

From the repository root and with the environment active:

```text
python -m pip install .
```

The installation is successful when pip finishes without an error.

#### 5. Verify the installation

```text
featurehero --help
featurehero version
```

The CLI help and installed package version should be displayed.

### <a id="en-macos"></a>macOS

With Homebrew installed, run `brew install libomp` before using
Feature Hero. XGBoost needs this library on macOS. Verify the
installation with `brew list --versions libomp`.

#### Public installation from PyPI

```bash
python3 -m pip install featurehero
featurehero --help
featurehero version
```

```bash
git clone https://github.com/carlosmorenophd/featurehero.git
cd featurehero
python3 --version
python3 -m venv .venv
source .venv/bin/activate
python -m pip install .
featurehero --help
featurehero version
```

Install Python 3.12 or another compatible version if `python3` is missing or too old.

### <a id="en-ubuntudebian"></a>Ubuntu/Debian

#### Public installation from PyPI

```bash
python3 -m pip install featurehero
featurehero --help
featurehero version
```

Install the system requirements:

```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip git
```

Check that Python meets `>=3.12,<4.0`:

```bash
python3 --version
```

Then download, install, and verify:

```bash
git clone https://github.com/carlosmorenophd/featurehero.git
cd featurehero
python3 -m venv .venv
source .venv/bin/activate
python -m pip install .
featurehero --help
featurehero version
```

### <a id="en-other-linux-distributions"></a>Other Linux distributions

Ubuntu/Debian is the step-by-step validated Linux path. On another distribution,
install Python `>=3.12,<4.0`, its virtual-environment module, pip, and Git using
the distribution's package manager. Then run:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install .
featurehero --help
featurehero version
```

These instructions are general guidance and do not certify a distribution that
has not been recorded in [validation-evidence.md](specs/002-guia-instalacion-uso/validation-evidence.md).

### <a id="en-quickstart"></a>Quickstart

With the environment active, create `data.csv` with:

```csv
feature,feature2,target
1,20,10
2,19,20
3,18,30
4,17,40
5,16,50
6,15,60
7,14,70
8,13,80
9,12,90
10,11,100
11,10,110
12,9,120
13,8,130
14,7,140
15,6,150
16,5,160
17,4,170
18,3,180
19,2,190
20,1,200
```

Run a lightweight transformation:

```bash
featurehero transform --file data.csv --type log1p --columns feature --out processed.csv
```

`processed.csv` should appear in the current directory.

Run the main flow with a small example:

In PowerShell:

```powershell
featurehero run --file data.csv --column target --params '{\"number_generation\": 10, \"number_population\": 10, \"machines\": [\"lasso_regression\"]}'
```

In CMD:

```cmd
featurehero run --file data.csv --column target --params "{\"number_generation\": 10, \"number_population\": 10, \"machines\": [\"lasso_regression\"]}"
```

In macOS or Linux:

```text
featurehero run --file data.csv --column target --params '{"number_generation": 10, "number_population": 10, "machines": ["lasso_regression"]}'
```

The command should accept the dataset, report progress or completion, and create
the documented workspace next to the input file. For command details, see the
[English README](README.md#english-optimization).

### <a id="en-troubleshooting"></a>Troubleshooting

#### `python`, `python3`, or `py` is not recognized

Install Python 3.12 or add Python to PATH. On Windows try `py -3.12`; on macOS
and Linux try `python3`.

#### `featurehero` is not recognized

Confirm the virtual environment is active, run `python -m pip install .` again
from the repository root, and retry `featurehero --help`.

#### PowerShell blocks `Activate.ps1`

Use CMD with `.venv\Scripts\activate.bat`, or review your system's PowerShell
execution policy before retrying:

```powershell
.\.venv\Scripts\Activate.ps1
```

#### You do not have permission to install

Work in a user-owned folder rather than a protected system folder. Do not use
`sudo pip install` to install into the virtual environment.

#### The file or column does not exist

Check the path from the current directory, the exact file name, and the exact
column name. Quote paths or column names containing spaces.

#### The dataset is invalid

`run` requires a numeric target greater than zero and numeric predictor columns.
Accepted formats are `.csv`, `.xls`, `.xlsx`, and `.numbers`.

#### You need more help

Save the command, complete error message, operating system, and output of
`featurehero version`. Then consult the [English technical reference](README.md#english-technical-reference)
and report the issue with that information.

### <a id="en-development-with-poetry"></a>Development with Poetry

Poetry is optional and intended for project development:

```bash
poetry install
poetry run featurehero --help
poetry run pytest
poetry build
```

Poetry is not required for the basic `pip install .` installation path.

### <a id="en-technical-reference"></a>Technical reference

The [English README](README.md#english) contains the complete reference for
commands, transformations, optimization, result analysis, jobs, artifacts,
development, and releases. Use its table of contents to jump to the section you need.
