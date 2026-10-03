# Source audit: 6j-symbol equivalence from isomorphic TQFTs

Target: rank 448, ID 10400167, AMR-103-0167. Source checked 2026-10-03 UTC.

## Exact scope in mathematical paraphrase

Kawahigashi asks what relation must hold between two fusion-rule algebras with 6j-symbols when their associated three-dimensional TQFTs are isomorphic. The accompanying remark asks about Sato's equivalence of bimodule systems, not mere change of bases in fixed fusion spaces.

Primary source: T. Ohtsuki (editor), *Problems on invariants of knots and 3-manifolds*, Geometry & Topology Monographs 4 (2002), pp. 377–572, Problem 9.3 on printed p. 510, PDF p. 138, and reference [362] on p. 563. [Publisher PDF](https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf).

The definition on printed p. 493 assigns vector spaces to oriented closed surfaces and maps to compact 3-cobordisms. Its subsequent use of “extended” can refer to framing/p1 data; this is not automatically extension to circles or points. Section 8.5 separately discusses lower-dimensional extension. No such extension is included in Problem 9.3's hypothesis.

The catalogue URL https://www.unsolvedmath.com/problems/10400167 was attempted with web retrieval and direct HTTPS on 2026-10-03; neither provided a readable page (direct HTTPS returned 403). The pinned catalogue record and primary publisher source agree on the target. No live catalogue status is claimed.

## Sources and what they establish

- N. Sato, *Constructing a non-degenerate commuting square from equivalent systems of bimodules*, IMRN (1997), 969–981, is the exact cited reference. The author's [1998 explanatory proceedings article](https://www.kurims.kyoto-u.ac.jp/~kyodo/kokyuroku/contents/pdf/1024-5.pdf), pp. 42–44, explicitly recalls the definitions and construction: equivalence is mediated by a finite system of four types of bimodules. It is Morita-type equivalence. The original IMRN article's complete text has not been independently inspected here; the author's exposition is the checked source for this identification.
- V. Turaev and A. Virelizier, [*On two approaches to 3-dimensional TQFTs*](https://arxiv.org/abs/1006.3501), Theorem 11.2, identify the spherical-category state-sum TQFT with the RT TQFT of its center. Corollary 11.5 gives a sufficient center-equivalence condition for isomorphic TQFTs. It does not state the converse needed here.
- P. Etingof, D. Nikshych and V. Ostrik, [*Weakly group-theoretical and solvable fusion categories*](https://arxiv.org/abs/0809.3031), Theorem 3.1, prove that fusion categories over an algebraically closed field of characteristic zero are Morita equivalent exactly when their centers are braided equivalent. An ordinary TQFT isomorphism must first be shown to produce that braided equivalence. Their [*Fusion categories and homotopy theory*](https://arxiv.org/abs/0909.3140) gives a related Brauer–Picard formulation.
- B. Bartlett, C. L. Douglas, C. Schommer-Pries and J. Vicary, [*Modular categories as representations of the 3-dimensional bordism 2-category*](https://arxiv.org/abs/1509.06811), Theorems 1–4, classify TQFTs whose domain includes circles and surfaces with boundary. Theorem 2 gives the oriented version. Applying it directly to an isomorphism only on closed surfaces changes the hypothesis.

No complete primary-source resolution of the original unextended converse was established in this bounded search. This is a statement about the search, not a claim that the literature has no resolution.

## Scope of the attempts

The constructive partial results below concern unitary fusion categories over C, with their canonical positive spherical structures, or explicitly specified finite-group state sums. This is a declared subcase, not an unstated replacement of the full target. We do not claim novelty for elementary consequences or known Morita examples. A complete result would need the converse in the original scope, or an actual counterexample to Sato/Morita-type equivalence.

## Finite-gauge references and normalization

R. Dijkgraaf and E. Witten, *Topological gauge theories and group cohomology*, Commun. Math. Phys. 129 (1990), 393–429, [author-hosted PDF](https://www.ias.edu/sites/default/files/sns/%5B126%5DCommMathPhys129-1990.pdf), is the primary finite-group/cohomology construction. The web tool could inspect its text; a direct local download returned 403. Our normalized untwisted partition function is groupoid cardinality, |Hom(pi_1(M),G)|/|G|, not unweighted conjugacy-orbit count. The explanatory sentence on Ohtsuki p. 510 should not override that normalization.

D. Altschüler and A. Coste, *Invariants of three-manifolds from finite group cohomology*, J. Geom. Phys. 11 (1993), 191–203, [publisher record](https://doi.org/10.1016/0393-0440(93)90053-H), establishes the classical cyclic/lens Gauss-sum setting. Its publisher abstract was accessible; the CERN full PDF was bot-blocked, so no particular numbered formula from that inaccessible PDF is cited as checked. TURN_4.md instead supplies a bar-resolution derivation of its precise formula.
