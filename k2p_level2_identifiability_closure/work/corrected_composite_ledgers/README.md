# Corrected raw-four and theta2 composite ledgers

## Result

This directory contains the authoritative principal-`D_plus` composite
ledgers required by
`work/final_theorem_release/CORRECTED_FINITE_UNIVERSE_CONTRACT.md`.
Both families pass the current release validator, independent primitive replay,
byte-for-byte gzip regeneration, exact whole-map algebra replay, and targeted
mutations.

The bounded composite-ledger objective is **100% complete**.  This statement is
about the two primitive composites only; it does not promote the outer global
theorem or make a mixed-sign claim.

| Family | Rows | Compressed SHA-256 | Summary payload | Independent replay payload | Mutations |
|---|---:|---|---|---|---:|
| raw-four | 405,216 | `431dac8898ad2a724d12c200687de1b377723e302214a79a11a03524a4084b96` | `8154acc38ad58b49e4f0f5b34f6fdb9999c0392dd947f91bc6017d8e2ab8d5cf` | `0e167e742907394a77a0eab1614366e2460b86b13241577ad25e902822241ea8` | 14/14 rejected |
| theta2 | 2,946,240 | `805fc7f5a3de9dad2c63a210208075cf19910cf811ffd08878f32782ce71b659` | `480c27d82924bbf12adf1357f9e3bc216d1818dce68d061bb134f387e9737194` | `2fa46fd0ca70dbe00e8231686bfd790f57d76d9a33ddc4b07cffaa72e3b07e8b` | 12/12 rejected |

The current outer release-contract replay has payload
`5fd774fb9335a7ce1900dd80226c79fab8459f8fa3738c5274237c131113cde7`.

## Authoritative partition

Raw-four has the exact partition

- 360,408 exact displayed-quartet exclusions;
- 16,974 exact whole-map `T_i` strict-sign exclusions;
- 23,822 directed exact-rank exclusions;
- 1,472 direct-terminal presentations in 934 classes; and
- 2,540 restoration-member presentations in 997 canonical parents.

The terminal class multiplicity histogram is
`{1:680,2:150,4:71,5:14,6:7,8:12}`.  The restoration-parent histogram is
`{1:424,2:112,4:449,8:12}`.  Every restoration presentation binds one
canonical parent, one physical member-root transport, and the finalized clean
restoration forest with file SHA-256
`43bd2be5e7626a954fc4fa4cf45e8d0e6483c947ddc9cba80f2b1a13351bc3a8`.

Theta2 has the exact partition

- 2,942,592 exact displayed-quartet exclusions;
- 2,528 exact whole-map `T_i` strict-sign exclusions;
- 800 directed exact-rank exclusions;
- 240 exact quadratic separators; and
- 80 labelled isomorphisms.

The 56 dummy-bearing isomorphism roots bind 864 distinct descendants and 864
one-parent edges.  The forest has 832 leaves: 760 exact displayed-quartet
separators and 72 labelled isomorphisms.  It has zero missing continuation
layers, cycles, or unresolved descendants.

## Proof bindings

The producer regenerates every source, target, raw ID, and physical port
permutation from the primitive graph grammar.  It recomputes every quartet
witness, including the distinguished split and the hashes of the two exact
displayed-split sets.  Historical selector ledgers are locked only as
provenance; no historical selection field or rooted restriction is copied into
an authoritative row.

Every whole-map row binds its exact coordinate triple and orientation,
source/target pullback hashes and term counts, polynomial relation class, exact
graph relation, and complete Bernstein coefficient certificate data.  The
independent replay additionally reconstructs all 16,974 raw-four and all 2,528
theta2 pullbacks algebraically.

Every rank exclusion makes the directed argument explicit:

- an exact nonzero source lower minor certifies the source rank;
- an exact target lower minor and symbolic target upper certificate agree; and
- the target exact rank is strictly below the source exact rank.

The raw-four terminal registry contains the exact proof payload and original
semantic/byte bindings for all 934 terminal classes.  It is a frozen proof
input to composite regeneration.  `build_terminal_registry.py` is the one-time
provenance extractor from the complete production record directory; referees
do not need that directory because the compact registry includes the proof
payloads themselves.

## Canonical serialization

The ledgers are gzip JSONL with `mtime=0` and compression level 6.  Every row
is compact UTF-8 JSON with sorted keys, separators `(",", ":")`, one LF, and
strictly increasing dense raw IDs.  Semantic summaries contain no timestamps
or runtimes.

The ordered row root is
`SHA256(concat(binary_SHA256(canonical_row_json)))`; the raw-ID root uses the
same construction on each canonical integer.  Independent replay parses,
rechecks, and recompresses every row in a temporary directory and requires the
compressed bytes to match exactly.

Uncompressed stream sizes and SHA-256 values are:

- raw-four: 391,559,514 bytes,
  `f3fa7f6568551e1f5daa5aa0fbeb7cfd5773c8fd1277588efed3f98a7c8f4033`;
- theta2: 2,766,984,898 bytes,
  `550e8c2d9d7f683d79e8955b91629f1fc527fc8b72a1f592e85d6ecc74642bb7`.

## Reproduction

Run from the repository root with the system Python that supplies NetworkX and
SymPy:

```sh
PYTHONHASHSEED=0 /usr/bin/python3 work/corrected_composite_ledgers/generate_corrected_composites.py --family all
PYTHONHASHSEED=0 /usr/bin/python3 work/corrected_composite_ledgers/verify_corrected_composites_independent.py --family raw4
PYTHONHASHSEED=0 /usr/bin/python3 work/corrected_composite_ledgers/verify_corrected_composites_independent.py --family theta2
/usr/bin/python3 work/corrected_composite_ledgers/run_composite_mutations.py --family raw4
/usr/bin/python3 work/corrected_composite_ledgers/run_composite_mutations.py --family theta2
PYTHONHASHSEED=0 /usr/bin/python3 work/corrected_composite_ledgers/validate_release_contract.py
```

Generation and replay are streaming.  The observed peak working set stayed
below 300 MB per process.  The theta2 ledger is about 58 MB compressed; no
multi-gigabyte uncompressed temporary ledger is written.  Mutation runners use
independent temporary copies and verify that source fingerprints are unchanged.

## Files

- `generate_corrected_composites.py`: primitive producer for both ledgers.
- `verify_corrected_composites_independent.py`: separately implemented replay
  and canonical-byte verifier.
- `run_composite_mutations.py`: fail-closed mutation suite.
- `validate_release_contract.py`: direct invocation of the current outer
  release validator.
- `composite_support.py`: serialization and streaming hashes only; it contains
  no classification logic.
- `artifacts/*_summary.json`: exact censuses, roots, and input bindings.
- `artifacts/*_independent_replay.json`: structural and whole-map replay reports.
- `artifacts/*_mutations.json`: mutation reports with zero survivors.
- `artifacts/release_contract_replay.json`: current outer-contract acceptance.

No final-theorem locator was modified by this package.
