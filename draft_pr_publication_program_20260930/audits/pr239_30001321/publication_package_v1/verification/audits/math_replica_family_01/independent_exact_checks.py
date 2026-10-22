#!/usr/bin/env python3
"""Independent exact checks of PR239 replica / heat-kernel inputs. Standard library only."""
from fractions import Fraction as F
from math import comb, factorial
from itertools import product
from pathlib import Path
import json, hashlib, datetime

LAWS = [
 ("deterministic_symmetric", [(F(1,2),F(1))]),
 ("deterministic_strong_bias", [(F(1,100),F(1))]),
 ("almost_arrows_symmetric", [(F(1,100),F(1,2)),(F(99,100),F(1,2))]),
 ("asymmetric_mixed", [(F(1,100),F(1,10)),(F(9,10),F(9,10))]),
 ("strongly_biased_mixed", [(F(1,10000),F(2,3)),(F(1,100),F(1,3))]),
 ("nearly_constant_mixed", [(F(49,100),F(1,3)),(F(51,100),F(2,3))]),
]
checks = {}
def ck(name, condition):
    if not condition: raise AssertionError(name)
    checks[name] = checks.get(name,0)+1
def add(d,key,value):
    d[key] = d.get(key,F(0))+value
def averaged(q,n):
    return {2*k-n:F(comb(n,k))*q**k*(1-q)**(n-k) for k in range(n+1)}
def pair_step(q,delta,pair):
    out={}
    for (x,y),mass in pair.items():
        probabilities = ((1,1,q-delta),(-1,-1,1-q-delta),(1,-1,delta),(-1,1,delta)) if x==y else ((1,1,q*q),(-1,-1,(1-q)**2),(1,-1,q*(1-q)),(-1,1,q*(1-q)))
        for dx,dy,p in probabilities: add(out,(x+dx,y+dy),mass*p)
    return out
def difference_step(a,delta,d):
    out={}
    for x,mass in d.items():
        rate = delta if x==0 else a
        for dx,p in ((-1,rate),(0,1-2*rate),(1,rate)):
            add(out,x+dx,mass*p)
    return out
def cell(x,length,alignment):
    return (F(x)-alignment)//length
def semigroup(q,t,f,x):
    return sum((p*f(x+k) for k,p in averaged(q,t).items()),F(0))
results=[]
for lname,law in LAWS:
    q=sum((p*w for p,w in law),F(0))
    delta=sum((p*(1-p)*w for p,w in law),F(0))
    a=q*(1-q)
    sig=a-delta
    ck("strict_law_parameters",0<delta<=a<=F(1,4))
    # Forward difference and backward hitting profile from genuinely different recursions.
    nmax=32
    d={0:F(1)}
    g=[]
    u={x:F(int(x==0)) for x in range(-nmax-2,nmax+3)}
    for n in range(nmax+1):
        g.append(d.get(0,F(0)))
        ck("forward_backward_return",g[-1]==u[0])
        ck("backward_zero_maximum",all(0<=value<=u[0] for value in u.values()))
        starting_mu={-4:F(1,6),0:F(1,3),2:F(1,2)}
        conditional=sum((mx*my*u[(x-y)//2] for x,mx in starting_mu.items() for y,my in starting_mu.items()),F(0))
        ck("conditional_overlap_arbitrary_old_mixture",conditional<=u[0])
        ck("backward_symmetry",all(u[x]==u[-x] for x in u))
        ck("profile_decreasing_distance",all(u[x]>=u[x+1] for x in range(nmax+1)))
        if n:
            ck("return_nondecreasing_refusal_monotone",g[-1]<=g[-2])
        if n<nmax:
            old=u
            u={}
            for x in old:
                rate=delta if x==0 else a
                u[x]=rate*old.get(x-1,F(0))+(1-2*rate)*old[x]+rate*old.get(x+1,F(0))
            for x in range(nmax):
                vd=old[x]-old[x+1]
                expected=((1-2*delta-a)*vd+a*(old[1]-old[2])) if x==0 else a*(old[x-1]-old[x])+(1-2*a)*vd+a*(old[x+1]-old[x+2])
                ck("gradient_maximality_recurrence",u[x]-u[x+1]==expected)
            d=difference_step(a,delta,d)
    # Exact formal radical denominator times observed return coefficients.
    rad=[F(1)]
    for n in range(1,nmax+1):
        polynomial = (-(2-4*a) if n==1 else (1-4*a if n==2 else F(0)))
        rad.append((polynomial-sum((rad[k]*rad[n-k] for k in range(1,n)),F(0)))/2)
    den=[(1-delta/a)*(F(1) if k==0 else (-F(1) if k==1 else F(0)))+(delta/a)*rad[k] for k in range(nmax+1)]
    for n in range(nmax+1):
        ck("closed_radical_generating_identity",sum((g[k]*den[n-k] for k in range(n+1)),F(0))==F(n==0))
    # Reflection at the absorbing origin for the lazy homogeneous half-gap.
    p={0:F(1)}
    killed={start:{start:F(1)} for start in range(1,19)}
    for n in range(17):
        for start,dist in killed.items():
            survival=sum(dist.values(),F(0))
            reflection=sum((p.get(j,F(0)) for j in range(1-start,start+1)),F(0))
            ck("lazy_reflection_survival",survival==reflection)
        if n<16:
            pn={}
            for x,mass in p.items():
                for dx,prob in ((-1,a),(0,1-2*a),(1,a)): add(pn,x+dx,mass*prob)
            p=pn
            for start,dist in killed.items():
                nxt={}
                for x,mass in dist.items():
                    for dx,prob in ((-1,a),(0,1-2*a),(1,a)):
                        if x+dx>0:add(nxt,x+dx,mass*prob)
                killed[start]=nxt
    # Pair joint density gives exact diagonal terms, variances and quenched-mean identity.
    pairs=[{(0,0):F(1)}]
    for n in range(1,9): pairs.append(pair_step(q,delta,pairs[-1]))
    for n,pair in enumerate(pairs):
        bm=averaged(q,n)
        ck("pair_total_mass",sum(pair.values(),F(0))==1)
        ck("pair_overlap_return",sum((mass for (x,y),mass in pair.items() if x==y),F(0))==g[n])
        for x in bm:
            ck("pair_marginal_averaged",sum((mass for (xx,y),mass in pair.items() if xx==x),F(0))==bm[x])
        meanvar=sum((F(x*y)*mass for (x,y),mass in pair.items()),F(0))-(n*(2*q-1))**2
        ck("quenched_mean_variance",meanvar==4*sig*sum(g[:n],F(0)))
        if n==0:continue
        for length in (F(1),F(2),F(3),F(5),F(3,2),F(7,2)):
            for alignment in (F(-2),F(0),F(1,2)):
                cells={cell(x,length,alignment) for x in bm}
                totalvar=F(0); rhsvar=F(0)
                for j in cells:
                    f=lambda x,j=j: F(cell(x,length,alignment)==j)
                    em=sum((mass*f(x) for x,mass in bm.items()),F(0))
                    second=sum((mass*f(x)*f(y) for (x,y),mass in pair.items()),F(0))
                    lhs=second-em*em
                    rhs=F(0)
                    for s in range(n):
                        t=n-s-1
                        for (x,y),mass in pairs[s].items():
                            if x==y:
                                grad=semigroup(q,t,f,x+1)-semigroup(q,t,f,x-1)
                                rhs+=sig*mass*grad*grad
                    ck("interval_variance_identity",lhs==rhs)
                    totalvar+=lhs; rhsvar+=rhs
                ck("sum_interval_variance_identity",totalvar==rhsvar)
    # Full finite-environment integration independently validates pair construction,
    # including probabilities of the shared-site four transitions.
    n=4
    sites=[(s,x) for s in range(n) for x in range(-s,s+1,2)]
    integ_mu={x:F(0) for x in averaged(q,n)}
    integ_pair={(x,y):F(0) for x in integ_mu for y in integ_mu}
    count=0
    occupation_moments={k:F(0) for k in range(1,9)}
    for choices in product(range(len(law)),repeat=len(sites)):
        weight=F(1); env={}
        for site,ix in zip(sites,choices):
            pval,pweight=law[ix]; env[site]=pval; weight*=pweight
        mu={0:F(1)}
        occupation=F(1)
        for s in range(n):
            nxt={}
            for x,mass in mu.items():
                pp=env[(s,x)]
                add(nxt,x+1,mass*pp);add(nxt,x-1,mass*(1-pp))
            mu=nxt
            if s<n-1: occupation+=sum((mass*mass for mass in mu.values()),F(0))
        for k in occupation_moments:occupation_moments[k]+=weight*occupation**k
        for x,mass in mu.items(): integ_mu[x]+=weight*mass
        for x,mx in mu.items():
            for y,my in mu.items(): integ_pair[(x,y)]+=weight*mx*my
        count+=1
    ck("enumerated_environment_mean",integ_mu==averaged(q,n))
    ck("enumerated_environment_pair",integ_pair==pairs[n])
    for k,value in occupation_moments.items():
        ck("occupation_moment_factorial_bound",value<=factorial(k)*sum(g[:n],F(0))**k)
    # Partition telescoping and L1-gradient bounds, actual binomial parity retained.
    for t in range(13):
        bm=averaged(q,t)
        maxb=max(bm.values())
        tv=sum((abs(bm.get(k+2,F(0))-bm.get(k,F(0))) for k in range(-t-2,t+1,2)),F(0))
        ck("unimodal_shift2_total_variation",tv==2*maxb)
        for length in (F(1),F(2),F(3),F(7),F(3,2),F(7,2)):
            for alignment in (F(-2),F(0),F(1,2)):
                for x in (-4,-1,0,3):
                    cells={cell(x+off+k,length,alignment) for off in (-1,1) for k in bm}
                    hs=[]
                    for j in cells:
                        f=lambda y,j=j: F(cell(y,length,alignment)==j)
                        hs.append(semigroup(q,t,f,x+1)-semigroup(q,t,f,x-1))
                    ck("partition_gradient_L1",sum(map(abs,hs),F(0))<=tv)
                    ck("partition_gradient_telescoping_max",max(map(abs,hs),default=F(0))<=maxb)
                    diffmax=max((abs(bm.get(k+2,F(0))-bm.get(k,F(0))) for k in range(-t-2,t+1,2)),default=F(0))
                    countmax=int(length)+1
                    ck("partition_gradient_site_count_max",max(map(abs,hs),default=F(0))<=countmax*diffmax)
                    ck("partition_gradient_L2_product",sum((h*h for h in hs),F(0))<=max(map(abs,hs),default=F(0))*tv)
    results.append({"law":lname,"q":str(q),"a":str(a),"delta":str(delta),"variance_p":str(sig),"environment_configurations_exactly_integrated_at_n4":count,"g1":str(g[1]),"g32":str(g[-1])})
output={"schema":"independent-pr239-replica-exact-controls-v1","UTC":datetime.datetime.now(datetime.timezone.utc).isoformat(),"status":"PASS","checks":checks,"check_count":sum(checks.values()),"laws":results,"limits":"Finite checks corroborate algebra and parity/bias cases, not the infinite-time theorem. General bounds are proved separately in DERIVATION.md. No supplied checker or historical/current review was executed or imported."}
out=Path(__file__).resolve().parent
(out/"EXACT_RESULTS.json").write_text(json.dumps(output,indent=2)+"\n")
print(json.dumps({"status":"PASS","check_count":output["check_count"],"families":len(checks),"laws":len(results),"result":str(out/"EXACT_RESULTS.json")}))
