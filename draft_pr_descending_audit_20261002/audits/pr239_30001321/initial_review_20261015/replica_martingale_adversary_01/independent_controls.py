"""Independent exact diagnostics for the assigned TURN_1/TURN_2 input family.
No original checker is imported. Fractions only; finite diagnostics do not prove
any asymptotic statement. Laws deliberately differ from source checker laws.
"""
from fractions import Fraction as F
from collections import Counter, defaultdict
from itertools import product
from math import comb, factorial
import json, platform, sys
C=Counter()
def ck(test,label):
    if not test: raise AssertionError(label)
    C[label]+=1
laws=[
 ('deterministic_biased',(F(2,7),),(F(1),)),
 ('biased_near_arrow',(F(1,1000),F(999,1000)),(F(1,7),F(6,7))),
 ('skew_three_point',(F(1,100),F(1,3),F(97,100)),(F(1,10),F(2,5),F(1,2))),
]
def step_mu(mu,ps):
    nxt=defaultdict(F)
    for x,w in mu.items():
        nxt[x+1]+=w*ps[x];nxt[x-1]+=w*(1-ps[x])
    return dict(nxt)
def anneal(n,q):
    return {2*j-n:F(comb(n,j))*q**j*(1-q)**(n-j) for j in range(n+1)}
def configs(sites,values,probs):
    for inds in product(range(len(values)),repeat=len(sites)):
        w=F(1)
        for i in inds:w*=probs[i]
        yield dict(zip(sites,(values[i] for i in inds))),w
law_records=[]
for name,values,probs in laws:
    q=sum(p*w for p,w in zip(values,probs));a=q*(1-q)
    delta=sum(p*(1-p)*w for p,w in zip(values,probs));sigma=a-delta
    ck(sum(probs)==1 and 0<delta<=a<=F(1,4),'fixed_law_domain')
    # Derive the half-gap one-step transition directly from joint local coins.
    for gap in [-2,-1,0,1,2]:
        direct=defaultdict(F)
        assignments=configs([0] if gap==0 else [0,2*gap],values,probs)
        for env,ew in assignments:
            px=env[2*gap] if gap else env[0];py=env[0]
            for sx,sy in product([-1,1],repeat=2):
                mass=(px if sx==1 else 1-px)*(py if sy==1 else 1-py)
                direct[gap+(sx-sy)//2]+=ew*mass
        z=delta if gap==0 else a
        ck(dict(direct)=={gap-1:z,gap:1-2*z,gap+1:z},'direct_pair_transition')
    # Forward return propagation and independent backward profile propagation.
    forward={0:F(1)};u={0:F(1)};profiles=[u];gs=[F(1)]
    for n in range(1,65):
        nxt=defaultdict(F)
        for d,w in forward.items():
            z=delta if d==0 else a
            nxt[d-1]+=w*z;nxt[d]+=w*(1-2*z);nxt[d+1]+=w*z
        forward=dict(nxt)
        backward={}
        for d in range(-n,n+1):
            z=delta if d==0 else a
            backward[d]=z*u.get(d-1,F(0))+(1-2*z)*u.get(d,F(0))+z*u.get(d+1,F(0))
        ck(forward[0]==backward[0],'forward_backward_return_agreement')
        ck(sum(forward.values())==1,'forward_chain_normalization')
        ck(backward[0]<=gs[-1],'return_monotonicity_new_laws')
        ck(backward[0]**2*(n+1)*delta**2<=a,'conservative_analytic_heat_bound_finite')
        for d in range(n+1):
            ck(backward[d]==backward[-d],'backward_symmetry_new_laws')
            ck(backward[d]>=backward.get(d+1,F(0)),'backward_radial_order_new_laws')
        u=backward;profiles.append(u);gs.append(u[0])
    # Check exact gradients by two descriptions; parity and every alignment.
    for t in range(0,13):
        b=anneal(t,q);peak=max(b.values())
        keys=set(b)|{x-2 for x in b}
        dif={x:b.get(x+2,F(0))-b.get(x,F(0)) for x in keys}
        tv=sum(abs(w) for w in dif.values());adj=max(abs(w) for w in dif.values())
        ck(tv==2*peak,'binomial_unimodal_total_variation')
        for M in range(1,8):
            for shift in range(M):
                for x in [-2,-1,0,1,2]:
                    h=defaultdict(F);h2=defaultdict(F)
                    for y,w in b.items():
                        h[(x+1+y-shift)//M]+=w
                        h[(x-1+y-shift)//M]-=w
                    for y,w in dif.items():
                        h2[(x+1+y-shift)//M]-=w
                    ck(all(h[k]==h2[k] for k in set(h)|set(h2)),'semigroup_gradient_reindexing')
                    ck(sum(abs(w) for w in h.values())<=tv,'partition_gradient_total_variation')
                    ck(max(abs(w) for w in h.values())<=min(2*peak,M*adj),'partition_gradient_sup_bound')
                    ck(sum(w*w for w in h.values())<=min(2*peak,M*adj)*tv,'partition_squared_gradient_bound')
        for M in range(1,12):
            for shift in range(M):
                residue=sum(w for x,w in b.items() if (x-shift)%M==0)
                ck(residue<=F(2,M)+2*peak,'parity_residue_bound_new_laws')
    # Start from an arbitrary nontrivial old parity law, rather than delta_0.
    old={-2:F(1,7),0:F(2,7),2:F(4,7)}
    f=lambda x:max(F(0),min(F(1),F(x+4,8)))
    kernels={t:anneal(t,q) for t in [0,1,2]}
    T=lambda t,x:sum(w*f(x+y) for y,w in kernels[t].items())
    mean=sum(w*T(2,x) for x,w in old.items());I0=sum(w*w for w in old.values())
    var=F(0);Qavg=F(0);EI=[I0,F(0),F(0)];mom=[F(0)]*7
    grad0={x:T(1,x+1)-T(1,x-1) for x in old}
    var0=sigma*sum(w*w*grad0[x]**2 for x,w in old.items())
    grad1={x:f(x+1)-f(x-1) for x in [-3,-1,1,3]}
    for env0,w0 in configs(sorted(old),values,probs):
        mid=step_mu(old,env0);I1=sum(w*w for w in mid.values())
        M1=sum(w*T(1,x) for x,w in mid.items())
        d0=sum(w*(env0[x]-q)*grad0[x] for x,w in old.items())
        ck(M1-mean==d0,'smoothed_layer_increment_first')
        ck(abs(d0)<=F(1,4),'lipschitz_increment_bound_first')
        var1=sigma*sum(w*w*grad1[x]**2 for x,w in mid.items())
        ck(var1<=4*sigma*I1/F(8**2),'lipschitz_predictable_variance_bound')
        sumD=F(0);sumD2=F(0)
        for env1,w1 in configs(sorted(mid),values,probs):
            terminal=step_mu(mid,env1);I2=sum(w*w for w in terminal.values());w=w0*w1
            Z=sum(p*f(x) for x,p in terminal.items())
            d1=sum(p*(env1[x]-q)*grad1[x] for x,p in mid.items())
            ck(Z-M1==d1,'smoothed_layer_increment_second')
            ck(abs(d1)<=F(1,4),'lipschitz_increment_bound_second')
            sumD+=w1*d1;sumD2+=w1*d1*d1
            var+=w*(Z-mean)**2;Qavg+=w*(var0+var1)
            EI[1]+=w*I1;EI[2]+=w*I2
            for k in range(1,7):mom[k]+=w*(I0+I1+I2)**k
        ck(sumD==0,'conditional_layer_centering')
        ck(sumD2==var1,'conditional_layer_exact_variance')
    ck(var==Qavg,'two_layer_martingale_orthogonality')
    for t in range(3):
        predicted=sum(wx*wy*profiles[t].get((x-y)//2,F(0)) for x,wx in old.items() for y,wy in old.items())
        ck(EI[t]==predicted,'arbitrary_old_law_conditional_replica')
        ck(EI[t]<=gs[t],'arbitrary_old_law_conditional_maximum')
    for k in range(1,7):ck(mom[k]<=factorial(k)*sum(gs[:3])**k,'arbitrary_old_law_occupation_moments')
    law_records.append({'name':name,'values':list(map(str,values)),'probabilities':list(map(str,probs)),'q':str(q),'a':str(a),'delta':str(delta),'sigma_squared':str(sigma)})
# Fixed-law nonuniformity diagnostic: exact finite arrow-path lower bound.
N=128;M=8;eps=F(1,10**6);b=anneal(N,F(1,2));cells=defaultdict(F)
for x,w in b.items():cells[x//M]+=w
bound=2*((1-eps)**N-max(cells.values()))
ck(bound>F(7,5),'near_arrow_large_finite_discrepancy_diagnostic')
# Reconstruct all exponent inequalities symbolically as rational identities.
for d in [F(1,10**6),F(1,1000),F(1,100),F(1,8),F(249,1000)]:
    gamma=F(1,4)+d;beta=F(1,4)+d/2;eta=d/4
    ck(beta-eta-(F(1,2)-gamma)==5*d/4>0,'entropy_margin_independent')
    ck(2*beta-F(1,2)-eta==3*d/4>0,'boundary_margin_independent')
print(json.dumps({'status':'PASS','scope':'Independent finite exact diagnostics only; analytic asymptotic conclusions are in INDEPENDENT_RECONSTRUCTION.md.','exact_assertions':sum(C.values()),'families':dict(sorted(C.items())),'laws':law_records,'near_arrow_boundary_diagnostic':{'N':N,'M':M,'epsilon':str(eps),'exact_L1_lower_bound':str(bound),'lower_bound_float':float(bound),'purpose':'Shows nonuniformity as the law approaches arrow-valued; not an admissible fixed-law asymptotic counterexample.'},'runtime':{'executable':sys.executable,'version':platform.python_version()}},indent=2,sort_keys=True))
