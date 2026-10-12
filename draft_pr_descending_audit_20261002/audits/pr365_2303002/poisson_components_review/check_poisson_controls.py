"""Independent exact controls and falsifying constructions; no existence proof."""
from fractions import Fraction as F
import json

checks = 0
negative_controls = []

def check(condition):
    global checks
    if not condition:
        raise AssertionError('Independent control failed')
    checks += 1

def reject(name, false_claim):
    check(not false_claim)
    negative_controls.append(name)

for n in [2, 3, 4, 7, 12, 25, 100]:
    for R in [F(1, 3), F(1), F(7), F(100)]:
        for q in [F(0), F(1, 100), F(1, 8*n), F(1, 2), F(9, 10), F(99, 100)]:
            x = q*R
            lo = (1-q)/(1+q)**(n-1)
            hi = (1+q)/(1-q)**(n-1)
            parallel = R**(n-2)*(R*R-x*x)/(R-x)**n
            opposite = R**(n-2)*(R*R-x*x)/(R+x)**n
            check(parallel == hi and opposite == lo)
            check(0 < lo <= 1 <= hi)
            check(q == 0 or (lo < 1 < hi))
            if q <= F(1, 8*n):
                check(hi <= F(9, 7) < F(3, 2))
        # Probability-sphere normalization at the center must equal one,
        # regardless of radius; the deliberately wrong exponent yields R.
        correct = R**(n-2)*R*R/R**n
        wrong = R**(n-1)*R*R/R**n
        check(correct == 1)
        if R != 1:
            reject('wrong radius exponent n-1 at n=%d R=%s' % (n,R), wrong == 1)

# Exact angular antiderivative identity for the normalized three-dimensional
# Poisson kernel: half its integral over t in [-1,1] equals this expression.
for q in [F(1, 100), F(1, 3), F(1, 2), F(9, 10), F(99, 100)]:
    integral = (1-q*q)/(2*q)*(1/(1-q)-1/(1+q))
    check(integral == 1)
    reject('omitted numerator in n=3 q=%s' % q, integral/(1-q*q) == 1)

# Constant-independent large-radius assertion fails when dimension varies.
q = F(1,10)
reject('universal dimension-free upper bound 2 at q=1/10',
       (1+q)/(1-q)**99 <= 2)

# Sign is necessary when bounding an integral by K times an unweighted mean.
# Entire harmonic f(x)=x_1 has mean zero about the origin but f(e_1/2)>0.
reject('Poisson upper mean inequality without nonnegativity', F(1,2) <= 0)

# One-sided harmonic Liouville derivative factor: differentiated center kernel
# has n/R, and a center value zero yields zero derivative bounds for any R.
for n in [2,3,7,100]:
    for R in [F(1,3),F(1),F(10),F(1000)]:
        check(n*F(0)/R == 0)
        check(n*F(2)/(2*R) == (n*F(2)/R)/2)

# Truncated radial example: finite at origin, correct surface-jump sign,
# harmonic exterior coefficient and finite supremum. This is an exact
# construction in the accompanying proof, not a finite-data inference.
for n in [3,4,7,100]:
    a=2-n
    check(a*(a+n-2)==0)
    check(n-2>0)
    for r in [F(0),F(1,4),F(1),F(2),F(100)]:
        b=F(-1) if r<=1 else -r**(2-n)
        check(-1<=b<0)
        if r>1:
            check(0<1+b<1)
    reject('negative distributional surface mass', -(n-2)>=0)

# For u=x_1, a polygon k e_1 -> 0 -> (k+1)e_1 has high escaping
# vertices but a returning midpoint for every k. Universal formula is exact.
for k in [1,2,10,1000000]:
    check(k>0 and k+1>k)
    midpoint=F(k)*(1-2*F(1,2))
    check(midpoint==0)
    reject('vertex escape implies entire-tail escape at k=%d'%k, midpoint>0)

# Finite-valued discontinuous subharmonic negative control in R^3.
# Let a_k=(0,2^-k,0), w_k=2^-3k, epsilon_k=w_k, and
# v=-sum_k w_k/max(|x-a_k|,epsilon_k). Each summand is a continuous
# subharmonic truncated negative Newtonian potential. The decreasing limit
# is finite everywhere: at 0 it is -sum 2^-2k=-1/3; for x!=0 the tail
# distances are bounded below, and there are finitely many initial finite
# summands. At a_k the kth term is -1, so v(a_k)<=-1. Thus {v>-1/2}
# contains 0 but contains no neighborhood of 0. This falsifies the extension
# of the open-component argument to general finite discontinuous functions.
origin_value=-F(1,4)/(1-F(1,4))
check(origin_value==-F(1,3)>-F(1,2))
for k in [1,2,10,100]:
    w=F(1,2)**(3*k)
    radius=w
    distance=F(1,2)**k
    check(w/distance==F(1,2)**(2*k))
    check(-w/radius==-1<=-F(1,2))
reject('all finite subharmonic strict superlevels are open', -1>-F(1,2))

print(json.dumps({'status':'PASS','exact_assertions':checks,
                  'rejected_false_claims':negative_controls,
                  'scope':'exact Poisson/scaling and falsifying constructions; universal proof is analytical'},
                 indent=2,sort_keys=True))
