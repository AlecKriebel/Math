#!/usr/bin/env python3
"""Exact, dependency-free geometric-family witness/control checks. Writes nothing."""
from collections import Counter
from fractions import Fraction as F
import json
from pathlib import Path

def require(condition, message):
    if not condition:
        raise ValueError(message)

def antipode(p):
    return tuple(-x for x in reversed(p))

def events(seq):
    out = []
    for a, b in zip(seq, seq[1:] + seq[:1]):
        changed = [i for i, (x, y) in enumerate(zip(a, b)) if x != y]
        require(len(changed) == 2 and changed[1] == changed[0] + 1,
                "move must exchange two adjacent positions")
        k = changed[0]
        require(a[k] == b[k+1] and a[k+1] == b[k], "move is not a swap")
        require(abs(a[k]) != abs(a[k+1]), "same-body swap")
        out.append((b[k], b[k+1]))
    return out

def weak_axioms(seq, n):
    length = 8 * n * (n - 1) // 2
    require(len(seq) == length and length > 0, "wrong full-period length")
    symbols = set(range(1, n+1)) | set(range(-n, 0))
    for p in seq:
        require(len(p) == 2*n and set(p) == symbols, "not a double permutation")
        require(all(p.index(i) < p.index(-i) for i in range(1,n+1)),
                "own endpoints reversed")
    require(all(seq[(k+length//2) % length] == antipode(seq[k])
                for k in range(length)), "wrong antipodal half")
    return events(seq)

def main():
    data = json.loads((Path(__file__).parent / "WITNESS.json").read_text())
    seq = [tuple(p) for p in data["sequence"]]
    ev = weak_axioms(seq, data["n"])
    require(data["n"] == 2, "audit is bound to the supplied n=2 witness")
    periods = [d for d in range(1,len(seq)+1)
               if all(seq[k] == seq[(k+d)%len(seq)] for k in range(len(seq)))]
    require(min(periods) == 8, "period is not primitive eight")
    mixed = [(x,y) for x,y in ev if (x > 0) != (y > 0)]
    require(not mixed, "witness unexpectedly has separating events")
    support = Counter(ev)
    expected_support = Counter({(1,2):2,(2,1):2,(-1,-2):2,(-2,-1):2})
    require(support == expected_support, "unexpected witness supporting schedule")
    require(not any(p in ((1,-1,2,-2),(2,-2,1,-1)) for p in seq),
                "witness unexpectedly has a fully separated term")

    # Two actual disks: centers (0,0),(3,0), radii 1,7/10.
    # q samples follow cos(theta) around the unit circle and are strictly
    # between the four exact exceptional cosine values.
    samples = [F(1),F(1,3),F(0),F(-1,3),F(-1),F(-1,3),F(0),F(1,3)]
    control = []
    for q in samples:
        points = [(F(-1),1),(F(1),-1),(3*q-F(7,10),2),(3*q+F(7,10),-2)]
        require(len({x for x,i in points}) == 4, "control sampled an event")
        control.append(tuple(i for x,i in sorted(points)))
    cev = weak_axioms(control, 2)
    allowed = {(x,y) for x in (1,-1,2,-2) for y in (1,-1,2,-2)
               if abs(x) != abs(y)}
    require(Counter(cev) == Counter({pair:1 for pair in allowed}),
            "actual disk control failed switch-once")
    require(sum((x>0)!=(y>0) for x,y in cev) == 4,
            "actual disk control lacks four mixed events")

    # Negative guards exercise generic invariant failure, not the conclusion.
    bad = seq.copy()
    bad[0] = (1,-1,2,-2)
    rejected = False
    try:
        weak_axioms(bad,2)
    except ValueError:
        rejected = True
    require(rejected, "corrupted witness guard failed")
    return {"status":"PASS","witness_events":ev,"least_period":min(periods),
            "witness_mixed_count":len(mixed),"control_sequence":control,
            "control_events":cev,"control_mixed_count":4,
            "corrupted_witness_rejected":rejected,
            "proof_limit":"Checks finite word and exact Euclidean control; topological necessity and normalization are analytic arguments."}

if __name__ == "__main__":
    print(json.dumps(main(), sort_keys=True))
