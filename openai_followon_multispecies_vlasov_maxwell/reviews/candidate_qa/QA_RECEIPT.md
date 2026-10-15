# Candidate package QA receipt

Review completed: 2026-10-07T04:36:51.199888+00:00. QA completion estimate: **100%**. Candidate remains **NOT PUBLISHED**.

**Result:** PASS for this scoped package, presentation, and reproducibility audit. No PDF/source mismatch or package integrity blocker found. Two nonblocking advisories are recorded below.

## Exact reviewed versions

| Input | SHA256 |
| --- | --- |
| `upload-kit/paper.pdf` | `91b45e243369d62a95d609f901adfe550659b27463136dd973124ff7aeeadc8a` |
| `upload-kit/source-and-verification.zip` | `bd8604219a0d2c147021f31d6c8737af4cb0298dc3a0d076ce73d1cbed7ce1da` |
| `source-and-verification/main.tex` | `64e2f3f4d7972274b29a77d7980bc9255d38d86879eff5fc2143dcb5ba9b8696` |
| `zenodo-deposit.json` | `db57320f7afa483e9940b8ce1e3c419e50003719784007f261712bdcb6330fa3` |

## Visual/source/build checks

All **10 pages (1-10)** were individually inspected from 110 dpi PNG renders. All equations, prose, headings, footer page numbers, candidate warnings, and five references are legible. No clipping, overlap, broken glyphs, formula/number collision, or unresolved reference/citation was seen. Page-spanning paragraphs and section transitions were checked, including section 6 on pages 8-9 and section 7 on pages 9-10.

The PDF is 10 A4 pages, 127826 bytes, with all 25 fonts embedded and subset. Five math symbol/extension font subsets lack Unicode maps, but their mathematical glyphs render correctly; extraction contains no replacement characters. The PDF has no forms or JavaScript, is unencrypted, and is not accessibility tagged.

The source has 28 unique labels and 5 cited bibliography keys; none are missing or unresolved. The final TeX log has zero overfull/underfull box warnings and zero LaTeX/hyperref warnings. All 48 PDF link annotations were checked; internal destinations resolve. External bibliography URLs were checked against source, not independently fetched for validity in this QA.

The existing bundled Tectonic **0.17.0** compiled a fresh temporary copy of main.tex with `--untrusted --only-cached --keep-logs --keep-intermediates`. The compilation exited 0 without installing a runtime or fetching TeX resources. Standard-library `ssl.get_default_verify_paths()` was used for trust paths. The rebuilt PDF has SHA256 `a823da16f271fbab9d4ef612154a4499f394b23c34c1d86fcea11f0b9e8b9300`. Every page content stream, extracted page text, whole layout text, and 110 dpi image matches the reviewed candidate exactly. The PDF byte hash differs because the build timestamp differs; metadata differs only in CreationDate.

Single author **Alec Kriebel**, ORCID **0009-0001-9320-500X**, no coauthors or affiliations; visible date October 6, 2026. PDF/source and intended deposit author/title/date/license/candidate disclosure are consistent. Hyphen/en-dash typography in Vlasov-Maxwell is a semantic title match.

## Pages actually inspected

- **Page 1:** Title, single author, ORCID, October 6 date, prominent candidate warning, abstract, normalization (1.1) and transport/Maxwell system (1.2) inspected.
- **Page 2:** Candidate Theorem 1.1 and data (1.3), attribution paragraph, section 2, characteristic equations (2.1), energy (2.2), and unnumbered flux formula inspected.
- **Page 3:** Budgets (2.3), disjoint-label paragraph, section 3, geometry (3.1), measure (3.2), signed source kernel (3.3), coefficient (3.4), and complete pair force inspected.
- **Page 4:** Universal pair Lemma 3.1, cancellation identity (3.5), proof formulas, residuals (3.6), section 4, and simultaneous bootstrap (4.1) inspected.
- **Page 5:** Hit measure (4.2), stable-cell scale (4.3), occupation (4.4), refined occupation (4.5), subsection 4.1 and majorants (4.6) inspected.
- **Page 6:** Near/far majorants, absolute/baseline estimate (4.7), receiver majorant (4.8), integration-by-parts discussion, and start of subsection 4.2 inspected.
- **Page 7:** Direction-count inequality, window (4.9), improved occupation (4.10), selected condition (4.11), coefficient (4.12), safety (4.13), and contradiction exponent bounds inspected.
- **Page 8:** Weighted impulse (4.14), section 5 closure and doubling formulas, and start of section 6 inspected.
- **Page 9:** Section 6 continuation/localization, Coulomb transform, potential formula, uniqueness, and section 7 opening inspected.
- **Page 10:** Remaining limitations and AI/non-peer-review/candidate disclosures; all five bibliography entries and URLs inspected.

## Reproducibility and archive checks

All three distributed Python certificates ran from isolated temporary copies under Python 3.12.14 with `-I` and exited 0. The kernel certificate reports zero universal residuals plus 292 exact rational checks; the selection certificate reports exact rational margins; the independent signed-pair polynomial certificate reports zero residuals. **These checks certify algebra only.** Their force/PDE/analytic premises, priority, and formal theorem scope are not certified.

Independent archive audit: 26 mandatory checks pass. Source and ZIP each contain exactly 20 whitelisted files, with byte equality for every member. All 19 source payload hashes, all 24 inventory size/hash entries, and the full 25-file packet whitelist match. No third-party cache, symlink, traversal path, or secret indicator was found. The original packet remained unchanged throughout QA.

## Nonblocking advisories

1. **Deposit path rebinding:** zenodo-deposit.json references project-root-relative `publication/upload-kit` paths. Those paths currently match candidate bytes but do not directly resolve from package_v1. Recheck authorized, approved hashes at any future staging step.
2. **Auxiliary bibliography catalog:** Bouchut-Golse-Pallard is in main.tex/PDF reference [5] and provenance but absent from references.bib. This does not affect the standalone build; optional catalog consistency edit would require a newly hashed candidate.

## Boundary of approval

This receipt is **not full mathematical or priority approval**. It does not verify the analytic transfer, inherited one-species theorem/dependencies, global PDE theorem, originality, or formal certification. It is not conventional human peer review. No upload, staging, external individual communication, git mutation, or publication was performed.

## Evidence

Machine receipt: `QA_RECEIPT.json`; clean console/TeX logs: `clean_build_console.log`, `clean_build_main.log`; PDF metadata/fonts: `pdfinfo.txt`, `pdffonts.txt`; reproduction and source integrity: `pdf_reproduction_comparison.json`, `source_pdf_integrity.json`; algebra logs and `certificate_receipt.json`; independent archive audit under `package_audit/`; input immutability: `input_preservation.json`. The 10 inspected candidate renders are retained under `visual_evidence/`. Temporary build files, copied certificates, and duplicate rebuilt renders were deleted after retaining logs and hash receipts.
