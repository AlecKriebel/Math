# Acceptance of the cofinite derivative zero theorem

## Decision and precise scope

Accepted for database 2376 / Erdős Problem 906: there exists a transcendental entire function f such that, for every nonempty open subset U of C, there is an integer N(U) for which f^(n) has a zero in U for every integer n >= N(U). More precisely, this holds with probability one for the planar Gaussian entire series F(z) = sum_{k>=0} xi_k z^k / sqrt(k!), with independent standard circular complex Gaussian coefficients.

The independent mathematical audit reports PASS, no mathematical residual, and no mandatory correction to the frozen candidate. PROOF.md is the complete standalone proof; AUDIT.md preserves all eight adversarial mathematical checks. Acceptance here records the result of this proof review. It does not describe journal acceptance or a maintained problem tracker's decision.

The cofinite conclusion is deterministically equivalent to requiring that the union of derivative-zero sets be dense along every infinite strictly increasing sequence of derivative orders. This universal subsequence conclusion is not obtained by an uncountable probabilistic intersection. The literal nonzero-entire statement also allows nonzero polynomials, whose sufficiently high derivatives vanish identically; the accepted theorem establishes the stronger transcendental statement.

## Complete argument retained

The proof constructs one probability-one event of entire, transcendental samples; establishes the differentiated Gaussian marginals and the exact covariance K_n(z) = n! exp(|z|^2) L_n(-|z|^2); and proves the uniform annular value estimate log L_n(-r^2) = 2r sqrt(n) + O(log n) by explicit upper and lower bounds. The factorial bound is derived by integration. No derivative of the error term is taken.

For a nonnegative nonzero smooth test function phi supported in a disk away from zero, put A = integral phi/|z| dA and L = integral |Delta phi| dA. Both are positive. Distributional zero counting, local integrability of the singular logarithm, joint measurability, and weighted Tonelli/Fubini give the mean zero statistic mu_n = A sqrt(n)/(2pi) + O_phi(log n). The proof then obtains the uniform exponential moment at most 3sqrt(pi)/2 and the tail bound P(|X_n-mu_n| >= lambda) <= 3 exp(-2pi lambda/L). Spatial independence and independence between derivative orders are not assumed.

The resulting hole probability is eventually at most 3 exp(-A sqrt(n)/(2L)), which is summable. Measurability of hole events is established through compact minima and countable dense subsets. First Borel–Cantelli and a countable pi-base of rational disks avoiding zero give eventual hitting of every nonempty open set, including sets containing zero. The common-null-set modification, singular-log justification, unbounded Jensen argument, and deterministic subsequence equivalence remain in the standalone proof.

## Attribution and source distinctions

This is a credited reconstruction of the Gaussian route proposed by Adriano Almeida and Przemek Chojecki in April 2026. Almeida's earlier posting is acknowledged. The covariance, expected-zero, hole-probability, and Borel–Cantelli mechanism are prior work; no novelty or priority is claimed. The proof supplies elementary derivations of the two analytic estimates rather than assuming a Laguerre asymptotic theorem or an Offord theorem.

Erdős's 1982 original statement, printed p.72, reports a historical affirmative resolution; note (1), printed p.79, lists four Barth–Schneider papers. That historical assertion and those older papers are not independently adjudicated by this acceptance. The theorem proved here does not depend on them. [Original source](https://users.renyi.hu/~p_erdos/1982-33.pdf)

The inspected Almeida source is the five-page April 2026 AI-assisted proposed manuscript. Hou's frozen GitHub source is a 12-page manuscript, distinct from the later 10-page arXiv version 2607.20816v5 revised 25 August 2026. The original audit inspected the later version's abstract, introduction, theorem, and attribution, with visual inspection of its first two pages; it did not audit either Hou proof in full. Public URLs, hashes, byte counts, retrieval dates, inspection scope, and stated manuscript status are recorded in SOURCE_PINS.json. [Almeida manuscript](https://github.com/Drill23/erdos-problem-906-proposed-solution/blob/d9aefa869577e6c0135dd994046a6b59b063733f/paper/erdos_906_proposed_solution.pdf), [Hou frozen version](https://github.com/erichou1/cofinite-derivative-zeros/blob/27e2206b984c3a0a284eb411a92eb18d5f097e6a/paper.pdf), [Hou arXiv v5](https://arxiv.org/abs/2607.20816v5)

The direct forum retrieval returned HTTP 403. Cached primary-site search results supported the historical attribution, but the site's current maintained open/solved status was not verified. [Historical discussion](https://www.erdosproblems.com/forum/thread/906)

## Verification and exclusions

The eight-artifact audit seal, frozen candidate, frozen source pins, independently retrieved source copies, and later arXiv PDF pin were rechecked. Normal Python and both optimization modes gave identical bounded-diagnostic results: 1,891 exact covariance comparisons, 70 numerical upper-bound comparisons, 40 numerical lower-bound comparisons, eight input-pin checks, and five negative controls. These finite arithmetic and integrity checks do not prove the infinite theorem and do not replace the mathematical argument.

No bounded-coefficient theorem, deterministic selected sample, finite-type growth claim, complete Hou audit, Lean certification, Boas–Reddy audit, journal acceptance, prize decision, or current tracker-status claim is accepted. No source-author code was executed. This packet contains authored mathematical text, public citations and source metadata, and aggregate verification metadata only. Copied third-party documents, source extracts, images, raw datasets, scripts, and private coordination material are excluded.
