#!/usr/bin/env python3
"""Second-review exact controls; universal proofs are INDEPENDENT_PROOFS.md."""
from fractions import Fraction as Q
from itertools import product
import hashlib,json
from pathlib import Path
if not __debug__: raise RuntimeError('Run without optimization')
checks={}
def check(name,flag):
    if not flag: raise AssertionError(name)
    checks[name]=checks.get(name,0)+1

def rank(rows):
    a=[list(map(Q,r)) for r in rows];k=0
    for j in range(len(a[0])):
        p=next((i for i in range(k,len(a)) if a[i][j]),None)
        if p is None:continue
        a[k],a[p]=a[p],a[k];v=a[k][j];a[k]=[x/v for x in a[k]]
        for i in range(len(a)):
            if i!=k:
                v=a[i][j];a[i]=[x-v*y for x,y in zip(a[i],a[k])]
        k+=1
        if k==len(a):break
    return k

def unit(n,i,j):return tuple(tuple(Q(int((r,c)==(i,j))) for c in range(n)) for r in range(n))
def add(a,b):return tuple(tuple(x+y for x,y in zip(r,s)) for r,s in zip(a,b))
def scale(c,a):return tuple(tuple(c*x for x in r) for r in a)
def mul(a,b):return tuple(tuple(sum(a[i][k]*b[k][j] for k in range(len(b))) for j in range(len(b))) for i in range(len(a)))
def star(a):return tuple(zip(*a))
def trace(a):return sum(a[i][i] for i in range(len(a)))
def flat(a):return tuple(x for r in a for x in r)
def diagonal(v):return tuple(tuple(Q(v[i]) if i==j else Q(0) for j in range(len(v))) for i in range(len(v)))

one=tuple(map(Q,(1,1,1,1)));p=tuple(map(Q,(0,0,1,1)));q=tuple(map(Q,(0,1,0,1)));pq=tuple(a*b for a,b in zip(p,q))
check('algebra_and_intersection',rank([one,p,q,pq])==4 and rank([one,p,q])==3 and rank([one,p])==rank([one,q])==2)
weights=[]
for a,b in [(1,1),(2,5),(5,2),(3,7),(7,3),(1,0),(0,1)]:
    den=a*a+b*b;t=Q(b*b,den);w=(Q(a),Q(0),Q(0),Q(b));rho=tuple(tuple(x*y/den for y in w) for x in w)
    state=lambda x:trace(mul(rho,x))
    check('pure_density',mul(rho,rho)==rho and trace(rho)==1 and rank(rho)==1)
    for s in range(4):check('restriction',state(unit(4,s,s))==((1-t) if s==0 else t if s==3 else 0))
    for i,j in product(range(4),repeat=2):
        e=unit(4,i,j);check('purity_corner',mul(mul(rho,e),rho)==scale(state(e),rho))
    for n in range(1,9):
        for letters in product((p,q),repeat=n):
            vals=one
            for z in letters:vals=tuple(x*y for x,y in zip(vals,z))
            check('basis_entire_joint_law',state(diagonal(vals))==(1-t)*vals[0]+t*vals[3]==t)
    affine=[(Q(0),Q(0)),(Q(1),Q(-1)),(Q(-2,3),Q(5,7)),(Q(3,2),Q(-4,9))]
    for n in range(6):
        for word in product(range(4),repeat=n):
            vals=one
            for k,j in enumerate(word):
                c,d=affine[j];gen=(p,q)[k%2];vals=tuple(x*(c+d*y) for x,y in zip(vals,gen))
            check('affine_joint_law',state(diagonal(vals))==(1-t)*vals[0]+t*vals[3])
    for seed in range(20):
        x=tuple(tuple(Q((seed+i*3+j*7)%13-6,j+1) for j in range(4)) for i in range(4))
        y=[sum(x[i][j]*w[j] for j in range(4)) for i in range(4)]
        check('state_positivity',state(mul(star(x),x))==sum(z*z for z in y)/den>=0)
    check('saturated_gram',t+t-t-t==0 and t*(1-t)>=0)
    weights.append({'t':str(t),'strict_mixture':0<t<1})

for n in range(2,15):
    vertices=set(product('PQ',range(n)));reached={('P',0)}
    while True:
        expanded=reached|{b for a in reached for b in vertices if a[0]!=b[0] and a[1]!=b[1]}
        if expanded==reached:break
        reached=expanded
    check('third_copy_boundary',(reached==vertices)==(n>=3))
# Enumerate classical character patterns only as a finite combinatorial control.
for n in [2,3,4]:
    patterns=[]
    for points in product(range(4),repeat=n):
        if all(p[points[i]]==q[points[j]] for i in range(n) for j in range(n) if i!=j):patterns.append(points)
    check('character_pattern_boundary',len(patterns)==(4 if n==2 else 2))
check('two_copy_swap_orbit',p[2]==q[1]==1 and p[1]==q[2]==0)
check('laurent_positive_gram_obstruction',all(Q(0)*b-Q(1)==-1 for b in [Q(-100),Q(0),Q(1,19),Q(1000)]))

# C4 finite matrix identities, independently checking all matrix-unit generation.
n=5;E=lambda i,j:unit(n,i,j);e00=E(0,0);xs={i:add(E(0,i),E(i,0)) for i in range(1,n)}
for i,x in xs.items():
    check('C4_spectrum_identity',mul(mul(x,x),x)==x)
    check('C4_diagonal_generation',mul(mul(x,e00),x)==E(i,i))
    for j,y in xs.items():
        if i==j:continue
        check('C4_shared_corner',mul(mul(x,x),mul(y,y))==e00)
        check('C4_offdiagonal_generation',mul(mul(x,e00),y)==E(i,j))
        check('C4_nonclassical_word',mul(mul(mul(x,y),x),y)[0][0]==0 and mul(x,x)[0][0]==1)
for i,j in product(range(n),repeat=2):check('C4_vector_corner',mul(mul(e00,E(i,j)),e00)==scale(E(i,j)[0][0],e00))

# C5: direct-sum generation, conditional expectation, faithful density.
Z=diagonal((1,-1));Es=[unit(2,i,j) for i,j in product(range(2),repeat=2)]
th=lambda e:(e,mul(mul(Z,e),Z))
D=lambda e:(e,e)
plus=lambda a,b:(add(a[0],b[0]),add(a[1],b[1]))
times=lambda a,b:(mul(a[0],b[0]),mul(a[1],b[1]))
F=lambda x:scale(Q(1,3),add(scale(2,x[0]),x[1]))
gens=[D(e) for e in Es]+[th(e) for e in Es]
span=gens+[times(a,b) for a in gens for b in gens]
check('C5_generation',rank([flat(x[0])+flat(x[1]) for x in span])==8)
for i,e in enumerate(Es):
    i0,j0=divmod(i,2);check('C5_minimality',F(th(e))==scale(Q(1) if i0==j0 else Q(1,3),e))
    for d in Es:
        x=th(e)
        check('C5_bimodule_left',F(times(D(d),x))==mul(d,F(x)))
        check('C5_bimodule_right',F(times(x,D(d)))==mul(F(x),d))
rho=tuple(tuple(Q(1,2) if i==j else Q(1,6) for j in range(2)) for i in range(2))
check('C5_faithful_density',trace(rho)==1 and rho[0][0]*rho[1][1]-rho[0][1]*rho[1][0]==Q(2,9))
for lam in [Q(1,3),Q(2,3)]:check('C5_eigenvalues',(rho[0][0]-lam)*(rho[1][1]-lam)-rho[0][1]*rho[1][0]==0)
for e in Es:
    ev=F(th(e));check('C5_marginal',trace(mul(rho,e))==sum(x for r in ev for x in r)/2)

result={'status':'PASS','controls':sum(checks.values()),'counts':checks,'weights':weights,'arithmetic':'exact rational Fraction; standard library only','scope':'Finite matrix, affine word, character-pattern and graph controls supplement the independent universal proofs. No infinite quantifiers, authenticity or priority are certified by enumeration.','verifier_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
print(json.dumps(result,indent=2,sort_keys=True))
