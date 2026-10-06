# Independent audit of the fourth-order Navier conditional result

Problem 30000801, OWR-1591-003, catalog rank 816.

**Accepted only as a conditional partial result. The full target is unresolved.**

This archive audits the exact author ZIP with SHA-256
`45ab3bf6abaa90e865cba7899a509de3a8343ab44b32bb09dbbad7ccd9f46434`
and size 22,361 bytes. The frozen author files were not changed.

Read `INDEPENDENT_AUDIT.md` for the acceptance decision and reproduction results,
and `MATHEMATICAL_AUDIT.md` for the independently checked argument and limits.
`PUBLIC_SOURCE_VERIFICATION.json` contains public verification metadata only.

Python 3 with SymPy 1.14.0 is required. With the author archive available:

    python independent_verify.py --author-zip /path/to/author.zip
    python -O independent_verify.py --author-zip /path/to/author.zip
    python independent_adversarial.py --author-zip /path/to/author.zip
    python audit_inventory.py

Optional arguments to independent_verify.py:

    --inputs /path/to/catalog.json /path/to/problems.json /path/to/reports.json
    --pdf-inputs /path/to/owr.pdf /path/to/struwe.pdf /path/to/robert.pdf /path/to/martinazzi.pdf

External inputs are read locally and are not included or reproduced in this
archive. Without them, replay status is explicitly NOT_REQUESTED. The checker
uses an externally pinned original author ZIP before inspecting it. Internal
manifests are inventories, not cryptographic signatures. Receipt/archive hashes
must be checked against a trusted independently supplied value.

No PDFs, screenshots, source extracts, corpus contents, private coordination,
credentials, or private personal information are included. The mathematical
examples are finite algebraic/measure controls, never PDE counterexamples.
