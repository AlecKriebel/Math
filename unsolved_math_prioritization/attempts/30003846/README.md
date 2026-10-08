# Fast bump groups: conditional scope audit

Start with [ACCEPTANCE.md](ACCEPTANCE.md). The connected classification and decomposition proof pass at an explicit restricted permutational wreath convention allowing nonfaithful action. The original undefined wreath terminology remains a scope hold. Queue status stays queued, 0/5; this verifies prior work and adds no attempt.

## Reading order

- CONNECTED_RECONSTRUCTION.md: credited reconstruction of Golan's connected classification and explicit imports
- HISTORICAL_CONNECTED_AUDIT.md: first independent review, with its chronological I0 hold explained
- SCOPE_AUDIT.md: the missing decomposition proof and precise product convention
- INDEPENDENT_REVIEW.md: independent acceptance of that supplement
- SCOPE_STATUS_CORRECTION.patch and PROVENANCE.json: narrowly scoped textual refinements
- HARDENING.patch, HARDENING.json and HARDENING_REPLAY.json: reproducibility-only checker corrections
- SOURCE_METADATA.json: public-source verification metadata; no source bodies

## Verification

Authenticate the BOOTSTRAP.py SHA-256 using the literal pin in the draft PR description before executing it. Use Python 3 with -I -S -B and optionally -O or -OO. Arguments, in order: packet directory, actual before-QUEUE path, actual after-QUEUE path. All packet files and both queue files must be mode 0444, and the packet directory mode 0555; run as UID/EUID 1000. The verifier always checks the actual queue pair. Neither queue body is bundled in this packet: the before file comes from the pinned base commit and the after file is the PR's actual unsolved_math_prioritization/QUEUE.md.

The bootstrap fixes the manifest/verifier identities; the manifest binds every remaining member. The verifier runs all three finite suites and compares their full outputs, allowing only the separately validated top-level elapsed_seconds numeric token to differ. Full raw reference and replay outputs are retained. No elapsed-time deletion hides another field. A standard-library mutation harness separately exercises fail-closed integrity and strict semantic controls under every optimization mode.

Use MUTATION_TESTS.py with arguments: packet directory, before-QUEUE path, after-QUEUE path, externally authenticated bootstrap SHA-256. Authenticate the harness hash from the PR pins as well before running it. The harness includes a full baseline replay and tests integrity failures before execution, then directly tests the authenticated verifier's schema and semantic validators to distinguish their rejection from a digest mismatch. Its mutable fixtures are temporary; the delivered packet and actual queue pair remain read-only.

These computations do not prove the all-n result. Mathematical acceptance is documented separately, with prior-result attribution to Golan's July 2026 preprint. No journal acceptance, novelty, merge, release or DOI is asserted.

PREPARATION_CONTROLS_normal/O/OO files retain complete raw receipts from the corrected preliminary packet. PREPARATION_STAGE.json explains their pre-freeze scope and the final destination-link refinement. The final manifest also authenticates those receipts; a separate final whole-delivery replay checks the final packet and actual queue pair, avoiding any self-referential receipt claim.
