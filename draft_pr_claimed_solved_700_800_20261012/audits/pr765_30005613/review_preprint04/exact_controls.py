"""Fresh exact finite diagnostics. No PDE convergence or infinite theorem certified."""
from fractions import Fraction as F
from itertools import product
from math import isqrt
from pathlib import Path
import json

def need(c,m):
    if not c:raise RuntimeError(m)
def diag(xs):return [[F(x) if i==j else F(0) for j in range(len(xs))] for i,x in enumerate(xs)]
def tr(a):return list(map(list,zip(*a)))
def mul(a,b):return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]
def sub(a,b):return [[x-y for x,y in zip(r,s)] for r,s in zip(a,b)]
def conj(u,a):return mul(mul(u,a),tr(u))

rows=[]
for den in [23,47,95,191]:
    t=F(1,den);c=(1-t*t)/(1+t*t);s=2*t/(1+t*t)
    u=diag([1]*6)
    for i,j in [(0,4),(1,5)]:u[i][i]=u[j][j]=c;u[i][j]=-s;u[j][i]=s
    need(mul(u,tr(u))==diag([1]*6),'orthogonal')
    p0=diag([1,1,0,0,0,0]);q0=diag([1,1,1,1,0,0])
    p=conj(u,p0);q=conj(u,q0);r=conj(u,diag([F(1,3)-t*t,F(1,3)+t*t,F(1,2),F(3,4),F(1,7),F(1,9)]))
    for a,rank in [(p,2),(q,4)]:
        need(mul(a,a)==a and tr(a)==a,'projection');need(sum(a[i][i] for i in range(6))==rank,'rank');need(mul(a,r)==mul(r,a),'commutation')
    need(mul(p,q)==p and mul(q,p)==p,'nesting')
    need(mul(sub(p,p0),sub(p,p0))==diag([s*s,s*s,0,0,s*s,s*s]),'exact norm difference')
    rows.append({'t':str(t),'ranks':[2,4],'projection_distance_exact':str(s),'all_identities':True})
u=[[F(8,17),F(-15,17)],[F(15,17),F(8,17)]];branch=conj(u,diag([1,0]));diff=sub(branch,diag([1,0]));need(mul(diff,diff)==diag([F(225,289)]*2),'branch instability')
qset=[5,9,17,29];maxsum=9*max(qset);bound=isqrt(maxsum);sums={0}
for d in range(5):sums={s+m*m for s in sums for m in range(1,bound+1) if s+m*m<maxsum}
forbidden={F(s,q) for s in sums for q in qset if 4<F(s,q)<9};a=F(19,8);need(a*a not in forbidden and all((q*a*a).denominator!=1 for q in qset),'d5 nonresonance')
geometry=[]
for d in [3,5,7]:
    delta=F(1,11);left=F(13,7);right=left+F(9,7);p=left*2;x2=p+right;count=0
    for offsets in product([F(-1,2),F(0),F(1,2)],repeat=d):
        point=[p+delta*offsets[0]]+[delta*x for x in offsets[1:]]
        old=abs(point[0]-left)<left and all(abs(x)<left for x in point[1:])
        new=abs(point[0]-x2)<right and all(abs(x)<right for x in point[1:])
        need((old or new)==(offsets[0]!=0),'null face connector')
        count+=1
    geometry.append({'dimension':d,'exact_samples':count})
tails=[]
for n in range(1,161):
    m=n+19;tail=F(1,2**(n+1));need(sum(F(1,2**(j+2)) for j in range(n,m))+F(1,2**(m+1))==tail,'tail');need(F(1,2**n)+tail==3*tail,'birth diagonal');tails.append(n)
# Auxiliary quintic profile, C2 after constant continuation, not the proof's C-infinity cutoff.
coeff=[F(0),F(0),F(30),F(-60),F(30)];integral=sum(coeff[i]*coeff[j]/F(i+j+1) for i in range(5) for j in range(5));need(integral==F(10,7),'quintic derivative energy')
result={'status':'PASS_FINITE_DIAGNOSTICS_ONLY','rotations':rows,'single_branch_distance':'15/17','forbidden_d5_squared_widths':len(forbidden),'chosen_width':'19/8','integer_multiindex_bound':bound,'geometry':geometry,'tail_and_birth_pairs':len(tails),'quintic_derivative_squared_integral':str(integral),'profile_warning':'C2 polynomial auxiliary diagnostic; analytic proof uses a smooth flat profile.','not_certified':['capacity and PDE form limits','norm-resolvent convergence','infinite-dimensional completeness','effective apertures','historical priority']}
print(json.dumps(result,indent=2,sort_keys=True))
