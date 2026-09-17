# Kernel checks, axioms, and reproducibility

The full verification command compiles the encoded statements and obtains Lean `#print axioms` reports for the explicitly named declarations in the inventory, including proof-bearing definitions and named instances. [CyclicBell/AxiomAudit.lean](CyclicBell/AxiomAudit.lean) contains the queries; [reference/expected_theorems.json](reference/expected_theorems.json) gives the expected names.

The only permitted foundational axioms are:

```text
propext
Classical.choice
Quot.sound
```

The current run status, source fingerprints, and evidence are indexed in [verification/README.md](verification/README.md). A failed or incomplete run is not certification. Counts in an inventory are not evidence that the corresponding reports were actually produced.

## Full verification

For installation, follow the [official elan instructions](https://github.com/leanprover/elan#installation), then run `elan toolchain install leanprover/lean4:v4.19.0`.

With Python 3.10+, Git, and Lean/Lake 4.19.0 available, run from the package directory:

```sh
python3 scripts/check.py --bootstrap
```

This uses the bundled [reference/manuscript/main.tex](reference/manuscript/main.tex). An optional `--manuscript /path/to/main.tex` checks a separate copy against the same pinned hash. `--bootstrap` fetches missing locked dependency revisions and their cache; it does not install Lean. Omit it when the required dependencies and cache are already present.

The full run checks compiler and dependency identities, validates the manuscript and source inventory, clears the companion's project build directory, and builds the imported library. The fresh build includes the mandatory axiom-query module; the runner parses its actual reports and requires exactly the expected declaration names and permitted axioms. It then runs the acceptance/rejection controls. Optional `--repeat-axiom-audit` reruns the query module separately and requires identical reports. Protected inputs must remain unchanged throughout the run.

The audit rejects missing or unexpected reports, duplicate query names, `sorryAx`, custom axioms, and native proof-evaluation trust. Static checks additionally look for admissions, unsafe substitutions, and unapproved compiler options. These checks supplement kernel elaboration and axiom inspection; they do not replace them.

For a lightweight static scan:

```sh
python3 scripts/check.py --static-only
```

That command does not run Lean and cannot establish kernel acceptance. `lake build` runs the ordinary library build but does not replace the full verification command's provenance and regression checks.

## What the controls establish

The [acceptance files](validation/) exercise intended physical and mathematical interfaces. The rejection controls test selected changes to normalization, source coefficients, conjugation, model domains, and table claims. A rejection counts only when Lean fails in the designated proof body. Missing imports, syntax errors, unknown names, process crashes, and resource exhaustion do not count as successful rejection.

These are regression controls. A failed proof attempt does not, by itself, prove the negation of its target proposition. Likewise, runner unit tests check the verification machinery rather than adding mathematical theorems.

## Trust and interpretation

A successful run establishes that the checked Lean statements have accepted proofs with the reported axiom dependencies, using the pinned toolchain and dependency artifacts. The trust base includes that compiler/kernel implementation, runtime, ordinary hardware and filesystem, and the upstream artifacts used by the build. This is not a from-source compiler bootstrap or verification by a second proof-assistant kernel.

The companion is rebuilt; use of the locked Mathlib cache does not mean that every dependency is rebuilt from source. Compiler success also does not decide whether an encoded definition matches a physical convention or a manuscript claim. That assessment requires reading the statements and constructions, guided by [REVIEWER_GUIDE.md](REVIEWER_GUIDE.md) and [COVERAGE.md](COVERAGE.md).
