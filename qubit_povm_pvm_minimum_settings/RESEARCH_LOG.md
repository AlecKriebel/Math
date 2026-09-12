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

## 2026-07-29 22:08 PDT — referee revision verified

- Completed the requested referee-facing expansion while preserving the
  theorem's exact scope: equality is asserted only for
  shared-randomness-convexified two-input behavior sets, not for raw strategy
  images or same-state simulations.
- Added the page-one Main Theorem, explicit proof bridges for the
  one-binary-party reduction, residual architecture, Lorentz incidence
  reconstruction, determinant multipliers, second variation, projective
  fibers, and rank-zero simulation, together with a theorem-to-artifact map.
- Updated the literature discussion and retained only qualified novelty
  language. The earlier \(3\times2\) phenomenon is identified as prior art.
- Revised the AI-use disclosure to state substantive use across the research
  workflow, the human-directed scope, author responsibility, independent
  checkability, and the absence of prior independent expert verification.
- Re-ran all exact checks under Python 3.14.6 and SymPy 1.14.0: eight artifact
  hashes, the exact separation certificate, all 39 closure checks, and the
  rank-zero simulator passed.
- Built warning-free 34-page publication and line-numbered review PDFs.
  Every publication page was rendered and inspected; representative first,
  middle, and final review pages confirmed clear continuous line numbering.
- Regenerated and clean-compiled the standalone arXiv source archive to the
  same 34-page manuscript.

## 2026-09-11T02:35:33.819693+00:00 — complete local Lean verification (goal completion: 100%)

Repaired the cloud Lean draft in `bell_lean/` and completed fresh pinned Lean 4.19.0 run `20260911T022153Z-2ea5f99b`: 58 production modules plus the umbrella, 25 expanded statement contracts, and 675 public theorem dependency audits passed. Only standard Lean axioms occur; no admitted proof or custom mathematical axiom was introduced. All main endpoints, finite complete-strategy simulation, 3×2 minimum-setting separation and strengthened Appendix B attainment are checked. The existing exact artifact suite also passed.

Independent adversarial reviews checked the mathematical interfaces, rank cases, manuscript correspondence, proof-dependency architecture and all final receipt/log/source hashes. See `bell_lean/CERTIFICATION.md` and its claim-to-theorem map for precise scope, repairs, trust assumptions and reproducibility. Main theorem hypotheses were retained; one intermediate permutation helper required its intended partition-preservation hypothesis. No outside individual was contacted, and no new GitHub/Zenodo release was created.

## 2026-09-12T04:17:26.963202+00:00 — Lean referee response (completion: 100%)

Corrected Definition 5.1: Lorentz signature is a separate requirement, not implied by positive ray pairings. Independent exact counterexample review and Lean probe confirm the issue; the existing physical Lean proof retains its invertible Gram-frame hypothesis and requires no repair. Clarified auxiliary coverage limits and fixed certificate evidence links to its original immutable run. Rechecked unchanged certified proof fingerprints, reran the independent matrix contract and exact artifact suite, and rebuilt/inspected both paper PDFs and the active source submission archive. Details: `referee_response_20260911/RESPONSE.md`.
