#!/usr/bin/env python3
"""Exact small certificate for enormous existence parameters, not enumeration."""
from fractions import Fraction as F
from math import comb
from pathlib import Path
import json
n=1<<256
p=F(1,1<<384)
m=1<<320
M=comb(n,3)
c=F(1,645120)
a=c*c/2
checks={}
def check(name,predicate):
    assert predicate,name
    checks[name]='PASS'
check('n_fourth_power',n==(1<<64)**4)
check('m_exponent',m==(1<<64)**5)
check('triangle_probability',p*p==F(1,n**3))
check('seven_set_double_count_identity',F(comb(n,7),n-6)==F(comb(n,6),7))
check('surviving_witness_lower_bound',F(comb(n,6),7)-m*M >= c*n**6)
mu_upper=F(M*M,2)*p*p
Delta_upper=M**3*p**3
check('janson_denominator_bound',mu_upper+Delta_upper <= (1<<1152)) # n^(9/2)
check('janson_rate_constant',a>F(1,1<<41))
check('janson_negative_exponent',a*(1<<384)>(1<<343))
# log(m+1)<=2m and log(n)<256 bound the logarithm of all placements/deletions.
log_prefactor_upper=770*m+5120*n
check('entropy_bound',log_prefactor_upper<(1<<331))
check('net_negative_exponent',(1<<343)-log_prefactor_upper>(1<<342))
expected_conflicts=comb(n,2)*comb(n-2,2)*p*p
check('conflict_expectation',expected_conflicts<=F(n,4))
check('conflict_markov',expected_conflicts/m<=F(1,1<<66))
lam=M*p
check('triangle_mean',lam>(1<<379))
check('chebyshev_bound',4/lam<F(1,1<<377))
check('retained_faces_nonplanar',lam/2-m>n)
# e^(-2^342)<1/8; the other two bounds are rational.
check('combined_failure_below_one',F(1,8)+F(1,1<<66)+F(1,1<<377)<1)
result={'passed':len(checks),'failed':0,'arithmetic':'exact Python integers and Fraction','parameters':{'n':'2^256','p':'2^-384','m':'2^320'},'checks':checks,'scope':'Checks finite probability inequalities only; no random sampling or enumeration, and no verification of imported theorems.'}
Path(__file__).with_name('check_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
