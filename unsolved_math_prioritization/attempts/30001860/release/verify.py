#!/usr/bin/env python3
"""Exact bounded controls. No finite run proves the asymptotic theorem."""
from fractions import Fraction as F
from itertools import product
from math import prod
import argparse, json, hashlib, pathlib

def v2(x):
    assert x>0
    return (x & -x).bit_length()-1

def coeff(weights,n):
    # exp(sum_d weights[d]*z^d/d); exact recurrence from differentiation.
    c=[F(1)]
    for k in range(1,n+1): c.append(sum((weights[d]*c[k-d] for d in range(1,k+1)),F(0))/k)
    return c

def color(t,j):
    return F(1,2**t) if j==0 else (F(2**(j-1),2**t) if j<=t else F(0))

def model(n,q,kind='GL'):
    """Return natural target probability using exact torus coefficients.
    Sp is the unconditional signed model on rank n, dimension 2n.
    U is the isometry group on dimension n over F_(q^2).
    """
    assert q%2 and kind in ('GL','U','Sp')
    ts={d: ([v2(q**d-1),v2(q**d+1)] if kind=='Sp' else [v2(q**d-(-1)**d) if kind=='U' else v2(q**d-1)]) for d in range(1,n+1)}
    maxj=max(t for tt in ts.values() for t in tt)
    total=F(0); layers=[]
    for j in range(1,maxj+1):
        wa={d:sum((color(t,j) for t in ts[d]),F(0))/len(ts[d]) for d in ts}
        wb={d:sum((min(F(1),F(2**(j-1),2**t)) for t in ts[d]),F(0))/len(ts[d]) for d in ts}
        A=coeff(wa,n); B=coeff(wb,n)
        p=sum((A[m]*B[n-m] for m in range(1,n+1) if n<3*m<=2*n),F(0))
        total+=p; layers.append(p)
    return total,layers

def ident(n): return tuple(int(i==j) for i in range(n) for j in range(n))
def mm(A,B,n,q):
    return tuple(sum(A[i*n+k]*B[k*n+j] for k in range(n))%q for i in range(n) for j in range(n))
def mp(A,e,n,q):
    R=ident(n)
    while e:
        if e&1:R=mm(R,A,n,q)
        A=mm(A,A,n,q);e//=2
    return R

def rank(A,n,q):
    B=[list(A[i*n:(i+1)*n]) for i in range(n)];r=0
    for c in range(n):
        pivot=next((i for i in range(r,n) if B[i][c]%q),None)
        if pivot is None:continue
        B[r],B[pivot]=B[pivot],B[r];t=pow(B[r][c],-1,q);B[r]=[(x*t)%q for x in B[r]]
        for i in range(n):
            if i!=r:
                t=B[i][c];B[i]=[(x-t*y)%q for x,y in zip(B[i],B[r])]
        r+=1
    return r

def det(A,n,q):
    B=[list(A[i*n:(i+1)*n]) for i in range(n)];ans=1
    for c in range(n):
        p=next((i for i in range(c,n) if B[i][c]%q),None)
        if p is None:return 0
        if p!=c:B[c],B[p]=B[p],B[c];ans=-ans
        t=B[c][c];ans=ans*t%q;B[c]=[(x*pow(t,-1,q))%q for x in B[c]]
        for i in range(c+1,n):
            t=B[i][c];B[i]=[(x-t*y)%q for x,y in zip(B[i],B[c])]
    return ans%q

def prime_factors(m):
    out=[];d=2
    while d*d<=m:
        if m%d==0:
            out.append(d)
            while m%d==0:m//=d
        d+=1
    if m>1:out.append(m)
    return out

def order(A,n,q,m):
    I=ident(n)
    assert mp(A,m,n,q)==I
    for p in prime_factors(m):
        while m%p==0 and mp(A,m//p,n,q)==I:m//=p
    return m

def test_mat(A,n,q,Gorder):
    o=order(A,n,q,Gorder)
    if o%2:return False,None
    T=mp(A,o//2,n,q);I=ident(n)
    k=n-rank(tuple((a-b)%q for a,b in zip(T,I)),n,q)
    return n<=3*k<2*n,k

def brute_gl(n,q):
    Gorder=prod(q**n-q**i for i in range(n));count=hit=sl=slhit=0
    digest=hashlib.sha256()
    for A in product(range(q),repeat=n*n):
        d=det(A,n,q)
        if not d:continue
        count+=1;yes,k=test_mat(A,n,q,Gorder);hit+=yes
        if d==1:sl+=1;slhit+=yes
        digest.update(bytes(A))
    assert count==Gorder and sl==Gorder//(q-1)
    exact,_=model(n,q)
    assert F(hit,count)==exact
    if n==2:
        assert exact==(1-F(1,4**v2(q-1)))/3 and slhit==0
    return {'family':'GL','dimension':n,'q':q,'candidate_matrices':q**(n*n),'group_order':count,'Q_count':hit,'proportion':str(exact),'SL_order':sl,'SL_Q_count':slhit,'matrix_stream_sha256':digest.hexdigest(),'method':'exhaustive matrices; exact determinant/order/fixed-space rank; torus model match'}

def pair(v,w,q):return (v[0]*w[2]+v[1]*w[3]-v[2]*w[0]-v[3]*w[1])%q

def brute_sp4(q=3):
    # Every symplectic basis in column order (v1,v2,w1,w2) occurs once.
    vs=list(product(range(q),repeat=4));nz=[v for v in vs if any(v)]
    Gorder=q**4*(q*q-1)*(q**4-1);count=hit=0;digest=hashlib.sha256()
    for v1 in nz:
        for w1 in vs:
            if pair(v1,w1,q)!=1:continue
            W=[v for v in vs if pair(v1,v,q)==pair(w1,v,q)==0]
            assert len(W)==q*q
            for v2 in W:
                if not any(v2):continue
                for w2 in W:
                    if pair(v2,w2,q)!=1:continue
                    A=tuple(v[i] for i in range(4) for v in (v1,v2,w1,w2))
                    count+=1;yes,k=test_mat(A,4,q,Gorder);hit+=yes;digest.update(bytes(A))
    assert count==Gorder
    exact,_=model(2,q,'Sp');assert F(hit,count)==exact
    return {'family':'Sp','dimension':4,'rank':2,'q':q,'group_order':count,'Q_count':hit,'proportion':str(exact),'matrix_stream_sha256':digest.hexdigest(),'method':'exhaustive symplectic bases; exact order/fixed-space rank; signed-torus match'}

def controls():
    rows=[]
    for q in (3,5,7,9,13,17):
        for kind in ('GL','U','Sp'):
            for n in range(2,13):
                p,layer=model(n,q,kind);assert 0<=p<=1 and sum(layer)==p
                rows.append({'kind':kind,'model_size':n,'q':q,'p':str(p)})
    # 2-adic recurrence check over bounded odd integers, not just prime powers.
    valuation_cases=0
    for q in range(3,100,2):
        a,b=v2(q-1),v2(q+1)
        for d in range(1,65):
            plus=a if d%2 else a+b+v2(d)-1
            minus=b if d%2 else 1
            assert v2(q**d-1)==plus and v2(q**d+1)==minus
            valuation_cases+=1
    # Negative control: strict versus closed upper endpoint.
    t=(1,0,0,0,2,0,0,0,2);neg=tuple((-x)%3 for x in t)
    assert test_mat(t,3,3,11232)==(True,1)
    assert test_mat(neg,3,3,11232)==(False,2)
    # Negative control: multiplicative 2-part orders are not ordinary parity.
    assert model(2,3)[0]==F(1,4) and model(2,5)[0]==F(5,16)
    # A weakened all-odd-rank-2 heuristic would miss q=5's order-four stratum.
    # Exact fractional-avoidance coefficients vs finite product.
    avoid_cases=0
    for L in (2,4,8):
        for rho in (F(1,2),F(1,4)):
            weights={d:(1-rho if d%L==0 else F(1)) for d in range(1,49)}
            cc=coeff(weights,48)
            for n in range(49):
                expected=prod((1-rho/(L*i) for i in range(1,n//L+1)),start=F(1))
                assert cc[n]==expected;avoid_cases+=1
    return {'exact_model_cases':len(rows),'valuation_cases':valuation_cases,'avoidance_identity_cases':avoid_cases,'negative_controls':{'strict_endpoint_detected':True,'field_2adic_dependence_detected':True,'GL_SL_difference_checked_in_enumeration':True},'model_results':rows}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--sp4',action='store_true');ap.add_argument('--output',default='verification_results.json');args=ap.parse_args()
    out={'scope':'Bounded exact controls only; not an asymptotic proof.','exhaustive':[brute_gl(2,q) for q in (3,5,7)]+[brute_gl(3,3)],'controls':controls()}
    if args.sp4:out['exhaustive'].append(brute_sp4())
    pathlib.Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='controls'},indent=2));print('all exact controls passed')
if __name__=='__main__':main()
