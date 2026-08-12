# Physical Review A / APS policy audit

**Checked against official APS pages:** 12 August 2026

## Submission choice

- Journal: Physical Review A
- Article type: Regular Article
- Suggested section: A-1E, Fundamental Concepts; A-2E, Quantum Information
  Science, is a plausible secondary classification.
- Regular Articles have no Letter-style length limit. APS can begin review
  from a PDF, and REVTeX is the preferred source format. The package now uses
  the official REVTeX 4.2f runtime in a stable one-column 11-point build.

## Required statements

- A Data Availability Statement is mandatory. The paper now states that no
  empirical data were generated and cites the public paper/software records.
- The exact software and mathematical data are archived on Zenodo.
- Substantive generative-AI use must be disclosed where research methods are
  discussed and in the manuscript acknowledgment/disclosure material. AI
  systems cannot be authors. The revised paper names recorded systems,
  explains their roles and verification limits, and assigns responsibility to
  the human author.
- Preprints are allowed. The cover letter discloses the public Zenodo preprint
  and confirms that the manuscript is not under journal consideration
  elsewhere.

## Supplemental Material

Supplemental Material is optional and cannot carry a load-bearing proof. The
prepared supplement contains coefficient tables, verification instructions,
the theorem-to-artifact map, certificate scope, and hashes. All universal
mathematics remains in the main paper. Code is primarily referenced through
the stable Zenodo software archive.

## Formatting decision

The canonical mathematical body is shared by the archival, line-numbered,
and PRA builds. The PRA wrapper uses the official REVTeX 4.2f runtime with the
`aps,pra,onecolumn,11pt,notitlepage` options and conventional author metadata. A two-column
prototype was rejected after it produced extensive overfull displays and
stuck floats in load-bearing equations and appendices; the submitted
one-column form is APS-compatible and materially safer to audit. The package
includes both the PRA PDF and a preservation-friendly source archive.

## Official sources

- PRA scope: <https://journals.aps.org/pra/about>
- Section selection: <https://journals.aps.org/pra/authors/guidelines-section-selection-physical-review-a>
- PRA author guidance: <https://journals.aps.org/pra/authors>
- APS web submission: <https://journals.aps.org/authors/web-submission-guidelines-physical-review>
- Data availability: <https://journals.aps.org/authors/data-availability-statements>
- AI tools: <https://journals.aps.org/authors/appropriate-use-ai-tools>
- Supplemental Material: <https://journals.aps.org/authors/supplemental-material-instructions>
- Editorial policies: <https://journals.aps.org/authors/editorial-policies>
- REVTeX: <https://journals.aps.org/revtex>

Policies can change. The author should recheck the portal immediately before
submission, especially section names, file limits, and referee fields.
