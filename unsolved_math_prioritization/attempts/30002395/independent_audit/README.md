# Independent acceptance audit for problem 30002395

Verdict: ACCEPTED AFTER CORRECTION for the five scoped partial results. Universal problem: UNSOLVED, 5/5 substantive approaches.

Start with AUDIT.md. CORRECTION.patch qualifies one Turn 2 sentence in PROOF.md and TURN_2.md. The corrected directory contains the complete corrected author packet; all other author members remain byte-identical. Its own MANIFEST.json records the corrected copy's provenance and hashes. The original author packet is unchanged.

Reproduce from this directory:

    python3 independent_controls.py --frozen ../public
    python3 scope_controls.py
    python3 verify_audit.py --self-test
    python3 corrected/verify_manifest.py
    python3 verify_audit.py --expected-sha256 <independently retained audit-manifest SHA-256>

CONTROL_RESULTS.json records 2,315,828 independent finite and integrity checks. SCOPE_CONTROL_RESULTS.json records 412 patch and analytical-witness regressions. AUTHOR_CONTROL_REPLAY.json records the author's 1,029,251 checks. Numerical counts do not certify infinite mathematical claims.

SOURCE_AUDIT.json records public PDF hashes, sizes, page counts, reinspection boundaries and source-status checks. This bundle contains no primary documents or copied primary-source text. The audit is AI review, not human peer review or theorem-prover certification. No remote action was performed.

MANIFEST.json lists every file recursively except itself. Its external digest must be retained separately to detect a replacement manifest. Running mathematical controls writes only to standard output; redirect replay output outside the frozen bundle if preserving its hash identity.
