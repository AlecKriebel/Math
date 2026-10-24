# Row 1898 recovery and literature gate

Checked 2026-10-21. ID 20000750; AIM-ANALYTIC_NUMBER_THEORY-0114. Queue title: Alternative GPY weights: exact perturbation geometry and a radial escape.

## Original target

AIM, Problems from the ARCC Workshop “Gaps Between Primes,” December 2005, notes by Angel Kumchev, Problem 15, printed page 4. https://aimath.org/WWN/primegaps/WorkshopProblems.pdf

The question concerns quantitative improvements from changing the single-divisor GPY coefficients. It specifically proposes multiplying a smooth cutoff by a product of smooth factors evaluated at log(p)/log(R), asks about other traditional sieve weights, and suggests upper/lower sieve mixtures with a warning about controlling negative contributions. The title is a later research-attempt title, not the original question. The divisor sum is not itself a nonnegative test weight; its square is.

## Prior result and scope gate

The supplied prior attempt is PARTIAL-PROGRESS, rigor claimed proved, novelty confidence low. It contains (1) an elementary exact generalized-Rayleigh two-plane improvement test, (2) a proof that no nonzero continuous radial profile is an eigenfunction of the full Maynard operator on the standard simplex for k >= 2, (3) the Rayleigh residual improvement and (4) an elementary signed-weight negativity budget. It does not evaluate arithmetic moments for the exact product-local family or supply a new prime-gap bound. The prior attempt is not independent validation.

The radial lemma appears structurally sound on inspection: for F(t)=G(S), LF=sum_i H(S-t_i), H(x)=integral_x^1 G. If LF is radial, continuity permits restriction to the boundary slice (x,s-x,0,...,0), giving H'(x)=H'(s-x); a small intermediate argument links all points and makes G constant. Nonzero constants are not eigenfunctions for k>=2. A full audit should explicitly justify passing an almost-everywhere radial identity to continuous representatives before restriction to the measure-zero boundary. The resulting residual is an improving variational direction, not automatically a new arithmetic theorem.

## Important missing prior art

Bálint Farkas, János Pintz, Szilárd Révész, *On the optimal weight function in the Goldston-Pintz-Yildirim method for finding small gaps between consecutive primes*, arXiv:1306.2133 (2013), https://arxiv.org/abs/1306.2133; author PDF https://www.renyi.hu/~revesz/ThreeCorr0grey.pdf.

This source is absent from the supplied attempt's reference list. It solves the one-variable weight optimization via a self-adjoint operator and Bessel eigenfunctions, and constructs approximately optimal polynomial weights. Its introduction credits related Conrey/AIM calculations to 2005. Any account of Bessel/radial optimization must cite it and distinguish the full multidimensional operator from the restricted one-dimensional operator. No novelty claim should be based on rediscovering that optimization. The full-operator no-radial-eigenfunction formulation was not found in this limited search; absence from search is not proof of novelty.

## Current primary literature checks

- Maynard, *Small gaps between primes*: https://arxiv.org/abs/1311.4600, latest arXiv v3 (2019); Annals 181 (2015). Establishes the multidimensional enlargement and an affirmative broad strengthening of GPY. It does not by itself classify the precise prime-local product family in Problem 15.
- D. H. J. Polymath, *Variants of the Selberg sieve, and bounded intervals containing many primes*: https://arxiv.org/abs/1407.4897, v4 (2014). Relevant prior art for generalized eigenvalue optimization and multidimensional sieve variants.
- Lewulis, *Variants of the Selberg sieve, and almost prime k-tuples*: https://arxiv.org/abs/2203.09432 (2022), weighted almost-prime improvements, not a complete answer for all original coefficient choices.
- Bin Chen, *Small gaps between almost-twin primes*: https://arxiv.org/abs/2402.00748, v2 July 2025, author reports accepted by Forum Mathematicum, DOI https://doi.org/10.1515/forum-2024-0036. Uses Maynard–Tao weights and a prime-indicator minorant with extra distribution information.
- Ford–Maynard, *On the theory of prime producing sieves*: https://arxiv.org/abs/2407.14368 (2024). A general Type I/II framework with upper/lower limits; latest public arXiv record checked has only v1. Not a blanket optimization theorem for the exact product-local GPY family.

Recommended classification remains partial / scoped historical resolution. Broad improvement by changing the architecture is known; one-variable optimization is known; the exact product-local and general mixture requests must not be declared completely solved by the recovered residual lemma.

## Duplicate and remote-state gate

All-state AlecKriebel/Math PR searches returned no hits for exact ID 20000750; GPY; and the combined query containing 20000750, ANALYTIC_NUMBER_THEORY-0114, radial escape, Maynard. Search is a checked negative result, not an exhaustive guarantee against indexing gaps.

No publication or queue modifications performed.

## Full-PDF cross-check

Downloaded and text-inspected the arXiv PDFs for Farkas–Pintz–Révész, Maynard and Polymath. Polymath printed page 46 explicitly gives the optimized radial value 4k(k-1)/j_(k-2,1)^2, cites Farkas–Pintz–Révész as reference 14, and notes this value is below 4. Maynard printed pages 17–18 identifies the radial functional with original GPY and defines the full operator in equation (7.2). Thus the literature omission is directly confirmed in a primary source already cited by the prior attempt, not merely a search result.

The AIM PDF was successfully opened and parsed through web retrieval, confirming printed page 4, Problem 15; direct filesystem download returned HTTP 403, so no local AIM PDF hash is claimed. The public source manifest records this accurately. No third-party source documents are included in this package.
