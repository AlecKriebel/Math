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
