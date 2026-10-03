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
- P. Etingof, D. Nikshych and V. Ostrik, [*Fusion categories and homotopy theory*](https://arxiv.org/abs/0909.3140), Theorem 1.1, identifies the Brauer–Picard 2-groupoid with the corresponding braided-equivalence data of centers. These are categorical equivalence data; an unextended TQFT isomorphism must first be shown to produce them.
- B. Bartlett, C. L. Douglas, C. Schommer-Pries and J. Vicary, [*Modular categories as representations of the 3-dimensional bordism 2-category*](https://arxiv.org/abs/1509.06811), Theorems 1–4, classify TQFTs whose domain includes circles and surfaces with boundary. Theorem 2 gives the oriented version. Applying it directly to an isomorphism only on closed surfaces changes the hypothesis.

No complete primary-source resolution of the original unextended converse was established in this bounded search. This is a statement about the search, not a claim that the literature has no resolution.

## Scope of the attempts

The constructive partial results below concern unitary fusion categories over C, with their canonical positive spherical structures, or explicitly specified finite-group state sums. This is a declared subcase, not an unstated replacement of the full target. We do not claim novelty for elementary consequences or known Morita examples. A complete result would need the converse in the original scope, or an actual counterexample to Sato/Morita-type equivalence.
