#!/usr/bin/env python3
"""Exact finite controls for the accompanying symbolic high-degree proof.

No asserts, floating-point root computations, external dependencies, network, or
filesystem writes. This validates this certificate family, not arbitrary roots.
"""
import argparse
from fractions import Fraction as F
import hashlib
import json
from math import comb
from pathlib import Path
import sys


class VerificationError(Exception):
    pass


def require(condition, label):
    if not condition:
        raise VerificationError(label)


def unique_object(pairs):
    d = {}
    for k, v in pairs:
        require(k not in d, "duplicate JSON key: " + k)
        d[k] = v
    return d


def sign(q):
    return (q > 0) - (q < 0)


def evaluate(coeffs, x):
    out = F(0)
    for a in reversed(coeffs):
        out = out*x+a
    return out


KEYS = set("schema problem_id problem_number v_denominator_power10 factor_exponents corrections sample_offsets expected_signs K N delta_power_of_two_exponent coefficient_denominator_power10 point_denominator_power10 evaluation_denominator_power10 H_upper_bound delta_comparison_power2 required_distinct_negative_roots expected_distinct_corners".split())


def verify(c):
    require(type(c) is dict and set(c) == KEYS, "certificate schema keys")
    require(c["schema"] == "binomial-corner-counterexample-v1", "schema version")
    require(type(c["problem_id"]) is int and c["problem_id"] == 2200013, "problem identity")
    require(c["problem_number"] == "AMR-021-0013", "problem number")
    for k in ["v_denominator_power10", "coefficient_denominator_power10", "point_denominator_power10", "evaluation_denominator_power10", "H_upper_bound", "delta_comparison_power2", "required_distinct_negative_roots", "expected_distinct_corners"]:
        require(type(c[k]) is int and 0 < c[k] < 1000000, "bounded integer: " + k)
    require(c["v_denominator_power10"] == 6, "seed parameter")
    for key in ["K", "N"]:
        require(type(c[key]) is str and c[key].isdigit() and len(c[key]) < 100, "integer string: " + key)
    K, N = int(c["K"]), int(c["N"])
    require(K >= 10**20 and K % 2 == 0, "large even K")
    v = F(1, 10**c["v_denominator_power10"])
    es = c["factor_exponents"]
    require(es == [5, 15, 25, 55], "seed odd exponents")
    require(c["corrections"] == [[3, 2], [2, 6], [1, 12]], "seed corrections")
    require(c["sample_offsets"] == [[-1, 1], [-1, 3], [-1, 5], [-1, 7], [1, 7]], "sample layout")
    require(c["expected_signs"] == [1, -1, 1, -1, 1], "claimed signs")
    require(c["delta_power_of_two_exponent"] == "N^2", "delta formula")

    q = [F(1)]
    support = {0}
    for e in es:
        require(e % 2 == 1, "odd seed factor")
        require(not support.intersection({j+e for j in support}), "distinct subset sums")
        support |= {j+e for j in support}
        new = [F(0)]*(len(q)+e)
        for i, a in enumerate(q):
            new[i] += a
            new[i+e] += a
        q = new
    for degree, power in c["corrections"]:
        for j in range(degree+1):
            q[j] += comb(degree,j)*v**power
    m = len(q)-1
    require(m == 100 and N == 2*K+m, "actual degree and symmetric block")
    C = q[0]
    require(C == 1+v**2+v**6+v**12 and 1<C<2, "seed endpoints")
    require(q[-1] == 1 and all(0<=a<=1 for a in q[1:-1]), "interior coefficient bounds")
    require(q[1] == 3*v**2+2*v**6+v**12 and q[2] == 3*v**2+v**6 and q[3] == v**2, "low coefficient expansion")

    Hmax = c["H_upper_bound"]
    product = 1
    for e in es:
        product *= e
    require(product == 103125 and sum(e-1 for e in es) == 96, "H data")
    require(96*v < 1 and F(product)/(1-96*v) < Hmax, "uniform H bound")
    require(-v**3+v**4+v**12 < 0, "first sign inequality")
    require(1-(Hmax+1)*v+v**4 > 0, "second sign inequality")
    require(-1+2*v < 0, "third sign inequality")
    require(1-v+v**4-Hmax*v**9 > 0, "fourth sign inequality")

    points = [-1+s*v**p for s,p in c["sample_offsets"]]
    require(all(points[i]<points[i+1] for i in range(4)), "disjoint ordered intervals")
    require(all(-2<t<-F(1,2) for t in points), "negative bounded sample points")
    values = [evaluate(q,t) for t in points]
    signs = [sign(a) for a in values]
    require(signs == c["expected_signs"], "exact Horner sign check")
    # Independent representation evaluates the product and corrections directly.
    for t, val in zip(points, values):
        direct = F(1)
        for e in es:
            direct *= 1+t**e
        direct += v**2*(t+1)**3+v**6*(t+1)**2+v**12*(t+1)
        require(direct == val, "independent seed evaluation agreement")

    cd, td, ed = (c[k] for k in ["coefficient_denominator_power10", "point_denominator_power10", "evaluation_denominator_power10"])
    require(cd <= 1000 and td <= 1000 and ed <= 100000, "denominator resource bounds")
    require(all(10**cd % a.denominator == 0 for a in q), "coefficient denominator bound")
    require(all(10**td % t.denominator == 0 for t in points), "point denominator bound")
    require(ed == cd+m*td, "evaluation denominator derivation")
    require(all(10**ed % a.denominator == 0 and a != 0 for a in values), "nonzero exact root-sign witnesses")
    require(10<2**4 and N*N>2*N+K+4*ed, "sign-preserving filler bound")

    require(F(10000,K)<=F(1,2), "binomial-ratio expansion domain")
    require((1+F(100,K))**100 <= 1+F(20000,K), "exact binomial-ratio majorant")
    L = 1+v*v/200
    require(L**100<C, "strict central chord comparison")
    p = c["delta_comparison_power2"]
    require(p<100000 and N*N>p and F(1,2**p)<v*v/1000, "delta comparison")
    margin = v*v/200-F(20000,K)-v*v/1000
    require(margin>0, "strict hull margin")
    require(100*N*N>K, "strict outer slope ordering")
    require(c["required_distinct_negative_roots"] == 4, "root lower bound claim")
    require(c["expected_distinct_corners"] == 3, "corner claim")
    return {
        "status": "PASS",
        "scope": "exact finite controls for symbolic proof, not expanded-polynomial enumeration",
        "degree": str(N),
        "K": str(K),
        "seed_degree": m,
        "sample_signs": signs,
        "distinct_negative_root_lower_bound": 4,
        "distinct_tropical_corners": 3,
        "upper_hull_indices": ["0",str(K),str(K+100),str(N)],
        "slope_jump_multiplicities": [str(K),"100",str(K)],
        "strict_hull_margin_lower_bound": str(margin),
        "full_support": True,
        "all_checks_use_exact_arithmetic": True,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("certificate", type=Path)
    args = parser.parse_args()
    try:
        require(args.certificate.is_file() and not args.certificate.is_symlink(), "regular nonsymlink certificate required")
        raw = args.certificate.read_bytes()
        require(len(raw) < 100000, "certificate too large")
        c = json.loads(raw, object_pairs_hook=unique_object)
        out = verify(c)
        out["certificate_sha256"] = hashlib.sha256(raw).hexdigest()
        print(json.dumps(out, sort_keys=True))
        return 0
    except (VerificationError, ValueError, TypeError, KeyError, OSError) as e:
        print(json.dumps({"status":"REJECT", "reason":str(e)}, sort_keys=True))
        return 2


if __name__ == "__main__":
    sys.exit(main())
