#!/usr/bin/env python3
"""Independent exact diagnostics; no author checker or library imported.
Counts exact identities actually tested, not a proof of the infinite statements.
"""
from itertools import product
from collections import Counter
import json, random

counts=Counter(); models=Counter()
def ck(p,tag):
    counts[tag]+=1
    if not p: raise AssertionError(tag)

def table(xs,op):
    ix={x:i for i,x in enumerate(xs)}
    return [[ix[op(a,b)] for b in xs] for a in xs]
def inverses(m):
    n=len(m); inv=[]
    for a in range(n):
        good=[b for b in range(n) if m[a][b]==m[b][a] and m[m[a][b]][a]==a and m[m[b][a]][b]==b]
        ck(len(good)==1,'unique_commuting_inverse'); inv.append(good[0])
    return inv

def sg_check(m,inv):
    for a,b,c in product(range(len(m)),repeat=3): ck(m[m[a][b]][c]==m[a][m[b][c]],'multiplication_associative')
    for a in range(len(m)):
        b=inv[a];ck(m[a][b]==m[b][a] and m[m[a][b]][a]==a and m[m[b][a]][b]==b,'inverse_axioms')

def source_map(m,inv,plus):
    n=len(m)
    return [[(m[a][plus[inv[a]][b]],m[inv[plus[inv[a]][b]]][b]) for b in range(n)] for a in range(n)]
def compatible(m,inv,plus):
    n=len(m)
    return all(m[a][plus[b][c]]==plus[m[a][b]][m[a][plus[inv[a]][c]]] for a,b,c in product(range(n),repeat=3))
def braid(r, count=False):
    n=len(r)
    for a,b,c in product(range(n),repeat=3):
        x,y=r[a][b]; u,v=r[y][c]; s,t=r[x][u]; L=(s,t,v)
        x,y=r[b][c]; u,v=r[a][x]; s,t=r[v][y]; R=(u,s,t)
        if count:
            for i in range(3): ck(L[i]==R[i],'full_braid_coordinate')
        elif L!=R:return False
    return True

def retracted(m,inv,f):
    n=len(m); return source_map(m,inv,[f[:] for _ in range(n)])

def meet_controls():
    # A three-element chain, a fork without a top, and a Boolean diamond.
    for xs,op in [([0,1,2],min),([0,1,2],lambda a,b:a if a==b else 0),([0,1,2,3],lambda a,b:a&b)]:
        m=table(xs,op); n=len(m); inv=list(range(n));sg_check(m,inv)
        for ft in product(range(n),repeat=n):
            f=list(ft); idem=all(f[f[x]]==f[x] for x in range(n))
            if not idem:continue
            lower=all(f[m[x][f[y]]]==m[x][f[y]] for x,y in product(range(n),repeat=2))
            plus=[f[:] for _ in range(n)]
            ck(compatible(m,inv,plus)==lower,'meet_compatibility_characterization')
            if not lower:continue
            monotone=all(m[a][b]!=a or m[f[a]][f[b]]==f[a] for a,b in product(range(n),repeat=2))
            down=all(m[f[a]][a]==f[a] for a in range(n))
            r=source_map(m,inv,plus)
            ck(braid(r)==(monotone and down),'meet_ybe_iff')
            if monotone and down:braid(r,True)
            models['meet_retractions']+=1

def projection_controls():
    # Enumerate all labeled associative binary laws on sets of size <=3.
    for n in (1,2,3):
        L=[[a for b in range(n)] for a in range(n)]
        R=[[b for b in range(n)] for a in range(n)]
        inv=list(range(n)); triples=list(product(range(n),repeat=3))
        assoc=0
        for flat in product(range(n),repeat=n*n):
            p=[list(flat[i*n:(i+1)*n]) for i in range(n)]
            if not all(p[p[a][b]][c]==p[a][p[b][c]] for a,b,c in triples):continue
            assoc+=1
            band=all(p[a][a]==a for a in range(n))
            rectangular=all(p[p[a][b]][c]==p[a][c] for a,b,c in triples)
            ck(compatible(L,inv,p)==band,'left_projection_compatibility')
            ck(compatible(R,inv,p)==rectangular,'right_projection_compatibility')
            if band:braid(source_map(L,inv,p),True)
            if rectangular:braid(source_map(R,inv,p),True)
        models['associative_labeled_laws_n'+str(n)]=assoc

def d4mul(a,b):return ((a[0]+(-1 if a[1] else 1)*b[0])%4,(a[1]+b[1])%2)
def d4inv(a):return (((1 if a[1] else -1)*a[0])%4,a[1])
D4=list(product(range(4),range(2))); one=(0,0)

def rees(xsG,mulg,invg,P):
    rows=len(P[0]); cols=len(P)
    xs=list(product(range(rows),xsG,range(cols)))
    def op(a,b):return (a[0],mulg(mulg(a[1],P[a[2]][b[0]]),b[1]),b[2])
    def iv(a):
        q=invg(P[a[2]][a[0]])
        return (a[0],mulg(mulg(q,invg(a[1])),q),a[2])
    m=table(xs,op); idx={x:i for i,x in enumerate(xs)};inv=[idx[iv(a)] for a in xs]
    sg_check(m,inv)
    return xs,m,inv,idx

def rees_exhaustive():
    xs,m,iv,ix=rees(list(range(3)),lambda a,b:(a+b)%3,lambda a:-a%3,[[0],[1],[2]])
    J=[i for i,x in enumerate(xs) if x[2] in (0,1)]; out=[i for i in range(len(xs)) if i not in J]
    for images in product(J,repeat=len(out)):
        f=list(range(len(xs)))
        for i,z in zip(out,images):f[i]=z
        ck(compatible(m,iv,[f[:] for _ in xs]),'rees_retraction_compatible')
        h=[m[iv[f[b]]][b] for b in range(len(xs))]
        crit=all(xs[f[b]][0]==xs[b][0] and f[h[b]]==m[f[b]][iv[f[b]]] for b in range(len(xs)))
        r=retracted(m,iv,f); actual=braid(r)
        ck(actual==crit,'rees_all_retractions_iff')
        if actual:braid(r,True)
        models['exhaustive_C3_retractions']+=1
        models['exhaustive_C3_solutions']+=actual

def rees_noncommutative():
    P=[[(1,0),(0,1)],[(1,1),(1,0)],[(3,0),(2,1)]]
    xs,m,iv,ix=rees(D4,d4mul,d4inv,P); n=len(xs)
    factor=all(P[mu][j]==d4mul(d4mul(P[mu][0],d4inv(P[0][0])),P[0][j]) for mu in range(3) for j in range(2))
    ck(not factor,'nonfactorizing_sandwich_negative_control')
    ck(compatible(m,iv,m)==factor,'coinciding_law_factorization_iff')
    # Independent one-column change of coordinates, with a genuinely nonfactorizing matrix.
    v=P[0]; newP=[[d4mul(z,d4inv(v[j])) for j,z in enumerate(row)] for row in P]
    def norm(a):return (a[0],d4mul(v[a[0]],a[1]),a[2])
    def newop(a,b):return (a[0],d4mul(d4mul(a[1],newP[a[2]][b[0]]),b[1]),b[2])
    for a,b in product(range(n),repeat=2):ck(norm(xs[m[a][b]])==newop(norm(xs[a]),norm(xs[b])),'one_column_noncomm_normalization')
    anti=all(iv[m[a][b]]==m[iv[b]][iv[a]] for a,b in product(range(n),repeat=2))
    ck(not anti,'global_anti_inverse_negative_control')
    rng=random.Random(314159)
    for model in range(6):
        # Six arbitrary fiber retractions. Some H-images are not subgroups and do not contain 1.
        H={}; kap={}
        for row in range(2):
            A,B=rng.sample(D4,2)
            hg={g:(A if rng.randrange(2)==0 else B) for g in D4}; hg[A]=A;hg[B]=B
            col={A:rng.randrange(2),B:rng.randrange(2)}
            H[row]=hg;kap[row]={g:col[hg[g]] for g in D4}
        f=[]
        for a in xs:
            row,g,mu=a
            if mu in (0,1):f.append(ix[a]);continue
            h=H[row][g];nu=kap[row][g]
            image=(row,d4mul(d4mul(g,d4inv(h)),d4inv(P[nu][row])),nu)
            f.append(ix[image])
        for b,a in enumerate(xs):
            ck(f[f[b]]==f[b],'noncomm_retraction')
            residual=m[iv[f[b]]][b]
            ck(f[residual]==m[f[b]][iv[f[b]]],'noncomm_residual')
            if a[2]==2:ck(xs[residual]==(a[0],H[a[0]][a[1]],2),'noncomm_H_parameter_order')
        ck(compatible(m,iv,[f[:] for _ in xs]),'noncomm_compatibility')
        braid(retracted(m,iv,f),True);models['D4_parameter_solutions']+=1
    # Direct substitution for both projection additions, without inverse anti-law.
    for side in (0,1):
        p=[[a if side==0 else b for b in range(n)] for a in range(n)]
        r=source_map(m,iv,p)
        e=[m[a][iv[a]] for a in range(n)]
        criterion=all(e[m[a][b]]==(e[m[a][e[b]]] if side==0 else e[m[e[a]][b]]) for a,b in product(range(n),repeat=2))
        ck(braid(r)==criterion,'projection_addition_crypt_criterion')
        for a,b in product(range(n),repeat=2):
            ck(r[a][b]==((e[a],m[a][b]) if side==0 else (m[a][b],e[b])),'projection_addition_source_substitution')


def clifford_controls():
    # Diamond of groups: top D4, two C2 groups, bottom trivial.
    xs=[(0,0,0)]+[(s,t,0) for s in (1,2) for t in (0,1)]+[(3,a,b) for a,b in D4]
    def restrict(x,s):
        lev,a,b=x
        if s==0:return (0,0)
        if lev==s:return (a,b)
        assert lev==3
        return (a%2,0) if s==1 else (b,0)
    def op(x,y):
        s=x[0]&y[0]; a=restrict(x,s);b=restrict(y,s)
        z=d4mul(a,b) if s==3 else ((a[0]+b[0])%2,0) if s else (0,0)
        return(s,*z)
    m=table(xs,op);iv=inverses(m);sg_check(m,iv);n=len(xs);ix={x:i for i,x in enumerate(xs)}
    e=[m[a][iv[a]] for a in range(n)]
    for a,b in product(range(n),repeat=2):
        ck(m[e[a]][b]==m[b][e[a]],'Clifford_central_idempotents')
        ck(iv[m[a][b]]==m[iv[b]][iv[a]],'Clifford_valid_anti_inverse')
    rng=random.Random(271828)
    for F in ({0},{0,1},{0,2},{0,1,2},{0,1,2,3}):
        J=[i for i,x in enumerate(xs) if x[0] in F];out=[i for i in range(n) if i not in J]
        tau={}
        for lev in range(4):
            below=[d for d in F if d&lev==d]
            greatest=[d for d in below if all(q&d==q for q in below)]
            tau[lev]=greatest[0] if greatest else None
        canonical=None
        if all(v is not None for v in tau.values()):
            canonical=[m[ix[(tau[x[0]],0,0)]][i] for i,x in enumerate(xs)]
        fs=[]
        if canonical is not None:fs.append(canonical)
        for _ in range(32):
            f=list(range(n))
            for b in out:f[b]=rng.choice(J)
            fs.append(f)
        for f in fs:
            ck(compatible(m,iv,[f[:] for _ in xs]),'Clifford_retraction_compatible')
            pred=(canonical is not None and f==canonical)
            ck(braid(retracted(m,iv,f))==pred,'Clifford_greatest_idempotent_iff')
            if pred:
                braid(retracted(m,iv,f),True)
                for a,b in product(range(n),repeat=2):ck(f[m[a][b]]==m[f[a]][f[b]],'Clifford_canonical_endomorphism')
            models['Clifford_retractions']+=1

def rectangle_failure():
    xs=list(product(range(2),repeat=2));m=table(xs,lambda a,b:(a[0],b[1])); iv=list(range(4))
    p=[[0 if a==0 or b==0 else 2 for b in range(4)] for a in range(4)]
    for a,b,c in product(range(4),repeat=3):ck(p[p[a][b]][c]==p[a][p[b][c]],'rectangular_bad_addition_associative')
    ck(compatible(m,iv,p),'rectangular_bad_addition_compatible');ck(not braid(source_map(m,iv,p)),'rectangular_braid_failure')
    # Genuinely two-argument addition and noncommuting multiplicative group component.
    prodxs=list(product(range(4),D4));idx={x:i for i,x in enumerate(prodxs)}
    pm=table(prodxs,lambda a,b:(m[a[0]][b[0]],d4mul(a[1],b[1])))
    pp=table(prodxs,lambda a,b:(p[a[0]][b[0]],d4mul(a[1],b[1])))
    pinv=[idx[(a[0],d4inv(a[1]))] for a in prodxs]
    ck(compatible(pm,pinv,pp),'two_argument_product_compatible');ck(not braid(source_map(pm,pinv,pp)),'two_argument_product_fails')
    ck(compatible(pm,pinv,pm),'same_multiplication_good_compatible');braid(source_map(pm,pinv,pm),True)

meet_controls();projection_controls();rees_exhaustive();rees_noncommutative();clifford_controls();rectangle_failure()
print(json.dumps({'status':'PASS','exact_assertions':sum(counts.values()),'counts':dict(sorted(counts.items())),'models':dict(sorted(models.items())),'scope':'Finite diagnostics only; infinite necessity/sufficiency and source scope are audited separately.'},indent=2,sort_keys=True))
