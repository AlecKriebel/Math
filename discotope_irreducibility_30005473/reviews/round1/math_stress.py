#!/usr/bin/env python3
"""Distinct mixed-rank exact stress test; universal results remain proved by hand."""
from datetime import datetime, timezone
from itertools import combinations
from pathlib import Path
import hashlib
import json
import platform
import sympy as s

def cols(ts, d, bottom_zero=False):
    return s.Matrix.hstack(*(s.Matrix([s.Integer(t)**k for k in range(d-1)] +
                                     [s.Integer(0 if bottom_zero else t**(d-1))])
                            for t in ts))

root=Path(__file__).resolve().parents[2]
paper=root/'paper.tex'
initial_hash=hashlib.sha256(paper.read_bytes()).hexdigest()
out={'utc':datetime.now(timezone.utc).isoformat(), 'python':platform.python_version(),
     'sympy':s.__version__, 'scope':'distinct finite exact examples, not proof certification',
     'paper_tex_sha256':initial_hash}

# Two killed, nonorthonormal rank-two discs and an un-killed rank-three disc.
A=[cols([1,2],5,True),cols([3,4],5,True),cols([5,6,7],5)]
rank_data={}
for k in range(1,4):
    for J in combinations(range(3),k):
        C=s.Matrix.hstack(*(A[j] for j in J))
        expected=min(5,sum(A[j].cols for j in J))
        assert C.rank()==expected
        rank_data[str(tuple(j+1 for j in J))]=expected
u=s.Matrix([0,0,0,0,1])
V=[s.Matrix([s.Rational(-7,25),s.Rational(24,25)]),
   s.Matrix([s.Rational(20,29),s.Rational(-21,29)])]
AJ=s.Matrix.hstack(A[0],A[1])
v=s.Matrix.vstack(*V)
w=s.Matrix.vstack(AJ[:4,:].T.inv()*v,s.zeros(1,1))
assert AJ.T*w==v
eps=s.symbols('eps', positive=True)
points=[]
for j in range(2):
    assert A[j].T*u==s.zeros(2,1)
    assert (V[j].T*V[j])[0]==1
    q=A[j].T*(u+eps*w)
    p=A[j]*q/s.sqrt((q.T*q)[0])
    expected=A[j]*V[j]
    assert s.simplify(p-expected)==s.zeros(5,1)
    points.append([str(x) for x in expected])
q=A[2].T*(u+eps*w)
q0=A[2].T*u
assert q0!=s.zeros(3,1)
p0=A[2]*q0/s.sqrt((q0.T*q0)[0])
assert s.simplify((A[2]*q/s.sqrt((q.T*q)[0])).subs(eps,0)-p0)==s.zeros(5,1)
out['mixed_rank_nonorthonormal_gp']={'ranks':rank_data,
   'killed_columns_top4_determinant':str(AJ[:4,:].det()),
   'normal':[str(x) for x in u], 'w':[str(x) for x in w],
   'killed_support_points':points,
   'remaining_support_point_limit':[str(x) for x in p0]}

# Independent elimination check using only squared auxiliary coordinates.
a,b,Y2,Z2=s.symbols('a b Y2 Z2')
P=((a+b)**2+Y2+Z2-5)**2-4*(4-Y2)*(1-Z2)
assert s.expand(P.subs({Y2:4-a*a,Z2:1-b*b}))==0
out['nongeneric_separation']={'circle_relation_reduction':'0',
                             'P_at_e3':str(s.expand(P.subs({a:0,b:0,Y2:0,Z2:1})))}
assert out['nongeneric_separation']['P_at_e3']=='16'

# A repeated rank-two example in R^4 reduces to one ellipse, preserving lower span.
B=s.Matrix([[2,1],[0,3],[0,0],[0,0]])
n=s.Matrix([1,2,3,4])
def support(C,n):
    q=C.T*n
    return C*q/s.sqrt((q.T*q)[0])
assert s.simplify(3*support(B,n)-support(3*B,n))==s.zeros(4,1)
out['repeated_lower_dimensional']={'rank':B.rank(), 'ambient_dimension':4,
                                  'three_identical_discs_equals_scaled_disc':True}
assert initial_hash==hashlib.sha256(paper.read_bytes()).hexdigest()
out['canonical_paper_unchanged']=True
out['result']='all assertions passed'
print(json.dumps(out,indent=2))
