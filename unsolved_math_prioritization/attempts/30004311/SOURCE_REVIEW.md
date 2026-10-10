# Source and scope audit

## Exact question and original source

Problem 30004311 / OWR-17294-011: Ferran Cedó, “Finite simple left braces: constructions and problems,” in *Mini-Workshop: Algebraic Tools for Solving the Yang–Baxter Equation*, Oberwolfach Report 51/2019, DOI 10.4171/OWR/2019/51. The contribution occupies printed pages 3226–3228, PDF pages 20–22. Problem 9 is on printed page 3228 / PDF page 22.

Official public report: https://ems.press/content/serial-article-files/46831

Faithful restatement: must every finite nontrivial simple left brace with metabelian multiplicative group and abelian multiplicative Sylow subgroups admit an asymmetric-product presentation with both factors trivial?

All six substantive restrictions are retained: finite, nontrivial, simple, abelian additive group (a left brace), metabelian multiplicative group, and abelian multiplicative Sylow subgroups. The construction in [PROOF.md](PROOF.md) verifies each restriction and excludes every two-trivial-factor presentation by a brace-isomorphism invariant.

During the original source review, the official statement image was visually inspected and its surrounding contribution was read. The independent audit also read the contribution and visually inspected the exact problem. The source PDF, extraction and rendered image are not distributed.

## Framework and mathematical credit

1. Catino, Colazzo and Stefanelli introduced the asymmetric product of braces in “Regular subgroups of the affine group and asymmetric product of braces,” *Journal of Algebra* 455 (2016), 164–182. We use the definition as restated, with full admissible symmetric-2-cocycle scope, in Theorem 2.2 of source 3 below. We did not newly retrieve the original 2016 paper and do not claim a fresh inspection of it.
2. Bachiller, Cedó, Jespers and Okniński, “Asymmetric product of left braces and simplicity; new solutions of the Yang–Baxter equation,” https://arxiv.org/abs/1705.08493. The official abstract/version page was checked, and the paper is cited in the original OWR contribution. It develops the construction and interprets earlier examples. The original source review did not claim a fresh complete read of this paper. The independent audit additionally read §3, Theorem 3.1, its lambda formula and Lemma 3.2.
3. Cedó, Jespers and Okniński, “Every finite abelian group is a subgroup of the additive group of a finite simple left brace,” https://arxiv.org/abs/2001.08905. The original source review reread §2, particularly Theorem 2.2 and its lambda formula, in a previously retrieved copy. The general definition allows a normalized symmetric 2-cocycle; restricting a priori to bilinear cocycles would be an unjustified narrowing. The authored obstruction explicitly shows that two trivial factors force biadditivity. The paper's main result is an existence/embedding theorem, not a classification.
4. Cedó, Jespers and Okniński, “An abundance of simple left braces with abelian multiplicative Sylow subgroups,” https://arxiv.org/abs/1807.06408. The original source review reread §2 and the §3 construction, including Theorem 3.3. The 72-element positive control is explicitly a specialization of that construction and is not claimed new. The present construction uses the same useful cyclic orthogonal-action idea, with a higher nilpotency truncated-polynomial primary brace. We give direct operations, so no unverified general construction theorem is needed for it.

Radical-ring braces, finite semidirect products, truncated logarithm/exponential identities, the even-weight binary space and its quadratic refinement are standard ingredients. Their specific combination, its simplicity, and its universal obstruction are established by the authored proof. A mathematical conclusion is not a claim of historical priority.

## Corrections preserved

The 2018 paper's §2 corrects an older proof of the assertion that finite solvable A-groups are IYB groups. The invalid shortcut claimed a normal Sylow subgroup in every such group. That premise is false; the source gives A₄×S₃ as a counterexample. We do not use the shortcut. The positive control has precisely that group; the manuscript's Sylow proof instead uses an explicit direct product of semidirect products.

Cedó–Okniński, “New simple solutions of the Yang–Baxter equation and their permutation groups,” https://arxiv.org/abs/2401.12904v2, was reread at Theorem 4.5, Remark 4.6 and the opening of §5. Theorem 4.5 has a generally nontrivial factor A1; Remark 4.6 identifies two trivial factors only for a special previous family. Section 5 states that the older Theorem 4.12 had an incorrect proof and supplies a repaired family. None of these statements is imported as a universal classification. The official arXiv record still listed v2 of 8 June 2024 when checked on 10 October 2026 and notes corrected typos in Theorem 3.1. Theorem 4.5's source page was also visually inspected during the original source review. The independent audit read Theorem 4.5, Remark 4.6 and the opening of §5 separately.

## Independent inspection and historical metadata

[SOURCE_METADATA.json](SOURCE_METADATA.json) preserves the four recorded PDF byte counts and SHA-256 digests, public source titles and URLs, and the full independent inspection boundaries. The original question was inspected on printed page 3228 / PDF page 22. The general asymmetric-product definition and lambda formula were checked against Theorem 2.2 of arXiv:2001.08905, including a visual inspection of PDF page 3, and independently against Theorem 3.1 of arXiv:1705.08493. The latter was read through its official PDF without a new local PDF copy; no unrecorded local hash is supplied.

The historical independent mathematical checker used no author code or random tests. Its exhaustive factored identities, group-generator cross-checks, all 19,999 nonzero ideal-seed derivations, mathematical mutations and asymmetric-product boundary controls supplement the written proof. Public counts and the ideal-derivation stream digest are preserved as metadata; programs, raw outputs and generated certificates are not distributed. The full proof and every substantive independent audit finding appear in [PROOF.md](PROOF.md) and [MATHEMATICAL_AUDIT.md](MATHEMATICAL_AUDIT.md).

## Novelty and review limits

The primary source records and bounded historical searches do not establish a complete current literature history. No historical novelty or priority is claimed. The complete negative answer has been accepted by the accompanying independent mathematical audit with no required mathematical correction. This AI-assisted manuscript and audit are unrefereed; acceptance is not external human peer review, journal acceptance or proof-assistant certification.

All edition changes are editorial. The separate recognition theorem is unnecessary and is omitted; the audit supplies standalone arguments for every intrinsic cross-check retained here. Edition preparation rechecked frozen input bytes and publication integrity without new scholarly-source retrieval, source-text inspection, literature search or rerunning mathematical computations. Copied third-party source documents/text/images, datasets, programs, raw outputs, generated certificates and private coordination material are excluded. No theorem depends on those omitted artifacts.
