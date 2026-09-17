# Offline build and repair handoff

## Status and safe application

This is an UNCOMPILED source continuation. The entire package has no new Lean
kernel evidence. It may require substantive proof repairs. Use the delta patch
only on the exact incoming models-and-appendices source; use the full additive
patch only where the companion directory does not already exist. Never overwrite
local repairs or parallel work just to make a patch apply.

Input archive SHA-256:
`e16c0c7edb25ead91fb958547cc1d1f73fb95523d4bb911e32ada93a59e27d8e`.

Install inside `Math/cyclic_bell_exact_values_and_randomness/lean_formalization/`.
The canonical manuscript remains outside the package. Its Git blob is
`bbd0667c934d5a34dd9c8ced50df91515cb1308c`; expected SHA-256 from the repository
manifest is `82a47d69e43a4a3d18aa8c351b81cfae09c9a06910e85d91ae7daf120f201b71`.
This continuation did not independently hash raw canonical manuscript bytes.

## One complete build-and-audit command

```sh
python3 scripts/check.py --bootstrap --manuscript ../main.tex
```

Lean: `leanprover/lean4:v4.19.0`; compiler commit:
`6caaee842e9495688c1567e78c0e68dbb96942aa`.
Mathlib: `c44e0c8ee63ca166450922a373c7409c5d26b00b`.
All nine dependencies remain fixed in `lake-manifest.json`. Omit `--bootstrap`
when the exact dependencies/cache are already available.

The command checks identities, refuses dirty dependency resets and symlinked
build directories, removes only the companion `.lake/build`, builds the default
umbrella, runs all actual Lean controls and axiom queries, and rechecks protected
fingerprints. It is not a bootstrap rebuild of the compiler or all third-party
software. It does not commit, push, contact people, edit the manuscript, publish,
create a release or mint a DOI.

## Repair order

Start with the first compiler error. The original d=4 branch remains a useful
pilot. Then repair the shared all-dimensional Fourier/phase/cycle/model path,
scalar/CFC bounds and witnesses, support/rigidity, arbitrary-Hilbert bounds,
actual bipartite model-value assembly, binary and setting results. Earlier
handoffs remain in `history/` for their detailed ordering.

The new chain is:

    GeneralExtendedBehavior -> GeneralTripartite -> GeneralCommutingGuessing
      -> GeneralAdversarialValues -> GeneralAdversarialEntropy
      -> GeneralPOVMMaximum -> GeneralNestedGuessing.

`GeneralSourceFourier` is a separate appendix branch. Then check
`GeneralAdversarialRegression`, `AdversarialStatements`, the original expanded
statements and the generated `AxiomAudit`. Every claimed module must participate
in the final clean default build. Do not omit a failing endpoint to get green.

`dimension_pos` now correctly lives in `GeneralFourier`, not `GeneralWitness`.
Do not restore the old import error or add a witness import to the scalar bound.

Expected repair-sensitive interfaces include arbitrary matrix/CLM coercions,
finite sum rewrites, positivity of tensor products and sandwich pairings,
compactness and IsMaxOn elaboration, dependent existential typeclass instances,
real conditionally complete suprema, and inherited CFC/support proofs. These
are risks from inspection, not compiler errors actually observed.

## Statement invariants

Keep arbitrary finite local/Eve dimensions and all normalized mixed states.
Alice/Bob PVMs may have zero effects; Eve is a general positive complete POVM,
NOT a PVM. Keep exact coefficients, Fourier signs, target `(1,none)`, transpose
and conjugation conventions. Keep positivity of conditional matrices tied to
actual post-measurement instruments. Cross-party commutation must not become
same-party commutation.

GuessQa is the closure of full extended correlations BEFORE the Bell-equality
slice. A physical saturating witness establishes nonemptiness. Real sSup is not
an assumed optimum field. Fixed finite-Eve maxima are obtained from Gram
compactness, not by assuming the optimal POVM exists. The same AB behavior is
proved unchanged when optimizing Eve. No worst-case realizing strategy or
arbitrary-Hilbert Eve maximum is claimed.

Retain no admissions, custom axioms, native_decide or unsafe proof substitutes.
Permitted foundational axioms: propext, Classical.choice, Quot.sound only.

## Regenerate and check metadata after source repairs

```sh
python3 scripts/source_inventory.py --write
python3 scripts/project_reference_audit.py --output logs/local_references.json
python3 scripts/static_audit.py --output logs/local_static.json
python3 scripts/test_runner.py
python3 scripts/check.py --manuscript ../main.tex
```

The first four commands are compiler-free. The reference scanner is deliberately
conservative: it checks selected known distinctive project identifiers, not all
Lean scopes, generated declarations, local shadowing or unknown symbols.

Supplementary new exact tests:

```sh
python3 scripts/adversarial_preflight.py --cases tiny unequal ranktwo trivialeve --output logs/local_adversarial.json
python3 scripts/source_fourier_preflight.py --dimensions 1 2 3 4 5 6 7 8 --output logs/local_source_fourier.json
python3 scripts/povm_gram_preflight.py --output logs/local_gram.json
```

These cannot prove compactness, closure, suprema or general mathematical claims.
The Gram example is a trine ensemble, not a cyclic-Bell maximizing witness.

## Final review and remaining scope

A real successful run supplies clean-build logs, actual axiom reports and Lean
control outcomes. An independent specialist must then inspect statement and
manuscript correspondence. The runner deliberately does not automatically mark
whole-paper certification true. Generic Qqa-subset-Qqc, full canonical-polar
source strategy identification and selected standard/anchored-table asymptotics
remain outside the supplied source endpoints. See current `COVERAGE.md`.
