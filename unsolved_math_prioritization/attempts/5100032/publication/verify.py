#!/usr/bin/env python3
"""Exact rational-chord controls; Python 3.10+ standard library only.

The independent antipedal solver uses only its two defining line equations.
All validation uses explicit exceptions and remains active under Python -O.
Finite cases do not replace the manuscript's all-real, all-period proof.
"""
import argparse
from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
import itertools
import json
from math import isqrt
import os
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
FAULTS = ("coefficient", "height", "sign", "proof-binding")


class VerificationFailure(Exception):
    pass


class Checks:
    def __init__(self):
        self.count = 0

    def require(self, condition, code):
        self.count += 1
        if not condition:
            raise VerificationFailure(code)


def sha256(body):
    return hashlib.sha256(body).hexdigest()


def binding(checks, fault=None):
    pin = json.loads((HERE / "proof_binding.json").read_text(encoding="utf-8"))
    checks.require(pin["path"] == "focal_antipedal_sum.tex", "binding: fixed manuscript path")
    body = (HERE / pin["path"]).read_bytes()
    expected = "0" * 64 if fault == "proof-binding" else pin["sha256"]
    checks.require(sha256(body) == expected, "binding: manuscript SHA256")
    checks.require(len(body) == pin["bytes"], "binding: manuscript bytes")
    return sha256(body)


def norm2(p):
    return p[0] * p[0] + p[1] * p[1]


def dot(p, q):
    return p[0] * q[0] + p[1] * q[1]


def det(p, q):
    return p[0] * q[1] - p[1] * q[0]


def sub(p, q):
    return (p[0] - q[0], p[1] - q[1])


def rational_sqrt(x, checks):
    checks.require(x > 0, "sqrt: strictly positive rational radicand")
    n, d = isqrt(x.numerator), isqrt(x.denominator)
    checks.require(n * n == x.numerator, "sqrt: square numerator")
    checks.require(d * d == x.denominator, "sqrt: square denominator")
    return F(n, d)


def antipedal_relative(A, B, f, checks):
    """Solve Z.(A-f)=|A-f|² and Z.(B-f)=|B-f|² exactly."""
    U, V = sub(A, f), sub(B, f)
    ru, rv, determinant = norm2(U), norm2(V), det(U, V)
    checks.require(determinant != 0, "solver: independent defining lines")
    Z = ((ru * V[1] - rv * U[1]) / determinant,
         (U[0] * rv - V[0] * ru) / determinant)
    checks.require(dot(Z, U) == ru, "solver: first antipedal line")
    checks.require(dot(Z, V) == rv, "solver: second antipedal line")
    return Z


def edge(a, b, c, A, B, checks, fault=None):
    a, b, c = F(a), F(b), F(c)
    checks.require(a > b > 0 and c > 0 and a*a == b*b+c*c, "axes: strict focal ellipse")
    for P in (A, B):
        checks.require(P[0]*P[0]/(a*a)+P[1]*P[1]/(b*b) == 1, "endpoints: outer ellipse")
    dx, dy = B[0]-A[0], B[1]-A[1]
    orientation = 1 if det(A, B) > 0 else -1
    alpha, beta, w = orientation*dy, -orientation*dx, orientation*det(A, B)
    T, K = alpha*alpha+beta*beta, a*a*alpha*alpha+b*b*beta*beta
    checks.require(T > 0 and w > 0, "chord: nonzero and positive support")
    lam = (K-w*w)/T
    checks.require(0 < lam < b*b, "caustic: strictly nested confocal ellipse")
    checks.require(w*w == (a*a-lam)*alpha*alpha+(b*b-lam)*beta*beta,
                   "tangency: exact support equation")
    W = rational_sqrt(K-w*w, checks)
    M = (a*a*w*alpha/K, b*b*w*beta/K)
    z = a*b*W/K
    leftA, leftB = (A, B) if orientation == 1 else (B, A)
    checks.require(leftA == (M[0]+z*beta, M[1]-z*alpha), "chord: first completed-square endpoint")
    checks.require(leftB == (M[0]-z*beta, M[1]+z*alpha), "chord: second completed-square endpoint")
    H = {sigma: w-sigma*c*alpha for sigma in (1, -1)}
    checks.require(H[1] > 0 and H[-1] > 0, "heights: both ordinary focal heights positive")
    checks.require(H[1]*H[-1]/T == b*b-lam, "heights: focal-height product")
    qscaled, q2s, vertices = {}, {}, {}
    for sigma in (1, -1):
        f = (sigma*c, F(0))
        rA, rB = a-sigma*c*A[0]/a, a-sigma*c*B[0]/a
        checks.require(rA > 0 and rB > 0, "radii: positive focal distances")
        checks.require(rA*rA == norm2(sub(A, f)), "radii: first squared focal norm")
        checks.require(rB*rB == norm2(sub(B, f)), "radii: second squared focal norm")
        R = rA*rB
        checks.require(R == (a*a*H[sigma]*H[sigma]+b*b*lam*T)/K,
                       "product: independently evaluated endpoint radii")
        Z = antipedal_relative(A, B, f, checks)
        reversedZ = antipedal_relative(B, A, f, checks)
        checks.require(Z == reversedZ, "reversal: unchanged antipedal intersection")
        height = H[sigma]+1 if fault == "height" and sigma == 1 else H[sigma]
        qscaled[sigma] = R/height
        if fault == "sign" and sigma == 1:
            qscaled[sigma] = -qscaled[sigma]
        checks.require(qscaled[sigma] > 0, "norm: positive ordinary root")
        q2s[sigma] = norm2(Z)
        checks.require(q2s[sigma] > 0 and q2s[sigma] == T*qscaled[sigma]*qscaled[sigma],
                       "norm: independent solver and focal height")
        checks.require(qscaled[sigma] == (a*a*H[sigma]+b*b*lam*T/H[sigma])/K,
                       "norm: manuscript simplified expression")
        vertices[sigma] = Z
    bracket = -a*a+b*b*lam/(b*b-lam)
    changed = bracket+1 if fault == "coefficient" else bracket
    gamma_scaled = c*changed/(a*b*W)
    difference = qscaled[1]-qscaled[-1]
    checks.require(difference == gamma_scaled*alpha, "coboundary: correct fixed coefficient")
    checks.require(difference == orientation*gamma_scaled*dy, "reversal: oriented coefficient sign")
    return {"lambda": lam, "T": T, "qscaled": qscaled, "q2": q2s,
            "vertices": vertices, "dy": dy, "orientation": orientation,
            "coefficient_sign": (bracket > 0)-(bracket < 0), "horizontal": dy == 0}


def rational_points(a, b):
    positive = [F(1,5), F(1,4), F(1,3), F(1,2), F(2,3), F(1),
                F(3,2), F(2), F(3), F(4), F(5)]
    values = [-p for p in reversed(positive)]+[F(0)]+positive
    points = [(F(a)*(1-p*p)/(1+p*p), F(b)*2*p/(1+p*p)) for p in values]
    return points+[(F(-a), F(0))]


def deliberate_fault(name, checks):
    if name == "proof-binding":
        binding(checks, fault=name)
    else:
        edge(5, 3, 4, (F(5), F(0)), (F(0), F(3)), checks, fault=name)
    raise VerificationFailure("negative control was unexpectedly accepted")


def rejection_controls(checks):
    expected = {"coefficient": "coboundary: correct fixed coefficient",
                "height": "norm: independent solver and focal height",
                "sign": "norm: positive ordinary root",
                "proof-binding": "binding: manuscript SHA256"}
    results = []
    for name in FAULTS:
        local = Checks()
        try:
            deliberate_fault(name, local)
        except VerificationFailure as exc:
            checks.require(str(exc) == expected[name], "negative control: expected rejection mechanism")
            results.append({"name": name, "rejected": True, "reason": str(exc),
                            "guard_calls_before_rejection": local.count})
        else:
            checks.require(False, "negative control: no rejection")
    return results


def run():
    checks = Checks()
    proof_hash = binding(checks)
    cases, horizontal, reversals = 0, 0, 0
    sign_counts = {-1: 0, 0: 0, 1: 0}
    axes = ((5,3,4), (13,5,12), (13,12,5), (17,8,15))
    for a,b,c in axes:
        for A,B in itertools.combinations(rational_points(a,b), 2):
            raww = det(A,B)
            if raww == 0:
                continue
            alpha, beta = B[1]-A[1], A[0]-B[0]
            T, K = alpha*alpha+beta*beta, a*a*alpha*alpha+b*b*beta*beta
            lam = (K-raww*raww)/T
            if not (0 < lam < b*b):
                continue
            data = edge(a,b,c,A,B,checks)
            reverse = edge(a,b,c,B,A,checks)
            checks.require(data["q2"] == reverse["q2"] and data["vertices"] == reverse["vertices"],
                           "paired reversal: both ordinary norms and intersections")
            cases += 2
            reversals += 1
            horizontal += 2*data["horizontal"]
            sign_counts[data["coefficient_sign"]] += 2
    # A genuine closed diamond billiard orbit; each edge has the same caustic.
    cycle = [(F(5),F(0)), (F(0),F(3)), (F(-5),F(0)), (F(0),F(-3))]
    cycles_checked = []
    for repeats, reversed_order in ((1,False), (3,False), (3,True)):
        vertices = cycle*repeats
        if reversed_order:
            vertices = list(reversed(vertices))
        data = [edge(5,3,4,vertices[i],vertices[(i+1)%len(vertices)],checks)
                for i in range(len(vertices))]
        checks.require(all(e["lambda"] == F(225,34) for e in data), "cycle: common caustic")
        checks.require(all(e["T"] == F(34) for e in data), "cycle: common exact norm scale")
        checks.require(sum(e["dy"] for e in data) == 0, "cycle: closure displacement")
        checks.require(sum(e["qscaled"][1] for e in data) == sum(e["qscaled"][-1] for e in data),
                       "cycle: exact positive focal sums")
        checks.require(all(e["coefficient_sign"] == 0 for e in data), "cycle: coefficient zero")
        cycles_checked.append({"edges":len(vertices), "repeats":repeats, "reversed":reversed_order})
        cases += len(vertices)
        sign_counts[0] += len(vertices)
    checks.require(horizontal > 0, "coverage: horizontal chords")
    checks.require(all(n > 0 for n in sign_counts.values()), "coverage: negative, zero and positive coefficient")
    negatives = rejection_controls(checks)
    return {"schema":"focal-antipedal-exact-verification/v1", "status":"passed",
            "actual_verifier_PID":os.getpid(), "UTC":datetime.now(timezone.utc).isoformat(),
            "python_version":sys.version.split()[0], "optimization_level":sys.flags.optimize,
            "proof_sha256":proof_hash, "directed_chord_cases":cases,
            "paired_reversal_cases":reversals, "horizontal_directed_chords":horizontal,
            "coefficient_sign_cases":{str(k):v for k,v in sign_counts.items()},
            "explicit_passing_guard_checks":checks.count,
            "closed_cycle_controls":cycles_checked, "mandatory_invalid_controls":negatives,
            "scope":"Finite exact controls supplement the written all-real and all-period proof."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--invalid-control", choices=FAULTS)
    args = parser.parse_args()
    try:
        if args.invalid_control:
            deliberate_fault(args.invalid_control, Checks())
        result = run()
    except VerificationFailure as exc:
        print(json.dumps({"status":"rejected", "reason":str(exc),
                          "actual_verifier_PID":os.getpid(), "optimization_level":sys.flags.optimize}), file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
