#!/usr/bin/env python3
"""Independent explicit-exception checks, separate from the sealed family checker."""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations
from math import comb, exp, pi, sqrt, cos, sin, ceil, floor, erf, log
from pathlib import Path
import cmath, hashlib, json, datetime

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def choose(n,k):
    return comb(n,k) if n>=k>=0 else 0

def phi(x): return exp(-x*x/2)/sqrt(2*pi)
def close(a,b,tol=1e-11): return abs(a-b)<=tol

def enumerate_graphs(n):
    edges=list(combinations(range(n),2)); N=len(edges)
    idx={e:i for i,e in enumerate(edges)}
    triangles=[sum(1<<idx[e] for e in combinations(v,2)) for v in combinations(range(n),3)]
    disjoint=[(i,j) for i,j in combinations(range(N),2) if len(set(edges[i]+edges[j]))==4]
    hist=Counter(); cond=Counter(); thist=Counter()
    for mask in range(1<<N):
        m=mask.bit_count(); deg=[0]*n
        for i,(u,v) in enumerate(edges):
            if mask>>i&1: deg[u]+=1;deg[v]+=1
        t=sum(mask&z==z for z in triangles)
        w=sum(choose(d,2) for d in deg)
        x=sum((mask>>i&1) and (mask>>j&1) for i,j in disjoint)
        require(x==choose(m,2)-w,'ordinary-copy identity')
        hist[m,t,w,x]+=1;cond[m,w]+=1;thist[m,t]+=1
    return N,hist,cond,thist

results={'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'method':'fresh independent enumeration; explicit exceptions remain active under python -O','cases':[],'negative_controls':{},'gaussian_checks':{},'clt_log_checks':[]}
graphs_total=0
for n in range(3,7):
    N,hist,cond,thist=enumerate_graphs(n);graphs_total+=1<<N
    C=choose(n,3);s=3*C;d=2*(n-2);A=N*choose(d,2);D=choose(n-2,2)
    require(2*A-4*F(s*s,N)==-2*s,'conditional cancellation')
    for m in range(N+1):
        ws={w:c for (mm,w),c in cond.items() if mm==m}
        den=choose(N,m);ew=sum(F(c*w,den) for w,c in ws.items());ew2=sum(F(c*w*w,den) for w,c in ws.items())
        r=lambda j: F(choose(m,j),choose(N,j)) if j<=N else None
        require(ew==s*r(2),'conditional mean')
        if n>=4:
            expected=s*(r(2)-r(4))+2*A*(r(3)-r(4))+s*s*(r(4)-r(2)**2)
            require(ew2-ew*ew==expected,'conditional variance H2')
    for p in [F(1,5),F(1,2),F(4,5)]:
        v=p*(1-p);mu=C*p**3;b=p*p*(n-2)
        weights={m:p**m*(1-p)**(N-m) for m in range(N+1)}
        moments={k:F(0) for k in ['mass','t','t2','l','l2','q','q2','c','c2','lq','lc','qc','x','x2']}
        pmf=Counter()
        for (m,t,w,x),count in hist.items():
            weight=count*weights[m];l=b*(m-N*p)
            q=w-p*d*m+p*p*s
            cubic=t-p*w+p*p*(n-2)*m-p**3*C
            require(t-mu==l+p*q+cubic,'centered expansion')
            for k,val in [('mass',1),('t',t),('t2',t*t),('l',l),('l2',l*l),('q',q),('q2',q*q),('c',cubic),('c2',cubic*cubic),('lq',l*q),('lc',l*cubic),('qc',q*cubic),('x',x),('x2',x*x)]:moments[k]+=weight*val
            pmf[t]+=weight
        varT=moments['t2']-mu*mu
        varL=N*(n-2)**2*p**5*(1-p)
        varR=s*p**4*(1-p)**2+C*p**3*(1-p)**3
        covform=C*p**3*(1-p**3)+12*choose(n,4)*p**5*(1-p)
        require(moments['mass']==1 and moments['t']==mu,'triangle mean')
        require(varT==varL+varR==covform,'triangle variance')
        require(moments['l']==moments['q']==moments['c']==moments['lq']==moments['lc']==moments['qc']==0,'orthogonality')
        require(moments['l2']==varL and moments['q2']==s*v*v and moments['c2']==C*v**3,'monomial variances')
        require(moments['x']==3*choose(n,4)*p*p,'ordinary 2K2 mean')
        require(moments['x2']-moments['x']**2==N*D*D*p**3*(1-p)+3*choose(n,4)*v*v,'ordinary 2K2 variance')
        require(pmf[0]>0 and pmf[1]>0,'primitive support')
        cf_remainder_max_ratio=0.0
        for tt in [i/10 for i in range(-40,41)]:
            sigma=sqrt(float(varT)); tau=tt*float(b)/sigma
            actual=sum(float(pr)*cmath.exp(1j*tt*(t-float(mu))/sigma) for t,pr in pmf.items())
            projected=((1-float(p))*cmath.exp(-1j*tau*float(p))+float(p)*cmath.exp(1j*tau*(1-float(p))))**N
            bound=abs(tt)*sqrt(float(varR))/sigma
            require(abs(actual-projected)<=bound+1e-12,'CLT projection remainder inequality')
            if bound:cf_remainder_max_ratio=max(cf_remainder_max_ratio,abs(actual-projected)/bound)
        fourier_max=0.0;lower_bound_margin=1.0
        for q in range(1,C+6):
            resid=[F(0) for _ in range(q)]
            for t,prob in pmf.items():resid[t%q]+=prob
            dn=max(abs(q*x-1) for x in resid)
            for a in range(q):
                cf=sum(sum(float(pr)*cmath.exp(2j*pi*ell*t/q) for t,pr in pmf.items())*cmath.exp(-2j*pi*ell*a/q) for ell in range(q))/q
                fourier_max=max(fourier_max,abs(cf-float(resid[a])))
            if q>=2:
                cf=abs(sum(float(pr)*cmath.exp(2j*pi*t/q) for t,pr in pmf.items()))
                require(cf<=float(dn)+1e-12,'first Fourier discrepancy bound')
                lower_bound_margin=min(lower_bound_margin,float(dn)-cf)
        require(fourier_max<1e-12,'Fourier inversion')
        for q in [10**12,10**100]:
            dn=max(q*max(pmf.values())-1,F(1))
            require(dn>0,'huge modulus empty-residue control')
        results['cases'].append({'n':n,'p':str(p),'graphs':1<<N,'mu':str(mu),'variance':str(varT),'H2_all_m_checked':n>=4,'max_fourier_inversion_error':fourier_max,'minimum_N1_margin':lower_bound_margin,'max_actual_projection_cf_error_over_L2_bound':cf_remainder_max_ratio})
        if n==5 and p==F(1,2):
            wrong=C*p**3*(1-p**3)+6*choose(n,4)*p**5*(1-p)
            require(wrong!=varT,'negative missing covariance factor not detected')
            results['negative_controls']['missing_covariance_factor']={'rejected':True,'true_variance':str(varT),'wrong_variance':str(wrong)}
            require(all((6*t)%2==0 for t in pmf),'labeled statistic control')
            results['negative_controls']['labeled_embedding_modulus_2']={'rejected':True,'D_for_6T':1,'fixed_modulus_subcritical':True}
            m=N//2;r=lambda j:F(choose(m,j),choose(N,j))
            correct=s*(r(2)-r(4))+2*A*(r(3)-r(4))+s*s*(r(4)-r(2)**2)
            wrongH=s*(r(2)-r(4))+A*(r(3)-r(4))+s*s*(r(4)-r(2)**2)
            require(correct!=wrongH,'negative wedge multiplicity not detected')
            results['negative_controls']['halved_wedge_pair_coefficient']={'rejected':True,'true_variance':str(correct),'wrong_variance':str(wrongH)}
results['graphs_enumerated_once']=graphs_total
# Gaussian folding: independent direct and dual calculations, translated grids, and enormous spacing.
def fold(h,theta):
    j0=round(-theta); radius=ceil(13/h)+3
    return h*sum(phi(h*(j+theta)) for j in range(j0-radius,j0+radius+1))
def dual(h,theta):
    cutoff=ceil(13*h/(2*pi))+3
    return 1+2*sum(exp(-2*pi*pi*ell*ell/(h*h))*cos(2*pi*ell*theta) for ell in range(1,cutoff+1))
max_poisson=0.0;max_tail_excess=-1e100;phase_records=[]
for h in [0.25,0.5,1,2,5,10,50,1000]:
    for theta in [0,0.01,0.127,0.499,0.5,0.999]:
        direct=fold(h,theta);fourier=dual(h,theta)
        max_poisson=max(max_poisson,abs(direct-fourier))
        require(abs(direct-fourier)<2e-9,'Poisson folding')
        for L in [1,2,4,8]:
            js=range(-ceil(13/h)-4,ceil(13/h)+5)
            tail=min(h,1)*sum(phi(h*(j+theta)) for j in js if abs(h*(j+theta))>L)
            bound=2*(phi(L)+0.5*(1-erf(L/sqrt(2))))
            max_tail_excess=max(max_tail_excess,tail-bound)
            require(tail<=bound+1e-14,'uniform Gaussian tail')
for h in [0.5,1,2,5,10]:
    Fh=dual(h,0)-1
    for q in [101,1009,10007]:
        for drift in [0,0.123,0.4999,0.87654321]:
            theta=(round(drift)-drift)/q
            nearest=abs(dual(h,theta)-1)
            # Positive Fourier coefficients prove no phase can exceed Fh.
            gridmax=max(abs(dual(h,(a-drift)/q)-1) for a in range(q))
            require(gridmax<=Fh+1e-11 and Fh-gridmax<=Fh-nearest+1e-11,'critical max/phase grid')
            phase_records.append({'h':h,'q':q,'drift':drift,'F_minus_gridmax':Fh-gridmax,'gridmax_minus_nearest_positive_peak':gridmax-nearest})
results['gaussian_checks']={'max_direct_dual_error':max_poisson,'max_tail_minus_bound':max_tail_excess,'critical_phase_checks':phase_records,'supercritical':[]}
for h in [10,50,1000]:
    highest=fold(h,0)/h
    require(abs(highest-phi(0))<1e-12,'supercritical Gaussian maximum')
    results['gaussian_checks']['supercritical'].append({'h':h,'fold_over_h':highest,'phi0':phi(0)})
# Explicit compact-t logarithm expansion. Independent Bernoulli factors, actual triangle sigma.
for n in [20,100,500,2000]:
    N=choose(n,2);C=choose(n,3);p=0.3;v=p*(1-p);b=p*p*(n-2)
    sigma2=C*p**3*(1-p**3)+12*choose(n,4)*p**5*(1-p);u=b/sqrt(sigma2)
    log_error=0.0;variance_error=abs(N*b*b*v/sigma2-1)
    for t in [i/20 for i in range(-160,161)]:
        z=(1-p)*cmath.exp(-1j*t*u*p)+p*cmath.exp(1j*t*u*(1-p))
        require(z.real>0,'log branch near 1')
        error=abs(N*cmath.log(z)+t*t*N*u*u*v/2)
        log_error=max(log_error,error)
    results['clt_log_checks'].append({'n':n,'p':p,'B':8,'max_remainder':log_error,'n_times_max_remainder':n*log_error,'n_times_variance_ratio_error':n*variance_error})
# Gaussian centered-cell bound, tested away from cancellation-dominated enormous sigma.
cell_max_ratio=0.0
for sigma in [1,2,10,50]:
    for z in [-4,-1.7,-0.5,0,0.3,1,3]:
        cell=0.5*(erf((z+0.5/sigma)/sqrt(2))-erf((z-0.5/sigma)/sqrt(2)))
        error=abs(cell-phi(z)/sigma)
        bound=phi(0)/(24*sigma**3)
        require(error<=bound+1e-14,'centered cell second derivative bound')
        cell_max_ratio=max(cell_max_ratio,error/bound)
results['centered_cell_max_error_ratio_to_bound']=cell_max_ratio
results['completed_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();results['status']='PASS'
out=Path(__file__).resolve().parent/'independent_checks.json';out.write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps({'status':results['status'],'graphs':graphs_total,'cases':len(results['cases']),'max_poisson_error':max_poisson,'negative_controls':list(results['negative_controls']),'output':str(out)},indent=2))
