"""Independent exact polynomial checks; no downloaded code or dependencies."""
from fractions import Fraction
import datetime
import json
from pathlib import Path

class P:
    """Sparse multivariate polynomial over Q, with fixed ordered variables."""
    names = ('B', 'C', 'L', 'F', 'h', 'f', 'g', 's', 'r', 'd', 'e', 'z')
    def __init__(self, value=0):
        self.a = dict(value) if isinstance(value, dict) else ({(0,) * len(self.names): Fraction(value)} if value else {})
        self.a = {k: Fraction(v) for k, v in self.a.items() if v}
    @classmethod
    def var(cls, name):
        powers = [0] * len(cls.names)
        powers[cls.names.index(name)] = 1
        return cls({tuple(powers): 1})
    def __add__(self, other):
        other = other if isinstance(other, P) else P(other)
        result = dict(self.a)
        for k, v in other.a.items(): result[k] = result.get(k, 0) + v
        return P(result)
    __radd__ = __add__
    def __neg__(self): return P({k: -v for k, v in self.a.items()})
    def __sub__(self, other): return self + -P(other) if not isinstance(other, P) else self + -other
    def __rsub__(self, other): return P(other) + -self
    def __mul__(self, other):
        other = other if isinstance(other, P) else P(other)
        result = {}
        for k, v in self.a.items():
            for j, w in other.a.items():
                powers = tuple(a + b for a, b in zip(k, j))
                result[powers] = result.get(powers, 0) + v * w
        return P(result)
    __rmul__ = __mul__
    def __pow__(self, n):
        result = P(1)
        for _ in range(n): result = result * self
        return result

B,C,L,F,h,f,g,s,r,d,e,z = [P.var(x) for x in P.names]
a2 = B+C
alpha_n = (B-L)*a2**2
beta_n = L*(a2+B)-a2*B
kappa_n = alpha_n+L*a2*B
A_n = alpha_n+beta_n*(C-F)
numerator_n = alpha_n*a2+beta_n*a2**2-beta_n*(B+F)*B-a2**2*B**2
tests = {
    'outer_conic_major_eigenvalue': alpha_n+beta_n*C-B**2*(a2-L),
    'paired_chord_coefficient_after_focal_relation': B*A_n-numerator_n-B*kappa_n,
    'opposite_pair_numerator': (h-f)*(s+g)*(r+g)-(h+f)*(s-g)*(r-g)-(2*h*g*(s+r)-2*f*(s*r+g**2)),
    'poncelet_discriminant': (e*z)**2-(d*z**2-1)*(d-z**2)-(d*z**4+(e**2-d**2-1)*z**2+d),
}
# The intersection-line checks use (h-f)Q_n=h(h-f)-(s-g)(r-g)
# and Q_t=s+r-g. The focal part of the normal is f, so the right
# side of the line equation is h(h-f)+s(s-g), and analogously for r.
tests['antipedal_intersection_first_line'] = h*(h-f)-(s-g)*(r-g)+(s-g)*(s+r-g)-(h*(h-f)+s*(s-g))
tests['antipedal_intersection_second_line'] = h*(h-f)-(s-g)*(r-g)+(r-g)*(s+r-g)-(h*(h-f)+r*(r-g))
def substitute_lambda_cleared(polynomial):
    index = P.names.index('L')
    degree = max(k[index] for k in polynomial.a)
    result = P(0)
    for powers, coefficient in polynomial.a.items():
        monomial = P(coefficient)
        for name, power in zip(P.names, powers):
            if name != 'L': monomial = monomial * P.var(name)**power
        result = result + monomial*(a2*B)**powers[index]*(a2+B)**(degree-powers[index])
    return result
tests['four_period_beta_after_lambda_substitution'] = substitute_lambda_cleared(beta_n)
tests['four_period_centroid_coefficient_after_lambda_substitution'] = substitute_lambda_cleared(kappa_n-2*alpha_n)
receipt = {
    'checked_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'method': 'Exact sparse polynomial expansion over rational coefficients; all variables are formal and independent before explicitly stated substitutions.',
    'definitions': {'B':'b^2', 'C':'a^2-b^2', 'L':'lambda', 'F':'f^2', 'e':'eta', 'a2':'B+C', 'common_denominator':'a2^2 B^2', 'focal_relations_used':'h^2=B+F; g^2=C-F'},
    'checks': {name: {'zero': not polynomial.a, 'remaining_terms': len(polynomial.a)} for name, polynomial in tests.items()},
    'limits': 'This checks algebraic reductions only. Smoothness, compactness, nonadjacent-pole cancellation and geometric least-period scope are checked analytically in the report; the receipt is not a substitute for them.'
}
assert all(check['zero'] for check in receipt['checks'].values()), receipt
Path(__file__).with_name('ALGEBRA_RECEIPT.json').write_text(json.dumps(receipt, indent=2)+'\n')
print(json.dumps(receipt, indent=2))
