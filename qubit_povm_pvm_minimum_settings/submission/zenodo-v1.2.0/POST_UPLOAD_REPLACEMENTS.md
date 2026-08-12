# Finite post-reservation, pre-publication replacement checklist

Record the five actual Zenodo-generated version DOIs:

- Paper PDF: `[NEW VERSION-SPECIFIC PAPER DOI]` / manuscript token
  `[ZENODO V1.2.0 VERSION-SPECIFIC DOI — INSERT AFTER UPLOAD]`
- Line-numbered PDF: `[NEW VERSION-SPECIFIC REVIEW DOI]`
- LaTeX source archive: `[NEW VERSION-SPECIFIC SOURCE DOI]`
- Integrity manifest: `[NEW VERSION-SPECIFIC CHECKSUM DOI]`
- Software archive: `[NEW VERSION-SPECIFIC SOFTWARE DOI]` / manuscript token
  `[ZENODO V1.2.0 SOFTWARE DOI — INSERT AFTER UPLOAD]`

Before publishing any draft, replace matching tokens and superseded public-
version links in:

- `CITATION.cff` (make the new paper version DOI the cited DOI, retain the
  concept DOI as an additional stable relation where useful, and add the
  actual release date);
- `submission/zenodo-v1.2.0/metadata/SOFTWARE_ARCHIVE_CITATION.cff` (make the
  new immutable software version DOI its cited DOI, retain the concept DOI as
  an additional relation where useful, and add the actual release date);
- `README.md`;
- `paper/main.tex` and `paper/references.bib` (the journal-facing v1.2.0 paper
  must cite its current version-specific paper and software records; retain
  the July 30 version DOI only in the chronology sentence/reference);
- `submission/pra-v1.2.0/cover_letter.md`;
- `submission/pra-v1.2.0/submission_form_dossier.md`;
- `submission/pra-v1.2.0/data_availability_statement.md`;
- `submission/pra-v1.2.0/supplement/supplement.tex`;
- `submission/pra-v1.2.0/supplemental_material_README.txt` if its status
  wording is affected;
- `submission/zcw_notification_email.md`;
- `submission/website-v1.2.0-draft/index.html`;
- `review_packet/theorem_summary.md` and
  `review_packet/theorem_to_artifact_map.md` where current-record links appear;
- `reports/version_history.md`, `reports/final_readiness_v1.2.0.md`, and
  `reports/readiness_report.md` (replace “prepared/not deposited” status with
  the exact freeze-time state);
- `CHANGELOG.md` and `submission/zenodo-v1.2.0/VERSION_NOTE.md` wherever their
  status wording must reflect the reserved DOI drafts or actual release date;
- all five metadata sheets and cross-links;
- release notes and repository tag/release description.

Search the entire project for `ZENODO V1.2.0`, `NEW VERSION`, `NEW_VERSION`,
`TO_BE_INSERTED`, `TO BE INSERTED`, `NEW_PUBLICATION_PDF_SHA256`, and the
release-tag token. No such token may remain in an externally submitted or
deployed file.

After replacement, rebuild both paper PDFs, the supplement and theorem
comparison, all source/software/verifier archives, the website PDF copies,
and every new release manifest. Rerun the exact verifier and recheck every
link and uploaded-file checksum. Do not alter the frozen 1.1.0 directory.
