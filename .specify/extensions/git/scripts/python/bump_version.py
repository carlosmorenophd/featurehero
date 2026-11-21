#!/usr/bin/env python3
"""Advance the repository CalVer profile YYYY.SSS.NNNNN before a commit."""
from __future__ import annotations

import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path


VERSION_PATTERN = re.compile(r"^(\d{4})\.(\d{3})\.(\d{5})$")
BRANCH_PATTERN = re.compile(r"(?:^|/)(\d{3})-")


def repository_root() -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        check=True,
        capture_output=True,
        text=True,
    )
    return Path(result.stdout.strip())


def feature_number(root: Path) -> str:
    branch = subprocess.run(
        ["git", "branch", "--show-current"],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    match = BRANCH_PATTERN.search(branch)
    if match:
        return match.group(1)
    features = sorted((root / "specs").glob("[0-9][0-9][0-9]-*"))
    if len(features) == 1:
        return features[0].name[:3]
    raise RuntimeError(f"Cannot determine the three-digit feature number from branch: {branch}")


def next_version(root: Path) -> str:
    year = datetime.now(timezone.utc).year
    spec = feature_number(root)
    path = root / "version"
    current = path.read_text(encoding="utf-8").strip() if path.exists() else ""
    match = VERSION_PATTERN.fullmatch(current)
    patch = int(match.group(3)) + 1 if match and match.group(1) == str(year) and match.group(2) == spec else 1
    if patch > 99999:
        raise RuntimeError("Version counter exceeded 99999")
    return f"{year}.{spec}.{patch:05d}"


def main() -> int:
    root = repository_root()
    (root / "version").write_text(next_version(root) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
