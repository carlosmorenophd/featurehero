# Quickstart: Validate the PyPI Distribution

## Prerequisites

- A published version of `featurehero` on PyPI.
- A clean temporary directory outside the repository.
- Python `>=3.12,<4.0` and pip.
- Internet access.

## Build and pre-publication checks

From the repository root:

```bash
poetry check
poetry run pytest -q
poetry build
poetry run featurehero --help
poetry run featurehero version
```

Confirm that `dist/` contains the expected wheel and source distribution and that
their version matches `pyproject.toml`.

## Clean installation from PyPI

Create a clean environment outside the repository:

```bash
python3 -m venv /tmp/featurehero-pypi-check
source /tmp/featurehero-pypi-check/bin/activate
python -m pip install --upgrade pip
python -m pip install featurehero
featurehero --help
featurehero version
```

On Windows PowerShell:

```powershell
py -3.12 -m venv .pypi-check
.\.pypi-check\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install featurehero
featurehero --help
featurehero version
```

On Windows CMD:

```bat
py -3.12 -m venv .pypi-check
.pypi-check\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install featurehero
featurehero --help
featurehero version
```

The command must succeed without cloning or entering the Feature Hero repository.

## Release checks

1. Verify the version is new and matches `pyproject.toml`.
2. Verify package metadata, dependencies, entry point, wheel, and source distribution.
3. Verify the release workflow uses protected publication permissions and no committed secret.
4. Publish the approved artifacts to PyPI.
5. Repeat the clean installation on Windows PowerShell, Windows CMD, macOS, and Ubuntu/Debian.
6. Record version, platform, Python version, commands, result, and any exception in the release evidence.

## Expected outcomes

- `python -m pip install featurehero` succeeds in a clean compatible environment.
- `featurehero --help` and `featurehero version` work without the source repository.
- The reported version matches the published distribution.
- The existing CLI commands and parameters remain available.
- README and `INSTALLATION_GUIDE.md` identify the PyPI route as primary and source/Poetry routes as development alternatives.
