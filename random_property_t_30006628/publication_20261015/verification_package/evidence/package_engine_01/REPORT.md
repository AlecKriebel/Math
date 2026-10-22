# PR #872 portable verification-engine engineering review

This directory contains three new standard-library templates and their public
reproducible guard harness. It does not contain or approve a final preprint,
production archive, mathematical result, priority conclusion or publication.
The parent and later fresh package adversaries must review the final assembly.
The original proof effort remains 1/5.

## Inputs and implementation

I read the complete supplied `SOURCE_MANIFEST.json`, the artifact audit's full
REPORT and DECISION, the complete historical wrapper and all four archived
Python code bodies. The source manifest identifies frozen PR-head
`e3d77731b45b5f463df46e769faa01d65fe193ec` and has SHA256
`4589f9b70e9a65ae67356544b5ad59644290902bb9b3df80406710a22559e3f8`.
The task treats that parent-supplied pin as an external trust anchor; this
engineering subtask did not independently retrieve remote Git objects.

`check_originals.py` authenticates the strict manifest and all 15 unchanged
source files by byte count, SHA256 and Git-blob SHA1, plus the exact historical
14-entry outer inventory. It checks the three archive/member inventories
(12+7+7=26), safe ordinary ZIP metadata, bounded members and three readable
copy bindings. All JSON bodies are parsed with duplicate-key and nonfinite
rejection, including numeric overflow. The historical first-review ZIP has
mode 0600 without Unix type bits; type zero is treated as implicit regular,
while explicit FIFO/device/symlink/directory types and executable modes reject.

The checker writes authenticated bytes to a temporary path containing spaces
and runs the archived finite programs directly with `-I -S -B`, in both normal
and optimized child modes. It never executes the historical wrapper. Positive
stdout matches frozen output bytes; negative output matches the exact intended
reason and status. Default replay has 14 receipts: 6 positive and 8 intended
negative. Optional provenance replay authenticates three corpora and six
historical PDFs, strictly parses corpus JSON, and adds 6 receipts (20 total:
8 positive and 12 negative). These finite diagnostics cannot certify the
asymptotic theorem, mathematical proof dependencies or priority.

`verify_package.py` takes an external index digest and enforces a strict closed
file-and-directory inventory with dynamic member count. It authenticates the
checker and every payload before running copied checker bytes. The separately
trusted startup verifier itself must be authenticated before invocation; no
self-hash claim establishes startup trust.

`build_verification.py` requires external index and startup-verifier digests,
checks all content and runs a copied authenticated verifier with full finite
replay before writing a ZIP. Output is fresh/empty and outside the assembly;
no existing file is overwritten. Entries are sorted regular 100644, deflated
at level 9 with fixed 2026-10-15 00:00:00 UTC timestamps. Reproducibility claims
are limited to identical input bytes, Python ZIP implementation and zlib.
No production or final publication archive was created in this subtask.

All optional source leaves are screened as regular and exact-sized before
any source payload is read. Actual reads repeat leaf and descriptor checks
with bounded reads, `O_NOFOLLOW` where available and nonblocking opens. Roots
and their ancestors may be aliases; aliases/nonregular entries inside a
portable tree and optional source leaves are rejected. The runtime,
filesystem and absence of hostile concurrent ancestor replacement are trust
assumptions. These Python switches are not a system sandbox.

## Probe accounting and evidence

The public `adversarial_probes.py` creates disposable engineering assemblies
and never changes originals. The final normal and optimized suites pass on the same recorded
three template hashes. Each includes the optional complete source replay.
A further optimized finite-only run also passes.

Per complete harness, classifications are:

| Classification | Count | Scope |
|---|---:|---|
| Ordinary expected rejection | 47 | 15 frozen-file corruptions; 8 closed-inventory mutations; 3 output-policy violations; incomplete source arguments and two basic catalog-leaf controls; all 18 corpus/PDF FIFO/alias controls |
| Artificially resealed parser rejection | 21 | 14 index schema/path/JSON controls; 7 ZIP metadata/member controls |
| Startup rejection before execution | 5 | Substituted checker marker; index FIFO; verifier FIFO; substituted-verifier and changed-index marker controls |
| Positive control | 7 | Frozen authentication; 14-receipt replay; documented root alias; two fixture builds; byte equality; 20-receipt provenance replay |

The resealed controls deliberately replace trusted test digests or the test
module's frozen source-manifest pin. They reach semantic guard branches and
are not successful attacks against fixed external hashes. Marker files remain
absent. Internal original diagnostics, including those repeated by each
fixture build, are recorded separately and are not additional independent
mathematical cases.

The normal engineering fixture has 20 indexed files plus its index (21 ZIP
members). Both normal fixture builds are 104803 bytes, SHA256
`e3fec54137907b921b4839f2f78acc65844292d44f45bf5459316d0322251024`.
This is an engineering fixture containing no paper; it is not the final
publication package and its dynamic count does not constrain future assembly.

Earlier concurrent full-source attempts and one optimized sequential attempt
returned a generic child-checker failure. A subsequent direct optimized
checker returned `[Errno 28] No space left on device`; the volume then had
337 MiB free. That establishes a real local capacity failure, without proving
the cause of every earlier generic failure. Temporary fixtures auto-remove;
no foreign files were deleted. After the parent freed only its own completed disposable fixtures, the
sequential optimized full-source suite passed on the same template bytes.
Final sequential outcomes are reported in the receipts and DECISION. A full provenance relocation needs about 163 MiB for
its three corpus files in addition to normal process and temporary overhead.

## Remaining boundary

Python 3.14.6 / zlib 1.2.12 were used. No cross-runtime or cross-zlib byte
reproducibility is certified here. The final paper, metadata, complete final
inventory, final trust record, independent package reviews and publication
are the parent's remaining work. See USAGE.md for assembly contract, commands,
trust boundaries and probe reproduction. No new original theorem or priority
claim is made by these scripts or these engineering results.
