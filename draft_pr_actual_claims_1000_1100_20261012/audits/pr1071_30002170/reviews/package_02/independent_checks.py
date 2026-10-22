#!/usr/bin/env python3
"""New exact-rational and finite sampled controls, no prior checker imported."""
from fractions import Fraction as Q
from functools import lru_cache
import itertools,json,math,random,sys

def need(ok,msg):
    if not ok:raise RuntimeError(msg)
def add(a,b):return [sum(x) for x in itertools.zip_longest(a,b,fillvalue=Q(0))]
def mul(a,b):
    r=[Q(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):r[i+j]+=x*y
    return r
def der(p):return [i*x for i,x in enumerate(p)][1:]
def ev(p,x):return sum(v*x**i for i,v in enumerate(p))
def integ(p,a=Q(0),b=Q(1)):return sum(c*(b**(i+1)-a**(i+1))/Q(i+1) for i,c in enumerate(p))
def transform(p,a,b):
    # p(a*x+b), exact polynomial composition.
    r=[Q(0)]
    for c in reversed(p):r=add(mul(r,[b,a]),[c])
    while len(r)>1 and r[-1]==0:r.pop()
    return r
def transpose(a):return list(map(list,zip(*a)))
def matmul(a,b):return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]
def gram(a):return matmul(a,transpose(a))
def trace(a):return sum(a[i][i] for i in range(len(a)))
def pair_sum(f,g,n,j,m):
    delta=Q(1,n)
    def cell(p,t):
        x=t/delta-j
        return ev(p,x) if 0<=x<=1 else Q(0)
    return sum(cell(f,Q(k,m))*(cell(g,Q(k+1,m))-cell(g,Q(k,m))) for k in range(m))
def rho(h,r):return ((r+1)**(2*h)+abs(r-1)**(2*h)-2*r**(2*h))/2

def main():
    phi=[Q(0)]*4+[Q(1),Q(-4),Q(6),Q(-4),Q(1)]
    derivatives=[phi]
    for _ in range(4):derivatives.append(der(derivatives[-1]))
    f,g=derivatives[1],phi
    need(all(ev(p,Q(0))==ev(p,Q(1))==0 for p in derivatives[:4]),'Endpoint traces')
    a=integ(mul(f,f));need(a==Q(4,45045),'Area pairing')
    need(2*ev(phi,Q(1,2))==Q(1,128) and integ(phi)==Q(1,630),'L1 norms')
    # In t=2x-1, phi''=(1-t²)²(7t²-1)/8. Evaluate at critical
    # t²=3/7 and t=0 in rational arithmetic; variation is exact.
    peak=(1-Q(3,7))**2*(7*Q(3,7)-1)/8
    valley=Q(-1,8)
    ng=4*peak-2*valley
    need(peak==Q(4,49) and ng==Q(113,196),'N_g total variation')
    phi2_t=transform(derivatives[2],Q(1,2),Q(1,2))
    expect=mul(mul([Q(1),0,-Q(1)],[Q(1),0,-Q(1)]),[-Q(1,8),0,Q(7,8)])
    need(phi2_t==expect,'Critical-value polynomial identity')
    # Exact left sum convergence: use m divisible by n so support boundaries
    # align. Check the integral by polynomial composition independently, and
    # compare dyadic refinements with the limiting rational a.
    pairings=[]
    for n in [1,2,4,7]:
        for j in range(n):
            fp=transform(f,Q(n),Q(-j));gp=transform(g,Q(n),Q(-j))
            value=integ(mul(fp,der(gp)),Q(j,n),Q(j+1,n))
            need(value==a,'Exact cell integral scaling')
            sums=[pair_sum(f,g,n,j,n*k) for k in [4,8,16,32]]
            need(all(abs(sums[i+1]-a)<abs(sums[i]-a) for i in range(3)),'Riemann refinement did not converge')
            need(integ(mul(gp,der(fp)),Q(j,n),Q(j+1,n))==-a,'Area order/sign')
            pairings.append({'n':n,'j':j,'integral':str(value),'left_sums':[str(x) for x in sums]})
    rng=random.Random(107102)
    psd=[];negative=noncommuting=0
    for n in range(2,7):
        for case in range(17):
            b=[[Q(rng.randint(-4,4),rng.randint(1,4)) for _ in range(n)] for _ in range(n)]
            d=[[Q(rng.randint(-4,4),rng.randint(1,4)) for _ in range(n)] for _ in range(n)]
            A,C=gram(b),gram(d);ac,ca=matmul(A,C),matmul(C,A)
            mf,mg=trace(A),trace(C);v=trace(ac)
            need(0<=v<=mf*trace(C)<=n*mf*mg,'PSD signed trace bound')
            negative+=any(A[i][j]<0 or C[i][j]<0 for i in range(n) for j in range(n) if i!=j)
            noncommuting+=ac!=ca
            psd.append({'dimension':n,'variance':str(v),'bound':str(n*mf*mg)})
    # Exact Wick recurrence with signed, correlated hidden vectors and
    # independent nontrivial Gaussian observed coordinates.
    A=[[Q(2),Q(-1)],[Q(-1),Q(3)]];C=[[Q(4),Q(1)],[Q(1),Q(1)]]
    O=[[Q(3),Q(-1)],[Q(-1),Q(2)]]
    covariance=[[Q(0) for _ in range(6)] for _ in range(6)]
    for offset,block in [(0,A),(2,C),(4,O)]:
        for i in range(2):
            for j in range(2):covariance[offset+i][offset+j]=block[i][j]
    @lru_cache(None)
    def wick(indices):
        if not indices:return Q(1)
        if len(indices)%2:return Q(0)
        i=indices[0]
        return sum(covariance[i][indices[k]]*wick(indices[1:k]+indices[k+1:]) for k in range(1,len(indices)))
    monomials=0
    for p in range(8):
        for q in range(8):
            observed=(4,)*p+(5,)*q
            need(sum(wick(tuple(sorted(observed+(j,j+2)))) for j in range(2))==0,'Nonlinear observed orthogonality')
            monomials+=1
    v=sum(wick(tuple(sorted((j,j+2,k,k+2)))) for j in range(2) for k in range(2))
    need(v==trace(matmul(A,C))==Q(9),'Wick witness variance')
    # Explicit mechanism faults. They are failures of the proof identities,
    # not string-marker tests and not claims of universal probabilistic proof.
    fault={}
    fault['wrong area order']=integ(mul(g,der(f)))!=a
    fault['omitted squared lag']=False
    samples=[]
    for h in [.251,.3,.49,.5,.6,.75,.9,.99]:
        for n in [1,2,3,5,11,23]:
            dense=sum(rho(h,abs(j-k))**2 for j in range(n) for k in range(n))/4/n**(4*h)
            lags=(n+2*sum((n-r)*rho(h,r)**2 for r in range(1,n)))/4/n**(4*h)
            need(math.isclose(dense,lags,rel_tol=2e-14,abs_tol=1e-15),'Correction lag count')
            if h==.5:need(math.isclose(dense,1/(4*n),rel_tol=1e-14),'Brownian correction')
            if h<.5 and n>2:
                wrong=(n+2*sum((n-r)*rho(h,r) for r in range(1,n)))/4/n**(4*h)
                fault['omitted squared lag']|=abs(wrong-dense)>1e-6
            samples.append({'H':h,'n':n,'variance':lags})
    fault['assumed independent cells']=sum(wick(tuple(sorted((j,j+2,k,k+2)))) for j in range(2) for k in range(2) if j!=k)!=0
    # All-one unit increments have variance n^(2H), refuting uniform rough
    # lower coercivity normalized by n. Ratios strictly fall at rough H.
    fault['rough increment coercivity']=64**(2*.3-1)<2**(2*.3-1)
    # Reflecting compactly supported path changes its support to negative
    # time; at x=1/4 it is zero rather than nonzero. This is the covariance
    # caused by omitting conjugation under the declared Fourier sign.
    fault['missing Fourier conjugation']=ev(f,Q(1,4))!=0
    need(all(fault.values()),'Fault control failed')
    # Finite power-tail checks span all permitted alpha, especially near 3.
    tails=[]
    for alpha in [Q(1501,1000),Q(7,4),Q(2),Q(5,2),Q(2999,1000)]:
        af=float(alpha);series=sum((2*k-1)**(af-6) for k in range(1,10000));bound=1+1/(2*(5-af))
        need(series<bound,'Odd tail upper bound sampled violation')
        tails.append({'alpha':str(alpha),'partial':series,'upper':bound})
    result={'exact_area_pairing':str(a),'exact_Lf':'1/128','exact_Lg':'1/630','exact_Ng':str(ng),'cell_pairings':pairings,'signed_psd_cases':len(psd),'negative_off_diagonal_cases':negative,'noncommuting_cases':noncommuting,'nonlinear_wick_monomials':monomials,'exact_wick_variance':str(v),'sampled_correction_cases':samples,'sampled_odd_tail_cases':tails,'mechanism_faults':fault,'limitations':'Finite exact identities and floating samples only; no interval quadrature or universal analytic certification. No prior checker imported.'}
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
