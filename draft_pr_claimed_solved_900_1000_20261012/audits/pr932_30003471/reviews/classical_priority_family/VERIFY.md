# Verification and release boundary

Run `python3 verify_review.py` from this directory to validate the external manifest SHA, all16 explicitly curated public files, both29-file authentication receipts, source-pin counts and historical/current finite-note equality. `python3 -O verify_review.py` must give the same result; integrity checks do not use assertions. `python3 verify_review.py --private` additionally verifies all26 successful private source retrieval records.

The public check requires only this review's16 curated files plus MANIFEST.json and its external MANIFEST.sha256. It performs no network access and no writes. It is an integrity check, not a theorem prover. The checkable mathematical implication is in PRIOR_IMPLICATION.md.

The original authentication replay requires the original repository Git objects and the selected original snapshot at its documented relative location. In this repository, `python3 authenticate_originals.py END` rereads the actual immutable29 Git blobs and disk copies and writes only this review's END receipt. It must not be run after sealing unless a new checkpoint is intentionally being prepared.

`fetch_primary.py` documents the28 bounded source requests and their URL identities; it overwrites local source receipts and is deliberately not run by verification. Re-fetching mutable metadata is a new observation and must not be represented as reproduction of frozen historical bytes. The exact September4 note also has an immutable commit URL. `render_primary.py` documents the29 complete source-page renders, stored privately; it is read-only with respect to the original sources.

PUBLIC_ALLOWLIST_MAP.json gives explicit roles and exclusions. Raw sources, HTML/JSON bodies, extracts, source-page renders, fetch stdout, private files and temporary files are excluded. MANIFEST.json excludes itself and the external pin. A final response supplies the manifest SHA independently so a reviewer can compare it without trusting a self-reported digest inside the manifest. No files outside this review directory are public outputs of this family.
