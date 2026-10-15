# Missing faces and topological embeddings of sphere skeleta

Alec Kriebel, Independent researcher.
ORCID: https://orcid.org/0009-0001-9320-500X.
Version 1.0, 12 October 2026.

Unrefereed research note and supporting materials. No independent human peer
review has been obtained. The recorded audits are AI-assisted and bounded.

This note proves the following statement: if a finite simplicial complex
triangulates the topological sphere S^(2d), adjoining a missing d-face on its
actual vertices to its d-skeleton prevents every topological embedding in
S^(2d). It supplies a credited synthesis of established algebraic and embedding
results for d>=3 and explicitly extends the Nevo-Wagner bistellar argument to
the actual PL class in dimension four. It makes no first-priority or new-method
claim. The conjecture's earlier formulation in Nevo's February 2006 preprint
and the prior PL-standard-source theorem are credited.

`manuscript.tex` is the current mathematical source. The PDF is intended to be
deposited alongside this source and verification archive.
`metadata.json` contains the canonical publication metadata, also used
unchanged in the repository's Zenodo upload-kit manifest.
`SHA256SUMS.json`, when generated, binds every selected archive payload file.
The archive excludes private third-party full texts and intentionally invalid
mutation fixtures.

For the supporting finite controls, read `verification/README.md`, then run
from that folder:

    python3 reproduce.py

The driver checks file hashes and reproduces all three current programs in
normal and optimized modes. The finite computations do not prove the universal
theorem or certify priority. Historical frozen inputs and their original
manifests are clearly separated under `verification/historical/`; the current
runtime checks and manuscript incorporate the recorded corrections.

The note and package are unrefereed. No independent human peer review has been
obtained. AI tools were used extensively in solving, drafting, independently
auditing, verifying finite computations, and preparing these materials.
AI-assisted review is neither formal verification nor independent human peer
review. Audit evidence is preserved in the supplement, with exact assignment
boundaries and the limitations of the priority search.

License: CC BY 4.0; see `verification/LICENSE.txt`.
