# PyPI Release Contract

This contract defines the observable distribution and release behavior. It does
not prescribe credentials or alter the Feature Hero CLI.

## Public installation

| Action | Command | Expected result |
|---|---|---|
| Install | `python -m pip install featurehero` | PyPI resolves and installs the requested package and dependencies |
| Verify help | `featurehero --help` | The installed CLI prints usage and available actions |
| Verify version | `featurehero version` | The installed package version is printed |

## Distribution requirements

- The project name is `featurehero`.
- The distribution metadata declares Python `>=3.12,<4.0`.
- The distribution exposes `featurehero = "featurehero.main:main"`.
- The release contains a wheel and a source distribution when both are produced.
- The published version is unique and matches `pyproject.toml` and `featurehero version`.
- Runtime commands and public parameters remain unchanged.

## Release validation

Before publication, the release process must validate:

```bash
poetry check
poetry run pytest -q
poetry build
poetry run featurehero --help
poetry run featurehero version
```

After publication, a clean environment must install the package from the public
index and run the two CLI smoke checks without the repository source present.

## Publication security

The release workflow must use a protected publishing identity or equivalent
short-lived credentials. No PyPI token, password, or private credential may be
committed to the repository or embedded in a distribution artifact.
