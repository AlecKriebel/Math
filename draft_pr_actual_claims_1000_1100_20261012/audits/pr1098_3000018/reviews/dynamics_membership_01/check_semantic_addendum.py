#!/usr/bin/env python3
"""Extra input-totality and genuinely dissipative-mutant controls.

Imports only this reviewer's own exact implementation. These bounded checks
support, and do not replace, the analytic proof.
"""
import json
import sys
from pathlib import Path

from check_dynamics_membership import construct, need, run_schedule, valid_graph


def normalize(raw):
    if type(raw) is not list:
        return "NO", []
    clauses = []
    names = set()
    for clause in raw:
        if type(clause) is not list or len(clause) > 3 or any(type(v) is not int or v == 0 for v in clause):
            return "NO", []
        literals = set(clause)
        if any(-v in literals for v in literals):
            continue
        if not literals:
            return "NO", []
        if len(literals) > 3:
            return "NO", []
        names.update(abs(v) for v in literals)
        clauses.append(literals)
    if not clauses:
        return "YES", []
    mapping = {name: i + 1 for i, name in enumerate(sorted(names))}
    return "FORMULA", [tuple(sorted((1 if v > 0 else -1) * mapping[abs(v)] for v in clause))
                       for clause in clauses]


def dissipative_schedule(adj, initial, Q):
    """Wrong model: a return firing deletes its chip instead of returning it."""
    x = list(initial)
    before = sum(x)
    losses = steps = 0
    for _ in range(10000):
        choices = [v for v in range(len(adj)) if x[v] >= len(adj[v])]
        if not choices:
            need(losses > 0 and sum(x) == before - losses, "mutant did not actually dissipate")
            return {"halts": True, "lost_chips": losses, "steps": steps,
                    "initial_total": before, "final_total": sum(x)}
        v = choices[-1]
        x[v] -= len(adj[v])
        if v > Q:
            losses += 1
        else:
            for w in adj[v]:
                x[w] += 1
        need(min(x) >= 0, "mutant illegal update")
        steps += 1
    raise RuntimeError("dissipative mutant failed to terminate within bounded control")


def main():
    malformed = [None, 0, "", {}, [1], [[0]], [[True]], [[1.0]], [[1, 2, 3, 4]], [[1, -1, 2, 3]]]
    for value in malformed:
        need(normalize(value)[0] == "NO", "malformed input not sent to fixed NO")
    huge = 10 ** 1000
    cases = [([], "YES", []), ([[]], "NO", []),
             ([[huge, -huge]], "YES", []),
             ([[huge, huge]], "FORMULA", [(1,)]),
             ([[huge, -2], [-huge, 2]], "FORMULA", [(-1, 2), (-2, 1)])]
    for raw, tag, normalized in cases:
        got = normalize(raw)
        need(got == (tag, normalized), "formula normalization mismatch")
    mutants = []
    for oriented in (False, True):
        adj, initial, _, Q, _ = construct([(3, {0}), (3, {1})], oriented)
        need(valid_graph(adj, oriented), "original control graph invalid")
        truth, _, _, lasso = run_schedule(adj, initial, "low")
        need(not truth and lasso > 0, "inconsistent predicates must not halt")
        wrong = dissipative_schedule(adj, initial, Q)
        need(wrong["halts"], "dissipative semantics failed to change outcome")
        mutants.append({"oriented": oriented, "conservative_halts": truth,
                        "conservative_lasso_length": lasso, "damaged_model": wrong})
    # Huge chips are legal binary inputs. Their mass alone rules out halting;
    # this exercises no exponentially long firing simulation or unary expansion.
    large = []
    for bits in (128, 1024, 16384):
        initial = (1 << (bits - 1), 0)
        capacity = 0  # directed two-cycle, E-N=0
        need(sum(initial) > capacity, "large binary nonhalting mass certificate")
        large.append({"initial_max_bit_length": max(initial).bit_length(),
                      "vertices": 2, "stable_capacity": capacity, "halts": False})
    return {"claim": "bounded exact supporting controls only",
            "malformed_input_controls": len(malformed),
            "normalization_controls": len(cases),
            "huge_variable_identifier_decimal_digits": len(str(huge)),
            "dissipative_model_faults": mutants,
            "large_binary_inputs": large}


if __name__ == "__main__":
    if sys.argv[1:] == ["--self-test-invalid"]:
        need(False, "explicit semantic-addendum optimized guard")
    need(len(sys.argv) == 2, "usage: check_semantic_addendum.py output.json")
    output = main()
    Path(sys.argv[1]).write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps(output, indent=2, sort_keys=True))
