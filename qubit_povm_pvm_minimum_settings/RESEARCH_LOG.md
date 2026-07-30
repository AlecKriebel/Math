# Research log

## 2026-07-29 20:14 PDT — publication production started

- Began a dependency-complete publication package for the fixed-qubit
  POVM-versus-PVM minimum-setting theorem.
- Frozen mathematical sources:
  - Phase-I separation and reduction artifacts supplied in the research
    staging archive and copied into this package where proof-critical;
  - residual closure release in commit `49c75ca5d658f030f8b8d3af640254e2d0913df6`.
- Governing editorial decisions:
  - state equality only for shared-randomness-convexified behavior sets;
  - do not claim equality of individual POVMs and PVMs;
  - do not claim either exact global optimum for the displayed `3 x 2`
    Bell functional;
  - omit the proposed private-randomness entropy corollary unless an
    adversarial extension is proved separately;
  - use conservative priority language and no unverified “first” claim;
  - keep numerical discovery code outside the exact proof path.
- Started parallel proof, reproducibility, and literature audits.

## 2026-07-29 20:29 PDT — theorem and verifier audits closed

- Consolidated the exact \(3\times2\) separation, one-binary-party theorem,
  residual-architecture reduction, and Lorentz-incidence closure into one
  self-contained manuscript.
- The adversarial proof audit found no unresolved load-bearing mathematical
  dependency. Publication-facing repairs were incorporated for zero effects,
  deterministic postprocessing, incidence-manifold dimension, tangent
  integration, multiplier signs, and exceptional fibers.
- Built an offline verification suite with byte-checked source artifacts and
  a pinned SymPy version. A clean run from outside the repository passed the
  separation, closure, and rank-zero checks in 7.28 seconds.
- Preserved the distinction between exact certificates and human proof:
  executable checks cover encoded identities and constructions, not the
  complete quantified convex-geometric argument.

## 2026-07-29 20:43 PDT — publication candidate frozen

- Completed a current primary-source priority and Bell-equivalence audit.
  The \(3\times2\) qualitative phenomenon is prior art; the defensible
  contribution is the arbitrary-output \(2\times2\) closure, the resulting
  minimum-input classification, and the exact rational certificate.
- Added a 22-entry audited BibTeX database and manuscript citations for the
  closest separation, simulability, dichotomic-reduction, finite-dimension,
  and zero-effect-corrigendum literature.
- A final manuscript-specific proof pass found one overbroad smoothness
  statement and four smaller definition/boundary issues. All were repaired,
  and the recheck passed.
- Compiled a 24-page warning-free PDF. Rendered and inspected every page;
  repaired the threshold and rank-trichotomy figures and checked all figures
  in grayscale.
- Built and clean-compiled `submission/arxiv_source.tar.gz`.
- Overall release assessment: **READY, NEEDS EXPERT SCRUTINY**. No independent
  expert human review or journal/arXiv submission has yet occurred.
