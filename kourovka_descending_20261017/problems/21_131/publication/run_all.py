#!/usr/bin/env python3
"""Reproduce finite supplements; this is not a certificate of the theorem."""
if not __debug__:
    raise SystemExit("Run without -O or PYTHONOPTIMIZE: the evaluators require assertions.")

from contextlib import redirect_stdout
import io
import json
from pathlib import Path
import runpy

HERE = Path(__file__).resolve().parent


def evaluate():
    def load(name):
        return runpy.run_path(str(HERE / "lib" / name))
    tree = load("tree_sections.py")
    cases = [(2, (1,), 3, 8), (2, (1, 2), 6, 10),
             (3, (2,), 1, 5), (3, (1,), 3, 6), (5, (1,), 3, 5)]
    sections = [tree["check_sections"](*case) for case in cases]
    count = sum(item["generator_word_checks"] for item in sections)
    assert count == 11778
    closures = [tree["group_order"](2, (1,), depth) for depth in range(1, 9)]
    assert closures == [2, 8, 16, 16, 32, 32, 32, 32]
    assert tree["word_action"]((1, 0), 2, 1) == (1, 1)
    assert tree["word_action"]((0,), 2, 1, shift=1) == (0,)
    author = load("finite_levels.py")["verify"]()
    noncomm = load("noncommutative.py")
    with redirect_stdout(io.StringIO()):
        named = sum(noncomm["check"](p) for p in (2, 3, 5))
    assert named == 63
    wreath = load("wreath_augmentation.py")
    augmentation = [wreath["check_prime"](p) for p in (2, 3)]
    fresh = load("fresh_independent.py")
    # Compare serialized results canonically: tuples become JSON arrays and
    # integer dictionary keys become strings in the archived checkpoint.
    fresh_tree = json.loads(json.dumps(fresh["tree_checks"]()))
    fresh_algebra = [fresh["algebra_checks"](p) for p in (2, 3, 5)]
    assert sum(item["comparisons"] for item in fresh_tree) == 348516
    assert sum(item["exact_assertions"] for item in fresh_algebra) == 3516
    return {"status": "all finite assertions passed", "section_checks": count,
            "binary_single_generator_orders": closures,
            "construction_family": author, "named_matrix_checks": named,
            "wreath_augmentation": augmentation,
            "fresh_tree": fresh_tree, "fresh_algebra": fresh_algebra,
            "limits": "Finite supplements only; the paper supplies the infinite proofs and cites external theorems."}


def main():
    result = evaluate()
    expected = HERE / "expected_results.json"
    if expected.exists() and result != json.loads(expected.read_text()):
        raise RuntimeError("Reproduction differs from the packaged expected results")
    (HERE / "latest_results.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": result["status"], "section_checks": result["section_checks"],
                      "named_matrix_checks": result["named_matrix_checks"],
                      "fresh_tree_comparisons": sum(x["comparisons"] for x in result["fresh_tree"]),
                      "fresh_algebra_assertions": sum(x["exact_assertions"] for x in result["fresh_algebra"])}, indent=2))


if __name__ == "__main__":
    main()
