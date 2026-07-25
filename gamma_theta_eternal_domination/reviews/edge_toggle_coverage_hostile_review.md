# Hostile review: edge-toggle coverage and isomorphism audit

Date: 2026-07-25 (America/Los_Angeles)

## Verdict

**ACCEPTED for the delimited coverage claim, with one LOW operational
finding.** I found no critical, high, or medium soundness defect. The package
independently covers the intended 391 seeds and all 25,641 unordered
one-edge toggles, reconstructs every raw graph byte for byte, and verifies an
explicit raw-to-stored-key isomorphism for every origin. It reconciles all
19,136 stored keys, multiplicities, first origins, seed stream hashes,
exports, and candidate-free database state.

This verdict is about coverage, reconstruction, and storage consistency. It
does not independently establish the stored values of `gamma`, `alpha`,
one-guard `gamma_infinity`, or `theta`; those values require the separate
mathematical audit. It also does not turn this bounded search into a
resolution of the universal gamma-theta conjecture.

## Reviewed scope and independence

I read all files in `src/edge_toggle_coverage_checker/`, both dedicated test
files, the production SQLite database and checkpoint, both CSV exports, the
extension seed table and its two prior audit reports, and the completed
receipt database and JSON report. The checker does not import the search
engine, verifier A, verifier B, nauty, or the earlier coverage checker.

I also wrote `reviews/edge_toggle_coverage_hostile_probe.py`. Its main
reconstruction uses only the Python standard library: it independently
decodes and encodes graph6, selects the source rows, constructs
`itertools.combinations(range(n), 2)`, toggles the exact adjacency bit,
checks raw bytes, directly verifies each saved permutation edge by edge,
recomputes the complete receipt chain, reconciles multiplicities and first
origins, compares both CSV exports to SQLite, and checks candidate absence.
The second part applies mutations to temporary copies and calls the
checker's fail-closed validation paths.

## Independent reconstruction result

The independent reconstruction obtained:

- 391 selected seeds: 285
  `eternal_false_without_private_obstruction` and 106
  `private_obstruction_eternal_false`;
- order census 15 at order 11 and 376 at order 12;
- exactly
  `15*binom(11,2) + 376*binom(12,2) = 25,641` scheduled origins;
- all 25,641 raw graph6 strings equal to an independently reconstructed
  one-bit toggle;
- all 25,641 receipt mappings are permutations in the correct
  raw-to-canonical direction and preserve every adjacency/nonadjacency;
- 19,136 used stored keys and no unused canonical row;
- receipt-chain SHA-256
  `d00dff4e6e0ad40b37e14da89c5deb2616ed10e39b08c81b1d5837723df1f5bb`;
- all production and receipt multiplicities and first-origin records agree;
- both CSV exports agree field for field with the production database;
- empty production candidate marker, zero candidate-category origin and
  canonical rows, and an empty designated production candidate directory.

The independently counted unique parameter tuples `(gamma, alpha,
gamma_infinity, theta)` were:

| tuple | unique keys |
|---|---:|
| `(3,3,4,4)` | 8,587 |
| `(2,3,4,4)` | 6,751 |
| `(3,4,4,4)` | 2,615 |
| `(2,3,3,3)` | 1,143 |
| `(2,3,3,4)` | 40 |

They total 19,136. All stored categories are `gamma_below_eternal`.

## Adversarial checks

### Scope and seed selection

The checker pins the exact seed CSV and both prerequisite audit reports. It
parses all 54,216 rows, rejects duplicate stored keys, recomputes graph order
and size, and selects the two intended categories in file order. It checks
the exact category census, the 391-row selection, the two order counts, and
the 25,641-origin arithmetic. The production seed table must then agree
row-for-row with the independently assigned `ET-0001` through `ET-0391`.
A byte mutation of the source CSV was rejected.

### Pair indexing, raw reconstruction, and graph6 strictness

Both production and checker use the lexicographic order supplied by
`combinations(range(n), 2)`. The checker compares seed index, seed ID, pair
index, and both endpoints at every global position before reconstructing the
action and raw graph. Mutations of the pair index, endpoint, add/delete
action, raw graph6, and stored key were all rejected.

Canonical and raw production records are forced to be headerless,
single-record, small graph6 data with zero padding. Malformed lengths,
extended headers, nonzero padding, and empty data were rejected. The
standalone decoder independently reproduced every raw record.

### Isomorphism direction and completeness

`find_isomorphism(left, right)` stores an old-left-to-new-right permutation.
The backtracker has no heuristic or node cutoff. Its pruning invariants
(degree, triangle count, neighbor-degree multiset, distance profile, and
joint color refinement) are isomorphism invariants, so they cannot prune a
genuine isomorphism. The final edge-by-edge verifier makes false positive
answers impossible. Random relabeling tests, brute-force order-five
comparisons, and a non-self-inverse direction probe passed. An intentionally
wrong-direction permutation was rejected.

The stated limitation is accurate: the checker proves that every raw origin
is isomorphic to its stored key but does not independently prove that
distinct stored keys are nonisomorphic. Duplicate isomorphic stored keys
would add redundant evaluations; they cannot omit an origin or create the
reported absence of a candidate.

### Multiplicity, receipts, and resumption

Every saved receipt is replayed from global index zero. The replay
reconstructs the production row, directly verifies the saved mapping,
recomputes a domain-separated hash chain, and rebuilds all canonical
multiplicities. It does not trust the progress counter alone. Mutations of a
canonical count, a saved mapping, and a receipt-chain entry were each
rejected.

A fresh isolated audit built 25,641 receipts from no prior state and
completed. A second run on that completed isolated state replayed all
receipts and returned the same chain and counts.

### Search artifacts, exports, candidate absence, and input mutation

The production database is refused if SQLite journal/WAL/SHM companions
exist, is opened read-only with `immutable=1`, and is checked for integrity,
foreign-key violations, table set, column order, and schema version. The
checkpoint binds the exact database bytes, configuration, complete seed
summaries, exports, and internal coverage census. The checker separately
reconciles the exports with SQLite.

All ordinary bound inputs and source manifests are recomputed before the
state is marked complete. A temporary provenance mutation changed the final
binding and would fail the initial/final equality check. The actual
production candidate marker, candidate-category rows, checkpoint candidate
state, and designated directory were all empty.

## Finding

### LOW: candidate-directory contents are not included in the final rebinding

`_validate_no_candidate_freeze` checks the caller-supplied candidate
directory once, but the production configuration does not record that
directory and `_audit_binding` binds only its path string, not its directory
contents. Consequently:

1. a caller can supply a different empty directory to the audit CLI; and
2. a file created in the checked directory after the initial absence check
   is not detected by the final concurrent-mutation rebinding.

The hostile probe demonstrated the second behavior. This does **not**
undermine the present finite result: the report uses the intended default
directory, that directory was empty when inspected, the immutable database
and checkpoint contain no candidate marker or candidate row, and the
independent reconstruction confirmed the same. It is nevertheless a real
TOCTOU/provenance weakness in the ancillary freeze-directory assertion.

Recommended repair for future runs: put the resolved candidate-directory
path into the production configuration, require the audit path to equal it,
and include an exact sorted directory-entry manifest in both the initial and
final audit bindings (or re-run the emptiness check immediately before
completion).

## Executed tests and runtimes

- Dedicated unit tests: 13/13 passed in 1.406 seconds.
- Hostile standard-library reconstruction plus mutation probes: passed in
  approximately 5.8 seconds.
- Fresh isolated receipt build:
  `/private/tmp/edge-toggle-hostile-full.1hgtdL`, complete in 16.768 seconds,
  maximum RSS 64,765,952 bytes, state SHA-256
  `9ac22bb722c406b0442dfaca59771fad9372a4cde7665cbb0f9988e76f7aa0ac`.
- Complete-state replay of that isolated build: complete in 4.931 seconds,
  maximum RSS 83,951,616 bytes; the state bytes and origin-chain digest were
  unchanged.

### Audit-run artifact note

During this hostile review I mistakenly performed one complete-state replay
against the default report path before switching to isolated temporary
paths. That replay did not change the receipt-state database (its SHA-256
remained
`b22618f266f39e2cb422fe30e942f678f2b52c3bed973df12657c66660b7693d`)
or any mathematical/coverage result, but it atomically rewrote the JSON
report's run timestamps and resource fields. The report SHA-256 therefore
changed from
`3a687fe78ea6946d77f64487df77c9610c637a7789c657fa4d4f3b0a12e7dc9f`
to the final frozen
`82c6918faec2105340205730a3e128d4be05b5c57190a58519e68b4cfe733679`.
No further default-path replay was performed.

## Frozen hashes reviewed

- production database:
  `2a6349452906cf2904a5e9e6284806f603619ad28ec66fa63fc383f2b833b258`
- production checkpoint:
  `f00b404fdfc09ac95f8b56325ef58a3399559b33eb1b659e304fdc81ed512ffc`
- provenance CSV:
  `378e867d5ec0d419f668f5169dbac6f2319cd2afc9ce3c5f63da2b9677dccba5`
- unique CSV:
  `a32505df6ba67479b5908a91711d21babb14fd8ac50cdfd0f0b92fc1001d4319`
- completed coverage state:
  `b22618f266f39e2cb422fe30e942f678f2b52c3bed973df12657c66660b7693d`
- final coverage report:
  `82c6918faec2105340205730a3e128d4be05b5c57190a58519e68b4cfe733679`
- checker source-set (as bound in the report):
  `46a5a684581678a5401502fff37a6da5df89657198694eb7401d4323e5730343`
- hostile probe:
  `20a97caa8ba42edbc16e3abdd592c58e753326fbaa9e9002289d41a0d2b167ab`

## Acceptance boundary

Subject to the separate mathematical evaluator audit, the coverage package
supports the precise finite statement:

> Every one-edge addition or deletion from each of the exact 391 selected
> extension seeds was represented among the 25,641 origin rows, and every
> origin maps by an explicitly checked isomorphism to one of the 19,136
> evaluated stored keys. No stored key is categorized as a counterexample.

It does not prove absence of a counterexample elsewhere at order 11 or 12,
does not prove a complete `n=12,k=3` slice, and does not resolve the
conjecture.
