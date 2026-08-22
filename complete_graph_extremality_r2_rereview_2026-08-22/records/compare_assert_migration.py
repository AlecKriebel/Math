#!/usr/bin/env python3
"""Statically compare R1 assertions with R2 fail-closed checks.

The delivered programs are parsed as text and are never imported or executed.
"""

from __future__ import annotations

import ast
from pathlib import Path


OLD = Path(
    "/Users/alec/Documents/Math/complete_graph_extremality_referee_audit_2026-08-22/"
    "work/package/source_and_certificates/universal_simultaneous_amplification"
)
NEW = Path(
    "/Users/alec/Documents/Math/complete_graph_extremality_r2_rereview_2026-08-22/"
    "work/package/source_and_certificates/universal_simultaneous_amplification"
)


def dump(node: ast.AST) -> str:
    return ast.dump(node, annotate_fields=True, include_attributes=False)


def assertion_conditions(tree: ast.AST) -> list[str]:
    return [dump(node.test) for node in ast.walk(tree) if isinstance(node, ast.Assert)]


def require_conditions(tree: ast.AST) -> list[str]:
    conditions = []
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "require"
        ):
            if not node.args:
                raise RuntimeError("require call has no condition")
            conditions.append(dump(node.args[0]))
    return conditions


def main() -> None:
    migrated_files = 0
    migrated_checks = 0
    for old_path in sorted(OLD.rglob("*.py")):
        relative = old_path.relative_to(OLD)
        new_path = NEW / relative
        if not new_path.is_file():
            continue
        old_tree = ast.parse(old_path.read_text(encoding="utf-8"), filename=str(old_path))
        old_conditions = assertion_conditions(old_tree)
        if not old_conditions:
            continue
        new_tree = ast.parse(new_path.read_text(encoding="utf-8"), filename=str(new_path))
        new_assertions = assertion_conditions(new_tree)
        new_conditions = require_conditions(new_tree)
        if new_assertions:
            raise RuntimeError(f"R2 still has bare assertions in {relative}")
        if old_conditions != new_conditions:
            raise RuntimeError(
                f"ordered check conditions changed in {relative}: "
                f"R1={len(old_conditions)} R2={len(new_conditions)}"
            )
        migrated_files += 1
        migrated_checks += len(old_conditions)
        print(f"PASS {relative}: {len(old_conditions)} conditions preserved")
    if migrated_files != 20 or migrated_checks != 406:
        raise RuntimeError(
            f"unexpected migration inventory: files={migrated_files}, "
            f"conditions={migrated_checks}"
        )
    print(
        f"PASS: all {migrated_checks} R1 assertion conditions in "
        f"{migrated_files} files are identical R2 require conditions"
    )


if __name__ == "__main__":
    main()
