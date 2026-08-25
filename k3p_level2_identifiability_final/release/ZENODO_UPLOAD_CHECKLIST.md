# Zenodo upload checklist

- Confirm quick, full, full-regeneration, source-reproduction, clean-clone,
  archive, mutation, manuscript, and visual-PDF gates all pass.
- Confirm the source commit and exact immutable tag agree with
  `RELEASE_ENVELOPE.json`.
- Upload the full reproducibility archive, its sidecar checksum, article PDF,
  supplement PDF, compact verifier ZIP, source archives, and release envelope.
- Enter Alec Kriebel's ORCID `0009-0001-9320-500X` exactly.
- Choose a license only after Alec explicitly authorizes it.  No license is
  inferred by this package.
- Mint the DOI in Zenodo; do not enter a placeholder or predicted DOI.
- Record the issued DOI, then follow `POST_DOI_REBUILD.md`.
- Verify the final Zenodo landing-page file hashes against
  `RELEASE_ASSET_SHA256SUMS` before publication.
