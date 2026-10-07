# V2 scoped QA receipt

Completed 2026-10-07T04:49:52.605570+00:00; scoped QA completion estimate **100%**. **Frozen v2: PASS.** Candidate remains **NOT PUBLISHED** and was superseded by v3 during this audit.

**Current-project upload binding fails for v2:** deposit paths name mutable publication/upload-kit files that now select v3 PDF/ZIP bytes. This is recorded separately from intact v2 package integrity. Do not select v2 using those current paths. No staging is authorized by this receipt.

## Exact reviewed versions

| Input | SHA256 |
| --- | --- |
| `upload-kit/paper.pdf` | `89aea154c312cb36a5520f25944f371975f0f5313acf316093792c4a6213f43e` |
| `upload-kit/source-and-verification.zip` | `28274ab18a2ab300160e25128419994b960de438bc582926a33e3ca0b2f3457a` |
| `source-and-verification/main.tex` | `8c6d45b8408bb89da4412263becc6956e1b63229ef81daec1caa28272fedad21` |
| `source-and-verification/ARCHIVE_MAP.json` | `ec2d026099483012d19ae77647b9801d3e8537e3bf7ca0383163714661094bcc` |
| `REVIEW_INVENTORY.json` | `76251455a069d065159940139c58618e6e3437d824b55d9c102d36018842b312` |
| `zenodo-deposit.json` | `898412d64eef19477c6dbc5eb299d607508d5f36ccdf5d99b9ce5a4a30e057f0` |

## Verified checks

All **10 pages (1-10)** were individually inspected from new 110 dpi renders. No visible clipping, overlap, unreadable glyphs, formula/number collision or unresolved references. The source has 28 unique labels and all 6 cited bibliography entries resolve. The final TeX log has no overfull/underfull boxes or LaTeX/hyperref warnings. All fonts (25) are embedded and subset; the five math font subsets without Unicode maps render correctly and produce no replacement glyphs. Internal PDF link destinations resolve.

The existing Tectonic **0.17.0** compiled a fresh temporary source copy using `--untrusted --only-cached --keep-logs --keep-intermediates` and standard-library SSL trust paths. Exit code 0; no runtime installation or network TeX fetch. Rebuilt PDF SHA256 `ca46d5fb0ccc16677c56049b88c7e734d27695c7a069df362f71f64748643bb2`. All 10 page images, extracted page text, complete layout text and page content streams match the reviewed v2 PDF. Metadata differs only in CreationDate; file hashes therefore differ.

All three standard-library certificate scripts run under isolated Python 3.12.14 and exit 0. The kernel checker reports zero residuals plus 292 exact rational inputs; the rational selection margins and signed-pair polynomials pass. **Certificates establish algebra only.** Mechanical comparison also finds all 42 displayed mathematical source blocks and the three certificate scripts byte-identical between v1 and v2; it does not validate their mathematical premises or the new inline equal-ratio explanation.

Independent frozen archive/metadata audit passes **31 checks**, plus **12 independent reference checks**: 31 packet files including inventory, 30 inventory entries, 26 archive/source files, 25 payload hash entries. Every size/hash/ZIP byte/CRC/whitelist check passes. All 128 document references are classified as supplied, contextually mapped, deliberately excluded pinned input, or historical/optional evidence. No broken current supplied-file promise was identified. Whitelist and credential-pattern scans found no cache/dependency tree, third-party source/PDF corpus, unsafe ZIP member, or credential indicator; arbitrary encoded secrets are not ruled out by pattern matching.

Author/title/date/license match: sole author Alec Kriebel, visible linked ORCID 0009-0001-9320-500X, no affiliation or coauthor, October 6, 2026, CC BY 4.0. V2 deliberately removes internal pending labels and presents final theorem language. This is editorial presentation; the packet inventory still records no publication, and this QA provides no mathematical certification. No own DOI or Zenodo record is claimed.

## Pages actually inspected

- **Page 1:** Title, sole author/ORCID/date, revised abstract without internal pending notice, section 1, normalization/system (1.1)-(1.2), and beginning of Theorem 1.1/data (1.3).
- **Page 2:** Theorem 1.1 continuation, expanded field-regularity explanation, pinned upstream attribution, equal charge-to-mass-ratio paragraph, new small-data literature paragraph/citation [6], section 2, flow (2.1), energy (2.2).
- **Page 3:** Energy/flux continuation, budgets (2.3), separate label spaces, section 3, geometry/measure/kernel/coefficient (3.1)-(3.4).
- **Page 4:** Complete interior pair force, Lemma 3.1/cancellation (3.5), proof identities, residuals (3.6), section 4 opening, common dyadic cap and definitions.
- **Page 5:** Bootstrap (4.1), bin definitions, hit/stable-cell/refined occupation (4.2)-(4.5) and exceptions.
- **Page 6:** Subsection 4.1, direct field/kernel majorants (4.6), near/far bounds, baseline/absolute estimate (4.7), receiver majorant (4.8), moving projector and integration-by-parts paragraph.
- **Page 7:** Subsection 4.2, direction-count inequality, window/improved occupation/selection/coefficient/safety (4.9)-(4.13), exponent definitions and comparison inequalities.
- **Page 8:** Exact exponent contradiction continuation, weighted impulse (4.14), section 5 closure and momentum doubling, section 6 opening.
- **Page 9:** Section 6 continuation/local theory, logarithmic derivative inequality, Coulomb transform, potential/localization formula, vacuum argument and uniqueness; revised proof-completion language.
- **Page 10:** Section 7 boundary cases, field regularity limitations, algebra/formal/AI/no-human-peer-review disclosures, all six bibliography entries including new [6].

Theorem 1.1 spans pages 1-2; section 6 begins with two lines on page 8 and continues on page 9. Neither creates an orphan heading or clipping. Section 7 and all six bibliography entries are on page 10.

## Recorded advisory gaps

The independent receipts identify three nonblocking historical-navigation observations: excluded formal reproduction/config/log artifacts still appear in historical report wording (qualified by its leading archive note); optional project-priority receipts are not supplied and the project-repository link is absent; the statement that source PDF/API hashes are supplied is broader than the actual included digest coverage. Exact locations and reference classifications are in `package_audit/reference_check/reference_receipt.md`. The v1 BGP auxiliary-bibliography omission is fixed.

Initial builder/source/upload matches and the later root-directed v3 drift are preserved in `INITIAL_MATCH_EVIDENCE.json` and `project_drift_detected.json`; v2 input bytes and v1 QA receipts remain unchanged.

## Scope and evidence

This is **presentation, source correspondence and package/reproducibility QA only**. It supplies no full mathematical, priority, novelty, Lean/formal, human-peer-review or publication approval. No source edit, Git, upload, tracker mutation or external individual communication occurred.

Machine receipt: `QA_RECEIPT.json`; all-page visual receipt: `MANUAL_VISUAL_REVIEW.json`; rebuild/certificate logs and comparisons remain adjacent. `run_source_pdf_checks.py` repeats mechanical checks using existing runtimes. Independent archive/reference receipts and reproducible scripts are under `package_audit/`. Inspected renders are retained in `visual_evidence/`; temporary duplicate builds/renders/certificate copies were cleaned. `QA_ARTIFACT_SHA256.json` identifies all retained receipt/evidence files.
