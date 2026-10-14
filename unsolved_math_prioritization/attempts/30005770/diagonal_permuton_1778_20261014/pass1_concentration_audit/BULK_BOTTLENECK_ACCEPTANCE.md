# Acceptance of the descendant-weighted bottleneck appendix

Date: 14 October 2026. This is a continuation of the existing concentration review, with no change to the main audit or its verdict.

## Pinned artifact and verdict

BULK_BOTTLENECK.md, final SHA-256 a877146631fe0f5552de95a9dd599d468cc77076a594caa1e8b09ebbb24b96f8, is accepted as an exact inversion identity, valid completion bounds and an explicitly unproved sufficient condition. It proves no new concentration theorem and does not close the universal weak-limit target.

The initial appendix inherited the nontrivial-case assumption from its main proof without stating it. The final version expressly assumes |alpha|>=2. This is important: the Catalan lower bound for descendants does not apply to alpha=1, whose generating tree is a chain. The final version also identifies its already-controlled levels precisely as j=n-o(n).

## Mathematical checks

1. Inserting a new minimum at gap k creates exactly k inversions, one with each old entry to its left. The old inversions are unchanged. Every final permutation has a unique successive minimum-insertion path. Thus summing k over that path gives inv(pi).

2. A fixed edge from sigma in C_j to child_k(sigma) has exactly D_(n-j-1)(child_k(sigma)) completions at level n. Summing its weight k over these completions and then over all edges proves the displayed expectation identity with denominator a_n. The ancestor marginal is exactly D_(n-j)(sigma)/a_n, because deleting the n-j smallest values uniquely recovers that ancestor. No uniformity or independence of the ancestor is assumed.

3. The proposed averaged weighted tail condition is sufficient. On a level where L<epsilon n the insertion contribution is at most epsilon n; on its complement it is at most n. Summing the conditional expectations over n levels and dividing by n^2 bounds expected inversion density by epsilon plus the stated average. Taking limsup in n and then epsilon down to zero is valid. The appendix does not claim to have proved that weighted tail condition.

4. The lower bound B(L,t)<=D_t is exactly the accepted Catalan comparison theorem for |alpha|>=2. For the upper bound, the inserted t smallest values occupy positions at most L+t-1 by the previously proved child-label upper bound. Choosing their positions and their standardized t-point pattern gives at most binom(L+t-1,t)a_t possibilities. Since L<=j+1, the coarser binom(j+t,t)a_t bound follows. For levels j=n-o(n), the completion factor has subexponential binomial cost after using a_(n-j)a_j<=a_n; for a linear remaining depth it can have an exponential cost. These inequalities alone do not control the proposed average over all macroscopic levels.

5. Sorting adjacent descents uses exactly inv(pi) swaps; each changes the footrule by at most two. Hence sum_i|pi(i)-i|<=2 inv(pi). In square i, |x-y|<=|i-pi(i)|/n+1/n, and that square has mass 1/n. The coupling to (X,X) therefore gives d_BL<=2 inv(pi)/n^2+1/n. This is a correct, slightly looser alternative to the independently accepted exact two-point-density correction in the main audit.

## Verification scope

The three existing normal, -O and -OO checker reports were read, their recorded proof and checker hashes were matched to the current files, and all mathematical records were compared after removing only the optimization-level field. All three agree and report PASS:

- 33 alpha classes of lengths 1 through 4
- Avoidance classes through size 7 and insertion parents through size 6
- 24,621 parents and 151,916 valid edges
- 607,244 low-value deletions, with deletion depth at most 4
- 30,610 individual descendant checks and 9,084 finite tail bounds

The checker uses explicit runtime failures rather than optimization-disabled assertions. These are bounded verification outputs from the author's completed executions, not a new execution by this reviewer, not tests of the unproved weighted-tail limit, and not an all-n proof. The symbolic arguments establish the accepted identities and bounds.

The main audit remains unchanged: AUDIT.md, SHA-256 0b1aaed351f9df13aa0f2e9f2ba41df131cef3cfeb82fe111bf189a3e57c7e0d.
