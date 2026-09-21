# Lean formalization of the qubit POVM–PVM minimum-setting result

Start with [CERTIFICATION.md](CERTIFICATION.md) for the current verification receipt, exact scope, and toolchain pins, and [the claim-to-theorem map](docs/CERTIFIED_COVERAGE.md) for the mathematical endpoints.

This development formalizes the arbitrary-finite-output two-input equality, finite shared-randomness projective simulation, minimum-setting classification, explicit 3×2 separation, and strengthened Appendix B attainment for Alec Kriebel's *Minimum Bell-Setting Complexity for Qubit POVM–PVM Separation*.

## Reproduce the complete check

With Lean/Lake available on PATH and network access for the pinned dependencies:

```sh
bash scripts/check.sh --bootstrap --serial
```

With the pinned environment already prepared:

```sh
bash scripts/check.sh --serial
```

The runner checks compiler identity and positive/negative controls, creates a fresh project build, compiles every mathematical module and `Bell`, elaborates every file under `validation/`, audits all public theorem dependencies, and verifies unchanged source and dependency fingerprints. See [OFFLINE_RUN.md](OFFLINE_RUN.md) for environment preparation and receipt interpretation.

For the separate exact algebra and verification-harness checks:

```sh
python3 -m pip install -r requirements-preflight.txt
python3 scripts/preflight_all.py
```

## Main sources

| Source | Purpose |
|---|---|
| [Assembly](Bell/Assembly.lean) | Unconditional main conjunction, arbitrary-output equality, minimum inputs |
| [SimulationCorollaries](Bell/SimulationCorollaries.lean) | Finite mixtures of complete PVM strategies and Bell-bound transfer |
| [ProjectiveBound](Bell/ProjectiveBound.lean) | Physical global projective bound and strict 3×2 separation |
| [StrengthenedWitness](Bell/StrengthenedWitness.lean) | Actual state and measurements attaining `(16+8√7813)/25` |
| [Quantum](Bell/Quantum.lean) | Complex qubits, density matrices, POVMs/PVMs, Born probabilities, convex hulls |
| [Original contracts](validation/Statements.lean) and [physical contracts](validation/PhysicalContracts.lean) | Expanded independent checks of definitions, quantifiers, exact values, and boundary cases |

Explicit operator-Hilbert, finite-label, and stochastic-output bridges are detailed in [MODEL_CONVENTIONS.md](docs/MODEL_CONVENTIONS.md).

The model permits mixed states, input-dependent finite output alphabets, unused labels, zero/identity projectors, and finite shared randomness selecting complete state-and-measurement strategies. Equality concerns the convexified behavior sets. The attained values are not claimed to be exact global POVM optima. The precise manuscript correspondence and modelling conventions are recorded in the certification and independent review.

## Evidence and provenance

The current run is identified by [reports/latest_run.json](reports/latest_run.json). Its kernel, statement, and dependency receipts and command logs belong to one run. Static reports deliberately retain `kernel_checked: false`: their own checks do not invoke Lean, even when the separate full run passes.

[local_verification/](local_verification/README.md) contains the research log, independent reviews, and development evidence. Historical cloud-stage status documents and nested archives are preserved and labelled as historical. Some development logs contain failures that were repaired; they are not the final verification result.

`SHA256SUMS.txt` certifies package byte integrity; it does not establish a theorem. Compiler binaries, dependency caches, build products, and Python virtual environments are excluded. No new immutable GitHub/Zenodo release is created by this verification work.
