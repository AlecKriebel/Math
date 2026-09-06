# Document and submission review

Target: unchanged commit `6f68ad3e795c239e452206c84ce4ce331386a094`.
Review date: 2026-09-05 America/Los_Angeles (2026-09-06 UTC).

All 94 supplied PDF pages were rasterized using Poppler, inspected in four-page
contact sheets, and compared with the read TeX content. The table defect below
was additionally inspected on a single page at 180 dpi and at enlarged detail.
This is a review of supplied PDFs, not a claim of fresh source-build success.

| Document | Pages | Result |
|---|---:|---|
| `manuscript/main.pdf` | 19 | Legible figures, equations, references, and body layout; no new clipping found. |
| `manuscript/supplement.pdf` | 19 | Certificate fractions have inadequate vertical separation, especially pp. 12–15. |
| `external_audit/theorem_summary.pdf` | 3 | Legible; claims track the theorem suite and its fixed-mass scope. |
| `external_audit/proof_skeleton.pdf` | 6 | Legible; proof map follows the canonical argument, without replacing it. |
| `submission/journal/manuscript.pdf` | 23 | Review margins, numbering, keywords, MSC, figures, and references present. |
| `submission/journal/supplement.pdf` | 23 | Same certificate-row problem, especially pp. 14–19. Contents page points to the observed section starts. |
| `submission/journal/cover_letter_SIADS.pdf` | 1 | Legible draft; explicitly retains author-confirmation placeholder. |

## Required presentation correction: certificate rows

The 77-term and 84-term tables use inline `\frac` in ordinary `longtable`
rows. Adjacent denominators and numerators visibly touch or overprint. For a
precise witness, journal supplement p. 15 begins with coefficients
`160888/91125` and `4420871/182250`. Poppler locates the first denominator at
`y=130.587052..136.744917` points and the next numerator at
`y=135.232052..141.389917` points, with overlapping horizontal intervals.
Their vertical font boxes overlap by 1.512865 points. Enlarged raster
inspection confirms that these adjacent rows touch; this is not merely a
text-extraction false positive.

Source: `data/certificate_tables.tex:50–80` and subsequent fraction-heavy
rows; the row generator is `computation/generate_tables.py:37–49`.
This file is generated, so repair the table generator or a scoped table
style, then regenerate. Add enough row height/spacing, or print rational
coefficients using a legible single-line convention. Do not shrink the type.
Rebuild both canonical and journal supplements to stable auxiliary files,
inspect every table page again, and refresh dependent archives and hashes.
No certificate coefficient or mathematical conclusion needs to change.

`check_table_spacing.py` reproduces the bounding-box witness. Its positive
result describes a defect; it must not be counted as a manuscript validation
pass. General semantic PDF checks do not detect this class of layout error.

## Current SIADS requirements and observed package

The [official SIADS instructions](https://epubs.siam.org/journal/siads/instructions-for-authors),
accessed 2026-09-06 UTC, permit the current alternative review layout. The main
PDF is 23 pages and 621,305 bytes; its source uses 11-point type and a 6-by-8-inch
text area. The supplement uses 10-point type with the same text area. Line
numbers, a single-paragraph abstract, visible keywords and MSC codes, embedded
figures, and a supplementary index with descriptions and justifications are
present. No page/file-size exception is needed for the main article.

The [SIAM AI policy](https://epubs.siam.org/artificial-intelligence), version 2.0,
requires disclosure and author accountability. The manuscript describes the
research uses of AI and includes the single-author responsibility sentence.
This audit is the author's pre-submission research assistance, not an official
SIAM referee report or a substitute for a journal referee's human judgment.

The draft cover letter still needs the author's factual funding,
competing-interest, and exclusivity declarations. Those facts cannot be
inferred from code or prior AI reviews. The portal preview is not available
and was not checked.

## Release link remains a real dependency

`manuscript/main.tex:1250–1258` says the files are already frozen in a v1.0.9
tag. The software auditor's live remote checks find no such tag or release.
The corresponding supplementary-index statement is likewise anticipatory.
The preceding v1.0.8 DOI is explicitly distinguished from the proposed new
version, which is correct, but it cannot identify the corrected v1.0.9 files.

Before upload, use a resolving immutable source reference that actually
contains the corrected package. If a new release is chosen, create it only
after corrections and verification and use the DOI actually assigned, if any.
A new Zenodo DOI is not itself a journal requirement: the essential issue is
accurate, accessible, version-specific evidence. Do not describe an absent tag
as already frozen. No tag or release was created during this referee audit.
