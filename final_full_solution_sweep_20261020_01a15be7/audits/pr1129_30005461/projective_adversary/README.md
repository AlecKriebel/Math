# PR1129 projective adversarial review

Read REVIEW.md for the independent mathematical reconstruction and its limits. CLAIM.json binds the exact target and immutable PR head. SOURCE_BINDINGS.json identifies freshly retrieved primary sources; private/ holds the actual ten-file head, primary PDFs, text extractions, images and retrieval receipts. These private third-party sources are local research inputs, not a redistribution package.

The mathematical verdict is acceptance of the coefficient-threshold projective route, conditional on its credited published theorem. Priority, optional delta material, the separate mixed-exponent proof and publication readiness are outside this review's verdict.

To verify locally without network access, supply the 64-character MANIFEST.json digest from SEAL.sha256 as an external argument:

    python3 -B verify_offline.py --manifest-sha256 DIGEST
    python3 -B -O verify_offline.py --manifest-sha256 DIGEST
    python3 -B -OO verify_offline.py --manifest-sha256 DIGEST

The verifier reads the packet and performs finite exact interface controls. It does not write files, execute captured scripts, call a provider, generate an SOS certificate, or certify a theorem by hashing. It requires the private inputs. VALIDATION_RUNS.json records normal/optimized runs and deliberately malformed controls. validate_packet.py is the review author's sealing/test driver; it writes only within this folder and is not part of the read-only verification entrypoint.
