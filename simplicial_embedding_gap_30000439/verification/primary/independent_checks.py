"""Independent exact arithmetic and finite sanity checks for the primary audit.
These do not replace the universal proofs in PRIMARY_REPORT.md.
No third-party packages, frozen proof scripts, or historical reviews are used.
"""
from datetime import datetime, timezone
from decimal import Decimal, localcontext
from fractions import Fraction as F
from itertools import combinations
from math import comb
from pathlib import Path
import json, random

checks=[]
def check(label,condition):
    if not condition: raise AssertionError(label)
    checks.append(label)

def det(a):
    a=[list(map(F,row)) for row in a]
    out=F(1)
    for k in range(len(a)):
        pivot=next((i for i in range(k,len(a)) if a[i][k]),None)
        if pivot is None:return F(0)
        if pivot!=k:a[k],a[pivot]=a[pivot],a[k];out=-out
        q=a[k][k];out*=q
        for i in range(k+1,len(a)):
            ratio=a[i][k]/q
            for j in range(k+1,len(a)):a[i][j]-=ratio*a[k][j]
            a[i][k]=0
    return out

# Independent cofactor test: the signs of ordered 5-minors determine every
# 6-point Radon split. Universal existence for 7 points is proved in the report.
rng=random.Random(43916)
accepted=0
attempts=0
while accepted<100 and attempts<2000:
    attempts+=1
    pts=[[rng.randint(-10,10) for _ in range(4)] for _ in range(7)]
    minors={s:det([[1]*5]+[[pts[i][j] for i in s] for j in range(4)])
            for s in combinations(range(7),5)}
    if not all(minors.values()):continue
    balanced=0
    for s in combinations(range(7),6):
        coefficients=[(-1)**k*minors[s[:k]+s[k+1:]] for k in range(6)]
        check(f'affine_cofactor_relation_{accepted}_{s}',
              sum(coefficients)==0 and all(sum(coefficients[k]*pts[s[k]][j] for k in range(6))==0 for j in range(4)))
        if sum(c>0 for c in coefficients)==3:balanced+=1
    check(f'seven_point_balanced_witness_{accepted}',balanced>=1)
    accepted+=1
check('100_generic_rational_placements_checked',accepted==100)

# Whole-triangle event coordinates; W is a simple graph on triangle IDs.
# Overlap denominator is the diagonal plus ordered distinct common-ID pairs.
p=F(1,3)
for trial in range(24):
    edges=[e for e in combinations(range(8),2) if rng.random()<0.4]
    if not edges:edges=[(0,1)]
    mu=len(edges)*p*p
    overlap=sum(bool(set(a)&set(b)) for a in edges for b in edges if a!=b)
    delta=overlap*p**3
    B=mu+delta
    pr0=F(0)
    for mask in range(1<<8):
        if not any((mask>>a)&1 and (mask>>b)&1 for a,b in edges):
            k=mask.bit_count();pr0+=p**k*(1-p)**(8-k)
    with localcontext() as ctx:
        ctx.prec=70
        q=Decimal(pr0.numerator)/Decimal(pr0.denominator)
        a=mu*mu/(2*B)
        bound=(-Decimal(a.numerator)/Decimal(a.denominator)).exp()
        check(f'exact_small_Janson_product_sample_{trial}',q<=bound)
check('ordered_star_overlap_is_6',sum(bool(set(a)&set(b)) for a in [(0,1),(0,2),(0,3)] for b in [(0,1),(0,2),(0,3)] if a!=b)==6)

# Huge n is symbolic, never enumerated. All displayed rational bounds fit
# standard-library integers; the forbidden giant exponent is not evaluated.
n=2**256;m=2**320;p=F(1,2**384);c=F(1,645120);M=comb(n,3)
check('fourth_power_and_sampling_parameters',m**4==n**5 and p*p==F(1,n**3))
check('robust_pair_lower_bound',F(comb(n,6),7)-m*M>=c*n**6)
mu_lower=c*n**6*p*p
B_upper=F(M*M,2)*p*p+M**3*p**3
check('mean_lower',mu_lower==c*n**3)
check('ordered_overlap_plus_diagonal_bound',B_upper<=2**1152)
check('Janson_exponent_gt_2pow343',c*c*2**384/2>2**343)
check('log_prefactor_lt_2pow331',770*m+5120*n<2**331)
check('failure_exponent_gt_2pow342',2**343-2**331>2**342)
check('exp_failure_lt_one_eighth_using_exp_x_ge_1_plus_x',2**342>7)
lam=M*p
check('lambda_ge_n_three_halves_over_24',lam>=F(2**384,24))
check('lambda_gt_2pow379',lam>2**379)
check('Chebyshev_failure_lt_2pow_minus377',4/lam<F(1,2**377))
check('cleaned_triangle_count_exceeds_n',lam/2-m>n)
check('Markov_failure_at_m',F(n,4*m)==F(1,2**66))
check('sum_of_failure_bounds_lt_one',F(1,8)+F(1,2**66)+F(1,2**377)<1)
# Goodman's original finite component proof gives D=4 binom(n,5).
D=4*comb(n,5)
check('Goodman_finite_base_bound_at_huge_n',D+2<=n**5)

out={'timestamp_utc':datetime.now(timezone.utc).isoformat(),
     'scope':'Independent exact arithmetic and finite sanity checks; universal geometry and source semantics are checked in PRIMARY_REPORT.md',
     'generic_placements':accepted,'attempts':attempts,'checks_passed':len(checks),'checks':checks}
root=Path(__file__).resolve().parent
(root/'independent_check_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='checks'},indent=2))
