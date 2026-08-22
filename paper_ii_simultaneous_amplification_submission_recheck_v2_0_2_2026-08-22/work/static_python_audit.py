#!/usr/bin/env python3
"""Independent AST inventory for every delivered Python program."""

from __future__ import annotations

import ast
import pathlib


ROOT = pathlib.Path(__file__).resolve().parents[1] / "delivered_copy"
NETWORK_ROOTS = {"aiohttp", "ftplib", "http", "requests", "socket", "urllib", "webbrowser"}


def main() -> None:
    paths = sorted(ROOT.rglob("*.py"))
    if not paths:
        raise SystemExit("FAIL: no Python programs found")
    all_imports: set[str] = set()
    assertions: list[str] = []
    dynamic_execution: list[str] = []
    network_imports: list[str] = []

    for path in paths:
        relative = path.relative_to(ROOT)
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(relative))
        compile(tree, str(relative), "exec")
        local_imports: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Assert):
                assertions.append(f"{relative}:{node.lineno}")
            elif isinstance(node, ast.Import):
                local_imports.update(alias.name.split(".", 1)[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                local_imports.add(node.module.split(".", 1)[0])
            elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec", "compile"}:
                dynamic_execution.append(f"{relative}:{node.lineno}:{node.func.id}")
        all_imports.update(local_imports)
        for name in sorted(local_imports & NETWORK_ROOTS):
            network_imports.append(f"{relative}:{name}")
        print(f"{relative}: imports={','.join(sorted(local_imports)) or '(none)'}")

    if assertions:
        raise SystemExit("FAIL: bare assert statements: " + ", ".join(assertions))
    if dynamic_execution:
        raise SystemExit("FAIL: dynamic execution calls: " + ", ".join(dynamic_execution))
    if network_imports:
        raise SystemExit("FAIL: network-capable imports: " + ", ".join(network_imports))
    print(f"PASS: parsed and compiled {len(paths)} Python programs")
    print("PASS: no bare assert, dynamic execution, or network-capable import")
    print("IMPORT_ROOTS: " + ", ".join(sorted(all_imports)))


if __name__ == "__main__":
    main()
