# Independent artifact and code audit of PR #872

Problem 30006628 / OWR-14299911-031. Audit completed 2026-10-15 UTC.

**Disposition: the immutable historical artifacts authenticate and reproduce.**
The historical wrapper has a limited, accurately identifiable coverage boundary
and an input-availability weakness. A new publication package should supply its
own complete external inventory and safe source-reader rather than silently
present the old wrapper as a complete publication validator. No original file
was repaired or changed in this audit. This is an AI artifact audit, not an
asymptotic mathematical proof, a priority audit, formal verification, or human
peer review.

## Claim, independent scope, and trust anchor

The frozen original claims an all-length asymptotic property-(T) result for at
least three fixed factors, fixed finite inverse-closed generating alphabets,
and fixed density strictly between 1/3 and 1. Its own proof says explicitly that
finite diagnostics cannot certify this theorem. This audit checks the narrower
claims that the published bytes are the frozen submitted bytes, the runnable
programs implement their stated finite diagnostics, provenance inputs match
their pins, and the recorded outputs and advertised mutation controls can be
reproduced.

The parent supplied a frozen manifest for head
`e3d77731b45b5f463df46e769faa01d65fe193ec`, source prefix
`random_property_t_30006628/`. Its SHA256 is
`4589f9b70e9a65ae67356544b5ad59644290902bb9b3df80406710a22559e3f8`.
I computed each of the 15 Git blob identifiers using
SHA1(`blob ` + decimal byte length + NUL + bytes), independently computed each
SHA256 and byte count, and matched all against that manifest. This establishes
consistency with the supplied frozen trust anchor. I did **not** independently
fetch GitHub Git objects or prove which remote commit contains those objects;
the parent must retain its separate remote freeze/acceptance evidence.

I read the complete 8,583-byte historical wrapper and all four distinct archived
Python programs **before** executing them. I did not consult the other current
audit families' reports or verdicts, change the queue, run Git commands, contact
anyone, or write outside this audit's dedicated directory. Temporary fixtures
and code extraction reside under its ignored `private_work/` or automatically
removed temporary directories.

## Authentication and source reproduction

All 15 frozen loose files authenticated; the outer publication manifest covers
the other 14 files exactly, excluding itself as stated. Each external archive
manifest binds its corresponding archive and all its members. I verified exact
member sets, duplicate absence, safe relative paths, ordinary member metadata,
bytes and hashes. The inventories are 12 author members, 7 first-audit members,
and 7 second-review members, for **26** total. The three loose proof/review
copies are byte-identical to their archived counterparts. All originals were
reauthenticated after the probes and replay.

The original proof remains 19,961 bytes, SHA256
`3bed7a81c5562d793bc4991fe62e1c06703818a9046495a7fe96d0b38e1ac100`.
The historical wrapper remains 8,583 bytes, SHA256
`11ca693b078d4616b34af6d340327b6dfc262d995a2f1c73b2b1bd4ff1f44eeb`.
The wrapper was authenticated against this external pin before subprocess
execution. A same-directory mutable manifest alone is not an independent trust
anchor; the original README already explains this correctly.

I independently checked all bytes of the supplied catalog, problem corpus and
research-results corpus against the archived `sources.json` pins. I parsed
these with duplicate-key rejection, selected the complete unique exact-ID
problem record, joined the report by its full problem number, and reproduced
the original canonicalization using Python's default `json.dumps` separators
and `sort_keys=True`. The complete pair is 3,767 bytes, SHA256
`f49c17584ada1a931294e4222414fc5b57ee1d60afca82d6818029457badf17f`.
It matches the unique catalog record's review hash, and the report record is
empty. No field projection or related-group substitution was used.

All six locally supplied primary PDFs match the archived byte counts and
SHA256 pins. This verifies the supplied PDF bytes; I did not retrieve them
again or review their mathematical content here. The parent's fresh retrieval
and the source-scope audit provide those separate evidentiary steps. The raw
corpora, PDFs and extracted text are not included in this audit's public files.

## Code review and finite diagnostic scope

The original code uses explicit `require`, `check`, `Failure`, or `ValueError`
branches rather than correctness assertions removed by `-O`. It uses standard
library integer, counter, and rational arithmetic for its finite tests; there
is no network operation or empirical random simulation in these programs.

| Code | What was read and checked | Exact finite scope reproduced |
|---|---|---|
| `checker.py`, SHA256 `4c101fe4a2e9ce158a56337a4f26b8ac9673e457530e08f4de8eec7f0016451f` | Inverse alphabet construction, cyclic syllable-word enumeration, inverse-fixed block removal, oriented corner counts, aggregate endpoint kernel, rational positive-definiteness check, deliberate mutations | 13 kernel cases; 12 limiting model cases; 54 finite-index suffix witnesses |
| `verify_sources.py`, SHA256 `1129e5e581dd9bbac841c363c0429e8cbc774a766b70dfcc39d3f0ba084a81e4` | Complete-file source pins before parse, exact-ID uniqueness and complete-record pair recipe, catalog binding, six PDF pins | 3 corpus files, 6 PDFs, exact complete-record pair; two intentional pin errors |
| `independent_kernel_check.py`, SHA256 `8979841d646328eea63a1b8969e3f0fef5e680a9d13586549e8a34950ce7b783` | Separate product enumeration, per-vertex rather than aggregate corner counts, inverse conventions and six oriented incidences per retained relator | 13 cases, including self-inverse and paired inverse alphabets |
| `independent_checks.py`, SHA256 `2458d9a1a8cb36f00dfddb71d712f93f068ee9f00bb73b2085e9c7ad679af5a1` | Recursive word enumeration, loop and degree tests, parallel-edge accounting, entrywise kernel identity, reversal symmetry, frozen author archive/proof bindings | 23 cases and 50,652 individual matrix entries |

The author checker's positive-definiteness routine is exact rational symmetric
elimination. For the finite graphs used, its matrix is
`D - 2A + 2dd'/vol`, so its strict positive-definiteness test expresses the
claimed normalized-Laplacian gap greater than one half after treating the
constant direction separately. This does not establish the spectral limit,
the Perron estimates, matrix concentration hypotheses, the property-(T)
criterion, or finite-index transfer for every large length. Those are proof
obligations for the mathematical audit, not covered by matching the above
finite cases.

The `critical_density` negative diagnostic deliberately tests the false
inequality `1/3 > 1/3`; it is a guard demonstration, not evidence about the
actual critical-density problem. Similarly, a finite two-factor gap diagnostic
does not resolve the excluded two-factor theorem. The publication must retain
these distinctions.

## Reproduction and classified adversarial controls

`adversarial_probes.py` is a public, reproducible harness. I ran it using Python
3.14.6 with `-I -S -B`, and repeated the harness with `-O`. It authenticates the
supplied frozen manifest and all sources before using archived code. Its outer
wrapper launches use `-I -S -B`; the unchanged historical wrapper internally
launches its diagnostics using its original `-I -B` and normal/optimized modes.

Both harness runs launch the full-source historical wrapper once normally and
once optimized. Each such wrapper launch internally runs both child modes and
contains 8 positive diagnostic receipts and 12 intentional negative diagnostic
receipts. All four outer full-source launches reproduce the exact same
7,619-byte output, and each parsed result equals the historical
`PREFLIGHT_VALIDATION.json`'s complete `replay` object. These counts are repeated
reproduction events, not additional independent mathematical cases.

Per harness run, the additional public probes are classified as follows:

| Classification | Count | Meaning |
|---|---:|---|
| Ordinary expected rejections | 28 | Nine pinned-file corruptions in each mode; missing, leaf-symlink, directory and FIFO core inputs in each mode; incomplete source arguments in each mode |
| Startup rejections before execution | 2 | Modified wrapper rejected against external pin; marker code never runs |
| Artificially resealed parser rejections | 5 | Duplicate manifest member, traversal path, absolute path, backslash path, ZIP symlink metadata |
| Positive controls | 5 | Two baseline verify-only runs, independent full source binding, two full-source wrapper runs |
| Accepted out-of-scope outer mutations | 12 | Five unpinned outer-file alterations and one extra file in each mode |
| Accepted directory aliases | 2 | A package-directory symlink is followed; only leaf core symlinks are rejected |
| Accepted resealed ZIP metadata | 1 | ZIP FIFO mode metadata is not explicitly rejected, although replay writes its authenticated bytes as a regular temporary file |
| Confirmed pre-read source guard gaps | 2 | Supplied catalog FIFO blocks until a one-second process timeout in each mode |

The original ten publication-integrity controls are reproduced in substance:
archive corruption, external-manifest corruption, proof alteration, missing
second archive, and changed-wrapper rejection, each in both modes. They are a
subset of the classifications above. Thus the ten original controls are not
merely accepted from a historical assertion. The 12 internal checker/source
negative receipts per wrapper launch are separate from these publication
controls and are not double-counted in the table.

The artificial parser tests deliberately replace the trusted module's in-memory
pin entries solely to reach otherwise hash-inaccessible parser branches. They
are **not** successful attacks against immutable external pins. The historical
source FIFO test demonstrates absence of a pre-read file-type check and an
availability issue, not execution of unauthenticated source code. The harness
terminates the blocked process and removes its temporary fixture.

## Historical boundary and recommendations for the new package

1. **Coverage.** `verify_publication.py` authenticates nine hard-coded core
   files, their archive members, and the readable duplicates. It does not
   authenticate the README, acceptance, preflight, queue delta, outer manifest,
   itself, or a closed inventory of extra outer files. Its own returned
   `core_file_count: 9` is accurate. The outer publication manifest covers those
   files, but a user must obtain a trusted external pin for that manifest and
   the startup verifier. The current independent audit authenticated all 15
   through the supplied external frozen manifest. A new package should have a
   complete explicitly pinned inventory and a separately trusted startup pin.
2. **Safe source reads.** The historical source-reader directly calls
   `read_bytes()` on supplied corpora and PDF paths; it does not reject a FIFO
   or leaf source symlink first. Hashes still prevent changed source bytes from
   being accepted. A new portable wrapper should reject nonregular input files
   before reading them, state its ancestor-symlink policy, and bound reads to
   the pinned expected sizes. Preserve the historical source-reader unchanged
   as evidence rather than silently rewriting it.
3. **Archive parsing.** External archive/member pins authenticate the observed
   ordinary members. The historical parser rejects ZIP symlinks but does not
   insist on regular ZIP mode metadata and uses ordinary permissive JSON
   parsing. A new publication wrapper should use strict JSON/schema and regular
   member checks. Any claim of parser rejection should be restricted to the
   branches actually tested; the fixed historical pins greatly narrow the
   reachable input set.
4. **Runtime trust.** Python, its standard library, and the local installed
   runtime are assumed trusted. The original internal `-I -B` does not disable
   system `site` startup; a new all-standard-library verifier should use
   `-I -S -B`. No site-hook compromise was attempted or observed. This is a
   runtime hardening recommendation, not a demonstrated mathematical failure.
5. **Immutable history and finite evidence.** Keep the original 15 files and
   all 26 members byte-for-byte, including their historical pending-review or
   draft-only language. Add current wrappers and acceptance outside this
   history. Label these programs as finite diagnostics and integrity checks,
   never as proof or priority certificates.

There is no artifact mismatch or unexplained replay failure. The identified
wrapper limits do not falsify the theorem or the provenance pins. They should
be carried into the parent's new-package acceptance checks; this report alone
does not certify that future package, mathematical soundness, or priority.

## Reproduce this audit

Obtain the frozen original files, `SOURCE_MANIFEST.json`, and an externally
authenticated copy of this harness. From any working directory, run Python
with `-I -S -B` and pass `adversarial_probes.py` these arguments:
`--base` pointing at the audit parent directory containing `source/` and
`SOURCE_MANIFEST.json`, `--repo` pointing at the repository root, and `--output`
pointing at a new results file. Add `--full-sources` only when the three pinned
corpora and six pinned PDFs are locally available. Repeat with `-O` if desired.
No network, Git operation, original artifact execution before authentication,
or raw source redistribution is required.
