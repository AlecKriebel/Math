# v1.1.2 release-hardening disposition

The external adversarial review was accepted on all three mandatory points:

1. The supplement now gives commands that work from the linked monorepository
   root.
2. The stale 18-page replay record and logs were moved to explicit history.
   Promotion of the current deterministic archive, envelope, manifests, and
   three clean transcripts is conditional on the post-upload public-release
   gate; the tracked source does not treat a URL string as proof of
   publication.
3. Section 10 now says “generic exact infinite-data” observations.

The optional wording suggestion was also adopted: reader-facing text uses
“separately implemented replay,” with the disclosure retaining the explicit
meaning “code-independent implementation, not independent human review.”

No theorem statement, parameter domain, network convention, local atlas, or
sharpness result was weakened or expanded in this revision.

## Clean-room package findings

The subsequent clean-room package review raised six release-engineering
findings. All were accepted and repaired as follows.

1. **R1 — stale replay evidence.** The old Outcome-P/18-page records now live
   only under `history/superseded_release_evidence/outcome_p_2026-08-13/`,
   with their own exact `SHA256SUMS`. The current eight-asset release has a
   distinct v1.1.2 tag and external envelope.
2. **R2 — archive-local build paths.** Every source ZIP carries instructions
   for its actual extracted layout. `verify_submission_source_archives.py`
   extracts all three ZIPs, executes those commands literally, and requires
   byte-for-byte agreement with all six packaged article/supplement PDFs and
   both cover letters.
3. **R3 — incomplete checksum manifests.** Package manifests must now be a
   flat exact bijection with the expected portal files. Deletion, duplication,
   renaming, and valid-hash misassignment mutations are rejected.
4. **R4 — provenance status.** The offline gate reports only
   `PACKAGE_CANDIDATE_VERIFIED`. The separate bounded network verifier reports
   `PUBLIC_RELEASE_VERIFIED` only after downloading the public annotated tag,
   envelope, archive, manifest, and every transcript.
5. **R5 — public manifest shape.** `RELEASE_ASSET_SHA256SUMS` is flat and
   covers the other seven downloaded release assets by basename, including
   `RELEASE_ENVELOPE.json`; the manifest itself is the explicit downloaded
   trust anchor. The public verdict records its SHA-256 and rejects a
   lightweight tag in place of the required annotated tag.
6. **R6 — JMB supplementary identification.** The JMB variant cites Online
   Resource 1, and that journal-specific PDF/source identifies the article,
   journal, author, affiliation, and corresponding email.

The two cover-letter punctuation blemishes were corrected, the harmless
Tectonic `lineno.sty` source-comment warning is recorded in the visual audit,
and all current package instructions preserve the human portal-day recheck.

The active source candidate is not represented as a completed public release
until `reproducibility/verify_public_release.py` has downloaded the eight
assets and returned `PUBLIC_RELEASE_VERIFIED`.
