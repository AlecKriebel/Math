# Portable independent audit

This package contains the unchanged authored frozen packet and its independent audit.
The mathematical target remains unresolved. No source PDFs, source full text, datasets,
or private coordination files are included.

Read `independent-audit/AUDIT.md` for the verdict, proof checks, qualifications, and
optional citation refinements. Source inspection metadata is in
`independent-audit/SOURCE_INSPECTION.json`.

From this package root run:

    python3 independent-audit/verify_audit.py

Only Python's standard library is required. The script verifies every frozen input
hash, runs the frozen author verifier, compares its stored output, checks the hashes
again, and runs separately authored exact controls. The finite tests supplement the
written arguments; they do not establish the unresolved global rigidity theorem.

The original inputs live in `public/`; the new review lives in `independent-audit/`.
`AUDIT_MANIFEST.json` binds all included files except itself, using relative paths.
The outer ZIP checksum is supplied separately.
