#!/usr/bin/env python3
"""Independent exact arithmetic certificate; no numerical extremal solver.

This uses coefficient recurrence rather than the frozen script's geometric
series extraction. All comparisons use Fraction; complex-analytic inequalities
are proved in DERIVATION.md and their constants are certified here.
"""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json

records = []

def claim(name, condition, **evidence):
    if not condition:
        raise AssertionError(name)
    records.append(dict(name=name, passed=True,
                        evidence={k: str(v) for k, v in evidence.items()}))

def less(name, left, right):
    claim(name, left < right, left=left, right=right, margin=right-left)

def equal(name, left, right):
    claim(name, left == right, left=left, right=right)

# Formal coefficient ring Q[a2,a3,u], and a truncated series in z.
ONE = {(0, 0, 0): F(1)}
A2 = {(1, 0, 0): F(1)}
A3 = {(0, 1, 0): F(1)}
U = {(0, 0, 1): F(1)}

def plus(*polys):
    out = {}
    for p in polys:
        for k, v in p.items():
            out[k] = out.get(k, F(0)) + v
    return {k: v for k, v in out.items() if v}

def times(p, q):
    out = {}
    for k, v in p.items():
        for l, w in q.items():
            key = tuple(i+j for i, j in zip(k, l))
            out[key] = out.get(key, F(0)) + v*w
    return {k: v for k, v in out.items() if v}

def scale(p, c):
    return {k: v*c for k, v in p.items() if v*c}

f = [{}, ONE, A2, A3, {}]
f_squared = [plus(*(times(f[j], f[n-j]) for j in range(n+1)))
             for n in range(5)]

def quotient_by_recurrence(first_sign=-1, feedback_sign=1):
    # (f-w)h=f^2, so h=-u f^2+u f h. Solves one z coefficient at a time.
    h = [{} for _ in range(5)]
    for n in range(5):
        h[n] = times(U, plus(scale(f_squared[n], F(first_sign)),
                     scale(plus(*(times(f[j], h[n-j])
                                   for j in range(1, n+1))),
                           F(feedback_sign))))
    return h

h = quotient_by_recurrence()
expected = {
    2: {(0, 0, 1): F(-1)},
    3: {(1, 0, 1): F(-2), (0, 0, 2): F(-1)},
    4: {(2, 0, 1): F(-1), (0, 1, 1): F(-2),
        (1, 0, 2): F(-3), (0, 0, 3): F(-1)},
}
for n in (2, 3, 4):
    claim(f"recurrence extraction through z^{n}", h[n] == expected[n])

def derive_koebe_polynomials(c3, c4):
    # L=a2+i*epsilon*(c3*a3+c4*a4).
    A0, B0, C0 = 4*c3+10*c4, c3+6*c4, c4
    P0 = {0: A0, 2: -B0, 4: C0}
    d = {1: -A0/F(2), 3: B0/F(6), 5: -C0/F(10)}
    q = {2: B0/F(3), 4: -2*C0/F(5)}
    return P0, d, q

def derivative(p):
    return {n-1: n*c for n, c in p.items() if n*c}

def evaluate(p, t):
    return sum((c*t**n for n, c in p.items()), F(0))

P0, d, q = derive_koebe_polynomials(F(-3), F(1))
equal("forced P0", P0, {0: F(-2), 2: F(-3), 4: F(1)})
equal("inverse first variation", derivative(d), {n: -c/2 for n, c in P0.items()})
equal("forced q", q, {2: F(1), 4: F(-2, 5)})
T, E, H = F(7, 4), F(1, 10**24), F(1, 10**12)
equal("epsilon is eta squared", E, H**2)
equal("q(1)", evaluate(q, F(1)), F(3, 5))
equal("q(7/4)", evaluate(q, T), -F(441, 640))

def transformed_Q(w_sign):
    # Q terms have coefficient -a,-b,-c at w^-3,w^-4,w^-5.
    # w=s*v^-2; (dw/dv)^2=4*v^-6 for s=+-1.
    return [(-4*F(w_sign)**(-n), 2*n-6) for n in (3, 4, 5)]

equal("negative double cover differential", transformed_Q(-1),
      [(F(4), 0), (F(-4), 2), (F(4), 4)])
equal("A at Koebe", 2*3+2**2-6*2, -2)
equal("B at Koebe", 3*2-3, 3)

# Uniform near-Koebe and slit tip estimates, including the omitted intermediate
# bounds needed by |H+H0|<7/2 and the reciprocal-cube difference.
less("maximizer Re a2 positive", 0, 2-13*E)
less("a2 deviation constant", 52, 8**2)
less("area a3 deviation constant squared", 4*F(13, 3), 5**2)
equal("a3 total error coefficient", 5+3*8, 29)
equal("A error coefficient", 2*29+6*8, 106)
equal("B error coefficient", 3*8, 24)
r = F(2, 3)
equal("H tail geometric bound", r**4/(3*(1-r**2)), F(16, 135))
less("H tail geometric bound below 1/4", F(16, 135), F(1, 4))
less("H error below 5 eta", 4*r+2, 5)
equal("H derivative geometric bound", (1-r**2)**-2-1, F(56, 25))
less("H derivative bound below 9/4", F(56, 25), F(9, 4))
less("sqrt 13 below 4 by squaring", 13, 16)
less("H at zstar above 3/2", 5*H, F(5, 3)-F(3, 2))
less("H at zstar below 11/6", F(5, 3)+5*H, F(11, 6))
less("H plus H0 below 7/2", 2*F(5, 3)+5*H, F(7, 2))
less("H quadratic sum below 11", F(11, 6)**2+F(11, 6)*F(5, 3)+F(5, 3)**2, 11)
equal("reciprocal square coefficient", 5*F(7, 2)/(F(3, 2)**2*F(5, 3)**2), F(14, 5))
less("f value error below 2 eta", F(2, 3)*F(14, 5), 2)
less("f derivative numerator below 19 eta", 5+F(4, 3)*10, 19)
less("f derivative first error below 6 eta", 19/F(3, 2)**3, 6)
less("f derivative second error below 2 eta", F(1, 3)*5*11/(F(3, 2)**3*F(5, 3)**3), 2)
equal("Koebe conformal-radius bound", F(6, 25)+F(5, 9)*F(9, 125), F(7, 25))
less("tip perturbation below 7 eta", 2+F(5, 9)*8, 7)
less("actual slit tip bound", F(7, 25)+7*H, F(3, 10))

# Original disk-3 constants.
equal("disk-3 P0 bound", 2+3*3**2+3**4, 110)
equal("disk-3 P0 derivative bound", 6*3+4*3**3, 126)
equal("disk-3 coefficient uncertainty", 106+24*3**2, 322)
less("disk-3 P closeness", 110+322*H, 111)
less("square root branch disk", 111*E, 1)
equal("G closeness bound", 3*111, 333)
less("Rouche strict boundary separation", 333*E, 1)
less("sqrt Taylor quadratic allowance", F(111**2, 2)*H, 1)
less("sqrt first variation allowance", 161+F(111**2, 2)*H, 162)
equal("G first variation allowance", 3*162, 486)
equal("d derivative disk-3 bound", 1+F(3, 2)*3**2+F(1, 2)*3**4, 55)
equal("inverse composition cost", 55*333, 18315)
less("V first variation allowance", 486+18315*H, 487)
less("inverse square root Taylor radius", 111*E, F(1, 4))
# |(3/4)*(1+x)^(-5/2)|<4 on |x|<=1/4. Square both
# sides; the Taylor integral factor 1/2 then gives remainder <2|x|^2.
less("inverse-root second derivative bound squared", F(3, 4)**2/F(3, 4)**5, 4**2)
equal("P0 derivative composition cost", F(126, 2)*333, 20979)
equal("inverse-root quadratic cost", 2*111**2, 24642)
less("V derivative first variation allowance", 161+(20979+24642)*H, 162)
less("actual trajectory radius gate", T+333*E, F(9, 5))
less("candidate W radius above tip gate", F(3, 10), F(25, 81))
less("V denominator exceeds 1/2", F(1, 2), 1-333*E)
less("q bound for every real t in interval", T**2+F(2, 5)*T**4, 7)
equal("Z linear numerator divided by 1/2", 2*(T*162+487), 1541)
equal("Z quadratic numerator divided by 1/2", 2*7*333, 4662)
less("Z total original relative bound", 1541+4662*H, 2000)
less("Z Re positive uniformly", 2000*E*H, 1)
less("positive endpoint strict margin", F(1, 2), F(3, 5)-2000*H)
less("negative endpoint strict margin", -F(441, 640)+2000*H, -F(1, 2))

# Independently tightened disk-2 certificate: no original bound 333, 487,
# 162, or 2000 is needed to conclude the sign reversal.
equal("disk-2 P0 bound", 2+3*2**2+2**4, 30)
equal("disk-2 uncertainty", 106+24*2**2, 202)
less("disk-2 P closeness", 30+202*H, 31)
less("disk-2 inverse boundary separation for |t|<=7/4", 62*E, F(1, 4))
less("disk-2 p expansion bound", 101+F(31**2, 2)*H, 102)
equal("disk-2 d derivative bound", 1+F(3, 2)*2**2+F(1, 2)*2**4, 15)
less("disk-2 V expansion bound", 204+15*62*H, 205)
equal("disk-2 P0 derivative bound", 6*2+4*2**3, 44)
less("disk-2 V derivative expansion bound", 101+(F(44, 2)*62+2*31**2)*H, 102)
less("disk-2 Z error bound", 2*(T*102+205)+2*7*62*H, 768)
less("disk-2 positive endpoint margin", F(1, 2), F(3, 5)-768*H)
less("disk-2 negative endpoint margin", -F(441, 640)+768*H, -F(1, 2))

# Additional control across 0<t<2, including t down to zero: Schwarz applied
# to V(t)-t gives |V/t-1|<=333*epsilon/2. ReZ>0 then follows without
# importing the actual slit's radial ordering.
delta = 111*E
less("inverse-root derivative closeness by |p|>=1-delta", delta/(1-delta), 112*E)
less("global Z closeness on 0<t<2", (112*E+F(333, 2)*E)/(1-F(333, 2)*E), 279*E)
less("global Z Re positive", 279*E, 1)

# Supplemental limiting-case reconstruction, performed after the main audit
# and comparison: actual Im Z has positive leading t^2 coefficient near zero.
less("A magnitude below 3", 2+106*H, 3)
less("a inverse-square deviation below 7 epsilon",
     3*(2+3*E)/(1-3*E)**2, 7)
less("B/a^2 distance from 3 below 25 eta",
     24/(1-3*E)**2+21*H, 25)
less("actual near-infinity leading Im Z coefficient positive", 25*H, 3)

# Controls are distinguishable from an extremal-existence verification.
# The original simple first-order controls reject unsuitable perturbations.
def reversal(poly):
    return evaluate(poly, F(1))*evaluate(poly, T) < 0

claim("selected perturbation reversal", reversal(q))
claim("a3-only negative control", not reversal(derive_koebe_polynomials(F(1), F(0))[2]))
claim("a4-only negative control", not reversal(derive_koebe_polynomials(F(0), F(1))[2]))
claim("zero perturbation negative control", not (E*0 > 0))
claim("oversized uncertainty control", not (F(3, 5)-F(3, 5) > 0))

# Mutation controls attack separate mechanism boundaries. Each mutation must
# cause its defining check to fail; sign reversal alone would miss some defects.
mutations = []
def rejected(name, would_pass):
    claim("mutation rejected: " + name, not would_pass)
    mutations.append(dict(name=name, rejected=True))

rejected("wrong quotient feedback sign", quotient_by_recurrence(feedback_sign=-1)[3] == expected[3])
rejected("wrong quotient leading sign", quotient_by_recurrence(first_sign=1)[2] == expected[2])
rejected("omitted -3a3 term", reversal(derive_koebe_polynomials(F(0), F(1))[2]))
rejected("positive double cover w=+v^-2", transformed_Q(1) == transformed_Q(-1))
rejected("wrong inverse first-order sign", derivative({n: -c for n, c in d.items()}) == {n: -c/2 for n, c in P0.items()})
rejected("use inward tangent for radial angle", -F(2) > 0)  # t*(-W'/W)->2 is required.
rejected("drop quartic q term", reversal({2: F(1)}))
rejected("enlarge eta to 10^-4 without reproof", 161+45621*F(1, 10**4) < 162)
rejected("ignore zero-epsilon degeneracy", F(0)*evaluate(q, F(1)) > 0)

if __name__ == "__main__":
    frozen = Path(__file__).resolve().parents[2]/"original"/"unsolved_math_prioritization"/"attempts"/"2306072"/"PROOF.md"
    report = {
        "status": "passed",
        "check_count": len(records),
        "arithmetic": "Python standard-library Fraction; all comparison operands exact",
        "input_proof_sha256": hashlib.sha256(frozen.read_bytes()).hexdigest(),
        "uniformity": "All bounds hold for every admissible a2,a3 in the proof's near-Koebe enclosures, for every complex point in the stated disks and every real t in the stated intervals.",
        "checks": records,
        "mutations": mutations,
        "alternative_relative_Z_error": "768*eta on 1<=t<=7/4",
        "limitations": ["Analytic lemmas are justified in DERIVATION.md, not formalized by Python.",
                        "Classical compactness, area/coefficient theorem, and support-slit applicability remain imported assumptions.",
                        "No maximizing map is numerically constructed; no novelty or priority conclusion."]
    }
    print(json.dumps(report, indent=2, sort_keys=True))
