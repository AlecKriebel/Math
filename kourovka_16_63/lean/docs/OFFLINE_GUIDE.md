# Offline compilation and continuation guide

This is a mathematically incomplete formalization draft. Local execution on
18 September 2026 exposed compiler errors and resource problems. The local
audit repaired and compiled the existing source. Consult the current verification
report and run logs for the precise acceptance and trust scope.
A successful current-source build does not prove the absent final group theorem.
Network access is used only when the requested bootstrap/cache operations need it.

## 1. Restore the pinned environment

Have `lean` and `lake` for Lean 4.19.0 on PATH, plus Python 3.10+ and Git. The
runner checks the reported version and pins each dependency. It refuses to reset
an existing dependency checkout at the wrong revision or with tracked or
untracked changes. Ignored Lean source outside normal `.lake` artifacts is also
rejected to prevent source shadowing.

From `kourovka_16_63/lean/`:

```sh
python3 scripts/check.py --bootstrap --cache --module Kourovka.Parameters
```

`--bootstrap` fetches the exact revisions in the source-derived manifest;
`--cache` explicitly allows the matching Mathlib cache. These options do not
mean all upstream dependencies were compiled from source. A dependency build or
cache may require ordinary upstream build tools.

The runner's per-command default timeout is 3600 seconds, an operational guard,
not a measured required time. It can be changed with `--timeout`. Each project module is compiled serially with `lean -j1`; a timeout kills the
whole child process group, including a Lean process spawned by Lake. It does not
launch remote jobs.

## 2. Compile meaningful slices in dependency order

A suggested debugging sequence is:

```sh
python3 scripts/check.py --module Kourovka.Linear.Basis
python3 scripts/check.py --module Kourovka.Ambient.Lie
python3 scripts/check.py --module Kourovka.Flag.Rigidity
python3 scripts/check.py --module Kourovka.Lattice.Integral
python3 scripts/check.py --module Kourovka.Lattice.IntegralGeneration
python3 scripts/check.py --module Kourovka.Finite.PadicQuotient
python3 scripts/check.py --module Kourovka.Finite.Nilpotency
python3 scripts/check.py --module Kourovka.Finite.LieAutomorphisms
python3 scripts/check.py --module Kourovka.Certificates.DerivationMatrix
python3 scripts/check.py --module Kourovka.Certificates.InnerScalarExtension
python3 scripts/check.py --module Kourovka.Certificates.DiagonalKernel
python3 scripts/check.py --module Kourovka.Certificates.Elementary
python3 scripts/check.py --module Kourovka.Analytic.TensorAction
python3 scripts/check.py --module Kourovka.Lattice.NearIdentity
python3 scripts/check.py --module Kourovka.BCH.CoefficientSoundness
```

Each command first removes the entire selected project closure's old `.olean`
and `.ilean` files, then compiles that exact closure serially in dependency order.
A failed prerequisite blocks its descendants, whose stale objects have already
been removed. Compiler exit zero without a new output object is rejected. It
requests transitive axiom output for statically inventoried public declarations
in that closure and emits their fully elaborated types for inspection. A module
run is explicitly partial. It is not a final-theorem certificate.

After intentional edits:

```sh
python3 scripts/check.py --prepare-audit
```

This updates only the **static** inventory and query files. It does not prove
that an edit is correct. The default checker refuses unnoticed source drift.
Retain compiler failures and repairs in the local Git history rather than
replacing hard theorems with admissions.

## 3. Likely repair and resource hotspots

The local audit has found real elaboration failures and high memory use.
Relevant areas for continued review include:

* Bilinear-map coercions and extensionality, `LieRing`/`LieAlgebra` instance
  diamonds, `LieEquiv` constructors and automatic residue-ring linearity.
* Integer casts versus residue-ring casts, scalar notation in p-adic modules,
  quotient-kernel APIs, and the scalar-extension proof for the small rank witness.
* Mathlib lower-central-series indexing and the induction over Lie-submodule
  spans. The intended zero term is index 846, corresponding to gamma_847.
* Kernel-evaluated finite checks. Start with a single `Ambient.Checks.Chunk00`
  or `Lattice.Checks.Chunk00` before timing the entire family. `decide` is
  deliberately not replaced by native compiler-trusting proof evaluation.

Generated data are ordinary proof inputs, not axioms. The raw-table comparison
was repaired by splitting it into 31 kernel-checked row equalities and disabling
asynchronous elaboration. This compiled with `decide +kernel`; its actual final
axiom dependency was only `propext`. Sampled memory was approximately 1.7 GB,
compared with roughly 8.5 GB swapped during the interrupted unsplit attempt.
Other large finite checks may also require smaller chunks. Python timings do
not predict Lean kernel performance. No native-evaluation axiom was introduced.

## 4. Reproduce the small witness generators

These commands are known to have passed without Lean:

```sh
python3 scripts/generate_certificates.py
python3 scripts/source_evidence.py
python3 scripts/direct_flag.py --check-only
python3 scripts/export_lean.py --check-only
python3 scripts/check.py --static-only
python3 scripts/check.py --self-test
```

The default new witness generator compares deterministic output with the stored
small certificates. `--write-generated` writes only the two new witness JSON
files. It does not overwrite original paper files or update Lean literals.
`source_evidence.py` independently reconstructs and compares the relevant
literals. A matching hash or external check never substitutes for a proof term.

## 5. Full current-source validation

When the source slices compile:

```sh
python3 scripts/check.py --milestones
```

The top-level `Kourovka.lean` imports all current source modules. The runner
rejects orphan modules in its static dependency graph. This prevents a green
arithmetic-only root from concealing excluded hard source files.

For explicit fresh project compilation and optional same-kernel replay:

```sh
python3 scripts/check.py --fresh-project --recheck --milestones
```

All project builds are fresh by default, so `--fresh-project` documents that
intent. Pinned upstream dependency objects are preserved; **upstream
dependencies have not been rebuilt from source by this audit**. Add
`--bootstrap` only when the pinned rechecker or dependencies are missing.

The old `--fresh` option requested deletion and rebuilding of all upstream
dependency outputs. The bounded serial runner explicitly rejects that option
rather than silently giving it a different meaning. A full upstream source
rebuild requires a separately documented workflow and is not claimed here.

`lean4checker --fresh` is a separate rechecker option using Lean's own kernel,
not an independently implemented checker. No comparator integration is claimed.

Outputs live in `logs/runs/<UTC>/` and `logs/serial_builds/<UTC>/`, with actual commands, exit codes, wall
measurements, toolchain identification, statement output, and actual axiom
reports when these are produced. A failure is not certification. Review the
source fidelity of the elaborated statements yourself; the script cannot decide
whether they represent the intended mathematics.

## 6. Continue the unfinished mathematics

Work from `docs/REMAINING_OBLIGATIONS.md`. The final group target is absent.
Changing `check.py` so its default gate turns green is not a mathematical repair.
Only add final certification after the actual BCH group, full automorphism
correspondence and exact actual-matrix count have been proved and imported.
