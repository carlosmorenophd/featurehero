#!/usr/bin/env python3
"""Validate Feature Hero distribution metadata and release artifacts."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tarfile
import tomllib
import urllib.error
import urllib.request
import zipfile
from email.parser import Parser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PYPROJECT = ROOT / "pyproject.toml"
DIST = ROOT / "dist"
EXPECTED_NAME = "featurehero"
EXPECTED_PYTHON = ">=3.12,<4.0"
EXPECTED_ENTRY_POINT = "featurehero = featurehero.main:main"


def fail(message: str) -> None:
    raise RuntimeError(message)


def load_project() -> tuple[str, dict[str, object]]:
    with PYPROJECT.open("rb") as handle:
        project = tomllib.load(handle)["project"]
    name = project["name"]
    if name != EXPECTED_NAME:
        fail(f"Expected project name {EXPECTED_NAME!r}, found {name!r}")
    if project["requires-python"] != EXPECTED_PYTHON:
        fail(f"Expected requires-python {EXPECTED_PYTHON!r}")
    scripts = project.get("scripts", {})
    if scripts.get(EXPECTED_NAME) != "featurehero.main:main":
        fail("The featurehero console entry point is missing or incorrect")
    return project["version"], project


def run(command: list[str]) -> None:
    print(f"$ {' '.join(command)}")
    subprocess.run(command, cwd=ROOT, check=True)


def project_dependency_names(project: dict[str, object]) -> set[str]:
    dependencies = project.get("dependencies", [])
    return {
        re.split(r"[ (<>=!~;]", dependency, maxsplit=1)[0].lower().replace("_", "-")
        for dependency in dependencies
    }


def metadata_from_wheel(path: Path) -> tuple[object, set[str], str]:
    with zipfile.ZipFile(path) as archive:
        metadata_name = next(
            name for name in archive.namelist() if name.endswith(".dist-info/METADATA")
        )
        metadata = Parser().parsestr(archive.read(metadata_name).decode())
        entry_points = next(
            name for name in archive.namelist() if name.endswith(".dist-info/entry_points.txt")
        )
        entry_text = archive.read(entry_points).decode()
    requirements = {
        re.split(r"[ (<>=!~;]", value, maxsplit=1)[0].lower().replace("_", "-")
        for value in metadata.get_all("Requires-Dist", [])
    }
    return metadata, requirements, entry_text


def metadata_from_sdist(path: Path) -> tuple[object, set[str]]:
    with tarfile.open(path, "r:gz") as archive:
        info = next(member for member in archive.getmembers() if member.name.endswith("/PKG-INFO"))
        metadata = Parser().parsestr(archive.extractfile(info).read().decode())
    requirements = {
        re.split(r"[ (<>=!~;]", value, maxsplit=1)[0].lower().replace("_", "-")
        for value in metadata.get_all("Requires-Dist", [])
    }
    return metadata, requirements


def validate_artifacts(version: str, expected_dependencies: set[str]) -> None:
    wheels = sorted(DIST.glob(f"*{version}*.whl"))
    sdists = sorted(DIST.glob(f"*{version}*.tar.gz"))
    if len(wheels) != 1:
        fail(f"Expected exactly one wheel, found {len(wheels)}")
    if len(sdists) != 1:
        fail(f"Expected exactly one source distribution, found {len(sdists)}")

    wheel_metadata, wheel_dependencies, entry_points = metadata_from_wheel(wheels[0])
    sdist_metadata, sdist_dependencies = metadata_from_sdist(sdists[0])
    for metadata, label in ((wheel_metadata, "wheel"), (sdist_metadata, "sdist")):
        if metadata["Name"].lower() != EXPECTED_NAME:
            fail(f"Invalid package name in {label}")
        if metadata["Version"] != version:
            fail(f"Version mismatch in {label}: {metadata['Version']} != {version}")
        if metadata["Requires-Python"] != EXPECTED_PYTHON:
            fail(f"Python requirement mismatch in {label}")
    if "featurehero=featurehero.main:main" not in entry_points.replace(" ", ""):
        fail("The wheel does not expose featurehero = featurehero.main:main")
    if wheel_dependencies != expected_dependencies or sdist_dependencies != expected_dependencies:
        fail("Packaged dependencies do not match pyproject.toml")
    print(f"Validated {wheels[0].name} and {sdists[0].name} for version {version}")


def ensure_version_not_published(version: str) -> None:
    url = f"https://pypi.org/pypi/{EXPECTED_NAME}/json"
    request = urllib.request.Request(url, headers={"User-Agent": "featurehero-release-validator"})
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            releases = json.load(response).get("releases", {})
    except urllib.error.HTTPError as error:
        if error.code == 404:
            print("PyPI project does not exist yet; first publication is allowed")
            return
        raise RuntimeError(f"Unable to query PyPI: HTTP {error.code}") from error
    except urllib.error.URLError as error:
        raise RuntimeError(f"Unable to query PyPI: {error.reason}") from error
    if version in releases:
        fail(f"Version {version} already exists on PyPI")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-preflight", action="store_true")
    parser.add_argument("--check-pypi", action="store_true")
    args = parser.parse_args()
    try:
        version, project = load_project()
        if args.run_preflight:
            run(["poetry", "check"])
            run(["poetry", "run", "pytest", "-q"])
            run(["poetry", "build"])
            run(["poetry", "run", "featurehero", "--help"])
            run(["poetry", "run", "featurehero", "version"])
        validate_artifacts(version, project_dependency_names(project))
        if args.check_pypi:
            ensure_version_not_published(version)
    except (RuntimeError, KeyError, StopIteration, OSError, subprocess.CalledProcessError) as error:
        print(f"Release validation failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
