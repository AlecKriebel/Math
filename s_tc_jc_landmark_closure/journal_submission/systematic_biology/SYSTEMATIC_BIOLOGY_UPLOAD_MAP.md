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

1. Deposit `stc_jc_sharp_boundary_atlas_certificates_v1.1.6.tar.gz`, its
   checksum and envelope in Zenodo; insert the issued DOI in the manuscript
   and metadata.
2. Rebuild this directory and verify `SHA256SUMS`.
3. Read the complete manuscript, supplement, cover letter, and metadata.
4. Confirm that the manuscript is not simultaneously under consideration.

Run the exact local package checks from the project root:

```bash
(cd journal_submission/systematic_biology && shasum -a 256 -c SHA256SUMS)
python reproducibility/verify_submission_source_archives.py
python reproducibility/verify_certificate_zenodo_release.py /path/to/downloaded/archive.tar.gz
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
5. Do **not** upload `SB_Exact_Verifier_Entry_Points.zip` to ScholarOne. The
   current journal instructions direct scripts and code to Zenodo rather than
   the manuscript system.  Include this small capsule in the repository
   deposit together with the curated certificate archive, and provide the
   issued reviewer link or DOI in ScholarOne only after it exists.
6. Upload `SB_Cover_Letter.pdf` as the cover letter.
7. Do not upload `SB_LaTeX_Source.zip` for initial review unless ScholarOne
   explicitly requests it; retain it for acceptance.
8. Enter the title, abstract, author, ORCID, keywords, funding, conflicts, and
   AI disclosure from `SB_SUBMISSION_METADATA.md`.
9. Enter the Zenodo DOI for code/scripts if one has actually issued.  This study uses no empirical
   sequence dataset.  If ScholarOne requires a Dryad reviewer URL despite
   that fact, follow the portal's current instruction before submitting.
10. Supply each figure's alt text from the text printed directly below its
   legend in the review PDF if the portal also provides an alt-text field.
11. Review the ScholarOne-generated PDF and verify equations, figures,
    references, supplement linkage, line numbers, and hyperlinks.
12. Stop before the final submission control until Alec Kriebel has completed
    `FINAL_HUMAN_CHECKLIST.md`.

## After acceptance

Upload `SB_LaTeX_Source.zip` plus any separately requested vector figure
files.  Replace reviewer-only repository links with permanent identifiers.
