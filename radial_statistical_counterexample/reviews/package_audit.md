# Final package audit

Checkpoint: **2026-09-23 03:46 UTC**. Completion estimate: **100% of this
bounded package-integrity and reproduction audit**.

**Verdict: PASS.** No release-blocking package defect remains in the reviewed
materials. One provenance wording issue found during the audit was corrected
and its propagation into the source archive, upload kit, and site was checked.
This verdict does not certify historical priority, a successful remote
deployment, or acceptance of metadata by Zenodo.

## Metadata and claims

The manuscript, `CITATION.cff`, both Zenodo JSON files, `UPLOAD.md`, README,
and site agree on the title, Alec Kriebel's name, ORCID
`0009-0001-9320-500X`, version `1.0.0`, and manuscript date
`2026-09-22`. The PDF contains four pages, agreeing with the descriptions.
The date is explicitly the manuscript's local date, not the next-day UTC
audit timestamp.

The API-form JSON is exactly the metadata object wrapped under `metadata`.
The prepared record is described as a preprint with open access and CC BY
4.0 for text; the separate MIT code license is present and disclosed. The
JSON does not contain an assigned DOI or a reserved DOI. The two DOI-valued
related identifiers are cited prior publications, not identifiers claimed
for this result. The guide correctly directs the user to upload a readable
PDF and the source archive and makes clear that no deposit has been created.
These are prepared metadata, not a server-validated submission.

The site, abstract, metadata, and guide describe a negative answer to the
printed implication and retain the limits of the priority search. They do
not convert the exact tensor computations into a claim of formal proof of
the analytic all-centres theorem, external human peer review, or guaranteed
historical priority.

The initial site/metadata wording attributed the supplied candidate itself
to Codex, although the record establishes only that it was AI-generated.
It now says the candidate was supplied as AI-generated work and attributes
the manuscript, verification, and audit preparation to Codex. This matches
the manuscript's disclosure; the corrected text was rechecked after a
package rebuild.

## Archive and checksum checks

The source ZIP has safe relative paths below one named top-level directory,
no duplicate members, valid ZIP checksums, and an internal SHA-256 manifest
whose entries all verify. At the initial checkpoint, every archived byte
also matched its corresponding source file. No unrelated gradient-path
scripts, cached environments, compiled Python files, TeX transient files,
downloaded third-party source PDFs, or old archives are included. References
to the unrelated filenames in explanatory notes are not input evidence.

The outer Zenodo kit has exactly these seven members:

```text
files/paper.pdf
files/source-and-verification.zip
files/SHA256SUMS.txt
UPLOAD.md
metadata.json
metadata-for-api.json
LICENSES.md
```

Both payload checksums verify. The nested PDF and source archive match the
canonical output files, and the guide/metadata match their prepared sources.
The site manifest also verifies every listed asset. Its PDF, source archive,
upload kit, HTML, and styles agree with the corresponding build outputs.
After the provenance correction, all three checksum layers and the
corrected archived text were checked again successfully.

## Clean extraction and script inspection

The source ZIP was extracted into a fresh temporary directory. With Python
3.9.6 and SymPy 1.14.0 already available in the interpreter, both
`verify_exact.py` and `verify_symbolic.py` ran successfully from that
extraction, once normally and once with `-O`. All four executions had empty
standard error, exited successfully, and produced output identical to the
included expected transcripts.

The quick check confirms ranks `(9,10)`, `(16,17)`, and `(25,26)` in
dimensions three, four, and five. Its exact `Fraction` row reduction,
coefficient indexing, compatible controls, dimension-two boundary, and
Ricci/Weyl checks are consistent with its stated pointwise scope. The
symbolic checker passes 403 exact checks and derives the tensors from the
coordinate metric. Failure checks in both scripts remain active with
optimization. No new script discrepancy was found.

## Packaging reproducibility and final-build scope

The extracted copy of `build_package.py` was executed twice, entirely in
the temporary directory. Both generated ZIPs were byte-identical to the
reviewed originals and to the repeated rebuild. Inspection confirms an
explicit source-file allowlist, sorted member order, fixed member timestamps
and permissions, and no upload operation. The optional deployment action
only copies finished local assets into the original repository's Pages
directory. Nothing in this audit used that action or performed git work.

Determinism here means **fixed input bytes and the tested runtime**. It does
not mean separate LaTeX compilations must have identical PDF metadata, or
that ZIP output is guaranteed identical across all compression-library
versions. The existing PDF is an input to the package builder.

The final release build will add this audit and the final research/delivery
notes, so its archive hashes will appropriately differ. No transient ZIP
hash is recorded here as a canonical permanent identifier. That final build
must regenerate the manifests and site downloads from the final sources;
its generated manifests are the checksum authority for those exact bytes.

**Remaining blockers:** none found within this audit's scope. The bounded
priority caveat and lack of a created Zenodo record remain disclosed
publication-status limits, not concealed package defects.
