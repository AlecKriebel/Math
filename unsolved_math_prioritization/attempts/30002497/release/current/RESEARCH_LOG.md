# Research log

Date: 2026-10-04 UTC. Exact target: a positive irrational strict local maximum
of the unnormalized fractional-part autocorrelation A. Percentages below
are subjective estimates toward full target resolution, not probabilities
or claims that the remaining work has known size.

## Source gate · 13:09 UTC · 10%

Verified OWR 06/2014, Question 2, printed p. 350, against the pinned target.
Read the 2003 companion's integral identities/rational expansion and
Balazard–Martin's differentiability theorem and parity-specific secants.
The catalogue page was inaccessible; the primary source was available.
Live queue entry was queued 0/5. No matching prior PR/branch/attempt README
was found. ID30002496 is a composite duplicate containing this target.

## Approach 1 · Direct finite-integral geometry · checkpoint 13:16 UTC · 15%

Derived the uniform positive tail bound 1/T, the finite-cutoff derivative
C_T−sum {m/x}/m, and positive second derivative floor(xT)/x² between
rational breakpoints. Thus every finite cutoff has only rational strict
local maxima. Tested the tempting passage to the uniform limit and rejected
it: rational moving cusps can converge uniformly to an irrational cusp.
The residual tail is not controlled relative to infinitesimal increments.
Status: blocked as a route to the full target; exact integration formulas
retained as computational controls.

## Approach 2 · Hilbert-space positivity and reciprocal symmetry · checkpoint 13:16 UTC · 15%

Derived A(x)=xA(1/x), the strict normalized Cauchy–Schwarz bound, and
xA′(x)+A′(1/x)=A(x). Checked the equality case directly on a small t interval.
The normalized maximum at 1 does not determine unnormalized local maxima.
A stationary point and its reciprocal cannot both be stationary.
Status: useful normalization guard; no full resolution.

## Approach 3 · Continued-fraction parity squeeze · checkpoint 13:16 UTC · 25%

Used the actual side information in Balazard–Martin equation (37), rather
than differentiability almost everywhere. A local maximum of r−cΥ with
c>0 forces odd Wilton partial sums above a common limiting threshold and
even partial sums below it. Positivity of individual gamma terms then
squeezes both subsequences to that threshold. This proves that any
irrational local maximum of A must be differentiable and stationary.
Reciprocal reparameterization handles x>1 without incorrectly preserving
maxima of A itself under reciprocal scaling.
Status: partial theorem written in PROOF.md; fresh audit requested after
freezing. No novelty or complete-target claim.

## Approach 4 · Stationary increments and rational cusps · checkpoint 13:17 UTC · 20%

Derived the exact increment formula (11) at a stationary Wilton point.
The explicit logarithmic term is negative quadratic, but the known
Lebesgue-point estimate leaves an o(|h|) remainder, too large to determine
the sign. Compared the fixed-rational cusp expansion with continued-
fraction approximation; denominator-dependent linear terms and shrinking
validity neighborhoods defeat the argument that a nearby rational peak
must exceed the candidate. Merely restating the desired remainder inequality
is not treated as a solution.
Status: exact residual gap identified; route blocked without new bounds.

## Approach 5 · Periodic-orbit identities and validated numerical exclusion · checkpoint 13:17 UTC · 20%

At quadratics with 1/x−x integral, periodicity of the Bernoulli series and
its reciprocity relation give A′(x)=(A(x)−log x)/(1+x). This analytically
excludes every root of x²+mx=1 in (0,1). An analytic Bernoulli-series bound
excludes reciprocal roots at least 11. Interval integration with cutoff
2048 and 40 decimal digits checks the finitely many smaller reciprocals:
positive derivatives for m=1,…,9 and negative for m=10; m=11 is an overlap
control. Exact A(1), integral reciprocity, and finite-cutoff convexity are
also tested. These finite controls do not test all irrationals.
Status: infinite explicit excluded family, conditional finite numerical
certificates reproducible with mpmath; whole target remains unsolved.

## Budget conclusion

Five substantive distinct approaches have been used. No sixth search route
is proposed as verification. The remaining task is independent audit of the
partial results and the accuracy of the unsolved disposition, not further
proof exploration. Best estimate toward full resolution: 20%; prepared
research packet: complete pending audit. No remote writes, merges, releases,
DOIs, or external communications were performed by this worker.

## Verification checkpoint · 13:21 UTC · 20%

Repeated all controls with cutoff 4096 and 60 decimal digits. All eleven
derivative intervals lie inside the first-run intervals and have identical
signs. Inspected rendered OWR p. 350 and Balazard–Martin p. 19 to verify the
exact target and the parity direction in equation (37). No new search route
was undertaken.

## Audit correction checkpoint · 13:39 UTC · 20%

The independent audit accepted the partial mathematics and all derivative
signs, while finding that mpmath str(iv.mpf) displays nearest-rounded
endpoints. The original saved strings must therefore remain historical
displays, not directed endpoint certificates. The original author files and
full audit were preserved unchanged. A separate corrected verifier now
exports exact binary-rational endpoints with decimal lower floor and upper
ceiling, using the supplied audited serializer. Its event integration and
analytic proof are unchanged. Both parameter sets are regenerated and the
release checks replay the original scripts, verify corrected nesting and
signs, and rerun the independent integer backend. This is correction and
verification only; the substantive approach count remains five and the
full target remains unsolved.
