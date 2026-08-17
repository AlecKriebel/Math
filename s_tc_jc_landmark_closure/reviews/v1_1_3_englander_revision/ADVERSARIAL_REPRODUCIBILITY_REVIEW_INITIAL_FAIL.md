# Initial adversarial reproducibility review — preserved failure

Date: 2026-08-17
Status: **FAIL — superseded only after the listed defects are repaired and
replayed**

The independent package referee found four pre-submission defects in the
first v1.1.3 candidate:

1. Archive-local PDF commands omitted
   `SOURCE_DATE_EPOCH=1786924800`, although the replay harness injected it.
   Literal documented builds therefore did not reproduce the delivered PDF
   bytes.  The capsule also called `requirements.txt` an environment lock even
   though Tectonic, its bundle, Bash, `gh`, and checksum tools are external.
2. The public-release verifier compared the archive's self-declared commit
   marker with the annotated tag but did not compare every tracked archive
   byte and mode with the tagged Git tree, nor run the extracted-archive
   verifier.  A coherent replacement of archive, envelope, manifest, and
   transcripts could therefore have asserted the legitimate tag hash while
   changing tracked source bytes.
3. The Systematic Biology upload map told the author to send the verifier ZIP
   to ScholarOne, contrary to the journal's current instruction to deposit
   scripts/code in Zenodo rather than upload them to ScholarOne.
4. The JMB map designated a generic verifier ZIP as an additional Online
   Resource even though it lacked that journal's required identifying front
   matter and manuscript citation.

The referee also noted the expected pre-seal state: stale v1.1.2 external
assets, unsealed core hashes, absent v1.1.3 tag, and absent final review files.
Those facts were not mathematical defects, but reuse of the old bytes was
forbidden.

This failure report is retained as part of the release history.  The active
final review must independently confirm each repair and end in `PASS`.

FAIL
