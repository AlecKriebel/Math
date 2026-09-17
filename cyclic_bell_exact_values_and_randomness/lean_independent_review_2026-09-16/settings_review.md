# Independent settings and review-tooling audit

Date: 2026-09-16 Pacific / 2026-09-17 UTC. Assigned source review complete (100%); machine replay recorded separately.

## Settings statement correspondence

I inspected the actual definitions and proofs in GeneralPhaseTables, GeneralPhaseBounds, GeneralAnchoredTables, GeneralPhaseEntropy, GeneralExposure and GeneralCoverageExposure against manuscript app:settings (main.tex:1898–1960). No scope or normalization mismatch was found.

- `GeneralPhaseTables.lean:31–45` constructs actual Alice/Bob phase PVMs on the normalized entangled state, not a stipulated probability table. Alice's negative Fourier sign and Bob's positive sign, including outcome inversion, are proved in the vector formulas at lines 79 and 91. Their actual Born amplitude is reduced to the geometric sum at line 101. The sine quotient is only asserted with a nonzero denominator; all standard and anchored cases discharge that condition. Normalization and uniform marginals are separately proved.
- `GeneralPhaseBounds.lean:107–123` uses offsets producing exactly the paper's displacement matrix (1/4, 3/4; -1/4, 1/4). `standard_behavior_formula` at line 168 states the physical table, and lines 185, 198, 232, 256 prove a universal entry bound, an attaining entry for every input pair, the strict excess over 1/d², and nonuniformity. Thus `standardPeak` is connected to the actual maximum; it is not merely an arbitrary definition named a peak.
- `GeneralAnchoredTables.lean:12` explicitly adds the third Bob PVM. The earlier tables are preserved, the matching table is delta/d, and the cross table is calculated at line 39. The maximum is bounded and attained. The strict gap is restricted to d≥3, and line 117 proves every entry is 1/4 for the exceptional qubit case. No impossibility theorem for arbitrary other third-setting constructions is claimed.
- `GeneralPhaseEntropy.lean:29` links the logarithmic expression to the proved physical table maximum; line 85 gives a literal sequential difference limit for the stated o(1) asymptotic. This is observed joint min-entropy, not conditional adversarial entropy. The proof treats the punctured sine limit correctly and is eventually restricted to d≥2, so Lean's total division/log definitions at small exceptional inputs cannot invalidate the asymptotic.
- `GeneralCoverageExposure.lean:74–96` identifies the real Hermitian Fourier/phase-Fourier coefficient system and proves the stated spectral obstruction. The formal statement applies to any unit diagonal phase rather than only the paper's half-step phase. Its eigenvalue premise and scalar-or-two-sided-spectrum conclusion match the paper. Line 136 proves the coefficientwise saturation consequence from actual state expectation and individual spectral caps. It does not silently generalize that obstruction to arbitrary joint Bell certificates.

## Valid alternative proof

The computational-MUB proof uses the elementary fact that a positive semidefinite matrix with zero diagonal is zero. Every operator in the relevant system has constant diagonal. A computational eigenvector fixes that diagonal to its eigenvalue; if this is a spectral extreme, subtracting from the scalar identity produces a positive semidefinite zero-diagonal matrix, hence the operator was scalar. This proves a stronger result than the paper's Toeplitz/SVD argument, so omission of those intermediates is not a gap in the proposition.

## Tooling and artifact integrity

- The archive was safely extracted and reviewed without editing its production sources.
- All 224 SHA256SUMS entries matched the archive bytes.
- The bundled manuscript TeX is byte-identical to canonical `cyclic_bell_exact_values_and_randomness/main.tex`, SHA-256 `82a47d69e43a4a3d18aa8c351b81cfae09c9a06910e85d91ae7daf120f201b71`.
- Active source and delivered archive source were compared: the sole packaging-file difference was SHA256SUMS, not mathematical code.
- Read the reproduction runner and static audit before executing. The runner deletes only the extracted project's build directory, verifies compiler commit and dependency revisions, recompiles the project including all axiom queries, and checks input preservation. Its controls distinguish proof failures from syntax/import/resource failures.
- 63 runner/tooling tests and 24 packaging tests passed. These verify the checking machinery, not the mathematical truth of the paper.
- A fresh project build reuses copied upstream Mathlib dependency caches with pinned clean source revisions, the normal Mathlib trust model. The Lean compiler and every upstream dependency artifact were not rebuilt from source. The final receipt makes the actual machine outcome explicit.

## Editorial inconsistency

`reference/paper_claim_ledger.json` row 26 still says no Qqa⊆Qqc theorem is claimed, while row 57 and GeneralCoverageClosureContainment supply that theorem. Row 44 similarly retains an old no-canonical-identification boundary while row 53 adds that bridge. These are stale scope descriptions, not proof failures; update or explicitly qualify them as statements about those individual older modules before sharing.
