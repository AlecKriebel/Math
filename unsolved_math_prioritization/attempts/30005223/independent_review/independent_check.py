#!/usr/bin/env python3
"""Independent exact Frobenius-alternant character controls.

No author module or external program is imported. Counts below are finite
controls; the analytical limits are reviewed separately in the report.
"""
from collections import Counter, defaultdict
from fractions import Fraction as F
from functools import lru_cache
from itertools import permutations
from math import comb, factorial, gcd, prod
import json
C=Counter()
def ck(test,key):
    assert test,key
    C[key]+=1
@lru_cache(None)
def partitions(n,cap=None):
    if not n:return ((),)
    cap=n if cap is None else cap
    return tuple((a,)+b for a in range(min(n,cap),0,-1) for b in partitions(n-a,a))
def transpose(lam):return tuple(sum(x>=j for x in lam) for j in range(1,lam[0]+1))
@lru_cache(None)
def signs(L):
    return tuple((p,(-1)**sum(p[i]>p[j] for i in range(L) for j in range(i+1,L))) for p in permutations(range(L)))
@lru_cache(None)
def power_product(mu,L):
    # Coefficients of product_j (x_1^mu_j+...+x_L^mu_j).
    d={(0,)*L:1}
    for a in mu:
        e=defaultdict(int)
        for mon,v in d.items():
            for i in range(L):
                new=list(mon);new[i]+=a;e[tuple(new)]+=v
        d=dict(e)
    return d
@lru_cache(None)
def character(lam,mu):
    if not lam:return int(not mu)
    if len(lam)>lam[0]:
        return (-1)**(sum(mu)-len(mu))*character(transpose(lam),mu)
    d=power_product(mu,len(lam))
    # Frobenius alternant: coefficient at lambda+rho in Delta times p_mu.
    return sum(s*d.get(tuple(lam[i]-i+p[i] for i in range(len(lam))),0) for p,s in signs(len(lam)))
def z(mu):return prod(j**a*factorial(a) for j,a in Counter(mu).items())
def hooks(lam):
    cols=transpose(lam)
    return [lam[i]-j+cols[j]-i-1 for i in range(len(lam)) for j in range(lam[i])]
def three(lam,mu):
    hs=hooks(lam)
    I=all(h%mu[0] for h in hs)
    II=any(all(h%a for h in hs) for a in mu)
    III=any(sum(a//t for a in mu if a%t==0)>sum(h%t==0 for h in hs) for t in range(1,sum(mu)+1))
    return I,II,III
small=[]
for n in range(1,10):
    ps=partitions(n);P=len(ps);tab=[[character(l,m) for m in ps] for l in ps]
    for i,l in enumerate(ps):
        ck(tab[i][-1]==factorial(n)//prod(hooks(l)),'hook_dimensions')
        for j,m in enumerate(ps):
            ck(character(transpose(l),m)==(-1)**(n-len(m))*tab[i][j],'conjugate_sign')
            ts=three(l,m)
            ck(not ts[2] or tab[i][j]==0,'weighted_type_III_sufficiency')
    for i,m in enumerate(ps):
        for j,nu in enumerate(ps):
            ck(sum(row[i]*row[j] for row in tab)==(z(m) if i==j else 0),'full_column_orthogonality')
    zero=F(sum(v==0 for row in tab for v in row),P*P)
    small.append({'n':n,'partitions':P,'uniform_table_zero_fraction':str(zero)})
    for size in range(n+1):
        for nu in partitions(size):
            if any(a<3 for a in nu):continue
            R=n-size;s=R//2;mus=[tuple(sorted(nu+(2,)*r+(1,)*(R-2*r),reverse=True)) for r in range(s+1)]
            diags=[]
            for l in ps:
                vals=[character(l,m) for m in mus]
                aa=[]
                for j in range(s+1):
                    mask=(1<<j)-1
                    a=F(sum((-1)**((x&mask).bit_count())*vals[x.bit_count()] for x in range(1<<s)),1<<s)
                    ck(a.denominator==1,'direct_boolean_trace_integrality');aa.append(a)
                for r in range(s+1):
                    mask=(1<<r)-1
                    direct=sum((-1)**((x&mask).bit_count())*aa[x.bit_count()] for x in range(1<<s))
                    ck(direct==vals[r],'direct_boolean_trace_reconstruction')
                top=max((j for j,a in enumerate(aa) if a),default=-1)
                ck(sum(v==0 for v in vals)<=top if top>=0 else all(v==0 for v in vals),'fiber_polynomial_degree_bound')
                d=sum((F(v*v,z(m)) for v,m in zip(vals,mus)),F(0));diags.append(d)
                ck(0<=d<=1,'projection_diagonal_interval')
            q=s+1;v=sum(d*d for d in diags)
            ck(sum(diags)==q,'projection_trace')
            ck(F(sum(d==0 for d in diags),P)<=1-F(q*q,P*v),'projection_fourth_moment_zero_bound')
    # Direct support/normalization checks from independently evaluated tables.
    if n>1:
        prev=partitions(n-1);Bprev=sum(character(l,m)!=0 for l in prev for m in prev)
        B=sum(v!=0 for row in tab for v in row)
        def down(l):
            return tuple(tuple(v for v in l[:i]+(l[i]-1,)+l[i+1:] if v) for i in range(len(l)) if i+1==len(l) or l[i]>l[i+1])
        dns={l:down(l) for l in ps};dn=max(map(len,dns.values()));bn=max(sum(l in ds for ds in dns.values()) for l in prev)
        for m in prev:
            for l in ps:ck(character(l,m+(1,))==sum(character(a,m) for a in dns[l]),'restriction_branching')
            for a in prev:ck(sum(character(l,m+(1,)) for l in ps if a in dns[l])==(m.count(1)+1)*character(a,m),'induction_branching')
        ck(F(Bprev,dn)<=B<=bn*Bprev+P*(P-len(prev)),'branching_support_bounds')
        r=F(len(prev),P);Q=F(Bprev,len(prev)**2);Qnext=F(B,P*P)
        ck(r*r*Q/dn<=Qnext<=bn*r*r*Q+1-r,'branching_normalization')
# Standard-row family, independent alternant formula and direct gcd classification.
for m in range(2,20):
    l=(m,1)
    for nu in partitions(m):
        if nu[-1]==1:continue
        mu=nu+(1,)
        ck(character(l,mu)==0,'standard_row_residual_zero')
        ck(three(l,mu)[2]==(gcd(*nu)>1),'standard_row_exact_gcd')
# S11 actual irreducible witness and complete S5 residual, independently recovered.
lam=(5,2,2,2);nu=(3,3);res={m:character(lam,tuple(sorted(nu+m,reverse=True))) for m in partitions(5)}
coeff={a:sum((F(res[m]*character(a,m),z(m)) for m in partitions(5)),F(0)) for a in partitions(5)}
coeff={a:c for a,c in coeff.items() if c}
ck(coeff=={(5,):F(2),(2,2,1):F(-2),(2,1,1,1):F(2)},'S11_complete_residual_Schur_coefficients')
for m,val in res.items():ck(val==(6 if m in ((3,2),(3,1,1)) else 0),'S11_complete_residual_power_sum')
for r in range(3):
    m=tuple(sorted(nu+(2,)*r+(1,)*(5-2*r),reverse=True))
    ck(character(lam,m)==0 and not any(three(lam,m)),'S11_zero_fiber_outside_III')
# Exact rational algebra underlying the two saddle scales.
for c in (F(1),F(4,3),F(5,2)):
    for u in range(3,28):
        t=c/u
        for v in range(1,42):
            ck(4*c*v-2*t*v*v-2*c*c/t==-2*t*(v-u)**2,'squared_partition_weight_saddle')
            ck(2*c*v-t*v*v-c*c/t==-t*(v-u)**2,'single_partition_weight_saddle')
            if F(3,4)<=F(v,u)<=F(5,4):
                # Difference of square roots is (m-n)/(sqrt(m)+sqrt(n)).
                ck((v-u)**2==F((v*v-u*u)**2,(v+u)**2),'central_window_exact_scale_identity')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'families':dict(C),'small_tables':small,'S11_residual_Schur_coefficients':{str(a):str(c) for a,c in coeff.items()},'method':'Independent Frobenius alternant plus Boolean Fourier sums; no author-code imports. Finite controls are not asymptotic proofs.'},indent=2))
