# Independent segment-mirror audit

Problem 5500031 / AMR-054-0031 / rank 776.

Verdict: scoped claims pass, with a related-catalog completeness addendum and minor reporting clarifications. The full problem remains unsolved, five approaches exhausted. This is an independent AI review, not human peer review.

## Included files

- AUDIT_REPORT.md: proof, source, provenance, and scope review
- ADDENDUM.md: non-destructive correction and clarifications
- independent_verify.py and independent_results.json: 58,598 independent exact checks
- verify_artifacts.py and artifact_results.json: freeze replay and provenance verification
- verification_metadata.json: public source hashes and inspection/search metadata
- MANIFEST.json: byte counts and SHA-256 digests of package members other than itself

No source texts/binaries, raw datasets, source images, raw API responses, or coordination files are included. The original author package was preserved.

## Replay

Python 3 standard library suffices.

    python independent_verify.py > replay.json
    cmp replay.json independent_results.json

For the author freeze and cross-certificate comparison:

    python verify_artifacts.py --author-package AUTHOR_DIRECTORY --author-zip AUTHOR_ZIP

The optional provenance mode additionally requires all nine flags together:

    --problems PROBLEMS_JSON
    --reports RESEARCH_RESULTS_JSON
    --catalog CATALOG_JSON
    --dataset-manifest MANIFEST_JSON
    --dataset-descriptor DESCRIPTOR_JSON
    --campaign-tree CAMPAIGN_TREE_JSON
    --attempts-tree ATTEMPTS_TREE_JSON
    --queue QUEUE_MD
    --primary-html TOPP_HTML

Use the exact repository revision, dataset revision, and object hashes in artifact_results.json. The descriptor URL contains mutable service counters, so a later descriptor response can have a different whole-response digest while still identifying identical immutable LFS files. The script checks those immutable file identities rather than assuming response-byte immutability.

Finite computation validates implementations and examples. It does not enumerate every direction or prove an unrestricted escape theorem.
