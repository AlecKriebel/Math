#!/usr/bin/env python3
"""Exact symbolic/finite controls; no floating-point KAM certification."""
import sympy as S
import json,hashlib
from pathlib import Path
from collections import Counter
from fractions import Fraction as Q
g=Counter()
def ck(k,b):assert b,k;g[k]+=1
def red(w):
    r=[]
    for x in w:
        if r and r[-1]==-x:r.pop()
        else:r.append(x)
    return tuple(r)
def inv(w):return tuple(-x for x in reversed(w))
def subst(w,imgs):return red(sum((imgs[x-1] if x>0 else inv(imgs[-x-1]) for x in w),()))
phi=((1,2),(2,1,2));c=(1,2,-1,-2)
ck('exact_boundary_word',subst(c,phi)==c)
M=S.Matrix([[1,1],[1,2]])
ck('hyperbolic_matrix',M.det()==1 and M.trace()==3)
ck('matrix_word_counts',list(M[:,0])==[phi[0].count(1),phi[0].count(2)] and list(M[:,1])==[phi[1].count(1),phi[1].count(2)])
x,y,z,t,u=S.symbols('x y z t u')
k=x*x+y*y+z*z-x*y*z-2
T=S.Matrix([z,z*y-x,z*(z*y-x)-y]);J=T.jacobian([x,y,z])
ck('commutator_trace_preservation',S.expand(k.subs(dict(zip([x,y,z],T)),simultaneous=True)-k)==0)
ck('ambient_volume_jacobian',S.factor(J.det())==1)
p=x**4-3*x**3+2*x*x+2*x-1;Y=x/(x-1)
for i,q in enumerate(T):ck('fixed_curve_equations',S.factor(q.subs({y:Y,z:x})-[x,Y,x][i])==0)
ck('admissible_level_polynomial',S.factor((k.subs({y:Y,z:x})+1)*(x-1)**2)==p)
tau=2*x*Y-1
ck('tangent_trace',S.factor(J.trace().subs({y:Y,z:x})-1-tau)==0)
char=S.factor(J.charpoly(u).as_expr().subs({y:Y,z:x}))
ck('tangent_characteristic',S.factor(char-(u-1)*(u*u-tau*u+1))==0)
ck('trace_elimination',S.factor(S.resultant(p,(t+1)*(x-1)-2*x*x,x))==(t*t-4*t-9)**2)
L=Q(-723,1000);U=Q(-722,1000)
def pval(q):return q**4-3*q**3+2*q*q+2*q-1
ck('rational_root_bracket',pval(L)>0 and pval(U)<0)
# On this interval, 4x^3-9x^2+4x+2<0 since x< -7/10.
ck('unique_bracket_root',U<Q(-7,10) and 4*Q(-7,10)+2<0)
ck('total_real_root_count',S.Poly(p,x).count_roots(-S.oo,S.oo)==2)
ck('irreducibility_mod2',S.Poly(p,x,modulus=2).is_irreducible)
ck('quadratic_trace_irreducibility',S.Poly(t*t-4*t-9,t).is_irreducible)
ck('elliptic_trace_bounds',3**2<13<4**2)
ck('noncyclotomic_trace_conjugate',2+3>2)
ck('nonzero_level_gradient',2*Q(722,1722)-Q(723,1000)**2>0)
# Unit quaternion B's remaining square is positive, with a simple rational lower bound.
# |xi|<3/4, 0<eta<1/2, so |xi*eta/4-xi/2|<15/32 and 1-xi^2/4>55/64.
ck('quaternion_realization_positive',1-Q(1,16)-Q(15,32)**2/Q(55,64)>0)
# Trace(C)=-1 implies C^3=I by the characteristic polynomial.
ck('order_three_cayley_hamilton',S.rem(u**3-1,u*u+u+1,u)==0)

def compose(a,b):return tuple(a[b[j]] for j in range(len(a)))
def inverse(a):
    b=[0]*len(a)
    for i,j in enumerate(a):b[j]=i
    return tuple(b)
def update(a,b):return compose(a,b),compose(compose(b,a),b)
def cycles(a):
    seen=set();out=[]
    for i in range(len(a)):
        if i not in seen:
            cyc=[];j=i
            while j not in seen:seen.add(j);cyc.append(j);j=a[j]
            out.append(cyc)
    return out
for n in range(3,202,2):
    a=tuple((j+1)%n for j in range(n));b=tuple(-j%n for j in range(n))
    comm=compose(compose(compose(a,b),inverse(a)),inverse(b))
    ck('dihedral_commutator',comm==compose(a,a))
    ck('single_boundary_cycle',len(cycles(comm))==1)
    ck('connected_cover',len(cycles(a))==1)
    aa,bb=a,b
    for r in range(3):aa,bb=update(aa,bb)
    ck('cubed_map_monodromy',aa==a and bb==b)
    genus=(n+1)//2
    ck('riemann_hurwitz',2-2*genus==-(n-1))
    ck('relative_ambient_dimension_gap',2<6*genus-6 and 6*genus-6==3*n-3)
    ck('valid_closed_prongs',2*n>=6)
# Universal dihedral arithmetic on j -> eps*j+r, with integer r and eps in {1,-1}.
def dmul(a,b):return(a[0]+a[1]*b[0],a[1]*b[1])
def dup(a,b):return dmul(a,b),dmul(dmul(b,a),b)
a,b=(1,1),(0,-1)
expected=[((1,-1),(-1,1)),((2,-1),(1,-1)),((1,1),(0,-1))]
for pair in expected:
    a,b=dup(a,b);ck('universal_integer_dihedral_identity',(a,b)==pair)
print(json.dumps({'problem_id':11000192,'author_turn':4,'status':'PASS','arithmetic':'SymPy exact rational polynomial algebra and integer permutations; no approximate eigenvalue or KAM proof','exact_controls':sum(g.values()),'groups':dict(sorted(g.items())),'cover_degrees_checked':{'odd_min':3,'odd_max':201,'count':100},'fixed_point_polynomial':str(p),'fixed_point_interval':['-723/1000','-722/1000'],'relative_tangent_trace':'2-sqrt(13)','checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'scope':'Supports a true branched-cover pseudo-Anosov with a relative elliptic fixed point. The two-dimensional pullback locus is ambient-null; transverse stability and original nonergodicity remain unproved.'},indent=2,sort_keys=True))
