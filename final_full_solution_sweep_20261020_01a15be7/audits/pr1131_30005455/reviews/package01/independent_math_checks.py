"""Independent review controls. Finite numerical probes are not universal proof."""
from fractions import Fraction as Q
from math import factorial, cos, sin, pi, exp, log
from pathlib import Path
import json
import numpy as np


def need(ok, message):
    if not ok:
        raise ValueError(message)


rows = [(Q(17,4),Q(13,3),Q(29,5)),(Q(13,3),Q(9,2),Q(25,4)),
        (Q(9,2),Q(5),Q(243,32)),(Q(5),Q(6),Q(729,64)),(Q(6),Q(7),Q(2187,128))]
exact = []
for A,B,T in rows:
    S=T/(1+T)
    value=(S*S+(Q(3,2)-S)**2)/Q(3,2)
    margin=1-1/A-value
    need(margin>0 and T**B.denominator >= Q(3,2)**B.numerator,"finite exact bound")
    exact.append({"A":str(A),"B":str(B),"f":str(value),"margin":str(margin)})
new_tail=sum((Q(8,5)**k/factorial(k) for k in range(5)),Q()) + Q(8,5)**5/factorial(5)/(1-Q(4,15))
old_tail=sum((Q(9,4)**k/factorial(k) for k in range(13)),Q()) + Q(9,4)**13/factorial(13)/(1-Q(9,56))
need(new_tail<6 and old_tail<Q(19,2) and Q(9,4)*(old_tail+1)<24,"exponential bounds")

rng=np.random.default_rng(113130005455)
probes=[]
for m in [3,4,5,6,7,9]:
    threshold=1/(cos(pi/(2*m))**2) if m%2 else 1.
    alpha=threshold+0.002
    for attachments in [False,True]:
        for trial in range(25):
            edges=[(i,(i+1)%m) for i in range(m)]
            if attachments:
                edges += [(0,m),(2,m+1)]
                if m>3:
                    edges += [(0,2)]
            nv=max(max(e) for e in edges)+1
            incidence=np.zeros((nv,len(edges)))
            for j,(u,v) in enumerate(edges):
                incidence[u,j]=incidence[v,j]=1
            b=np.exp(rng.uniform(-1,1,nv))
            log_a=np.array([-log(b[u]+b[v])/(alpha-1) for u,v in edges])
            def logsumexp(xs):
                top=float(np.max(xs))
                return top+log(float(np.sum(np.exp(xs-top))))
            log_sums=np.array([logsumexp(alpha*log_a[incidence[v]>0]) for v in range(nv)])
            # rates=b*S; the field divided by a depends on b and a^(alpha-1).
            field_ratio=np.exp((alpha-1)*log_a)*(incidence.T@b)
            need(float(np.max(np.abs(field_ratio-1)))<1e-12,"constructed equilibrium")
            log_D=(1-2*alpha)*log_a
            log_c=np.log(b)-log_sums
            # sqrt(c_v/D_e) is bounded on incident pairs; avoid squaring tiny S.
            P=np.zeros_like(incidence)
            for v in range(nv):
                mask=incidence[v]>0
                P[v,mask]=np.exp((log_c[v]-log_D[mask])/2)
            normalized=(alpha-1)*np.eye(len(edges))-alpha*(P.T@P)
            eigmax=float(np.linalg.eigvalsh(normalized)[-1])
            if m%2:
                theta=pi-pi/m
                c_over_D=exp(logsumexp(log_c[:m])-logsumexp(log_D[:m]))
                combined=(alpha-1)-alpha*4*sin(pi/(2*m))**2*c_over_D
                lower=alpha*cos(pi/(2*m))**2-1
                need(combined+1e-12>=lower and combined>0,"odd direction sum")
            else:
                v=np.array([(-1.)**i for i in range(m)]+[0]*(len(edges)-m))
                need(np.max(np.abs(incidence@v))==0,"even cancellation")
                combined=alpha-1
            need(eigmax>0,"nonpositive spectrum counterexample")
            probes.append({"m":m,"attachments":attachments,"trial":trial,"alpha":alpha,
                           "largest_normalized_eigenvalue":eigmax,"cycle_form_per_Dsum":combined})

scalar=[]
for alpha in [4.25,4.3,4.5,5,6,7,8,10,20,100,10000]:
    best=-float("inf");witness=None
    for a in np.linspace(1,1.5,2001):
        s=1/(1+exp(-alpha*log(a)))
        if s<a/2:
            continue
        slack=(s*s+(a-s)**2)/a-(1-1/alpha)
        if slack>best:
            best=float(slack);witness=float(a)
    need(best<0,"sampled scalar exclusion failed")
    scalar.append({"alpha":alpha,"largest_sampled_slack":best,"at_weight":witness})

# Direct rational Hessian for the old unequal-rate diameter-four path.
a=[Q(1,12),Q(1,4),Q(3,4),Q(9,4)]
rates=[Q(1,16),Q(5,24),Q(5,8),Q(15,8),Q(9,16)]
inc=[[0],[0,1],[1,2],[2,3],[3]]
sums=[sum((a[j]**2 for j in v),Q()) for v in inc]
K=[[Q(0) for _ in a] for _ in a]
for j in range(4):K[j][j]=-a[j]**(-3)
for rate,S,indices in zip(rates,sums,inc):
    for i in indices:
        for j in indices:K[i][j]+=2*rate/S**2
minors=[]
for n in range(1,5):
    matrix=[row[:n] for row in K[:n]];det=Q(1)
    for i in range(n):
        pivot=matrix[i][i];need(pivot!=0,"zero path pivot");det*=pivot
        for k in range(i+1,n):
            factor=matrix[k][i]/pivot
            for j in range(i,n):matrix[k][j]-=factor*matrix[i][j]
    need(det>0,"nonpositive path minor");minors.append(str(det))

print(json.dumps({"scope":"Fresh finite controls; analytic universal arguments separately checked in FIRST_DERIVATION.md",
                  "exact_rows":exact,"new_exp_upper":str(new_tail),"old_exp_upper":str(old_tail),
                  "cycle_probe_count":len(probes),"cycles":probes,"scalar_probes":scalar,
                  "unequal_rate_path_minors":minors},indent=2))
