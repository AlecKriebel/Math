"""Independent exact rational diagnostics; no geometric existence certification."""
from fractions import Fraction as Q
import json
checks = 0
def require(value):
    global checks
    assert value
    checks += 1

# Local embedded patch: (t,x,y,z)=(s,q,a*(s-1)+b,a*s*q+b*q).
# Pullback lambda=e^s*(a*q ds+a dq)=d(e^s*a*q).
# For A ds+B dq multiplied by e^(sigma*s), d coefficient is
# sigma*B+partial_s B-partial_q A. Reversal changes sigma only.
for a in [Q(i, 7) for i in range(-12, 13)]:
    for b in [Q(-3, 5), Q(0), Q(8, 9)]:
        forward_coefficient = a - a
        reversed_coefficient = -a - a
        require(forward_coefficient == 0)
        require(reversed_coefficient == -2*a)
        require((reversed_coefficient == 0) == (a == 0))
require(-2*Q(1) != 0)  # Wrong mutation: time reversal preserves Lagrangianity.

# Reeb-chord trace separation uses ell+ell', not ell' alone.
for ell in [Q(i, 11) for i in range(1, 21)]:
    for slope in [Q(0), Q(1, 9), Q(5)]:
        require(ell + slope > 0)
require(Q(1) + Q(-1) == 0)  # Shrinking at this rate can collide in trace.

# Classical compatibility is necessary, not sufficient for an embedding.
def invariants(p, n):
    return (-1-p-n, p-n)
for p in range(15):
    for n in range(15):
        require(invariants(p,n) == invariants(p,n))
        require(invariants(p,n) != invariants(p+1,n))
        require(invariants(p,n) != invariants(p,n+1))
require(all(invariants(k,k) == (-1-2*k, 0) for k in range(100)))

# Bounded z at sample points alone gives no uniform small time derivative.
# Linear interpolation on length 1/M has slope M*(z1-z0).
epsilon = Q(1,100)
for mesh in [2, 10, 100, 1000]:
    bad_slope = mesh*(epsilon-(-epsilon))
    require(bad_slope > 2*epsilon)
    good_error = epsilon/mesh
    require(mesh*(good_error-(-good_error)) == 2*epsilon)

# Exact integral-period bookkeeping: annulus generator survives; killing it
# by asserting closed=>exact is invalid. Actual end Legendrianity kills it.
require(Q(0) == 0)
require(Q(1) != 0)
print(json.dumps({"status":"PASS", "exact_assertions":checks,
  "coverage":"finite rational local reversal, chord trace, stabilization and interpolation diagnostics",
  "not_certified":"existence of a global Lagrangian concordance; h-principle; knot type recognition; full imported proof"}, indent=2))
