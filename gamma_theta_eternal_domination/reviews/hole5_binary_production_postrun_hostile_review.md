# Clean-room hostile review of the `hole5` binary production result

## Verdict

**`ACCEPT_C5_UNSAT_CERTIFICATE_FOR_C033`.**

The exact retained `hole5` S6-signature-broken CNF is certified UNSAT.  The
certificate side of the C033 activation gate is satisfied.  In conjunction
with the separately reviewed complete-bank and S6 coverage results, this
certifies the finite C5 branch; it is not a universal resolution of the
gamma--theta conjecture.

This verdict does not trust or import
`src/synthesis_k3/hole5_binary_production.py`.  The original solver was not
rerun.  The decisive evidence is the retained proof, parsed independently
from its binary bytes and replayed from scratch by the pinned proof checker.

Review date: 2026-07-25 PDT.

## Decisive audit artifacts

| artifact | bytes | SHA-256 |
|---|---:|---|
| `reviews/hole5_binary_production_postrun_hostile_probe.py` | 61,778 | `e480f7a27b5e5424b6ba7507a85a57144949f974b37351ee0872cca1ba8a7937` |
| `reviews/hole5_binary_production_postrun_hostile_probe_log.json` | 24,943 | `bd7693fdad225f733c0d2e704c4de45186324cc62ffdec09a112836ceec014e5` |

The probe is a standalone Python-standard-library implementation.  It imports
neither the production runner nor any synthesis module.  A stdout-only run
and the permanent-log run each performed a fresh strict proof replay and
produced byte-identical canonical JSON with the log hash above.

The reproducibility gate caught one nonmathematical issue during audit: an
early draft recorded the randomized temporary pathname used for parser
output.  Both proof replays in that draft verified, but their enclosing JSON
hashes differed.  That provisional log was deleted, the temporary pathname
was normalized to `<TEMP>/additions.bdrat`, and the two final full runs then
matched byte-for-byte.  No proof byte, formula byte, parser result, or checker
result changed.

The canonical log has schema
`gamma-theta-hole5-binary-postrun-hostile-audit-v1`, records verdict
`ACCEPT_C5_UNSAT_CERTIFICATE_FOR_C033`, and explicitly records
`production_runner_imported_or_trusted=false` and
`production_solver_launched=false`.

## Exact formula and S6 reconstruction

The clean-room probe parsed the source and derived DIMACS files directly and
rejected malformed headers, clauses, literals, duplicate literals,
tautologies, out-of-range variables, and noncanonical line structure.

| formula | variables | clauses | literals | bytes | SHA-256 |
|---|---:|---:|---:|---:|---|
| complete source bank | 6,886 | 23,653 | 188,959 | 742,899 | `76bf36ecb663cd37272acded2208206fdba6aa571dd5f2e757cc132bd533e0b7` |
| S6-strengthened formula | 6,886 | 23,968 | 192,169 | 754,323 | `c6a0811c718ff8e9352f253e4ce225ce2826def9c3e4a9cd55f0b0152703d104` |

Without consulting the author implementation, the probe reconstructed the
edge-variable map and all 315 lexicographic signature-order clauses.  The
suffix has 3,210 literals, 11,424 bytes, and SHA-256

`ddd32969558030c22b7b4f182dfd9f96b65bb572a7e240957d202fb32b0158c6`.

Its clause-length distribution is

```text
2:5, 4:10, 6:20, 8:40, 10:80, 12:160.
```

For each adjacent free-vertex pair

```text
(6,7), (7,8), (8,9), (9,10), (10,11),
```

all 4,096 pairs of six-bit signatures were evaluated.  Each comparator
accepted exactly 2,080 nondecreasing pairs and had zero truth-table
mismatches.  The probe then proved byte-for-byte that

```text
derived CNF
= updated DIMACS header
+ exact 23,653-clause source body
+ exact independently reconstructed 315-clause suffix.
```

As an independent regression, the previously accepted retained-package probe
was launched in a separate isolated process.  It exited zero, emitted empty
stderr, and reproduced its accepted canonical log, SHA-256
`58edf995b84de703c466e956f47d50443de025fa8b5c5268d781f8962a39d694`,
byte-for-byte.

## Independent binary-proof parse

The decisive proof artifacts are:

| proof | records | additions | deletions | bytes | SHA-256 |
|---|---:|---:|---:|---:|---|
| raw binary DRAT | 493,420 | 247,981 | 245,439 | 12,524,020 | `c17ed1ee2782270ed861462ae7bdd94420a2079edf419a7d778d7096a67d1be4` |
| addition-only binary DRAT | 247,981 | 247,981 | 0 | 6,337,621 | `c6c24853e30073e66fb396441edb176a0160d062a8558e25fa18a955f33927c3` |

The post-run probe contains its own streaming parser rather than calling the
accepted parser for these statistics.  It checked record prefixes, bounded
and canonical varints, literal signs and range, duplicate and complementary
literals, empty-record placement, and complete EOF.  The maximum variable was
6,886.  The one empty addition was the final record in each stream.

The raw proof contains 4,372,774 addition literals and 4,298,890 deletion
literals.  Its first deletion is record 96.  The exact deletion-byte stream
has 6,186,399 bytes and SHA-256
`9a26725ceb8ddb4bdbec3e9397d796f4bed94288a9ba2a8a014cb2e7694e6711`.

Most importantly, the independent parser compared every raw addition record
directly against the retained addition-only file while streaming.  The
6,337,621 addition bytes are an exact, in-order subsequence of the raw proof;
no literal was decoded and re-encoded for this comparison.  There are no
unmatched leading or trailing bytes.

The separately accepted parser, SHA-256
`02c3c00faf7afb91a3217f5b738d0dacf7699875928162d01ce2df97e600007d`,
was then run in an isolated Python process against the raw proof.  Its report
was byte-identical to the retained report and object-identical to the new
parser's statistics.  Its newly stripped proof was byte-identical to the
retained addition-only proof.  Thus neither implementation solely validates
its own deletion stripping.

## Fresh strict RUP replay

The pinned checker has SHA-256

`31df522b8b2b71acd357723b0e826cf488826ed78ad9e3a7bcad241271812beb`,

with source archive SHA-256

`2ac28cd9e38e050b4f78fbff0efd4a1aa2349d157aef08c9b1fb6c7139949108`.

Each final audit pass launched the exact command

```text
drat-trim instance.cnf proof.additions.bdrat -i -f -W -U -t 1200
```

under the campaign-wide one-heavy-child lock and a 2 GiB address-space limit.
The checker exited zero with empty stderr.  Its normalized stdout has SHA-256

`7562757d554c11f8cead844c8fc5f6a93fc72eb9a2b3d5ec68c3bcd6ad5fc1b2`

and reports:

```text
c turning on binary mode checking
c parsing input formula with 6886 variables and 23968 clauses
c finished parsing, read 6337621 bytes from proof file
c start forward verification
c 18740 of 23968 clauses in core
c 148710 of 247982 lemmas in core using 10912555 resolution steps
c 0 RAT lemmas in core; 0 redundant literals in core lemmas
c optimized proofs are not supported for forward checking
s VERIFIED
c verification time: <ELAPSED> seconds
```

Only the elapsed-time number is normalized.  Every semantic line agrees
exactly with the retained checker transcript.  The explicit options enforce
binary input, forward checking, warning-fatal operation, and RUP-only
checking.  Zero RAT lemmas were used.

This replay, rather than the original `s UNSATISFIABLE` solver result, is the
mathematical basis for the UNSAT verdict.

## Frozen output tree and Git provenance

The run directory has mode `0700` and contains exactly twelve regular,
single-link artifacts; no transient or unbound entry exists.  Their total
payload is 18,897,622 bytes.  The sorted length-delimited path/payload tree
has SHA-256

`16f7e62e48a6c2ddb5cf1930f10f72c90256d477f33d745f77e87f0a0fb4b1a2`.

The decisive structured anchors are:

| artifact | SHA-256 |
|---|---|
| `run_config.json` | `6d899e212d2f349b48eefad5037ea007981a331b7e581966165ae861c741221b` |
| `certificate.json` | `f54d7bf8a50f24e3a5084442d84f07548a60401faca8ec18bfd07f24f0e337e8` |
| `outcome.json` | `ea2ea36321a786aa40aff1e68587474bbdba5402abc800b1a0816d65b6df8df4` |
| `checker.stdout` | `582074fe80efc122bef5586bc9768e32dfbb3a7bb5758f04b5fe23d0862b6515` |
| `parser.stdout` | `435ac813fbc0a345816256397bccf9a3f0dc662f3e4a338cc3cc31bd25c19fe1` |

The original run binds its 23 runtime sources and six package inputs to source
commit

`6f3ef0a0970b7214c34018fe32ea1ceeb5764d17`.

The independently recomputed ordered runtime-source-set SHA-256 is

`ab4a918526e4e6482ee895439bf805681a39003d24ccf10d7c93bd0482dcf24b`.

Every current runtime/package file was compared both with its expected hash
and with the exact Git blob payload at that source commit.

The untouched twelve-file run is durably frozen at preservation commit

`dff45f4239e4acabc461533a0a213beec18ec56d`.

That commit has root tree

`7e2e9e6c056f4c1460d260f0e266dfa59d510cc4`,

and the exact run-directory Git tree is

`aaef13bba428f8722ad167158360da831a7d1998`.

The probe resolves and records all twelve individual Git blob IDs, reads each
blob directly, and requires byte-for-byte equality with the audited working
copy.  The hard-coded subtree ID also cryptographically binds the entry names,
types, modes, and blob IDs.  The source commit is an ancestor of the
preservation commit, and the preservation commit was confirmed as an ancestor
of both current `HEAD` and `origin/main`.

## Certificate activation and recorded execution

The replay certificate deliberately has status `UNSAT_REPLAY_ARTIFACT` and
claim status `NO_STANDALONE_MATHEMATICAL_CLAIM`.  The final outcome has status
`UNSAT_VERIFIED_FINITE_CERTIFICATE`, claim status
`VERIFIED_FINITE_CERTIFICATE`, and an empty failure list.

The outcome's complete artifact map binds every retained file other than the
outcome itself by exact size and SHA-256.  In particular, it binds the exact
certificate hash above, satisfying the certificate's recorded
self-activation condition.  The probe reconstructed and checked that
activation relation rather than trusting either status string alone.

The recorded solver, parser, and checker command arrays and their canonical
command hashes are exact.  Their exit codes were respectively 20, 0, and 0;
none timed out, received a signal, exceeded its memory/file limit, or emitted
stderr.  The solver's exact result file is `s UNSATISFIABLE` followed by one
line feed.  Resource records and executable hashes before and after every
child agree with the frozen configuration.

## Claim boundary

Accepted as `CERTIFIED-FINITE`:

- the exact retained S6-strengthened `hole5` CNF is UNSAT;
- the raw proof and exact addition-only subsequence are well formed;
- the addition-only proof is a warning-free forward RUP certificate for that
  exact CNF;
- the run output, activation records, source inputs, tools, and durable Git
  objects are coherently bound; and
- the certificate may activate the separately reviewed C033/C5 branch
  exclusion.

Not accepted by this audit alone:

- any assertion about formulas outside the exact retained complete-bank/S6
  package;
- the C7 branch or any other template branch;
- completeness of the whole \((n,k)=(12,3)\) slice without the separate
  mathematical coverage argument and other branch certificates;
- exclusion at another order or parameter; or
- resolution of the universal gamma--theta conjecture.

Within that boundary, no open certificate, provenance, parser, checker,
deletion-stripping, activation, or reproducibility blocker remains.
