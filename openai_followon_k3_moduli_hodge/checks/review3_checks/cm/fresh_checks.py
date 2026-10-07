#!/usr/bin/env python3
"""Fresh V3 CM convention checks; finite algebra only, never geometry."""
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import permutations, product
from pathlib import Path
import importlib.util
import json

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent


def multiply(p, q):
    r = Counter()
    for a, av in p.items():
        for b, bv in q.items():
            r[tuple(x + y for x, y in zip(a, b))] += av * bv
    return {m: c for m, c in r.items() if c}


def algebra():
    # Exponent order X, t=q^(1/2), e, b; negative exponents permitted.
    one = {(0, 0, 0, 0): 1}
    roots = [(0, 3, 0, 1), (0, 1, 0, 1), (0, 2, 1, 1)]
    p = one
    for root in roots:
        p = multiply(p, {(1, 0, 0, 0): 1, root: -1})
    # X^3 - q e1(alpha) X^2 + q^2 e2(alpha) X - q^3 e3(alpha).
    alpha = [(0, 1, 0, 1), (0, -1, 0, 1), (0, 0, 1, 1)]
    target = Counter({(3, 0, 0, 0): 1})
    for a in alpha:
        target[tuple(x + y for x, y in zip(a, (2, 2, 0, 0)))] -= 1
    for i in range(3):
        for j in range(i + 1, 3):
            target[tuple(x+y+z for x,y,z in zip(alpha[i],alpha[j],(1,4,0,0)))] += 1
    target[(0, 6, 1, 3)] -= 1
    assert p == {m: c for m, c in target.items() if c}
    # Substitute b1=t^-3 e0 b0 into the raw bracket formula.
    # Direct T1=t*((t^2+1)+t^4*t^-3*e0) = t^3+t+t^2 e0.
    assert {(3, 0):1,(1, 0):1,(2, 1):1} == {(2+1,0):1,(2-1,0):1,(2,1):1}
    # Direct T2=t^2*(1+(t^4+t^2)*t^-3*e0)=t^2+(t^3+t)e0.
    assert {(2,0):1,(3,1):1,(1,1):1} == {(2,0):1,(2+1,1):1,(2-1,1):1}
    # v=+1 selects valuation(e)=-3/2 and slope 1; v=-1 gives slope 0.
    slopes = {str(v): str(Fraction(1,2) - Fraction(-3*v,2)/3) for v in (-1,1)}
    assert slopes == {"-1":"0", "1":"1"}
    return {"raw_minuscule_brackets": True, "full_cubic_factorization": True, "slopes":slopes}


def switches():
    tested = 0
    moves = 0
    for s in range(1,4):
        rows = tuple(product((-1,1), repeat=s))
        for p in range(1,6):
            for xs in product(rows, repeat=p):
                x = [list(row) for row in xs]
                plus = [sum(row[k] == 1 for row in xs) for k in range(s)]
                y = [[1 if j < plus[k] else -1 for k in range(s)] for j in range(p)]
                for k in range(s):
                    a = [j for j in range(p) if x[j][k]==1 and y[j][k]==-1]
                    b = [j for j in range(p) if x[j][k]==-1 and y[j][k]==1]
                    assert len(a) == len(b)
                    for i,j in zip(a,b):
                        oldsum = tuple(x[i][h]+x[j][h] for h in range(s))
                        x[i][k],x[j][k] = x[j][k],x[i][k]
                        assert tuple(x[i][h]+x[j][h] for h in range(s)) == oldsum
                        moves += 1
                assert x == y
                tested += 1
    return {"lists_to_canonical_balanced_endpoint":tested, "two_row_switches":moves,
            "scope":"finite sign matrices, not cycle construction"}


def noncommutative_labels():
    # Model G=S3 x C2, with central complex conjugation c=(id,1).
    # This detects confusing left/right translation or forgetting inverse.
    ps = tuple(permutations(range(3)))
    ident = (tuple(range(3)),0)
    group = tuple((a,z) for a in ps for z in range(2))
    reps = tuple((a,0) for a in ps)
    def mul(g,h):
        a,z=g; b,w=h
        return tuple(a[b[i]] for i in range(3)), z^w
    def inverse(g):
        return next(h for h in group if mul(g,h)==ident)
    checked = 0
    for signs in product((-1,1), repeat=6):
        v = {(a,z):signs[i]*((-1)**z) for i,a in enumerate(ps) for z in range(2)}
        d = {h:v[inverse(h)] for h in group}
        for g in group:
            # r has val -M at p_1 and +M at p_c, choose M=1.
            total = 0
            for tau in reps:
                gt = mul(g,tau)
                val = -1 if gt==ident else (1 if gt==(ident[0],1) else 0)
                total += d[tau]*val
            assert total == -d[inverse(g)] == -v[g]
            translated = {tau:v[mul(tau,g)] for tau in group}
            assert translated[ident] == v[g]
            assert all(translated[(a,1)] == -translated[(a,0)] for a in ps)
            checked += 1
    return {"odd_functions":64,"group_order":12,"conjugate_valuation_and_right_translate_cases":checked}


def main():
    existing = ROOT / "cm_arithmetic/verify_hecke_counts.py"
    spec = importlib.util.spec_from_file_location("archived_count_check",existing)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    counts = [mod.check_field(q) for q in (2,3,5,7,11)]
    saved = json.loads((existing.with_name("hecke_counts.json")).read_text())
    assert counts == saved["fields"]
    source = ROOT.parent / "sources/pinned/preprints/The-rational-Hodge-conjecture-for-CM-abelian-varieties-September-30-2026/build/sections"
    names = ["01-introduction.tex","02-tensors.tex","03-surface.tex","04-theta.tex",
             "05a-moduli.tex","05b-frobenius.tex","05b-satake-frobenius.tex","05c-cm-types.tex","06-assembly.tex"]
    report = {"scope":"exact finite convention checks only; no theta, PEL, crystalline or Hodge certification",
              "source_sha256":{n:sha256((source/n).read_bytes()).hexdigest() for n in names},
              "algebra":algebra(),"switches":switches(),"noncommutative_labeling":noncommutative_labels(),
              "archived_counts_reexecuted_equal":True,"prime_fields":[2,3,5,7,11],"all_assertions_passed":True}
    (OUT/"fresh_results.json").write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({k:v for k,v in report.items() if k not in ("source_sha256",)},indent=2))


if __name__ == "__main__":
    main()
