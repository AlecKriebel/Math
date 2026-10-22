# Final acceptance: corrected prior theorem, coefficient one unresolved

## What is accepted

The complete corrected proof establishes one absolute C>0 and infinitely
many positive integers n with omega(n-k)<=Omega(n-k)<=C log k for every
integer 2<=k<n. The multiplicity extension uses only the proved schedule
A=100, s=ceil(4 log k), 2<=k<=floor(x^.01); larger shifts use the deterministic
factor-count bound. The same nonnegative sieve weight is used for every k.

The endpoint transfer N=n-1, epsilon=1/(C log 2) establishes
m+epsilon*Omega(m)<=N, hence m+epsilon*omega(m)<=N, for every positive m<N
and infinitely many N. The constant is fixed before x tends to infinity.
Every endpoint, including m=N-1 and m=1, is included. No explicit numerical
epsilon and no assertion for all prescribed positive epsilon are supplied.

Credit belongs to Lau's prior stated backwards theorem, Theorem 1.3 of
*On the Number of Prime Factors of Consecutive Integers*,
[arXiv:2604.15042v2](https://arxiv.org/abs/2604.15042v2), 24 June 2026.
This edition is an authored correction and audit of that proof and consequence.
No novelty claim is made. The original formulation uses distinct factors and
a weak inequality: P. Erdős, *Some unconventional problems in number theory*,
Acta Mathematica Academiae Scientiarum Hungaricae 33 (1979), 71–80,
[printed p.71](https://users.renyi.hu/~p_erdos/1979-23.pdf).

## Complete mathematical evidence

KERNEL_REPAIR.md + DISTINCT_OMEGA_RECONSTRUCTION.md + MULTIPLICITY_REPAIR.md
contain the complete primary reconstructed chain. The complete independent
chain is SECOND_KERNEL_REPAIR.md + SECOND_DISTINCT_OMEGA_CHAIN.md +
SECOND_MULTIPLICITY_AUDIT.md, with SECOND_AUDIT.md explaining the kernel error.
These are analytical derivations, not summaries substituted for a proof.

The final independent acceptance includes: exact CRT/Fourier representation;
normalization without a many-coordinate absolute-value loss; fixed-schedule
small- and medium-prime moments; arbitrary-prime-power compatibility and
signed density cancellation; uniform normalized CRT errors; the complete
repeated-power tuple budget; maximum-exponent block enumeration and its
exponential generating function; tiny-prime signed-main scaling and
composition counts; the T<=w case; a common-distribution union bound;
smallest shifts; infinitely many witnesses; and the complete endpoint map.

Earlier independent distinct-only documents retain their narrower acceptance.
Their scope exclusions describe those documents alone. The separate full
multiplicity supplement supersedes that earlier acceptance boundary in the
final edition, without changing the earlier proof or endorsing unrelated
parts of the manuscript.

## What is rejected or unproved

The p.28 equality of a complex-kernel L1 norm with its real integral is false.
Its pointwise many-coordinate error argument is insufficient. The p.16
standalone prime-sum estimate uniform in a growing order is also false.
The printed inconsistent parameter choices and signed Möbius inequalities
are replaced, not accepted. No claim certifies all arbitrary-A/order lemmas.

The coefficient-one barrier remains unresolved by this work. The logarithmic
bound handles that coefficient only beyond one fixed terminal cutoff. The
finitely many remaining shifts, including shift 1 at an unshifted witness,
still require simultaneous control. Finitely many missing inequalities do
not disappear when the conclusion demands infinitely many full barriers.

## Meaning of acceptance

This is independent internal AI review of the specified written arguments.
The AI-assisted work is unrefereed. No external human peer review, journal
acceptance, formal proof-assistant certification, exhaustive literature
review, or new live tracker status is asserted. Historical exact algebra and
rational-margin checks supplement the analytic proof; they do not certify it.
Publication preparation verifies byte integrity and addition-only structure,
without new mathematical test execution or scholarly-source inspection.
