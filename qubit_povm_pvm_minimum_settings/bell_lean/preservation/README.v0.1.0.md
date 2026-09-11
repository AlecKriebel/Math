# Minimum Bell-Setting Complexity — Lean source checkpoint

**PARTIAL PROOF-SOURCE DRAFT. LEAN COMPILATION AND KERNEL VERIFICATION HAVE NOT RUN.**

This is a formalization-in-progress of Alec Kriebel's *Minimum Bell-Setting Complexity for Qubit POVM–PVM Separation*, requested via DOI **10.5281/zenodo.21699161**. It is not a completed formalization of the paper and is not a certificate that the paper's principal theorems have been verified.

## Current evidence

| Layer | Result in this release |
|---|---|
| Written Lean sources | 114 theorem declarations in 10 source files, plus a generated dependency-audit file; **all uncompiled** |
| Static source audit | Passed: no `sorry`, `admit`, custom `axiom`, `native_decide`, `unsafe`, `implemented_by`, or `extern` tokens outside comments/strings in the audited source |
| Independent Python/SymPy checks | Passed: 122 exact algebra/finite checks; 1,215 rational transportation regression instances; 43,740 simulator probabilities compared |
| Lean build | **Not invoked:** the build wrapper exited 127 because `lake` is absent |
| Main two-input equality theorem | **Not proved in Lean** |
| Global physical PVM upper bound | **Not proved in Lean** |
| Complete paper formalization | **Incomplete** |

A theorem declaration with a tactic script is only a *proof attempt* until elaboration and kernel checking succeed. The static audit and Python checks do not change that fact. Even a future successful build of these files would establish only the written subset: it would not fill the missing main arguments.

## What has been written

`Bell/Quantum.lean` defines complex two-dimensional local Hilbert spaces, a four-dimensional joint density matrix, positive normalized POVMs, orthogonal projective measurements with zero projectors allowed, input-dependent finite output alphabets, the Born-rule behavior map, and separate raw and shared-randomness convexified behavior sets. The project uses Mathlib's actual `Matrix.PosSemidef` and `convexHull`, rather than surrogate predicates whose fields assume the desired conclusion.

`Bell/Witness.lean` gives the explicit physical strategy of Section 3.1, including rational Gram factorizations of the state and auxiliary effects and its Bell value. `Bell/Discrimination.lean` contains the ideal discrimination dual certificate and a proof script for its upper bound over arbitrary complex three-outcome qubit POVMs. `Bell/Scalars.lean` contains the strict numerical gap, the robust scalar inequalities, completion of the square, and the strengthened scalar comparison. The bridge from arbitrary physical PVM strategies to those scalar hypotheses is still missing.

`Bell/Lorentz.lean` contains universally quantified finite algebra: the five-ray circuit, outer-product independence, metric/null-polynomial identities, the quadratic map and generic inverse, base-locus calculations, exceptional-chart eliminants, and bilinear square completion. These are not the complete differential-geometric or exceptional-fiber proofs.

`Bell/Transportation.lean` contains the general real-parameter bounded-flow construction, including zero capacities. `Bell/LocalSimulation.lean` connects those flows to a single common-randomness mixture of actual identity-and-zero qubit PVM strategies and all four input blocks. The remaining geometric reduction of a general rank-zero incidence point to the normalized table is not included.

See [the coverage register](docs/COVERAGE.md) for precise boundaries and [the dependency blueprint](docs/BLUEPRINT.md) for the remaining work. The complete theorem-name inventory is `reports/declarations.json`.

## Main targets are deliberately unproved

`Bell/Targets.lean` defines the propositions `ProjectiveGlobalUpperBound`, `UniversalTwoInputEquality`, `OneInputEquality`, `StrengthenedAttainment`, and `MainClaims`. **A definition of a proposition is not a proof of that proposition.** No unconditional proof of any of these targets is supplied.

For example, `three_by_two_separation_of_projective_upper_bound` takes an explicit argument of type `ProjectiveGlobalUpperBound`. It must not be quoted as an unconditional formal proof of Theorem 3.1. Likewise, `main_claims_of_missing_theorems` is only conditional assembly with three unsolved premises.

## Reproduce and resume

The pinned versions are **Lean 4.19.0** and Mathlib commit **`c44e0c8ee63ca166450922a373c7409c5d26b00b`**, corresponding to Mathlib v4.19.0. This is a reproducibility pin, not a claim to use the latest release. The root `lake-manifest.json` was reconstructed from the retrieved upstream dependency manifest; Lake has not validated it in this runtime.

With the `elan` toolchain manager installed and available on `PATH`, the first unfinished computation is:

```bash
cd bell_lean
bash scripts/check.sh --bootstrap
```

This command retrieves dependencies/cache, attempts `lake build`, prints axiom dependencies for every inventoried theorem, and records results under `reports/`. Initial setup requires Internet access. Compiler binaries, Mathlib, and its compiled cache are **not bundled**. Consult the official installation documentation at <https://lean-lang.org/install/> for installing `elan`; the repository's `lean-toolchain` selects the compiler version.

The source is uncompiled: the first build may expose parser errors, API mismatches, tactic failures, or deeper statement/proof problems. Resolving those is an unfinished task, not merely an expected administrative step. Return the *first* failing module and its complete error log rather than adding placeholder proofs to force a green build.

The independent, non-Lean checks are reproducible separately:

```bash
python3 -m pip install -r requirements.txt
python3 scripts/exact_checks.py
```

The static source inventory can be regenerated without Lean or SymPy:

```bash
python3 scripts/source_audit.py
```

A GitHub Actions workflow is included but **has not been installed in a repository or executed**. Its successful outcome would certify only the written subset. The supplied build wrapper is fail-closed and permits only the standard axioms `propext`, `Classical.choice`, and `Quot.sound` in the printed theorem dependencies. That axiom audit itself has not run against Lean output.

## Source version and provenance

The Zenodo endpoint did not return the paper in this session. The included 34-page July 2026 PDF was retrieved from the author's Library and **SHA-256 matched** to `paper/main.pdf` in the original GitHub release:

- Repository: `AlecKriebel/Math`
- Tag: `qubit-povm-pvm-minimum-settings-v1.1.0`
- Directory: `qubit_povm_pvm_minimum_settings`
- SHA-256: `1a408e9d98f5166e8ffa6adf607413132facb51fa6f8d3108843b5f0280f2c66`

The later 35-page version found in the Library was not used. The hash match identifies the exact source used; it does not claim that a live Zenodo redirect was resolved. Full provenance is in `reports/source_provenance.json`. The source PDF is retained solely to make the intended theorem statements and version unambiguous.

## Trust and interpretation

The independent checks are newly written checks based on the paper, not a claimed replay of all original repository verifiers. They include exact symbolic identities as well as finite examples. In particular, 1,215 transportation examples are regression tests, not a proof covering arbitrary real input.

The Lean proof scripts attempt the corresponding universal statements where indicated in the coverage register. No raw-set equality, same-state measurement simulation, general operator-level PVM simulation, exact global Bell optimum, or stronger-strategy attainment is inferred from the current result. Formal statement fidelity must also be reviewed: a correct kernel-checked proof of the wrong model would not verify the paper.

A factor-of-two transcription error in the initial *new implementation* of the witness correlations was detected and corrected by the independent checks. The corrected correlations are `sqrt(2)/2, sqrt(2)/2, sqrt(2)/2, -sqrt(2)/2`, so the CHSH value is `2*sqrt(2)`. This was not a reported error in the paper.

This release is a resumable source checkpoint, not a publication-ready verification claim.
