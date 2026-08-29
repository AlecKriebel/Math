# Source-archive reproduction audit

**Audit date:** 2026-08-29
**Delivered package:**
`/Users/alec/Documents/Math/k3p_level2_third_revision_referee_final_2026-08-29`
**Exact source checkout:**
`738b662aa9c4e6201277f60b249afd4de9bcd9d6`
**Audit evidence root:**
`/Users/alec/Documents/Math/k3p_level2_third_revision_fresh_referee_2026-08-29`

## Result

**PARTIAL PASS.** Both delivered source ZIPs pass independent structural,
manifest, commit-content, and canonical-byte reconstruction checks. The reader
supplement also passes a fresh, offline, isolated two-build PDF reproduction at
the declared commit. The article does **not** receive a fresh PDF-reproduction
PASS in this audit: its sole permitted command invocation stopped before any
completed build because the initial macOS sandbox omitted a SystemConfiguration
Mach lookup required by Tectonic's HTTP-library initialization. In accordance
with the at-most-once instruction, the article command was not relaunched.

This is an audit-infrastructure failure, not an observed archive, TeX, or PDF
mismatch. The article claim is strongly corroborated by a prior two-build report
for byte-identical article source members, the same pinned Tectonic executable,
and the same delivered PDF hash, but that prior report is ignored live-work
evidence from commit `825fd0bc...`, not a report sealed in this package and not a
fresh run at `738b662a...`. The appropriate final classification is therefore:

| Claim | Audit result |
|---|---|
| Article source ZIP is canonical and contains exactly the declared commit's source | **PASS** |
| Supplement source ZIP is canonical and contains exactly the declared commit's source | **PASS** |
| Supplement rebuilds twice to the delivered PDF | **PASS** |
| Article rebuilds at the final declared commit in this fresh audit | **INCONCLUSIVE — sandbox setup failure; no relaunch** |
| Package contains a final-commit, independently inspectable two-PDF reproduction certificate | **NO** |

No package file was edited. No credential, network access, external service, or
external communication was used.

## Delivered artifacts and independent archive checks

The source members were compared byte-for-byte with Git blobs from the exact
clean checkout. I also implemented the documented canonical JSON and ZIP rules
independently, without importing package code, and rebuilt each ZIP in memory
from those Git blobs under Python 3.14.6 with zlib 1.2.12. Both reconstructed
ZIP byte strings equal the delivered ZIP byte strings.

| Property | Article | Reader supplement |
|---|---:|---:|
| ZIP bytes | 65,299 | 20,150 |
| ZIP SHA-256 | `683285f7ef3271349a996df93ee96e7e29cb44d17543e7871071e00fc4e6a366` | `4d235bcafd73017c5a02e9ba8b1c3b9eaba920ff09d02db3bc27da24146b7406` |
| ZIP entries, including manifest/build record | 25 | 3 |
| TeX/Bib source members | 23 | 1 |
| Git-member mismatches | 0 | 0 |
| Source-member logical payload SHA-256 | `78c6ae8ddb0a7d1abbd2b3d81a4637b120a5135e77abb53f657cbb87af2fb9ea` | `64480ff653200c335dd71cb12a406648d478f8f1cbb689e53320e9a08833e4de` |
| Manifest payload SHA-256 | `824cd6a71f0b2d3f1a48f2ed7c1547bf4e5ddc8d97870f9a1b38f197d5a5d5dd` | `1ead4afe3e7522beada82a5a626eeef2dae2c9c3c63d64bfa8142f74da87fdb3` |
| `SOURCE_BUILD.json` SHA-256 | `4ad2185a9e78202b34cc03abd6aa447ee5ff9aaff8ad0ba540c7ac3b30d786d7` | `d0e3772da344599ade168df2b023061ba937e4e60f589f89ee9eddffd8bb800a` |
| Manifest source commit | `738b662aa9c4e6201277f60b249afd4de9bcd9d6` | same |
| Manifest archive epoch | `1788019048` | same |
| ZIP timestamp | 2026-08-29 15:57:28 UTC | same |
| Modes | all `0644` | all `0644` |
| CRC/order/path/root checks | PASS | PASS |
| Independent canonical reconstruction | byte-identical | byte-identical |

The delivered PDFs also equal the committed PDFs at `HEAD`:

| PDF | Pages | Bytes | SHA-256 |
|---|---:|---:|---|
| Article | 38 | 258,457 | `5fd4fb902ee72c619c75846e2e5f561b018b4096a659b895063c0758dfc5d9df` |
| Reader supplement | 14 | 130,692 | `e82d1afb01f937872ec06ee1b1529fe736362c3496721b99813d8849ff7327e6` |

The package implementation supports these archive conclusions. It constructs
source members from committed `HEAD` blobs and deterministically creates the
build record and ZIP (`release/build_release.py:498-538`); canonicalizes JSON,
mode, ordering, timestamp, and compression (`release/archive_tools.py:37-80`,
`:117-153`); validates CRC, paths, roots, duplicates, ordering, modes,
timestamps, and the manifest (`release/archive_tools.py:156-210`, `:265-311`);
and extracts only validated members with resolved containment checks
(`release/archive_tools.py:314-328`).

## Static audit of the PDF-reproduction command

The local reproduction command is bounded and credential-free, but it is
Git-checkout-bound rather than standalone-package-only:

- `release/README.md:21-30` gives one article and one supplement command.
- The verifier requires each archive's commit and outer epoch to equal the
  checkout's `HEAD`, and every source member to equal the corresponding Git
  blob (`release/verify_source_reproduction.py:88-170`).
- It requires the expected PDF to be committed at `HEAD` and byte-equal to that
  blob (`release/verify_source_reproduction.py:233-260`). Thus a copied referee
  package without the exact Git repository is not by itself a runnable source
  reproduction environment.
- The build record fixes the command, PDF epoch, locale, timezone, Tectonic
  version, and executable hash (`release/verify_source_reproduction.py:59-85`;
  `release/RELEASE_FILESET.json:5-7`).
- Each run extracts into a distinct temporary directory, uses private
  `TEXMFVAR`/`TEXMFCONFIG`, has an 1,800-second child timeout, and requires an
  output PDF (`release/verify_source_reproduction.py:200-230`).
- It performs exactly two builds and requires equality between them and the
  committed delivered PDF (`release/verify_source_reproduction.py:265-275`).
- It records both transcripts and a report (`release/verify_source_reproduction.py:276-318`).

The core equality checks are strong and fail closed. Three reproducibility
limitations remain:

1. **The TeX resource bundle/cache is not package-bound.** The policy binds the
   Tectonic executable but not the bundle payload or cache inventory. The
   recorded command is `tectonic <main> --outdir .`, without an explicit
   vendored bundle or an offline/only-cached option
   (`release/verify_source_reproduction.py:74-80`, `:207-224`;
   `release/build_release.py:510-527`). Consequently, an ordinary invocation
   can consult or fetch resources not identified by `SOURCE_BUILD.json`. The
   audit supplied a private copied cache and externally denied all network.
2. **The build inherits the caller's entire environment.** It starts with
   `dict(os.environ)` and overwrites only selected variables
   (`release/verify_source_reproduction.py:211-220`). The audit launcher used a
   deliberately small clean environment, but the package verifier does not
   enforce that property itself.
3. **Current reproduction evidence is not delivered.** The package contains
   the verifier, archives, PDFs, and prose assertion, but no current article or
   supplement JSON reproduction report and no build transcript. The current
   prose says both PDFs reproduce byte-for-byte
   (`release/FINAL_RELEASE_ENGINEERING_REPORT.md:45-54`), while warning that
   older hashes are historical (`:66-70`). The machine-readable current proof
   of that statement therefore has to be regenerated rather than inspected.
   In addition, the report's `logical_payload_sha256` intentionally omits
   `tool_versions` and collapses each build row to run/hash/bytes
   (`release/verify_source_reproduction.py:311-317`); only the full report, if
   separately sealed, binds tool path, transcripts, and timings.

For a publication-grade closed reproduction contract, the package should bind
and vendor the exact Tectonic resource bundle (or its complete immutable
digest), force offline/only-cached operation, construct a minimal child
environment, and seal the final-commit JSON reports plus transcripts in the
handoff.

## Isolated execution boundary

The exact checkout was a self-contained detached copy at commit
`738b662aa9c4e6201277f60b249afd4de9bcd9d6`, with no alternates, no promisor
pack, one local pack containing 3,578 objects (78,704 KiB), and empty porcelain
status before and after. Inputs were copied to an ignored work namespace inside
that checkout so the package verifier's project-relative and Git checks could
operate. Reports were written only to that namespace; outer transcripts and the
attempt seals were outside the child-writable boundary.

The clean launch environment fixed `HOME`, `TMPDIR`, `PATH`, locale, timezone,
`SOURCE_DATE_EPOCH`, Python flags, and Git configuration. A default-deny macOS
sandbox allowed reads only from the system toolchain, exact checkout, pinned
virtual environment, and audit runtime; writes only to the dedicated work,
temporary, and private-home paths; and denied `network*`. Prelaunch probes
confirmed that the exact checkout and pinned Tectonic could be read, while the
live manuscript, referee results, unauthorized audit writes, and local socket
binding were denied.

The exact Tectonic executable was:

- path: `/opt/homebrew/Cellar/tectonic/0.16.9/bin/tectonic`
- version: `Tectonic 0.16.9`
- executable SHA-256:
  `38eff9059ed622672c9a2590415a8f01c043df4232baa459628a2cd86e512d95`
- cached bundle payload SHA-256:
  `6ffe055852f8faf66c0acbe1a7fb27f87b869a90bad1204f3bf4d9683f597c7c`
- private cache: 730 entries, 725 files, 57,507,581 bytes; inventory SHA-256
  `e9612d0f190a5078122514e8df625e04d0904cdbe5041a368e068800303e4de7`

The private cache inventory was identical before and after. No Tectonic or
source-reproduction process remained after the run.

### Article: one invocation, no relaunch

The attempt seal records a start at `2026-08-29T20:11:05.905142Z`. The article
package command was invoked exactly once. It returned nonzero immediately,
before producing a report or completing either of its two intended builds,
because Tectonic's `reqwest` initialization tried to open the macOS
SystemConfiguration dynamic store and received a null object under the initial
sandbox. The outer failure transcript is 612 bytes with SHA-256
`ed49897ab2680a01df78830c105eaaeb6d5f8fd471c9f524b65ee2974adb3536`.

The initial sandbox-profile SHA-256 was
`5b4e63e032d6a17b874e1ef89b335e4b2d5b783104cec2b5a41c6e95733fddd2`.
After preserving the failure, the profile received only the narrow
`com.apple.SystemConfiguration.configd` Mach-lookup permission; network denial
and all file boundaries remained unchanged. A small cached TeX probe then
confirmed that this was the missing infrastructure permission. The article was
nevertheless **not** run again. There is no article JSON report and no article
PASS sentinel.

### Supplement: one invocation, two successful internal builds

The supplement attempt began at `2026-08-29T20:13:19.133305Z` and ended at
`2026-08-29T20:13:21.073345Z`. Its one outer invocation took
1.93922975 seconds; the two internal builds took 0.780711333 and 0.766220333
seconds. Each produced exactly 130,692 bytes with SHA-256
`e82d1afb01f937872ec06ee1b1529fe736362c3496721b99813d8849ff7327e6`,
equal to one another and to the delivered committed PDF. Both 256-byte Tectonic
transcripts have SHA-256
`6e050affeded2c349176fe12083a6eff0c5374ffb586639541828588bf0bf58c`.

The package report is 2,576 bytes with SHA-256
`50229dbf65f93ce60041510f71fb63a800e6f4a7949df830fc18a6a0852f1761`;
its logical payload SHA-256 is
`001aa81d2644bc4d0938b88f012be7087c713ba0fd1973668ffe4c23426b1050`.
The 333-byte outer transcript has SHA-256
`f31439ee5da8474a1b16f24606a0ff51ceff9645a148f0d220a29e553e58d018`.
The corrected supplement sandbox-profile SHA-256 was
`f75c973694a72b63171dc26021a237ba9e2468828b15b046622189c50b052f09`.

Across the audit there were exactly two package-command invocations: one
article and one supplement. There were exactly two completed PDF builds, both
internal to the supplement command. The article relaunch count is zero.

## Article corroboration and its limit

The prior ignored report at
`release/work/final_second_referee_source_reproduction/article_report.json` in
the live development tree has SHA-256
`d307fa450b69f61e29e503293de98cd4b91e5e9692ca47fa0a64d0bdbfccc345`.
It records two successful builds at commit `825fd0bc...`, taking 4.098438 and
4.2382325 seconds, both producing the current 258,457-byte article PDF with
SHA-256 `5fd4fb90...`. It records the same Tectonic executable hash and the same
23-member article source payload `78c6ae8d...`. I independently compared the
old and current article archives after excluding their manifest and build
record: all 23 source names and byte strings are identical. Their outer archive
hashes differ because the final archive binds the later commit and epoch.

This makes a source/PDF defect unlikely, but the evidence cannot be promoted to
a fresh final-commit PASS: the prior report is not sealed in the delivered
package, its commit differs, and the audit was expressly prohibited from
rerunning the article command after the sandbox failure.

## Evidence inventory

- `execution/source_archive_reproduction_738b/ATTEMPT_STARTED.json` — SHA-256
  `f8443ba027ff7f43c57ec9116a3f06100ce7be486f9352bddaa2f570743fb59d`
- `execution/source_archive_reproduction_738b/SUPPLEMENT_ATTEMPT_STARTED.json`
  — SHA-256
  `e322aa9414ee199f1ee264148f243320fb78de1129b0dd43aa2a764d9aae9e1e`
- `execution/source_archive_reproduction_738b/SUMMARY.json` — 4,045 bytes,
  SHA-256
  `41be73c4e9b44845c9405d8a7aa00deda310b292178e1931710b76cb2f827c57`
- `logs/source_archive_article_738b.log` — SHA-256
  `ed49897ab2680a01df78830c105eaaeb6d5f8fd471c9f524b65ee2974adb3536`
- `logs/source_archive_supplement_738b.log` — SHA-256
  `f31439ee5da8474a1b16f24606a0ff51ceff9645a148f0d220a29e553e58d018`
- generated supplement package report under the exact checkout — SHA-256
  `50229dbf65f93ce60041510f71fb63a800e6f4a7949df830fc18a6a0852f1761`

## Required disposition

Do not describe this fresh audit as a dual-PDF reproduction PASS. It establishes
canonical, commit-exact source archives and a fresh supplement reproduction;
the fresh article replay remains procedurally inconclusive. To close that one
gap, a later, explicitly authorized audit should invoke the article command
once under the corrected offline sandbox, then seal its report and transcripts.
Independently of that rerun, the release format should close the TeX-resource
and inherited-environment gaps described above.
