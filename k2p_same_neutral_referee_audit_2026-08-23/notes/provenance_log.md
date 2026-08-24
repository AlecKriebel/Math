# Provenance and reproducibility audit log

## 2026-08-24T04:49:39Z — checkpoint 0

- Completion estimate: 5%.
- Scope fixed: integrity, outer/inner ledgers, supplemental dependency binding, deterministic handoff archive reproduction, PDF/source/report/lock/telemetry consistency, verifier mutation behavior, and clean five-source manuscript builds.
- Safety boundary: authoritative files under `isolated_handoff/` are read-only for this audit. Independent scripts live under `scripts/provenance/`; logs, reports, and disposable copies live elsewhere in this audit folder.
- Initial observation: the containing repository already has unrelated user changes. This audit will not touch them.

## 2026-08-24T04:55:29Z — checkpoint 1

- Completion estimate: 28%.
- Inspected `verify_handoff.py`, `test_handoff_mutations.py`, `build_handoff_manifest.py`, `build_handoff_archive.py`, `check_manuscript_build.py`, and `setup_environment.sh` before running them.
- Submitted verifier: PASS, exit 0, 0.90 s real, maximum RSS 283,279,360 bytes. Submitted outer mutation suite: PASS, exit 0, 2.63 s real, maximum RSS 280,723,456 bytes.
- Independent ledger implementation (no submitted module imported): PASS. It compared all 492 outer paths and all 447 sealed inner paths, plus the inner manifest and five explicitly unsealed dependencies. Counts, byte totals, every file hash, both payload hashes, both content-ledger roots, the combined inner root, and the outer content root agree.
- The complete inner project has exactly 453 non-environment files: 447 sealed files, the inner manifest, and the five declared supplemental dependencies. There are no other extras, overlaps, missing paths, symlinks, or row mismatches.
- All five supplemental dependency bytes match Git commit `078b573d214ff598868d1b5dbf9565ef267bb257`; exactly the declared two have byte-identical copies in the older inner seal. The content ledger `output/referee/REFEREE_BUNDLE_CONTENTS.json`, required by the theorem-artifact crosswalk producer, is one of the three with no sealed copy.
- Captured each mutation's actual stderr separately. All six routes (five resealed manifest mutations plus optimized Python) failed for their intended reason.
- Evidence at this checkpoint is provenance/computational integrity only, not mathematical validation.

## 2026-08-24T05:10:50Z — checkpoint 2

- Completion estimate: 76%.
- Deterministic archives: two separately copied clean handoff trees each passed integrity verification, then independently produced a 493-member, 178,524,867-byte ZIP. Both rebuilt ZIPs and the distributed ZIP are byte-identical with SHA-256 `c681f1984dbd95c7a8095593da339488544e03825232b5f8488050e94cdc27fd`. All member content, order, CRCs, timestamps, compression, Unix modes, and absence of extras/comments were independently checked. The older 448-member inner archive likewise matches its `ab7c3c...` binding and every inner-ledger member.
- Clean manuscript builds: exactly the five bound source files were copied to a disposable tree. Tectonic 0.16.9 compiled the 26-page article and 24-page supplement with exit 0. Both new log files are byte-identical to the sealed logs (`beff8b...` and `d1bef9...`) and contain none of the declared defect patterns.
- Current-time PDFs differ from sealed PDF bytes only in creation metadata/trailer IDs; all 50 corresponding 96-dpi rendered PNGs are byte-identical. Rebuilding with `SOURCE_DATE_EPOCH=1787465144` (article) and `1787465911` (supplement), the creation instants stored in the sealed PDFs, reproduces the sealed PDFs byte-for-byte (`86b7ac...` and `177006...`). These epoch values are derivable from PDF metadata but are not documented in the build report.
- Omission tests: removing `compression_tables.tex` fails at `supplement.tex:307`; removing `certificate_appendix.tex` fails at `supplement.tex:441`. Removing `references.bib` is tolerated by Tectonic with BibTeX errors and undefined-citation warnings, exactly as the report says, but physical omission from a disposable full handoff is rejected by the outer ledger (`declared=492 actual=491`).
- PDF integrity: Poppler parsed all pages, extracted text, and rendered every page; all fonts are embedded. Complete-page montages plus dense representative pages showed no apparent clipping, overlap, broken glyphs, or unreadable layout.
- Mutual consistency: independently checked the 198-row release lock, 374-row frozen content ledger, inner source manifest, 35-layer stored replay report and telemetry, PDF build JSON/Markdown, five sources, two PDFs, two build logs, and 130 theorem-crosswalk artifact rows. All hashes, byte counts, payloads, statuses, and cross-bindings agree. This is provenance/computational consistency, not validation of theorem semantics.
- Nonblocking review-process event: a reviewer-generated PNG was briefly written under `isolated_handoff/tmp/`, causing both outer checks to detect an extra 493rd file. It was moved recoverably to audit-root `tmp/pdfs/`; subsequent submitted-verifier, producer `--check`, and independent-ledger runs all returned PASS with the original 492-file ledger. This was external audit interference, not a submission defect.

## 2026-08-24T05:29:43Z — checkpoint 3

- Completion estimate: 100% for the assigned provenance, integrity, archive, dependency-binding, and manuscript-reproducibility track.
- Reconciled the Englander-v4 hash: the exact historically reviewed 31-page, 927,795-byte file with SHA-256 `3c140c36...` is retained in Downloads with an August 17 acquisition record. The current official download is the same size with SHA-256 `69f04a54...`; only 55 bytes of mutable PDF dates/IDs differ. Both text extractions and all 31 corresponding 96-dpi page renders are byte-identical. Classified as a nonblocking literature-provenance/external-rendition observation, not a citation or mathematical defect.
- Searched the current Git object database, all 84 readable ZIP archives, and 60 readable non-environment TAR archives under the Math repository. Three unrelated `.tar`-suffixed files had invalid headers. The exact `3c14...` bytes are not redistributed in the readable archives; Git contains two other metadata renditions. This is consistent with the package's decision not to redistribute a third-party PDF.
- Final track result: provenance/integrity PASS; manuscript reproducibility PASS; rendered-PDF integrity PASS; human metadata/release HOLD as deliberately pending and non-scientific. No reproducibility-blocking defect remains.
- Final report: `notes/provenance_reproducibility.md`, SHA-256 `5b72cff511e35d9408fc91194fb12b28acc26b27e2a421fd443ebeb1716b683f`.
- Machine execution ledger: `reports/provenance/execution_ledger.json`, SHA-256 `8001f09b7f3952ce96d55707fd8889cee77c868c9d4b8acbd75461dcc7c9dd80`.
