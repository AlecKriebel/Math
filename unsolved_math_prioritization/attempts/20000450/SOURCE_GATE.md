# Source and prior-attempt gate: 20000450 / AIM-ALGEBRAIC_NUMBER_THEORY-0102

2026-10-02, rank 352. Initial substantive author count 0/5. The requested unsolvedmath.com problem page was attempted and inaccessible; the complete pinned dataset record and its full prior report were then read at revision 37e53eabe540fb458758e198be61634bd02ee008.

## Exact primary target

The complete AIM workshop PDF, *Rational and integral points on higher dimensional varieties*, was downloaded from https://www.aimath.org/WWN/qptsurface2/qptsurface2.pdf (502,057 bytes; SHA256 8b64d2f6b91f791c35afae10b2ef79c15a927a94c2142a56386f80c8b8a596e6). The apex-host download returned 403; the official www host succeeded. Its cover identifies the December 11–20, 2002 workshop and November 22, 2004 document version. Question 17 and all four remarks on printed p.51 were rendered and visually inspected. The official HTML also agrees: https://www.aimath.org/WWN/qptsurface2/articles/html/27a/ .

The question asks to compute the 5-torsion of the genus-one normalization of the plane pencil P+lambda C^2=0, where P is the regular pentagon's five-side-line product and C its circumcircle equation. The five points at infinity are already identified in the remarks as torsion. The remarks motivate twists and possible Tate–Shafarevich classes, ask about the elliptic pencil, and suggest variants. They do not specify a ground field, an origin or an equation scaling. The projective equation requires the homogenizing factor T multiplying C^2.

We retain the prior report's explicit K=Q(sqrt(5)) model and chosen rational infinity origin. This computes the source's regular-pentagon pencil up to the specified coordinate/parameter normalization. A full arithmetic answer must specify its field and the smooth parameter locus. It must not confuse the five known infinity points with all twenty-five geometric torsion points, or claim locally soluble nontrivial torsors from a model already having a rational point.

## Imported work and exact remaining task

The full imported report is a separate earlier dataset computation, dated July 27, 2026, not a repository author turn or independent proof certificate. It gives the regular side-line polynomial, proves the infinity cyclic subgroup and its quadratic Galois character, states the Weil-pairing quotient character, and normalizes the reflection quotient to a rational conic. It explicitly leaves the other twenty torsion points, the extension/division field, the Tate modular reparameterization and the full exceptional parameter set uncomputed. We will check its identities before depending on them, credit those reductions, and pursue the remaining computation rather than relabeling its partial result as a new answer.

The normalization has phi=(1+sqrt(5))/2, Q=X^2+Y^2-T^2 and
P=2(X^5-10X^3Y^2+5XY^4)+5phi(X^2+Y^2)^2T-5phi^3(X^2+Y^2)T^3+phi^5T^5.
The origin is [0:1:0]. Parameter rescaling is material; every formula below will use this P and Q.

## Current literature and related-attempt checks

Primary AIM pages and exact-phrase searches were checked. No direct published full computation of this precise pencil was located; that bounded search does not establish novelty or current open status. Relevant established machinery includes Fisher's *The Cassels–Tate pairing and the Platonic solids*, JNT 98 (2003), 105–155, DOI 10.1016/S0022-314X(02)00038-0, and his 2001 JEMS 5- and 7-descent paper. Those describe Tate families, split torsion and isogenies; their applicability must be derived for the singular plane model, not assumed from an unrelated normal quintic embedding.

Live exact-ID PR, branch and target-path commit searches are empty. Default-branch code search returns only assignment metadata. Available all-ref history (411 refs) has no exact ID, qptsurface2 or McCallum attempt. The related pentagon PR90 is a different eight-line marked-lifting problem; PR190 concerns a dodecahedral-geodesic argument, also distinct. No overlapping computation was found. The catalog gives queued 0/5, eligible, no holds, review hash fdab0cef33226347101e4c4069ae57e771eb606a84dc03b737701c3640d091cc. No target entry was found in current state or related-target groups. Adjacent imported targets 20000448–20000453 were inspected.

Repository policies, the dedicated folder, five substantive turns, independent audit, no outside contact and no routine release remain in force. Source retrieval and this gate consume no author turn. Source PDFs, screenshots and raw imports remain local-only. Completion estimate at this gate: 10%, subjective.
