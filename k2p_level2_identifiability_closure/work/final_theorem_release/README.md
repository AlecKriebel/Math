# Final principal-D+ theorem release harness

This directory is the promotion-grade integration and reproducibility layer
for the unconditional `K2P-SAME` theorem on the principal positive K2P domain.
It locks every load-bearing proof and computation, checks exact cross-layer
censuses and hash roots, and orchestrates independent quick and full replays
without writing into producer directories.

The current submission theorem authority is
`../../proof_compression_submission/article/main.tex`, with the rendered
article bound by the submission manifest.  The release also retains and
checks the frozen theorem narrative
`../global_theorem_closure/promotion_manuscript/K2P_SAME_PROMOTION_MANUSCRIPT.md`;
it is the machine-bound computational theorem-promotion companion, not the
current submission proof authority.  Its reconstruction procedure mirrors the
article's retain-all-candidates and final exact-membership steps.  The earlier
`../global_theorem_closure/GLOBAL_PROOF.md` is historical provenance only.
The oddly named `PROBE_PROMOTION_PLACEHOLDER.json` in the promotion-manuscript
directory is not pending: it is the completed frozen `PASS` binding checked by
the promotion guard.

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
execution. The outer suite has 25 conceptual gates, including fresh
production-verifier-facing exact-rank and weak-sharpness mutation gates.
The revoked raw-ledger mutation suite and the historical rooted-theta2
quadratic suite remain byte-bound as nonauthoritative provenance regressions;
neither is invoked by, or counted in, the promotion suite. The current
corrected raw-four full-map, theta2 full-map, and exact-rank suites cover those
promotion semantics. Attacks rerun by the
outer command use disposable ledgers, reports, or isolated project copies.
The raw-four and theta2 full-map, canonicalizer, parameter-transport, rank,
restoration, and probe mutation rows are freshly rerun with caller-owned
disposable reports and checked against their sealed logical payloads.  The two
full-map suites require clean production-verifier baselines, exact per-case
diagnostics, exit status one, no unrelated crash, and no success artifact. The
unified corrected-universe suite uses the same
caller-owned output contract and is rerun by full mode. Rows explicitly labelled `frozen` instead bind
already sealed nested suites and are not described as freshly rerun by the
outer process.

All bound local theorem replay readers that interpret compressed JSON
evidence, together with the outer bundle producer, use the lock-bound
`strict_json.py` syntax boundary. The independently implemented outer checker
enforces the same policy without importing that module. At the package
boundary, plain JSON rejects repeated object names recursively and non-finite
numeric values. Every `.json.gz` document and every `.jsonl.gz` row must
additionally equal its compact sorted-key UTF-8 serialization exactly,
including one terminal LF.
Compressed inputs are capped at 512 MiB, gzip JSON documents at 64 MiB,
individual JSONL rows at 16 MiB, and each expanded JSONL stream at 4 GiB.
These caps exceed every frozen artifact while making decompression behavior
finite and explicit.

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
.venv/bin/python -B work/final_theorem_release/run_corrected_universe_mutations.py --output /tmp/k2p-corrected-universe-mutations.json
```

The corrected-universe mutation report follows the same caller-owned output
rule.  A maintainer may reseal exactly
`work/final_theorem_release/corrected_universe_mutation_report.json` by adding
`--allow-authoritative-output`; that flag licenses no alias or other path.

When `verify_final_theorem_release.py` is given `--output`, routine replay
reports must use a caller-owned path outside the project tree.  The entry point
removes stale bytes before any replay or optimized-Python guard and atomically
replaces the report only after completed report construction.  A maintainer may reseal exactly
`proof_compression_submission/output/FINAL_CLEAN_FULL_REPLAY.json` by adding
`--allow-authoritative-output`; that flag licenses no alias or other path.  The
focused collision, stale-output, hardlink, and symlink regression is
`test_final_replay_output_contract.py`.

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
or alter the 25-gate census. Reports are fsynced to a new same-directory file
and atomically replaced, and the regression attacks both external hardlinks
and late output-symlink swaps without allowing either to modify source bytes.

Run the clean-room exhaustive path when full primitive regeneration is
desired. Full mode has 41 named layers: in addition to the prior primitive
gates, it freshly replays all 36,824 restoration edges into an external report
and binds that layer's semantic command and exact verifier/forest/crosswalk
source hashes:

```sh
.venv/bin/python -B work/final_theorem_release/verify_final_theorem_release.py --full
```

Quick mode executes exactly 23 named layers. Its cycle row is the current
authoritative promotion replay over all 13,440 base rows and 536,364 children;
the superseded rooted cycle replay remains historical provenance and is not
executed. Quick mode also executes the final promotion guard, the fail-closed
full-map reseal audit, and the unified independent replay as well as every
standard theorem layer. Full mode additionally reconstructs the composite reseal differential
and regenerates the raw/rank, direct, theta2, corrected probe, independent
primitive-graph probe audit, and unified mutation packages in isolated
temporary trees.

The full replay row named
`four_port_exact_rank_staged_atlas_omission_mutation` is only a staged
dependency-omission/import preflight: it proves that a missing atlas cannot be
silently accepted. It is not counted as a semantic rank-certificate attack.
The exact rank-v2 mutation report supplies the separate production-verifier
semantic attack.

Every documented release entry point, and every portable sweep production
entry point enumerated by `test_optimized_entrypoints.py`, rejects optimized
mode before writing output. No load-bearing atlas certificate check depends
on Python `assert`. The ordinary-triangle replayer likewise contains no
Python `assert` statements and uses explicit exact checks.

## Scope

The release proves the principal-domain theorem for

```text
D_plus = {0 < s < 1, 0 < g < 1, g > 2s - 1},
```

its strict continuous-time corollary `0 < s < 1, s^2 < g < 1`, and the
`4n-3` weak-class sharpness theorem. It makes no mixed-sign claim.
