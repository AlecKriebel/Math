"""Exact scope checks; these do not verify the main asymptotic proof."""
from fractions import Fraction as Q
from math import comb,isqrt
import json
# Pair p=2^-k and 1-2^-k each has mass 2^-k, k>=2.
# The sums are geometric; the law is fixed, merely elliptic, with no inverse first moment.
normalization=2*(Q(1,4)/(1-Q(1,2)))
delta=2*(Q(1,16)/(1-Q(1,4))-Q(1,64)/(1-Q(1,8)))
assert normalization==1 and delta==Q(11,84)
assert Q(1,4)-delta==Q(5,42)
# Fixed-law quantifier cannot be replaced by a triangular array of near-arrow laws.
# At horizon N choose p in {2^-N,1-2^-N} equally at each site.
# Every environment has a distinguished arrow path of mass >=1-N 2^-N.
# Its M-site endpoint cell has annealed mass <=M times binomial peak.
rows=[]
for N in [16,256,4096]:
    M=isqrt(isqrt(N));peak=Q(comb(N,N//2),2**N)
    lower=2*(1-Q(N,2**N)-M*peak)
    assert lower>1 and 1<=M<N
    rows.append({'N':N,'M':M,'quenched_coarse_L1_uniform_lower_bound':float(lower)})
result={'status':'PASS','heavy_tail_fixed_law':{'q':'1/2','a':'1/4','delta':str(delta),'variance_p':'5/42','mass_sum':str(normalization),'support':'p=2^-k and 1-2^-k, each mass 2^-k for k>=2','uniform_ellipticity':False,'E_inverse_p':'infinite'},'triangular_near_arrow_law':rows,'scope':'Boundary checks only: fixed heavy-tailed law is admissible, while uniformity over N-dependent near-arrow laws is false.'}
print(json.dumps(result,indent=2,sort_keys=True))
