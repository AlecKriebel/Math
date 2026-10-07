# Independent audit: rational VOA finiteness

The five partial mathematical routes and the precise Han v5 limit objection are accepted. The full conjecture remains unsolved in this work. AUDIT.md contains the independent reasoning and acceptance boundary. ACCEPTANCE.json and SOURCE_CHECKS.json record the decision and primary-source inspection.

The original read-only release is preserved. READONLY_REPLAY_FIX.patch fixes the original mutation runner's disposable-copy permissions and updates its manifest entry. The corrected runner was tested from another read-only release and completed all 54 checks. Apply the patch only to a separate working copy if desired.

Independent checks require Python 3, no third-party packages or network. Use the original author packet and the independently recorded SHA-256 of this audit's MANIFEST.json:

    python verify_audit.py --author-root AUTHOR_PACKET --expected-audit-manifest AUDIT_MANIFEST_SHA256
    python test_audit.py --author-root AUTHOR_PACKET --expected-audit-manifest AUDIT_MANIFEST_SHA256

The suite runs normal, -O, and -OO automatically. It invokes the trusted verifier against mutated data, never executes modified target code, and checks for the intended explicit rejection. TEST_RESULTS.json records final observed counts. Independent arithmetic includes normalized descendants, the moving nonzero tail, spectral filters, exact derivation ranks, and central-charge-preserving permutations.

The manifest uses an exact flat inventory and SHA-256 checks. It is not a digital signature. Supply its separately recorded digest; trusting a changed digest supplied by the changed packet defeats authentication. No program here formally proves infinite-dimensional VOA theorems.

Only authored audit text, authored correction/code, and public-source verification metadata are included. Source PDFs, extracts, images, corpus contents, private coordination, and queue/chat material are excluded. No publication or author contact was performed.
