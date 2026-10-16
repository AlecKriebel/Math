# Binary directed chip-firing reachability: verification kit

This kit accompanies Alec Kriebel's *CoNP-completeness of binary directed
chip-firing reachability*, version 1.0, prepared on 15 October 2026. The full
proof is in `paper.pdf` and `paper.tex`. The theorem is ordinary legal
reachability coNP-completeness under deterministic polynomial-time many-one
reductions for **loopless strongly connected directed multigraphs**, explicit
binary adjacency, nonnegative binary initial/target configurations, and varying
vertex count. The proof makes no simple-graph, unary, bounded-degree,
bounded-chip-count or signed-membership extension.

The source hardness is Farrell-Levine; period deletion/reduced counts are
Björner-Lovász; coNP membership and recurrent-target results are
Hujter-Kiss-Tóthmérész; the earlier recurrence conversion and hierarchy barrier
are Tóthmérész; the prior large-reserve finite-horizon simulation is
Kiss-Tóthmérész 2015, Section 4. Exact-result, gadget and method priority,
independent discovery, and current worldwide openness remain UNKNOWN after
the bounded audit. This is an attributed complete proof of the historical
general-digraph hardness question. Historical open labels are not current
openness certificates. Read `SOURCE_AUDIT.md` for the precise comparison.

AI tools were used extensively in solving, checking, programming, source
comparison and writing. This work is unrefereed. Internal AI reviews do not
constitute human peer review, journal acceptance or proof-assistant
certification. As recorded at preparation on 15 October 2026, this candidate
had zero fresh whole-package reviews of this new preprint edition; at least
two are required by the publication process. `STATUS.json` is a dated
preparation record, not a timeless assertion about later events.

## Reproduce

Python 3.10 or later and its standard library suffice for all proof controls,
integrity checks and ZIP construction. Work in the extracted kit root. These
commands write only stdout:

```sh
python3 -B scripts/verify.py
python3 -B scripts/run_checks.py
python3 -O -B scripts/run_checks.py
python3 -O -B scripts/verify.py
```

Both check results must equal `EXPECTED_RESULTS.json` as complete JSON objects.
The controls are exact finite falsification checks; the universal theorem is
proved in the paper. There are no assert-dependent verification conditions.
The following deliberately fails in both modes:

```sh
python3 -B scripts/run_checks.py --inject-failure
python3 -O -B scripts/run_checks.py --inject-failure
```

`run_checks.py` is newly authored for this edition. It does not import the
original or review-family checkers. The original eight-file proof edition
distributed no executable, so these are not replays of its omitted historical
programs or aggregate counts. Results include exhaustive small state graphs,
all-order pre-gate invariants and cleanup transitions, unrestricted target
searches, an explicit pair of different target-reaching firing vectors,
signed/relay interfaces, singleton degree-zero cases, reduced-count negative
certificates, large-binary arithmetic and six deliberately broken variants.

Create a scratch parent outside the kit and the original canonical audit tree.
On macOS `/private/tmp` avoids the `/var` symlink used by some default temp paths:

```sh
scratch=$(mktemp -d /private/tmp/pr1097.XXXXXX)
python3 -B scripts/build_support.py --out "$scratch/support.zip"
python3 -O -B scripts/build_support.py --out "$scratch/support-optimized.zip"
python3 -B scripts/rebuild_pdf.py --out-dir "$scratch/pdf-normal"
python3 -O -B scripts/rebuild_pdf.py --out-dir "$scratch/pdf-optimized"
```

PDF regeneration additionally requires Tectonic and already cached standard
LaTeX resources. The script uses `--untrusted --only-cached`; it makes no
network request. It records the compiler output in the newly allocated
directory, checks for zero overfull boxes, and reports whether its PDF bytes
equal the distributed PDF. `SOURCE_DATE_EPOCH=1792022400` fixes the creation
date to 15 October 2026 UTC. Byte identity is an observed compiler/runtime
property, not a guarantee for every TeX installation. ZIP output is fully
deterministic: sorted flat member paths, stored compression, 1980-01-01
timestamps, Unix regular-file 0644 attributes, no comment or extra data.

Supported writers require fresh nonexistent output leaves outside protected
trees. Existing files, hardlinks, symlink leaves/ancestors, nested protected
paths, actual case/normalization aliases of protected directories, traversal
components and existing PDF-output directories are rejected
before writes. The PDF compiler receives only a newly allocated directory
and fixed copied source. Read-only commands have no file-output option;
caller-chosen shell redirection is outside their filesystem interface.
`PROTECTED_PATHS.json` retains the original canonical audit root as an
additional output guard even after extraction. It is not required to exist
and is not a dependency for verification or calculation. Existing protected
root identities are compared against every existing output ancestor, in addition
to lexical containment. This does not promise safety against hostile concurrent
filesystem mutation. The scripts create
no bytecode cache.

## Integrity and upload interface

`MANIFEST.json` is a self-excluded content inventory, not a digital signature.
The verifier checks a regular manifest and regular ancestry **before parsing
it**, all listed bytes, exact file inventory, consistent native metadata and
every selected authored custody copy. It rejects extra files. Keep generated
outputs outside the extracted tree. The original audit's own old manifests
are immutable historical records; their private/omitted paths are resolved
by the captured-stage decisions in `provenance/CUSTODY.json`, not by silently
claiming that every old source remains distributed.

The separate canonical delivery contains `paper.pdf`,
`pr1097_support_v1_0.zip`, `.zenodo.json` (bare native metadata),
`zenodo-metadata.json` (the metadata wrapper), `zenodo-deposit.json` (the exact
repository uploader schema), and `DEPOSIT_BINDING.json` (the external hash
binding). The bare kit metadata and all native wrapper metadata objects agree.
The external binding is excluded from the ZIP to avoid a hash cycle.

Default verification checks a sibling `DEPOSIT_BINDING.json` whenever it is
present. An extracted kit without that external file reports
`ABSENT_OPTIONAL`; this is not a check of the delivery assets. A present
binding is never silently skipped. To require delivery verification:

```sh
python3 -B scripts/verify.py --require-binding
python3 -O -B scripts/verify.py --binding /absolute/delivery/DEPOSIT_BINDING.json --require-binding
```

The explicit binding must be present and regular. Required mode fails when
it is absent. Present mode checks the canonical paper and ZIP hashes, the
kit manifest, exact asset names, native uploader file list, and all supplied
metadata objects. The repository's local command, from its root, is:

```sh
python3 zenodo_deposit_tool/zenodo.py check path/to/preprint_v1_0/zenodo-deposit.json
```

That `check` is local only. This kit does not perform staging, publication,
DOI registration, tracker mutation or a PR disposition. Ordered external
actions remain held at PR #1032 as recorded on 15 October 2026.

## Custody and license

`provenance/INPUT_PINS.json` hashes every preexisting regular audit file at
preparation start. `provenance/CUSTODY.json` makes an individual include or
exclude decision for each one. Selected authored records are exact byte
copies under `provenance/selected/`; third-party PDF bodies, extracted source
text, source pixels, environments and private caches are excluded. Reading
scopes and source hashes are metadata, not claims of full-source inspection
or equality between arXiv and publisher PDFs. Old status/acceptance/pending
fields remain dated history and do not override the new paper's qualified
attribution or later root decisions. Paper and original verification material
are CC BY 4.0; source authors retain rights in their omitted bodies.

## Repair-stage checkpoint, 16 October 2026

`CURRENT_REPAIR.json` records one complete whole review and the sole P3 repair.
A NEW complete whole review02 is required after root adoption; minimum two
complete reviews, publication-ready/published false, services held at #1032.
The 15 October zero-review preparation STATUS and copied historical pending
records are preserved. No paper, mathematics, mathematical checker, priority
qualification or native bibliographic metadata changed in this repair.

`provenance/repair01/` gives the new hash-only capture, exact authored whole01
and root-adoption copies, exact changed-interface before-bytes, one distribution
decision per captured file and individual resolution of prior pin records.
The original 83 copy decisions and 82 exclusions remain byte-exact. Before-byte
interfaces are historical, not active commands. Copied reviewer programs are
authored historical evidence, not supported kit controls or claims that omitted
programs were replayed. Source bodies/text/pixels, raw compiler streams and old
ZIPs remain omitted with hashes and individual reasons.
