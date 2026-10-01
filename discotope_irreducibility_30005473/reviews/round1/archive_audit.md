# Round 1 archive and reproducibility audit

Independent bounded audit of the frozen preprint package. No prior `reviews/initial*` review prose was read. The mathematical proof is assigned to a separate audit. Canonical scientific files, branches, commits, and remote state are outside this audit's write scope.

Target received and copied into ignored `tmp/round1/archive_audit/`:

- `paper.pdf`: SHA-256 `c13dc861e8e5b5c1d980bdd78d14aff8e4b1a130800c4f942b3bedafbc5f6b2a` (79,805 bytes).
- `source-and-verification.zip`: SHA-256 `bd03b7a8bee9c8f4efdaac2fcf83f424be3a0570a3c5a57313f70822ce449a85` (815,805 bytes, 70 members).
- `zenodo-upload-kit.zip`: SHA-256 `e4f4c499f763f31a053449b97409b5d423338d66177f66805f9ed8a7a30d2b33` (889,429 bytes).

## Audit log

- 2026-10-01T03:52:57Z — Scope defined: verify hashes, packaging consistency, metadata/licenses, frozen-source provenance, dependencies, executable reproduction, references, exclusion policy, and credential/full-text exposure. Completion estimate: 10% of this bounded audit; no correctness probability implied.
- 2026-10-01T03:54Z — Refreshed target copied and safely extracted into scratch after earlier package revision. Confirmed frozen PDF hash, ZIP integrity, unique member paths, and no absolute/traversal paths. Independent static audit delegated without access to historical review prose. Completion estimate: 20%.
- 2026-10-01T03:56:35Z — All 69 declared member hashes/sizes and the 70-member inner inventory matched. Outer upload kit, metadata, checksum file, PDF binding, historical 16-file snapshot manifest, and recorded reproduction manifest matched. Fresh CPython 3.14.6 environment with pinned SymPy 1.14.0 and mpmath 1.3.0 reproduced both scripts with assertions enabled, empty stderr, preserved snapshot bytes, exact original output, and independent output equal apart from timestamp. Completion estimate: 70%.
- 2026-10-01T03:56Z — All 16 historical snapshot hashes also matched their files read directly from local Git commit `a29887ed0e341851d02fa992c26500d4089267be`. A separate pristine extracted copy plus the frozen PDF rebuilt both archives byte-for-byte. Completion estimate: 80%.
- 2026-10-01T03:59Z — Static findings independently confirmed: raw retrieval JSON contains substantial third-party PDF/HTML extracts; current archive contains only historical `initial_*` reviews. Credential-pattern screening of 66 non-review text files found no candidate credentials. Reference/exclusion classification completed. Completion estimate: 100% of this frozen-target audit; publication readiness remains contingent on the repairs below.

## Result

**Executable reproduction and integrity pass. Two package assembly repairs are required before publication.** Neither finding questions the finite symbolic output; universal mathematical claims remain the responsibility of the separate proof audit.

### A1 — Material: raw third-party text survives the intended exclusion

`build_package.py`, lines 56–73, recursively includes all `.json` files under `priority/`. This includes these frozen archive members:

- `priority/equivalent_results/web_results_archive.json` (372,235 bytes).
- `priority/equivalent_results/web_results_archive_addendum.json` (99,392 bytes).
- `priority/equivalent_results/citation_subaudit/evidence/search_responses.json` (129,988 bytes).

The files contain literal captured PDF/HTML text, beyond concise source identifiers or query metadata. Independently counted examples:

| File and JSON field | Characters | Approximate whitespace words |
|---|---:|---:|
| `web_results_archive.json`, `results.open02` | 23,269 | 3,739 |
| `web_results_archive.json`, `results.open04` | 24,378 | 3,067 |
| `web_results_archive_addendum.json`, `results.find02` | 10,350 | 1,540 |
| `citation_subaudit/evidence/search_responses.json`, `responses.content_checks` | 25,461 | 3,191 |

Counts include retrieval wrappers and sometimes multiple documents; they are evidence of substantial copied extraction, not an assertion that every word belongs to one source or that an entire source was copied. The independent static auditor reached the same finding before this confirmation. A scan of all archived JSON leaves larger than 2,500 characters found such large text fields only in these three files.

This directly contradicts `PACKAGE_MANIFEST.json`'s exclusion of “third-party source PDFs and full-text extracts,” `priority/README.md`'s statement that extracted full texts are excluded, and `priority/equivalent_results/priority_report.md`, line 146, which describes downloaded PDFs/full extracted texts as local audit aids and the concise report/structured evidence as the intended publication artifacts. This is an internal package-policy failure; no legal conclusion about a particular source license is required to establish it.

**Exact repair:** exclude the three raw retrieval capture paths from the public source builder, preserving them locally. Retain the authored reports, complete query lists, bibliographic evidence, inspected locations, source URLs, and hash manifests. Update the affected report/evidence references to explicitly identify raw captures as local-only, then rebuild the inner archive, upload kit, `SHA256SUMS`, and `package-build.json`. Recheck member inventory and all hashes on the rebuilt target.

### A2 — Final assembly: fresh preprint reviews are absent from this target

The frozen inner archive has exactly these review members:

- `reviews/initial_algebra_reproduction_audit.md`.
- `reviews/initial_analytic_convex_audit.md`.
- `reviews/initial_generic_face_audit.md`.

Their prose was not read. `README.md`, line 7, expressly distinguishes historical original-PR reviews from the fresh reviews required for the new research note, yet says fresh publication reviews are in `reviews/`. The metadata/manuscript also present independent adversarial reviews as package contents. Current-round review reports are absent from this particular frozen archive. The initial archive may sensibly be an input to review, but it cannot serve as the final package with those fresh-review statements still in force.

**Exact repair:** complete and include the final fresh preprint review reports, then rebuild and verify the release package. Each review should retain the precise target hash it actually audited; the final package can include the review of its scientific inputs together with the post-assembly inventory verification, without falsely claiming a review of its own recursively included final bytes. Alternatively qualify the content claim if fresh reviews will remain external.

## Reproducibility and integrity evidence

- `PACKAGE_MANIFEST.json` has 69 content entries, plus its own unlisted inventory file, exactly covering the 70-member source ZIP. Every archived size and SHA-256 matched.
- `output/package-build.json` binds the observed source ZIP, kit, metadata, and 79,805-byte frozen PDF. `SHA256SUMS` matches both deposited files.
- The upload kit has exactly `paper.pdf`, `source-and-verification.zip`, `api-metadata.json`, `zenodo-deposit.json`, `SHA256SUMS`, and `UPLOAD.md`. Its deposited file bytes equal the frozen audit copies. Its metadata equals the inner metadata and root deposit metadata, and the path adjustment to flat kit names is consistent.
- The 16-file original source snapshot is complete, matches `original_snapshot_manifest.json`, matches the before-hash map in `reproduction_manifest.json`, and matches the claimed historical commit directly from local Git objects. The new manuscript is correctly distinguished from that original snapshot.
- Source ZIP and kit CRC tests pass; members are unique, use relative paths, and contain no traversal. Symlinks, hidden folders, environments, and scratch are excluded by the builder. The only PDF member of the source ZIP is the authored historical `verification/source_snapshot/proof.pdf`; third-party PDF files themselves are absent.
- No credential-pattern candidates appeared in 66 inspected non-review text files. Historical review prose and binary PDF internals were outside this semantic credential screen. Filename-level exclusions also omit credentials and publication receipts. This is a bounded screen, not a certificate that every possible secret encoding is absent.
- License and author metadata consistently identify Alec Kriebel, the supplied ORCID, CC BY 4.0 research prose, MIT verification/build code, an unrefereed preprint, and substantial generative-AI assistance. Third-party references are explicitly excluded from the author's relicensing claim.

Fresh reproduction was performed only in ignored scratch extracted from the audited archive:

```
tmp/round1/archive_audit/.venv/bin/python -B extracted/verification/source_snapshot/checks.py
tmp/round1/archive_audit/.venv/bin/python -B extracted/verification/independent_checks.py
```

Both scripts were inspected before execution. They request no network access; the independent script writes only its expected verification outputs in the extracted scratch copy. Environment: CPython 3.14.6, SymPy 1.14.0, mpmath 1.3.0; optimization level 0. Both exits were zero and both stderr streams empty. Fresh independent JSON equals archived `independent_results.json` after removing only `utc`. Original output is byte-identical to `source_snapshot/checks_output.json`, SHA-256 `1bab82a3df95caf30ce8c5a91916625b464e9c71b489f66009e3cb369fea314a`. All snapshot bytes remained unchanged.

The original requirements pin both Python packages exactly. The recorded exact Python version is reproduced here. Dynamic timestamps in fresh output are an explicitly identified nondeterministic field; they are not silently discarded from an alleged byte-exact result. A separate pristine archive extraction with the separately deposited frozen PDF placed at `output/pdf/paper.pdf` ran `build_package.py` successfully and regenerated source ZIP `bd03b7a8…` and kit `e4f4c499…` byte-for-byte.

Scratch evidence files include `frozen-target.json`, `integrity-results.json`, `fresh-reproduction.json`, `rebuild-results.json`, and captured fresh stdout/stderr. They remain ignored audit scratch and are not publication artifacts. No canonical scientific file, branch, commit, push, or outside communication was changed by this audit.

## Referenced artifacts: inclusion versus deliberate local evidence

`priority/equivalent_results/priority_report.md`, lines 140–142, lists the two raw web archives and `kk2017_ocr-11.png` plus its OCR derivative among checkable artifacts. In this target the two web archives are included; the PNG and OCR derivative are absent. The report's line 146 and the package exclusion policy explicitly identify downloaded PDFs and extracted source texts as local evidence. Therefore omission of the page image/OCR is deliberate source-exclusion, not loss of executable verification inputs. The report supplies the primary PDF URL, printed p.95/Proposition 4.3 location, source hash via `local_sources_manifest.json`, and a short quoted observation, allowing independent retrieval.

The list should nevertheless distinguish **included public artifacts** from **local source audit aids**. That clarification is part of A1's exact repair and prevents treating the missing image/OCR or newly excluded raw captures as promised archive members. The source check scripts and all their required archived inputs are present; they do not depend on those excluded literature aids.

Strongest verified result: the frozen package is internally hash-consistent and its advertised finite exact checks reproduce. Exact remaining publication gap: repair the declared source-exclusion policy and finish fresh-review package assembly; then verify the new package inventory/hashes. No unconditional publication-ready verdict is issued for this frozen target.
