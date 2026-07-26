# Research log: hostile simplicial-neighborhood audit

## 2026-07-26 06:03 PDT (13:03 UTC) -- scope freeze

- Target frozen for review:
  `math/lemmas/simplicial_neighborhood_reduction.md`.
- Target SHA-256:
  `87cdebc4177bf7703a53892f84d436c0a52eb5444a6b0ac14663284c0351b25a`.
- Target Git blob:
  `9a2e5589e4eca7b6716e4ef28d6a6a7252ea07a4`.
- The repository already had unrelated modified and untracked files.  They are
  outside this review's scope and will not be touched.
- Required model frozen: attacks only at unoccupied vertices; exactly one guard
  moves along one edge to the attacked vertex; all post-move configurations
  dominate.
- Preliminary clean-room proof audit found no defect in the equality collapse,
  well-coveredness step, nonempty family slice, exclusion of a simultaneous
  guard in `N(v)`, projected-family closure, or clique consolidation.
- Literature search begun with exact-phrase and concept queries.  A related
  same-model result is Klostermeyer--MacGillivray (2017), Proposition 11, on a
  single vertex covered by another closed neighborhood not being eternal-
  domination critical.  It is not the deletion of the whole `N[v]` used here.
- Added a standalone probe source in this folder.  It uses nauty `geng` only
  for graph6 instances and contains its own graph6 parser and parameter/game
  logic.

## 2026-07-26 06:12 PDT (13:12 UTC) -- exhaustive probe complete

- Exhausted all 13,598 nonempty unlabeled graphs of orders 1 through 8.
- The exact greatest-fixed-point one-guard solver found 694 graphs with
  `gamma=gamma_eternal`.
- Checked every one of 1,694 eligible simplicial vertices in 554 graphs.
  All parameter, well-coveredness, clique-partition, slice, exclusion, and
  projected-family checks passed.
- Directly discharged 27,923 projected state/attack obligations over 8,808
  projected states.  Each projected response was also lifted to a response in
  the original eternal family.
- Checked 5,413 independent target states, 36 empty-`Q` simplicial cases, and
  the stated minimum-degree consequences on all 3,314 connected graphs in the
  range with no simplicial vertex.
- There is no `gamma=gamma_eternal<theta` graph through order 8, so the finite
  counterexample-preservation check is vacuous; the corollary was audited
  analytically.
- Probe verdict: `PASS`.
- Deterministic artifact hashes:
  - `probe.py`:
    `fad436f80642cc1291616252aadbcb1244f2c1ae869bc62bbb46a9a87267226f`
  - `probe_result.json`:
    `cbfe53e601ce6753181ac2263b2a248fb85117c429191d7ec9bdadaca154eeb7`
  - nauty `geng`:
    `588052a87e5313f331aa145a0a641702b6c13b6e2387dd3c4807bf7f49fdaca1`

## 2026-07-26 06:17 PDT (13:17 UTC) -- proof and literature audit frozen

- Completed a line-by-line audit of Theorem 1 and both corollaries.  Defect
  counts are critical 0, high 0, medium 0, low 0.
- Rechecked the imported component-additivity argument in
  `math/reductions.md` (SHA-256
  `d2c899b68f0d2142c250dee26047af43d01e10d83a0ed112c289a14c3f3d5e13`);
  its count-vector slice correctly establishes the one-guard lower bound.
- Current primary-literature search located known static
  `alpha(G-N[v])=alpha(G)-1` and gap-critical no-simplicial results, plus a
  related one-guard single-vertex criticality result.  It located no source
  matching the combined arbitrary-family projection and parameter identities.
- The 2016 survey's superficially similar `G-N[v]` induction is explicitly for
  all-guards `m`-eternal domination and cannot be transferred without proof.
- Novelty remains unresolved because the directly relevant 2018 manuscript
  *On graphs with domination number equal to eternal domination number* was
  cited in a 2020 primary survey chapter but no inspectable copy was located.
- Wrote `REVIEW.md`.  Verdict:
  `ACCEPT -- proved in the stated one-guard model; no exact prior match
  located; novelty unresolved`.
- Confirmed the target hash is unchanged and the target has no review edits.
