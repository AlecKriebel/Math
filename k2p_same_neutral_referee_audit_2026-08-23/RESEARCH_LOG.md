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
