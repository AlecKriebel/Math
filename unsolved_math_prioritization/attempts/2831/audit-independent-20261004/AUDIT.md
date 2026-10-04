# Independent audit of degree one Heegaard genus monotonicity

Problem 2831, K3 Problem 3.33, queue rank 594. Audited 2026-10-04 UTC.

## Verdict

**PASS as an unsolved partial-results package.** No mathematical error requiring a correction was found in the propositions or the stated barriers. This is not a proof or refutation of the universal conjecture, and the audit does not turn it into a solution candidate. Retain `ownStatus: unsolved`, `Turns: 5`, and `complete_candidate: false`. The five documented routes are substantively distinct; their reconstructed ledger is not independently authenticated as a historical transcript of five timed work sessions.

The complete frozen seven-file release, plus its hash manifest, was read. Its manifest SHA-256 is `ba0d7d679c1b07f93703e7f247b6761091b5435868a3a8515a7c3038666de8fb`. All seven entry hashes pass. The original controls reproduce their saved output byte for byte. Independent arithmetic checks also pass. The freeze was not modified. No remote writes, publication, commits, or pushes were made.

This audit checked the mathematical arguments in full, the relevant primary-source statements and restrictions, selected source provenance, and reproducibility. It did not reprove Li's or Gadgil's published theorems, certify the absence of all later literature, or renew the historical repository duplicate gate.

## Exact target and source identity

The target is genus monotonicity for every degree-one map between connected closed oriented 3-manifolds. It does not assume irreducibility, asphericity, torus decomposition, or a favorable Heegaard splitting. Choosing orientations reconciles this with the source's orientable formulation. Connectedness is an explicit conventional clarification.

The locally preserved author PDF was checked at physical PDF page 155 and its displayed printed page 155; the statement and remarks were also visually inspected. It gives precisely the general problem and discusses Li's torus-pinching theorem as a special case. The linked AIM item was independently opened and is a four-page workshop report. It is not the cited problem book, so the release's source correction is justified. Historical Kirby-list problem numbering must remain separate from K3 numbering. Sources: [K3 author version](https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf), [AIM workshop report](https://aimath.org/pastworkshops/kirbylistrep.pdf).

The frozen selected corpus record matches ID 2831, code KP-3.33, and the stated mathematical target. The corpus hashes and repository facts in SOURCE_STATUS.md are historical provenance supplied with the attempt; this audit did not independently redownload the complete upstream corpora or re-query the live repository. Their absence-of-duplicate claim was already explicitly bounded, and must stay bounded.

## Fundamental groups and free group sources

Proposition 1.1 is sound. A lift to the image-subgroup cover always exists. If that cover is infinite-sheeted, it is noncompact and has zero ordinary top homology. Compact support homology is not being substituted, so factoring the fundamental-class map through zero is legitimate. If the cover has finite index d, its pulled-back orientation gives degree d for the covering; `1 = d deg(f_tilde)` forces d=1. The Heegaard handle decomposition supplies at most g(M) group generators, giving `g(M) >= r(M) >= r(N)`.

The rank-sharp-target corollary follows. The source-genus-zero case uses the Poincare theorem exactly where claimed. It does not circularly claim to prove Poincare.

Proposition 1.2 is also sound. A classifying map from the connected sum of r copies of S1 x S2 to a rank-r rose induces the selected identification of its free fundamental group. Any homomorphism from that free group is realized by choosing loops on the rose. Since the target is a K(pi,1), equality of based induced homomorphisms yields a based homotopy between the original map and the rose-factorized map. The rose has no degree-three homology, so the map's degree vanishes. The case r=0 is included. This argument does not wrongly claim that the source itself is a K(F_r,1).

The source's genus equals r by a standard connected-sum upper bound and its first Betti number lower bound. Thus the existence of a group epimorphism is correctly separated from the existence of a degree-one realization. Li's Theorem 1.1 really supplies closed hyperbolic rank-genus gaps, with unbounded discrepancy; those examples alone do not produce counterexamples to degree-one monotonicity. Source statement checked: [Li 2013 preprint v2](https://arxiv.org/abs/1106.6302v2).

## Integral transfer and homology cases

The transfer in Proposition 2.1 has the correct domains and direction: integral Poincare duality sends cohomology degree 3-i to homology degree i. Naturality of cap product gives `f_* t_i = id` on every integral homology group, including torsion. An abelian-group section makes the target homology a direct summand of the source homology. No field-only argument has been improperly promoted to an integral splitting.

Repeating the same duality argument over any field gives the Betti-number inequality. The presentation on g(M) generators bounds first homology dimension over every characteristic. The same-prime lens-sum calculation is valid because tensoring Z/p_j with a field of characteristic p gives one dimension exactly when p divides p_j. The standard genus-one splittings supply the matching upper bound, so no connected-sum additivity theorem is needed for that equality.

For L(2,1)#L(3,1), integral first homology is cyclic of order six and first Betti number over a field is at most one. The fundamental group is the free product C2*C3 and is nonabelian, yet two-generated; its rank is therefore exactly two. This and the standard splitting prove genus two. The example defeats field homology alone, not the stronger rank argument, exactly as stated.

## Finite covers and the rank ceiling

All three propositions in Section 3 are valid, including nonnormal covers.

1. For any finite-index subgroup K of the target group, the epimorphism f_* gives a bijection of the relevant coset sets, so the preimage subgroup has the same index d. The compatible source cover is connected, and the lifted map has degree one by comparing the two compositions of degree d.
2. In a Heegaard splitting, each handlebody and the splitting surface surject onto the ambient fundamental group. This ensures connected inverse images in a connected cover; it is not an implicit connectedness assumption. A cover of a handlebody is a handlebody. Multiplicativity of Euler characteristic gives genus `1+d(k-1)`. The genus-zero exception only permits d=1.
3. Combining the resulting **upper** bound for source-cover genus with the target-cover homology lower bound gives `b1(N';F) <= d(g(M)-1)+1`, hence `g(M) >= 1+(b1(N';F)-1)/d`. There is no reversal of the cover inequality.
4. Pull back K through an epimorphism F_r onto pi1(N). Schreier gives rank `1+d(r-1)` for that free subgroup, which surjects onto K. Thus both b1(N';F) and r(N') are at most that number. Every normalized bound, and its integer ceiling, is at most r(N). Taking a supremum over all covers or fields cannot change this conclusion.

The trivial-group edge case is correctly isolated. The bound is sharp as a method ceiling: for a degree-d cover of the connected sum of r copies of S1 x S2, the free group's first Betti number is `1+d(r-1)`, attaining normalized bound r. This sharpness example says nothing about the rank-gap cases. Virtual positive Betti number or virtual fibering cannot, by itself, eliminate the normalization.

## Pinching and the conditional amalgamation proof

Proposition 4.1 is correct with its stated minimal-amalgamation assumption. A relative splitting of a compact manifold with sole boundary T has the T-adjacent compression body built from T x I by one-handles. This gives a >= h. On the V side, filling its negative boundary by a genus-h handlebody turns that compression body into a handlebody with genus b, regardless of the attaching homeomorphism. The other side is already a handlebody. Hence N has a genus-b splitting.

The standard amalgamation construction has genus a+b-h. Equivalently its Euler characteristic is `chi(S_W)+chi(S_V)-chi(T)`. Because the chosen amalgamation is assumed minimal for M, `g(M)=a+b-h >= b >= g(N)`. One does not need to assume that the two individual relative splittings were minimal. For h=0, the same assertion can instead be viewed using punctured closed manifolds and connected sum if one's compression-body convention excludes spherical negative boundary.

This is a genuine conditional theorem. Arbitrary decompositions do not supply a minimal amalgamation. The source's informal generator-counting explanation of amalgamation should be read as a standard handle-construction formula, not as a statement that pi1(T) has h generators. CORRECTIONS.md offers an optional wording clarification; no change is needed for validity.

The Haken-Waldhausen reduction and the general cut-system replacement conjecture are explicitly formulated as equivalent in Li's Introduction. Theorem 1.3 assumes replacement of a knot exterior in a homology sphere by a solid torus with the Seifert-boundary slope becoming meridional. Remark 2.2 treats the minimal-amalgamation subcase; the theorem extends beyond that subcase. Neither licenses arbitrary higher-genus pinching. These restricted claims match [Li 2022 preprint v2](https://arxiv.org/abs/2007.14534v2) and the [published abstract](https://doi.org/10.1112/topo.12253).

Boileau-Wang Theorem 1 requires both closed manifolds to be small and the named target submanifold to be irreducible, with a homeomorphism outside it. Its alternative is a component carrying the target group with a genus bound, or homeomorphism of the two manifolds. It is not a general source-target genus monotonicity theorem. The package respects this restriction. Source: [Boileau-Wang 2005](https://msp.org/agt/2005/5-4/agt-v5-n4-p07-s.pdf).

## Surgery and the invalid induction

Gadgil Theorem 1.1 has exactly the direction used: existence of a degree-one map M to N is equivalent to obtaining M from N by surgery on a link whose components individually are unknots in N. It does not assert a split unlink or survival of the unknot condition through sequential surgeries. Source statement checked: [Gadgil preprint v1](https://arxiv.org/abs/0809.3102v1). The 2007 journal date and 2008 arXiv posting refer to different events and are not contradictory.

Proposition 5.1 is valid even for a locally contained link with knotted components. Surgery inside a ball replaces that ball with the punctured surgery manifold Q. The resulting closed manifold is N#Q, and the independently known connected-sum additivity theorem gives the claimed inequality. The proof explicitly records that nontrivial theorem as a dependency.

The Hopf-link obstruction is correct. Its exterior has first homology freely generated by the two meridians, and its preferred longitudes have the other meridian's homology class. Filling K1 with zero slope kills mu2. Restoring the original neighborhood of K2 is meridian filling and adds that same relation mu2=0, so the intermediate closed manifold retains Z generated by mu1. A longitude of the restored K2 represents its core class; this is mu1, nonzero in homology. Hence K2 is not even null-homotopic after the first surgery, and cannot be a local unknot. There is no confusion between the boundary longitude and a meridian of the reinserted solid torus.

The determinant -1 of the full two-component surgery matrix only shows that final first homology vanishes. It does not identify the final manifold or certify a genus, and the package makes no such inference. The example invalidates the proposed induction hypothesis; it is not a counterexample to the original conjecture. Controlling the full individually unknotted link would be the full conjecture again through Gadgil's characterization.

## Computation and adversarial checks

The frozen script was inspected before execution. It uses only standard-library exact arithmetic and local output, and does not read private sources or access a network. Its 100 same-prime lens examples and 560 sampled normalized-cover examples were reproduced. The complete stdout matches CONTROL_RESULTS.json byte for byte.

A separate script, independent_checks.py, checks the seven-file freeze before and after replay. It additionally checks 320 lens-presentation cases, 89,550 normalized-cover arithmetic cases, and 729 amalgamation arithmetic cases. A concrete noncommuting permutation quotient witnesses the free product's nonabelianity; a trivial-group edge case and the Hopf quotient are checked separately. All pass. These counts describe arithmetic identities, not manifolds searched or topology certified. In particular, none of these tests proves a published theorem, detects every proof gap, or establishes the universal conjecture.

## Fresh literature check and limits

A bounded fresh search on 2026-10-04 used degree-one/degree-1, Heegaard genus, conjecture, proof, counterexample, and recent-year queries. It found no verified complete resolution. The 2026 K3 statement is direct support for the release's cautious unresolved classification.

A potentially confusing recent hit is Binns-Ghosh's 2025 [Degree-1 maps and rank inequalities in Heegaard Floer homology](https://arxiv.org/abs/2504.19871). The primary abstract concerns Floer-homology ranks for particular rational-homology-solid-torus maps. It does not supply a verified theorem on the minimum genus of arbitrary Heegaard splittings. It must not be counted as solving this target merely because both titles contain Heegaard, rank, and degree-one maps. No full audit of that paper is claimed.

Search absence is not a universal literature certificate. External published theorem statements were checked in their preserved primary versions; their full long proofs were not independently reconstructed.

## Rights and release gate

All five preserved primary PDFs match the hashes reported in the release. Full PDFs, extracted scholarly text, and page images remain outside the release and this audit package. The author-version restriction on reposting the K3 book was checked. This audit contains original mathematical review and short attributed descriptions with source links, and does not redistribute that book.

There are no mandatory corrections to the frozen mathematical package. Its embedded `independent_audit: pending` describes the pre-audit snapshot. Keep the freeze intact and attach this separate audit, or deliberately issue a newly hashed version if updating that metadata. This verdict approves only the package's integrity and candid unsolved-partial-results framing. Root publication policy, a refreshed repository gate when needed, and authorized remote changes remain separate decisions.
