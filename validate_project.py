"""Lightweight offline checks for source files and the notebook."""

from __future__ import annotations

import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main() -> int:
    failures: list[str] = []
    for path in sorted(ROOT.glob("*.py")):
        try:
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except SyntaxError as exc:
            failures.append(f"{path}: {exc}")

    notebook = ROOT / "SHEGLAM_WEB_SCRAPING.ipynb"
    try:
        json.loads(notebook.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        failures.append(f"{notebook}: {exc}")

    if failures:
        print("Validation failed:")
        print("\n".join(failures))
        return 1
    print("AST and notebook JSON validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
