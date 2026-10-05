#!/usr/bin/env python3
"""Read-only frozen-input audit and independently implemented exact controls.

No network, source documents, corpus records, or third-party packages are used.
These finite calculations do not decide the infinite-volume almost-Gibbs limit.
"""
import argparse
from fractions import Fraction as F
import hashlib
from itertools import product, combinations
import json
from pathlib import Path
import runpy
import zipfile


def digest(data):
    return {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def verify_freeze(author, archive):
    names = {"README.md", "PROOFS.md", "APPROACHES.md", "SOURCE_VERIFICATION.json",
             "PRIOR_WORK_CHECK.json", "verify_controls.py", "CHECK_RESULTS.json", "MANIFEST.json"}
    assert {p.name for p in author.iterdir()} == names
    receipt = digest(archive.read_bytes())
    assert receipt == {"bytes": 20899, "sha256": "a6b1e798dfa5776e174ed2bf01ee273c6923988d1cb1a2e3b846da63ef108d83"}
    with zipfile.ZipFile(archive) as z:
        assert len(z.namelist()) == 8 and set(z.namelist()) == names
        for name in names:
            assert z.read(name) == (author / name).read_bytes()
    manifest = json.loads((author / "MANIFEST.json").read_text())
    for name, expected in manifest["files"].items():
        assert digest((author / name).read_bytes()) == expected
    return {"status": "PASS", "archive": receipt, "members": 8,
            "every_member_equals_author_file": True, "manifest_entries_matched": 7,
            "snapshot": {n: digest((author / n).read_bytes()) for n in sorted(names)}}


def replay_author(author):
    # run_path does not invoke main or write bytecode. The author's main would
    # overwrite CHECK_RESULTS.json, so call only its reviewed pure controls.
    ns = runpy.run_path(str(author / "verify_controls.py"))
    expected = json.loads((author / "CHECK_RESULTS.json").read_text())
    for function, key in (("mixture_controls", "mixture_controls"),
                          ("ising_control", "ising_finite_control"),
                          ("markov_control", "markov_control")):
        assert ns[function]() == expected[key]
    return {"status": "PASS", "all_recorded_values_exactly_reproduced": True,
            "mixture_cases": 960, "ising_states": 32768,
            "ising_monotonicity_comparisons": 81, "markov_cases": 84}


def mixture_controls():
    # Integers proportional to component likelihoods, independent of the
    # author's direct powers of Bernoulli fractions.
    def q(N, k):
        lo, hi = 3 ** (N-k), 3 ** k
        return F(lo + 3*hi, 4*(lo+hi))
    cases = 0
    for n in range(11):
        for k in range(2*n+1):
            low = high = q(2*n, k)
            for added_pairs in range(21):
                N = 2*n + 2*added_pairs
                a, b = q(N, k), q(N, k+2*added_pairs)
                assert F(1,4) <= a <= low <= high <= b <= F(3,4)
                low, high = a, b
                cases += 1
    rare = []
    for k in (1, 4, 8, 12, 20, 40):
        prior_odds = F(1, 3**k)
        likelihood_ratio = 3**k
        posterior_odds = prior_odds * likelihood_ratio
        assert posterior_odds == 1
        lam = prior_odds/(1+prior_odds)
        bernoulli_before = lam*(1-lam)/4
        bernoulli_after = F(1,16)
        assert bernoulli_after > bernoulli_before
        # Spin coding 2I-1 multiplies covariance by four.
        rare.append({"k": k, "indicator_covariance_before": str(bernoulli_before),
                     "indicator_covariance_after": str(bernoulli_after),
                     "spin_covariance_after": "1/4"})
    gap = q(24,22)-q(24,2)
    assert gap == F(871696100,1743392201)
    return {"status": "PASS", "monotone_annulus_cases": cases,
            "rare_evidence": rare, "original_finite_gap": str(gap)}


def row_transfer_control(r, author_result):
    """Sum top and bottom rows separately instead of enumerating 2^15 states."""
    rows = list(product((0,1), repeat=5))
    def horizontal_agreements(row):
        return row[0] + row[-1] + sum(a == b for a,b in zip(row,row[1:]))
    def transfer(a,b):
        return sum(x == y for x,y in zip(a,b))
    row_weights = {}
    for middle in rows:
        one_side = sum(r ** (horizontal_agreements(outer) + sum(outer) +
                           transfer(outer,middle)) for outer in rows)
        row_weights[middle] = r ** horizontal_agreements(middle) * one_side**2
    def cond(pins):
        selected = [(row,w) for row,w in row_weights.items()
                    if all(row[i] == v for i,v in pins.items())]
        return F(sum(w for row,w in selected if row[2]), sum(w for row,w in selected))
    # Every arbitrary-sign partial pinning of the four noncentral sites.
    positions = (0,1,3,4)
    partial = {}
    for code in product((-1,0,1), repeat=4):
        pins = {i:v for i,v in zip(positions,code) if v != -1}
        partial[code] = cond(pins)
        assert F(1,1+r**4) <= partial[code] <= F(r**4,1+r**4)
    comparisons = 0
    for code, value in partial.items():
        for j, v in enumerate(code):
            if v == 0:
                changed = list(code)
                changed[j] = 1
                assert value <= partial[tuple(changed)]
                comparisons += 1
    # Elementary lattice inequalities with all other row coordinates pinned.
    lattice_checks = 0
    for i,j in combinations(range(5),2):
        rest = [k for k in range(5) if k not in (i,j)]
        for assignment in product((0,1), repeat=3):
            w = {}
            for a,b in product((0,1), repeat=2):
                row = [0]*5
                for k,v in zip(rest,assignment): row[k] = v
                row[i],row[j] = a,b
                w[a,b] = row_weights[tuple(row)]
            assert w[0,0]*w[1,1] >= w[0,1]*w[1,0]
            lattice_checks += 1
    brackets = []
    for left,right in product((0,1), repeat=2):
        lo, mid, hi = (cond({0:0,1:left,3:right,4:0}),
                       cond({1:left,3:right}), cond({0:1,1:left,3:right,4:1}))
        assert lo <= mid <= hi
        brackets.append({"inner": [left,right], "lower": str(lo),
                         "central": str(mid), "upper": str(hi)})
    if r == 2:
        assert brackets == author_result["ising_finite_control"]["brackets"]
    return {"exp_2beta": r, "partial_pinnings": len(partial),
            "pin_flip_comparisons": comparisons, "lattice_checks": lattice_checks,
            "brackets": brackets}


def solve(matrix, rhs):
    a = [[F(v) for v in row] + [F(b)] for row,b in zip(matrix,rhs)]
    n = len(a)
    for i in range(n):
        p = next(j for j in range(i,n) if a[j][i])
        a[i],a[p] = a[p],a[i]
        scale = a[i][i]
        a[i] = [v/scale for v in a[i]]
        for j in range(n):
            if j != i:
                scale = a[j][i]
                a[j] = [v-scale*w for v,w in zip(a[j],a[i])]
    return [a[i][-1] for i in range(n)]


def memory_two_bayes():
    states = list(product((0,1),repeat=2))
    p = {(0,0): F(1,5), (0,1): F(2,7), (1,0): F(3,5), (1,1): F(4,5)}
    def g(c, a,b): return p[a,b] if c else 1-p[a,b]
    T = [[g(d,a,b) if b == c else F(0) for c,d in states] for a,b in states]
    M = [[T[i][j]-int(i==j) for i in range(4)] for j in range(3)] + [[1]*4]
    pi = solve(M,[0,0,0,1])
    assert all(v>0 for v in pi) and sum(pi)==1
    assert all(sum(pi[i]*T[i][j] for i in range(4))==pi[j] for j in range(4))
    cases = 0
    for m in (2,3,4):
        for exterior in product((0,1),repeat=2*m):
            weights, predicted = [], []
            for a in (0,1):
                word = exterior[:m]+(a,)+exterior[m:]
                w = pi[states.index(word[:2])]
                for j in range(2,len(word)): w *= g(word[j],word[j-2],word[j-1])
                weights.append(w)
                predicted.append(g(a,*exterior[m-2:m]) *
                                 g(exterior[m],exterior[m-1],a) *
                                 g(exterior[m+1],a,exterior[m]))
            assert weights[1]/sum(weights) == predicted[1]/sum(predicted)
            cases += 1
    return {"status": "PASS", "stationary_pair_distribution": [str(v) for v in pi],
            "finite_conditioning_cases": cases,
            "scope": "Positive order-two Markov process; later likelihood factors cancel exactly."}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--author-dir", type=Path,
                        default=Path(__file__).resolve().parent.parent/"specifications_30004429")
    parser.add_argument("--archive", type=Path)
    parser.add_argument("--output", type=Path,
                        default=Path(__file__).resolve().with_name("INDEPENDENT_CHECK_RESULTS.json"))
    args = parser.parse_args()
    archive = args.archive or args.author_dir.parent/"SPECIFICATIONS_30004429_AUTHOR_SAFE_FREEZE.zip"
    freeze = verify_freeze(args.author_dir, archive)
    recorded = json.loads((args.author_dir/"CHECK_RESULTS.json").read_text())
    result = {"problem_id": "30004429", "result": "PASS", "freeze": freeze,
              "author_replay": replay_author(args.author_dir),
              "independent_mixture": mixture_controls(),
              "independent_ising_row_transfer": [row_transfer_control(r, recorded) for r in (2,3,5)],
              "independent_memory_two_bayes": memory_two_bayes(),
              "target_resolved": False,
              "scope": "Finite exact rational controls and immutable-input checks only; no infinite-volume conclusion."}
    assert verify_freeze(args.author_dir, archive) == freeze
    args.output.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"result": "PASS", "freeze_unchanged": True, "target_resolved": False}))


if __name__ == "__main__":
    main()
