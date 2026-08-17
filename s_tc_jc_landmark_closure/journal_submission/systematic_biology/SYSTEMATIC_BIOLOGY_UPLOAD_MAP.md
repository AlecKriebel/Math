# Systematic Biology upload map

Verified on 2026-08-16 against the official instructions:

- https://academic.oup.com/sysbio/pages/General_Instructions
- https://mc.manuscriptcentral.com/systbiol

The official instructions classify original theoretical studies as Research
Articles, accept a PDF for a new LaTeX submission, require continuous line
numbers, 12-point type, 1.5 or double spacing, approximately one-inch margins,
ragged-right text, running heads, figure alt text, a data-availability
statement, and disclosure of substantive AI use in both the cover letter and
manuscript.  Full LaTeX sources are requested on acceptance.

## Before opening ScholarOne

1. Deposit `stc_jc_sharp_boundary_reproducibility.tar.gz` and its outer
   release envelope in Zenodo; insert the issued DOI in the manuscript and
   metadata.  Do not fabricate a DOI.
2. Rebuild this directory and verify `SHA256SUMS`.
3. Read the complete manuscript, supplement, cover letter, and metadata.
4. Confirm that the manuscript is not simultaneously under consideration.

Run the exact local package checks from the monorepository root:

```bash
(cd s_tc_jc_landmark_closure/journal_submission/systematic_biology && shasum -a 256 -c SHA256SUMS)
python s_tc_jc_landmark_closure/reproducibility/verify_submission_source_archives.py
python s_tc_jc_landmark_closure/reproducibility/verify_public_release.py
```

The final command is the post-upload release-provenance gate. Run it again
after any release asset is replaced.

## ScholarOne sequence

1. Start **Create a New Submission** at
   https://mc.manuscriptcentral.com/systbiol.
2. Select **Research Article**.
3. Upload `SB_Main_Manuscript.pdf` as the main manuscript.  It already has
   continuous line numbering, 12-point type, 1.5 spacing, running heads,
   ragged-right text, page numbers, embedded figures, and alt text.
4. Upload `SB_Supplementary_Material.pdf` and designate it **Supplementary
   Material**.
5. Upload `SB_Cover_Letter.pdf` as the cover letter.
6. Do not upload `SB_LaTeX_Source.zip` for initial review unless ScholarOne
   explicitly requests it; retain it for acceptance.
7. Enter the title, abstract, author, ORCID, keywords, funding, conflicts, and
   AI disclosure from `SB_SUBMISSION_METADATA.md`.
8. Enter the Zenodo DOI for code/scripts.  This study uses no empirical
   sequence dataset.  If ScholarOne requires a Dryad reviewer URL despite
   that fact, follow the portal's current instruction before submitting.
9. Supply each figure's alt text from the text printed directly below its
   legend in the review PDF if the portal also provides an alt-text field.
10. Review the ScholarOne-generated PDF and verify equations, figures,
    references, supplement linkage, line numbers, and hyperlinks.
11. Stop before the final submission control until Alec Kriebel has completed
    `FINAL_HUMAN_CHECKLIST.md`.

## After acceptance

Upload `SB_LaTeX_Source.zip` plus any separately requested vector figure
files.  Replace reviewer-only repository links with permanent identifiers.
