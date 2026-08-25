# Current journal requirements snapshot

Checked against the official publisher pages on 2026-08-25.  This is a
preparation checklist, not a submission record.  No journal, editor,
repository, or other person was contacted.

## Systematic Biology (Oxford University Press)

Official instructions:
<https://academic.oup.com/sysbio/pages/General_Instructions>

- A new LaTeX submission is uploaded as a PDF.  The complete LaTeX package is
  requested upon acceptance; the generated PDF accompanies it.
- The main review manuscript uses continuous line numbers, 12-point type,
  double or 1.5 spacing, approximately one-inch margins, consecutive page
  numbers, and a ragged right margin.
- Online appendices and other non-data/non-code supplementary material are
  separate PDFs and should already be in publishable form.
- Supporting datasets must be deposited in Dryad and supporting code/scripts
  in Zenodo.  During review the manuscript uses the temporary Dryad reviewer
  URL and the Zenodo record/DOI; after acceptance those are replaced with the
  permanent identifiers.  Repository README files explaining every main
  directory and major script are requested.
- A standalone Data Availability section follows the acknowledgments and
  links both data and code.  Public dataset citations belong in the reference
  list.
- Generative-AI use must be disclosed in the cover letter and in Methods or
  Acknowledgments.  AI systems are not authors.
- Funding sources (or absence of funding) and conflicts must be supplied.
- The current public instructions do not state that this journal uses a
  double-anonymous manuscript.  The identified manuscript is therefore the
  required build; an anonymized build may be supplied only if the live portal
  later requests one.

Project consequences:

1. The article uses no empirical biological dataset.  Confirm at release time
   whether the portal classifies any generated proof ledger as a dataset
   requiring Dryad rather than as part of the Zenodo code/certificate record.
2. Prepare the verifier, exact certificates, and source archive as a
   Zenodo-ready bundle with repository README files.
3. Do not invent an identifier.  Rebuild the Data Availability section after
   the human obtains the real reviewer URL or DOI.
4. Prepare one line-numbered, review-spaced PDF and one separate supplement
   PDF.  Keep an editable accepted-version LaTeX package ready.

## Journal of Mathematical Biology (Springer Nature)

Official instructions:
<https://link.springer.com/journal/285/submission-guidelines>

- Complete editable source files are required at every submission and
  revision.  For LaTeX, submit the source (including styles and figures) and
  a compiled PDF; the Springer Nature LaTeX template is recommended.
- The title page includes the author name, affiliation, city/state/country,
  active corresponding email, and ORCID when available.
- The abstract is 150--250 words, followed by four to six keywords and
  appropriate Mathematics Subject Classification codes.
- Decimal section numbering should use no more than three levels.
- A `Statements and Declarations` section must include the relevant competing
  interest and other disclosures.  Every original research article requires
  a Data Availability Statement.
- Textual supplementary information is supplied in PDF form, cited as an
  `Online Resource`, named consecutively (for example, `ESM_1.pdf`), and is
  published without copyediting or reformatting.
- LLM use beyond copyediting must be documented in Methods or another suitable
  section.  LLMs are not authors, and the human author remains accountable.
- The current journal-specific page does not identify this submission as
  double-anonymous.  No anonymized manuscript is required by the published
  instructions; an optional portal-only variant may be retained.

Project consequences:

1. Build a Springer-compatible LaTeX source ZIP and compiled manuscript PDF.
2. Supply the reader supplement as `ESM_1.pdf` with its caption in the article.
3. Include the exact archive citation and a complete Data Availability
   Statement, but do not invent a DOI.

## Human-only decisions and actions

- Confirm the author affiliation and corresponding email shown in the source.
- Choose repository and publication licenses; no license is inferred here.
- Create any required Dryad review deposit and the Zenodo record, then supply
  their real identifiers.  No empirical dataset or Dryad identifier is
  claimed in the draft.
- Choose a journal and perform the actual portal submission.  The same article
  must not be submitted to both journals simultaneously.
