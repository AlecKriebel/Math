# Kourovka Notebook 16.63 — expanded Lean source draft

**Source revision 0.1.0 · 17 September 2026 · UNCOMPILED.**

This standalone package extends the earlier checkpoint with concrete Lean proof
bodies for the explicit Lie construction, both classification-free flag-rigidity
arguments, generation, weighted coordinates, nilpotency, all Lie-ring
automorphisms versus matrices, the full derivation matrix, an independent rank
upper-bound witness, scalar kernel counting, and some analytic/BCH algebra.

**It is not a complete formalization.** The paper's BCH `Group G` instance,
`Nat.card (MulAut G) = 1009^52359`, and the unconditional notebook theorem are
absent. No Lean compiler, axiom query, or kernel rechecker was run in this
source-only continuation. The missing mathematics is not merely an assortment
of compiler errors. Read [the remaining obligations](docs/REMAINING_OBLIGATIONS.md).

## Start offline

Use Lean/Lake **4.19.0**. This package does not install Lean or contact a remote
execution service. Dependency fetching happens only when explicitly requested.
From `kourovka_16_63/lean/`:

```sh
python3 scripts/check.py --bootstrap --cache --module Kourovka.Parameters
```

This is the first **unexecuted** compiler command, not a known-passing command.
It fetches the pinned dependencies and optional Mathlib cache, compiles the
selected module and its imports, then requests real statement and axiom output.
After that succeeds, follow the [offline guide](docs/OFFLINE_GUIDE.md). In
particular the substantive flag milestone is:

```sh
python3 scripts/check.py --module Kourovka.Flag.Rigidity
```

After intentional source repairs, refresh the *static* declaration inventory:

```sh
python3 scripts/check.py --prepare-audit
```

To build and inspect **every current draft module**, not just the easy ones:

```sh
python3 scripts/check.py --milestones
```

`Kourovka.lean` imports the whole current local source tree. A successful
`--milestones` run would validate those statements, **not** the absent group
theorem. The default command deliberately exits nonzero:

```sh
python3 scripts/check.py
# INCOMPLETE_FINAL_GROUP_THEOREM_ABSENT
```

For a from-source dependency rebuild and the pinned same-kernel fresh recheck,
once the source errors have been repaired:

```sh
python3 scripts/check.py --bootstrap --fresh --recheck --milestones
```

Do not combine `--fresh` with `--cache`. No such Lean command ran in this session.
The rechecker uses Lean's own kernel; it is not a second independently
implemented theorem-prover kernel.

## Checks that ran without Lean

The following use the Python standard library only and execute no Lean:

```sh
python3 scripts/generate_certificates.py
python3 scripts/source_evidence.py
python3 scripts/direct_flag.py --check-only
python3 scripts/export_lean.py --check-only
python3 scripts/check.py --static-only
python3 scripts/check.py --self-test
```

They passed in this session. They reconstruct the actual coefficients and new
small witnesses, check deliberately incorrect witnesses, and test the runner.
They do not validate Lean syntax, theorem statements, proof terms, or kernel
acceptance. See [the session report](SESSION_REPORT.md) and the retained
`logs/source_expansion_2026-09-17/` records.

## The mathematical source path

- `Ambient/`, `Lattice/`, `Finite/`: integer table, bilinearity/alternation/Jacobi,
  adapted basis, scaled bracket, finite Lie ring and p-adic quotient coordinates,
  length-847 bracket vanishing and the standard lower-central-series conclusion.
- `Flag/`: concrete generators, the 88-node generation certificate, and proof
  bodies for the **full** and infinitesimal flag stabilizers. The direct route
  replaces the full finite-field automorphism classification for this purpose.
- `Finite/LieAutomorphisms.lean`, `Certificates/`: all additive bracket
  automorphisms versus all invertible matrices; exact derivation equations;
  30 independent inner directions and a characteristic-zero rank bound;
  elementary-operation checker and general finite-kernel counting lemmas.
- `Analytic/`, `Lattice/NearIdentity.lean`, `BCH/`: two-lattice power estimates,
  finite geometric inverses, commuting tensor actions, conditional exact
  factorization lemmas, and Dynkin/collected-coefficient soundness.

The last two directories are **not** a completed exponential/logarithm or Lazard
implementation. The generic operation checker is **not** an accepted replay of
the actual 931-pivot Smith certificate.

## Pinned identity and trust

The paper target is DOI `10.5281/zenodo.22770864`, publication tag
`kourovka-16-63-v1.1.0`, commit
`b575b59086c1f9756c4c65991f6aa8905a73304e`. The earlier checkpoint matched the
three original data files against the publication tag's Git blob hashes.
**Identity with the deposited DOI archive is still unverified.** The local
historical report is not mislabeled as the tagged or deposited version.

Mathlib is pinned to `c44e0c8ee63ca166450922a373c7409c5d26b00b`. The root Lake
manifest is source-derived, not the result of a successful local Lake command.
The optional compatible rechecker is pinned to
`e11f65c651edd58d68ba260015d2bfde5102cd7f`.

The static scan rejects direct admissions, project axioms and prohibited
compiler-trusting proof patterns. Actual axiom dependency lists remain
**unknown**. Sources use ordinary proof terms/tactics and kernel-evaluated
`decide` attempts, not `native_decide`. Finite checking cost in Lean is
unmeasured.

Start review with [the statement contract](STATEMENT_CONTRACT.md),
[the declaration map](docs/DECLARATION_MAP.md), and
[the trust report](docs/TRUST_REPORT.md). `progress.json` tracks named
mathematical obligations, not a percentage based on source size.
