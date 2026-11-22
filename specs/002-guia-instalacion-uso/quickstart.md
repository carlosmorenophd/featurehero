# Quickstart: Validate the Installation and Usage Guide

## Prerequisites

- Repository checked out on branch `002-guia-instalacion-uso`.
- Windows, macOS, Ubuntu/Debian, or another Linux distribution for the relevant path.
- Python `>=3.12,<4.0` available from the platform's terminal.
- Internet access for repository and dependency downloads.

## Validation sequence

1. Follow `INSTALLATION_GUIDE.md` from platform selection without reading the
   technical README first.
2. Open `README.md` in Spanish and English. Verify that each language has an
   index and a visible link to the matching language section of the guide.
3. Open `INSTALLATION_GUIDE.md` in both languages. Verify that each index links
   to platform setup, installation, quickstart, troubleshooting and technical
   reference sections, and that every target heading exists.
4. Download or clone the repository and enter its root directory.
5. Create and activate the platform-specific isolated environment.
6. Install the local package:

   ```bash
   python -m pip install .
   ```

7. Verify the installed command:

   ```bash
   featurehero --help
   featurehero version
   ```

   Expected result: usage is displayed and the package version is printed.

8. Create the small CSV described by the guide and run the lightweight first-use example:

   ```bash
   featurehero transform --file data.csv --type log1p --columns feature --out processed.csv
   ```

   Expected result: `processed.csv` exists and contains transformed output.

9. Run the main flow with a valid dataset and reduced parameters documented by the guide:

   ```bash
   featurehero run --file data.csv --column target --params '{"number_generation": 10, "number_population": 10}'
   ```

   Expected result: the CLI accepts the dataset, reports progress or completion,
   and creates the documented workspace outputs.

10. Repeat the installation and first-use path on Windows PowerShell, Windows CMD,
   macOS, and Ubuntu/Debian. Record shell-specific corrections in troubleshooting.
11. Verify that every executable instruction has an observable success signal or
   recovery step, and that advanced details link to `README.md`.
12. Run the project checks:

    ```bash
    poetry check
    poetry run pytest
    poetry run featurehero --help
    poetry run featurehero version
    poetry build
    ```

## Acceptance evidence

- A reviewer can find the three platform paths, quickstart, and troubleshooting
  from guide navigation in under 30 seconds.
- The package installation command matches `pyproject.toml` and the repository README.
- `README.md` points to `INSTALLATION_GUIDE.md` in both languages.
- Both documents expose working language-specific indexes and equivalent internal destinations.
- No referenced dataset path is assumed to exist unless the guide creates or provides it.
- SC-001 through SC-006 can be assessed from walkthrough and review evidence.
