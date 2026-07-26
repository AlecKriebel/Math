# External exact-byte code audit: verifier B for order-13, k=3, `hole9`

## Verdict

`ACCEPT_WITH_CAVEATS_NO_SOUNDNESS_BLOCKER`

This verdict applies only to these exact final bytes:

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `src/verifier_b/order13_k3_hole9_certificate.py` | 39,193 | `4adf3691f438c03b230ff323ea5f7c180db9b5c8cd895b6f31327f5e154a97ee` |
| `tests/test_order13_k3_hole9_certificate_verifier_b.py` | 3,826 | `2ca00e46efee4597fcc532ffe9e8d9fc61c73631def42011d26ab7a3cf516fc5` |
| retained verifier `evidence.json` | 15,105 | `3de45d16b906e52c3960e4b2e75604908c8cacf356b84d7337db721f4fa49af8` |
| corrected `tool-source-provenance.json` | 2,518 | `95702f678c8fbbde5f733e121105d59b2c3890821b1195300d7ec5f03cefa275` |
| this audit's canonical `evidence.json` | 8,482 | `97aad1ec54552aca510d511063ccca74de702dc4f9f1796dbbc2333f4c42ecd9` |
| this audit's read-only `replay.py` | 21,785 | `e7627c21fa588ec4b1efd2438d6666acf6f437bbed6dcff7ebe5b592fe38e66f` |

The accepted claim is deliberately narrow: the exact SHA-256-bound
order-13, parameter-three, `hole9` DIMACS formula is UNSAT. This audit does
not promote that result to an order-13-wide exclusion and makes no universal
gamma-theta claim. The retained verdict correctly remains
`VERIFIED_EXACT_HOLE9_CNF_UNSAT_CANDIDATE_ONLY_PENDING_HOSTILE_ACCEPTANCE`.

## What was audited

The audit inspected the verifier without importing any constructor, search,
production runner, normalizer, or candidate-manifest logic. It checked:

- binary DRAT literal decoding, unsigned LEB128 canonicality, record
  boundaries, deletion exclusion, variable bounds, and the unique final
  empty addition;
- DIMACS header, clause, literal, empty-clause, and maximum-variable
  accounting;
- proof-checker commands, warning and RUP-only flags, exit codes, stderr,
  transcript grammars, and unique success markers;
- exact formula equality and all formula, proof, checker, mathematical
  source, and review bindings;
- candidate-manifest nonreliance and the candidate-only claim boundary;
- final-symlink handling, fresh private copies, pre/post byte checks, source
  self-observation, and remaining race implications; and
- whether the hostile corruptions and focused tests fail closed.

## Exact technical findings

### Binary proof

The parser at verifier lines 370--452 matches the retained checker's binary
literal convention at `drat-trim.c` lines 983--994: an unsigned LEB128 value
encodes the variable as `value >> 1` and the sign in its low bit. The verifier
requires the canonical re-encoding of each value, rejects values for variable
zero or above 9,802, rejects deletion and unknown record prefixes, and rejects
truncation, multiple or early empty records, and all post-empty bytes.

A separate parser reproduced:

- 45,281 addition records;
- 45,280 nonempty additions followed by one unique final empty addition;
- 410,400 literals;
- maximum variable 9,802;
- maximum clause size 284; and
- zero deletions and zero post-empty records.

The exact normalized proof is 742,337 bytes with SHA-256
`af216ef2d7698db2b1d1c55411bc05025bfe25f10c16f2e85c5301f7a88bdd5f`.

### Formula

The independent DIMACS parser at verifier lines 281--356 treats clauses as a
whitespace-delimited token stream, so clauses may span lines without changing
the count. It enforces a unique prior header, legal decimal integer tokens,
the header variable bound, final clause termination, and the declared clause
count.

A separate parser reproduced:

- 9,802 variables;
- 32,108 clauses;
- 281,028 literals;
- maximum clause size 286;
- no comments; and
- no empty clauses.

The certificate formula and accepted constructor formula are byte-identical:
1,168,197 bytes, SHA-256
`3fff100cbfe66b422f9148fda66b6d1ccf6060a4ffbcdb37a54bde415e95e9ea`.

### Proof checkers and transcripts

The private-checker code at verifier lines 577--681 copies the exact formula,
both proofs, and both checker executables into a new mode-0700 temporary
directory. It executes:

```text
drat-trim instance.cnf proof.normalized.bdrat -i -f -W -U -t 1800
lrat-check instance.cnf proof.lrat
```

The retained `drat-trim.c` option definitions confirm that `-i` forces binary
parsing, `-f` selects forward UNSAT checking, `-W` makes the first warning
fatal, and `-U` permits only RUP additions. The validators at verifier lines
467--560 require exit zero, empty stderr, the exact ordered transcript shape,
a unique verified marker, and zero RAT lemmas for the binary proof. The LRAT
validator additionally requires the exact added/deleted/live clause totals.

Both retained executables replayed successfully. The exact C sources were
also freshly compiled with the recorded commands:

```text
cc drat-trim.c -std=c99 -O2 -o drat-trim
cc lrat-check.c -std=c99 -DLONGTYPE -O2 -o lrat-check
```

On Apple clang 21.0.0 targeting `arm64-apple-darwin25.5.0`, the clean builds
were byte-identical to the retained executables:

- `drat-trim`: 70,088 bytes, SHA-256
  `31df522b8b2b71acd357723b0e826cf488826ed78ad9e3a7bcad241271812beb`;
- `lrat-check`: 36,520 bytes, SHA-256
  `5d7d77a57457db82e57f2505ea9d0267ff0bceff197235b6edfc8fda1f26c7a2`.

The rebuilt checkers independently returned one verified marker, exit zero,
and empty stderr. The rebuilt DRAT checker also reported zero RAT lemmas.

### Bindings, reviews, and claim boundary

Verifier lines 938--1064 require the certificate and constructor formulas to
be byte-identical, recheck the exact censuses, bind the corrected candidate
README census, check four exact review verdicts, run the hostile suite, replay
both checkers, and then rebind every frozen input. The retained verifier
evidence contains 23 exact frozen bindings covering:

- the C-055 graph-to-CNF theorem and its two-stage hostile mathematical
  review;
- constructor acceptance and exact live-`hole9` preflight;
- the accepted constructor formula, manifest, and coloring bank;
- the certificate formula, normalized binary proof, LRAT proof, corrected
  candidate README, and provenance-only candidate manifest; and
- both proof-checker executables.

This is sufficient for the exact-CNF candidate-only verdict. Semantic
promotion from that formula to a template-level or order-wide mathematical
claim remains correctly deferred to a separate integration audit.

The verifier does not use claims from the candidate manifest. The source
self-observation at verifier lines 940--941 and 1002--1004 detects a source
file change across the run. Its disclosure at lines 1047--1060 correctly says
that this is provenance, not authentication of already-loaded interpreter
state. This review supplies the required external binding to the exact
verifier bytes.

### Corruption tests

The complete verifier replay rejected 24 of 24 hostile mutations. These
include malformed or miscounted DIMACS, deletions, unknown prefixes, early and
post-empty records, noncanonical and truncated LEB128 values, variables above
9,802, nonzero checker exits, missing success markers, nonempty stderr, a RAT
core, and bit flips in the formula, both proofs, both checkers, C-055, and
constructor evidence.

The focused test file independently passes all seven tests. Its
`run_hostile_mutations` call covers the 18 base mutations. The six
decisive-payload bit flips and full private-checker integration run through
the complete verifier rather than through that focused unit test. This is a
test-layer coverage caveat, not a soundness gap in the accepted run.

## Required provenance repair and final re-audit

During this audit, the initial
`tool-source-provenance.json` (SHA-256 `1408a61a...`) was found to record two
clean-build hashes that did not follow from its stated commands and exact
sources. Rerunning those commands produced `31df522b...` and `5d7d77a5...`,
byte-identical to the retained decisive checker executables.

The provenance JSON was corrected to those values. This review re-read,
replayed, and binds the corrected final file:

```text
95702f678c8fbbde5f733e121105d59b2c3890821b1195300d7ec5f03cefa275
```

The defect affected supporting build provenance only. The decisive checker
binaries, formula, proofs, and successful proof checks never changed, so
there was no mathematical soundness impact.

## Nonblocking caveats

1. The focused unit test covers 18 base mutations; the retained complete
   verifier run covers all 24 and the private checker processes.
2. Runtime source authentication must come from this external exact-byte
   binding, not the verifier's explicitly limited source self-observation.
3. Exact clean-build equality is platform-specific. On other systems an
   independent user should build trusted proof checkers locally and replay
   both certificates. Platform drift causes this package to fail closed.

None of these caveats permits an invalid certificate to be accepted by the
reviewed exact bytes.

## Read-only reproduction

From the campaign root:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONWARNINGS=error \
python3 -B -W error \
  reviews/order13_k3_hole9_certificate_verifier_b/external_code_audit/replay.py
```

The script binds 13 exact repository inputs, independently recounts the
formula and binary proof, requires a byte-identical fresh verifier replay,
runs the seven focused tests, validates the corrected source provenance,
freshly rebuilds both checkers, and replays both certificates. Repository
inputs are read-only; all build and checker outputs live in a temporary
directory.

The canonical detailed audit evidence is `evidence.json`, SHA-256
`97aad1ec54552aca510d511063ccca74de702dc4f9f1796dbbc2333f4c42ecd9`.
