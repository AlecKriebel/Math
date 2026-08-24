# Independent mathematical referee log

## 2026-08-23 21:25 PDT — intake checkpoint

- Read `START_HERE.md` and mapped the current article, supplement, five declared TeX/Bib inputs, theorem–artifact crosswalk, and proof-compression tree.
- Review stance: all stored PASS reports, hashes, and certificate summaries are assertions; mathematical status will be based on deductions, inspected semantics, and independently reproducible checks.
- Submission tree remains read-only. Notes are being written outside `isolated_handoff`.
- Estimated completion toward the mathematical-review assignment: **5%**.

## 2026-08-23 22:20 PDT — analytic checks and first adversarial finding

- Independently derived the inverse Fourier inequalities, closure and surjectivity of paired serial products on `D_plus`, the strict continuous-time power-root sections, and both principal/continuous-time simultaneous bridge-gluing inequalities.
- Independently expanded the three-sunlet map.  The printed `T_i` factorization is exact.  Independently differentiated the symmetric triangle witness and reproduced the displayed `4x4` and `5x5` blocks and determinants `-1/2` and `-1/4`.
- Found a convention-sensitive counterexample to the *printed quartet polynomial lemma*: the article declares edge spectrum `(1,s,g,s)`, hence `{C,T}` is the equal sector, but prints separators using `G,T`.  On a `12|34` tree, `q_GGGG-q_GGTT` is generally nonzero.  A strict continuous-time example with pendant pairs `(1/2,1/2),(1/2,1/2),(1/2,1/3),(1/2,1/2)` gives `1/24-1/16=-1/48`.  The cited Englander paper uses the different convention `a_G=a_T`; uniform relabelling gives the correct local formulas `q_CCCC-q_CCTT` and `q_CCCC-q_CCTT-q_CTTC+q_CTCT`.
- The graph-level implication “different displayed-quartet sets have disjoint images” appears salvageable by this relabelling, but the submission's literal proof and its purported exact certificate semantics are not correct as written.  The existing quartet replay checks only the seven-set logic after assuming the sign theorem; it does not symbolically check the Fourier formulas.
- Independently regenerated the weak-sharpness common tensor from the two rooted arc lists, with no atlas import; reproduced both normalized tensors, the common strict continuous-time tensor, the named nine-column minors and exact determinants, and the rooting censuses `(5,2,3)` and `(7,2,5)`.  Pairwise labelled leaf distances already rule out underlying-graph isomorphism, hence also triangle equivalence.
- Estimated completion toward the mathematical-review assignment: **42%**.

## 2026-08-23 22:16 PDT — global proof and finite-boundary checkpoint

- Completed adversarial checks of the bridge fibre, semialgebraic localization,
  fixed-full restoration quantifiers, cycle/theta reduction, no-omnian repair
  table, completion-count formula, triangle contextual gluing, both global
  implications, genericity, exact reconstruction, and continuous-time
  transfer.
- Independently reproduced the minimal repair transversals and the per-core
  completion subtotals [7,100,100,416,208],
  [9,210,210,1036,518], and [11,392,392,2240,1120].
- No additional analytic counterexample was found.  The global theorem is
  logically sound conditional on a corrected quartet binding and the exact
  finite classification.  Genericity, reconstruction and continuous-time
  transfer introduce no further gap, but inherit those open premises.
- Estimated completion toward the mathematical-review assignment: **82%**.

## 2026-08-23 22:21 PDT — independent artifacts and literature checkpoint

- Preserved three independent scripts and deterministic JSON outputs under
  scripts/mathematical/ and outputs/mathematical/.  They use no submission
  module, atlas, canonicalizer or stored certificate.
- The quartet program symbolically confirms the false printed pullback and
  the corrected C/T formulas.  The triangle program reconstructs the map and
  exact 4x4/5x5 blocks.  The weak-sharpness program independently enumerates
  rootings, switching tensors, named Jacobian minors, graph distances and the
  cherry determinant.  All checks finished in under one second each.
- Retrieved Englander et al. version 4 from the official bioRxiv version API
  and PDF.  PDF p. 10 explicitly uses a_eG=a_eT; p. 12 gives Propositions
  2.9–2.10 and equations (2)–(3); pp. 12–13 give Theorem 2.11 and Corollary
  2.12; p. 22 repeats the Proposition 2.10 calculation.  This verifies the
  external attribution and localizes the error to the submission's failed
  specialization.
- Draft mathematical verdict: **HOLD**, with >99% confidence in the concrete
  convention defect and 90% confidence that repair, rather than rejection,
  is scientifically appropriate.
- Estimated completion toward the mathematical-review assignment: **96%**.

## 2026-08-23 22:23 PDT — final checkpoint

- Re-ran all three independent mathematical producers from their preserved
  sources.  Observed the expected defect/PASS/PASS sentinels and byte-stable
  JSON hashes.
- Completed the claim matrix, exact locations, theorem-dependency analysis,
  confidence assessment, literature comparison, and minimal repair/reseal
  instructions in notes/mathematical_review.md.
- Final recommendation from this track: **HOLD**.  No central-theorem
  counterexample was established; one false load-bearing specialization and
  its missing semantic replay must be corrected before acceptance.
- Estimated completion toward the mathematical-review assignment: **100%**.
