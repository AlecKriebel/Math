#!/usr/bin/env python3
"""Exact small checks for problem 30006308. No downloads or remote writes.
Requires Python 3 and SymPy (tested with 1.14.0).
These checks support, rather than replace, the proofs in PROOF.md.
"""
from fractions import Fraction
from itertools import product, combinations_with_replacement
import json
import platform
import sympy as sp


def dot(a,b): return sum(x*y for x,y in zip(a,b))
def add(*vs): return tuple(map(sum,zip(*vs)))
def scale(a,v): return tuple(a*x for x in v)
def rays(e,a,b): return [(1,0,0),(0,1,0),(-1,e,a),(0,-1,b),(0,0,1),(0,0,-1)]
PAIRS=[(0,2),(1,3),(4,5)]
CONES=list(product(*PAIRS))

def data(e,a,b):
    out=[]
    for x in range(1-e,0):out.append((2,(x,-1,0),'I'))
    for y in range(b+1):
        for x in range(e*y+a+1,0):out.append((6,(x,y,1),'II'))
    for y in range(1-b,0):
        for x in range(e*y-a+1):out.append((5,(x,y,-1),'III'))
    if b==0:
        for x in range(1-a,0):out.append((5,(x,0,-1),'IV'))
    return out

def obstruction_degrees(e,a,b):
    return [(x,y,-1) for y in range(1-b,0) for x in range(e*y-a+1,0)]

def complex_vertices(rs,rho,u):
    return tuple(j+1 for j,v in enumerate(rs) if dot(v,u)<(-1 if j+1==rho else 0))

def counts(params):
    ds=data(*params);rs=rays(*params)
    dets=[int(sp.Matrix.hstack(*(sp.Matrix(rs[i]) for i in c)).det()) for c in CONES]
    assert all(abs(d)==1 for d in dets)
    supports=[complex_vertices(rs,r,u) for r,u,_ in ds]
    assert all(s in [(1,3),(2,4)] for s in supports)
    return dict(parameters=params,dimension_T1=len(ds),abstract_complex_types=1,
      embedded_supports=len(set(supports)),ray_support_types=len(set((d[0],s) for d,s in zip(ds,supports))),
      ray_degree_pairs=len(ds),support_multiplicities={str(s):supports.count(s) for s in sorted(set(supports))},
      smooth_cone_determinants=dets,first_order=[dict(ray=r,degree=u,type=t,support=s) for (r,u,t),s in zip(ds,supports)])

def homogeneous_monomials(us,v,ell=(-2,-2,-1)):
    ws=[dot(ell,u) for u in us];bound=dot(ell,v)
    assert all(w>0 for w in ws) and bound>=0
    ans=[]
    def rec(i,remaining,powers):
        if i==len(ws):
            if remaining==0 and tuple(sum(p*u[k] for p,u in zip(powers,us)) for k in range(3))==v:
                ans.append(tuple(powers))
            return
        for power in range(remaining//ws[i]+1):rec(i+1,remaining-power*ws[i],powers+[power])
    rec(0,bound,[])
    return ans

def exponent(n,*ix):
    z=[0]*n
    for i in ix:z[i-1]+=1
    return tuple(z)

def cup(rs,first,second):
    r,u,ca=first;s,v,cb=second
    sums={r:Fraction(0),s:Fraction(0)}
    for i,j in [(0,1),(1,2),(2,3),(3,0)]:
        factor=Fraction(ca[i]*cb[j]-ca[j]*cb[i],2)
        sums[r]+=factor*dot(rs[s-1],u)
        sums[s]-=factor*dot(rs[r-1],v)
    return {str(r):str(v) for r,v in sums.items() if v}

A=counts((3,-4,3));B=counts((4,-4,3))
for name in ['dimension_T1','abstract_complex_types','embedded_supports','ray_support_types','ray_degree_pairs']:
    assert A[name]==B[name]
ua=[(0,-1,-1),(1,-1,-1),(-1,0,1),(-1,-1,0),(-2,0,1),(-2,-1,0),(-3,0,1)]
va=(-1,-2,-1)
ma=homogeneous_monomials(ua,va)
assert set(ma)=={exponent(7,1,4),exponent(7,2,6),exponent(7,1,1,3),exponent(7,2,2,7),exponent(7,1,2,5)}
ub=[(0,-1,-1)]+[u for k in range(1,4) for u in [(-k,-1,0),(-k,0,1)]]
mb={}
for k in range(1,4):
    v=(-k,-2,-1);mb[str(k)]=homogeneous_monomials(ub,v)
    assert set(mb[str(k)])=={exponent(7,1,2*k),exponent(7,1,1,2*k+1)}
c5=(0,1,1,0);c2=(0,0,1,1)
qa=[cup(rays(3,-4,3),(5,ua[i],c5),(2,ua[j],c2)) for i,j in [(0,3),(1,5)]]
qb=[cup(rays(4,-4,3),(5,ub[0],c5),(2,ub[2*k-1],c2)) for k in range(1,4)]
assert all(q=={'5':'-1'} for q in qa+qb)
t=sp.symbols('t1:8');a3,a4,a5=sp.symbols('a3 a4 a5')
f=-t[0]*t[3]-t[1]*t[5]+a3*t[0]**2*t[2]+a4*t[1]**2*t[6]+a5*t[0]*t[1]*t[4]
new=t[0]*(-t[3]+a3*t[0]*t[2]+a5*t[1]*t[4])+t[1]*(-t[5]+a4*t[1]*t[6])
assert sp.expand(f-new)==0
# Rank four excludes a product of two linear forms for this quadratic.
quad=t[0]*t[3]+t[1]*t[5]
assert sp.hessian(quad,t).rank()==4
z=sp.symbols('z1:5');P=z[0]*z[1]*z[3]
published=z[2]**2*z[3]-2*z[0]*z[1]*z[2]*z[3]**2+z[0]**2*z[1]**2*z[3]**3
assert sp.expand(published-z[3]*(z[2]-P)**2)==0
mock=z[3]*(z[2]**2-P**2)
assert sp.expand(mock-z[3]*(z[2]-P)*(z[2]+P))==0
u4=[(0,-1,-1),(1,-1,-1),(0,-2,-1),(-1,0,1)]
assert u4[2]==add(u4[0],u4[1],u4[3])
assert add(scale(2,u4[2]),u4[3])==add(scale(2,u4[0]),scale(2,u4[1]),scale(3,u4[3]))
for j in range(4):assert mock.subs({z[i]:0 for i in range(4) if i!=j})==0
C=counts((2,-4,4));dc=data(2,-4,4)
vs=obstruction_degrees(2,-4,4);assert vs==[(-1,-3,-1)]
quadratic_pairs=[(i,j) for i,j in combinations_with_replacement(range(len(dc)),2) if add(dc[i][1],dc[j][1])==vs[0]]
assert quadratic_pairs==[(0,5)]
assert cup(rays(2,-4,4),(dc[0][0],dc[0][1],c2),(dc[5][0],dc[5][1],c5))=={'5':'-2'}
assert add(dc[4][1],dc[7][1])==(0,0,0)
assert add(scale(2,dc[3][1]),scale(2,dc[6][1]),dc[7][1])==vs[0]
results={'status':'PASS','python':platform.python_version(),'sympy':sp.__version__,
 'claims_not_checked':['No universal tangent-cone theorem','No toric realization of the mock hypersurface','No all-order hull calculation for (2,-4,4)'],
 'count_collision':{'A':A,'B':B,'hull_component_counts':[1,2]},
 'complete_degree_support_A':ma,'complete_degree_support_B':mb,
 'cup_coefficients_A':qa,'cup_coefficients_B':qb,'quadratic_rank_A':4,
 'normalization_identities':'exact symbolic identities passed',
 'mock_hypersurface':{'first_order_weight_relation':[1,1,-1,1],'coordinate_axes_extend':True,'reduced_components':3,'tangent_cone_components':2,'tangent_cone_nonreduced':True},
 'resonant_candidate':{'data':C,'obstruction_degrees':vs,'quadratic_pairs_zero_based':quadratic_pairs,'quadratic_cup_coefficient':'-2','zero_weight_pair_zero_based':[4,7],'allowed_residual_quintic':'c^2 p^2 q','quintic_coefficient':'NOT COMPUTED'}}
print(json.dumps(results,indent=2))
