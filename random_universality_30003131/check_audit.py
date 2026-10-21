import math, itertools, json
from pathlib import Path

def require(condition, message):
    if not condition:
        raise RuntimeError(message)
# Finite sanity checks supplement, rather than replace, the analytic audit.
max_tail_ratio=0.0
for b in range(1,201):
    p=sum(math.comb(3*b,j) for j in range(b))/2**(3*b)
    max_tail_ratio=max(max_tail_ratio,p/math.exp(-b/12))
    require(p<=math.exp(-b/12), f'Binomial bound failed at b={b}')
count=0
for n in range(1,11):
    for ell in range(1,n+1):
        for S in itertools.combinations(range(1,n+1),ell):
            shifts=[set(s+t for s in S) for t in range(1,n+1)]
            deg=max(sum(bool(A&B) for j,B in enumerate(shifts) if i!=j) for i,A in enumerate(shifts))
            require(deg<=ell*(ell-1), f'Overlap bound failed at n={n}, S={S}')
            count+=1
# An explicit conservative large-n regime: x=log(n)>=32, b<=49x.
# e^x/x^3 is increasing for x>3, so this base check proves the required
# inequality n>=117600(log n)^3 throughout that real interval.
x=32
require(math.exp(x)>=117600*x**3, 'Asymptotic base inequality failed')
require(6*49*x<=2*math.exp(x), 'Strip allocation base inequality failed')
result={'binomial_tail_b_range':[1,200], 'max_tail_to_chernoff_bound_ratio':max_tail_ratio,
        'dependency_support_sets_checked':count,'explicit_log_n_threshold':32,
        'explicit_c':'1/2352', 'base_asymptotic_ratio':math.exp(x)/(117600*x**3),
        'status':'PASS','scope':'finite checks plus explicit threshold algebra, not a formal proof assistant certificate'}
print(json.dumps(result,indent=2))
