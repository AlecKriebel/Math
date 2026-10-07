# SIRSN tree obstruction: independent audit

Problem 9700036 / AMR-096-0036, queue rank 936.

The exact mathematical acceptance covers both the clarified application in `accepted/RESULT.md` and the explicit sufficient corollary in `SOURCE_PROOF_REPAIR.md`. Read `AUDIT_REPORT.md` and `ACCEPTANCE.json` for the verdict and limits. The credited obstruction theorem is Aldous (2021), not a new theorem claimed here. This is AI review, not human peer review or formal verification.

`author/` preserves all five frozen original files. `accepted/` reproduces the five-file clarified archive. `CLARIFICATION.patch` was applied in an isolated copy and reproduced that archive exactly. The source-proof repair is supplied separately and must accompany the clarified archive when sharing the mathematical acceptance.

Replay with an externally trusted manifest pin:

python -I -B verify_audit.py --manifest-sha SHA256_OF_MANIFEST

Also run with -O. Optional `--catalog FILE --problems FILE --reports FILE --sources-dir DIRECTORY` rebinds and replays against the complete external corpora and all four source PDFs. Optional `--author-zip FILE --clarified-zip FILE` checks the external archives and every member. The audit ZIP external manifest and receipt supply the required pins. Neither source documents nor datasets are bundled.

The verifier checks integrity and finite diagnostics. The mathematical conclusion comes from the written argument and cited prior theorem; passing Python checks does not establish a continuum proof.
