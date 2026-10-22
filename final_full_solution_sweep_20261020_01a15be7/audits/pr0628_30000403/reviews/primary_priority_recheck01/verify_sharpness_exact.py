"""Independent standard-library check of the candidate's finite lower-bound certificate."""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import datetime
import json

def q(a=0, b=0):
    return F(a), F(b)

def add(z, w):
    return z[0] + w[0], z[1] + w[1]

def neg(z):
    return -z[0], -z[1]

def sub(z, w):
    return add(z, neg(w))

def mul(z, w):
    return z[0]*w[0] - z[1]*w[1], z[0]*w[1] + z[1]*w[0]

def inv(z):
    n = z[0]*z[0] + z[1]*z[1]
    assert n != 0
    return z[0]/n, -z[1]/n

def div(z, w):
    return mul(z, inv(w))

def power(z, n):
    r = q(1)
    for _ in range(n):
        r = mul(r, z)
    return r

def det(p, r):
    return sub(mul(p[0], r[1]), mul(p[1], r[0]))

def J(points):
    u, v, w, t = points
    lam = div(mul(det(u,w),det(v,t)),mul(det(u,t),det(v,w)))
    numerator = mul(q(256),power(add(sub(power(lam,2),lam),q(1)),3))
    denominator = mul(power(lam,2),power(sub(lam,q(1)),2))
    return div(numerator,denominator)

zero, one = q(), q(1)
a, b = q(2,2), q(F(-1,4),F(-1,4))
D = [(zero,one),(one,zero),(one,one),(q(-1),one),(a,one),(b,one)]
rows = []
values = []
for labels in combinations(range(6),4):
    value = J([D[i] for i in labels])
    values.append(value)
    rows.append({'four_subset': ''.join(map(str,labels)),
                 'real': str(value[0]), 'imaginary': str(value[1])})
assert len(set(values)) == 15

def conj(z):
    return z[0], -z[1]

def tau_point(p):
    # tau([X:Y]) = [-conjugate(Y):conjugate(X)].
    return neg(conj(p[1])), conj(p[0])

permutation = []
for point in D:
    target = tau_point(point)
    matches = [i for i,other in enumerate(D) if det(target,other) == zero]
    assert len(matches) == 1
    permutation.append(matches[0])
assert permutation == [1,0,3,2,5,4]

result = {
    'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'arithmetic': 'fractions.Fraction pairs in Q(i); no floating-point comparisons',
    'distinct_J_values': len(set(values)),
    'four_subset_count': len(rows),
    'tau_permutation': permutation,
    'finite_certificate_pass': True,
    'logical_scope': 'The distinct projective four-subset invariants prove trivial stabilizer; tau preserves the six-point divisor. The fixed-point-free real descent obstruction is a separate proof in the report.',
    'values': rows,
}
Path(__file__).with_name('SHARPNESS_CERTIFICATE.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k != 'values'},indent=2))
