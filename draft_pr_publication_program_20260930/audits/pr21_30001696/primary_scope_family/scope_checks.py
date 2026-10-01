#!/usr/bin/env python3
"""Finite semantic diagnostics, not a proof or priority certificate."""
from itertools import product
from math import comb
from pathlib import Path
import datetime
import hashlib
import json


def variation(word):
    nonzero = [x for x in word if x]
    return sum(a != b for a, b in zip(nonzero, nonzero[1:]))


def completions(word):
    zero_positions = [j for j, x in enumerate(word) if not x]
    for choices in product((-1, 1), repeat=len(zero_positions)):
        result = list(word)
        for j, choice in zip(zero_positions, choices):
            result[j] = choice
        yield tuple(result)


def main():
    root = Path(__file__).resolve().parent
    seal = json.loads((root / "first_pass_seal.json").read_text())
    snapshot = root.parent / "source_snapshot"
    assertions = 0
    for item in seal["snapshot_files"]:
        data = (snapshot / item["path"]).read_bytes()
        assert len(data) == item["bytes"]
        assert hashlib.sha256(data).hexdigest() == item["sha256"]
        assertions += 2
    assert len(seal["snapshot_files"]) == 14
    assert seal["proof_sha256"] == "58809f3edaa2930f1111ba823b1ce50c8e328dd8388b2e19323600ede3d04305"
    assertions += 2
    nonzero_ternary_patterns = 0
    sign_words = 0
    for d in range(1, 9):
        words = list(product((-1, 1), repeat=d))
        sign_words += len(words)
        for i in range(d):
            admitted = sum(variation(word) <= i for word in words)
            assert admitted == 2 * sum(comb(d - 1, k) for k in range(i + 1))
            assertions += 1
        for word in product((-1, 0, 1), repeat=d):
            if not any(word):
                continue
            nonzero_ternary_patterns += 1
            possible = [variation(c) for c in completions(word)]
            minimum = variation(word)
            assert min(possible) == minimum
            assert variation(tuple(-x for x in word)) == minimum
            assertions += 2
            for i in range(d):
                assert any(k <= i for k in possible) == (minimum <= i)
                assertions += 1
    # Separates a closing-edge count from the actual OWR switch count.
    noncyclic = variation((1, 1, -1))
    cyclic = noncyclic + int(-1 != 1)
    assert noncyclic == 1 and cyclic == 2
    # A nonsingular TN matrix (identity) does not supply the strict-zero input.
    witness = (1, 0, 1)
    witness_min = variation(witness)
    witness_max = max(variation(c) for c in completions(witness))
    assert witness_min == 0 and witness_max == 2
    assertions += 2
    result = {
        "utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "head": seal["head"],
        "proof_sha256": seal["proof_sha256"],
        "status": "PASS",
        "assertions": assertions,
        "d_range": [1, 8],
        "nonzero_ternary_patterns": nonzero_ternary_patterns,
        "sign_words": sign_words,
        "meaning": "Snapshot binding, noncyclic facet counts, zero-completion realization, and antipodal invariance.",
        "limits": "Finite semantic tests supplement the general derivations. They do not certify the new homeomorphism, classical theorems, global priority, or current open status.",
    }
    (root / "scope_checks.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
