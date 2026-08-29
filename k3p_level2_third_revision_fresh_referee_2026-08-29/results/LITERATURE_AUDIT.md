# Literature and novelty audit

**Audit date:** 2026-08-29
**Package audited:** `/Users/alec/Documents/Math/k3p_level2_third_revision_referee_final_2026-08-29`
**Scope:** the comparison and priority claims in
`proof_package/manuscript/sections/01_introduction.tex:22-105`, the
same-author comparison in
`proof_package/manuscript/sections/15_kimura_perspective.tex:3-41`, and the
corresponding entries in `proof_package/manuscript/references.bib`.

## Verdict

**PASS — no mandatory literature or novelty correction.**

The related-work claims are accurately scoped, and a bounded search of current
primary sources found no obvious priority conflict that subsumes the stated
K3P theorem.  In particular, I found no prior primary paper proving the same
complete directed-containment classification for binary standard
semi-directed strongly tree-child level-2 networks under K3P, nor a prior
paper giving the same explicit K3P triangle quartic together with its strict
physical smooth-germ statement and the all-$n$ weak-class sharpness family.

The manuscript also avoids an absolute “first-ever” claim.  Its most delicate
priority sentence, `01_introduction.tex:35-53`, correctly separates facts
already in the literature—the K3P three-sunlet dimension defect and equality
of the three triangle-orientation ideals—from the exact refinements claimed
here.

This is a bounded calibration, not a proof of worldwide priority.  Searches
were made on official journal pages, arXiv, and bioRxiv using combinations of
“K3P,” “Kimura 3-parameter,” “level-2,” “strongly tree-child,” “weakly
tree-child,” “3-sunlet,” “triangle,” “quartic,” “rank 14,” “6n-3,”
“containment,” and “identifiability.”  No
secondary literature was used as evidence for the conclusions below.

## Claim-by-claim reconciliation

### 1. Level-one and triangle background

- **`01_introduction.tex:31-35` — accurate.** Gross–Long proves generic
  identifiability for the JC model on large single-cycle networks;
  Hollering–Sullivant extends cycle-network identifiability to K2P and K3P;
  Gross et al. proves generic identifiability for triangle-free level-1
  networks under JC, K2P, and K3P. These are appropriately summarized as
  broad level-one invariant/Jacobian results rather than as a solution to the
  present level-two problem.

  Primary sources:
  [Gross–Long 2018](https://epubs.siam.org/doi/10.1137/17M1134238),
  [Hollering–Sullivant 2021](https://arxiv.org/abs/1909.13754), and
  [Gross et al. 2021](https://link.springer.com/article/10.1007/s00285-021-01653-8).

- **`01_introduction.tex:35-38` — accurate and carefully qualified.** Gross,
  Krone, and Martin report the exceptional K3P three-sunlet deficiency in
  their computational table, while their proved general dimension theorem is
  for triangle-free level-1 networks. Cox, Gross, and Martin prove the
  three-sunlet dimension formula for finite abelian groups of odd order at
  least five and treat even-order groups computationally; their paper
  explicitly says the even-order proof remains open.

  Primary sources:
  [Gross–Krone–Martin 2024](https://link.springer.com/article/10.1007/s11538-024-01314-z)
  (Discussion and Table 1) and
  [Cox–Gross–Martin 2025](https://link.springer.com/article/10.1007/s11538-025-01506-1)
  (Theorem 1.1 and Section 4).

- **`01_introduction.tex:39-43` — accurate.** Currie et al. gives complete
  semialgebraic descriptions of the three oriented three-leaf JC triangle
  models and proves full-dimensional pairwise intersections and set
  differences. The manuscript correctly calls that a close JC analogue, not a
  K3P result.

  Primary source:
  [Currie et al. 2026, arXiv v1](https://arxiv.org/abs/2606.26673v1).

- **`01_introduction.tex:44-48` — accurate.** Cummings–Hollering computes all
  twelve quadratic and sixty-four cubic minimal generators for the four-leaf
  K3P sunlet, and all 648 quadratic generators for the five-leaf K3P sunlet.
  It also reports that the earlier degree-limited four-leaf cubic Gröbner
  computation had not terminated after 100 days. The manuscript does not
  incorrectly attribute a three-leaf quartic to this paper.

  Primary source:
  [Cummings–Hollering, official arXiv text](https://arxiv.org/html/2311.07678)
  (Theorems 3.3–3.4).

- **`01_introduction.tex:48-53` — accurate, with an important calibration
  already present in the text.** Gross et al. explicitly states that the ideals
  of all three three-leaf semi-directed triangle orientations are identical.
  Gross–Krone–Martin's computed deficiency already foreshadows the normalized
  dimension/rank value. Consequently, the numerical value “14” alone is not a
  wholly new observation. The current wording properly identifies the new
  *exact local refinements* as a certified rank theorem, an explicit
  irreducible eight-term defining quartic, and a common strict smooth physical
  germ. I found no primary source among the nearby papers that states those
  latter two results.

  Primary sources:
  [Gross et al. 2021](https://link.springer.com/article/10.1007/s00285-021-01653-8)
  (the paragraph immediately before Lemma 1) and
  [Gross–Krone–Martin 2024](https://link.springer.com/article/10.1007/s11538-024-01314-z)
  (Discussion and Table 1).

- **`01_introduction.tex:54-58` — accurate.** Brits et al. v3 proves full
  pointwise identifiability of level-1 semi-directed networks modulo triangle
  redirection under JC, K2P, and K3P on its stated probabilistic parameter
  domain. Its definition uses exhaustive suppression, so the manuscript's
  convention-translation and standard-admissibility qualifiers are material
  and should be retained.

  Primary source:
  [Brits et al. 2026, arXiv v3](https://arxiv.org/html/2607.12919v3)
  (abstract, Sections 2.1 and 4).

### 2. Level-two and practical-inference comparisons

- **`01_introduction.tex:60-63` — accurate.** Ardiyansyah proves only
  conditional distinguishability statements for restricted “nice” simple and
  semisimple level-2 networks, with explicit assumptions on reticulation
  leaves or branches. Holtgrefe et al. reconstructs a canonical form for
  outer-labeled planar, galled, level-2 networks from displayed quartets. These
  are genuinely complementary partial results and do not amount to the present
  K3P containment classification.

  Primary sources:
  [Ardiyansyah 2021](https://arxiv.org/html/2104.12479) (Introduction and
  Theorems 6.13–6.16, 7.6–7.9) and
  [Holtgrefe et al. 2025](https://link.springer.com/article/10.1007/s11538-025-01549-4)
  (Theorem 5.5).

- **`01_introduction.tex:63-68` — accurate.** Englander et al. proves generic
  identifiability under JC for binary, triangle-free, strongly tree-child
  level-2 semi-directed networks. It separately proves model-set disjointness
  under JC and K2P when networks have different displayed quartet sets, so
  “pointwise displayed-quartet tools” is fair. It does not prove the K3P
  theorem here, and its main level-two theorem excludes triangles. Thus the
  manuscript's statement that removing triangle-freeness and classifying the
  triangle ambiguity is part of the present advance is well calibrated.

  Primary source:
  [Englander et al., current bioRxiv record](https://doi.org/10.1101/2025.04.18.649493)
  (main abstract and displayed-quartet theorem).

- **`01_introduction.tex:69-72` — accurate.** Martin et al. develops a
  four-taxon invariant method for JC/K2P, tests it on simulated alignments, and
  applies it to Xiphophorus data. Its target is finite-data inference of
  four-leaf four-cycle networks, not exact K3P level-two containment.

  Primary source:
  [Martin et al. 2026](https://academic.oup.com/sysbio/article/75/4/657/8285810).

- **`01_introduction.tex:72-79` — accurate.** Allman et al. works with quartet
  concordance factors under gene-tree/coalescent models and proves results for
  explicitly restricted galled tree-child classes, including arbitrary-level
  and nonplanar cases under stated genericity, sampling, and small-cycle/blob
  conditions. The manuscript correctly says its data, model, and topology
  assumptions differ and do not subsume displayed-tree K3P site-pattern
  containment.

  Primary source:
  [Allman et al. 2025](https://link.springer.com/article/10.1007/s11538-025-01545-8).

### 3. Same-author companions and the main novelty claim

- **`01_introduction.tex:79-93` and
  `15_kimura_perspective.tex:3-8,34-41` — appropriately disclosed.** The JC,
  K2P, and tree–theta items are repeatedly labeled “same-author” and
  “unreviewed,” and the paper explicitly denies that they are independent
  corroboration. The article uses them for provenance and comparison, not as
  outside validation. This is the correct treatment.

- **`01_introduction.tex:95-105` — no obvious priority conflict found.** The
  closest primary results split into non-subsuming pieces:

  1. level-one K3P identifiability and triangle redirection (Gross et al.;
     Brits et al.);
  2. a computational K3P three-sunlet dimension defect (Gross–Krone–Martin);
  3. odd-order three-sunlet dimension theory and even-order experiments
     (Cox–Gross–Martin);
  4. restricted level-two group-based distinguishability (Ardiyansyah);
  5. triangle-free level-two identifiability only under JC (Englander et al.);
     and
  6. quartet/gene-tree canonical-form results under different data and model
     assumptions (Holtgrefe et al.; Allman et al.).

  None of these states the article's complete K3P directed-containment
  classification on the strong class, its physical triangle-germ theorem, or
  its claimed sharp weak-versus-strong boundary family.

## Bibliographic metadata checks

The entries that carry substantive comparison claims were reconciled against
their official records. I found no material metadata error.

- `references.bib:49-121` matches the official DOI records for Gross–Long,
  Hollering–Sullivant, Gross et al., Cox–Gross–Martin,
  Gross–Krone–Martin, and Holtgrefe et al.
- `references.bib:150-175` correctly records the original 2025 bioRxiv posting
  year for Englander et al. while noting the 4 July 2026 v4 revision, and
  correctly records Brits et al. v3 as 25 August 2026.
- `references.bib:177-228` matches the official journal/arXiv records for
  Cummings–Hollering, Currie et al., Martin et al., and Allman et al.
- `references.bib:230-239` correctly identifies Ardiyansyah's arXiv v1.
- `references.bib:241-284` labels the author's own materials as unreviewed
  companions and supplies immutable version/commit information; these entries
  should not be counted as independent literature, and the prose does not do
  so.

## Calibration to preserve in later revisions

No edit is required, but two qualifications in the current draft are
load-bearing and should not be weakened:

1. Do not recast the local novelty as the first observation of normalized
   rank 14. Prior work computationally records the corresponding K3P
   three-sunlet defect. The defensible novelty is the exact certification,
   explicit irreducible quartic, strict physical smooth germ, and its role in
   the complete level-two classification.
2. Keep the convention-translation and standard-admissibility qualifiers in
   the comparison with Brits et al.; its exhaustive cleanup convention is not
   literally identical to the manuscript's one-step root-suppression
   convention.

Subject to those already-present qualifications, the literature framing and
novelty claims pass this audit.
