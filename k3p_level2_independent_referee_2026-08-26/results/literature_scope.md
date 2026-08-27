# Independent novelty and literature-positioning audit

Audit date: 2026-08-26 (America/Los_Angeles). I checked the article's introduction, conventions, three-leaf geometry, Kimura-family comparison, scope, and full bibliography against primary papers, publisher/DOI records, arXiv/bioRxiv versions, and institutional research archives. A literature search cannot prove a universal negative, so conclusions labelled **inference** are novelty assessments rather than mathematical deductions.

## Bottom line

The principal novelty claim is **plausible and well differentiated from the verified prior work**. I found no prior primary source claiming a complete K3P containment classification for binary standard semi-directed strongly tree-child level-2 networks. In fact, the immediately preceding level-1 K3P paper, arXiv:2607.12919v3 (25 August 2026), explicitly lists lifting level-2 identifiability to K2P/K3P as open. The article's local K3P triangle contribution also appears genuinely new: prior work reports dimension evidence for the Klein-four three-sunlet and low-degree invariants for four-/five-sunlets, but I found no prior source giving the article's explicit irreducible eight-term quartic, equality of the three K3P orientation closures, or a common strict physical rank-14 germ.

The literature section nevertheless needs a **minor revision**. It omits a directly relevant June 2026 paper giving the complete semialgebraic geometry of the three JC triangle orientations, and it omits two recent peer-reviewed works that materially improve the level-2/higher-level positioning. The cross-Kimura synthesis also depends almost entirely on same-author companion manuscripts; that status should be made explicit, and the unarchived K2P companion should receive a durable citation before publication.

## Verified comparison claims

1. **Fourier/group-based background is correctly attributed.** The statement at `proof_package/manuscript/sections/01_introduction.tex:22-29` is consistent with Evans--Speed, DOI [10.1214/aos/1176349030](https://doi.org/10.1214/aos/1176349030), and Sturmfels--Sullivant, DOI [10.1089/cmb.2005.12.204](https://doi.org/10.1089/cmb.2005.12.204).

2. **The level-1 generic-identifiability summary is accurate.** Gross et al. prove generic identifiability for triangle-free level-1 semi-directed networks under JC, K2P, and K3P; see DOI [10.1007/s00285-021-01653-8](https://doi.org/10.1007/s00285-021-01653-8). Hollering--Sullivant cover cycle-network identifiability under K2P/K3P; see DOI [10.1016/j.jsc.2020.04.012](https://doi.org/10.1016/j.jsc.2020.04.012). These support the aggregate statement at `01_introduction.tex:31-35`.

3. **The three-sunlet dimension history is represented fairly.** Gross--Krone--Martin report computational deficiency for the Klein-four/K3P three-sunlet and identify it as an exceptional deficient case; see DOI [10.1007/s11538-024-01314-z](https://doi.org/10.1007/s11538-024-01314-z). Cox--Gross--Martin prove the odd-order dimension theorem and treat even-order cases computationally, including the Klein-four group; see DOI [10.1007/s11538-025-01506-1](https://doi.org/10.1007/s11538-025-01506-1). Thus `01_introduction.tex:35-38` is accurate. Their affine/tropical rank conventions include the normalizing coordinate; the article's normalized rank 14 is not a conflict with the prior affine rank 15 evidence.

4. **The multigraded-implicitization claim is accurate.** Cummings--Hollering state that the earlier four-leaf K3P degree-limited Groebner computation did not finish the cubics after 100 days, then compute 12 minimal quadrics and 64 minimal cubics for the four-sunlet and 648 minimal quadrics for the five-sunlet. See DOI [10.1016/j.jsc.2025.102459](https://doi.org/10.1016/j.jsc.2025.102459) and its [official MathRepo companion](https://mathrepo.mis.mpg.de/MultigradedImplicitization/). This supports `01_introduction.tex:39-43`.

5. **The comparison with Brits et al. is substantively correct.** Theorem 4.9 of arXiv:2607.12919v3 states that distinct level-1 semi-directed networks, modulo placement of reticulations in triangles, have disjoint physical models under JC, K2P, and K3P. Its parameter set requires stochastic positive-definite nonidentity transition matrices and nontrivial mixing, matching the article's principal-positive K3P edge domain. See [arXiv:2607.12919v3](https://arxiv.org/abs/2607.12919v3). This supports `01_introduction.tex:48-50`, and its Lemma 4.2 supports the more precise citation at `proof_package/manuscript/sections/05_three_leaf_geometry.tex:46-51`.

6. **The pre-existing level-2 claims are accurate.** Ardiyansyah studies only conditional distinguishability results for simple/semisimple nice level-2 networks ([arXiv:2104.12479](https://arxiv.org/abs/2104.12479)). Holtgrefe et al. address displayed quartets and inter-taxon quartet distances for galled outer-labelled-planar level-2 networks, not full K3P site-pattern containment (DOI [10.1007/s11538-025-01549-4](https://doi.org/10.1007/s11538-025-01549-4)). Englander et al. v4 prove generic JC identifiability for binary triangle-free strongly tree-child level-2 semi-directed networks and pointwise quartet tools under JC/K2P (bioRxiv DOI [10.1101/2025.04.18.649493](https://doi.org/10.1101/2025.04.18.649493); the bioRxiv API confirms v4 was posted 4 July 2026). This supports `01_introduction.tex:52-60`.

## Issues requiring repair

### LIT-1 — Directly relevant 2026 triangle paper omitted

- **Location:** `proof_package/manuscript/sections/01_introduction.tex:31-50`; `proof_package/manuscript/sections/15_kimura_perspective.tex:17-29`; absent from `proof_package/manuscript/references.bib`.
- **Severity:** minor revision, but substantively important literature context.
- **Dependency:** novelty/presentation only; no mathematical theorem depends on the omitted paper.
- **Evidence:** Currie et al., *Semialgebraic Conditions for Identifying Triangles in Phylogenetic Networks*, [arXiv:2606.26673](https://arxiv.org/abs/2606.26673), give a complete semialgebraic description of all three physical JC three-leaf triangle models. Their Lemma 3.4 and Theorem 3.5 show that each pair has a full-dimensional overlap while full-dimensional orientation-specific regions also exist. This is the closest published/preprint analogue to the article's distinction between common germ and equality of full stochastic images.
- **Repair:** cite Currie et al. beside the level-1 triangle discussion and explicitly contrast: JC orientations have ambient full-dimensional intersections and differences, whereas the claimed K3P common germ is relative to the codimension-one quartic `H_14` (`05_three_leaf_geometry.tex:104-180`). This would sharpen, rather than diminish, the K3P novelty.

### LIT-2 — Recent practical invariant paper omitted from the claimed computational landscape

- **Location:** `proof_package/manuscript/sections/01_introduction.tex:39-43`; absent from `references.bib`.
- **Severity:** minor.
- **Dependency:** literature completeness and motivation only.
- **Evidence:** Martin, Holtgrefe, Moulton, and Leggett, *Algebraic Invariants for Inferring 4-Leaf Semi-Directed Phylogenetic Networks*, *Systematic Biology* 75 (2026), 657--672, DOI [10.1093/sysbio/syaf071](https://doi.org/10.1093/sysbio/syaf071), develops and empirically tests four-cycle invariant inference under JC/K2P and explicitly reports that only degree-2 K3P invariants were obtainable by their elimination workflow, while crediting Cummings--Hollering for the K3P cubics.
- **Repair:** add one sentence after `01_introduction.tex:39-43` distinguishing practical four-cycle inference from the present exact three-cycle/local-to-global classification.

### LIT-3 — Higher-level tree-child positioning is incomplete

- **Location:** `proof_package/manuscript/sections/01_introduction.tex:52-59`; absent from `references.bib`.
- **Severity:** minor.
- **Dependency:** breadth of novelty comparison only.
- **Evidence:** Allman, Ane, Banos, and Rhodes, *Beyond Level-1: Identifiability of a Class of Galled Tree-Child Networks*, *Bulletin of Mathematical Biology* 87 (2025), 166, DOI [10.1007/s11538-025-01545-8](https://doi.org/10.1007/s11538-025-01545-8), proves identifiability for substantial galled tree-child classes, including arbitrary levels, from quartet concordance-factor data under gene-tree models. It does not subsume the present K3P site-pattern result, but it is directly relevant to the article's claim that strong tree-childness is a conceptual boundary.
- **Repair:** cite it as a complementary different-data result and state explicitly that it neither treats K3P displayed-tree site-pattern maps nor the present directed analytic-containment relation.

### LIT-4 — Cross-Kimura synthesis relies on same-author, not-yet-independent literature

- **Location:** `proof_package/manuscript/sections/01_introduction.tex:61-64`; `proof_package/manuscript/sections/15_kimura_perspective.tex:3-21`; bibliography `references.bib:199-237`.
- **Severity:** minor revision / confidence limitation, not a mathematical contradiction.
- **Dependency:** the assertions in the JC/K2P columns of the comparison table, and the claimed common sharp strong-tree-child boundary. It does not by itself refute the K3P theorem.
- **Evidence:** the JC item is a same-author dataset/manuscript archived 23 August 2026 at DOI [10.5281/zenodo.22064121](https://doi.org/10.5281/zenodo.22064121). The K2P item is a same-author GitHub snapshot dated 25 August 2026 with no DOI or journal/preprint identifier. The tree--theta item is likewise cited only by GitHub commit. These are accessible immutable commits, but they are not independent peer-reviewed corroboration.
- **Repair:** call them “same-author companion preprints/reproducibility packages” in the prose, avoid using “completed” in a way that implies established external consensus, and archive the K2P and tree--theta manuscripts with durable DOIs before publication. Retain exact version/commit identifiers.

### LIT-5 — Convention translation in the Brits comparison should be explicit

- **Location:** `proof_package/manuscript/sections/01_introduction.tex:48-50` versus the article's one-step convention at `proof_package/manuscript/sections/03_conventions_model.tex:16-24`.
- **Severity:** minor clarity issue.
- **Dependency:** only the claim that the two topology quotients “agree”; not the article's internally defined theorem.
- **Evidence:** Brits et al. define a semi-directed network by root suppression followed by exhaustive suppression of parallel edges and degree-two vertices (arXiv:2607.12919v3, Section 2.1), while this article expressly forbids later exhaustive cleanup. The quotients appear compatible after restricting/translating to the article's standard-admissible class, but that qualification is not stated.
- **Repair:** add “after translating conventions and restricting to standard-admissible presentations” (or prove a short equivalence lemma).

## Novelty assessment (inference)

- **Local K3P triangle geometry:** high plausibility of novelty. Prior primary literature verifies the one-dimensional deficiency and studies even-order tropical ranks, but I found no primary source predating this package with `F_{H_14}` or the common strict rank-14 germ claimed at `05_three_leaf_geometry.tex:104-180`.
- **Global K3P level-2 containment classification:** high plausibility, conditional on correctness of the manuscript's proof/certificates. The strongest external comparator (Brits et al. v3) explicitly describes lifting level-2 results to K2P/K3P as open; Englander et al. cover JC and exclude triangles. Searches found no competing K3P level-2 classification.
- **Weak-tree-child sharpness and exact dimension `6n-3`:** plausible but only moderately externally corroborated. I found no prior primary paper with this construction/dimension; absence of a hit is not proof of priority, and the closest precedents are the author's JC/K2P companion packages.
- **Exact reconstruction theorem:** the exact-real/RCF formulation is unusually strong and appears new in this network class, but its novelty is inseparable from the global classification and should not be marketed as a practical inference algorithm (`proof_package/manuscript/sections/02_main_theorems.tex:38-44` and `proof_package/manuscript/sections/16_scope.tex:30-36` already make the latter limitation clear).

## Recommended literature verdict

**Minor revision.** The novelty claims are credible and the cited comparisons I checked are materially accurate. The needed repairs are targeted: add the direct 2026 JC triangle paper, broaden the current higher-level context, explain the convention translation, and label/archive the same-author companion program more transparently. Overall confidence in this literature assessment: **0.86**. The confidence is below 1 because priority searches cannot establish a universal negative and three load-bearing comparison works appeared only within the three days preceding this audit.
