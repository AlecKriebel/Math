"""Finite exact checks for the Piranian-p.260 fixed rule; not a proof of limits."""
import hashlib, json
from fractions import Fraction as Q

v = [1]
rows = []
for n in range(9):
    N = 4**n
    assert len(v) == N and min(v) >= 0 and max(v) <= n+1
    assert sum(v) == N
    neighbor = max(abs(v[(j+1)%N]-v[j]) for j in range(N))
    assert neighbor <= 2
    if n:
        assert v[0] == v[-1] == 0
    rows.append({'n': n, 'cells': N, 'total_integer_mass': sum(v),
                 'positive_cells': sum(x>0 for x in v), 'max_height': max(v),
                 'circular_neighbor_bound': neighbor,
                 'vector_sha256': hashlib.sha256(json.dumps(v,separators=(',',':')).encode()).hexdigest(),
                 'first_vector': v if n <= 2 else None})
    nxt = []
    for x in v:
        child = [0,0,0,0] if x == 0 else [x-1,x+1,x+1,x-1]
        assert sum(child) == 4*x
        assert x == 0 or all(abs(y-x)==1 for y in child)
        nxt.extend(child)
    v = nxt

# Exact quadratic-field polynomial multiplication, r^2=2.
def add(a,b): return (a[0]+b[0],a[1]+b[1])
def mul(a,b): return (a[0]*b[0]+2*a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def poly_mul(a,b):
    out = [(Q(0),Q(0)) for _ in range(len(a)+len(b)-1)]
    for i,x in enumerate(a):
        for j,y in enumerate(b): out[i+j] = add(out[i+j],mul(x,y))
    return out
zero,one,two,r = (Q(0),Q(0)),(Q(1),Q(0)),(Q(2),Q(0)),(Q(0),Q(1))
minus_r,minus_two,minus_one,minus_half_r = (Q(0),Q(-1)),(Q(-2),Q(0)),(Q(-1),Q(0)),(Q(0),Q(-1,2))
# (-r*z-2*z^2)/(2+r*z) = -z*(z+r/2)/(1+(r/2)*z).
left = poly_mul([zero,minus_r,minus_two],[one,(Q(0),Q(1,2))])
right = poly_mul([zero,minus_half_r,minus_one],[two,r])
assert left == right
print(json.dumps({'scope':'finite exact diagnostic only; no sampled purity or Bloch certification',
                  'rule_source':'Piranian 1966 p.260', 'levels':rows,
                  'first_cayley_stages':{'B0':'-z',
                    'B1':'-z*(z+1/sqrt(2))/(1+z/sqrt(2))'},
                  'quadratic_field_identity':'passed'},indent=2))
