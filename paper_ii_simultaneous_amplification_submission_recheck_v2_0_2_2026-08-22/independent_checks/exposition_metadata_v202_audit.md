# Independent exposition, metadata, and submission-facing audit (v2.0.2)

## Scope and independence

I audited the frozen package under `delivered_copy/` as a set of claims, without
editing it.  This pass was deliberately limited to submission-facing matters:
the title/abstract/theorem relationship, definitions and cross-references,
bibliography, declarations and availability statements, PDF metadata and
presentation, and reader-facing package instructions.  Mathematical proof and
software correctness are being audited separately.

The audited manuscript is the 21-page PDF
`delivered_copy/simultaneous_amplification_beyond_three_halves.pdf` and its
1,660-line `main.tex`.  All shell commands used in this pass are recorded under
the `agent-v202-exposition-*` labels in the shared command log.  No file in
`delivered_copy/` was changed, no person was contacted, and no file was
uploaded or external state changed.

## Checks performed

- Read the full rendered PDF page by page at high resolution and reviewed the
  corresponding LaTeX, including the title page, abstract, all numbered
  statements, discussion, declarations, and bibliography.
- Recompiled `main.tex` independently with Tectonic 0.16.9.  The compiler log
  contains no overfull/underfull-box, undefined-reference, undefined-citation,
  duplicate-label, missing-file, or other document warning.  The extracted text
  of the independent rebuild is byte-identical to the extracted text of the
  frozen PDF.  (The raw PDF bytes differ because the direct diagnostic command
  did not impose the release builder's deterministic metadata environment.)
- Parsed all LaTeX labels, references, citations, and bibliography keys with an
  independent script.  Results: 49 labels, 64 `ref`/`eqref` uses, 12
  bibliography items, and 12 cited keys; no duplicate labels, undefined
  references, duplicate bibliography keys, undefined citations, or uncited
  bibliography entries.  Some deliberately reusable labels are not referenced
  elsewhere, which is harmless.
- Inspected PDF metadata, fonts, URL annotations, page geometry, and security
  features with Poppler.  All 26 fonts are embedded and subset; the PDF has no
  encryption, form, JavaScript, or suspect object; all expected hyperlinks are
  present.
- Resolved the ten external journal/conference DOIs against publisher or
  official proceedings pages.  Titles, author lists, years, volume/article
  data, and DOI targets agree with the bibliography.  Resolved the two cited
  Kriebel releases and the prior full-repository DOI against Zenodo's record
  metadata; the manuscript correctly distinguishes those earlier releases from
  this superseding revision.
- Compared the manuscript with the current official
  [*Journal of Mathematical Biology* submission instructions](https://link.springer.com/journal/285/submission-guidelines),
  because the bundled research log identifies that journal as the intended
  primary venue.

## Submission-facing claim ledger

### Title, abstract, definition, and theorem

The title, PDF title metadata, package title, abstract, Definition 1, Theorem 3,
discussion, source README, and release notes all state the same result:

- a single graph family is selected independently of fitness;
- for every fixed `1 < r < R_hyb`, both Bd and dB amplification hold for all
  sufficiently large family indices;
- `R_hyb` is the unique sextic root in `(3/2,151/100)` and is reported
  consistently as `1.5028569127905696...`;
- optimality is restricted to fixed positive response parameters in the stated
  first-order dilute pair--pendant model; and
- no unrestricted value or finite universal upper bound for `R_sim` is claimed.

The abstract does not overstate the theorem or the computational evidence.  It
contains about 222 words, within the target journal's 150--250-word range.  Bd,
dB, `R_sim`, and `R_hyb` are defined before use.  The six keywords and three MSC
codes are present and appropriate.  The main theorem's quantifier order agrees
with both the displayed quantifier formula in the introduction and Definition
1.

### Numbering and internal references

Sections run consecutively from 1 through 8.  The shared statement counter runs
cleanly from Definition 1 through Corollary 16, and displayed equation numbers
run consecutively through (44).  Figure 1 is legible, has a descriptive caption,
and is introduced in the construction.  No visible `??`, broken citation,
wrong statement number, or dangling equation/section reference appears in the
PDF.  The programmatic cross-reference check agrees with the compiled output.

### Bibliography and citation use

The 12-entry reference list is alphabetized and every entry is used in the
text.  Publisher/official metadata checks found no title, author, year,
volume/article-number, or DOI mismatch.  The introductory claims are supported
by the cited sources at the level asserted: weighted-network behavior,
transient dB amplification, mixed update-order processes, the previous
simultaneous interval, and the two classical Moran/graph references are not
misattributed.  The two self-citations are explicitly described as unrefereed
releases rather than journal articles.  The full-repository Zenodo DOI in the
availability statement is correctly identified as a v1 snapshot, not as the
persistent identifier for v2.0.2.

### Declarations and availability

The manuscript has a single, clearly headed `Statements and Declarations`
section containing:

- Data and code availability, including the exact supplementary archive name,
  replay boundary, bundled-wheel boundary, external document-tool boundary,
  frozen repository tag, and prior-DOI limitation;
- funding;
- competing interests;
- author contributions and responsibility;
- ethics/consent applicability; and
- a substantive AI-use disclosure.

The AI disclosure is unusually candid and is placed in a suitable alternative
part of a paper with no Methods section, satisfying the target journal's rule
that non-copy-editing LLM use be documented and that a human author remain
accountable.  The exact programs are correctly described as finite
transition/algebra audits rather than proof of the analytic asymptotics.

### PDF metadata and visual presentation

The PDF title, author, subject, and keywords agree with the manuscript.  It is a
21-page US-letter document with clean margins and page numbers.  All equations,
tables, the TikZ figure, proof-ending symbols, and hyperlinks render correctly;
there is no clipping, collision, missing glyph, raster degradation, or illegible
text.  The long supplementary filename wraps awkwardly but remains within the
text block and readable.  The declarations' continuation onto page 21 and the
remaining whitespace after the short bibliography are ordinary pagination, not
layout defects.

The displayed PDF creation timestamp is 2026-08-21 17:00 PDT while the title
page says August 22.  This is not stale metadata: it is the local rendering of
the deterministic `SOURCE_DATE_EPOCH=1787356800`, exactly 2026-08-22 00:00 UTC.
All other version/date metadata is v2.0.2/August 22, 2026.  The PDF is untagged
for accessibility and a few mathematical symbol fonts lack Unicode maps; the
document remains visually correct and text extraction is successful.  Neither
condition is a current submission requirement for this mathematical journal.

## Findings by severity

### Submission-procedural item requiring human confirmation

1. **The title page does not give a city and country for the independent
   affiliation.**  `main.tex` lines 36--39 give the author, `Independent
   Researcher`, email, and ORCID, but no location.  The current *Journal of
   Mathematical Biology* instructions ask for affiliations with city/country
   and state that temporarily unaffiliated authors should supply city and
   country of residence.  This is not a scientific, expository, or
   reproducibility defect, and the corresponding-author details may be entered
   in the submission portal.  Nevertheless, it is the one item that can cause
   a technical-check return if the journal requires the location on the PDF
   title page itself.  Only the human author can supply or approve this private
   metadata.  Before clicking submit, either (a) add the approved city/country
   to the title page and refreeze, or (b) confirm that completing the portal
   affiliation field is sufficient.

2. **Portal classification of the supplement should be confirmed.**  The
   journal instructions conventionally call supplementary files `Online
   Resource 1` and request a concise caption and identifying metadata.  The
   manuscript instead calls the tarball a deterministic Supplementary Material
   archive by its exact filename.  The file is in an accepted `.gz` container,
   is specifically mentioned in the manuscript, and contains title/author and
   contact information through its source, so this does not justify reopening
   the scientific freeze.  At upload, label it `Online Resource 1`, paste a
   concise caption, and let the portal rename it if required.  If the technical
   check insists on the phrase `Online Resource 1` in the manuscript, that is a
   minor venue-format edit, not a content correction.

### Low-severity supplementary-documentation issues (not submission-blocking)

1. `vendor/README.md` line 27 refers to
   `submission/ENVIRONMENT.md`, which is not included in the frozen public
   archive.  The reference is genuinely dangling.  It does not hide any needed
   instruction: the same external Tectonic/Poppler/resource-cache boundary is
   stated completely in `README_FIRST.md` lines 75--82, the paper-root
   `README.md` lines 58--62, `VERSION.md`, `BUNDLE_METADATA.txt`, and the
   manuscript availability statement.  A reader can reproduce the stated
   boundary without the absent private file.

2. The paper-root `README.md` lines 3--5 says the folder contains a “human
   submission handoff,” although the public archive intentionally omits private
   venue metadata and cover letters (as `RELEASE_NOTES.md` lines 27--34 makes
   clear).  This is inherited repository wording rather than a missing
   scientific payload.  `README_FIRST.md` accurately describes the delivered
   package's scope and layout.

Changing either wording nit would force new source/PDF/package identities for
no scientific or operational benefit.  They can reasonably remain as disclosed
limitations of v2.0.2 and be cleaned up in a later release.

### No major or scientific findings

I found no inconsistent title or theorem, undefined notation affecting the
claim, broken numbering, erroneous bibliography record, missing declaration,
misstated code boundary, stale version identity, visual defect, or reader-facing
instruction error that prevents mathematical review or use of the supplement.

## Readiness conclusion

**The frozen manuscript and scientific supplement are submission-ready on
content, exposition, citations, declarations, metadata, and visual layout.  No
scientific re-freeze is indicated by this audit.**

For literal portal readiness at the intended *Journal of Mathematical Biology*,
the human author should first resolve the title-page city/country question and
upload/caption the tarball as the portal's first online resource.  If those
administrative fields can be supplied solely in the portal, the existing v2.0.2
bytes can be submitted unchanged.  If the journal requires the location or
`Online Resource 1` wording inside the manuscript itself, only a minor
venue-format revision is needed; it does not affect the theorem, proof, code, or
referee package.
