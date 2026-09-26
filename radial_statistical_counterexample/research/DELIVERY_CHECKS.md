# Delivery checks

> Historical audit snapshot. Version 1.0.1 (26 September 2026) supersedes earlier manuscript/package and access-status statements. See the [current priority statement](PRIORITY_STATUS.md) and the current manuscript; the dated findings below are retained for provenance.

Package checkpoint: 2026-09-23T03:51:05Z. Mathematical verification complete; public-serving check pending when this package snapshot was made.

- The four-page paper source and PDF received a final independent adversarial review; their hashes are in `reviews/final_manuscript_audit.md`.
- The manuscript's 1-conformal definition and original question were read in the publisher PDFs. The priority audit records known ingredients and source-access limits.
- The source and upload archives passed clean-extraction integrity checks and deterministic rebuilds. Both verification scripts passed from the extraction with and without Python optimization.
- Every relative link in the local webpage resolves. The hero, proof, and verification/download sections were visually inspected in the in-app browser. The existing host uses main:/docs with .nojekyll.
- The JSON metadata is syntactically valid. Base fields pass Zenodo's published legacyrecord schema. That old schema omits version/language; those two fields were separately checked against their explicit definitions in the current developer documentation. No server-side Zenodo acceptance is claimed.
- CITATION.cff passes the official CFF 1.2.0 JSON Schema after correcting its top-level type and adding the unpublished paper as preferred-citation.
- No GitHub release, Zenodo deposit, or DOI has been created. No person was contacted.

The initial publication commit is `70fbc44f6cae708bda1840de8269222ee851abdb`. The final metadata/checkpoint commit also regenerates source, upload, and webpage manifests. Generated manifests identify the exact payload bytes without attempting to embed the hash of an archive inside itself. Final HTTP serving is checked after that push; this document records completed local checks, not a prediction of deployment success.
