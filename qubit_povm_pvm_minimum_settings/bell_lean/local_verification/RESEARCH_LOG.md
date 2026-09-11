# Local Lean verification research log

## 2026-09-11T01:41:03Z — import checkpoint (estimated completion: 5%)

Goal: kernel-check the paper’s actual complex-qubit, finite-output, shared-randomness equality and separation claims, including all dependencies, statement contracts and allowed-axiom audit. Success requires a real pinned Lean build without sorry/custom axioms and an independent correspondence review. Static or numerical checks alone do not qualify.

Imported 294 files from `bell_lean_mathematical_audit_20260910.zip` into the existing research program. SHA-256: `cbaa94b0f9b6c254dca19a8d4757600d53368b4747097d93d6e99c7ba1a851c5`. The archive’s integrity checker passed for 293 listed files before edits. Incoming documentation explicitly reports uncompiled source; it is evidence, not an instruction or certification.

Repository branch is main. Unrelated worktree changes are excluded. Installing the pinned Lean 4.19.0 toolchain. Independent audit families: (1) residual incidence/rank geometry and (2) physical interfaces, projective bound and paper correspondence. No external outreach. Exact remaining gap: all real compilation, proof repair, dependency checking and statement validation.

## 2026-09-11T01:48:05.842371+00:00 — compiler repair checkpoint (estimated completion: 12%)

Pinned Lean compiler successfully installed (full commit `6caaee842e9495688c1567e78c0e68dbb96942aa`); pinned Mathlib and 6,641 cache files acquired. Native cache executable hit macOS dyld DATA_CONST loader error; unmodified cache code succeeded via `lake env lean --run .lake/packages/mathlib/Cache/Main.lean get`. Initial all-module build exceeded practical memory with five concurrent umbrella Mathlib imports and was stopped after real Quantum errors. Narrowing imports removed unnecessary memory load.

Now actually built: Quantum, EntrywiseTopology, Expectation, Convexity, ProjectionSupport, Scalars, Transportation. Repairs include PSD lemma applications, explicit tensor arithmetic, matrix identity equality, and an explicit convex-weight identity. Renamed reserved lambda identifiers in ten files without changing meanings. Independent initial mathematical and interface audits found no counterexample on the stated hypotheses, but identified boundary conditions and scope correspondence still needing explicit review. No complete theorem, paper verification, or axiom audit is claimed. Exact remaining gap: the rest of the dependency graph and complete final build/contracts/axioms.

## 2026-09-11T01:54:49.660547+00:00 — geometric and separator checkpoint (estimated completion: 35%)

Actual module builds now include the arbitrary complex POVM witness, exact scalar separation, transportation and classical product distributions, finite convex compactness, projective-fiber injectivity and rank-one obstruction, uphill directions, incidence algebra, annihilator duality, Pauli coordinates, complex purification, SOS algebra, the complete rational LDL certificate, and universal projective SOS inequalities. Selected axiom audits (compactness, rank-one, certificate) contain only standard axioms. The matrix-state and physical probability definitions remain unchanged. Strongest verified result is these assembled partial chains, not main_claims. Main assembly, physical maximum reduction and remaining calculus are still pending.

## 2026-09-11T02:11:17.214871+00:00 — assembled physical/geometric checkpoint (estimated completion: 85%)

51/58 mathematical modules have actual local build outputs. Completed chains now include all incidence ranks, residual physical closure and coordinates, complex purification/steering, extrema/filtering, quantum compactness, physical global PVM bound and exact strengthened witness. The cone/circuit branch has also compiled. Remaining source assembly: ConeCompression, BinaryParty, SmallOutputEncoding, ResidualEncoding, ResidualStrategy, Assembly, SimulationCorollaries; full fresh runner and endpoint audits still required.

One intermediate helper had a genuinely missing implicit hypothesis: ternaryLabelMap_injective requires block-preservation hπ. The repaired theorem explicitly includes it; all callers derive it and the final simulation statement is unchanged. Independent auditors recorded a counterexample when that helper hypothesis is removed. A malformed grouped structure declaration was split into the two intended operator fields. No main claim gained premises.

The strengthened witness numerical proof triggered a recovered Matrix.cons_val simplifier PANIC despite Lean exiting zero. Replacing that simproc with explicit vector evaluation lemmas produced a clean successful rebuild. The runner now rejects PANIC as well as errors/sorry, interprets the unmodified cache program to avoid the macOS native loader bug, and snapshots both generated audit manifests. The 45 software control tests pass; these are not counted as theorem verification. Standalone development probes remain separate from actual production build evidence.

## 2026-09-11T02:21:46.891644+00:00 — complete production build (estimated completion: 95%)

All 58 production modules and the Bell umbrella compiled. Both original and independent supplementary physical statement contracts elaborated successfully. Original contracts needed explicit matrix construction for the tensor formula and an explicit natural-number reduction for the zero-input edge case; their meanings are unchanged. All exact preflight families and 45 runner control tests passed. Updated obsolete source comments to point to verification evidence. Production sources, contracts, and verifier are now frozen for a fresh serial rebuild and complete public-axiom audit. Remaining gap: one final run with unchanged fingerprints, independently checked receipt, publication documentation, and commit/push.

## 2026-09-11T02:34:22.003305+00:00 — complete fresh kernel run (estimated overall completion: 99%; mathematical verification: 100%)

Run `20260911T022153Z-2ea5f99b` passed all 58 fresh module builds plus Bell, both contract files (25 examples), all 675 public theorem dependency reports, compiler controls, and unchanged-source/dependency checks. All 123 command logs have matching hashes; the sole nonzero command was the intentionally rejected invalid proof. Standard axioms only. The paper artifact suite also passed. Exact remaining task: independent successful-receipt audit, final package hashes, final commit/push. No unresolved proof gap remains in the named certified conclusions; modelling and manuscript scope are explicit in CERTIFICATION.md.

## 2026-09-11T02:35:33.819693+00:00 — final publication checkpoint (formalization goal: 100%)

The full Lean run and all 31 independent receipt-consistency checks passed. All 88 protected inputs and 123 command-log hashes match. Certification, current status, 25 statement contracts, manuscript fingerprints, exact-check logs, and independent mathematical/verification reviews are complete. The original helper-premise correction and precise formal scope are documented. No unresolved gap remains in the named formalized conclusions. This checkpoint publishes the final source and evidence on main; no immutable DOI release or external outreach is requested or performed.
