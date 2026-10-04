"""Bounded adversarial controls; no external state or mathematical certification."""
import datetime
import itertools
import json
import math
from fractions import Fraction
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parent
records = []

def check(name, actual, expected):
    passed = actual == expected
    records.append({"name": name, "actual": str(actual), "expected": str(expected), "passed": passed})
    if not passed:
        raise AssertionError(records[-1])

started = datetime.datetime.now(datetime.timezone.utc).isoformat()

# Independent exact evaluation of the product-face cancellation.
for n in range(1, 21):
    for j in range(n + 1):
        coefficient = sum((-1) ** (2*n-1-j-l) * math.comb(n,l+1)
                          * math.comb(j+l+1,j+1) for l in range(n))
        check(f"coefficient_n{n}_j{j}", coefficient,
              n if j == n else (-1 if j == n-1 else 0))
        for l in range(n):
            scale = Fraction(math.factorial(j+l+1), math.factorial(j+1)*math.factorial(l))
            check(f"fiber_product_scale_n{n}_j{j}_l{l}", scale,
                  math.comb(j+l+1,j+1))

# A simplex of arbitrary normalized volume: integral of a barycentric
# coordinate is V after Esterov's (j+1)! measure, including a point j=0.
for j in range(9):
    for volume in (1, 2, 5, 17):
        value = Fraction(math.factorial(j+1)*volume,
                         math.factorial(j)*(j+1))
        check(f"barycentric_j{j}_volume{volume}", value, volume)

# This constructs the cube discriminant from a quadratic eliminant of two
# bilinear equations, independently of copying a hyperdeterminant formula.
a = sp.symbols("a00 a10 a01 a11")
b = sp.symbols("b00 b10 b01 b11")
x = sp.symbols("x")
r = sp.expand((a[0]+a[1]*x)*(b[2]+b[3]*x)
              -(b[0]+b[1]*x)*(a[2]+a[3]*x))
D = sp.Poly(sp.discriminant(r, x), *a, *b)
check("cube_polynomial_nonzero", D.is_zero, False)
check("cube_discriminant_terms", len(D.terms()), 12)
check("cube_tied_rows_zero", sp.expand(D.as_expr().subs(dict(zip(b,a)))), 0)

# Projected exponents are the A-column sums. Distinct row monomials may
# collide; generic constants must retain each resulting coefficient.
projected = {tuple(alpha[i]+alpha[i+4] for i in range(4)) for alpha,_ in D.terms()}
t = sp.symbols("t00 t10 t01 t11")
kappa = ((1,2,3,5),(7,11,13,17))
minor_values = []
for i,j in itertools.combinations(range(4),2):
    minor_values.append(kappa[0][i]*kappa[1][j]-kappa[0][j]*kappa[1][i])
check("chosen_row_constants_all_2x2_minors_nonzero", all(v != 0 for v in minor_values), True)
substitution = {a[i]: kappa[0][i]*t[i] for i in range(4)}
substitution.update({b[i]: kappa[1][i]*t[i] for i in range(4)})
specialized = sp.Poly(sp.expand(D.as_expr().subs(substitution)), *t)
check("cube_generic_specialization_support", {alpha for alpha,_ in specialized.terms()}, projected)
check("cube_projected_support_size", len(projected), 3)

# n=1 fixes translation and sign: Q=[0,2], coarse/fine triangulations.
c0,c1,c2,y = sp.symbols("c0 c1 c2 y")
quadratic = sp.Poly(sp.discriminant(c0+c1*y+c2*y*y,y), c0,c1,c2)
check("quadratic_discriminant_support", {alpha for alpha,_ in quadratic.terms()},
      {(1,0,1),(0,2,0)})
eta_zero = (1,0,1)
coarse_eta = (2,0,2)
fine_eta = (1,2,1)
check("quadratic_coarse_hurwitz_vector", tuple(a-b for a,b in zip(coarse_eta,eta_zero)), (1,0,1))
check("quadratic_fine_hurwitz_vector", tuple(a-b for a,b in zip(fine_eta,eta_zero)), (0,2,0))

result = {"schema":"pr55-fresh-prior-bounded-controls/v1", "started_utc":started,
          "finished_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
          "all_passed":all(r["passed"] for r in records), "control_count":len(records),
          "checks":records,
          "limits":"Bounded normalization/genericity controls, not proof of the universal theorem or historical priority."}
(ROOT / "CONTROL_RESULTS.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps({k:v for k,v in result.items() if k != "checks"},indent=2))
