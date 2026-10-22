# Independent mathematical audit: problem 30005082

**Publication context:** This historical independent review is preserved below. REPORT.md is the byte-identical corrected derivative named in the audit, including Mohammadi in the coauthor attribution. References below to the original packet, original verifier, derivative manifest, audit controls, and their filenames describe the earlier review stage. They are not fresh checks of this public delivery. The complete superseded original and prior manifests are omitted. Fresh portable checks and all-mode references are supplied here; SOURCE_AUDIT.json retains only public inspection and source-byte metadata. Final sealing evidence is external to avoid circular hashes. No source PDF or extracted source body is included or replayed.

Audit date: 8 October 2026. Scope: the five already completed approaches in the frozen v2 packet. No additional proof-search approach was undertaken.

## Decision

**Accept the five scoped mathematical results. The general higher-Grassmannian mutation comparison remains unresolved here, with the existing exhausted 5/5 disposition unchanged.** No mathematical correction to the pinned report or its local formula correction was needed. One bibliographic correction is required: the work at arXiv:2208.04521 is by Clarke, Higashitani, **and Mohammadi**. A separate derivative and exact patch implement only that attribution change and the corresponding manifest update.

The audited original `REPORT.md` has SHA256:

`603c7dfd4c47072bd49e04bd078c06b938ab0b08c29bc61c39a92c59a9b06579`

The corrected derivative's `REPORT.md` has SHA256:

`d6be3600406a3c8b111c16815601a7a477d73b2265b6d62c6dbba4e44d5b73b3`

Both the original packet and source files were preserved. This audit made no GitHub changes. Acceptance does not certify novelty, a literature-exhaustion claim, journal-version wording, or a solution of the global question.

## 1. Local min/max correction: accepted

Write the mutation coordinate as t, the remaining coordinates as x, and A = a(x), B = b(x). Let m = min(A,B), M = max(A,B), w = -e_t, and F = conv(a,b). The factor F is orthogonal to w because neither endpoint uses t. Reflection epsilon sends t to -t without changing A or B.

For the dual-side convention phi_(w,E)(v) = v - min(E(v)) w, the relevant support values are m for F, -M for -F, and -|A-B| for F-F. Direct substitution therefore gives

- Psi_min = phi_(w,F) composed with epsilon;
- Psi_max = phi_(-w,-F) composed with epsilon;
- Psi_min = phi_(w,F-F) composed with Psi_max.

This proves the identities on the entire real vector space. In particular, the last identity uses M - |A-B| = m, rather than a numerical sample argument. The alternative formulas with the shear L(x,t) = (x,t+A+B) also follow: the output of phi_(w,F) composed with Psi_max is -t+A+B, and applying L inverse and then phi_(w,F) twice gives -t+m. The inverse of phi_(w,E) is phi_(-w,E) because the support function is constant along w. Integral covectors give integral branch shears of determinant one; epsilon has determinant minus one. Thus the stated integral piecewise-linear bijectivity is valid.

Negating only w produces -t-m. At t=0, A=0, B=1, this is 0 while Psi_max is 1. The rectangle valuation of p_145 supplies exactly that input in the stated coordinates. This is a genuine valuation-point counterexample to the displayed ambient identity, without any inference about the actual geometric flip.

I inspected the pixels of HN arXiv:2107.04264v2, printed page 30: Definition 6.4 uses max, while Proposition 6.5 prints the unnegated F in the purported max factorization. Its preceding Remark 6.3 already warns that a max-style image need not be convex. The report correctly separates the algebraic repair from convexity. The published 2023 work is bibliographically confirmed, but its article body was not available for this audit; **the formula-defect claim remains restricted to arXiv v2**. [HN v2](https://arxiv.org/abs/2107.04264v2); [author publication record](https://sv2-mat.ist.osaka-u.ac.jp/~higashitani/papers.html).

## 2. Rectangle identification and the nonconvex max image: accepted

The partition attached to a triple J is mu_i = 3+i-j_i. With row-major rectangle order (11,12,13,21,22,23,31,32,33), the maximum diagonal count outside mu produces the two vectors stated in the report. HN Table 2 uses a different order, (11,12,21,22,13,31,23,32,33). I inspected the graphical column headers on printed page 32 and checked all twenty table rows after that permutation: all agree with the independently generated values.

The rectangle-body identification is stronger than a claim about a few generators. In Rietsch-Williams v2, Proposition 14.4 gives the diagonal-count valuation, Lemma 16.2 gives the unimodular diagonal-difference transformation to GT coordinates, and Proposition 16.6 identifies the rectangle convex hull with the superpotential body. Their general body identification supplies the Newton-Okounkov interpretation. These are cited geometric inputs, not inferred from finite Hilbert counts. [Rietsch-Williams v2](https://arxiv.org/abs/1712.00447v2).

As an independent finite cross-check, diagonal differences of the twenty generated vectors are exactly the twenty weakly row- and column-increasing binary 3 by 3 patterns. This also confirms the coordinate convention and the nonnegative first coordinate.

The Young-diagram labels at the square are 356 for 11, 256 for 12, 346 for 21, 236 for 22, and 456 for the empty diagram. The exchange with 246 is the determinant identity in the report. I checked it independently by recursive Laplace expansion, rather than reusing the author's permutation-polynomial implementation.

For u = val(p_145) and v = val(p_356), the max map changes only their first coordinates, to 1 and 2 respectively. Its image midpoint is

(3/2,1/2,1/2,1/2,1,3/2,1/2,3/2,2).

The map is an involution since its exchange terms do not use the changed coordinate. At the midpoint the two exchange sums are both 1, so the unique preimage has first coordinate -1/2. All points of the rectangle body have nonnegative first coordinate. The image midpoint is therefore excluded although both endpoints belong to the image. This is an exact nonconvexity proof.

Its scope is exactly the unadjusted max map in the specified rectangle coordinates. It neither contradicts the min-cluster theorem nor disproves an Escobar-Harada map after a compatible coordinate identification.

## 3. Label-preserving additive transport: accepted

For B_0, the equality between the exponent sums with labels 134+245 and 145+234 follows row by row. Under B_1, the four row assignments become respectively (3,1,4), (2,4,5), (4,1,5), and (2,3,4). The difference between the two sums is precisely

 e_(1,3) - e_(1,4) + e_(2,4) - e_(2,3),

which is nonzero. An additive map must preserve every equality of sums in its domain, so no additive semigroup map can realize all these prescribed generator images. Any linear lattice map with that prescribed action is likewise impossible.

This does not prohibit nonlinear polytope mutations or general standard-basis wall-crossing bijections. In particular, Escobar-Harada do not assert that their algebraic wall-crossing is always a semigroup homomorphism. Their arXiv v2 Example 4.5 explicitly distinguishes these notions using a hypersurface. Their general adjacent-prime-cone theorem and two-plane result do not supply the missing higher-Grassmannian characterization. I checked that example in arXiv v2 and publication metadata separately; I did not establish textual identity with the journal typesetting. [Escobar-Harada v2](https://arxiv.org/pdf/1912.04809v2); [publication record](https://academic.oup.com/imrn/article-abstract/2022/7/5152/5901312).

## 4. Exact ranks and labeled-cone nonadjacency: accepted

Independent fraction-free integer elimination gives rank 10 for every B_ell exponent matrix, ell = 0,...,6, and rank 12 for the row stack of A_0 and A_1. Therefore their rational or real row spaces intersect in dimension 10+10-12 = 8. These are ranks of integer lattices; no unproved lattice-index or unimodularity assertion is being added.

The geometric step in the report is valid under its cited block-field SAGBI theorem. The initial ideal is the matching-field prime binomial ideal, with lattice of exponent relations ker_Z(A_ell). A weight in the corresponding relatively open Groebner cone makes every binomial homogeneous, so it annihilates this relation lattice. By closure the entire cone lies in row_R(A_ell). The cone has dimension 10, equal to that row-space dimension, so its linear span is exactly row_R(A_ell). Binomial coefficient signs do not affect this argument.

In the unquotiented weight space, an adjacent pair of ten-dimensional maximal cones must share a nine-dimensional face. A common face lies in the intersection of their linear spans, here only eight-dimensional. Thus these two particular cones, in the common fixed Plucker labeling, are not directly adjacent. Quotienting common lineality consistently preserves the obstruction. Relabeling one cone independently, changing embeddings, or supplying a multi-wall path would be different claims. None is ruled out or supplied by this test.

The positive block-field toric-degeneration and mutation results are prior theorems, not conclusions drawn from the finite computations. [Clarke-Higashitani-Mohammadi, arXiv:2010.04079v1, Theorems 1-2](https://arxiv.org/abs/2010.04079v1).

## 5. Coherence versus SAGBI: accepted

The reconstructed hexagonal matrix is exactly the first three rows of the CMZ Definition 10 construction with p=7, c=3, sigma=615234. Exhaustive determinant-term evaluation finds a unique minimum for every triple, with minimum gap 2 to the next term. Thus coherence is established for this matrix.

Independent packed-monomial multiset enumeration yields semigroup dimensions 1,20,174,968,4040 in degrees 0 through 4. Separately enumerating semistandard tableaux of shape (d,d,d) on six letters gives the Plucker-ring dimensions 1,20,175,980,4116. In particular the degree-two discrepancy is exact. If these twenty minors were a SAGBI basis, their initial monomials would generate the full initial algebra, which has the same graded dimensions as the original algebra. Since 174 differs from 175, they do not. This concerns the degeneration supplied by this matching field and says nothing against other toric degenerations.

The seven valid block controls have unique minima, minimum gap 1, and the expected counts through degree four. Finite agreement alone proves no all-degree property. The report correctly imports the positive block theorem and treats the excluded hexagonal field as a known boundary example.

CMZ v2 Theorem 2 has the stated pattern-avoidance hypothesis; Example 5/Table 1 identifies six prime types, five realizable by matching fields and EEEE excluded; Example 6 gives the hexagonal example; Conjecture 1 remains a conjecture in the inspected source. HN v2's separate Appendix A has a conflicting prime-type count; the report does not rely on that count and correctly follows CMZ v2 for this classification. [CMZ v2](https://arxiv.org/abs/2206.13975v2).

## 6. Remaining source scope and correction

The 2022 GT/FFLV/block-polytope paper is by Oliver Clarke, Akihiro Higashitani, and Fatemeh Mohammadi. Its scope agrees with the report; only the abbreviated attribution was incomplete. `ATTRIBUTION_FIX.patch` changes that name and refreshes the affected manifest entry. [Exact arXiv record](https://arxiv.org/abs/2208.04521).

Kowaki's inspected local source is arXiv:2405.15215v1, whose Theorem 3.2 requires the specified tropical-line swap and additional condition. The publisher confirms a 28 May 2025 version of record; this audit does not transfer uninspected theorem numbering or text to that version. [Publisher metadata](https://link.springer.com/article/10.1007/s40879-025-00832-x).

Cho-Kim-Kim-Park's inspected June 2026 v1 Proposition A/Theorem 4.3 constructs a cluster-seed-indexed family of Newton-Okounkov bodies; it does not state exhaustion of arbitrary prime tropical cones. This remains a preprint-version scope check. [June 2026 v1](https://arxiv.org/html/2606.08570v1).

The motivating Oberwolfach question concerns higher-Grassmannian comparison; it does not license replacing arbitrary maximal cones by prime binomial ones without stating that restriction. The report does state it. [Oberwolfach Report 17/2022, printed page 917](https://ems.press/content/serial-article-files/46955).

## 7. Reproducibility and falsification controls

`independent_checks.py` is an independently authored standard-library checker. It uses fraction-free elimination instead of the author's rational RREF, packed base-eight monomials and multisets instead of iterative tuple-semigroup generation, semistandard tableaux instead of the Weyl dimension product, and recursive Laplace expansion instead of direct permutation expansion. Twelve chamber-coefficient identities supplement 125 exact rational comparisons against the supplied candidate functions. It does not use the author's claimed status as evidence.

The original checker, original manifest verifier, and independent checker all pass in normal Python, -O, and -OO. The independent output is identical across modes. The corrected derivative's verifier also passes in all three modes.

Actual UID 1000 replay used a disposable directory of mode 0555 and files of mode 0444. The independent checker succeeded in each interpreter mode; actual create and append operations both raised PermissionError. Original packet hashes were checked before and after and are unchanged.

Ten meaningful semantic mutations were independently rejected in all three modes: replacing max with min, dropping factor negation, reversing the direction sign, removing the difference factor, swapping the wrong block cardinality, misorienting diagonals, falsifying semigroup counts, lowering ranks, reversing an exchange sign, and selecting maximum rather than minimum determinant terms. These tests load modified candidate functions directly, so rejection is semantic rather than merely a stale-hash failure. Six separate integrity mutations were rejected in all three modes: changed report, extra file, extra directory, missing report, duplicate manifest entry, and path traversal. Total: 30 semantic and 18 integrity rejection runs.

Eight retained source PDFs independently match their declared byte counts and SHA256 hashes. Source PDFs, extracted source text, and private coordination material are not included in this audit deliverable. `SOURCE_HASH_CHECKS.json`, `AUDIT_CONTROLS.json`, `INDEPENDENT_RESULTS.json`, and `DERIVATIVE_RECEIPT.json` contain the evidence metadata.

The verifier is a reproducibility/integrity check against the pinned packet. A self-consistent manifest is not a signature against an adversary who rewrites both files and manifest; the external pinned hashes and this independent audit are essential. None of the programs independently proves the cited geometric theorems or exhausts the literature.

## Final boundary

Retain only the local correction and the four additional scoped boundary results. Do not promote them to a general equivalence theorem, a counterexample to the actual Escobar-Harada theorem, or a classification of all relevant higher-Grassmannian prime-cone wall crossings. The correct global disposition remains **unfinished, exhausted 5/5**.
