# Offline build and repair handoff

## Safe input/application

This archive contains UNCOMPILED source. No Lean result is simulated or claimed.
The input is the exact prior adversarial/source-Fourier package, SHA-256
`601b8be5807e0af2597a821c8b47363d142c02f80006b588e59aba6b21829bb1`.
Apply the delta only to that source state. The full additive patch is for a
checkout where the companion directory does not yet exist. Run
`git apply --check` first; never overwrite concurrent work or local repairs.

Location: `Math/cyclic_bell_exact_values_and_randomness/lean_formalization/`.
Canonical manuscript blob: `bbd0667c934d5a34dd9c8ced50df91515cb1308c`.
Expected SHA-256 from the repository manifest:
`82a47d69e43a4a3d18aa8c351b81cfae09c9a06910e85d91ae7daf120f201b71`.
This cloud pass did not independently recompute the entire raw TeX hash.

## One final build-and-audit command

```sh
python3 scripts/check.py --bootstrap --manuscript ../main.tex
```

Lean: `leanprover/lean4:v4.19.0`, compiler commit
`6caaee842e9495688c1567e78c0e68dbb96942aa`.
Mathlib: `c44e0c8ee63ca166450922a373c7409c5d26b00b`; all nine dependency
commits remain fixed in `lake-manifest.json`. Omit `--bootstrap` when the
pinned dependencies and cache are already installed.

The command checks identities, refuses dirty dependency resets or symlinked
build locations, cleans only the companion build directory, builds all source
and statement audits, runs five positive and twenty negative controls, obtains
all 1,538 requested axiom reports, and rechecks protected fingerprints. It is
not a rebuild of Lean and all third-party software from bootstrap sources.
It performs no Git commit, push, release, DOI or correspondence.

Resource exhaustion, timeouts, crashes and signal/nonstandard negative-control
exits invalidate a run; they are not mathematical rejections. A true negative
must report a recognized proof error, not an unknown import/identifier or other
rejected diagnostic. Inspect the actual logs, not only a PASS line.

## Repair order

Retain the existing advice to compile the foundations and a complete d=4
endpoint first, then extend along the all-dimensional, support, Hilbert/model,
and adversarial dependencies. The prior full order is preserved in
`history/adversarial_source_snapshot_20260914/OFFLINE_HANDOFF.md`.

For this new bounded appendix, the order is:

    shared Model/Fourier/Phases/Witness
      -> GeneralPhaseTables -> GeneralPhaseBounds
      -> GeneralAnchoredTables -> GeneralPhaseEntropy -> PhaseTableStatements.

Temporary module-by-module work is appropriate; the final certification must
still clean-build every endpoint being claimed. Do not delete a troublesome
module or alter physical validity to force a successful result.

Preserve negative Alice and positive Bob Fourier signs, ordinary lifted a-b
with fractional offsets, state amplitude 1/sqrt(d), and d^(-3) Born scaling.
Do not divide at resonant equal offsets. Preserve d>=2 for standard nonuniformity
and d>=3 for the anchor strict gap, with a literal d=2 uniform cross-table theorem.
The entropy is observational, not conditional on Eve. Its limit is not proved
by numerical sampling. The appendix source is not an external self-testing
formalization or a universal low-setting no-go theorem.

## Compiler-free reproductions

```sh
python3 scripts/source_inventory.py --write
python3 scripts/static_audit.py --output logs/local_static.json
python3 scripts/test_runner.py
python3 scripts/phase_tables_preflight.py --min-d 2 --max-d 8 --output logs/local_settings_exact.json
```

These do NOT run Lean. The reporting tests mock compiler subprocess outputs;
none of their mock acceptances is a theorem certificate. The source scanner is
not a Lean parser or external-library API resolver. The finite exact checker
uses rational/cyclotomic equality and rational folded-angle comparisons, not a
proof of universal inequalities or the asymptotic statement.

Refresh the inventory after legitimate source repair, then freeze all protected
source inputs throughout the final clean run. Record actual axiom output and
independent statement review before describing the result as verified.
