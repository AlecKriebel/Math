# Two nonblocking clarifications from the independent audit

These additive clarifications accompany the unchanged frozen author packet. They do not change the local theorem, strengthen the target disposition, or constitute a further proof attempt. The full mathematical review is [included](independent_review_v1/FULL_ADVERSARIAL_AUDIT.md).

## 1. Measurable weights: essential uniformity and almost-everywhere data

The contributing calculation's general weighted-Funk lemma permits the weight E(x,u) to be merely measurable in x, with a uniform C⁴ bound in the normal variable u outside an x-null set. In that generality, read its uniform-convergence and integral-identification statements as follows:

- The harmonic expansion in the normal variable converges uniformly in u and essentially uniformly in x: there is one fixed x-null set outside which the common summable bounds hold.
- By incidence Fubini, that exceptional x-set meets the incidence circle in an arclength-null set for almost every normal u. The harmonic-series operator therefore agrees with the original circle integral for almost every normal, with the usual almost-everywhere interpretation of L² and H½ functions.
- The actual geometric weights in Attempt 1 are jointly continuous in x and u. For those weights the expansion is genuinely uniform on the product sphere, and the original circle-integral equality for continuous input is valid for every normal. No exceptional-set change to the principal C² local theorem is needed.

No assertion is made that an arbitrary representative of a measurable weight has correctly defined or matching data on every individual circle.

## 2. Midpoint data: nonincrease everywhere, strict decrease somewhere and in mean

For unequal positive radial functions ρ₀,ρ₁ with equal endpoint perimeter data, set ρ_m=(ρ₀+ρ₁)/2. Attempt 2 proves

P(ρ_m)(θ) ≤ P(ρ₀)(θ)=P(ρ₁)(θ) for every θ.

The inequality is strict for some normals and strictly decreases the integral over all normals. It need not be strict for every normal: equality occurs whenever the two radial restrictions on that circle agree. The positive mean defect follows from the proved Dirichlet-energy lower bound; the log-ratio cannot be constant unless the equal-data endpoints are identical.

Thus the phrase “smaller perimeter data” in the frozen attempt means no larger for every normal, strictly smaller for some normals, and strictly smaller in mean. Equal endpoint data still do not impose midpoint data equality, so this observation does not prove global uniqueness.
