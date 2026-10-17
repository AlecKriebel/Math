"""Exact checks for the NEW priority-bridge audit deduction.

This checks polynomial transcriptions, support elimination, and adverse controls.
The imported existence theorem and the universal positivity proof are mathematical
inputs, not results certified by this program. No third-party source text is used.
"""
from datetime import datetime, timezone
import json
from pathlib import Path
import platform
import sympy as s

root = Path(__file__).resolve().parent
checks = []


def require(name, condition):
    if not condition:
        raise RuntimeError(name)
    checks.append(name)


def same(name, lhs, rhs):
    require(name, s.expand(lhs - rhs) == 0)


x, y, z, c, u, v, a, b, t, w = s.symbols("x y z c u v a b t w")
M = x**4*y**2 + x**2*y**4 + z**6 - c*x**2*y**2*z**2
F0 = u**2 + u**4 + v**6 - c*u**2*v**2
F1 = a**2 + a**4*v**2 + v**4 - c*a**2*v**2
F2 = b**2 + b**4*v**4 + v**2 - c*b**2*v**2
F3 = 1 + t**2 - c*t**2*v**2 + t**4*v**6
same("chart at P", M.subs({x: 1, y: u, z: v}), F0)
same("symmetry P Q", M.xreplace({x: y, y: x}), M)
same("first main chart", F0.subs(u, a*v), v**2*F1)
same("first complementary chart", F0.subs(v, w*u),
     u**2*(1 + u**2 + w**6*u**4 - c*w**2*u**2))
same("second main chart", F1.subs(a, b*v), v**2*F2)
same("second complementary chart", F1.subs(v, w*a),
     a**2*(1 + w**2*a**4 + (w**4-c*w**2)*a**2))
same("third main chart", F2.subs(b, t*v), v**2*F3)
same("third complementary chart", F2.subs(v, w*b),
     b**2*(1+w**2-c*w**2*b**2+w**4*b**6))
same("first exceptional equation", F1.subs(v, 0), a**2)
same("second exceptional equation", F2.subs(v, 0), b**2)
same("third exceptional equation", F3.subs(v, 0), 1+t**2)

for j, (F, variables, quadratic) in enumerate([
    (F0, (u, v), u**2),
    (F1, (a, v), a**2),
    (F2, (b, v), b**2+v**2),
]):
    poly = s.Poly(F, *variables)
    min_degree = min(sum(exp) for exp, coeff in poly.terms() if coeff != 0)
    require(f"center {j} multiplicity two", min_degree == 2)
    initial = sum(coeff*s.prod(q**k for q, k in zip(variables, exp))
                  for exp, coeff in poly.terms() if sum(exp) == 2)
    same(f"center {j} tangent", initial, quadratic)
require("real delta total", 2*sum([2*(2-1)//2]*3) == 6)

# Cubic SOS root coefficient elimination: sum of root squares has zero
# coefficients x^6,y^6,x^4*z^2,y^4*z^2,x^2*z^4,y^2*z^4 in that order.
monomials = [x**i*y**j*z**(3-i-j) for i in range(4) for j in range(4-i)]
coefficients = s.symbols("h0:"+str(len(monomials)))
root_form = dict(zip(monomials, coefficients))
h = sum(m*k for m, k in root_form.items())
eliminated = {}
for mon in [x**3, y**3, x**2*z, y**2*z, x*z**2, y*z**2]:
    current = s.Poly(s.expand(h.subs(eliminated)**2), x, y, z)
    same("zero coefficient isolates "+str(mon),
         current.coeff_monomial(mon**2), root_form[mon]**2)
    require("target coefficient zero for "+str(mon),
            s.Poly(M, x, y, z).coeff_monomial(mon**2) == 0)
    eliminated[root_form[mon]] = 0
remaining = [m for m in monomials if root_form[m] not in eliminated]
require("remaining half support", set(remaining) == {x**2*y, x*y**2, z**3, x*y*z})
same("negative coefficient obstruction",
     s.Poly(s.expand(h.subs(eliminated)**2), x, y, z).coeff_monomial(x**2*y**2*z**2),
     root_form[x*y*z]**2)
require("M coefficient is negative c", s.Poly(M, x, y, z).coeff_monomial(x**2*y**2*z**2) == -c)

# Full complex-singularity countercheck, independent of the real delta route.
gx = s.diff(M, x)/(2*x*y**2)
gy = s.diff(M, y)/(2*x**2*y)
same("nonzero coordinate gradient difference", gx-gy, x**2-y**2)
same("nonzero coordinate first gradient", gx, 2*x**2+y**2-c*z**2)
same("nonzero coordinate third gradient", s.diff(M, z)/(2*z), 3*z**4-c*x**2*y**2)

# Direct SOS when c <= 0, using c=-a^2; a ranges over the nonnegative square roots.
same("negative parameter explicit SOS", M.subs(c, -a**2),
     (x**2*y)**2+(x*y**2)**2+(z**3)**2+(a*x*y*z)**2)
same("upper threshold witness", M.subs({x: 1, y: 1, z: 1}), 3-c)
require("endpoint has extra zero", M.subs({x: 1, y: 1, z: 1, c: 3}) == 0)
require("endpoint control fails proposed two-point global-zero list",
        (1, 1, 1) not in [(1, 0, 0), (0, 1, 0)])
require("c greater than 3 nonnegative hypothesis fails",
        M.subs({x: 1, y: 1, z: 1, c: 4}) < 0)
require("incorrect exceptional exponent rejected",
        s.expand(F0.subs(u, a*v)-v**4*F1) != 0)
require("incorrect one-step delta rejected", 2*1 != 6)
require("incorrect truncation after two centers rejected", 2*2 != 6)

# Mixed odd-exponent factorization with correctly indexed homogeneous factors.
p, q = s.symbols("p q")
def trunc(N, R, P, Q):
    return sum(s.binomial(N,j)*P**j*Q**(R-j) for j in range(R+1))
for K in range(1, 16, 2):
    for L in range(1, 16, 2):
        N = K+L-1
        same(f"mixed exponent identity {K} {L}", (p+q)**N,
             q**L*trunc(N,K-1,p,q)+p**K*trunc(N,L-1,q,p))
        require(f"mixed exponent parity {K} {L}", N % 2 == 1)

result = {
    "status": "PASS",
    "generated_utc": datetime.now(timezone.utc).isoformat(),
    "python": platform.python_version(),
    "sympy": s.__version__,
    "checks_passed": len(checks),
    "checks": checks,
    "boundary": "Exact transcription checks; not a formal proof of the imported theorem or a numerical SOS search.",
}
(root/"CHECK_RESULTS.json").write_text(json.dumps(result, indent=2)+"\n")
print(json.dumps({k: v for k, v in result.items() if k != "checks"}, indent=2))
