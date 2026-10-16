"""Execute a current script while measuring actual mandatory guard evaluations."""
import ast
import contextlib
import hashlib
import io
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True


def main():
    if len(sys.argv) != 3:
        raise RuntimeError("usage: run_checked.py script expected_runtime_count")
    path = Path(sys.argv[1]).resolve()
    expected = int(sys.argv[2])
    text = path.read_text(encoding="utf-8")
    tree = ast.parse(text)
    nodes = [n for n in ast.walk(tree) if isinstance(n, ast.If)
             and len(n.body) == 1 and isinstance(n.body[0], ast.Raise)
             and isinstance(n.body[0].exc, ast.Call)
             and isinstance(n.body[0].exc.func, ast.Name)
             and n.body[0].exc.func.id == "AssertionError"
             and n.body[0].exc.args
             and isinstance(n.body[0].exc.args[0], ast.Constant)
             and str(n.body[0].exc.args[0].value).startswith("mandatory checkpoint ")]
    counts = {n.body[0].exc.args[0].value: 0 for n in nodes}
    if "__record_mandatory" in text:
        raise RuntimeError("reserved instrumentation name collision")

    def record(label, predicate):
        counts[label] += 1
        return predicate

    # A line tracer overcounts multiline expressions because Python revisits
    # their first line. Wrap the original predicate instead: evaluate it once,
    # record that completed evaluation, return its original value unchanged,
    # then let the original `not` perform the original truth conversion.
    for node in nodes:
        if not isinstance(node.test, ast.UnaryOp) or not isinstance(node.test.op, ast.Not):
            raise RuntimeError("unexpected mandatory guard form")
        node.test.operand = ast.Call(
            func=ast.Name(id="__record_mandatory", ctx=ast.Load()),
            args=[ast.Constant(value=node.body[0].exc.args[0].value), node.test.operand],
            keywords=[])
    ast.fix_missing_locations(tree)

    captured = io.StringIO()
    with contextlib.redirect_stdout(captured):
        exec(compile(tree, str(path), "exec"),
             {"__name__": "__main__", "__file__": str(path), "__record_mandatory": record})
    if sum(counts.values()) != expected or not counts or any(count < 1 for count in counts.values()):
        raise RuntimeError("mandatory runtime checkpoint count mismatch: " + str(counts))
    stdout = captured.getvalue()
    print(json.dumps({"runtime_checkpoints": sum(counts.values()),
                      "static_checkpoints_reached": len(counts),
                      "checkpoint_evaluation_counts": counts,
                      "stdout_sha256": hashlib.sha256(stdout.encode()).hexdigest(),
                      "stdout": stdout}, sort_keys=True))


if __name__ == "__main__":
    main()
