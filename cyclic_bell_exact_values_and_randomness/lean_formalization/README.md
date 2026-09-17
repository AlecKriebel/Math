# Cyclic Bell inequalities — Lean companion

This package accompanies **Exact Quantum Values and Permutation-Blind Maximizers in Cyclic Bell Inequalities**. It contains Lean proofs of the encoded value bounds, physical attaining strategies, permutation counterexamples, support rigidity, and related randomness and settings results.

Start with the [reviewer guide](REVIEWER_GUIDE.md) for a mathematical reading path and [coverage map](COVERAGE.md) for precise claims and boundaries. The current validation status and reproducible evidence are indexed in [verification/README.md](verification/README.md).

## Manuscript and source conventions

The package includes the [manuscript source](reference/manuscript/main.tex) and [PDF](reference/manuscript/paper.pdf). The pinned `main.tex` has SHA-256:

```text
82a47d69e43a4a3d18aa8c351b81cfae09c9a06910e85d91ae7daf120f201b71
```

The literal positive clock, forward shift, source coefficients, Bob transpose, and canonical polar construction are proved in the source-strategy modules. A useful first comparison with the paper is [GeneralSourceFourier.lean](CyclicBell/GeneralSourceFourier.lean), followed by [GeneralCoverageSourceStrategy.lean](CyclicBell/GeneralCoverageSourceStrategy.lean).

## Reproduce the checks

Requirements: Python 3.10+, Git, and Lean/Lake **4.19.0** on `PATH`. The [toolchain file](lean-toolchain), [Lake configuration](lakefile.toml), and [dependency lock](lake-manifest.json) fix the compiler and dependencies. Install [elan using its official instructions](https://github.com/leanprover/elan#installation), then install the pinned toolchain:

```sh
elan toolchain install leanprover/lean4:v4.19.0
```

From this directory:

```sh
python3 scripts/check.py --bootstrap
```

`--bootstrap` fetches missing locked dependencies and the Mathlib cache; it does not install Lean. Omit it when those dependencies and cached artifacts are already present. The full check validates the bundled manuscript, rebuilds the companion from a clean project build directory, runs acceptance/rejection controls, and inspects transitive axiom reports. See [AXIOMS.md](AXIOMS.md) for what these checks establish.

For lightweight checks without compiling Lean:

```sh
python3 scripts/check.py --static-only
```

For the ordinary library build alone:

```sh
lake build
```

To compare against a separate copy of the pinned manuscript, add `--manuscript /path/to/main.tex` to the verification command. A different manuscript hash requires a new correspondence review; it is not silently accepted.

## Package layout

| Path | Contents |
| --- | --- |
| [CyclicBell/](CyclicBell/) and [CyclicBell.lean](CyclicBell.lean) | Proof modules and library entry point |
| [validation/](validation/) | Positive interface examples and designated proof-rejection controls |
| [scripts/](scripts/) | Verification and inventory tools |
| [reference/manuscript/](reference/manuscript/) | Pinned manuscript source and PDF |
| [reference/paper_claim_ledger.json](reference/paper_claim_ledger.json) | Machine-readable manuscript-to-source map |
| [reference/source_inventory.json](reference/source_inventory.json), [reference/expected_theorems.json](reference/expected_theorems.json) | Declaration inventory and expected axiom-query names |
| [verification/](verification/) | Current verification status and retained evidence |

Lean checks the propositions actually encoded in the source. Assessing whether those definitions and hypotheses express the intended paper claims is a separate mathematical review. This companion uses alternative proofs for some claims and does not translate every prose calculation or external cited theorem; those boundaries are listed in [COVERAGE.md](COVERAGE.md).
