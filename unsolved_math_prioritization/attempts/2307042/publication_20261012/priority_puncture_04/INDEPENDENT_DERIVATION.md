# Independent punctured-disc derivation

Checkpoint 2026-10-13 04:30 UTC. Prepared before reading package_review_03/PRIORITY_INFERENCE_PUNCTURED_DISC.md, any source_priority_01 disposition, or other review verdict. Source author proof/note and primary-source passages have been read. Completion estimate: 45% of this audit; mathematical mechanism proved, source priority comparison pending.

Let D*= {0<|z|<1}, a=1/2, P_e(z)=(1-|z|^2)/|z-e|^2 for |e|=1. Set K=P_{-1}/P_{-1}(a)=3P_{-1}; F_+=P_i/P_i(a), F_-=P_{-i}/P_{-i}(a), L=log(1/|z|)/log 2. These are strictly positive harmonic on D*, and all equal one at a. Thus F_+,F_-,L are eligible in the envelope H_a.

At a, gradients of these normalized functions equal their logarithmic gradients, and direct differentiation gives:

* grad K=(-8/3,0).
* grad F_+=(-32/15,8/5), grad F_-=(-32/15,-8/5).
* grad L=(-2/log 2,0).

The exact inequalities log 2<3/4 and log 2>0 give 2/log 2>8/3>32/15. The upper bound follows, for example, because exp(3/4)>1+3/4+(3/4)^2/2>2. Put t=2/log 2, s=8/3, r=32/15. Then grad K is the strictly interior point

(-s,0)=lambda(-t,0)+(1-lambda)/2*(-r,8/5)+(1-lambda)/2*(-r,-8/5),

lambda=(s-r)/(t-r) in (0,1).

Therefore the origin is strictly inside the triangle formed by grad(F_+-K), grad(F_--K), grad(L-K). Equivalently, the continuous function on the unit circle

m(d)=max{(s-t)d_x, (s-r)d_x+(8/5)d_y, (s-r)d_x-(8/5)d_y}

is everywhere positive. To verify strict positivity without a convexity slogan: if d_x<0 its first entry is positive; if d_x>=0, the maximum of the last two entries is (s-r)d_x+(8/5)|d_y|>0 for any nonzero d. Compactness supplies eta=min_{|d|=1}m(d)>0. Taylor expansion of this finite family then supplies C and rho_0 such that

max{F_+(a+d),F_-(a+d),L(a+d)}-K(a+d)>=eta|d|-C|d|^2>0

for 0<|d|<min(rho_0,eta/(2C)). Thus K<H_a on a punctured neighborhood of a. This independently proves the proposed local-isolation mechanism; no numerical evidence is needed.

## Green and Martin eligibility

D* is a bounded doubly connected Green domain, with one polar/irregular boundary component {0}. Its Green function is the disc Green function G(z,w)=log |(1-z*conj(w))/(z-w)|. One direct justification is exhaustion by epsilon<|z|<1: the difference from G is a nonnegative harmonic function bounded by M log(1/|z|)/log(1/epsilon) for any fixed pole away from zero (with M uniformly bounding G on the inner circle). It tends to zero on compact subsets as epsilon->0. This identifies the exhaustion Green function on D* with G.

For w->e on |e|=1, the Green quotient G(z,w)/G(a,w) tends locally uniformly to P_e(z)/P_e(a). These are minimal on D*: if 0<=v<=P_e, v is bounded near the puncture, so extends harmonically across zero; minimality on the disc gives v=cP_e. Disc minimality may be proved from Poisson measure uniqueness: the representing positive measure of v is dominated by the point mass representing P_e.

For w->0, the Green quotient tends to L. L is also minimal: a nonnegative harmonic v<=log(1/r) has no negative-power singular terms and has at most a logarithmic singularity at zero; subtracting its logarithmic coefficient times log(1/r) removes that singularity, leaving a harmonic function on the disc with continuous zero outer-boundary values, hence zero. This also follows from the positive-harmonic Bôcher decomposition explicitly used in Bear–Smith Proposition 2.6.

Thus the selected K is a legitimate normalized minimal Martin kernel, and its three competitors are legitimate positive harmonic functions, regardless of whether a broader historical question intended to exclude degenerate boundary components. The printed Problem 7.42 itself says only Green domain/multiply connected; no such exclusion occurs in its statement.

## Immediate scope consequence

Any nonconstant equality curve issuing from a contains non-base points arbitrarily near a and is excluded. Hence in the literal Green-domain scope and equality-along-the-line reading, the punctured disc is a negative example. This statement does not show that anyone historically recognized or published this consequence as a resolution of Problem 7.42, and it does not give the nondegenerate smooth annulus theorem for 1<|z|<e.
