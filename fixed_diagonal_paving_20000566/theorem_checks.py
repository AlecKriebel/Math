"""Finite exact sanity checks of the necessity construction, not its proof."""
import json
from fractions import Fraction
import sympy as s

def require(ok, label):
    if not ok:
        raise RuntimeError(label)

def prefix(d,r):
    d=sorted(d,reverse=True)
    return all(sum(d[:k*r+1]) < (r-1)*k+1 for k in range((len(d)-1)//r+1))

out={'status':'PASS','scope':'Exact sanity checks only; Schur-Horn and matroid arguments are the general proof.','cases':[]}
# An explicit nontrivial fractional Schur-Horn block conjugation.
t=s.Rational(1,4)
C=s.Matrix([[t,s.sqrt(t*(1-t))],[s.sqrt(t*(1-t)),1-t]])
require(C*C==C,'fractional coupling projection')
Q=s.zeros(4); Q[0,0]=1; Q[1,1]=C[0,0]; Q[1,2]=Q[2,1]=C[0,1]; Q[2,2]=C[1,1]
U=s.Matrix([[s.Rational(3,5),-s.Rational(4,5)],[s.Rational(4,5),s.Rational(3,5)]])
V=s.diag(U,U); Q=V*Q*V.T
require(Q*Q==Q and Q==Q.T,'conjugated projection')
a=sum(Q[i,i] for i in range(2))
require(a==s.Rational(5,4),'fractional trace')
require(Q[:2,:2].rank()==s.ceiling(a)==2,'minimum fractional compression rank')
require(Q[2:,2:].rank()==1,'complement fractional rank')
out['cases'].append({'name':'fractional_real_conjugation','diagonal':list(map(str,Q.diagonal())),'subset_trace':str(a),'rank':2,'complement_rank':1})
# Integer direct sum attains ceil(trace), including zero and full-rank boundaries.
for Q,k,rank in [(s.diag(1,0,1,0),2,1),(s.zeros(3),2,0),(s.eye(3),3,3)]:
    require(Q*Q==Q,'integer projection')
    require(Q[:k,:k].rank()==rank==s.ceiling(sum(Q[i,i] for i in range(k))),'integer minimum rank')
    out['cases'].append({'name':'integer_boundary','size':Q.rows,'subset_size':k,'rank':rank})
# Necessity: equality is a failure, not a weakly accepted prefix.
d=[s.Rational(2,3)]*3+[s.Rational(1,3)]*3
require(not prefix(d,2),'equality prefix must fail')
Q=s.diag(s.ones(3)/3,s.eye(3)-s.ones(3)/3)
require(Q[:3,:3].rank()==1,'obstruction compression rank')
require(3>2*Q[:3,:3].rank(),'matroid obstruction')
require(not prefix([s.Rational(3,4)]*4,2),'strict violation must fail')
require(prefix([s.Rational(1,2)]*4,2),'constant threshold equality remains strictly pavable')
require(prefix([0,0,0],1),'zero projection r=1')
require(not prefix([1,0,0],1),'nonzero projection r=1')
require(prefix([s.Rational(1,2)]*2,2),'singleton blocks positive gap')
require(not prefix([1,0],2),'diagonal one cannot be paved')
out['cases'].append({'name':'necessity_and_boundary_logic','tests':8})
# Independently verify all pair polynomials rather than merely recording them.
x,y,z=s.symbols('x y z', real=True); L=s.Symbol('L')
A=s.Matrix([[0,x,y,z],[x,0,-s.I*z,s.I*y],[y,s.I*z,0,-s.I*x],[z,-s.I*y,s.I*x,0]])
for i,j,v in [(0,1,x),(0,2,y),(0,3,z),(1,2,z),(1,3,y),(2,3,x)]:
    require(s.expand(A.extract([i,j],[i,j]).charpoly(L).as_expr().subs({'L':L})-(L*L-v*v))==0,'pair polynomial')
out['all_six_pair_polynomials_verified']=True
print(json.dumps(out,indent=2))
