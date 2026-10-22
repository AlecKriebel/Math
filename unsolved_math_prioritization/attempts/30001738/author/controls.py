"""Finite diagnostics only. This does not prove a representation-theoretic theorem."""
import sys
if not sys.flags.isolated or not sys.flags.no_site:
    raise SystemExit("Use python -I -S -B controls.py")
from collections import Counter
from fractions import Fraction as Q
from itertools import product
import json
import math

checks = 0
families = {}
def check(ok, label):
    global checks
    checks += 1
    if not ok:
        raise RuntimeError("FAILED: " + label)
    families[label.split("/")[0]] = families.get(label.split("/")[0], 0) + 1

TAU = {"a":"a", "b":"b", "c":"d", "d":"c"}
DIMS = {"a":1, "b":2, "c":1, "d":1}
SCOPE = {"base":"p-adic", "base_characteristic":0, "coefficients":"complex",
         "irreducible":True, "generic":True, "normalized_induction":True}
def scoped_formula(labels, scope):
    if scope != SCOPE:
        raise ValueError("Outside the explicitly verified theorem scope")
    if not labels or any(x not in TAU for x in labels):
        raise ValueError("Nonempty known inducing multiset required")
    counts = Counter(labels)
    n = sum(DIMS[x] for x in labels)
    stable = counts == Counter(TAU[x] for x in labels)
    fixed = sum(TAU[x] == x for x in labels)
    degree = (1 << fixed) if stable else 0
    if n % 2:
        if degree % 2:
            raise ValueError("Inconsistent odd-dimensional Hermitian data")
        per_orbit = (degree // 2, degree // 2)
    else:
        per_orbit = ((degree + 1)//2, degree//2)
    return {"n":n, "stable":stable, "fixed_occurrences":fixed,
            "degree":degree, "orbit_multiplicities":per_orbit}

def sign_enumeration(labels):
    """Independent finite count of choices on labelled fixed occurrences."""
    counts = Counter(labels)
    if counts["c"] != counts["d"]:
        return (0,0)
    fixed = [x for x in labels if x in ("a","b")]
    out = [0,0]
    for bits in product((0,1), repeat=len(fixed)):
        out[sum(bits)%2] += 1
    return tuple(out)

patterns = 0
for counts in product(range(9), repeat=4):
    if not 1 <= sum(counts) <= 8:
        continue
    labels = sum(([t]*c for t,c in zip(TAU,counts)),[])
    result = scoped_formula(labels,SCOPE)
    expected = sign_enumeration(labels)
    patterns += 1
    check(result["degree"] == sum(expected), "counting/total")
    check(tuple(result["orbit_multiplicities"]) == expected, "counting/orbits")
    check(result["degree"] == sum(result["orbit_multiplicities"]), "counting/sum")

repeated = scoped_formula(["a","a"],SCOPE)
paired = scoped_formula(["c","d"],SCOPE)
check(repeated["degree"] == 4, "semantic/repeated-occurrences")
check(repeated["degree"] != 2**len(set(["a","a"])), "semantic/not-distinct-count")
check(paired["stable"] and paired["degree"] == 1, "semantic/product-only")
check(paired["degree"] != 2**len(["c","d"]), "semantic/not-total-factor-count")
check(scoped_formula(["a","c"],SCOPE)["degree"] == 0, "semantic/nonstable")
check(scoped_formula(["b"],SCOPE)["orbit_multiplicities"] == (1,1),
      "semantic/even-dimension-fixed-block")
check(scoped_formula(["a"],SCOPE)["orbit_multiplicities"] == (1,1),
      "semantic/odd-dimension-two-quasisplit-orbits")

for key, value in [
    ("base","archimedean"), ("base_characteristic",3),
    ("coefficients","modular"), ("irreducible",False), ("generic",False),
    ("normalized_induction",False),
]:
    bad = dict(SCOPE)
    bad[key] = value
    try:
        scoped_formula(["a"],bad)
    except ValueError:
        rejected = True
    else:
        rejected = False
    check(rejected,"scope/"+key)
for labels in ([],["unknown"]):
    try:
        scoped_formula(labels,SCOPE)
    except ValueError:
        rejected = True
    else:
        rejected = False
    check(rejected,"scope/invalid-labels")

# F_9 as pairs a+b*i, i^2=-1 in F_3.
def add(x,y): return ((x[0]+y[0])%3,(x[1]+y[1])%3)
def mul(x,y):
    return ((x[0]*y[0]-x[1]*y[1])%3,(x[0]*y[1]+x[1]*y[0])%3)
def power(x,n):
    v = (1,0)
    for _ in range(n): v=mul(v,x)
    return v
field = list(product(range(3),repeat=2))
nonzero = [x for x in field if x != (0,0)]
for x,y,z in product(field,repeat=3):
    check(mul(x,add(y,z)) == add(mul(x,y),mul(x,z)), "field/distributivity")
    check(mul(mul(x,y),z) == mul(x,mul(y,z)), "field/associativity")
u=(1,1)
powers=[power(u,j) for j in range(8)]
check(len(set(powers)) == 8 and set(powers)==set(nonzero), "field/generator")
check(power(u,2)==(0,2) and power(u,4)==(2,0) and power(u,8)==(1,0),
      "field/displayed-powers")
log={x:j for j,x in enumerate(powers)}
for x,y in product(nonzero,repeat=2):
    check(log[mul(x,y)] == (log[x]+log[y])%8, "character/homomorphism")
for x in nonzero:
    check(log[power(x,3)] == 3*log[x]%8, "character/arithmetic-twist")
    check(power(power(x,3),3)==x, "character/involution")
check((3*1)%8 == 3 and (-1)%8 == 7 and (-3)%8 == 5,
      "character/three-different-involutions")
check((-2)%8 != 0, "character/ratio-nontrivial-on-units")

# Quotient Q[s]/(s^4-4s^2), rational exact arithmetic.
def reduce_poly(coeffs):
    p=list(map(Q,coeffs))
    while len(p)>4:
        d=len(p)-1
        c=p.pop()
        p[d-2]+=4*c
    return tuple(p+[Q(0)]*(4-len(p)))
def poly_add(p,q): return reduce_poly([a+b for a,b in zip(p,q)])
def poly_mul(p,q):
    out=[Q(0)]*7
    for i,a in enumerate(p):
        for j,b in enumerate(q):out[i+j]+=a*b
    return reduce_poly(out)
one=(Q(1),Q(0),Q(0),Q(0))
s=(Q(0),Q(1),Q(0),Q(0))
sq=poly_mul(s,s)
p=(Q(-1),Q(0),Q(1,2),Q(0))
check(poly_mul(p,p)==one,"fiber/p-invertible")
check(poly_add(sq,tuple(-2*a for a in p)) == tuple(2*a for a in one),
      "fiber/target-A")
check(poly_mul(poly_mul(s,s),poly_add(sq,tuple(-4*a for a in one)))==(0,0,0,0),
      "fiber/quartic-relation")
def eval_poly(c,x): return sum(a*Q(x)**i for i,a in enumerate(c))
def derivative(c): return [i*c[i] for i in range(1,len(c))]
quartic=[Q(0),Q(0),Q(-4),Q(0),Q(1)]
local_lengths=[]
for root in [-2,0,2]:
    c=quartic
    order=0
    while eval_poly(c,root)==0:
        order+=1
        c=derivative(c)
    local_lengths.append(order)
check(local_lengths==[1,2,1],"fiber/local-lengths")
check(sum(local_lengths)==4 and len(local_lengths)==3,"fiber/degree-not-point-count")

receipt = {"schema":"galois-multiplicity-controls-v1","status":"pass",
           "checks":checks,"families":dict(sorted(families.items())),
           "synthetic_multiset_patterns":patterns,"field_size":9,
           "singular_fiber_local_lengths":local_lengths,
           "repeated_fixed_factors":repeated,"nonfixed_paired_factors":paired,
           "limits":"Finite algebra and scope diagnostics only; no computation of infinite-dimensional Hom spaces."}
print(json.dumps(receipt,indent=2,sort_keys=True))
