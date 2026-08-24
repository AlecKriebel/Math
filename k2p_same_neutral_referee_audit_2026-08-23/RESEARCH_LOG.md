# Research log

## 2026-08-24T04:48:15Z - Audit opened

- Goal: independently referee the complete K2P-SAME article, supplement, proof,
  code, exact certificates, and reproducibility package under the protocol in the
  user request.
- Exact target claim: on binary standard semi-directed strongly tree-child level-2
  networks with strict inheritance and all K2P edges in
  `D_plus = {(s,g): 0<s<1, 0<g<1, g>2s-1}`, directed containment, structural
  equivalence modulo coherent ordinary-triangle redirection, and a shared
  full-dimensional physical regular analytic germ are claimed equivalent, with the
  stated generic identifiability, reconstruction, continuous-time, and weak-class
  sharpness consequences.
- Success criteria: each major theorem layer receives PASS, FAIL, or UNVERIFIED;
  load-bearing computer lemmas have a defined finite universe, predicate,
  certificate semantics, exhaustiveness argument, and independent attack; the
  required quick/full runs and clean builds either complete or have exact blockers;
  all findings are traceable to files, records, commands, and hashes.
- Boundary cases in scope include strict-domain limits, reticulation-adjacent edge
  operations, root movement, all theta event placements, restoration/probe
  transports, ordinary-triangle rank-nine germs, and weak-but-not-strong examples.
- Explicit exclusions are recorded as scope, not inferred theorem claims: mixed
  sign, stochastic boundary, singular edges, higher level, weak-class
  identifiability, numerical stability, bit complexity, and finite-sample inference.
- Environment: macOS 26.5.2 (Darwin 25.5.0), Apple M1 Pro, 10 logical CPUs,
  16 GiB RAM, arm64; system Python 3.14.6; Tectonic 0.16.9.
- Workspace state: branch `main`; unrelated pre-existing modifications and
  untracked files were observed and will not be altered.
- Isolation: copied the 420 MiB, 493-file handoff to
  `isolated_handoff/`; authoritative source folder remains untouched.
- Initial code inspection: `verify_handoff.py`, `test_handoff_mutations.py`,
  `build_handoff_manifest.py`, `build_handoff_archive.py`,
  `run_all_verifiers.py`, and `setup_environment.sh` read before execution.
- Completion estimate: **4%**. Provenance architecture is understood; no
  mathematical or computational claim has yet earned PASS.

## 2026-08-24T04:59:50Z - Printed quartet gate falsified

- Independent mathematical and computational tracks converged on the same
  coordinate-convention defect without sharing a derivation first.
- The article declares state/character order `(0,C,G,T)` and spectrum
  `(1,s,g,s)`, hence `C,T` are the equal Fourier sectors, but article
  equations (quartet-F/G) and `work/quartet_separation_closure/PROOF.md` use
  `G,T` as the equal pair.
- Exact symbolic pullback on `A=12|34` gives
  `q_GGGG-q_GGTT = g1*g2*(g3*g4-s3*s4)`, not zero in general.
- Exact strict continuous-time witness: every quartet edge has `s=3/4`,
  `g=3/5`. It satisfies `0<s,g<1`, `g>2s-1`, `g>s^2`, and all transition
  probabilities are positive, yet on `A` both printed separators equal
  `-729/10000`; the printed `F_A` is also negative on both crossing trees.
- The submitted low-level map independently agrees with this calculation.
- Replacing the formulas by the `C/T` analogues gives the claimed exact
  zero/positive pattern. Thus this is currently a false printed lemma and a
  missing algebraic-verifier defect, not yet a counterexample to the corrected
  central classification theorem.
- Current quartet replay checks only the abstract logic of seven nonempty split
  sets; it never evaluates the printed Fourier polynomials. All finite rows whose
  terminal semantics are "displayed-quartet separator" therefore remain
  computationally unsupported until coordinates are corrected and rebound.
- Independent artifact:
  `outputs/computational/quartet_coordinate_audit.json`, file SHA-256
  `c6517e0659df6a13a970e94af6b238dec02afb95e417f61bd06ebaf94b649017`,
  internal payload SHA-256
  `924508d6e0eb5095e3d3113f6809bfc82a7b0873732c974ad43b5342a4787e0b`.
- Completion estimate: **16%**. A proof/computational-completeness blocker is
  established; exhaustive replay and the remaining theorem layers are still in
  progress.

## 2026-08-24T05:03:21Z - Required quick replay completed

- Command: locked-environment Python with `-B`, `run_all_verifiers.py --quick`,
  wrapped by macOS `/usr/bin/time -l`.
- Result: exit 0; 21/21 harness stages reported PASS; wall time 778.96 s;
  maximum resident set size 1,460,994,048 bytes.
- Execution-ledger SHA-256:
  `76236eebb4900c2aa3b616470d5a15fd9de9228c3fe0a5cdc43bd472bc9ef2cd`.
- This establishes successful replay only. In particular, the quartet logic
  stage's PASS is now demonstrated not to validate its printed polynomial
  semantics.
- Completion estimate: **20%**. Quick reproducibility is evidenced, but the
  exhaustive primitive regeneration and most independent attacks remain open.

## 2026-08-24T05:05:37Z - Reviewer scratch contamination detected and removed

- A page-6 PNG rendered for visual inspection was mistakenly written below
  `isolated_handoff/tmp/pdfs/`. The outer manifest intentionally does not ignore
  that location, so an independent concurrent check detected one unexpected file
  (declared 492, actual 493).
- The scratch PNG was moved recoverably to this audit's ignored `tmp/pdfs/`
  directory; no submitted byte was edited or deleted.
- A first attempted recheck used the audit root as its working directory and
  exited 2 because `verify_handoff.py` is inside `isolated_handoff/`; this was a
  reviewer command error, not a package failure.
- Correctly rerun from `isolated_handoff/`, both `python3 -B verify_handoff.py`
  and `python3 -B build_handoff_manifest.py --check` exited 0, restoring the
  exact 492-file, 439,308,215-byte outer ledger and payload SHA-256
  `f56215708d3cb89b43108827fa588330e00c2aec7c3249c00dcf8c9a192c2c7d`.
- This incident is positive evidence that extra review-side files are detected;
  it is not a submission defect.

## 2026-08-24T05:26:50Z - Independent mathematical and structural audits converge

- The independent mathematical track completed all sixteen requested theorem
  layers.  It assigns PASS to the physical-domain, bridge-fibre, core/count,
  PC-PARTIAL-boundary, triangle-germ, and weak-sharpness arguments; FAIL to the
  literal quartet formula and its certificate semantics; and UNVERIFIED to the
  global equivalence and its genericity/reconstruction/continuous-time
  corollaries until the quartet binding is repaired.
- Three separate mathematical programs reproduce the convention mismatch, the
  exact rank-nine triangle blocks, and both weak-sharpness constructions.  The
  current official Englander version-4 PDF confirms that its theorem and
  proposition numbering are correct and that it uses the different G/T
  equal-sector convention.
- An independent finite-census streamer that imports no submitted generator,
  classifier, canonicalizer, or verifier reproduces the primitive count
  formula, raw-ID domains, all requested partitions, restoration forest shape,
  and all probe totals.  It explicitly treats these as structural checks rather
  than validation of the terminal algebra.
- A self-contained graph-to-Fourier/Jacobian replay reconstructs raw ID 97 and
  reproduces source rank 13, target rank 10, and both exact stored minors.
- The existing quartet verifier accepts two targeted semantic mutations—one to
  the declared spectrum and one to the printed coordinate labels—because it
  checks only abstract split-set logic.  This establishes a computational
  false-negative mechanism independent of checksums.
- Preliminary disposition remains **HOLD**: no corrected-theorem counterexample
  has been found, but a proof and computational-completeness blocker is exact.
- Completion estimate: **64%**.  The full required replay is running once and
  uninterrupted; provenance and final adversarial report review are still in
  progress.

## 2026-08-24T05:49:07Z - Provenance closed; independent mutation scope fixed

- The provenance/reproducibility track independently reconciled all 492 outer
  and 447 sealed inner rows, all five supplemental dependencies, both archive
  layers, all five manuscript sources, both PDFs, build reports, locks,
  crosswalk, and telemetry. Two clean outer archive builds are byte-identical
  to the distributed ZIP. The package provenance layer is PASS.
- The historical Englander PDF bound by the handoff was recovered with its
  exact claimed hash. A fresh official rendering differs only in 55 mutable
  metadata/identifier bytes; extracted text and all 31 page renders agree.
- A fresh incidence-graph audit reconstructed 196 direct labelled
  isomorphism/ordinary-triangle presentations without calling the submitted
  canonicalizer. A wholly independent all-universe canonical partition remains
  explicitly UNVERIFIED.
- The restoration mutation suite was freshly executed in a disposable copy:
  all 13 corruptions were rejected for the intended semantic reason (exit 0,
  66.46 s, peak RSS 569,540,608 bytes; report SHA-256
  `79645c56cc0b4689eafcd7abc5f78f7854dac694e32a5915c905f557e7f1e6c0`).
  The fresh probe suite and the single uninterrupted full replay are still
  running.
- The report now distinguishes fresh injections from frozen sealed mutation
  reports and leaves literal source/target reversal, inheritance-complement,
  domain-formula, sampled-for-symbolic, all-universe canonicalizer, and
  coherently resealed fabricated-triangle mechanisms as explicit unrun gates.
- Completion estimate: **88%**. The scientific disposition is stable at HOLD;
  the remaining work is execution closure, final report reconciliation, and
  release of the independent audit artifacts.

## 2026-08-24T06:40:23Z - Full replay and neutral referee report complete

- The single uninterrupted required full command completed with exit 0:
  22/22 harness stages PASS in 5,684.81 s, maximum resident set size
  2,034,221,056 bytes. The full-only 35-layer primitive-regeneration stage
  took 4,911.44 s. Fresh execution-ledger SHA-256:
  `7146e52b0708ba7f459d27a9125203a973aab614668486eb985c908f16bf64cf`.
- The full replay establishes reproducibility PASS but does not alter the
  independently demonstrated quartet semantic defect: its quartet gate still
  checks abstract split-set logic rather than the printed Fourier coordinates.
- Final scientific recommendation: **HOLD**. Mathematics HOLD; computational
  evidence FAIL; reproducibility PASS; human metadata/release HOLD. The global
  equivalence, genericity, reconstruction and continuous-time conclusions are
  UNVERIFIED pending the uniform C/T correction, formula-aware rebinding and
  resealing.
- An independent final consistency review checked all eight requested report
  sections, exact paths/hashes, fresh-versus-frozen mutation labels, command
  retention limits, and the separation of submitted and genuinely independent
  replayers. Reporting corrections did not change the scientific disposition.
- Final report: `reports/K2P_SAME_NEUTRAL_REFEREE_REPORT.md`, SHA-256
  `f320f1c27abbf7591870e6ba0208a2d9fd441f2a4e61e1e36a4757a8edbbb963`.
- Completion estimate: **100%**. The stated neutral-referee goal is complete;
  all remaining actions belong to a corrected submission or to human release
  choices.
