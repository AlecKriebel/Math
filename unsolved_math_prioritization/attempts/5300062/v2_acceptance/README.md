# V2 bounded-delta acceptance: problem 5300062

Read ACCEPTANCE.md. Current scoped verdict: ACCEPT_SCOPED_PARTIAL_V2.
The original problem remains UNSOLVED, 5/5. The historical author and independent
audit freezes remain unchanged.

Verify this packet with an independently retained digest:

    python -B verify.py --expected-manifest ACCEPTANCE_MANIFEST_SHA256

Replay the full bounded delta against the three immutable input ZIPs:

    python -B verify.py --expected-manifest ACCEPTANCE_MANIFEST_SHA256 --original ORIGINAL_AUTHOR_ZIP --v2 AUTHOR_V2_ZIP --audit ORIGINAL_AUDIT_ZIP

All three input flags must be supplied together. Python 3 plus mpmath 1.3.0 are
needed for the full replay, because it also replays the original independent
controls. Packet-only verification uses the Python standard library. The input
ZIPs contain authored materials and metadata, not third-party source content.

The code authenticates each ZIP before reading it, checks strict manifests,
reconstructs the exact three-edit report, compares the full patch, checks the
permitted file delta, and replays the original/v2/audit verifiers after relocation.
Only hashes, match results, locations and status metadata are emitted.

Integrity tamper controls, isolated in temporary copies:

    python -B code/test_verifier.py

The acceptance manifest is supplied separately in the freeze receipt. A trusted
verifier and an independently retained external digest are assumed; no script
can authenticate itself against an attacker who replaces both it and its anchor.
