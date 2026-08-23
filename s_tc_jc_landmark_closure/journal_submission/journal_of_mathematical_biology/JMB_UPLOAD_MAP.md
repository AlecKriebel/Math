# Journal of Mathematical Biology upload map

Verified on 2026-08-16 against:

- https://link.springer.com/journal/285/submission-guidelines

The current instructions require editable source files at every submission,
recommend LaTeX, request a 150–250 word abstract, 4–6 keywords, MSC codes,
`Statements and Declarations`, a data-availability statement, and disclosure
of substantive LLM use in the manuscript.

## Portal warning

On 2026-08-16, the Editorial Manager URL reached from the official journal
page displayed a site-under-development warning.  Therefore do **not** rely on
a hard-coded portal URL in this package.  On the submission day, begin from
the official journal page above and use its live **Submit manuscript** link.

Before opening that link, run from the project root:

```bash
(cd journal_submission/journal_of_mathematical_biology && shasum -a 256 -c SHA256SUMS)
python reproducibility/verify_submission_source_archives.py
python reproducibility/verify_certificate_zenodo_release.py /path/to/downloaded/archive.tar.gz
```

These commands check the exact portal set, reproducible article/supplement and
cover-letter builds, and the public DOI-bearing curated certificate archive,
its canonical envelope, and its committed verifier logs.

## Upload sequence

1. Recheck the official guidelines and live submission link.
2. Upload `JMB_Main_Manuscript.pdf` as the manuscript PDF.
3. Upload `JMB_LaTeX_Source.zip` as the complete editable LaTeX source.  It
   includes the article, bibliography, TikZ figures, supplement source, and
   build instructions.
4. Upload `JMB_Supplementary_Information.pdf` as **Online Resource 1**. Its
   title block identifies the article, journal, author, affiliation, and
   corresponding email; the JMB manuscript cites Online Resource 1.
5. Do not designate `JMB_Exact_Verifier_Entry_Points.zip` as a second Online
   Resource.  Retain it in the local support package and include it in the
   external repository deposit.  The manuscript cites Online Resource 1; the
   curated atlas-certificate archive and verifier capsule are reached through
   its data/code statement.
6. Upload `JMB_Cover_Letter.pdf` if the portal requests a cover letter.
7. Enter the metadata from `JMB_SUBMISSION_METADATA.md`.
8. Provide the author’s city and country if the current title-page/portal
   fields require them; this package intentionally does not invent them.
9. Insert the real public repository or persistent archive identifier.  Do
   not enter an unissued DOI.
10. Confirm the funding, competing-interest, data/code, contribution, and AI
   declarations.
11. Inspect the portal-generated proof, especially formulas, TikZ figures,
    references, supplement linkage, and author information.
12. Stop before final submission until `FINAL_HUMAN_CHECKLIST.md` is complete.

If Systematic Biology rejects the manuscript, revise the cover letter to
reflect that history only when the portal asks; do not include confidential
review material unless explicitly authorized and appropriate.
