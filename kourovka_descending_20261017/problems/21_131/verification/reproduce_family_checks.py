#!/usr/bin/env python3
"""Root reproduction of independent family computations, standard library only.

These checks supplement the infinite proofs. They do not certify either the
external embedding theorem, universal group embeddings, or originality.
"""
from contextlib import redirect_stdout
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path
import runpy


ROOT = Path(__file__).resolve().parents[1]


def load(relative):
    path = ROOT / relative
    data = path.read_bytes()
    return runpy.run_path(str(path)), {"path": relative, "sha256": hashlib.sha256(data).hexdigest()}


def main():
    tree, tree_receipt = load("tree_targets/adversary/check_construction.py")
    cases = [(2, (1,), 3, 8), (2, (1, 2), 6, 10),
             (3, (2,), 1, 5), (3, (1,), 3, 6), (5, (1,), 3, 5)]
    sections = [tree["check_sections"](*case) for case in cases]
    total = sum(item["generator_word_checks"] for item in sections)
    assert total == 11778
    closures = [tree["group_order"](2, (1,), depth) for depth in range(1, 9)]
    assert closures == [2, 8, 16, 16, 32, 32, 32, 32]
    assert tree["word_action"]((1, 0), 2, 1) == (1, 1)
    assert tree["word_action"]((0,), 2, 1, shift=1) == (0,)

    author_tree, author_receipt = load("tree_targets/verify_finite_levels.py")
    author_result = author_tree["verify"]()
    assert author_result == json.loads((ROOT / "tree_targets/finite_level_results.json").read_text())

    matrices, matrix_receipt = load("nil_embeddings/adversarial_review/noncommutative_check/check.py")
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        matrix_count = sum(matrices["check"](p) for p in (2, 3, 5))
    assert matrix_count == 63

    wreath, wreath_receipt = load("nil_embeddings/adversarial_review/check_wreath_augmentation.py")
    wreath_results = [wreath["check_prime"](p) for p in (2, 3)]
    saved = json.loads((ROOT / "nil_embeddings/adversarial_review/wreath_augmentation_results.json").read_text())
    assert wreath_results == saved["UT3_examples"]
    result = {
        "utc": datetime.now(timezone.utc).isoformat(),
        "status": "all exact assertions passed",
        "section_checks": total,
        "binary_single_generator_depth1_through8_orders": closures,
        "tree_author_output_matches": True,
        "noncommutative_named_checks": matrix_count,
        "noncommutative_stdout": buffer.getvalue(),
        "wreath_augmentation_output_matches": True,
        "wreath_augmentation_results": wreath_results,
        "inputs": [tree_receipt, author_receipt, matrix_receipt, wreath_receipt],
        "limits": "Finite supplemental checks; no certification of external theorem, universal conclusion, originality, human review or formal proof."
    }
    output = Path(__file__).with_name("family_reproduction_results.json")
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({key: result[key] for key in ("utc", "status", "section_checks", "noncommutative_named_checks", "tree_author_output_matches", "wreath_augmentation_output_matches")}, indent=2))


if __name__ == "__main__":
    main()
