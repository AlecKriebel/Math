# V3 scoped QA receipt

Completed 2026-10-07T04:53:08.569566+00:00; scoped QA completion estimate **100%**. Frozen v3 integrity, source reproduction and legibility **PASS**. Candidate remains **NOT PUBLISHED** and was superseded by repaired v4.

**Presentation finding V-P1:** Page 11 contains only bibliography entry [7], three lines, leaving nearly the entire final page blank. Content is readable and complete, but the short final page is a pagination blemish. It was reported to root; root subsequently froze v4 with a bibliography-only repair. This v3 receipt preserves the original finding and reviewed bytes.

**Current upload paths select v4:** v3 deposit paths refer to mutable project upload files, whose PDF/ZIP hashes no longer match v3. Initial v3 matches and subsequent drift are separately preserved by the independent archive audit. Do not select v3 through those current paths.

## Exact reviewed versions

| Input | SHA256 |
| --- | --- |
| `upload-kit/paper.pdf` | `20581b8b253c470d9fd775f88931002fc99729b7d7db21da5e6274482c5b990a` |
| `upload-kit/source-and-verification.zip` | `b14fa882d987ef6b168b9b821c86b1685f4e6abcd7540837e9f3afa9c0cff527` |
| `source-and-verification/main.tex` | `2f98fe5e29570675d4d583b1151a247ead90c6ed0d44302aa5d47c74c4964872` |
| `source-and-verification/ORIGINAL_CONTINUATION_ATTRIBUTION.json` | `f22169b396017e2b066f4f6695125948b2c306cdf8a60cf5640167104c99478a` |
| `source-and-verification/ARCHIVE_MAP.json` | `19a89b46da112bc7ade64a202097d0247e32e8ea75149c505383288724c63927` |
| `REVIEW_INVENTORY.json` | `618a97cb40f8e31debfd21a7bdd9d96dbc39dfdc857a44a0de74385ca39229fc` |
| `zenodo-deposit.json` | `898412d64eef19477c6dbc5eb299d607508d5f36ccdf5d99b9ce5a4a30e057f0` |

## Check evidence

All **11 pages (1-11)** were individually visually inspected from new 110 dpi renders. Apart from V-P1, no clipping, overlap, broken glyph, formula/number collision or unresolved reference was found. All 7 citation keys and 28 unique labels resolve; TeX reports no overfull/underfull box or LaTeX/hyperref warning. All 25 fonts are embedded/subset. Five math subsets without Unicode maps render correctly; no replacement characters occur. PDF links resolve internally.

Existing bundled Tectonic **0.17.0** clean temporary build using `--untrusted --only-cached --keep-logs --keep-intermediates` exits 0, with standard-library SSL trust paths and no runtime install/network fetch. Rebuilt SHA256 `d4afecb9b2c9d3abc916b0b9e4835a9998d5a325ef693affd08adffd4fb9eb3a`. Every one of the 11 page rasters, page texts and content streams matches v3; whole layout text matches. Metadata differs only in CreationDate.

All three isolated standard-library Python certificates exit 0, covering only algebra. All 42 displayed mathematical blocks and certificate scripts remain byte-identical from v2 to v3. This mechanical comparison does not approve any mathematical premise or inherited dependency.

Independent archive audit passes **35 frozen-package checks** plus **16 reference checks**: 32 packet files including inventory, 31 inventory entries, 27 source/ZIP files, 26 payload hashes. Every checksum/size/CRC/byte/whitelist check passes; all 128 document reference occurrences are classified. No broken current supplied-file promise, third-party source/PDF corpus/cache tree, unsafe ZIP entry or credential-pattern hit was found. Pattern inspection does not exclude every possible secret encoding.

Metadata remains consistent: sole author Alec Kriebel, linked visible ORCID 0009-0001-9320-500X, no affiliation/coauthor, October 6, 2026, CC BY 4.0/open access. The new original continuation attribution is in section 6 and reference [5]; its source receipt explicitly covers publisher metadata/abstract only, without revalidating the original theorem/proof or adding an analytic dependency. AI-use, no-human-peer-review and failed-formal-build disclosures remain clear. No existing own DOI/Zenodo record is claimed.

## Pages actually inspected

- **Page 1:** Title, sole author/ORCID/date, revised abstract, section 1, normalization/system (1.1)-(1.2), and beginning of Theorem 1.1/data (1.3).
- **Page 2:** Theorem continuation, field regularity explanation, upstream attribution/equal-ratio reduction, recent literature citation now [7], section 2, flow (2.1) and energy (2.2).
- **Page 3:** Energy/flux, budgets (2.3), separate label spaces, source-receiver geometry/measure/kernel/coefficient (3.1)-(3.4).
- **Page 4:** Complete pair force, Lemma 3.1/cancellation (3.5), proof identities/residuals (3.6), section 4 cap and definitions.
- **Page 5:** Joint bootstrap and occupation displays (4.1)-(4.5), bin definitions and exceptional cases.
- **Page 6:** Subsection 4.1/direct majorants (4.6), near/far estimates, baseline (4.7), receiver majorant (4.8), projector/cutoff/integration-by-parts paragraph.
- **Page 7:** Subsection 4.2/direction count, selection/window/safety displays (4.9)-(4.13) and exponent comparisons.
- **Page 8:** Exponent contradiction, weighted impulse (4.14), closure/doubling, section 6 opening with new original Glassey-Strauss attribution citation [5].
- **Page 9:** Section 6 continuation/local theory, Coulomb transform, potential/localization, vacuum argument, uniqueness and proof conclusion.
- **Page 10:** Section 7 boundary cases and limitations/disclosures; references [1]-[6], including new original Glassey-Strauss1986 reference [5].
- **Page 11:** Only reference [7] Mattingly-Pankavich-Ben-Artzi appears, three lines plus page footer; legible but nearly blank final page.

## Advisory scope and remaining gaps

Three historical-navigation advisories remain: excluded formal local reproduction/config/log artifacts referenced in qualified historical wording; optional priority receipts without a project repository link; incomplete supplied PDF/API digest coverage compared with a broad archive note. Exact source locations are in the independent reference receipt under `package_audit/reference_check/`. These do not break current supplied-file promises. Mutable upload binding is version-specific and now superseded for v3.

This receipt gives **no full mathematical, priority/novelty, formal/Lean, conventional-human-peer-review or publication approval**. No source change, Git, upload, tracker mutation or external individual communication occurred. V3 inputs and v1/v2 QA receipts remained unchanged.

Evidence: `QA_RECEIPT.json`, `MANUAL_VISUAL_REVIEW.json`, build and certificate logs, `pdf_reproduction_comparison.json`, `source_pdf_integrity.json`, `v2_v3_mechanical_comparison.json`, reusable `run_source_pdf_checks.py`, and independent archive/reference receipts/scripts in `package_audit/`. All11 inspected page renders remain in `visual_evidence/`; temporary duplicated builds/renders were cleaned. `QA_ARTIFACT_SHA256.json` hashes retained receipts and evidence.
