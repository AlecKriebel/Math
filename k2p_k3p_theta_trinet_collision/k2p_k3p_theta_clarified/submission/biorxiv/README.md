# bioRxiv submission packet

This directory is an author-facing staging packet, not material to upload as a
supplement. `submission/build_release.sh` excludes the whole directory from its
generated archives.

Use the files in this order:

1. `OFFICIAL_REQUIREMENTS.md` records the official bioRxiv guidance checked on
   23 August 2026.
2. `UPLOAD_METADATA.md` is the reusable metadata worksheet. Resolve every
   angle-bracket placeholder after the manuscript is frozen.
3. `FINAL_CHECKLIST.md` is the final pre-approval gate.
4. `zenodo.template.json` is a `.zenodo.json`-style metadata-object template for
   a separate permanent reproducibility-package deposit. It is intentionally
   invalid for use until its double-underscore placeholders are replaced or
   the inapplicable fields are removed. A direct Zenodo deposition API request
   wraps this object under its top-level `metadata` field.

The manuscript to upload is `../../combined-paper-clarified.pdf`, release
version `1.2.2` under tag `k2p-k3p-theta-v1.2.2`. The current
paper title, abstract, author list, theorem statements, and PDF are authoritative;
duplicated metadata must be checked against them immediately before approval.

No bioRxiv distribution license has been selected here. That is a consequential
author choice in the upload system, and a posted preprint becomes a permanent,
citable part of the scholarly record.
