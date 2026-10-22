#!/usr/bin/env python3
"""Exact finite diagnostics for the explicitly scoped ground-state results.

Run beside PARTIAL.md. Universal statements are proved in that file.
Requires SymPy; no numerical eigensolver is used.
"""
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations, product
from pathlib import Path
import json
import sympy as s

counts=Counter()
def ck(cat, ok):
    assert bool(ok), cat
    counts[cat]+=1
def det(a):
    n=len(a)
    if n==0:return F(1)
    if n==1:return a[0][0]
    return sum((-1)**j*a[0][j]*det([row[:j]+row[j+1:] for row in a[1:]]) for j in range(n))
def psd(a):
    n=len(a)
    return all(det([[a[i][j] for j in ids] for i in ids])>=0 for k in range(1,n+1) for ids in combinations(range(n),k))
def affine(m,d,t):
    return [[F(m[i][j])+t*d[i][j] for j in range(len(m))] for i in range(len(m))]
def zero(a):return all(s.simplify(x)==0 for x in a)
def tr(a):return s.simplify(s.trace(a))

# All 2x2 integer directions in this finite box: exact principal-minor tests.
for q,c,r,z in product((1,2,5),range(-3,4),range(-3,4),range(-3,4)):
    m=[[0,0],[0,q]];d=[[c,r],[r,z]]
    criterion=c>=0 and (c!=0 or r==0)
    t=F(1,32*(1+abs(c)+2*abs(r)+abs(z))**2)
    ck('two_by_two_radial_criterion',psd(affine(m,d,t))==criterion)
    for t2 in (F(1,8),F(1),F(3)):
        ck('two_by_two_necessity',not psd(affine(m,d,t2)) or criterion)

# Ground-kernel dimension two, including a non-coordinate null direction.
m=[[0,0,0],[0,0,0],[0,0,1]]
for a,b,r1,r2,z in product(range(-2,3),range(-2,3),range(-2,3),range(-2,3),(-2,0,2)):
    if a==b==0:continue
    c=[[a*a,a*b],[a*b,b*b]]
    d=[[c[0][0],c[0][1],r1],[c[1][0],c[1][1],r2],[r1,r2,z]]
    criterion=-b*r1+a*r2==0
    t=F(1,256*(1+sum(abs(x) for row in d for x in row))**2)
    ck('rank_one_compression_null_coupling',psd(affine(m,d,t))==criterion)
for c11,c12,c22,r1,r2,z in product((1,2,4),(-1,0,1),(1,2,4),(-2,0,2),(-2,0,2),(-2,0,2)):
    if c11*c22-c12*c12<=0:continue
    d=[[c11,c12,r1],[c12,c22,r2],[r1,r2,z]]
    t=F(1,256*(1+sum(abs(x) for row in d for x in row))**2)
    ck('positive_kernel_compression_sufficiency',psd(affine(m,d,t)))
for r1,r2,z in product(range(-2,3),range(-2,3),(-2,0,2)):
    d=[[0,0,r1],[0,0,r2],[r1,r2,z]]
    ck('zero_kernel_compression',psd(affine(m,d,F(1,100)))==(r1==r2==0))

# Kernel equals the entire Hilbert space: the test reduces to positivity of D.
for a,b,c in product(range(-2,3),repeat=3):
    d=[[a,b],[b,c]]
    ck('zero_slack_boundary_case',psd(affine([[0,0],[0,0]],d,F(1,17)))==psd(d))

I=s.I
V=s.Matrix([[1,1],[1,-1],[1,-I],[1,I],[s.sqrt(2),0],[0,s.sqrt(2)],[0,0]])/s.sqrt(6)
e=s.eye(7)[:,6]
B=[s.diag(1,-1,0,0,0,0,0),s.diag(0,0,1,-1,0,0,0),s.diag(0,0,0,0,1,-1,0)]
pauli=[s.Matrix([[0,1],[1,0]]),s.Matrix([[0,-I],[I,0]]),s.diag(1,-1)]
P=s.simplify(V*V.conjugate().T+e*e.T)
A=s.eye(7)-P
ck('seven_dimensional_isometry',zero(V.conjugate().T*V-s.eye(2)))
ck('seven_dimensional_projection',zero(P*P-P))
ck('seven_dimensional_projection',zero(A*A-A))
ck('seven_dimensional_projection',A.rank()==4 and P.rank()==3)
for i in range(3):
    ck('Pauli_compression',zero(s.simplify(V.conjugate().T*B[i]*V)-pauli[i]/3))
    ck('critical_state',zero(B[i]*e))
    for j in range(3):ck('commuting_source_observables',zero(B[i]*B[j]-B[j]*B[i]))
ck('independent_identity_and_observables',s.Matrix.hstack(*[s.Matrix(list(x)) for x in [s.eye(7)]+B]).rank()==4)
rho0=e*e.T;rho1=V*V.conjugate().T/2
for rho in (rho0,rho1):
    ck('different_ensemble_representatives',tr(rho)==1)
    ck('different_ensemble_representatives',zero(A*rho))
    for bi in B:ck('different_ensemble_representatives',tr(bi*rho)==0)
ck('different_ensemble_representatives',rho0!=rho1 and rho0.rank()==1 and rho1.rank()==2)
ck('maximal_optimal_support',(rho0+rho1).rank()==3)
x,y,z,w=s.symbols('x y z w',real=True)
xi=s.Matrix([x+I*y,z+I*w])
bloch=[s.expand((xi.conjugate().T*p*xi)[0]) for p in pauli]
ck('pure_unique_Bloch_identity',s.expand(sum(v*v for v in bloch)-(x*x+y*y+z*z+w*w)**2)==0)
for coords in product(range(-2,3),repeat=4):
    values={x:coords[0],y:coords[1],z:coords[2],w:coords[3]}
    bv=[v.subs(values) for v in bloch]
    ck('pure_unique_exact_controls',all(v==0 for v in bv)==all(c==0 for c in coords))
d1,d2,d3,lam=s.symbols('d1 d2 d3 lam',real=True)
D=d1*pauli[0]+d2*pauli[1]+d3*pauli[2]
ck('parameter_unique_Pauli_spectrum',s.expand(D.det()+d1*d1+d2*d2+d3*d3)==0)
ck('parameter_unique_Pauli_spectrum',s.expand(s.trace(D))==0)
for ds in product(range(-2,3),repeat=3):
    if not any(ds):continue
    dd=D.subs(dict(zip((d1,d2,d3),ds)))
    ck('parameter_unique_exact_directions',dd.det()<0)

# Hermitian (real-linear) measurement rank on the three-dimensional optimal support.
compressed=[s.eye(3)]+[s.diag(p/3,s.zeros(1,1)) for p in pauli]
hb=[]
for i in range(3):
    h=s.zeros(3);h[i,i]=1;hb.append(h)
for i in range(3):
    for j in range(i+1,3):
        h=s.zeros(3);h[i,j]=h[j,i]=1;hb.append(h)
        h=s.zeros(3);h[i,j]=I;h[j,i]=-I;hb.append(h)
measure=s.Matrix([[tr(c*h) for h in hb] for c in compressed])
ck('ensemble_support_test',measure.shape==(4,9) and measure.rank()==4 and len(measure.nullspace())==5)

# Exact small examples and source quantifiers.
beta=s.symbols('beta',real=True)
B2=s.Matrix([[0,1],[1,0]]);M=s.diag(0,1)
ck('off_diagonal_obstruction',s.expand((M+beta*B2).det())==-beta**2)
ck('regular_ground_point',s.Matrix.hstack(s.Matrix([1,0]),B2*s.Matrix([1,0])).rank()==2)
bd=s.diag(-1,0,1)
for bb in (-3,-1,0,1,3):
    ck('unique_parameter_many_pure_states',all(bb*v>=0 for v in (-1,0,1))==(bb==0))
psi=s.Matrix([1,0,1])/s.sqrt(2);aa=-psi*psi.T
ck('critical_value_unique_state',zero(aa*psi+psi))
ck('critical_value_unique_state',(aa+s.eye(3)).rank()==2)
ck('critical_value_unique_state',s.Matrix.hstack(psi,bd*psi).rank()==2)
ck('critical_value_unique_state',zero(bd*s.Matrix([0,1,0])))
ck('unique_state_many_parameters',s.diag(0,1)+beta*s.diag(0,1)==s.diag(0,1+beta))
ck('no_boundary_parameter',(s.Matrix([[0,1],[1,0]])+beta*s.diag(0,1)).det()==-1)

root=Path(__file__).resolve().parent
out={'verdict':'PASS','assertions':sum(counts.values()),'categories':dict(counts),
     'artifact_sha256':sha256((root/'PARTIAL.md').read_bytes()).hexdigest(),
     'sympy_version':s.__version__,
     'scope':'Exact matrix diagnostics; universal kernel/support theorems are proved in PARTIAL.md. No new general pure-state classification or infinite-dimensional result.'}
(root/'verification.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))

