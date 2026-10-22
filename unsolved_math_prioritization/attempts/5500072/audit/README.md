# Independent audit: regular-pentagon surfaces

Decision: original author packet accepted unchanged as a bounded partial, unresolved 3/5. No author mathematical correction was required and no global resolution or novelty claim is made. This updated packet corrects the previous audit's false human-review label; see `PROVENANCE_CORRECTION.md` and `provenance_correction.patch`.

Review provenance: independent AI review with executable checks. No human peer review or formal verification has been performed.

Start with `INDEPENDENT_AUDIT.md` for the complete mathematical/source/artifact review and `EXACT_ACCEPTANCE.json` for the exact accepted object and scope.

This packet includes the unchanged author ZIP, its original external manifest, and its original bootstrap. The author's historical audit-pending wording is preserved; the independent acceptance here records the later review.

Run `python -I independent_exact_checks.py` for the separate exact-arithmetic checks. Run `python -I audit_replay.py` for archive, isolated replay, and adversarial checks without external data. That mode explicitly reports complete-corpus/source verification as absent.

To repeat all 81 checks, supply independently obtained complete inputs:

    python -I audit_replay.py --catalog CATALOG --problems PROBLEMS --reports REPORTS --source-dir PUBLIC_SOURCE_DIRECTORY

The source directory must contain the five exact files named in `source_verification.json`. Full source and corpus checks are read-only; the inputs are never included in output. Paths with spaces are supported. Normal and optimized isolated Python are exercised internally; the full test driver was also independently run with `python -I -O`, producing identical results.

`audit_replay_results.json` records the full-input run. `independent_exact_results.json` records the mathematical checks. `source_verification.json` contains only public bibliographic, hash, retrieval, and inspection metadata. No third-party PDFs, extracted source text, datasets, private sources, or coordination material are included.

The external audit bootstrap verifies the separately pinned ZIP and all its members before replaying in a fresh unrelated directory. The external manifest is an integrity reference, not a digital signature. No supplied executable verifies the global geometric problem or replaces the full written mathematical audit.
