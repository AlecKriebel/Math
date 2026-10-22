#!/usr/bin/env python3
"""Hostile graph controls; no candidate/package imports and no filesystem mutation."""
import importlib.util
import json
from pathlib import Path

spec = importlib.util.spec_from_file_location("fresh_lc", Path(__file__).with_name("independent_lc.py"))
lc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lc)


def mutant_graph(m, n, segments, shift=-1, reverse_first=False, reverse_second=False):
    prec = lc.precedes
    X = [(i, j) for i, u in enumerate(m) for j, v in enumerate(n) if prec(segments[u], segments[v])]
    Y = [(i, j) for i, u in enumerate(m) for j, v in enumerate(n)
         if prec(tuple(t + shift for t in segments[u]), segments[v])]
    edges = {}
    for i, j in X:
        edges[(i, j)] = []
        for k, h in Y:
            first = prec(segments[m[k]], segments[m[i]]) if reverse_first else prec(segments[m[i]], segments[m[k]])
            second = prec(segments[n[j]], segments[n[h]]) if reverse_second else prec(segments[n[h]], segments[n[j]])
            if i == k and second or j == h and first:
                edges[(i, j)].append((k, h))
    return X, Y, edges


def run():
    calibrations = [
        {"kind": "first-coordinate edge", "m": ("u", "v"), "n": ("w",),
         "segments": {"u": (0, 1), "v": (1, 2), "w": (2, 2)}, "x": (0, 0), "y": (1, 0)},
        {"kind": "second-coordinate edge", "m": ("A",), "n": ("B", "D"),
         "segments": lc.SEG, "x": (0, 1), "y": (0, 0)},
    ]
    mutants = [
        ("reversed first-coordinate arrow", {"reverse_first": True}),
        ("reversed second-coordinate arrow", {"reverse_second": True}),
        ("reversed both arrows", {"reverse_first": True, "reverse_second": True}),
        ("shift right instead of left", {"shift": 1}),
        ("omit shift", {"shift": 0}),
    ]
    records = []
    for name, opts in mutants:
        detected = []
        for c in calibrations:
            baseline = lc.graph(c["m"], c["n"], c["segments"])
            lc.require(c["y"] in baseline[2][c["x"]], "bad baseline calibration")
            mutated = mutant_graph(c["m"], c["n"], c["segments"], **opts)
            if c["y"] not in mutated[2].get(c["x"], []):
                detected.append(c["kind"])
        if (0, 0) not in mutant_graph(("D",), ("E",), lc.SEG, **opts)[1]:
            detected.append("D/E shifted Y vertex")
        lc.require(bool(detected), "hostile mutation survived all controls")
        # Deliberately also observe whether the weak all-partitions-only claim detects it.
        all_fail = True
        for size in (1, 2):
            for m in lc.itertools.combinations(lc.SEG, size):
                n = tuple(x for x in lc.SEG if x not in m)
                both = True
                for first, second in ((m, n), (n, m)):
                    X, Y, edges = mutant_graph(first, second, lc.SEG, **opts)
                    both = both and lc.exhaustive_match(X, edges) is not None
                all_fail = all_fail and not both
        records.append({"mutation": name, "detected_by": detected,
                        "weak_all_15_partitions_still_fail": all_fail})
    # Testing only one direction incorrectly accepts an E / ABCD product.
    lc.require(lc.direction(("E",), ("A", "B", "C", "D"))["LC"], "vacuous direction")
    lc.require(not lc.direction(("A", "B", "C", "D"), ("E",))["LC"], "reverse direction")
    records.append({"mutation": "omit reverse LC", "detected_by": ["E/ABCD direction asymmetry"]})
    return {"mutation_verdict": "ALL_6_HOSTILE_MUTATIONS_DETECTED", "records": records,
            "security_claim": "None; these are mathematical semantic controls."}


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, sort_keys=True))
