# Frozen KTG dependency audit

Row 1885 / ID 10400212 / Ohtsuki Problem 12.6.

Status: NOT SOLVED. Five routes were audited; no new invariant, new impossibility theorem, blanket refutation, or full-closure claim is made. This is an analytic dependency audit, not a mathematical certificate. Acceptance is bound to the exact authored audit bytes, not to a solution.

EXISTENCE_PROOF_AUDIT.md and ACCEPTANCE.md are unchanged authored artifacts. RECOVERY_PUBLIC.md is an expressly limited public-safe synthesis. PUBLIC_SOURCES.json contains public URLs, hashes, sizes, and historical inspection metadata only. Original local provenance labels in the authored acceptance identify its reviewed artifact, not an included directory or a dependency to open.

Important limitations: operation and half-framing dictionaries remain necessary; associated-graded injectivity must not be presumed; recursive obstruction cycles need not be boundaries; compatible all-degree lifts have not been constructed; universality needs simultaneous compatible crossing templates and normalized symbols. The source's omitted degree-two calculation was not independently reimplemented.

Offline integrity check from the parent directory:

    python3 -B ktg_1885_frozen/verify_package.py --receipt KTG_1885_FROZEN_RECEIPT.json
    python3 -B -O ktg_1885_frozen/verify_package.py --receipt KTG_1885_FROZEN_RECEIPT.json

The external receipt is the trusted anchor and must be kept separately. Validation checks exact inventory before reading payloads, disallows symlinks/hardlinks/special files and directories, checks all hashes, and verifies pinned source provenance. It does not validate the mathematics, establish novelty, or authenticate an untrusted replacement receipt/validator. Run only the trusted pinned validator; filesystem mutation during validation is outside this static-package protocol. No sockets are used. No copied source documents, dataset contents, private corpus or coordination files are included. No publication or QUEUE changes were made.
