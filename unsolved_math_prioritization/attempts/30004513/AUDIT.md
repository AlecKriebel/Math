# Source-credit audit: sharp constrained-star bound

## Decision and provenance

**Accept the sharp-star theorem as a credited result of Alper Ferudun's September 30, 2026 unrefereed preprint. The original question bundle is only partially resolved; no new theorem, proof novelty or priority is claimed.**

Primary claim: Alper Ferudun, *A Proof of Paták's kb+1 Conjecture for Constrained Stars, with Improved Bounds for Complete Graphs*, version 1.0, manuscript/online date September 30, 2026, EulerSolve, OWR-1703876-006. Landing page: <https://eulersolve.org/papers/owr-1703876-006/>. Canonical retrieved PDF: <https://eulersolve.org/papers/owr-1703876-006/paper.pdf?v=b2db3bc623ae>. Its page states DOI <https://doi.org/10.5281/zenodo.23062843>; the DOI and Zenodo API fetches failed with HTTP 403 in this audit, so DOI registration/content was not independently verified. The PDF was obtained directly from the author's public landing-page link.

PDF identity: 159570 bytes; SHA-256 `b2db3bc623aec9e6efdc4986489270ca0343bec3288c658745a5d06267c68001`.

The source labels itself an unrefereed, AI-assisted preprint. Those facts neither establish nor refute its claims. The acceptance here rests on independently checking the finite induction and all reductions described below. The source archive and author verification report were not read or executed before the historical independent checker was written, and are not used as correctness evidence. No author was contacted. This authored reconstruction and audit are also AI-assisted and unrefereed; acceptance does not mean external human peer review, journal acceptance or proof-assistant certification.

This audit credits a later proof claim rather than treating an earlier explicit conjecture as evidence of present unsolved status. Bounded source discovery does not establish exhaustive literature coverage or priority absence. Historical retrieval and inspection details are recorded in [SOURCE_METADATA.json](SOURCE_METADATA.json).

## Original and later primary statements checked

1. Pavel Paták, “Helly numbers of disconnected sets,” in *Oberwolfach Report 30/2020*, printed pp.1500–1501 (PDF pp.32–33): <https://ems.press/content/serial-article-files/46867>. The report's star question asks whether `bk+1` points suffice. It also separately asks about better complete-graph bounds and extending the method to nontrivial higher homology/homotopy.
2. Pavel Paták, *A sharper Ramsey theorem for constrained drawings*, arXiv:1909.08489v4, November 2024: <https://arxiv.org/abs/1909.08489v4>. Definitions 1, 3 and 4, Proposition 1(5)–(6), Lemmas 1–2, and Conjecture 1 were checked against the full local extraction. The current arXiv landing page was checked on October 10, 2026 and still lists v4 as its latest version. We did not inspect the typeset 2025 journal version.
3. Ferudun, cited above: full text extracted, §§2–3 read line by line, plus Lemma 4.1, Corollary 4.2 and Proposition 4.3. PDF pages 3–7 were rendered and visually inspected, not merely extracted. The rest was read for scope only; this audit does not accept every theorem or computation in that manuscript.

Credited pre-existing cases: Paták already proved the sharp bound for `b=1,2` and all `k`, and the cases `k=0,1` are elementary. Paták also gave the `bk`-vertex lower example for b-iatlon graphs. The general star theorem and the monotone-system coloring proof are credited here to Ferudun, not to this audit.

## Exact definitions and scope

Let `b >= 1` and `k >= 0` be integers. A labelled graph H has, for each edge e, a family L_e of subsets of `V(H) \ e`. It is b-iatlon when every `(b+1)`-subset Y contains an edge e whose complementary set `Y \ e` belongs to L_e.

A constrained copy of a graph F consists of a subgraph F' isomorphic to F and one allowed label l(e) for each edge, satisfying:

- `l(e) ∩ V(F') = ∅` for every edge e;
- `l(e) ∩ l(f) = ∅` for every pair of vertex-disjoint edges e and f.

Labels of adjacent edges may overlap. All star edges share the center, so the second condition is vacuous for a star. It becomes essential in the complete-graph consequence and is checked there separately. No geometric disjointness of star paths is introduced.

In the closure setting, vertices are distinct members of a given finite set S in a topological space X, and each edge e is represented by a path within `cl(e ∪ l(e))`. A closure operator is extensive, monotone and idempotent. The imported planar hypothesis, that `cl(A)` has at most b path components for every finite A, implies the weaker condition used by Ferudun: every set Y of b+1 points contains two points lying in the same path component of `cl(Y)`.

## Independent check of the central induction

A monotone graph system on a finite set V is a graph G_T with vertex set T for every `T ⊆ V`, such that edges persist when T grows. Call I independent if G_I has no edges. Let α be the maximum size of an independent I. A good k-star is a center c with k distinct leaves L such that, for every x in L,

`cx ∈ E(G_{V \ (L \ {x})})`.

**Lemma (Ferudun, Theorem 2.2).** If a monotone graph system has no good k-star, where k>=1, then V admits a partition into k independent classes; hence `|V| <= kα`.

Here is a full independent verification of the proof.

Induct on |V|, keeping k fixed. For V empty, use k empty classes. Otherwise choose p in V and write W=V\{p}. On W define the link system

`J_T = G_{T ∪ {p}}[T]`, for `T ⊆ W`.

This is monotone: an edge present with support T∪{p} stays present with the larger support T'∪{p}. A good k-star `(c,L)` in J would be a good k-star in G, because for every leaf x,

`(W \ (L \ {x})) ∪ {p} = V \ (L \ {x})`,

and p is neither the center nor a leaf. Consequently J has no such star, and the induction hypothesis gives a disjoint partition `W=B_1 ⊔ ... ⊔ B_k` independent in J. Thus G_{B_i∪{p}} has no edge with both ends in B_i; every one of its edges, if any, meets p.

If one of these k graphs is edgeless, put p in that corresponding class. It remains independent by construction. Every unchanged class B_j is independent in G, since G_{B_j} is a subgraph of G_{B_j∪{p}} and the latter has no edge inside B_j. This is the required partition.

Otherwise every class yields an edge `p b_i` with `b_i ∈ B_i`. The b_i are distinct because the classes are disjoint. Let `L={b_1,...,b_k}`. For every i,

`B_i ∪ {p} ⊆ V \ (L \ {b_i})`.

Monotonicity therefore puts `p b_i` in the graph indexed by the set on the right. This constructs a good k-star, contradicting the hypothesis. The induction is complete.

**Adversarial checks.** The link, not ordinary deletion, is essential: p can activate edges between other vertices. The inductive statement applies to all monotone systems, so the proof need not assert that a link retains any b-iatlon property. Empty classes cause no problem: they immediately give the first branch. The case k=1 is valid. For k>=|V| the independent singleton/empty partition is also consistent. There is no demand that the k edge supports be disjoint.

## Transfer to arbitrary b-iatlon graphs

For a given labelled H with vertex set V, put an edge uv in G_T exactly when u,v belong to T and some allowed label of uv is contained in T. This is a monotone graph system regardless of whether the allowed-label families themselves are upward closed.

Every `(b+1)`-subset Y contains an edge in G_Y by b-iatlon. A larger independent set cannot contain such a Y, by monotonicity. Therefore α<=b. If `|V|>=bk+1`, then `|V|>kα`, and the preceding lemma gives a good k-star when k>=1.

For its edge cx, the definition of G supplies a label contained in `V\(L\{x})`. Allowed labels already avoid the endpoints c,x, so this label avoids all of `L∪{c}`. These edge labels satisfy exactly the constrained-copy condition. Since every pair of star edges meets at c, no further label-disjointness condition remains. The case k=0 is one chosen vertex.

Thus **every b-iatlon graph on at least bk+1 vertices has a constrained K_{1,k}.** This is the full arbitrary-b-iatlon statement, not merely a closure-induced special case.

The lower bound is Paták's construction: take b disjoint copies of K_k and allow every possible label avoiding an edge's endpoints. Every b+1 vertices contain a same-copy pair, so the labelled graph is b-iatlon. It has no ordinary K_{1,k}, since any connected copy would need k+1 vertices in a component of size k. Therefore

`p(K_{1,k},b)=bk+1`.

## Closure realization and sharpness

Given P of bk+1 points satisfying the weaker pair condition, for each `(b+1)`-subset Y choose two points u,v connected by a path in cl(Y), and give uv the label `Y\{u,v}`. This is a b-iatlon graph; each retained label has exactly b−1 elements. Its constrained star transfers edge by edge to the selected paths. Label restrictions are preserved exactly. Hence the original planar upper bound is proved, and in fact the same argument works in any topological space under that pair condition.

For a sharp closure example in R^d, d>=1, partition R^d into b disjoint convex slabs R_i (and use all of R^d when b=1), and define

`cl(A) = union_i conv(A ∩ R_i)`, with `conv(∅)=∅`.

Each hull remains in its slab. Extensivity and monotonicity are immediate; moreover `cl(A)∩R_i=conv(A∩R_i)`, so convex-hull idempotence gives `cl(cl(A))=cl(A)`. A union of at most b path-connected sets has at most b path components, even when some merge.

Choose a finite S with k points in each slab. For any proposed edge with label in S, the set `A=e∪l(e)` is finite. Each nonempty `conv(A∩R_i)` is therefore compact; these finitely many compact sets are disjoint, so each is relatively clopen in their union. A connected path in cl(A) cannot move from one of them to another. Every star leaf must lie in the center's slab, forcing k+1 points of S there, which is impossible.

**Important qualification:** the proof needs compactness only for those finite A. For arbitrary infinite A, the slab hulls need not be compact or separated; the source does not need or assert that arbitrary cl(A) has exactly b components. At most b always suffices. Thus there is no hidden closure/topology defect in the lower example.

This proves sharpness in the plane and in every R^d for d>=1. The k=0 threshold is separately one point.

## Complete-graph consequence independently checked

Paták's join mechanism, with the newly proved star theorem, gives

`p(K_1+F,b) <= b p(F,b)+1`.

Set N=p(F,b). Find a constrained N-leaf star with center v and leaf set X. Restrict H to X while retaining only labels contained in X; this restriction is b-iatlon. It supplies a constrained copy F' of F whose labels lie in `X\V(F')`. Retain the star edges from v to V(F'). Their labels avoid X∪{v}, whereas all inner F' labels lie in X. Therefore outer-versus-inner disjoint edges have disjoint labels. Inner disjoint-edge pairs were already valid, and two outer edges meet at v. All labels avoid the final vertices. This verifies every required label condition.

Starting with p(K_1,b)=1 yields the credited upper bound

`p(K_n,b) <= 1+b+...+b^(n−1)`.

The usual all-labels encoding of an ordinary Ramsey-extremal graph gives

`R(n,b+1) <= p(K_n,b)`.

This Ramsey lower bound concerns arbitrary b-iatlon graphs; the encoding need not be realizable by a planar closure. In the closure setting the directly checked slab lower bound is `(n−1)b+1`. The join upper bound does transfer to closure drawings. Thus the second question has an improved general upper bound, but no all-n exact value is claimed here.

For completeness, the same join recurrence proves `p(K_{m,n},b) <= n b^m + sum_{j=0}^{m−1} b^j`, which gives `p(K_{3,3},3)<=94`. This is an arithmetic consequence, not an independent new theorem claimed by this audit.

## What is not accepted or claimed

- The whole imported record is not marked solved. Its third question on nontrivial higher homology/homotopy is not answered by the inspected star theorem, and is explicitly excluded by Ferudun.
- Exact complete-graph thresholds for general n,b are not determined here.
- The source's computational triangle-threshold assertion, other SAT-derived values, and SAT/exhaustive audits were not used or independently certified here.
- The source's Radon/Helly corollaries and higher-dimensional topological dependencies were not independently re-proved. No vanishing-homology result is silently promoted to a nontrivial-homology extension.
- No novelty or priority-absence certificate is asserted. The checked general coloring/star proof is attributed to the September 2026 source; the original cases and mechanisms retain Paták credit.
- This edition proposes no change to QUEUE.md or unrelated repository content and implies no merge, release, DOI creation, journal submission or external outreach.

## Independent finite validation

The historical independent checker used only the Python standard library and was written without reading the source's verification scripts. It checked the full coloring implication, not only the numeric n<=kα consequence, on every monotone graph system with at most four vertices. Edge activation was represented as an upward-closed family on the complement of its endpoints; all 46,656 four-vertex systems were enumerated. It independently searched for good stars and computed the chromatic partition number by subset dynamic programming. A separate recursive implementation of the link proof returned a star or coloring certificate, checked directly against the input.

Historical checks passed in normal and optimized execution. Their substantive results agreed; elapsed timings differed. There were 191,110 monotone-system/k checks, including exhaustive system counts 1, 1, 2, 27 and 46,656 at 0, 1, 2, 3 and 4 vertices, respectively; 750 seeded random larger systems (300 at five vertices, 300 at six, 100 at seven, 50 at eight); 210 b-iatlon sharp-threshold label checks against the original label exclusions; and eight deliberately corrupted certificate/system controls, all rejected. These are historical supplementary check-count metadata, not distributed raw outputs, certificates or datasets.

Finite computations corroborate the definitions and implementation. The all-size proof is the complete written induction and reductions above; it does not depend on omitted code or data. This proof-only edition excludes programs, raw outputs, generated certificates, datasets, copied third-party source documents/text/images and private coordination material. Edition preparation rechecked frozen input byte identities and publication integrity, without new source retrieval, source-text inspection, literature search or rerunning historical mathematical computations. [ACCEPTANCE.json](ACCEPTANCE.json) binds the exact distributed audit bytes.
