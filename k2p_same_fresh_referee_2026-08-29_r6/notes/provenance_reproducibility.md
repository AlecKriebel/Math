# R6 independent provenance, document, and reproducibility audit

Date: 2026-08-29 (America/Los_Angeles)

Read-only package root:
`isolated/k2p_principal_d_plus_submission_referee`

Source archive:
`/Users/alec/Documents/Math/k2p_level2_identifiability_closure/proof_compression_submission/output/K2P_Principal_D_Plus_Referee_Package_20260829.zip`

## Status

**HOLD; semantic document consistency FAIL.** Byte integrity, archive
determinism, local Git provenance, exact PDF rebuilding, PDF layout, and the
specific R5 typed-terminal-registry repair all PASS. A fresh independent check,
however, found one current authoritative proof-to-artifact contradiction:
`proof_compression_submission/probe/PROBE_WORD_THEOREM.md` labels two stale
hashes as the **current** coverage artifact even though C09, the submission
manifest, and the compressed-result certificate bind a different current
coverage file and payload. No counterexample or mathematical invalidity is
established by this document finding, but the current release should be held
until the contradiction is repaired and the affected byte graph is resealed.

The fresh bundle, crosswalk, and configured static-article checks passed. The
word verifier regenerates the coverage JSON but does not read the theorem
narrative. None compares the theorem's printed "Current coverage artifact"
fields to that JSON, so this mismatch is outside their semantic gates. Hash
agreement is treated here only as provenance evidence, never as mathematical
validation or semantic reconciliation.

No authoritative package file was edited. PDF builds ran in the disposable
execution copy, the bibliography attack ran in a temporary clone, and all
review-authored evidence is outside the package.

## Finding R6-M1: stale current coverage binding in C09 proof authority

Classification: **reproducibility-blocking current-proof narrative
contradiction**. This is not theorem-fatal on the present evidence.

The C09 authoritative artifact
`proof_compression_submission/probe/PROBE_WORD_THEOREM.md` has SHA-256
`f45cd543b6cafbada2c9cd361b06f708f2bdebe112c596a774cd0ee7736a17e8`.
Its "Current coverage artifact" section at lines 306--311 prints:

- file SHA-256
  `3791e4bb829976aa78289281b9998bfe0605ba4a20518f1e8dd660d7d1a91bb8`;
- logical payload
  `1d4248028b38f6b731f066960d9e584240de68a17323539fe5b47f119a8086f6`.

The actual current
`proof_compression_submission/probe/PROBE_WORD_COVERAGE.json` is 6,854 bytes,
has schema `k2p-probe-word-theorem-coverage-v1`, status PASS, file SHA-256
`c2e32b37d32eda11470afc7f747cb2bca5fa58c78fd92793f8fa94309f3d3660`,
and declared/canonically replayed payload
`d66b28240092a04112fde67d54527e3df3964d7eea64f7b75ed75f877435ec49`.
Both printed values are therefore wrong.
An independent scan of all decodable Markdown, JSON, Python, TeX, BibTeX, and
text files in `proof_compression_submission` found each stale value exactly
once, at the two lines above; neither is a competing current certificate
binding elsewhere in the submission.

This is a contradiction among current objects, not a historical-label issue:

1. theorem-artifact crosswalk row
   `C09-coherent-probe-word-reconstruction` calls the Markdown object the
   "uniform word theorem", records proof status
   `uniform_word_theorem_from_frozen_finite_premises`, and binds it together
   with the actual current coverage JSON;
2. template row `CBT-5` likewise uses both as evidence for the proved word
   theorem; and
3. `REVISED_REFEREE_BUNDLE_MANIFEST.json` and
   `PROOF_COMPRESSION_RESULT.json` bind the actual current JSON hash/payload,
   while also binding the stale theorem prose as authentic bytes.

The independent reproducer
`independent_checks/provenance/probe_narrative_binding_audit.py` (SHA-256
`364985fb5fb03b2d97a6d77696f8c9db9a09ab34662fcf21a8d548ff7248dc5f`)
imports no submitted module. It emitted
`evidence/provenance/PROBE_NARRATIVE_BINDING_AUDIT.json` (SHA-256
`bf4aea4e4905c2629441486855942c506a45880112a12d53a90572b91d7ec7f6`,
logical payload
`b80a7c40cc84be9de814f020a5a38076c933e684e326ebc80e852423790c0543`),
status FAIL with exactly two mismatches. Its exit 1 is the expected observed
finding, not a harness crash.

Smallest adequate repair:

1. replace the two stale hashes with the actual current coverage file and
   payload hashes;
2. add a semantic gate and targeted mutations that parse this named current
   section and compare both fields to the certificate bytes and canonical
   payload; and
3. regenerate and reseal every derived object whose byte graph includes the
   corrected theorem: at least the compressed result, theorem-artifact
   crosswalk, revised submission manifest, referee archive and digest, commit,
   and annotated tag. Rerun the template-crosswalk and bundle-content checks;
   those files need not change unless their own regenerated content does.

The five TeX/Bib inputs and the two PDFs do not depend on this Markdown file,
so their bytes need not change solely for this repair. The stored clean-full
telemetry binds those five sources and `RELEASE_LOCK.json`; it remains valid as
stored-run provenance if those inputs remain unchanged. The release/package
checks must nonetheless be rerun after resealing, and any changed telemetry or
release-lock input must receive a new clean full replay rather than an inferred
PASS.

## Environment

- macOS 26.5.2, build 25F84; Darwin 25.5.0; arm64.
- Apple M1 Pro; 10 physical/logical cores; 17,179,869,184 bytes RAM.
- Python 3.14.6; NetworkX 3.5; SymPy 1.14.0.
- Tectonic 0.16.9; Poppler 26.08.0; Git 2.38.2.

## Independent archive and ledger reconstruction

The review-owned
`independent_checks/provenance/independent_provenance_audit.py` (SHA-256
`23ea1773e9b896a26f5de9d7fdd732f752d316136ad09727ed851da2f70da02d`)
imports no submitted code. It independently implements duplicate-aware JSON
decoding, payload hashing, recursive nested-ledger expansion, submission-source
selection, ZIP inspection, telemetry and PDF-report binding, crosswalk path/hash
resolution, and Git-blob comparison.

Result:
`evidence/provenance/INDEPENDENT_PROVENANCE_AUDIT.json` (SHA-256
`8b2224f9316f56b19709b8406ef3d3484f9d12227885106ffe5d733856347d97`,
logical payload
`7bb498c2bde79a48338cabe009327bbd120ff0af79eb5b25975f572f480520c8`),
status PASS.

### Outer referee archive

- SHA-256:
  `fef886379d9682586920a9f1112465dccab75267dbdd87a5b87b38dc4dbea513`.
- Size: 214,977,546 bytes.
- Exactly 495 unique regular members; 483,751,133 uncompressed member bytes
  and 214,834,734 compressed member bytes.
- No duplicate names, directories, symlinks, encryption, comments, or extra
  fields.
- Exact declared prefix and lexicographic project-relative order.
- Every member uses deflate, fixed DOS time 2026-08-27 00:00:00, Unix creator,
  and archive mode 100644.
- Every member is byte-identical to the isolated extraction.

The two-day difference between the archive filename and fixed member timestamp
is explicitly declared in the archive policy. The annotated Git tree retains
four executable modes while the portable ZIP deliberately normalizes all modes
to 100644; the underlying bytes agree.

### Recursive frozen theorem-evidence ledger

- `RELEASE_LOCK.json`: 80,180 bytes; SHA-256
  `bbb411dde4a13f001d9c2b5fac97722a54bb6ce604b6aff476de44f7ce4b8f53`;
  logical payload
  `3a0c89c4cedb7202161289eab7b3671c004ae638bcf90eba837e45e3e1890fc5`.
- `promotion_ready=true`; zero blockers and missing required files.
- 231 direct outer rows.
- Nested rows encountered: 94 rank-manifest, 17 cycle-manifest, 60 direct
  closure-lock, and 16 direct input-lock rows.
- After overlap removal and adding the release lock: exactly 408 files,
  479,383,009 bytes.
- Canonical recursive content root:
  `ed3beb4fca8338a3b97c7e5a0ff2bb58460ee7a244ea030bb7d3f837b5563d73`.
- `REFEREE_BUNDLE_CONTENTS.json`: SHA-256
  `b3af4bab82d9715841aed7f4c666309720f52fc78f6f560fd6325e26267b2753`;
  every row, count, byte total, lock binding, and root agrees.

The current package declares three supplemental execution dependencies, all
present in the 86-file submission ledger:

| path | bytes | SHA-256 |
|---|---:|---|
| `output/referee/README.md` | 2,898 | `76b8f7480e164d8667b4e4507e8662a897b9db22fc01cc3bda0410326f8bfc54` |
| `output/referee/REFEREE_BUNDLE_CONTENTS.json` | 77,354 | `b3af4bab82d9715841aed7f4c666309720f52fc78f6f560fd6325e26267b2753` |
| `output/referee/build_referee_bundle.py` | 7,401 | `b59301e07adbd232c45de820979a0f11aba88acb82bbcdb9456f4d886aa88207` |

The older five-dependency formulation does not describe this release. The
content ledger is one of these three; the theorem-artifact crosswalk producer
is an ordinary submission member.

### Submission layer and combined manifest

- Exactly 86 submission-source files and 4,268,041 bytes.
- Submission content root:
  `68c93bf97428d2f27064974f02cab5c1a0b3ac8ac863440adb96ebdc9ebad07c`.
- Combined count excluding the manifest: 494; combined root:
  `c63d27090e3598c45999db88db414de1fe20c654aa7bcec8cfa0508566bd06e7`.
- Manifest SHA-256:
  `fe9125f446556664c7ca3c818ba816aa84709956c6426acbea33dd5d81f66610`;
  logical payload
  `2a871f6f69561ac7a02b7fb167d655b712ba00b352cb0a3b254df41419fc7b77`.
- The theorem-artifact crosswalk has SHA-256
  `43b8a284d1a5c2a3997d467f6d917eaaa00378f432ab434913bf7868151698c8`,
  payload
  `5392819dff6b208569bfd1d6ec30f498b847d243708a4d6d665acafbefe6dc6a`,
  status `PASS_PC_PARTIAL`; 176 path/SHA occurrences were resolved directly to
  current files. This is a byte/path result only. It does not reconcile the
  stale current hashes printed inside the C09 word-theorem narrative; indeed,
  the crosswalk's current authoritative binding is what makes R6-M1 a live
  proof-to-artifact contradiction rather than a historical-document issue.

## Deterministic archive rebuilds

The independent archive writer
`independent_checks/provenance/independent_archive_rebuild.py` (SHA-256
`0b7f12d90b4f73b21d9dabbe5efeac1bfe4d9d0fb089a0794c6ed5b5dc118103`)
validated each manifest row and rebuilt the 495-member archive twice. Both
rebuilds and the distributed archive have exactly 214,977,546 bytes and SHA-256
`fef886379d9682586920a9f1112465dccab75267dbdd87a5b87b38dc4dbea513`.
Result: `evidence/provenance/INDEPENDENT_ARCHIVE_REBUILDS.json` (SHA-256
`a9816e541d52775b893d0e8498d376d6c56a575aea30504fb819833744427f99`),
PASS.

The separately asserted five-file bioRxiv source archive was also rebuilt
twice independently. All three archives are 57,892 bytes with SHA-256
`66527a3e3018b054f9e6b618a6c9e81a4ddbc6e2d0cced81542a0a7fe3eb3cd3`.
Result:
`evidence/provenance/INDEPENDENT_BIORXIV_SOURCE_REBUILDS.json`, PASS.

## Local Git commit and annotated tag

- `k2p-same-biorxiv-v1.0.5` is an annotated tag object.
- It peels to commit
  `5628a08f6bf3e5573ebbbf3e2dd8636ad00b338e`, matching the asserted seal
  commit.
- All 495 distributed package members are byte-identical to blobs in that tag:
  491 tagged as mode 100644 and four as mode 100755.
- Clean full replay telemetry names commit
  `5d541c46969e1508596e62a21bc5647dd1f1ba3c`, which is an ancestor of the
  tagged seal commit.
- The five exact submission sources and `RELEASE_LOCK.json` have identical Git
  blob IDs at the telemetry commit and final tag. Thus the post-replay seal did
  not change any telemetry-bound input.

This is a local Git audit. It verifies the commit and tag objects available in
the repository; it does not claim a GitHub Release or Zenodo state.

## Clean replay telemetry

- Stored report SHA-256:
  `0d2fd0206181fe4c08ebff1367592809d0b8126d58aee3d91980941bfa55a95e`.
- Telemetry SHA-256:
  `eab3c1d6a096ef469b3db4844ea567a49e8e8ea6e62a6c8a2506814773cb6d50`.
- Full mode, 41 layers, status PASS, promotion-ready, zero blockers.
- Internal elapsed time 6,361.013807 s; measured real time 6,361.55 s.
- Maximum resident set 2,543,091,712 bytes; peak memory footprint
  487,932,720 bytes.
- The telemetry's exact five source rows, release-lock bytes/payload, report
  hash, layer count, timing relation, and clean-detached flag all validate.

These are stored-run provenance facts. The root reviewer is separately running
fresh quick/full execution; this subaudit does not infer current computational
PASS from the stored report.

## R5 repair: typed terminal-registry anchor and narrative tables

The review-owned
`independent_checks/provenance/semantic_repair_audit.py` (SHA-256
`78dc80f064548082c0c35a7bc68b3ff715b104420e25e12410439b170294516f`)
imports no submitted module. Its result
`evidence/provenance/SEMANTIC_REPAIR_AUDIT.json` has status PASS, zero
mismatches, and independently establishes:

1. Supplement source lines 781--782 print
   “raw-four 934-class terminal certificate registry” with SHA-256
   `8d821c2000da5cf2647913cbdb42f8a42dfeb6826b8b76be49d91d78ebaf9998`.
2. The explicitly printed path is
   `work/corrected_composite_ledgers/artifacts/raw4_terminal_certificate_registry.json.gz`.
   It has schema `k2p-raw4-terminal-certificate-registry-v1`, payload
   `8f41e576ac8551ead8fd75d87c4b8d4aee85f5ba1007c0dcf8aaeb62fbfb1439`,
   and `terminal_class_count=934`.
3. The supplement explicitly distinguishes that object from the 16,974-row
   strict-sign overlay. The overlay remains SHA-256
   `5810ffb1d023e503eaa62d9705c28a85e9c724a6ad8357f49ebe61b2dde675dc`,
   schema `k2p-raw4-corrected-terminal-overlay-v2`; it is no longer mislabeled.
4. The submitted static auditor maps the printed label to the actual registry
   and requires both its schema and its 934 cardinality. Its stored result
   records the same typed values.
5. All 23 rows of the promotion manuscript's Appendix A snapshot have file
   hashes equal to current frozen bytes and payload hashes equal to the
   corresponding current certificate/summary payloads.
6. All previously stale raw-four, theta2, restoration, registry, stream, and
   release-replay values in the corrected-composite README and corrected-
   universe contract are current. Their release-replay payload is now
   `98c564205133bc383ba8814ef674c65ea09fe891f9898139f11d313afb107e64`.
7. The three narratives are current lock-bound reader snapshots, explicitly
   defer to `RELEASE_LOCK.json`, and contain current values. The theorem
   crosswalk marks the promotion manuscript as a machine-bound companion, not
   current submission proof authority.
8. The separate historical registry contains eight correctly classified,
   non-promoting objects with bound current replacements. None of the three
   current narratives is misclassified as historical.

The submitted focused semantic mutation suite freshly rejected all 11 cases,
with zero survivors. In particular:

- replacing the typed registry with an overlay is rejected for
  `PRINTED_FROZEN_ANCHOR_SCHEMA_DRIFT`;
- changing the registry to 16,974 rows is rejected for
  `PRINTED_FROZEN_ANCHOR_CARDINALITY_DRIFT`;
- stale hashes, missing/duplicated/extra rows, reassigned metadata kind, and a
  missing target are rejected for their intended diagnostics.

The fresh static audit passed in the configured disposable copy. A deliberate
attempt in the bare isolated extraction failed closed at
`CROSSWALK_PATH_MISSING:.venv/bin/python`; this is the documented environment
setup boundary, not a package defect. No PASS was inferred from that failed
attempt.

## PDFs and exact five-source build

Result:
`evidence/documents/PDF_SOURCE_CONSISTENCY_AUDIT.json` (SHA-256
`c222b6a5753df5f7b4743240acfaf3f4192adf5f9eee5422dc6df2a3a31dea2d`,
payload
`bdc2d37f04fde8709861ed9bc6c0bd5ba58c51c3ad958372790696950c53a82f`),
PASS.

Exactly these five sources were staged:

| source | bytes | SHA-256 |
|---|---:|---|
| `article/main.tex` | 85,978 | `43278b63cc6d123fc8ec970178e886e9a57d02c879a2ff748887572f29eeb27d` |
| `article/references.bib` | 6,960 | `781dd3503c00d9bbd9c1a7d551786fc4be393e883f7ac4c0b0fd712943a9e5c6` |
| `supplement/supplement.tex` | 46,724 | `d5f79a95a7ec0aff2ce4e8e3f818dcf930435dcde2265ed23dc6bacede1fea33` |
| `supplement/compression_tables.tex` | 3,269 | `22ff0534b79cf226c9041703ab9d87ab123914bbb55ec1d44c84041a8616be81` |
| `supplement/certificate_appendix.tex` | 22,405 | `1f7590b2930f8ac1536724763d0b30e330f817fd3127edae0df3ee520180c649` |

The disposable build rebuilt both PDFs twice. Each pair was byte-identical and
also byte-identical to the distributed output:

| PDF | pages | bytes | SHA-256 | embedded fonts |
|---|---:|---:|---|---|
| article | 26 | 194,542 | `e49e72c09183679f04362afe37917e410f0b8b6fe5dc98f423a0b642dce78cf4` | 22/22 |
| reader supplement | 24 | 160,762 | `0448cfc078f91d0bb5f08097e3055d302e1ef5308664dc3a7443e728f38ffd9d` | 28/28 |

The build logs match the report and contain zero fatal LaTeX errors, overfull
boxes, undefined citations/references, or hyperref PDF-string warnings. Omission
of either generated supplement input failed at its unconditional input. In a
separate coherent outer-manifest attack, deletion of
`article/references.bib` exited 1 with exactly:

```text
required submission source missing: ['proof_compression_submission/article/references.bib']
```

All 50 pages were rendered through Poppler and visually inspected in 13 contact
sheets; supplement page 21 was additionally inspected at full render
resolution. I found zero clipping, overlap, broken tables, unreadable glyphs,
or layout defects. The repaired registry hash, typed path, schema, 934 count,
and explicit distinction from the 16,974-row overlay are legible on page 21.

The fixed PDF source epoch is 2026-08-27T00:00:00Z; the corresponding local
PDF creation timestamp appears as 2026-08-26 17:00 PDT. This is the declared
reproducibility epoch, not package-date drift.

## Command ledger for this subaudit

All ordinary commands exited 0. The one isolated static-audit attempt noted
below intentionally exited 1 because the bare extraction has no `.venv`; the
configured-copy rerun exited 0.

Exact substantive commands (the review command wrapper recorded the absolute
working directory, stdout/stderr hashes, resource use, and exit status):

```sh
python3 -B independent_checks/provenance/probe_narrative_binding_audit.py --project isolated/k2p_principal_d_plus_submission_referee --output evidence/provenance/PROBE_NARRATIVE_BINDING_AUDIT.json
python3 -B independent_checks/provenance/semantic_repair_audit.py --project isolated/k2p_principal_d_plus_submission_referee --output evidence/provenance/SEMANTIC_REPAIR_AUDIT.json
python3 -B proof_compression_submission/adversarial_review/test_printed_authority_hash_gate.py
python3 -B independent_checks/provenance/independent_provenance_audit.py --project isolated/k2p_principal_d_plus_submission_referee --archive /Users/alec/Documents/Math/k2p_level2_identifiability_closure/proof_compression_submission/output/K2P_Principal_D_Plus_Referee_Package_20260829.zip --git-repo /Users/alec/Documents/Math/k2p_level2_identifiability_closure --output evidence/provenance/INDEPENDENT_PROVENANCE_AUDIT.json
python3 -B independent_checks/provenance/independent_archive_rebuild.py --project isolated/k2p_principal_d_plus_submission_referee --source-archive /Users/alec/Documents/Math/k2p_level2_identifiability_closure/proof_compression_submission/output/K2P_Principal_D_Plus_Referee_Package_20260829.zip --first tmp/archive_rebuild_1/K2P_Principal_D_Plus_Referee_Package_20260829.zip --second tmp/archive_rebuild_2/K2P_Principal_D_Plus_Referee_Package_20260829.zip --output evidence/provenance/INDEPENDENT_ARCHIVE_REBUILDS.json
python3 -B independent_checks/provenance/independent_biorxiv_source_rebuild.py --source-root isolated/k2p_principal_d_plus_submission_referee/proof_compression_submission --archive /Users/alec/Documents/Math/k2p_level2_identifiability_closure/proof_compression_submission/output/K2P_SAME_bioRxiv_Source_20260829.zip --first tmp/biorxiv_rebuild_1.zip --second tmp/biorxiv_rebuild_2.zip --output evidence/provenance/INDEPENDENT_BIORXIV_SOURCE_REBUILDS.json
.venv/bin/python -B output/referee/build_referee_bundle.py --check-only
.venv/bin/python -B work/final_theorem_release/build_release_lock.py --check --require-ready
.venv/bin/python -B proof_compression_submission/crosswalk/build_theorem_artifact_crosswalk.py --check
.venv/bin/python -B proof_compression_submission/crosswalk/build_revised_referee_bundle.py --check
.venv/bin/python -B proof_compression_submission/crosswalk/check_revised_referee_bundle.py --manifest proof_compression_submission/crosswalk/REVISED_REFEREE_BUNDLE_MANIFEST.json
.venv/bin/python -B proof_compression_submission/build_submission_pdfs.py --visual-pass --check
python3 -B independent_checks/provenance/bibliography_omission_test.py --project isolated/k2p_principal_d_plus_submission_referee --python execution/k2p_principal_d_plus_submission_referee/.venv/bin/python --scratch tmp --output evidence/documents/BIBLIOGRAPHY_OMISSION_TEST.json
python3 -B independent_checks/provenance/build_pdf_evidence.py --project isolated/k2p_principal_d_plus_submission_referee --review-root . --output evidence/documents/PDF_SOURCE_CONSISTENCY_AUDIT.json
.venv/bin/python -B proof_compression_submission/adversarial_review/audit_article_sources.py
```

| command/evidence | exit | wall s | peak RSS bytes | stdout SHA-256 |
|---|---:|---:|---:|---|
| independent C09 narrative-binding attack | 1 expected (finding reproduced) | 0.084670 | 34,635,776 | `c0eaac37c4077b0f5d1f1e58c720a60ba1dc37b750ba1d6cf643e22fda8fe62a` |
| independent semantic repair audit | 0 | 0.591940 | 218,431,488 | `c65563f0ce94c9fc6565fd448c6adcccdb5589e311f0ad26954b2c923f47688a` |
| printed authority/hash mutations | 0 | 0.058697 | 28,098,560 | `f88d3b23d5be6348e13bc68ef9442cfb2809719a284db981198535c69b1b7246` |
| independent provenance audit | 0 | 2.188059 | 393,560,064 | `49de2115968b8251b7d9532be6e3fca3bafcf8ae624d334734f90699b92a412e` |
| independent referee-archive double rebuild | 0 | 41.879459 | 250,576,896 | `7088fc92c2c3ec19fa26aa06812b73a20d20b49e20451ed0477fe36e49ee96ae` |
| independent bioRxiv-source double rebuild | 0 | 0.075176 | 24,576,000 | `382e8adf23884276b597245e994edd1c91fd7b9c5d04085e551ae18ee8b6e2cb` |
| portable referee-ledger check | 0 | 0.674669 | 231,473,152 | `e629be6db2848c9a83376f28c15bcb169af53c607167f27c761adbd37197699c` |
| release-lock check/require-ready | 0 | 16.108591 | 491,061,248 | `94e35b899bc88b934be42a11f470355f645b4fb1aaa35bd305574fbd5894350e` |
| theorem crosswalk regeneration check | 0 | 0.299272 | 178,733,056 | `26cc1c27c8d650495eb2d4bb328c7c1980653a5771c5f8faf6477b1855480c35` |
| revised-bundle producer check | 0 | 122.143495 | 277,233,664 | `415373e5b9a0caca9351c8bcb0b9aeb9a2dad6d1993a2eab118fae01e08f3adb` |
| revised-bundle independent checker | 0 | 127.083402 | 279,773,184 | `415373e5b9a0caca9351c8bcb0b9aeb9a2dad6d1993a2eab118fae01e08f3adb` |
| PDF double build + two generated-input omissions | 0 | 13.315202 | 256,344,064 | `37d452846e17e734c72c499f57503a7363d02df145fcaf02ae49928a9d39975a` |
| bibliography outer-manifest omission attack | 0 (attack observed 1) | 120.749663 | 382,763,008 | `5036a493e1aa1e05bb0632dc465dda8e67a1450cb400ec4c567d0ee8067bc021` |
| PDF/source evidence collation | 0 | 0.195544 | 24,952,832 | `b9f80fd194b94f3f57117874012edc1dfa3b32a5e6734a4ca0f359e9821dc831` |
| static article audit, bare extraction without `.venv` | 1 expected | 0.208714 | 44,646,400 | `3f793e0faa5a122f9b747dbaf95fe0bda96fc93ab0f22d47606377791e907207` |
| static article audit, configured disposable copy | 0 | 0.242604 | 45,219,840 | `df9582acafb22ad14c3283f3c8558258c91fd60cd9cc7ae29c68808574699cc9` |

Every recorded stderr hash, including the expected R6-M1 failure, is the empty SHA-256
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

## Assessment for the main referee report

- Integrity/provenance: **PASS**.
- Deterministic archive reconstruction: **PASS** for both distributed ZIPs.
- Release lock and stored telemetry byte provenance: **PASS**.
- Crosswalk path/hash resolution: **PASS**; C09 semantic narrative binding:
  **FAIL**.
- R5 semantic-anchor and stale-current-narrative repair: **PASS**.
- Exact five-source PDF reconstruction and omission gates: **PASS**.
- PDF visual/layout and font audit: **PASS**.
- Overall document/reproducibility release status: **HOLD** pending R6-M1
  repair and affected resealing.
- Human release state: local commit/tag facts verified; remote hosting, GitHub
  Release, Zenodo, and DOI state are outside this local audit.

The two hashes in the current C09 word-theorem narrative must be corrected; a
semantic theorem-to-certificate binding gate and focused mutations must be
added; and affected derived manifests, archives, digests, commit, and tag must
be regenerated and rechecked before submission.
