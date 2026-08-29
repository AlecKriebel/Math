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
| raw-four | 405,216 | `7cf3f953fca695d612387143818843650498f84f55cf0a776f90c9afdd95eef6` | `92880c7655e6e6d906c0d6dbe2089043289c7496d1d9883a3fdc69f4de2bd331` | `6364abb6c504b511700f2256ab044640ae89a1dbba62e6447e73c252e2d8d5bc` | 14/14 verifier-facing; payload `94b2f2f90ab77eee454bdbf1c5f81b3be8fd0f89d24b45a15bfed6e92f59a04c` |
| theta2 | 2,946,240 | `805fc7f5a3de9dad2c63a210208075cf19910cf811ffd08878f32782ce71b659` | `bdf85d7d02d7a4540da2e9357c948a9e0b30aa799940240323c9d2821d4738d4` | `6a3902aaee5f58a0dd45ed1a65d8e5f27cc8bdda6c3999422437f52482256de5` | 12/12 verifier-facing; payload `6395c6a79540fb05fe10fc54b55bf446d09023e2c6107148926a9c8f6848ac80` |

The current outer release-contract replay has payload
`98c564205133bc383ba8814ef674c65ea09fe891f9898139f11d313afb107e64`.
These displayed values are a reader snapshot only.  The generated current byte
authority is `work/final_theorem_release/RELEASE_LOCK.json`; this README is
explanatory and does not supersede that lock.

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
`396d1970af17b5e90c3f1b00ceab1b810816e93ec68a566bd0479f05c722793f`.

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
  `21637421a9b1a0cd4e62c6333e133b7530fd1ac5a387314069824088c74f2bff`;
- theta2: 2,766,984,898 bytes,
  `550e8c2d9d7f683d79e8955b91629f1fc527fc8b72a1f592e85d6ecc74642bb7`.

## Reproduction

Run from the repository root with the system Python that supplies NetworkX and
SymPy:

```sh
PYTHONHASHSEED=0 /usr/bin/python3 work/corrected_composite_ledgers/generate_corrected_composites.py --family all
PYTHONHASHSEED=0 /usr/bin/python3 work/corrected_composite_ledgers/verify_corrected_composites_independent.py --family raw4
PYTHONHASHSEED=0 /usr/bin/python3 work/corrected_composite_ledgers/verify_corrected_composites_independent.py --family theta2
/usr/bin/python3 work/corrected_composite_ledgers/run_composite_mutations.py --family raw4 --output /tmp/k2p_raw4_composite_mutations.json
/usr/bin/python3 work/corrected_composite_ledgers/run_composite_mutations.py --family theta2 --output /tmp/k2p_theta2_composite_mutations.json
/usr/bin/python3 work/corrected_composite_ledgers/test_composite_mutation_output_safety.py
PYTHONHASHSEED=0 /usr/bin/python3 work/corrected_composite_ledgers/validate_release_contract.py
```

Generation and replay are streaming.  The observed peak working set stayed
below 300 MB per process.  The theta2 ledger is about 58 MB compressed; no
multi-gigabyte uncompressed temporary ledger is written.  For every advertised
semantic attack, the mutation runner streams one complete deterministic gzip
ledger into scratch, invokes the production independent verifier, requires both
a nonzero exit and the intended semantic diagnostic, and deletes the scratch
ledger before starting the next case.  Optimized-mode refusal and aggregate
source immutability are separate gates.  Reports contain no absolute paths or
runtime fields and are therefore byte-identical across extraction directories.
The output is required to be caller-owned and outside the project tree.  The
explicit `--allow-authoritative-output` override accepts only the one canonical
family report path and is reserved for resealing a release.

## Files

- `generate_corrected_composites.py`: primitive producer for both ledgers.
- `verify_corrected_composites_independent.py`: separately implemented replay
  and canonical-byte verifier.
- `run_composite_mutations.py`: fail-closed mutation suite.
- `test_composite_mutation_output_safety.py`: atomic-output, symlink/hardlink,
  and optimized-mode regressions.
- `validate_release_contract.py`: direct invocation of the current outer
  release validator.
- `composite_support.py`: serialization and streaming hashes only; it contains
  no classification logic.
- `artifacts/*_summary.json`: exact censuses, roots, and input bindings.
- `artifacts/*_independent_replay.json`: structural and whole-map replay reports.
- `artifacts/*_mutations.json`: mutation reports with zero survivors.
- `artifacts/release_contract_replay.json`: current outer-contract acceptance.

No final-theorem locator was modified by this package.
