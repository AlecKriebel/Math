# v1.0.8 independent core-mathematics rereview log

## 2026-08-23T20:44:56-07:00 — rereview opened (3%)

- Target: immutable tag snapshot `maximally-collective-stable-turing-v1.0.8` at commit `b4607c4cc9fe6931cedbbd0c5cd7e6e68a704f9f`.
- Baseline: independently verified v1.0.7 core findings in `independent_referee_audit_v1.0.7_2026-08-22/agent_core_math/`.
- Scope: inspect the tag diff without relying on disposition notes or stored `PASS` logs; independently check the revised `b=2a` SCC explanation, the displayed three-by-three determinant remainder, the generic cubic-recurrence verifier, theorem statements, and any central mathematical change.
- Source snapshot and live project are read-only. All new notes and controls stay in `agent_core_rereview/`.

## 2026-08-23T20:53:11-07:00 — mathematical diff reconstructed (68%)

- The extracted proposition/lemma/theorem/corollary environments in `main.tex`
  are byte-identical between v1.0.7 and v1.0.8.  No hypothesis, quantifier,
  endpoint, conclusion, or headline claim changed.
- The core proof changes are localized: the `b=2a` SCC paragraph now records
  that the deleted edge is in neither long cycle, and Supplement S2 now prints
  the lower-bidiagonal Schur complement instead of merely citing sparse
  expansion.  The remaining manuscript changes are functional-analytic detail
  and release metadata.
- Independently reconstructed the core Jacobian from the indexed reaction list.
  For `m=3,...,8`, exact Schur complements equal the displayed three-by-three
  matrix and have determinant `2*a**2*b`; exhaustive induced-set enumeration
  at generic parameters and `b=2a` found no SCC outside the claimed list.
- Read all 309 lines of `verify_generic_cubic_recurrence.py` before execution.
  It is genuinely symbolic in `m` and a formal harmonic sum and checks the
  local kernel identities, zero-mode and second-harmonic recurrences, boundary
  solve/determinant, interior arithmetic sum, cubic contraction, and gauge
  contraction.  It does not itself reconstruct the reaction list or prove
  domain/sign inequalities, so those remain human-proof dependencies.
- An independent reaction/Hessian reconstruction solved `w_0` and `w_2`
  exactly and matched `R_m+C_m*hfrak_m` at `m=3,4,5,8,12`, including the
  overlapping-index base case.  A separate symbolic derivation verified the
  generic recurrence and the only dimension-dependent product sum.
- Independently shifted and re-expanded `Q_m`, `P_R`, `P_C`, `L_m`, and the
  harmonic-bound numerator for `ell^T r`; every required coefficient was
  strictly positive, closing the all-dimensional cubic-sign step.
- Execution: the system Python 3.14.6 lacks SymPy and failed as expected; the
  pre-existing research environment Python 3.9.6/SymPy 1.14.0 ran the new
  verifier successfully (exit 0, about 0.66 s).  Optimized Python was rejected
  (exit 1).  A `+1` mutation of the claimed terminal numerator was rejected.
- Current best assessment: the v1.0.8 changes strengthen exposition and close
  the former finite-regression-only cubic bridge; no new core defect found.

## 2026-08-23T20:59:44-07:00 — rereview complete (100%)

- Wrote `CORE_REREVIEW.md`, `INDEPENDENT_CONTROL_RESULTS.md`, and the independent
  source `independent_v108_core_controls.py`.
- Rechecked the four target-source hashes after all work; they remain identical
  to the immutable v1.0.8 tag blobs.  Neither `source_snapshot` nor the live
  project was modified.
- Final assigned-core verdict: independently verified; no v1.0.8 mathematical
  defect and no theorem-statement change.  The SCC and Schur revisions are
  correct expository strengthening.  The new cubic verifier is a genuine exact
  generic identity bridge with clearly stated limits, not a finite regression
  and not a stand-alone nonlinear theorem proof.
