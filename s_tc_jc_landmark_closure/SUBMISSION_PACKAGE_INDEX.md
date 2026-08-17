# Submission package index

Release: `stc-jc-sharp-boundary-v1.1.3`

All three packages derive from the same canonical article and supplement. The
SHA-256 manifest in each directory covers every delivered file, including
repository-deposit or acceptance-stage support files that the corresponding
upload map says not to send through the initial manuscript portal.
From the monorepository root, the exact package gate is:

```bash
python s_tc_jc_landmark_closure/reviews/v1_1_3_englander_revision/verify_englander_revision.py
python s_tc_jc_landmark_closure/reproducibility/verify_submission_source_archives.py
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

The eight public assets and their publication command are listed in:

- `release/PUBLIC_RELEASE_ASSETS.md`
- `release/UPLOAD_RELEASE_ASSETS.md`

After those eight assets are public, run:

```bash
python s_tc_jc_landmark_closure/reproducibility/verify_public_release.py
```

Only its `PUBLIC_RELEASE_VERIFIED` result closes the external provenance gate.

The active source tag and public release envelope replace the superseded
18-page replay record stored under `history/superseded_release_evidence/`.

No command in this repository submits a manuscript, selects a license, or
contacts an editor.  Those actions remain exclusively with the human author.
