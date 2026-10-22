# Independent mathematical audit: problem 30002618

Date: 2026-10-06. Decision: **accept the corrected rigorous partial results**. No full solution, intrinsic general classification, geometric-origin theorem, or novelty claim is accepted or asserted.

## Input and exact question

The author freeze is 11,786 bytes, SHA-256 `0947c56eb1d4642ac9e92298022a21419aac91a740d1b0ee4ace588260dd2665`. All six members were read, including their metadata. The external inventory, CRCs, member lengths and hashes match. The complete problem and corresponding research-report entry were independently inspected from the complete corpora; the entry is empty, the statement hash matches, and the complete-record review hash is `5eb4c6f3e31ac0d51d0bea619752f16f9bfd38ecee4c23801b8862107b2fb0ef`. Rank 843 and identifier OWR-13102-007 match.

The [original report](https://ems.press/journals/owr/articles/13102), contribution pp. 1790–1792, distinguishes universal exactness (Question 4), its failure (Theorem 5), and the coefficient-classification/geometric-origin question (Question 6). The problem is the cohomological invariant-cycle sequence. A Tannakian homotopy sequence would not answer it. The report carries volume year 2014 and was published in 2015.

## Source-dependent inputs and hypotheses

The [journal article](https://www.research.unipd.it/handle/11577/3187169) was inspected throughout, including Sections 2–4, Theorem 10 and Appendix A. Its Proposition 1 supplies the coefficient comparison; its monodromy construction and Lemma 7 supply N=j q R and ker R=im i. Annular residues are isomorphisms for the coefficient objects used here. The unipotent non-exactness mechanism and the Tate-curve example are published results, correctly credited. Frobenius fixedness of an extension class must be retained.

[Chiarellotto–Le Stum, Proposition 2.1.4](https://doi.org/10.1023/A:1000602824628) gives the full Gysin sequence, not merely exactness at H¹(U). Its smooth connected curve, nonempty affine open, and overconvergent-coefficient hypotheses hold: each proper smooth component meets a node, deleting these finitely many points gives a nonempty affine open, and the coefficient on the proper component can be treated as overconvergent. A sentence making these implications explicit was added.

All component/node identifications are over K after scalar extension. The node is k-rational, and the coefficient is defined on the special-fiber scheme without a logarithmic structure. General log coefficients with residues are excluded. The Frobenius-equivariant interpretation has the Tate twist; the audit accepts the stated underlying-vector-space formulas, not an untwisted Frobenius-equivariance assertion.

## Independent proof reconstruction

Write V=C1(E). The incidence map A records restrictions of component horizontal sections to common node fibers. On an oriented edge, a change of orientation changes both the incidence coordinate and the chosen residue coordinate by a minus sign. If S is the corresponding diagonal sign matrix, A changes to SA, D to DS, and R to SR. Thus im A intersect ker D is transported isomorphically and DA is unchanged. No doubled edge is introduced.

For a global class h, the two outward residues at a shared node are opposite. Component Gysin exactness therefore proves DR(h)=0. Conversely, for r in ker D, the same exact sequence produces component classes with their prescribed signed residues. On the overlap annulus their residues in one common orientation coincide, so their cohomology classes coincide because annular residue is an isomorphism. Mayer–Vietoris then lifts the compatible component tuple to a global class. This proves im R=ker D; no unjustified global residue-surjectivity assertion is needed.

Since j is injective, N(h)=0 is equivalent to R(h) in im A. Therefore R induces the isomorphism

    ker N / im i  ≅  im A ∩ ker D.

Restrict D to im A and use rank-nullity. Its image is im(DA), giving exactly rank A − rank(DA). In particular, DA is not asserted to be zero. In general D is not the transpose of A. The scalar constant-coefficient graph Laplacian argument remains legitimate because its matrices are rational; positivity is not being imported for arbitrary p-adic coefficient matrices.

## Cycle calculation and its scope

Under the stated componentwise trivial-connection hypothesis, horizontal changes of basis reduce n−1 transitions to identity and leave T on the closing edge. The displayed A and D equations are consistent: the closing residue is transported by T⁻¹ at vertex 1. Hence ker D consists of constant tuples (t,…,t) with Tt=t.

Let M=T−I. The sum map Wⁿ→W/(I−T)W kills im A. Conversely, choose a₁ solving (I−T)a₁=Σrᵢ, then recursively define aᵢ₊₁=aᵢ−rᵢ. The last equation follows exactly. This establishes the quotient without a dimension-only shortcut. On ker D the quotient map is t↦[nt]; n is invertible in characteristic zero, even when the residue characteristic divides n.

The resulting defect is ker M∩im M. The map M from ker M² onto that intersection has kernel ker M. Each Jordan block at 1 of size at least two therefore contributes one, not its size minus one. Blocks away from 1 contribute zero. These arguments work over K because the nilpotent generalized 1-eigenspace is defined over K. Conjugating T or replacing it with T⁻¹ preserves the condition.

The original phrase “the 1-eigenspace is semisimple” was imprecise: T already acts as identity on its ordinary 1-eigenspace. It was replaced by “eigenvalue 1 is semisimple,” with the precise condition ker M²=ker M. The main displayed theorem and Jordan-block criterion were already correct; this is a terminology correction, not a counterexample to them.

The audit does not turn arbitrary matrix examples into isocrystals. The classification applies to coefficient objects already satisfying the hypotheses. A compatible Frobenius structure, descent and realization are separate constraints. The published rank-two example supplies an actual nontrivial instance; the other matrices are explicitly algebraic diagnostics. Local triviality is an additional assumption, not an automatic property of all convergent F-isocrystals.

## Bounded literature and approach count

[Wu, Theorem 1.1](https://arxiv.org/abs/1511.08323) concerns the ordinary-coefficient slope [0,1) comparison in its finite-residue-field setting. [Binda–Vezzani, Section 4.5](https://arxiv.org/abs/2508.16196) distinguishes a constructed complex from exactness supplied under weight-monodromy. The inspected statements do not establish the unrestricted coefficient classification. This is a bounded scope check, not an exhaustive current-status or novelty certificate.

The packet enumerates exactly five disclosed approaches: source/prior-attempt reconstruction; residue factorization; component Gysin/rank reduction; cycle holonomy; and bounded later-literature/weight-theory inspection. STATUS.json records five used with a five-approach limit. There is no chronological research log in the packet, so a stronger historical assertion that no unrecorded approach occurred is not independently verified. The desk assessment is not counted as an actual prior proof attempt. Repository-search results are inherited bounded metadata, not fresh independently rerun searches by this auditor.

## Correction and acceptance

CORRECTION.patch gives every byte-level textual change to the six-file author payload. It makes two mathematical-precision edits in PROOF.md and updates audit-status metadata. The immutable original archive is preserved. The corrected six-file payload is supplied separately and also inside the independent audit archive.

Acceptance rests on the mathematical arguments above, supported by the recorded exact-rational diagnostics and strict inventory replay. Runtime tests do not prove the imported comparison or Gysin theorems. The original and corrected proof packets contain no executable entrypoint; code-entrypoint, hostile-import and package-cache controls therefore do not apply to their mathematical content. The separate validation/diagnostic runner was actually exercised normally, with optimization, and after relocation. Results and limits are recorded in ACCEPTANCE_REPORT.json.

No source PDF or extracted source text, corpus contents, private source, or private coordination file is included in either safe archive. Publication was not performed by this audit.
