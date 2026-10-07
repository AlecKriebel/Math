#!/usr/bin/env python3
"""Exact diagnostics for the authored sphere counterexample. No network or writes."""
import itertools
import json
import sympy as sp

u, v, x, y, z, t, s = sp.symbols('u v x y z t s')

def Q(a, b):
    r = a*a + b*b
    return (2*a/(1+r), 2*b/(1+r), (r-1)/(1+r))

def P(a, b, c):
    return (a/(1-c), b/(1-c))

checks = []
def check(name, condition):
    ok = bool(condition)
    checks.append({'name': name, 'passed': ok})
    if not ok:
        raise AssertionError(name)

def zero(expr):
    return sp.cancel(expr) == 0

q = Q(u, v)
check('stereographic image lies on sphere', zero(sum(a*a for a in q)-1))
check('stereographic image avoids north pole by exact denominator identity',
      zero(1-q[2]-2/(1+u*u+v*v)))
pq = P(*q)
check('P after Q first coordinate', zero(pq[0]-u))
check('P after Q second coordinate', zero(pq[1]-v))
qp = Q(*P(x,y,z))
gb = sp.groebner([x*x+y*y+z*z-1],x,y,z)
for index, (out, target) in enumerate(zip(qp,(x,y,z))):
    numerator = sp.fraction(sp.cancel(out-target))[0]
    check('Q after P coordinate %d modulo sphere equation' % index,
          gb.reduce(numerator)[1] == 0)

h = Q((1-t)*u, (1-t)*v)
check('contraction start is identity in plane chart', all(zero(a.subs(t,0)-b) for a,b in zip(h,q)))
check('contraction endpoint is south pole', tuple(sp.simplify(a.subs(t,1)) for a in h)==(0,0,-1))
check('contraction remains on sphere', zero(sum(a*a for a in h)-1))
check('contraction avoids north pole', zero(1-h[2]-2/(1+(1-t)**2*(u*u+v*v))))
curve=(2*s/(1+s*s),sp.Integer(0),(1-s*s)/(1+s*s))
check('north-pole accumulation curve lies on sphere',zero(sum(a*a for a in curve)-1))
check('north-pole accumulation curve endpoint',tuple(a.subs(s,0) for a in curve)==(0,0,1))
check('north-pole accumulation curve first coordinate numerator',sp.fraction(curve[0])[0]==2*s)

vertices=[(i,) for i in range(4)]
edges=list(itertools.combinations(range(4),2))
faces=list(itertools.combinations(range(4),3))
def boundary_matrix(simplices, lower):
    out=sp.zeros(len(lower),len(simplices))
    index={simplex:i for i,simplex in enumerate(lower)}
    for j,simplex in enumerate(simplices):
        for k in range(len(simplex)):
            face=simplex[:k]+simplex[k+1:]
            out[index[face],j]=(-1)**k
    return out
D1=boundary_matrix(edges,vertices)
D2=boundary_matrix(faces,edges)
fundamental=sp.Matrix([-1,1,-1,1])
check('tetrahedron chain complex boundary squares to zero',D1*D2==sp.zeros(4,4))
check('tetrahedron face boundary rank is three',D2.rank()==3)
check('tetrahedron oriented boundary is a cycle',D2*fundamental==sp.zeros(6,1))
check('tetrahedron degree-two cycle module has rank one',len(D2.nullspace())==1)
check('tetrahedron computed nullspace equals displayed primitive generator',D2.nullspace()[0]==fundamental)

# This enumerates only the combinatorics of the finite quotient, not definability.
classes={0:{'north'},1:{'punctured_sphere'}}
subsets=[tuple(i for i in classes if mask&(1<<i)) for mask in range(4)]
preimages=[sorted(set().union(*(classes[i] for i in subset))) for subset in subsets]
check('all four subsets of the two-point quotient enumerated',len({tuple(p) for p in preimages})==4)

result={
  'all_passed':all(c['passed'] for c in checks),
  'check_count':len(checks),
  'sympy_version':sp.__version__,
  'checks':checks,
  'tetrahedron':{
    'oriented_faces':[list(f) for f in faces],
    'boundary_matrix':[[int(a) for a in row] for row in D2.tolist()],
    'kernel_generator':list(map(int,fundamental)),
    'rank_d2':D2.rank(),
    'rank_H2':4-D2.rank()
  },
  'scope':'Exact rational identities and a finite simplicial chain calculation. Saturation, first-order transfer, continuity arguments, logic topology, homotopy invariance, and identification of simplicial with singular homology are proved or stated with foundational citations in PROOF.md and BRIDGE_LEMMAS.md; they are not mechanically formalized here.',
  'formal_proof_checker_run':False,
  'large_exhaustive_search_run':False
}
print(json.dumps(result,indent=2))
