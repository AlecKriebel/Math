# Integrity, provenance, and manuscript reproducibility audit

Date: 2026-08-23/24 (America/Los_Angeles / UTC rollover)

Scope: the isolated handoff at
`/Users/alec/Documents/Math/k2p_same_neutral_referee_audit_2026-08-23/isolated_handoff`.
All writing producers were run only in disposable copies.  No authoritative
file was repaired or rewritten during this audit.  Hash agreement in this
report is provenance evidence, not mathematical validation.

## Status and conclusion

**Provenance/integrity: PASS.**  The submitted verifier, independently
implemented ledgers, all path/byte/hash/count comparisons, source-commit
checks, deterministic archive rebuilds, PDF/source/report cross-bindings, and
targeted mutations agree.

**Manuscript reproducibility: PASS.**  Exactly the five bound TeX/Bib sources
produce a clean 26-page article and 24-page supplement with Tectonic 0.16.9.
Both sealed PDFs can be reproduced byte-for-byte when the creation epochs
stored in those PDFs are supplied.  The two generated supplement inputs fail
at their literal `\input` sites when omitted.  Bibliography omission is
rejected by both the outer file ledger and the retained, resealed source-ledger
mutation.

**Rendered-PDF integrity: PASS.**  Poppler parsed, extracted, and rendered all
50 submitted pages; every listed font is embedded.  Complete montages and
dense representative pages showed no apparent clipping, overlap, missing
glyph, or unreadable layout.

**Human metadata/release: HOLD (expected and non-scientific).**
`SUBMISSION_BINDING.json:72-82` deliberately leaves journal ID, immutable tag,
DOI, licenses, email confirmation, contributions, funding, and conflicts for
human action.  This does not downgrade the scientific provenance PASS.

There is no reproducibility-blocking or provenance-blocking defect in this
track.  Four nonblocking observations are recorded below.

## Claim matrix

| Layer | Status | Authoritative location | Independent evidence | Evidence type / remaining gap |
|---|---:|---|---|---|
| Outer handoff integrity | PASS | `PACKAGE_MANIFEST.json`; `verify_handoff.py` | All 492 rows independently recomputed and compared path-by-path; six semantic mutations rejected | Provenance/computational; no mathematical implication |
| Inner seal | PASS | `proof_compression_submission/crosswalk/REVISED_REFEREE_BUNDLE_MANIFEST.json` | 374 frozen + 73 submission rows independently recomputed; roots/payloads agree | Provenance/computational |
| Five supplemental dependencies | PASS | `SUBMISSION_BINDING.json:45-70` | Current bytes match commit `078b573d...`; two and only two have the declared byte-identical sealed copies | Provenance/computational |
| Archive determinism | PASS | `build_handoff_archive.py` | Two independently copied, verified trees produced byte-identical ZIPs, also identical to distribution | Computational reproducibility |
| Five-source clean build | PASS | `SUBMISSION_BINDING.json:21-26`; `PDF_BUILD_REPORT.json:1-41` | Fresh exact-five-file builds; logs match seal; fixed-epoch PDFs match seal | Computational reproducibility; epochs are not documented |
| Generated supplement inputs | PASS | `supplement.tex:307,441` | Each omission fails at its own literal input line | Computational |
| Bibliography retention | PASS | `main.tex:1860-1861`; `supplement.tex:951-952`; crosswalk mutation line 114 | Physical outer omission and retained `omitted_bibliography` mutation both reject for the intended ledger reason | Computational/provenance; compiler exit alone is insufficient |
| PDF rendering/fonts | PASS | Both sealed PDFs; `PDF_BUILD_REPORT.json:12-25,41` | 50 pages parsed/rendered; all fonts embedded; visual inspection | Computational/visual |
| PDF/source/build/lock/crosswalk/telemetry consistency | PASS | Bound artifacts listed below | 79 independent cross-checks, including every row in the relevant ledgers | Provenance/computational |
| Englander-v4 historical source identity | PASS | `TOPOLOGY_DIRECTIONAL_THEOREM.md:69-73`; `topology_direction_certificate.json:28-30` | Exact historical bytes retained; current official bytes differ only in mutable metadata/ID; text and all 31 renders identical | Literature provenance; no mathematical validation |

## 1. Outer and inner ledger audit

I inspected the submitted verifier and mutation code before running it.  I
then implemented `scripts/provenance/audit_ledgers.py` independently; it does
not import the submitted verifier or manifest builder.

### Outer handoff

- Manifest file SHA-256:
  `35b8207cf05f48465a4e48588cf82d488f4abd3b68d30dd942d873df1e01680b`.
- Independently enumerated rows: 492; declared rows: 492.
- Independently summed bytes: 439,308,215.
- Every relative path, byte count, and SHA-256 agrees.
- Independent content root:
  `f76605c76cc711a7261ccfd9de693076515b3eab7f5abd178761f804346bfbc2`.
- Payload SHA-256:
  `f56215708d3cb89b43108827fa588330e00c2aec7c3249c00dcf8c9a192c2c7d`.
- No unsafe paths, unlisted files, missing files, or symlinks were present at
  final verification.

### Inner seal

- Inner manifest file SHA-256:
  `c1621602b933b6113ed9f29e47211b423dbbe802cedd86346c76546e803e4c3f`.
- Frozen ledger: 374 rows; content root
  `7004e3e26bf359d0a11c07fd51cb1636859b30b07a97ca6c9cfd0dcd082dfc92`.
- Submission ledger: 73 rows; content root
  `30117737e2e0c53483a8c4003a9a6076da0fbc8111c4259ec6c7ebdca14b1f26`.
- Combined: 447 sealed rows; combined root
  `4bc3a77677415ac373176550db228bf6c22969b4c628861875f147aff147d94f`;
  inner payload
  `1e1b545bc62bb822c560a467026374e69546e603aabb49e0491d6e2a56b6ec7c`.
- The complete non-environment inner project has exactly 453 files: 447
  sealed rows, the inner manifest, and the five explicitly declared
  supplemental dependencies.  There are no other extras, overlaps, missing
  rows, or symlinks.

The detailed 413-KB row-by-row result is
`reports/provenance/independent_ledger_audit.json`, SHA-256
`ffba4b73cc4ebbf14decfb97c9a418c16d15706bf177108a2c30a18db8f3c41e`.

## 2. Mutation behavior

The submitted top-level suite returned PASS.  I also executed every mutation
separately and captured its exact failure, ensuring that rejection was not an
unrelated checksum side effect.

| Mutation | Exit | Exact rejection |
|---|---:|---|
| wrong file hash in a resealed manifest | 1 | `outer file ledger mismatch: declared=492 actual=492` |
| omitted manifest row | 1 | `outer file ledger mismatch: declared=491 actual=492` |
| unsafe `../escape` path | 1 | `unsafe manifest path: '../escape'` |
| wrong inner payload binding | 1 | `outer-to-inner manifest binding mismatch` |
| false ready status | 1 | `outer manifest status mismatch` |
| optimized Python | 1 | `optimized Python is forbidden` |

Evidence: `reports/provenance/outer_mutation_reasons.json`, SHA-256
`cee3fbced5f28a4b11d337a5a4c1dbe4bcacdb5f661a3ebca55256d9bd926972`.
The archive builder, manifest checker, and manuscript checker also each reject
optimized execution with the same exact message; the attempted optimized
archive created no output.

### Bibliography gate

The generic top-level mutation suite does not name a bibliography-specific
case.  A dedicated retained mutation nevertheless exists at
`proof_compression_submission/crosswalk/test_crosswalk_bundle_mutations.py:106-115`.
It removes precisely
`proof_compression_submission/article/references.bib`, recomputes the manifest
payload, and invokes the independent revised-bundle checker.  The retained
mutation report is 2,889 bytes, SHA-256
`9692005ca9c3e69db2f564356e8e588f1e22a997975797f676cbbf2b4e1fb37f`,
and is itself sealed.  Fresh execution returned 14/14 PASS and the exact
rejection was:

`submission sources ledger mismatch; missing=['proof_compression_submission/article/references.bib'] extra=[]`

I separately moved the bibliography recoverably out of a disposable complete
handoff.  Its outer verifier exited 1 with
`outer file ledger mismatch: declared=492 actual=491`; after restoration the
copy verified again.  Detailed evidence is
`reports/provenance/bibliography_omission_audit.json`, SHA-256
`cefe4001fea2a964dcfcd63b350c56be28d98329a8afa91f03abe4f06a6dfda3`.

## 3. Supplemental execution dependencies and source commit

`SUBMISSION_BINDING.json:5-7` binds Git commit
`078b573d214ff598868d1b5dbf9565ef267bb257`.  That object exists locally.
For each of the five dependencies, I compared the handoff bytes directly with
`git show 078b573d...:<path>`, independently of the submitted verifier.

| Dependency | Bytes | SHA-256 | Byte-identical sealed copy |
|---|---:|---|---|
| `output/referee/REFEREE_BUNDLE_CONTENTS.json` | 70,753 | `5799d8f3127a3d1e43f28610a3753a3da2a2a0de5c021ce45efc5665058d24bd` | none |
| `work/four_port_direct_residual_closure_certificate.json` | 124,547 | `fb6e5f1c23c8c3291ddc8c822171cae9c2df05b0d449249813b40e958e17bddc` | none |
| `work/theta0_quintic_orbit_certificate.json` | 24,057 | `f863afd5875a74be818141990863344fae09fd4269a803d3a1bfeb67a8a595e0` | portable proof copy |
| `work/theta3_cubic_obstruction_certificate.json` | 1,837 | `fb1512e260b5a88b5ac3a4b55d6c756e401baebd08866d6e39bb2153b63aa4d8` | portable proof copy |
| `work/theta_quartic_obstruction_certificates.json` | 20,740 | `5204593fb2b47914dbdf2d7846d1e9fbd5671fa9f29e89862d29b16a45bb08db` | none |

Thus exactly two, not five, have declared byte-identical copies in the older
seal.  The five include the content ledger consumed by the theorem-artifact
crosswalk producer at
`build_theorem_artifact_crosswalk.py:187`.  All five source files also match
the same Git commit byte-for-byte.

Nonblocking verifier-coverage note: `verify_handoff.py` checks the declared
dependency hashes and bindings but does not itself fetch the named Git object.
The independent direct `git show` comparison closes that provenance check.

## 4. Deterministic archive reproduction

Two separately copied handoff trees were created under disposable audit
locations, excluding environment/output scratch, and each passed the submitted
verifier before archive creation.  The archive builder produced:

- build A: 19.01 s real, peak RSS 312,262,656 bytes;
- build B: 19.05 s real, peak RSS 316,915,712 bytes;
- each archive: 178,524,867 bytes, 493 members, SHA-256
  `c681f1984dbd95c7a8095593da339488544e03825232b5f8488050e94cdc27fd`.

Build A, build B, and the distributed
`/Users/alec/Documents/Math/k2p_ai_referee_handoff_2026-08-23.zip` are
byte-identical.  The two large audit rebuilds are retained outside the compact
report area at `archives/outer_rebuild_A.zip` and
`archives/outer_rebuild_B.zip`.

Independent ZIP inspection checked every member's content against the clean
tree, member order, CRC, fixed timestamp, compression method, Unix mode,
absence of duplicate names, and absence of comments/extra fields.  It also
checked the older 178,019,313-byte, 448-member inner archive, SHA-256
`ab7c3cef83d1bd7bb8c330b25ace118ae7ee583a39f7f55c7363b37e3ab4fe3d`,
against every sealed row.  Report:
`reports/provenance/archive_audit.json`, SHA-256
`1df225f1ed375fcee2be0ea6e3ac420e2f95a890eb28f610b1b72db9bdd2a4da`.

## 5. Five-source manuscript builds and PDF checks

The five bound sources and hashes are:

| Source | SHA-256 |
|---|---|
| article `main.tex` | `1107e5395a0e2ad4da0333cda066ae587d9a9854e61aeba3d2aadcf62e23e45b` |
| `references.bib` | `14dbb4901d924b068c8cc2d050e73bae3cf996a72863a22ade90d6f8e6b4057c` |
| supplement `supplement.tex` | `fcb9df1f2ac3d31354e7a67ccb94700f1b67c8ef13db985bef34e327c58d58de` |
| `compression_tables.tex` | `c96e994e64f7767f9583bd68d6d0f07af936bb227858c33bb1553e5db23644b8` |
| `certificate_appendix.tex` | `ef878c24ff3f6b28d70b6c3dbf90c6d1e7d3c85a2bece621c96f47c409ca0ffa` |

A static dependency scan found no other local source dependency.  The only
generated `\input` sites are supplement lines 307 and 441; bibliography sites
are article lines 1860-1861 and supplement lines 951-952.

### Clean builds

| Document | Exit / runtime / peak RSS | Fresh output | Sealed output | Result |
|---|---|---|---|---|
| Article | 0 / 4.71 s / 253,263,872 B | 193,906 B; `1e134c82...` | 193,906 B; `86b7ace4...` | build log exactly sealed; 26 rendered pages identical |
| Supplement | 0 / 3.82 s / 249,577,472 B | 158,531 B; `5ce7a90f...` | 158,528 B; `177006b4...` | build log exactly sealed; 24 rendered pages identical |

The current-time PDFs differ because Tectonic records the creation instant
and associated trailer identifiers.  With the creation instants already
stored in the sealed PDFs supplied as `SOURCE_DATE_EPOCH`, exact bytes are
reproduced:

- article: epoch `1787465144`, SHA-256 `86b7ace41d025caddcecae2accb04c496a401501b2a6e65233ad60cfc80e3e2a`;
- supplement: epoch `1787465911`, SHA-256 `177006b4d2a21d958f1811c3920bbbfca18fdff87cda8da99b97c9c950dd15cb`.

Those two epoch values are derivable from the PDFs but are not printed in
`PDF_BUILD_REPORT.json`.  This is nonblocking because the report claims a
clean five-source build, not an epoch-free bitwise build.  Recording them in
future build metadata would make exact-byte reproduction more direct.

### Omission behavior

- No `compression_tables.tex`: exit 1 at `supplement.tex:307`, log SHA-256
  `4acd49f9b1227fc90ec1e3d10947772825be1e4387745a6bc775e1ebd2187354`.
- No `certificate_appendix.tex`: exit 1 at `supplement.tex:441`, log SHA-256
  `b5e3e12a3dba74d30df9b5d0a8c1585237575b5c005da7816ee16bca818d5f9f`.
- No bibliography: Tectonic exits 0 for both documents while explicitly
  logging that BibTeX cannot open the database, citations are undefined, and
  the bibliography is empty.  Therefore compiler exit is not the gate.  The
  outer and source-manifest mutations above reject the omission.

### Submitted PDFs

- Article: 193,906 bytes, 26 pages, SHA-256
  `86b7ace41d025caddcecae2accb04c496a401501b2a6e65233ad60cfc80e3e2a`.
- Supplement: 158,528 bytes, 24 pages, SHA-256
  `177006b4d2a21d958f1811c3920bbbfca18fdff87cda8da99b97c9c950dd15cb`.
- Submitted build logs: article `beff8b7e...`; supplement `d1bef905...`.
- `pdfinfo`, `pdffonts`, `pdftotext`, and 96-dpi `pdftoppm` all succeeded;
  every font was embedded.

## 6. Mutual artifact consistency

The independent consistency audit performed 79 checks and all passed:

- release lock: 70,167 bytes, 198 file rows, SHA-256
  `58e32bd29f7a039e3da4e47398e32ee8277ad46cf62271a7ed80bf41688b18fb`,
  payload `3b7de4c60315a5820a2623de860f493d6b76a645b5c674ffda89f12fc31a5c90`;
- frozen content ledger: 70,753 bytes, 374 rows, SHA-256 `5799d8f3...`,
  content root `7004e3e2...`;
- theorem-artifact crosswalk: 13 claims, 130 artifact rows, SHA-256
  `918d9704469b016c7efc7c847dddb6ccc7da21c820d2259307729cf8c714d026`,
  payload `ef596a50330766c126e7776c9fd8088260a42a129ca47ba16e50389e971f299b`;
- stored replay: 35 layers, report SHA-256
  `7939b389880de80b7d8abd69022e0b69d2dc4188815854b294d3384fa24c9e18`,
  telemetry SHA-256
  `8779854633d9a52ba3d7bc9278ccbcc3918e51987bb4c30204c0adcd9771ce16`,
  historical commit expanded to `1e9ff6c6052d7528b17806910a086d3584d446ac`;
- PDF report JSON: SHA-256
  `b8900d8e4bbcaed1330a9ebeaa823edeb50c60ecee8d8c6b8d75b3181d70c982`;
- every reported PDF, source, build-log, lock, ledger, crosswalk, and replay
  byte/hash/status cross-binding agreed.

Evidence: `reports/provenance/artifact_consistency_audit.json`, SHA-256
`c5d67f0ea7c5504a9cf90d9b19a342b28cfeae2f824cf42bc65e77350b799a85`.
These checks authenticate relationships among artifacts; they do not prove
the mathematics represented by those artifacts.

## 7. Englander-v4 PDF provenance reconciliation

The package accurately says that its cited SHA-256 belongs to a “locally
reviewed PDF,” at `TOPOLOGY_DIRECTIONAL_THEOREM.md:69-73` and
`topology_direction_certificate.json:28-30`.  It does not claim that bioRxiv
will return immutable bytes forever.

The exact historically bound file is retained at
`/Users/alec/Downloads/2025.04.18.649493v4.full.pdf`:

- 927,795 bytes, 31 pages;
- SHA-256
  `3c140c36aae45cd07040b0f1e03b55b40f7c61f14a04b9fbe9cd8c48112e8ba5`;
- local creation 2026-08-17 11:07:49 -0700 and modification one second later;
- macOS acquisition metadata records a `chatgpt.com` content attachment,
  consistent with the retained narrative's “supplied PDF” wording.  Sensitive
  query/signature material was not copied into the audit report.

The current official bioRxiv download retained in audit scratch is also
927,795 bytes and 31 pages, but has SHA-256
`69f04a54d7deb5e12485ba566b50bdcffddf5cd1d80c6c7cfb0c656bc504e40d`.
The two files differ in only 55 bytes across 21 short runs.  After
canonicalizing only the XMP modification/metadata dates, XMP document and
instance IDs, top-level `/ModDate`, and the second trailer ID, the files are
byte-identical.  Ordinary and layout-preserving text extraction hashes agree,
and all 31 corresponding 96-dpi PNG renders are byte-identical.

The exact `3c14...` bytes are not in the current Git object database and are
not redistributed in any of the 84 readable ZIP or 60 readable
non-environment TAR archives scanned under the Math repository.  Three
unrelated files bearing a `.tar` suffix had invalid headers and could not be
treated as archives.  Git contains two other 927,795-byte
metadata renditions (`260a977d...` and `ead61aab...`).  The handoff's omission
of a third-party PDF is deliberate; the exact historical copy remains locally
retained and the current official content is identical.

**Classification:** nonblocking literature-provenance/external-rendition
observation, not a citation defect, attribution defect, or mathematical
defect.  No theorem or code change is needed and no reseal is required.  As a
future convenience, the source note could record access date plus a
content-normalized digest, since the publisher rewrites metadata on access.

Evidence: `reports/provenance/englander_pdf_provenance.json`, SHA-256
`77424fc67e4c2c4c8be26a081dfd7aa5e7328853f9d01cd76cc09bc1965b6fe8`.

## 8. Execution ledger

Environment:

- macOS 26.5.2 (25F84), Darwin 25.5.0 arm64;
- Apple M1 Pro; 17,179,869,184 bytes physical memory;
- Python 3.14.6; NetworkX 3.5; SymPy 1.14.0;
- Tectonic 0.16.9; Poppler 26.08.0; Git 2.38.2.

| Command/gate | Exit | Real time | Peak RSS | Principal output/hash |
|---|---:|---:|---:|---|
| submitted `verify_handoff.py` (initial) | 0 | 0.90 s | 283,279,360 B | PASS, 492/374/73 |
| submitted `test_handoff_mutations.py` | 0 | 2.63 s | 280,723,456 B | all six routes PASS |
| independent ledger audit | 0 | 1.21 s | 32,833,536 B | `ffba4b73...` |
| independent outer mutation capture | 0 | 2.25 s | 283,885,568 B | `cee3fbce...` |
| submitted five-source build checker | 0 | 12.26 s | 254,115,840 B | article `8a9275f1...`; supplement `d86cca90...` (temporary timestamps) |
| verify disposable archive copy A | 0 | 0.99 s | 262,111,232 B | PASS |
| verify disposable archive copy B | 0 | 1.03 s | 266,141,696 B | PASS |
| archive build A | 0 | 19.01 s | 312,262,656 B | `c681f198...` |
| archive build B | 0 | 19.05 s | 316,915,712 B | `c681f198...` |
| independent archive inspection | 0 | 6.50 s | unavailable | `1df225f1...` |
| retained clean article build | 0 | 4.71 s | 253,263,872 B | PDF `1e134c82...`; log `beff8b7e...` |
| retained clean supplement build | 0 | 3.82 s | 249,577,472 B | PDF `5ce7a90f...`; log `d1bef905...` |
| missing compression-table build | 1 | 2.46 s | 217,153,536 B | intended line-307 failure; log `4acd49f9...` |
| missing appendix build | 1 | 2.45 s | 217,219,072 B | intended line-441 failure; log `b5e3e12a...` |
| article without bibliography | 0 | 3.89 s | 254,148,608 B | warnings; log `56a42cde...` |
| supplement without bibliography | 0 | 3.37 s | 251,101,184 B | warnings; log `a2e4fed4...` |
| physical bibliography outer omission | 1 | 0.41 s | 197,853,184 B | intended 492/491 mismatch |
| retained crosswalk mutations | 0 | 3.74 s | 550,862,848 B | 14/14; retained report `9692005c...` |
| fixed-epoch article | 0 | 3.96 s | unavailable | exact sealed PDF `86b7ace4...` |
| fixed-epoch supplement | 0 | 3.37 s | unavailable | exact sealed PDF `177006b4...` |
| artifact consistency | 0 | 0.40 s | unavailable | 79 PASS; `c5d67f0e...` |
| final submitted verifier | 0 | 0.82 s | 284,114,944 B | PASS, 492 |
| final manifest producer `--check` | 0 | 0.54 s | 215,695,360 B | PASS, payload `f5621570...` |
| optimized archive/manifest/manuscript gates | 1/1/1 | not separately timed | unavailable | exact rejection each; no archive |
| historical/current Englander renders | 0/0 | 6.77/6.73 s | 30,720,000/30,490,624 B | 31/31 byte-identical |
| independent Englander comparison | 0 | 0.79 s | 29,966,336 B | `77424fc6...` |

Exact command strings, working directories, user/system times, all available
RSS readings, retained log/PDF hashes, and the reviewer-interference event are
in `reports/provenance/execution_ledger.json`, SHA-256
`8001f09b7f3952ce96d55707fd8889cee77c868c9d4b8acbd75461dcc7c9dd80`.

## 9. Numbered findings

1. **Nonblocking reproducibility metadata.**  Exact sealed PDF bytes require
   `SOURCE_DATE_EPOCH=1787465144` and `1787465911`; the values are stored
   implicitly in the PDFs but absent from the build report.  Effect: none on
   clean compilation or rendering.  Smallest optional remedy: record the two
   epochs in future build metadata.  Current downstream artifacts need no
   reseal unless authoritative metadata is edited.
2. **Nonblocking verifier-coverage observation.**  The outer verifier checks
   declared dependency bytes but does not itself authenticate the named Git
   commit.  The independent `git show` checks passed.  Smallest optional
   remedy: add a Git-object check when Git history is available, clearly
   outside archive-only operation.  No current reseal is needed.
3. **Nonblocking external-rendition observation.**  The historical Englander
   PDF hash is real and retained.  Current publisher bytes differ only in
   access-time metadata/IDs.  Text and renders are identical.  No remedy or
   reseal is required.
4. **Nonblocking audit-process event, not a submission defect.**  A reviewer
   briefly rendered `article-page-6.png` under `isolated_handoff/tmp/pdfs`, and
   the outer checker correctly failed on a 493rd file.  The file was moved
   recoverably to audit-root `tmp/pdfs`; final submitted, producer, and
   independent checks all pass at 492 files.  This demonstrates fail-closed
   behavior under reviewer interference.

No theorem-fatal, proof-blocking, computational-completeness-blocking, or
reproducibility-blocking finding arose in this track.

## 10. Required actions

No mathematical or code action is required by this audit track.

Human release choices remain exactly those declared in
`SUBMISSION_BINDING.json:72-82` (journal ID, immutable tag, DOI, licenses,
email/contribution approval, funding, and conflicts).  Those decisions are
outside this scientific PASS and were not inferred, prepared, or initiated.
