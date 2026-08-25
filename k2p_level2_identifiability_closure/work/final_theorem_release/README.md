# Final principal-D+ theorem release harness

This directory is the promotion-grade integration and reproducibility layer
for the unconditional `K2P-SAME` theorem on the principal positive K2P domain.
It locks every load-bearing proof and computation, checks exact cross-layer
censuses and hash roots, and orchestrates independent quick and full replays
without writing into producer directories.

The authoritative theorem text is
`../global_theorem_closure/promotion_manuscript/K2P_SAME_PROMOTION_MANUSCRIPT.md`.
The earlier `../global_theorem_closure/GLOBAL_PROOF.md` is historical
provenance only. The oddly named `PROBE_PROMOTION_PLACEHOLDER.json` in the
promotion-manuscript directory is not pending: it is the completed frozen
`PASS` binding checked by the promotion guard.

Legacy handoff names are not additional gates.  The canonical mapping is in
`../../output/referee/README.md`: in particular, `verify_handoff.py` maps to
the bundle/lock checks plus this harness's quick replay,
`test_handoff_mutations.py` maps to `run_release_mutations.py`,
`run_all_verifiers.py` maps to this harness with `--full`, and
`SUBMISSION_BINDING.json` maps to `RELEASE_LOCK.json` together with the
portable bundle ledger.  Reviewers should run the current commands printed
below rather than search for legacy-named wrapper files.

The outer lock has three disjoint semantic partitions: authoritative proof
inputs, bound runtime evidence, and bound historical provenance. The eight
proof-like historical files found by the final adversarial scanner are listed
in `HISTORICAL_ARTIFACT_REGISTRY.json`; each has an exact byte hash, a revoked
or superseded status, and an authoritative replacement. In particular, the
old depth-one restoration certificate, replay, and narrative are quarantined
runtime provenance only. They cannot satisfy promotion semantics; the
corrected v3 forest and replay are the sole restoration authorities.

The frozen corrected universe binds:

- every one of the 405,216 raw four-port directional presentations;
- every one of the 2,946,240 theta2 directional presentations and all
  dummy-restoration descendants;
- 997 canonical restoration parents, 2,540 physical member roots, and the
  terminating 36,824-edge restoration forest;
- all 13,440 corrected cycle-base records and 536,364 fixed-full children;
- all 29,964 one-port and 544,571 two-port probe rows, including 2,107
  one-port parents, 32,729 reverse marginals, 67,741 exact transports, and
  4,379 parent restrictions.

The unified independent replay passes with zero unresolved records, zero
rooted-oracle reasons, zero missing children, zero cycles, and zero incoherent
transports. All 22 unified certificate mutations reject. The outer suite also
targets raw omissions, false rank exclusions, wrong parents, missing children,
broken transports, reassigned quadratic/cubic/quartic/quintic and `T_i`
certificates, the historical `raw4424` oracle regression, promotion document
drift, historical-artifact promotion or omission, and optimized-Python
execution. The outer suite has 27 conceptual gates.  Attacks rerun by the
outer command use disposable ledgers, reports, or isolated project copies.
Rows explicitly labelled `frozen` instead bind already sealed nested mutation
suites and validate their exact producer, verifier, source, census, and
semantic-diagnostic contracts; they are not described as freshly rerun by the
outer process.

The release additionally binds the correction of an original certificate
serialization defect. `verify_full_map_reseal.py` proves that the raw-four and
theta2 truth certificates changed only in 8 and 85 domain-description leaves,
their dependent nested seals, and their top seals; it also rejects arbitrary
fully resealed domain prose and stale seals. In full mode,
`verify_composite_reseal_diff.py` proves that the raw-four composite is
byte-identical and that exactly 2,528 theta2 rows changed at the single leaf
`evidence_binding.coefficient_certificate_sha256`, while reconstructing the
prior theta2 gzip byte-for-byte.

## Referee commands

The locked bundle does not contain a machine-specific virtual environment.
On a fresh copy, run the following commands from the project root. They create
the environment and install the two exact versions in this release's locked
requirements file:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install \
  -r work/final_theorem_release/requirements.txt
```

The release was qualified with Python 3.14.6, NetworkX 3.5, and SymPy 1.14.0.
The source requires Python 3.10 or newer. The virtual environment is execution
infrastructure, not theorem evidence; every project file read by the quick
qualification is committed by the outer or recursively validated nested
locks.

Then, still from the project root, build and byte-check the promotion-ready
lock:

```sh
.venv/bin/python -B work/final_theorem_release/build_release_lock.py --require-ready
.venv/bin/python -B work/final_theorem_release/build_release_lock.py --check --require-ready
```

Run the ordinary qualification path:

```sh
.venv/bin/python -B work/final_theorem_release/verify_final_theorem_release.py --quick
.venv/bin/python -B work/final_theorem_release/run_release_mutations.py
```

When a machine-readable outer mutation report is wanted, `--output` must name
a caller-owned path outside the project tree.  The v2 report deliberately
excludes elapsed time, temporary paths, and hashes of raw child output; it
records stable semantic rejection markers and return codes and is therefore
byte-comparable across differently named clean extractions.  The focused
output-contract regression is:

```sh
.venv/bin/python -B work/final_theorem_release/test_release_mutation_output_contract.py
.venv/bin/python -B work/final_theorem_release/test_nested_mutation_output_contract.py
```

The documented outer mutation command runs this regression as a mandatory
preflight before any conceptual mutation gate; it does not add a mutation row
or alter the 27-gate census. Reports are fsynced to a new same-directory file
and atomically replaced, and the regression attacks both external hardlinks
and late output-symlink swaps without allowing either to modify source bytes.

Run the clean-room exhaustive path when full primitive regeneration is
desired:

```sh
.venv/bin/python -B work/final_theorem_release/verify_final_theorem_release.py --full
```

Quick mode executes the final promotion guard, the fail-closed full-map reseal
audit, and the unified independent replay as well as every standard theorem
layer. Full mode additionally reconstructs the composite reseal differential
and regenerates the raw/rank, direct, theta2, corrected probe, independent
primitive-graph probe audit, and unified mutation packages in isolated
temporary trees.

Every entry point explicitly rejects `python -O`. The ordinary-triangle
replayer contains no Python `assert` statements and uses explicit exact
checks.

## Scope

The release proves the principal-domain theorem for

```text
D_plus = {0 < s < 1, 0 < g < 1, g > 2s - 1},
```

its strict continuous-time corollary `0 < s < 1, s^2 < g < 1`, and the
`4n-3` weak-class sharpness theorem. It makes no mixed-sign claim.
