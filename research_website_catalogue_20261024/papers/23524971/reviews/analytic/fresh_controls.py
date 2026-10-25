#!/usr/bin/env python3
"""Independent exact generator controls, written before packaged helpers were read.

The corrector is solved backwards from the reflecting terminal equation,
not calculated using the manuscript's prefix-sum formula. All arithmetic
used in assertions is rational. These finite tests do not prove recurrence.
"""
from fractions import Fraction as F
from itertools import product
from math import ceil, floor
import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone

HERE = Path(__file__).resolve().parent

def parameters(lam):
    beta = 17 * lam / 8
    q = F(7, 8)
    c = 2 * (beta + 4)
    m = 4 * c
    theta = beta + c + 4
    gamma = (theta + 1) / (theta + 2)
    eta = (1 + gamma) / 2
    ell = 1 / (eta - gamma)
    R = 1
    # Closed geometric-mean tail condition, independently derived.
    while (R + 2) * gamma ** (R + 1) >= 1 or q * (R + 1) <= beta + c + 2:
        R += 1
    mu = gamma / (1 - gamma) - (R + 1) * gamma ** (R + 1) / (1 - gamma ** (R + 1))
    assert mu > theta and q * (R + 1) > beta + c + 2
    weights = [gamma ** k for k in range(R + 1)]
    assert mu == sum(k * w for k, w in enumerate(weights)) / sum(weights)
    # h[k] = g(k)-g(k+1), from the terminal death equation backwards.
    h = [F(0)] * R
    h[R - 1] = (R - mu) / R
    for k in range(R - 1, 0, -1):
        h[k - 1] = (k - mu + gamma * (k + 1) * h[k]) / k
    assert gamma * h[0] == mu
    assert all(v > 0 for v in h)
    gvals = [F(0)] * (R + 1)
    for k in range(R - 1, -1, -1):
        gvals[k] = gvals[k + 1] + h[k]
    G = gvals[0]
    N = max(R + 2, 3 * (R + 1), ceil((m + (1 + eta) * R + eta) / (1 - eta)),
            ceil(ell * G * (lam + 4 * (2 * R + 1))))
    B = (N + R + 1) * (beta + c + G * (lam + 2 * (N + R)) + 1)
    return locals()

def run_one(lam):
    p = parameters(lam)
    R, G, N, B = (p[k] for k in ('R', 'G', 'N', 'B'))
    beta, q, c, m, gamma, eta, ell, mu = (p[k] for k in ('beta','q','c','m','gamma','eta','ell','mu'))
    def g(k):
        assert k >= 0
        return p['gvals'][k] if k <= R else F(0)
    def f(r):
        return max(F(0), min(F(1), ell * (r - gamma)))
    def h(z):
        return F(z*z, 1)/(2*m)+m/2 if abs(z) <= m else F(abs(z))
    def hp(z):
        return max(F(-1), min(F(1), z / m))
    def W(s):
        a,b,x,y=s
        return 2*a+2*b+x+y
    def Z(s):
        a,b,x,y=s
        return a+x-b-y
    def J(s):
        a,b,x,y=s; D=x+y+1
        return f(F(b,D))*g(y)+f(F(a,D))*g(x)
    def V0(s):
        return W(s)+c*h(Z(s))
    def V(s):
        return V0(s)+J(s)
    def transitions(s):
        a,b,x,y=s; D=x+y+1
        specs=[((1,0,0,0),lam/2),((0,1,0,0),lam/2),
               ((-1,0,1,0),F(a*(x+1),D)),((0,-1,0,1),F(b*(y+1),D)),
               ((0,0,-1,0),F(x*(y+1),D)),((0,0,0,-1),F(y*(x+1),D))]
        return [(tuple(v+d for v,d in zip(s,delta)),rate,idx)
                for idx,(delta,rate) in enumerate(specs) if rate]
    def L(s,fun):
        old=fun(s)
        return sum(rate*(fun(new)-old) for new,rate,idx in transitions(s))
    poisson_count=0
    for k in range(R+1):
        val=(gamma*(k+1)*(g(k+1)-g(k)) if k<R else 0)
        val+=(k*(g(k-1)-g(k)) if k else 0)
        assert val==k-mu
        poisson_count+=1
    # Dense small states plus exact cutoff, rounding, terminal, and large-region boundaries.
    states=set(product(range(4),repeat=4))
    for y in (0,1,R-1,R,R+1):
        for x in (0,R,R+1,R+2,N-1,N,N+1):
            D=x+y+1
            bs={0,1,floor(gamma*D),ceil(gamma*D),floor(eta*D),ceil(eta*D),D,10**9}
            bs|={max(0,k+d) for k in list(bs) for d in (-1,1)}
            for b in bs:
                for a in (0,b,max(0,b+y-x+floor(m)),max(0,b+y-x+ceil(m)),10**9):
                    states.add((a,b,x,y)); states.add((b,a,y,x))
    for y in (0,R,N+R):
        for a in (floor(B),ceil(B),ceil(B)+1):
            states.add((a,0,0,y)); states.add((0,a,y,0))
    counts={'states':0,'outside_F':0,'corner_high_cutoff':0,'corner_low_cutoff':0,
            'both_large':0,'actual_poisson_comparison':0,'first_download_nonpositive_interfaces':0}
    max_outside=None
    for s in sorted(states):
        a,b,x,y=s; D=x+y+1
        u=F(a*(x+1)+b*(y+1),D); d=F(2*x*y+x+y,D)
        assert L(s,W)==2*lam-u-d
        assert L(s,Z)==F(y-x,D)
        assert 0<=J(s)<=2*G
        assert W(s)<=V(s)<=(1+c)*W(s)+c*m/2+2*G
        assert L(s,V0)<=beta-u-q*d+c*hp(Z(s))*F(y-x,D)
        Lgx=L(s,lambda t:g(t[2])); Lgy=L(s,lambda t:g(t[3]))
        LJ=L(s,J)
        assert LJ<=f(F(b,D))*Lgy+f(F(a,D))*Lgx+ell*G*(lam+4*d)/D
        assert LJ<=G*(lam+2*d)
        for k,w,lg in ((x,a,Lgx),(y,b,Lgy)):
            if k<=R and F(w,D)>=gamma:
                assert lg<=k-mu
                counts['actual_poisson_comparison']+=1
            if k>R:
                assert lg==0
        for new,rate,idx in transitions(s):
            aa,bb,xx,yy=new; DD=xx+yy+1
            if idx in (2,3):
                for oldw,neww,newk in ((b,bb,yy),(a,aa,xx)):
                    assert g(newk)*(f(F(neww,DD))-f(F(oldw,D)))<=0
                    counts['first_download_nonpositive_interfaces']+=1
                assert J(new)<=J(s)
            assert abs(V(new)-V(s))<=2+c+2*G
        lv=L(s,V)
        if min(x,y)>=R+1:
            assert J(s)==0 and all(J(t)==0 for t,_,_ in transitions(s))
            assert d>=min(x,y) and lv<-2
            counts['both_large']+=1
        if (y<=R and x>=N) or (x<=R and y>=N):
            small,large,w=(y,x,b) if x>=N else (x,y,a)
            assert d<=2*R+1 and q*d>=small
            assert ell*G*(lam+4*d)/D<=1
            if F(w,D)>=eta:
                assert lv<-3
                counts['corner_high_cutoff']+=1
            else:
                assert abs(Z(s))>=m and lv<=-3
                counts['corner_low_cutoff']+=1
        if x+y>N+R or a+b>B:
            assert lv<=-1
            counts['outside_F']+=1
            max_outside=lv if max_outside is None else max(max_outside,lv)
        counts['states']+=1
    # Removing the corrector is an intentionally false proposed certificate.
    bad_s=(0,10**6,10**6,0)
    no_corrector=L(bad_s,V0)
    if lam==3:
        assert no_corrector>0
    # Reversing a cutoff destroys the first-download sign at a fresh state.
    yy=0;xx=ceil(4*ell);DD=xx+1;bb=ceil((gamma+eta)*DD/2)
    wrong=f(F(bb,DD))-f(F(bb,DD+1))
    assert wrong>0 and g(yy)>0
    wrong_error=F(10**9*(xx+1),DD)*g(yy)*wrong
    # Common Chunk's 3-sample rule and this generator disagree already here.
    common=sum(any(t) for t in product((0,1),repeat=3))/F(8)
    assert common==F(7,8) and common!=F(1,2)
    return {
        'lambda':str(lam),'parameters':{k:str(p[k]) for k in ('R','N','B','beta','c','m','theta','gamma','eta','ell','mu','G')},
        'poisson_states':poisson_count,'counts':counts,
        'largest_tested_outside_F_drift':str(max_outside),
        'negative_controls':{'without_corrector_state':bad_s,'without_corrector_drift':str(no_corrector),
                             'reversed_cutoff_first_download_interface':str(wrong_error),
                             'Common_Chunk_one_peer_departure':str(common),'DFC_one_peer_departure':'1/2'},
        'assertions':'PASS',
    }

def main():
    started=datetime.now(timezone.utc).isoformat()
    results=[]
    for lam in (F(1,8),F(1),F(3)):
        r=run_one(lam); results.append(r)
        print(json.dumps({'lambda':r['lambda'],'R':r['parameters']['R'],'counts':r['counts'],'status':r['assertions']}),flush=True)
    payload={'started_utc':started,'finished_utc':datetime.now(timezone.utc).isoformat(),
             'method':'Independent six-rate generator; backwards reflecting Poisson solve; exact rational arithmetic.',
             'scope':'Finite falsification controls only; no stationary simulation or universal proof claim.',
             'loads':results,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (HERE/'fresh-control-results.json').write_text(json.dumps(payload,indent=2)+'\n')

if __name__=='__main__':
    main()
