# Attempt 5: an exact parametric tolerance transition

## Model and claim

Observe n iid Bernoulli(p) variables. Use the known reference Ber(0) and total variation distance F(p)=p. For 0<=nu<nu+delta<=1/2, consider

H0: p<=nu; H1: p>=nu+delta.

The minimum sample size that makes both errors at most 1/3 is of order

(nu+delta)/delta^2.

Equivalently, within the nonvacuous range, the critical gap has order sqrt(nu/n)+1/n. This is an elementary parametric example, not a new general transition theorem.

## Endpoint reduction

Binomial probabilities have a monotone likelihood ratio in the count. The likelihood-ratio test between p_0=nu and p_1=nu+delta is a count-threshold test (allowing randomization at the threshold). Its rejection probability is nondecreasing in p. Thus its worst null error and worst alternative error occur at these two endpoints. Every composite test must in particular distinguish the endpoints.

## Hellinger calculation

Let A=sqrt(p_0 p_1)+sqrt((1-p_0)(1-p_1)) be the single-observation affinity and h^2=1-A. Rationalizing square roots gives

2h^2 = delta^2/(sqrt(p_1)+sqrt(p_0))^2
       + delta^2/(sqrt(1-p_1)+sqrt(1-p_0))^2.

For p_1<=1/2,

delta^2/[8(nu+delta)] <= h^2 <= delta^2/(nu+delta).

Indeed, the first denominator is at most 4p_1 and at least p_1. The second term is at most delta^2/(1-p_1)<=2delta^2<=delta^2/p_1. These bounds also hold at p_0=0.

The n-fold affinity is A^n. The endpoint likelihood-ratio test has sum of errors 1-TV<=A^n<=exp(-nh^2). Hence n>=8 log(3)(nu+delta)/delta^2 makes both errors at most 1/3, and endpoint monotonicity makes it valid for the composite hypotheses.

Conversely, both errors at most 1/3 imply TV>=1/3. By Cauchy–Schwarz,

TV<=sqrt(1-A^{2n})<=sqrt(2nh^2).

Consequently n>=1/(18h^2)>=(nu+delta)/(18delta^2). This proves the sample-complexity claim with explicit universal constants.

To check the critical-gap equivalence, write a=sqrt(nu/n), b=1/n. For delta=C(a+b), n delta^2/(nu+delta)>=C^2/(1+C). If delta<=c(a+b), then n delta^2/(nu+delta)<=4c for 0<c<=1: when a>=b use denominator>=nu and when a<b use denominator>=delta. These bounds establish the claimed order, provided the chosen endpoints remain in [0,1/2].

## Interpretation and final obstruction

At zero tolerance the gap is of order 1/n. At fixed positive nu bounded away from 1/2, it is of order 1/sqrt(n), the ordinary Bernoulli estimation scale. Intermediate tolerances give an explicit interpolation. The transition reflects increasing noise near the least-favorable boundary, and has no high-dimensional moment-matching barrier.

This closes the Bernoulli subproblem. It does not extend automatically to nonsmooth Gaussian norms or arbitrary density references. Existing literature already treats major discrete and Gaussian cases; the source's unrestricted classification is not established by these five approaches. Final classification: partial progress / no full resolution, with existing results credited and a fresh audit required before any public update.
