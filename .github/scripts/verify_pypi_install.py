#!/usr/bin/env python3
"""Install and smoke-test a published Feature Hero version in a clean venv."""

from __future__ import annotations

import argparse
import importlib.metadata
import os
import subprocess
import sys
import tempfile
import time
import venv
from pathlib import Path


def run(command: list[str], *, env: dict[str, str] | None = None) -> str:
    print(f"$ {' '.join(command)}")
    result = subprocess.run(command, check=True, text=True, capture_output=True, env=env)
    if result.stdout:
        print(result.stdout.strip())
    return result.stdout


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", required=True)
    parser.add_argument("--max-wait-seconds", type=int, default=300)
    parser.add_argument("--interval-seconds", type=int, default=15)
    args = parser.parse_args()

    deadline = time.monotonic() + args.max_wait_seconds
    while True:
        try:
            with tempfile.TemporaryDirectory(prefix="featurehero-pypi-") as directory:
                root = Path(directory)
                environment = root / "venv"
                venv.EnvBuilder(with_pip=True).create(environment)
                python = environment / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
                scripts = environment / ("Scripts" if os.name == "nt" else "bin")
                featurehero = scripts / ("featurehero.exe" if os.name == "nt" else "featurehero")
                run([str(python), "-m", "pip", "install", "--upgrade", "pip"])
                run([str(python), "-m", "pip", "install", f"featurehero=={args.version}"])
                installed = run([
                    str(python), "-c",
                    "import importlib.metadata; print(importlib.metadata.version('featurehero'))",
                ]).strip()
                if installed != args.version:
                    raise RuntimeError(f"Installed version {installed} != {args.version}")
                run([str(featurehero), "--help"])
                version_output = run([str(featurehero), "version"])
                if args.version not in version_output:
                    raise RuntimeError("featurehero version output does not contain the published version")
            print(f"PyPI installation verified for featurehero {args.version}")
            return 0
        except (subprocess.CalledProcessError, OSError, RuntimeError) as error:
            if time.monotonic() >= deadline:
                print(f"PyPI installation verification failed after {args.max_wait_seconds}s: {error}", file=sys.stderr)
                return 1
            print(f"PyPI version not ready; retrying in {args.interval_seconds}s: {error}")
            time.sleep(args.interval_seconds)


if __name__ == "__main__":
    raise SystemExit(main())
