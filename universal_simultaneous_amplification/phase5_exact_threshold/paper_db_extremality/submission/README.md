# Submission handoff for Paper I

> **DRAFT — NOT SUBMITTED OR SENT.** These materials prepare a human-led
> submission. No portal has been opened, no declaration has been accepted on
> the author's behalf, and no editor, reviewer, or specialist has been
> contacted.

The intended sequence is:

1. bioRxiv, **Evolutionary Biology**, article type **New Results**;
2. *Journal of Mathematical Biology*, as an original research article; and
3. *Theoretical Population Biology* if the first journal declines the paper.

The files in this directory are:

- `BIORXIV_METADATA.md` and `BIORXIV_CHECKLIST.md`: portal-ready metadata and
  human sign-off gates for the preprint;
- `JMB_COVER_LETTER.md` and `JMB_CHECKLIST.md`: primary-journal materials;
- `TPB_COVER_LETTER.md`, `TPB_HIGHLIGHTS.txt`, and `TPB_CHECKLIST.md`:
  fallback-journal materials;
- `DECLARATIONS.md`: one consistent source for funding, interests, ethics,
  authorship, availability, and AI-assistance statements;
- `PROVENANCE_AND_RELATED_RELEASES.md`: precise disclosure of earlier public
  software snapshots and the boundary between Papers I and II;
- `EXTERNAL_COMMUNICATION_BOUNDARY.md`: records the independent-research
  communication constraint; and
- `BUNDLE_REPRODUCTION.md` and `bootstrap_replay.sh`: clean-extraction replay
  instructions for the source-and-certificate archive; and
- `ENVIRONMENT.md`: exact interpreter, library, and PDF-toolchain versions;
  and
- `REPRODUCTION_TEST.md`: the clean-extraction and pinned-environment test
  record; and
- `verify_submission_materials.py`: static checks for identity, abstract
  length, highlights, placeholders, and software-archive provenance.

Only one field is intentionally unresolved:

- `[[POSTAL_ADDRESS]]`

It is a stable placeholder for private human metadata and must be replaced by
the author in a private portal entry or private cover-letter copy. The public
source-and-certificate archive deliberately excludes venue metadata, cover
letters, and checklists so that replacing this field cannot publish a postal
address accidentally. No theorem, publication-status, funding,
competing-interest, or release identifier is represented by a placeholder.

## Requirements checked

The *Journal of Mathematical Biology* instructions were checked on
2026-08-20 at
<https://link.springer.com/journal/285/submission-guidelines>. They request
editable LaTeX sources and a PDF, a 150--250-word abstract, four to six
keywords, MSC codes, corresponding-author details, and statements and
declarations. The bioRxiv screening description and Evolutionary Biology
category were checked at
<https://connect.biorxiv.org/news/2022/06/13/screening_procedures> and
<https://connect.biorxiv.org/relate/content/181/channel/175>.

Elsevier's current journal guide should be reopened directly from the
*Theoretical Population Biology* journal page immediately before submission.
The fallback package follows Elsevier's standard highlights format of three
to five bullets, each no longer than 85 characters, and deliberately labels
all portal-dependent choices for human rechecking.

Live rules and portal fields can change. The human author must compare these
materials with each live portal immediately before use.
