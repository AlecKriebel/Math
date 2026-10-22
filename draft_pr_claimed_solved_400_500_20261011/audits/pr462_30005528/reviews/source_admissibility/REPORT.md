# Independent source-admissibility report

Reviewer: /root/pr462_source_admissibility
PR: 462
Problem: 30005528 / OWR-13750333-009
Frozen head: 3d5701d67e18745715d384c3db3fbee588b42a98
Completed: 2026-10-12T16:45:21.702196+00:00
Verification-goal completion estimate: 100%

## Verdict

The frozen construction is an admissible, exact, nonvacuous counterexample to the abstract compact linear-domino Question 1 on printed p.1254 of OWR 22/2023. All additional mathematical properties in the frozen proof are verified. I found no blocking issue, required repair, or unresolved mathematical gap for that narrowly stated claim. This report does not establish historical priority and makes no publication or problem-disposition decision.

## Independence and frozen input

SOURCE_INTERPRETATION.md was saved at 2026-10-12T16:40:39.248651+00:00 before I read the frozen proof, source gate, or any historical/peer report. I retrieved the original official EMS PDF and inspected complete printed pp.1253-1255 as rendered images, using the PDF skill. This fixed the formal target, average normalization, legal-period convention, stated assumptions, and possible hidden restrictions independently of the submitted argument.

I subsequently read only the frozen release/PROOF.md and release/SOURCE_GATE.md semantically. I checked hashes and byte counts for all 12 frozen files against the supplied SOURCE_RECEIPT.json without using their historical audit conclusions. Every value matches. I have not interpreted historical audits or peer reports. Zero original proof-search attempts were made. All authored artifacts are in this isolated reviewer folder; no Git, source, service, paper, publication, or disposition mutation was performed.

## Exact source target

The [official EMS report](https://ems.press/content/serial-article-files/47016), DOI [10.4171/OWR/2023/22](https://doi.org/10.4171/OWR/2023/22), puts the problem in the Problem session, chaired by Jens Marklof with notes by Paul Nelson. Definition 1 makes tiles ordered pairs of arbitrary symbols. Question 1 adds an infinite compact topological alphabet and continuous real-positive size, then asks for strict separation of every periodic legal sequence from the infimum over all legal sequences.

The average counts N+1 symbol occurrences for N tiles:

    A(w)=limsup_(N->infinity) [s(a_1)+sum_(i=1)^N s(b_i)]/N.

Neither the formal definition nor Question 1 states reversal symmetry, size injectivity, connectedness, tile-relation closedness, or a geometric realization. The subsequent Remark 4 motivates a separate packing question. The proof's compact connected metric cylinder, closed graph, and strictly positive size meet the original requirements and several stronger ones.

## Adversarial findings

| Falsification target | Result and checkable reason |
| --- | --- |
| Misread average normalization | No mismatch. The frozen proof retains the N+1 numerator terms and obtains ((N+1)/N)(1+t), so the limit is 1+t. |
| Missing legal sequences | None. T is exactly a deterministic graph and matching forces every sequence to follow one orbit at a fixed height. |
| Compactification creates cheaper periodic cycles | No. The cylinder already includes both boundary circles and the graph is closed. Its limit edges remain the same irrational rotation at height 0. |
| Disconnectedness exploited | No. S^1 x [0,1] is connected. |
| Size fails positivity or continuity | No. s=1+t is continuous and lies in [1,2]. Either conventional reading of R_+ is satisfied. |
| Circle seam or special phase | No. Complex multiplication is globally continuous, and |z|=1 permits cancellation at every phase. The excluded origin is never a symbol. |
| Periodic bottom or upper boundary | No. alpha and alpha+1 are irrational. Exact returns require q(alpha+t) to be an integer. |
| Eventual periodicity at minimum | No. The global inverse converts any eventual return into a return at the starting point. |
| Vacuous periodic exclusion | No. There is a period-one circle at t=2-sqrt(2), and dense periodic starting points with costs tending to 1. |
| Nonattained infimum | No. Every t=0 orbit attains 1; every minimizer must have t=0 and is aperiodic. |
| Compactness forces a periodic limit | No. Approximating rational-angle circles have unbounded least periods. The union of finite-period sets is not closed in this example. |
| Bounded-period gap has a sign/denominator flaw | No. p^2-2q^2 is a positive integer, r<=sqrt(2)+1, q<=Q, and the displayed positive lower bound follows exactly. |
| Planar reparametrization adds zero/singular points | No. The annulus has inner radius 1 and the explicit inverse u/|u| is continuous throughout it. |
| Hidden reversal requirement | Absent from the original definition. Adding reverse edges would change the legal relation and permit different cycles; this altered game is outside the claim. |

The detailed deductions are in CHECKS.md. The finite exact-arithmetic script independently confirms 4,096 explicit competitors and 1,260 reduced rational angles through denominator 64. Its computation supplements rather than replaces the universal deductions.

## Related source and excluded claim

I inspected the native primary [Goncalves-Vedana 2025 paper](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/8980920479977FE37DB355A8E601A5A8/S205050942500009Xa.pdf/sphere_packings_in_euclidean_space_with_forbidden_distances.pdf), DOI [10.1017/fms.2025.9](https://doi.org/10.1017/fms.2025.9), including full rendered pp.9-10 and Section 4 pp.15-19. Conjecture 4 concerns compact K subset [1,infinity) containing 1 and a periodic K-admissible packing of maximum density. Section 4 builds equal-length words of physical gaps and permits block pairs only when every contiguous subword's sum is an allowed distance or exceeds sup(K). Proposition 12 supplies the packing-to-block correspondence for these specifically constructed relations. Theorem 13 assumes a finite domino set and an appropriate word norm.

The cylinder graph supplies neither a set K with that partial-sum structure nor the required packing correspondence. The paper's discussion of an infinite-symbol generalization does not prove that every arbitrary ordered graph has a K-realization. Thus this review verifies the source gate's exclusion of the motivating packing problem and Conjecture 4. No conclusion about their truth follows here.

## Strongest verified result and exact remaining gap

For the displayed compact connected cylinder game, every legal sequence has average exactly 1+t. The minimum 1 is attained precisely by the bottom-circle irrational orbits; no minimizing sequence is periodic or eventually periodic. Periodic starting points are dense, periodic costs have infimum 1 with no attainment, the graph is closed, and for alpha=sqrt(2) every least-period-q<=Q competitor has cost gap at least 1/((2sqrt(2)+1)Q^2). The annulus coordinate version is equivalent. There is no remaining mathematical gap in these assertions or their admissibility to the literal original Question 1.

Historical novelty is unassessed by this review. The original publication's intended broader packing motivation could differ from its literal symbolic formulation, but no unprinted restriction is assumed here. A geometric counterexample would require a new, verified realization mechanism; no such result is asserted in the frozen proof or this report.

## Artifact boundary

SOURCE_METADATA_RECEIPT.json contains retrieval metadata, primary-source hashes, inspected page locators, and frozen-file integrity results only. Foreign PDFs, rendered source images, and full extracts remain under private_sources/ and are excluded from the public whitelist. PUBLIC_FILES.json positively lists authored safe artifacts using explicit paths, bytes, and SHA256 values; it performs no recursive directory inclusion. Its own hash is recorded separately in PUBLIC_FILES_SELF.json. No credentials, invalid fixtures, or environment dumps are included.
