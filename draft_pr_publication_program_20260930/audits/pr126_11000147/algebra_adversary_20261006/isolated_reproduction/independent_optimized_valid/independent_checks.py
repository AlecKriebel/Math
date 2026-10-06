"""Independent integer, finite-group and exact quadratic-field controls."""
from fractions import Fraction as F
from itertools import permutations, combinations, product
from pathlib import Path
from hashlib import sha256
import json

counts={}
def ck(cat,p):
    assert p,cat
    counts[cat]=counts.get(cat,0)+1

def mm(a,b):
    return tuple(tuple(sum(a[i][k]*b[k][j] for k in range(2)) for j in range(2)) for i in range(2))
I=((1,0),(0,1)); A=((3,1),(2,1)); B=((1,-2),(-1,3)); C=((8,-11),(3,-4))
def inv(a):return ((a[1][1],-a[0][1]),(-a[1][0],a[0][0]))
for m in (A,B,C):
    ck('determinant_one',m[0][0]*m[1][1]-m[0][1]*m[1][0]==1)
    ck('trace_four',m[0][0]+m[1][1]==4)
    ck('integral_inverse',mm(m,inv(m))==I)
    m2=mm(m,m)
    ck('characteristic_identity',all(m2[i][j]-4*m[i][j]+I[i][j]==0 for i,j in product(range(2),repeat=2)))
for p,q in combinations((A,B,C),2):
    ck('braid_identity',mm(mm(p,q),p)==mm(mm(q,p),q))
    ck('noncommutation',mm(p,q)!=mm(q,p))
    ck('distinct_homology_actions',p!=q)
ck('conjugation',mm(mm(A,B),inv(A))==C)
ck('second_conjugation',mm(mm(inv(B),A),B)==C)
x=((0,1),(-1,0));y=((-2,-1),(3,1))
ck('source_pair_x_square',mm(x,x)==((-1,0),(0,-1)))
ck('source_pair_y_cube',mm(mm(y,y),y)==I)
ck('source_pair_xy',mm(x,y)==A)
ck('source_pair_yx',mm(y,x)==B)

# Exact Q(sqrt(3)) operations; no floating-point eigenvalue tests.
def add(z,w):return (z[0]+w[0],z[1]+w[1])
def mul(z,w):return (z[0]*w[0]+3*z[1]*w[1],z[0]*w[1]+z[1]*w[0])
def scale(z,a):return (a*z[0],a*z[1])
zero=(F(0),F(0)); one=(F(1),F(0))
def qm(a,b):
    return tuple(tuple(add(mul(a[i][0],b[0][j]),mul(a[i][1],b[1][j])) for j in range(2)) for i in range(2))
for m in (A,B,C):
    mat=tuple(tuple((F(m[i][j]),F(0)) for j in range(2)) for i in range(2))
    # P+ = (I + (M-2I)/sqrt(3))/2; P- = I-P+.
    pp=tuple(tuple((F(I[i][j],2),F(m[i][j]-2*I[i][j],6)) for j in range(2)) for i in range(2))
    pm=tuple(tuple((F(I[i][j])-pp[i][j][0],-pp[i][j][1]) for j in range(2)) for i in range(2))
    for p,lam in ((pp,(F(2),F(1))),(pm,(F(2),F(-1)))):
        ck('spectral_projector_idempotent',qm(p,p)==p)
        ck('spectral_scaling',qm(mat,p)==tuple(tuple(mul(lam,z) for z in row) for row in p))
        ck('spectral_rank_one',add(p[0][0],p[1][1])==one)
    ck('spectral_transversality',qm(pp,pm)==((zero,zero),(zero,zero)))

# The universal lemma cannot be proved by finite groups; these are independent controls.
def comp(p,q):return tuple(p[q[i]] for i in range(len(p)))
def pinv(p):return tuple(p.index(i) for i in range(len(p)))
tested_pairs=0
for size in range(2,6):
    group=list(permutations(range(size)))
    for a,b in combinations(group,2):
        if comp(comp(a,b),a)!=comp(comp(b,a),b):continue
        tested_pairs+=1
        c=comp(comp(a,b),pinv(a))
        ck('group_lemma_second_conjugation',c==comp(comp(pinv(b),a),b))
        ck('group_lemma_three_distinct',len({a,b,c})==3)
        for p,q in combinations((a,b,c),2):
            ck('group_lemma_braid',comp(comp(p,q),p)==comp(comp(q,p),q))
            ck('group_lemma_noncommutation',comp(p,q)!=comp(q,p))

for mod in range(2,10):
    def act(m,v):return tuple(sum(m[i][j]*v[j] for j in range(2))%mod for i in range(2))
    for v in product(range(mod),repeat=2):
        for p,q in combinations((A,B,C),2):
            ck('finite_torus_braid',act(p,act(q,act(p,v)))==act(q,act(p,act(q,v))))
    for m in (A,B,C):
        ck('finite_torus_bijection',len({act(m,v) for v in product(range(mod),repeat=2)})==mod*mod)

r=Path(__file__).resolve().parent
out={'artifact_sha256':sha256((r/'author_replay/CANDIDATE.md').read_bytes()).hexdigest(),
     'exact_assertions':sum(counts.values()),'categories':counts,'distinct_finite_group_braid_pairs':tested_pairs,
     'scope':'Independent exact controls; the written group argument and invariant foliations supply the universal proof.'}
(r/'independent_checks.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps(out,sort_keys=True))
