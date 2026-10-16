#!/usr/bin/env python3
"""Fresh finite adversarial probes; these supplement, never certify, the proof."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json
import math

out = {"status": "passed", "scope": "Finite exact/numerical probes and closed-form negative controls; general proof requires analytic reconstruction."}

# Nonuniformity control: each orbit has a finite flat plateau, but their
# lengths tend to infinity. Adjacent density ratios stay in [1/2,2]. For
# each fixed d select k>d, so rho(-d,k)=rho(0,k)=rho(d,k)=1.
rho = lambda n,k: F(2) ** (-max(0, abs(n)-k))
checks = 0
for k in range(1,31):
    for n in range(-40,41):
        assert F(1,2) <= rho(n+1,k)/rho(n,k) <= 2
        checks += 1
for d in range(1,31):
    assert rho(-d,d+1) == rho(0,d+1) == rho(d,d+1) == 1
    checks += 1
out["unbounded_plateaux"] = {"exact_checks": checks, "deduction": "No common d,eta<1 can satisfy the density condition, despite each finite-plateau orbit being generalized hyperbolic."}

# Independent q=infinity witness for p=1: triangular tents fit inside the
# central unit-weight plateau, so the difference norm tends to zero.
tents = []
for k in (2,4,8,16,32,64):
    h = lambda n: max(F(0),1-F(abs(n),k))
    defect = max(abs((rho(n-1,k)/rho(n,k))*h(n-1)-h(n)) for n in range(-k-2,k+3))
    assert defect == F(1,k)
    tents.append({"k": k, "norm": 1, "difference_norm": str(defect)})
out["p1_uniformity_obstruction"] = tents

# Exact cutoff identity and bound, with small alternating weight errors,
# square m so the published geometric r is rational. Tiny fiber measure
# must cancel in the normalized ratio. All terms use rational arithmetic;
# q roots are evaluated only after the exact sums are established.
cutoff = []
for t in (2,4,8,16):
    m=t*t; r=1-F(1,t); eps=F(1,m**3); n0=3
    chi=lambda n: r**abs(n-n0) if abs(n-n0)<=m else F(0)
    b=lambda n: 1+eps*(F(-1)**n)
    defects=[]
    hs=[]
    for n in range(n0-m-2,n0+m+3):
        h=chi(n); sh=b(n)*chi(n-1)
        rhs=(chi(n-1)-chi(n))+chi(n-1)*(b(n)-1)
        assert sh-h == rhs
        defects.append(abs(sh-h)); hs.append(abs(h))
    for q in (1,2,4,math.inf):
        if math.isinf(q):
            ratio=float(max(defects)/max(hs))
            error_bound=float((1-r)/r+4*r**m+2*eps)
        else:
            ratio=(float(sum(x**q for x in defects))/float(sum(x**q for x in hs)))**(1/q)
            error_bound=float((1-r)/r+4*r**m)+2*float(eps)*(2*m+1)**(1/q)
        assert ratio <= error_bound+1e-14
        cutoff.append({"m": m,"q": "infinity" if math.isinf(q) else q,"normalized_defect": ratio,"certificate_bound": error_bound})
out["cutoff_transfer"] = cutoff

# A fresh exact two-residue cut exhibits why a power split cannot simply
# be reused one step: A0 fails one-step invariance, while the prescribed
# intersection A(n)=A0(n) and A0(n+1) repairs it.
def rr(n):
    k,s=divmod(n,2)
    return F(2)**(-abs(k-(0 if s==0 else 5)))
A0=lambda n:rr(n-2)<=rr(n)/2
A=lambda n: A0(n) and A0(n+1)
bad0=[]; repaired=0
for n in range(-30,31):
    assert min(rr(n-2),rr(n+2)) <= rr(n)/2
    if A0(n) and not A0(n-1): bad0.append(n)
    if A(n): assert A(n-1)
    else: assert not A(n+1)
    repaired+=1
assert bad0
out["power_to_one_step"]={"A0_one_step_failures":bad0,"intersection_cases_passed":repaired}

# Test strict drops arbitrarily close to one, and a sparse strong-drop
# scale, rather than only the submitted verifier's eta=1/2 dyadic data.
strict_drops=[]
values=(F(1,100),F(1,3),F(1),F(3),F(100))
for eta in (F(1,100),F(1,2),F(9,10),F(99,100)):
    count=0
    for seq in product(values,repeat=5):
        if not all(min(seq[i-1],seq[i+1])<=eta*seq[i] for i in (1,2,3)):
            continue
        neg=lambda i:seq[i-1]<=eta*seq[i]
        if neg(2): assert neg(1)
        else: assert not neg(3)
        count+=1
    assert count
    strict_drops.append({"eta":str(eta),"admissible_five_term_sequences":count})
out["strict_drop_near_one"]=strict_drops

out["excluded_p_infinity_boundary"]={"density":"rho(n)=2^n","finite_p":"T is a contraction of norm2^(-1/p)","p_infinity":"T is an isometry; x(j)=j delta times1 cannot be uniformly shadowed by any bounded L-infinity orbit","scope":"Closed-form scope counterexample; p=infinity is correctly excluded."}

# Stone residue argument is finite and independent of atom/separability:
# shift by r sends every residue modulo r+1 to a different residue.
residue_checks=0
for r in range(1,101):
    for n in range(r+1):
        assert (n-r)%(r+1) != n
        residue_checks+=1
out["stone_aperiodicity_residue_checks"]=residue_checks

# The source equation33's norm equality itself is false in an allowed
# Kaplansky module. U=c(n)shift with positive periodic c=(4,1/4,1) is
# conjugate to the plain shift by multiplier h=(4,1,1). A second disjoint
# component uses plain U and b=2, so r=1 is an interior spectral gap and
# P1 is the first component. On P1, T=bU with b=(1/4,1/2,3/4).
c=(F(4),F(1,4),F(1)); b=(F(1,4),F(1,2),F(3,4)); h=(F(4),F(1),F(1))
assert all(c[n]==h[n]/h[(n-1)%3] for n in range(3))
lhs=tuple(b[n]*b[(n+1)%3]/(c[(n+1)%3]*c[(n+2)%3]) for n in range(3))
rhs=tuple(b[n]*b[(n-1)%3]/(c[(n+1)%3]*c[(n+2)%3]) for n in range(3))
assert lhs == (F(1,2),F(3,32),F(3,16))
assert rhs == (F(3,4),F(1,32),F(3,8))
assert max(lhs)!=max(rhs)

# The replacement identity can nevertheless repair the growth conclusion:
# tildeT^n=U^(1-n)T^nU^(-n-1). Verify all factors pointwise for n=1..10.
def Ucoef(n,k):
    if k>=0: return math.prod(c[(n-j)%3] for j in range(k))
    return 1/math.prod(c[(n+j)%3] for j in range(1,-k+1))
for k in range(1,11):
    for n in range(3):
        direct=math.prod(b[(n+j)%3]/c[(n+j+1)%3] for j in range(k))
        j=n-(1-k)
        middle=math.prod(b[(j-i)%3]*c[(j-i)%3] for i in range(k))
        composed=Ucoef(n,1-k)*middle*Ucoef(j-k,-k-1)
        assert direct==composed
out["equation33_norm_counterexample"]={"left_coefficients":list(map(str,lhs)),"middle_coefficients":list(map(str,rhs)),"left_norm":str(max(lhs)),"middle_norm":str(max(rhs)),"replacement_identity_checks":30,"scope":"The displayed equality is false; the old theorem is not refuted, and its growth conclusion has a repair."}

Path(__file__).with_name("BOUNDARY_PROBES.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps(out,indent=2))
