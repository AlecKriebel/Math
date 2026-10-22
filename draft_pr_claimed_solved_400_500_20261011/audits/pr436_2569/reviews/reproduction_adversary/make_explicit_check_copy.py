#!/usr/bin/env python3
"""Generate separate optimization-safe copies; never edit frozen scripts."""
import ast
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
CASE = HERE.parents[1]
SOURCE = CASE / "source_snapshot/unsolved_math_prioritization/attempts/2569"
REPAIRED = HERE / "repaired_verification"


class ExplicitChecks(ast.NodeTransformer):
    def __init__(self, source_name):
        self.source_name = source_name
        self.changed = []

    def visit_Assert(self, node):
        # Normal assert semantics: evaluate the test once; message only on failure.
        message = node.msg or ast.Constant(
            f"Verification failed at frozen source {self.source_name}:{node.lineno}")
        replacement = ast.If(
            test=ast.UnaryOp(op=ast.Not(), operand=node.test),
            body=[ast.Raise(exc=ast.Call(func=ast.Name(id="AssertionError", ctx=ast.Load()),
                                        args=[message], keywords=[]), cause=None)],
            orelse=[])
        self.changed.append({"source_line": node.lineno,
                             "test_ast": ast.dump(node.test, include_attributes=False)})
        return ast.copy_location(replacement, node)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    rows = []
    for original in sorted(SOURCE.rglob("*.py")):
        relative = str(original.relative_to(SOURCE))
        raw = original.read_bytes()
        tree = ast.parse(raw.decode())
        transformation = ExplicitChecks(relative)
        transformed = transformation.visit(tree)
        ast.fix_missing_locations(transformed)
        repaired_bytes = (ast.unparse(transformed) + "\n").encode()
        repaired_tree = ast.parse(repaired_bytes.decode())
        if any(isinstance(node, ast.Assert) for node in ast.walk(repaired_tree)):
            raise RuntimeError("Assertion survived explicit-check transformation")
        compile(repaired_bytes, relative, "exec", optimize=1)
        output = REPAIRED / relative
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(repaired_bytes)
        rows.append({"path": relative, "source_sha256": sha(raw),
                     "repaired_sha256": sha(repaired_bytes),
                     "replaced_assert_count": len(transformation.changed),
                     "replaced_assertions": transformation.changed})
        if original.read_bytes() != raw:
            raise RuntimeError("Frozen input changed")
    count = sum(row["replaced_assert_count"] for row in rows)
    if count != 82:
        raise RuntimeError(f"Unexpected assertion count {count}")
    result = {"generated_utc": datetime.now(timezone.utc).isoformat(),
              "change_scope": "Replace assert tests by explicit if-not/raise checks; AST unparse reformats code.",
              "proof_search_turns_added": 0, "frozen_original_bytes_edited": False,
              "source_assertions_replaced": count, "remaining_assertions": 0,
              "scripts": rows,
              "frozen_noncode_inputs": {str(p.relative_to(SOURCE)): sha(p.read_bytes())
                                        for p in sorted(SOURCE.rglob("*"))
                                        if p.is_file() and p.suffix != ".py"}}
    (REPAIRED / "REPAIR_PROVENANCE.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"generated_scripts": len(rows), "explicit_checks": count,
                      "remaining_asserts": 0, "frozen_bytes_edited": False}))


if __name__ == "__main__":
    main()
