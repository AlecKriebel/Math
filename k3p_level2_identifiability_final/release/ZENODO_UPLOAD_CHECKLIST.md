# Zenodo upload checklist

- Confirm the exact historical full-regeneration evidence still binds every
  unchanged mathematical producer.  Rerun only the dependency-scoped quick,
  archive, source-reproduction, referee-integrity, manuscript, and visual-PDF
  gates affected by the public-release edits.
- Confirm the source commit and annotated tag
  `k3p-level2-identifiability-v1.0.0` agree with the public Zenodo manifest.
- Push that annotated tag and require
  `release/zenodo/verify_zenodo_upload_set.py --require-remote-tag` to pass;
  its peeled remote commit must equal the manifest commit.
- Upload every file, and only the files, in the generated
  `release/dist/zenodo_v1.0.0/UPLOAD_THESE_FILES/` directory.
- Enter Alec Kriebel's ORCID `0009-0001-9320-500X` exactly.
- Use Publication--Preprint, version 1.0.0, public/open access, and the
  author-approved CC BY 4.0/MIT file-level license mapping in `LICENSES.md`.
- Let Zenodo assign the DOI at publication; do not enter a placeholder or
  predicted DOI.
- Before publication, compare exact filenames and byte sizes with the metadata
  guide, confirm that the stated date is the actual Zenodo publication date,
  and select the article PDF as the default preview.  Zenodo commonly displays
  MD5; use `SHA256SUMS` for the post-download SHA-256 check.
- After publication, download every landing-page file, verify it against
  `SHA256SUMS`, and record the issued DOI.  Do not rebuild version 1.0.0 solely
  to embed that DOI.
