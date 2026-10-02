"""Independent exact controls for the frozen 30002011 scoped packet.

No author checker is imported. Weighted isotonic fits use the max-min formula,
not PAVA. Positive-h fits are enclosed using reciprocal positive-series bounds
for exp(h), with a rigorous geometric tail bound for the remaining series.
"""
from fractions import Fraction as Q
from math import factorial, comb
from itertools import combinations_with_replacement
from collections import Counter
import random,json
checks=Counter()
def ck(p,name):
    if not p:raise AssertionError(name)
    checks[name]+=1

def isotonic(values,weights):
    m=len(values)
    def average(s,t):
        return sum(values[k]*weights[k] for k in range(s,t+1))/sum(weights[s:t+1])
    return [max(min(average(s,t) for t in range(i,m)) for s in range(i+1)) for i in range(m)]

def exp_positive_bounds(h,K=28):
    low=sum(h**j/Q(factorial(j)) for j in range(K+1))
    rem=h**(K+1)/factorial(K+1)/(1-h/Q(K+2))
    return low,low+rem

def raw_enclosure(hist,y,h,J=32):
    xs=sorted(hist);n=sum(hist.values());m=xs[-1]
    el,eu=exp_positive_bounds(h)
    total=Q(0); jumps=Q(0);firstjump=Q(0)
    nextx=next((t for t in xs if t>y),None)
    for j in range(J+1):
        z=y+j;s=max(t for t in xs if t<=z)
        den=sum(Q(hist[t])*h**(z-t)/factorial(z-t) for t in xs if t<=z)
        low=sum(Q(t*hist[t])*h**(z+1-t)/factorial(z+1-t) for t in xs if t<=z)/den
        jump=Q((z+1)*hist.get(z+1,0))/den
        a=low+jump
        ck(Q(0)<=low<=m*n*h,'uniform_low_component_bound')
        direct=((z+1)*sum(Q(hist[t])*h**(z+1-t)/factorial(z+1-t) for t in xs if t<=z+1)/den)-h
        ck(a==direct,'shifted_convolution_exact')
        term=h**j/Q(factorial(j))
        total+=term*a
        if jump:
            t=z+1
            rs=sum(Q(hist[r],hist[s])*h**(s-r)*Q(factorial(t-s-1),factorial(t-r-1)) for r in xs if r<s)
            formula=Q(t*hist[t],hist[s])*h**(s-y)*Q(factorial(t-s-1),factorial(t-y-1))/(1+rs)
            ck(term*jump==formula,'exact_jump_decomposition')
            if t==nextx:
                firstjump=formula
                ck(rs<=n*h,'first_jump_denominator_bound')
            else:jumps+=formula
    ck(jumps<=h*n*m,'later_jump_sum_bound')
    # J >= m-y: all omitted a_h(y+j) <= m*h by the tail bound.
    assert J>=m-y and h<=1
    coefftail=h**(J+1)/factorial(J+1)/(1-h/Q(J+2))
    lo=total/eu
    hi=(total+m*h*coefftail)/el
    bp=Q(nextx*hist[nextx],hist[y]) if nextx is not None else Q(0)
    bound=m*n*(n+3)*h
    ck(lo>=bp-bound and hi<=bp+bound,'positive_h_raw_uniform_interval')
    return lo,hi

def histogram_checks():
    rng=random.Random(83002011)
    samples=set(combinations_with_replacement(range(7),2))
    samples.update((j,) for j in range(10))
    for _ in range(180):samples.add(tuple(sorted(rng.randrange(10) for _ in range(rng.randrange(1,7)))))
    for sample in sorted(samples):
        hist=Counter(sample);xs=sorted(hist);weights=[Q(hist[x]) for x in xs];n=len(sample);m=max(xs);ell=min(xs)
        bp=[Q(xs[i+1]*hist[xs[i+1]],hist[x]) if i+1<len(xs) else Q(0) for i,x in enumerate(xs)]
        br=[Q((x+1)*hist.get(x+1,0),hist[x]) for x in xs]
        dp=isotonic(bp,weights);dr=isotonic(br,weights)
        ck(all(Q(0)<=a<=b<=m for a,b in zip(dr,dp)),'ordered_projected_endpoints')
        ck(sum(w*v for w,v in zip(weights,dp))==sum(w*v for w,v in zip(weights,bp)),'gap_projection_mean_preserved')
        ck(sum(w*v for w,v in zip(weights,dr))==sum(w*v for w,v in zip(weights,br)),'robbins_projection_mean_preserved')
        missing=sum(Q(t*hist[t],n) for t in xs if t>ell and not hist.get(t-1,0))
        gap=sum(w*(b-a) for w,a,b in zip(weights,dr,dp))/n
        ck(gap==missing,'projected_missing_bin_identity')
        ck(sum(w*(b-a)**2 for w,a,b in zip(weights,dr,dp))/n<=m*missing,'missing_bin_squared_bound')
        for h in [Q(3,4),Q(1,32),Q(1,2048)]:
            intervals=[raw_enclosure(hist,x,h) for x in xs]
            lo=isotonic([z[0] for z in intervals],weights)
            hi=isotonic([z[1] for z in intervals],weights)
            bound=m*n*(n+3)*h
            ck(all(p-bound<=a<=b<=p+bound for p,a,b in zip(dp,lo,hi)),'positive_h_isotonic_uniform_interval')
            ck(all(Q(0)<=a<=b<=m for a,b in zip(lo,hi)),'positive_h_sample_max_envelope_interval')
            # Check consistency with the exact h>0 mean identity.
            exp_lo,exp_hi=exp_positive_bounds(h)
            mean=Q(sum(sample),n);lost=Q(ell*hist[ell],n)
            predicted_lo=mean-lost/exp_lo;predicted_hi=mean-lost/exp_hi
            calc_lo=sum(w*v for w,v in zip(weights,lo))/n
            calc_hi=sum(w*v for w,v in zip(weights,hi))/n
            ck(max(predicted_lo,calc_lo)<=min(predicted_hi,calc_hi),'full_source_mean_identity_interval_consistency')
    return len(samples)

def multinomial_checks():
    for n in range(1,8):
        for probs in [(Q(1,4),Q(1,2),Q(1,4)),(Q(2,5),Q(1,10),Q(1,2)),(Q(1),Q(0),Q(0))]:
            for t in [1,2]:
                expectation=Q(0)
                for a in range(n+1):
                    for b in range(n-a+1):
                        c=n-a-b;ks=[a,b,c]
                        mass=Q(factorial(n),factorial(a)*factorial(b)*factorial(c))
                        for k,p in zip(ks,probs):mass*=p**k
                        if ks[t-1]==0:expectation+=ks[t]*mass
                ck(expectation==n*probs[t]*(1-probs[t-1])**(n-1),'multinomial_missing_predecessor_exact')
                ck(probs[t-1]*(1-probs[t-1])**(n-1)<=Q(1,n),'empty_predecessor_mass_bound')

def binmass(y,alpha):return [(u,Q(comb(y,u))*alpha**u*(1-alpha)**(y-u)) for u in range(y+1)]
def finite_score_checks():
    for y in range(16):
        for alpha in [Q(1,8),Q(1,3),Q(2,3),Q(15,16)]:
            eta=1-alpha
            scores={}
            for c in [Q(0),Q(1,2),Q(3,5)]:
                direct=sum(p*((c*u-alpha*(y-u)/eta)**2-(alpha*(y-u)/eta)**2) for u,p in binmass(y,alpha))
                formula=c*c*(alpha*eta*y+alpha*alpha*y*y)-2*c*alpha*alpha*y*(y-1)
                ck(direct==formula,'actual_n1_family_centered_score')
                scores[c]=direct
                if not y:continue
                A=lambda v:c*c*v*v
                F=lambda v:c*v
                c1=A(y)-2*y*F(y-1)
                anchor=c1+2*eta*y*F(y-1)
                correction0=sum(p*(A(u)-A(y)) for u,p in binmass(y,alpha) if u<y)
                correction1=-2*alpha*y*sum(p*(F(u)-F(y-1)) for u,p in binmass(y-1,alpha) if u<y-1)
                ck(direct==anchor+correction0+correction1,'rare_deletion_anchor_exact')
                q0=1-alpha**y;q1=1-alpha**(y-1)
                L=q0*y*y+2*alpha*q1*y*y
                ck(L<=eta*(y**3+2*y*y*(y-1)),'rare_deletion_range_bound')
            if alpha>Q(1,3):
                choose=scores[Q(1,2)]<scores[Q(0)]
                ck(choose==(y>=2),'actual_n1_adaptive_threshold')
                # The plug-in/refit correction integrand is nonzero only at y=2.
                now=Q(1,2) if y>=2 else Q(0)
                before=Q(1,2) if y>=3 else Q(0)
                integrand=2*y*(now-before)*(y-1) if y else Q(0)
                ck(integrand==(2 if y==2 else 0),'actual_n1_optimism_integrand')
    for B in range(1,7):
        for alpha in [Q(2,3),Q(3,4),Q(7,8)]:
            ck((alpha**2)**B==alpha**(2*B),'naive_zero_deletion_probability')

if __name__=='__main__':
    histograms=histogram_checks();multinomial_checks();finite_score_checks()
    print(json.dumps({'status':'PASS_INDEPENDENT_SCOPED_CONTROLS','exact_assertions':sum(checks.values()),'histograms':histograms,'counts':dict(sorted(checks.items())),'scope':'Independent finite rational source-smoother enclosures, max-min isotonic identities, missing-bin combinatorics and anchored-score algebra. Asymptotic rates and full scope are assessed in the analytic review.'},indent=2,sort_keys=True))
