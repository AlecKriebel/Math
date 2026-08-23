# Submission package index

Release generation: `v1.1.7` (reserved Zenodo DOI
`10.5281/zenodo.22064121`)

All three packages derive from the same canonical article and supplement. The
SHA-256 manifest in each directory covers every delivered file, including
repository-deposit or acceptance-stage support files that the corresponding
upload map says not to send through the initial manuscript portal.
From the project root, the exact package gate is:

```bash
python reproducibility/verify_submission_source_archives.py
```

The second command extracts all three source ZIPs into fresh temporary
directories, executes their documented archive-local commands literally, and
requires byte-for-byte equality with all six packaged article/supplement PDFs
and both cover letters.

## 1. bioRxiv

Directory: `biorxiv_submission/`

- main PDF: `Strong_Tree_Childness_Sharp_Level2_JC.pdf`
- supplement: `Strong_Tree_Childness_Sharp_Level2_JC_supplement.pdf`
- source: `Strong_Tree_Childness_Sharp_Level2_JC_source.zip`
- verifier entry points: `Strong_Tree_Childness_Sharp_Level2_JC_verifier_entrypoints.zip`
- metadata: `BIORXIV_METADATA.md`
- portal steps: `BIORXIV_UPLOAD_MAP.md`
- human gate: `FINAL_HUMAN_CHECKLIST.md`

## 2. Systematic Biology (primary journal)

Directory: `journal_submission/systematic_biology/`

- review-format main PDF: `SB_Main_Manuscript.pdf`
- supplement: `SB_Supplementary_Material.pdf`
- cover letter: `SB_Cover_Letter.pdf`
- acceptance-stage source: `SB_LaTeX_Source.zip`
- repository-deposit verifier entry points (do not upload to ScholarOne): `SB_Exact_Verifier_Entry_Points.zip`
- metadata: `SB_SUBMISSION_METADATA.md`
- ScholarOne steps: `SYSTEMATIC_BIOLOGY_UPLOAD_MAP.md`
- human gate: `FINAL_HUMAN_CHECKLIST.md`

Before journal submission, the exact code/certificate archive must receive a
real Zenodo DOI.  No DOI is invented in this package.

## 3. Journal of Mathematical Biology (fallback)

Directory: `journal_submission/journal_of_mathematical_biology/`

- main PDF: `JMB_Main_Manuscript.pdf`
- supplement: `JMB_Supplementary_Information.pdf`
- complete editable source: `JMB_LaTeX_Source.zip`
- repository-deposit verifier entry points (not an Online Resource): `JMB_Exact_Verifier_Entry_Points.zip`
- cover letter: `JMB_Cover_Letter.pdf`
- metadata: `JMB_SUBMISSION_METADATA.md`
- portal steps: `JMB_UPLOAD_MAP.md`
- human gate: `FINAL_HUMAN_CHECKLIST.md`

The author must add city and country if the current Springer portal requires
them.  The JMB live submission link must be rechecked from the official
journal page because its linked Editorial Manager site was marked under
development during package preparation.

## 4. Exact replay assets

The canonical proof object is
`release_artifacts/stc_jc_sharp_boundary_atlas_certificates_v1.1.7.tar.gz`.
Its checksum, envelope, and three run logs are the primary Zenodo assets. The
broader reproducibility snapshot is secondary. Authenticate a public download
with `reproducibility/verify_certificate_zenodo_release.py`.

No command in this repository submits a manuscript, selects a license, or
contacts an editor.  Those actions remain exclusively with the human author.
