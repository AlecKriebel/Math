# Independent package audit of the retained `hole5` binary run

Date: 2026-07-25 PDT

## Verdict and boundary

**`PASS_EXACT_RETAINED_PACKAGE`; no new mathematical claim.**

The exact twelve-file run at
`results/synthesis_k3_hole5_signature_seed0_600s_binary` is internally
coherent, completely hash-bound, durably preserved in Git, and independently
reproducible at the certificate-checking level.  This package audit supports
the already delimited `CERTIFIED-FINITE` result for the exact
S6-signature-broken induced-\(C_5\) branch.

This audit does **not** certify the whole \((n,k)=(12,3)\) slice, another
template branch, another order or parameter, or the universal
\(\gamma\)--\(\theta\) conjecture.  It did not rerun the original SAT solver.
The decisive computational evidence is the retained proof and a fresh strict
proof-checker replay.

## Standalone reproduction artifacts

| artifact | SHA-256 |
|---|---|
| `reviews/hole5_binary_run_package_auditor.py` | `5e4f9fbeec4c95900df82af6a6af277a9522ad245f96c8ab9815f63c78a10984` |
| `results/logs/hole5-binary-run-package-audit.json` | `470f58bf532ae8ff68ac3b8f096ba20166e6bcd91bee4924c1f924e276fea2cb` |

The auditor is a Python-standard-library program.  It imports no search,
production-runner, proof-parser, or certificate implementation.  Two full
temporary-output executions and the permanent-log execution produced
byte-identical canonical JSON with the hash above.

Run it from the campaign directory with a fresh output path:

```text
python3 reviews/hole5_binary_run_package_auditor.py \
  --output /tmp/hole5-binary-run-package-audit.json
```

The auditor uses the campaign-wide one-heavy-child lock for its parser and
checker subprocesses.  It refuses to overwrite an existing output path and
never writes inside the audited run directory.

## Provenance and tree closure

The exact runtime source boundary comprises 23 files at source commit

`6f3ef0a0970b7214c34018fe32ea1ceeb5764d17`.

Every current file was compared with both its expected digest and the exact
Git object at that commit.  The independently recomputed ordered source-set
digest is

`ab4a918526e4e6482ee895439bf805681a39003d24ccf10d7c93bd0482dcf24b`.

The untouched run is frozen at package commit

`dff45f4239e4acabc461533a0a213beec18ec56d`.

Its exact Git subtree is

`aaef13bba428f8722ad167158360da831a7d1998`.

The auditor requires this to be a `040000 tree`, enumerates exactly twelve
`100644 blob` entries, reads every blob from that commit, and compares every
payload byte with the working copy.  It also verifies the source/package
ancestry and that the package commit is contained in current `HEAD` and
`origin/main`.

The working output tree contains exactly twelve regular single-link files.
There are no unbound entries and no `.partial`, temporary, or lock artifacts.
Its sorted length-delimited tree digest is

`16f7e62e48a6c2ddb5cf1930f10f72c90256d477f33d745f77e87f0a0fb4b1a2`.

The directory and files remain owner-writable.  This is recorded rather than
hidden: physical write protection is false.  The durable Git commit binds all
twelve payloads, names, types, and Git modes, so later working-tree mutation
is detectable.  No hash-binding gap remains inside the stated boundary.

## Independent formula reconstruction

The auditor parses the exact DIMACS input, checks 6,886 variables, 23,968
clauses, and 192,169 literals, and obtains SHA-256

`c6a0811c718ff8e9352f253e4ce225ce2826def9c3e4a9cd55f0b0152703d104`.

It independently reconstructs the edge-variable map and all 315 S6
signature-order clauses.  The reconstructed suffix has 3,210 literals,
11,424 bytes, and SHA-256

`ddd32969558030c22b7b4f182dfd9f96b65bb572a7e240957d202fb32b0158c6`.

It then reconstructs the full derived CNF byte-for-byte from the updated
header, the exact source clause body, and that suffix.

## Independent proof handling and replay

The auditor has a separate binary-DRAT parser.  It enforces canonical
base-128 varints, exact addition/deletion record syntax, variables in
`1..6886`, no duplicate or complementary literals, no empty deletion, and
one final empty addition.

It checks:

- raw proof: 493,420 records, 12,524,020 bytes, SHA-256
  `c17ed1ee2782270ed861462ae7bdd94420a2079edf419a7d778d7096a67d1be4`;
- addition-only proof: 247,981 records, 6,337,621 bytes, SHA-256
  `c6c24853e30073e66fb396441edb176a0160d062a8558e25fa18a955f33927c3`;
- every raw-proof addition byte occurs in exact order in the retained
  addition-only proof; and
- both independent statistic records agree exactly with the retained parser
  report.

In a private scratch directory under `results/logs`, the auditor reruns the
pinned clean-room stripping parser and requires byte-for-byte equality with
the retained addition-only proof and parser report.  It then runs the pinned
checker with strict binary, forward, warning-fatal, RUP-only options:

```text
drat-trim instance.cnf proof.additions.bdrat -i -f -W -U -t 1200
```

The checker exits zero, emits empty stderr, reports exactly one `s VERIFIED`,
and reports zero RAT lemmas.  Only its elapsed-time number is normalized when
the fresh transcript is compared with the retained transcript.

## Structured records and remaining limitations

The canonical schemas and exact hashes of `run_config.json`, `outcome.json`,
and `certificate.json` are checked, including their cross-links, complete
artifact map, activation relation, tool identities, command hashes, resource
records, exit codes, and failure flags.

The original configuration contains absolute paths.  This audit therefore
binds the exact current checkout; it does not claim that the original
production invocation is path-relocatable.  The original solver is not
rerun because the retained proof is independently parsed and strictly
replayed.

The separate clean-room hostile post-run audit reached verdict
`ACCEPT_C5_UNSAT_CERTIFICATE_FOR_C033`:

| artifact | SHA-256 |
|---|---|
| `reviews/hole5_binary_production_postrun_hostile_probe.py` | `e480f7a27b5e5424b6ba7507a85a57144949f974b37351ee0872cca1ba8a7937` |
| `reviews/hole5_binary_production_postrun_hostile_probe_log.json` | `bd7693fdad225f733c0d2e704c4de45186324cc62ffdec09a112836ceec014e5` |
| `reviews/hole5_binary_production_postrun_hostile_review.md` | `060c65bbc5b08f562289dcf43e36924d34a0ae90ae2cc72c895c59b7eaf916a3` |

Within the exact retained-package boundary, this audit found no open
provenance, schema, hash-coverage, transient-file, parser, deletion-stripping,
checker, or reproducibility blocker.
