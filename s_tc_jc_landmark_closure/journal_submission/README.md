# Journal submission packages

These packages are generated from the same canonical article and supplement
used for bioRxiv.  Run:

```bash
python s_tc_jc_landmark_closure/reproducibility/build_biorxiv_release.py submission
python s_tc_jc_landmark_closure/reproducibility/build_journal_packages.py
python s_tc_jc_landmark_closure/reproducibility/verify_submission_source_archives.py
```

The final command independently extracts each source ZIP, follows the
archive-local instructions, and compares all six article/supplement PDFs and
both cover letters byte for byte with the corresponding upload files.

- `systematic_biology/` is the primary journal package.  Its review PDF uses
  12-point type, one-and-a-half spacing, continuous line numbering, one-inch
  margins, ragged-right text, running heads, and figure alt text.
- `journal_of_mathematical_biology/` is the fallback package.  It includes a
  complete editable LaTeX ZIP, PDF, supplement, declarations, and MSC codes.

The upload maps record portal-specific human actions.  They do not authorize
submission, select a license, invent a persistent identifier, or claim that
the manuscript has undergone external human specialist review.
