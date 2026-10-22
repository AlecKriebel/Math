#!/usr/bin/env python3
"""Make a retained review program's verification guards survive python -O.

Only assert statements are changed. Evaluation order and failure conditions are
preserved. This is packaging hardening, not a change to mathematical checks.
"""
import argparse
import ast
import hashlib
import json
from pathlib import Path


class ExplicitGuards(ast.NodeTransformer):
    def __init__(self):
        self.count = 0

    def visit_Assert(self, node):
        self.count += 1
        message = node.msg or ast.Constant(f"verification failed at original line {node.lineno}")
        return ast.copy_location(ast.If(
            test=ast.UnaryOp(op=ast.Not(), operand=node.test),
            body=[ast.Raise(exc=ast.Call(func=ast.Name(id="AssertionError", ctx=ast.Load()),
                                      args=[message], keywords=[]), cause=None)],
            orelse=[]), node)


def convert(source):
    tree = ast.parse(source)
    transform = ExplicitGuards()
    tree = transform.visit(tree)
    ast.fix_missing_locations(tree)
    if any(isinstance(n, ast.Assert) for n in ast.walk(tree)):
        raise RuntimeError("An assertion remained after conversion")
    return ast.unparse(tree) + "\n", transform.count


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    raw = args.input.read_bytes()
    guarded, count = convert(raw.decode())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(guarded)
    print(json.dumps({"source": str(args.input), "output": str(args.output),
                      "source_sha256": hashlib.sha256(raw).hexdigest(),
                      "output_sha256": hashlib.sha256(guarded.encode()).hexdigest(),
                      "asserts_replaced": count}))


if __name__ == "__main__":
    main()
