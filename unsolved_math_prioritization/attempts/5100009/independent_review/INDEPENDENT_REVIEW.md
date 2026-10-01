# Independent source-scope review: 5100009 / k118

**Verdict: PASS_ALREADY_SOLVED_SOURCE_MATCH.** The frozen packet correctly identifies an exact published resolution. Recommend `already_solved`, with **0/5 substantive author turns**. This is credited source correction, not a new discovery or an original proof campaign.

Reviewed on 2026-10-01. The reviewer did not contribute to the author's source-transfer packet. No mandatory revision to the frozen author files is required.

## Exact bytes reviewed

- `STATUS_CORRECTION.md`: `faec0bc6959f1fa190a1c6a2c73f584d03fa429e833b086d3f488de7376a918f`
- `MANIFEST.json`: `b7beb5f2342ffe9e396410d953a1d1c0bad6076c16335fcabd19ea720199f3d8`
- All eight files listed by that manifest match their recorded SHA-256 hashes.
- All three complete source PDFs match the author's recorded sizes and hashes. The Stachel publisher PDF has SHA-256 `21708aaf65e1a54ee350b9798ca3aae3927d4e9ad12e085db65c8c06f56aeb58`.

## Exact source and scope

The pinned record's target is the pair of positive segment-length sums, each equal to half the perimeter for odd-period elliptic billiards. Both [arXiv v11](https://arxiv.org/pdf/2004.12497v11), Table 2, p. 5, and the [published invariant list](https://armj.math.stonybrook.edu/pdf-Springer-final/021-0174.pdf), Table 2, p. 345, retain precisely this k118 row and credit Hellmuth Stachel. The definitions in Section 3.1 also agree. Neighboring numbering changes do not alter k118.

The complete [published Stachel article](https://doi.org/10.1007/s00022-021-00606-2), *The geometry of billiards in ellipses and their Poncelet grids*, Journal of Geometry 112, article 40 (2021), was accessed and read. It was published online on 18 October 2021. Theorem 4.5, p. 24, explicitly identifies k118 and states the two half-perimeter sums. Lemma 4.4 supplies family-invariance of the perimeter. These are full published results, not an inference from an abstract.

The reviewer checked the full theorem/proof, equation (3.1), Lemma 3.11 and its proof, Corollary 4.2 and its proof, and the relevant source tables. The theorem/table pages were also visually inspected, including a fresh rendering of the published Corollary 4.2 page.

## Indexing, positivity, and generality

Use the author's temporary name rho for Stachel's right-adjacent length. On the chord from P_i to P_(i+1), the invariant-list right length is rho_(i+1), not rho_i. Therefore its cyclic sum is exactly the same sum. For N=2n+1, Stachel's congruence ell_(i+n)=rho_i supplies equality of the two totals. Since the contact point lies on the traversed chord, these two positive lengths partition that chord, so their combined total is L. This gives each total L/2 with no sign convention or area interpretation.

Corollary 4.2 includes both turning-number parities for odd N: the conjugate orbit is either centrally symmetric to the original or coincides after a cyclic shift. Both preserve the required ordinary distances. Thus the proof includes primitive odd stars, not merely convex orbits. Reversing traversal only exchanges the two kinds of lengths and does not change the conclusion. An odd-length repeated traversal has odd least period and scales all three sums by the same repetition count.

The packet's strict nested confocal-ellipse scope agrees with the source. No degenerate, focal, nonclosed, or even-period extension is being claimed. The source also explains that hyperbolic-caustic periodic billiards have even period. The conjugate billiard denoted P' in Stachel is not the outer tangent polygon denoted P' in the invariant list. The frozen packet correctly keeps those objects distinct.

## Nonblocking printed sign inconsistency

There is a local typographical inconsistency in the proof of published Lemma 4.4. Its displayed definition subtracts the caustic arc from the two adjacent lengths, so summing that definition yields L_e = N D_e + tau P_c for a positively traversed caustic. Equation (4.2) instead prints a minus. This does not affect perimeter invariance: D_e, tau, and P_c are fixed. The packet does not reproduce or depend on that sign, and Theorem 4.5's half-perimeter conclusion does not depend on it. Record the distinction without promoting it into a claim that the theorem fails.

## Independent controls and provenance

`independent_check.py` supplies 5,400 exact cyclic-index/repetition assertions and 7,770 numerical diagnostics at 80 decimal digits. The numerical check uses Euclidean ray/ellipse intersection and reflection after initialization, rather than generating all vertices from the author's formula. It covers 42 primitive families for N=3,5,7,9,11, both turning parities, three eccentricities, and three phases. Positive contacts, tangency, chord partition, closure, both sums, individual odd-index congruences, and perimeter invariance pass. The largest scaled residual is approximately 2.87e-79. These are finite diagnostics, not interval certificates or a proof.

The inspected author program was also replayed. Its output is byte-identical to its frozen receipt: 5,096 exact and 6,822 numerical assertions. These counts are separate from the reviewer's checks.

A fresh connected-repository search for 5100009, k118, and AMR-050-0009 found no matching prior PR. The current branch is the author's disclosed WIP checkpoint, not evidence of a prior independent attempt. The earlier imported report is third-party status triage. The neighboring k117 product result is a distinct target and is not used as a substitute for the sums.

The original PDFs, extracted full texts, and page images are access evidence only and are excluded from the portable review package. Publication should retain Stachel's authorship, the exact source attribution, the zero-turn source-only disposition, and the unchanged frozen packet.
