#!/usr/bin/env python3
"""Fresh falsification controls; no packaged helper import.

Uses complete group-word expansion, integral unitriangular matrices, a
mixed two-variable nilpotent ring, and exhaustive finite-field matrices.
Finite evaluations are not substituted for the all-ideal-power proof.
"""
from pathlib import Path
from datetime import datetime,timezone
from itertools import product
from collections import Counter
import hashlib,json,random
HERE=Path(__file__).resolve().parent;C=Counter()
def ck(ok,label):
    assert ok,label
    C[label]+=1
def invword(w):return tuple(-g for g in reversed(w))
def reduceword(w):
    out=[]
    for a in w:
        if out and out[-1]==-a:out.pop()
        else:out.append(a)
    return tuple(out)
def wc(a,b):return reduceword(a+b+invword(a)+invword(b))
x1=(1,);x2=(2,);x3=(3,)
U=wc(x1,x2);w=wc(wc(U,wc(x1,x3)),x1);v=wc(wc(U,wc(x1,U)),x1)
def subst(word,images):
    return reduceword(tuple(z for g in word for z in (images[g] if g>0 else invword(images[-g]))))
def ncadd(a,b,sign=1):
    out=dict(a)
    for m,c in b.items():out[m]=out.get(m,0)+sign*c
    return {m:c for m,c in out.items() if c}
def ncmul(a,b,degree):
    out={}
    for u,c in a.items():
        for v,d in b.items():
            if len(u)+len(v)<=degree:out[u+v]=out.get(u+v,0)+c*d
    return {m:c for m,c in out.items() if c}
def ncc(a,b,degree):return ncadd(ncmul(a,b,degree),ncmul(b,a,degree),-1)
def magnus(word,degree):
    out={():1}
    for a in word:
        t={():1,(a,):1} if a>0 else {tuple([-a]*i):(-1)**i for i in range(degree+1)}
        out=ncmul(out,t,degree)
    return ncadd(out,{():1},-1)
def ident(n):return tuple(tuple(int(i==j) for j in range(n)) for i in range(n))
def madd(a,b,sign=1):return tuple(tuple(x+sign*y for x,y in zip(r,s)) for r,s in zip(a,b))
def mm(a,b,mod=None):
    n=len(a)
    out=tuple(tuple(sum(a[i][k]*b[k][j] for k in range(n)) for j in range(n)) for i in range(n))
    return tuple(tuple(v%mod for v in r) for r in out) if mod else out
def mc(a,b,mod=None):
    out=madd(mm(a,b),mm(b,a),-1)
    return tuple(tuple(v%mod for v in r) for r in out) if mod else out
def ut(n,edges):
    a=[list(r) for r in ident(n)]
    for i,j in edges:a[i-1][j-1]+=1
    return tuple(map(tuple,a))
def utinv(a):
    n=len(a);N=madd(a,ident(n),-1);term=ident(n);out=term
    for k in range(1,n):term=mm(term,N);out=madd(out,term,(-1)**k)
    ck(mm(a,out)==ident(n) and mm(out,a)==ident(n),'unitriangular_inverse')
    return out
def evaluate_int(word,images):
    inverses={i:utinv(a) for i,a in images.items()};out=ident(len(next(iter(images.values()))))
    for g in word:out=mm(out,images[g] if g>0 else inverses[-g])
    return out

# Z[e,t]/(e,t)^9; it embeds in the corresponding Q-algebra.
MAX=8
def pa(a,b,sign=1):
    o=dict(a)
    for m,c in b.items():o[m]=o.get(m,0)+sign*c
    return {m:c for m,c in o.items() if c}
def pm(a,b):
    o={}
    for u,c in a.items():
        for v,d in b.items():
            z=(u[0]+v[0],u[1]+v[1])
            if sum(z)<=MAX:o[z]=o.get(z,0)+c*d
    return {m:c for m,c in o.items() if c}
ONE={(0,0):1};ZERO={}
def pminus(a):return {m:-c for m,c in a.items()}
def pinv1(a):
    out=ONE;term=ONE
    for k in range(1,MAX+1):term=pm(term,a);out=pa(out,term,(-1)**k)
    ck(pm(pa(ONE,a),out)==ONE,'nilpotent_scalar_inverse')
    return out
def pmatmul(a,b):
    return tuple(tuple(pa(pm(a[i][0],b[0][j]),pm(a[i][1],b[1][j])) for j in range(2)) for i in range(2))
PI=((ONE,ZERO),(ZERO,ONE))
def pmatinv(a):return ((a[1][1],pminus(a[0][1])),(pminus(a[1][0]),a[0][0]))
def chart(a,b,c):
    M=((pa(ONE,a),b),(c,pm(pa(ONE,pm(b,c)),pinv1(a))))
    ck(pa(pm(M[0][0],M[1][1]),pm(M[0][1],M[1][0]),-1)==ONE,'mixed_ring_determinant_one')
    ck(pmatmul(M,pmatinv(M))==PI,'mixed_ring_matrix_inverse')
    return M
def peval(word,images):
    out=PI
    for g in word:out=pmatmul(out,images[g] if g>0 else pmatinv(images[-g]))
    return out
def order(M):
    entries=[pa(M[i][j],PI[i][j],-1) for i in range(2) for j in range(2)]
    return min((sum(m) for e in entries for m in e),default=None)
def main():
    started=datetime.now(timezone.utc).isoformat();rows=[]
    for word,target,n,k,monomial,coef in [(w,4,4,5,(1,1,2,1,3),-1),(v,3,3,6,(1,1,1,2,1,2),1)]:
        im={i:(i,) for i in range(1,n+1)};im[target]=(target,)+word
        iv={i:(i,) for i in range(1,n+1)};iv[target]=(target,)+invword(word)
        for i in range(1,n+1):
            ck(subst(subst((i,),im),iv)==(i,) and subst(subst((i,),iv),im)==(i,),'both_automorphism_compositions')
        expansion=magnus(word,k)
        ck(all(len(m)==k for m in expansion),'first_possible_Magnus_degree')
        ck(expansion.get(monomial)==coef,'integral_coefficient_witness')
        A={(1,):1};B={(2,):1};D={(3,):1}
        expected=ncc(ncc(ncc(A,B,k),ncc(A,D,k),k),A,k) if k==5 else ncc(ncc(ncc(A,B,k),ncc(A,ncc(A,B,k),k),k),A,k)
        ck(expansion==expected,'full_word_series_matches_free_associative_bracket')
        rows.append({'word':'w' if k==5 else 'v','reduced_length':len(word),'degree':k,'leading_terms':len(expansion),'coefficients':{''.join(map(str,m)):c for m,c in sorted(expansion.items())}})
    bad={1:(1,),2:(2,),3:(3,)+w};bad_inv={1:(1,),2:(2,),3:(3,)+invword(w)}
    ck(subst(subst((3,),bad),bad_inv)!=(3,),'negative_no_spare_generator_inverse')
    A6=ut(6,[(1,2),(2,3),(4,5)]);B6=ut(6,[(3,4)]);C6=ut(6,[(5,6)])
    W=evaluate_int(w,{1:A6,2:B6,3:C6});expected=[list(r) for r in ident(6)];expected[0][5]=-1
    ck(W==tuple(map(tuple,expected)),'published_integral_UT6_witness')
    A7=ut(7,[(1,2),(2,3),(3,4),(5,6)]);B7=ut(7,[(4,5),(6,7)])
    V=evaluate_int(v,{1:A7,2:B7});expected=[list(r) for r in ident(7)];expected[0][6]=1
    ck(V==tuple(map(tuple,expected)),'published_integral_UT7_witness')
    mats=[((a,b),(c,d)) for a,b,c,d in product(range(2),repeat=4)]
    zero=((0,0),(0,0))
    for a,b,c in product(mats,repeat=3):
        ck(mc(mc(mc(a,b,2),mc(a,c,2),2),a,2)==zero,'P_exhaustive_Mat2_F2')
    for a,b in product(mats,repeat=2):
        ck(mc(mc(mc(a,b,2),mc(a,mc(a,b,2),2),2),a,2)==zero,'Q_exhaustive_Mat2_F2')
    X=((1,0,0),(0,0,0),(0,0,-1));Y=((0,1,0),(0,0,0),(0,0,0));Z=((0,0,0),(0,0,1),(0,0,0))
    wrong3=mc(mc(mc(X,Y),mc(X,Z)),X)
    ck(wrong3[0][2]==-2,'negative_Mat3_extension')
    rng=random.Random(23387442);mixed=[]
    for trial in range(8):
        def choose():return {(1,0):rng.randrange(-3,4),(0,1):rng.randrange(-3,4),(1,1):rng.randrange(-2,3),(2,0):rng.randrange(-2,3)}
        images={i:chart(choose(),choose(),choose()) for i in (1,2,3,4)}
        ow=order(peval(w,images));ov=order(peval(v,images))
        ck(ow is None or ow>=6,'mixed_nilpotent_w_actual_order')
        ck(ov is None or ov>=7,'mixed_nilpotent_v_actual_order')
        # Products with a moving-generator matrix also retain the same ideal order.
        mw=pmatmul(images[4],peval(w,images));mv=pmatmul(images[3],peval(v,images))
        for moved,original,k in [(mw,images[4],6),(mv,images[3],7)]:
            ck(all(sum(m)>=k for i in range(2) for j in range(2) for m in pa(moved[i][j],original[i][j],-1)),'full_generator_difference_order')
        mixed.append({'trial':trial,'w_order':ow,'v_order':ov})
    out={'started_utc':started,'finished_utc':datetime.now(timezone.utc).isoformat(),'assertions':sum(C.values()),'counts':dict(C),
         'word_certificates':rows,'UT6_w':W,'UT7_v':V,'Mat3_negative':wrong3,'mixed_nilpotent_trials':mixed,
         'mixed_ring':'Z[e,t]/(e,t)^9, viewed inside Q[e,t]/(e,t)^9; mixed terms and actual SL2 inverses retained.',
         'scope':'Finite exact controls; universal ideal membership is supplied by the written filtered-ring proof. F2 tests concern only the any-commutative-ring matrix lemma, not a specialization of the rational representation ring.',
         'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (HERE/'fresh-control-results.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'assertions':out['assertions'],'counts':out['counts'],'mixed_nilpotent_trials':mixed},indent=2))
if __name__=='__main__':main()
