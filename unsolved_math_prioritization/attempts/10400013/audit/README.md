# Independent audit and correction

AMR-103-0013 / 10400013, rank 1009. Accepted as a scoped partial attempt: **UNSOLVED, 5/5 approaches**. Read AUDIT.md for mathematical review and source limits, ACCEPTANCE.json for the disposition, and CORRECTION.patch for the exact integer-arithmetic repair.

The corrected freeze changes only verify.py and the two necessary integrity anchors. The original author packet and archive remain separate and unchanged. The author CLAIMS.json retains its historical independent_audit_completed=false flag; the independent audit is attested separately here and does not rewrite the author's provenance.

Authenticate AUDIT_MANIFEST.json against its separately supplied SHA-256 before relying on the artifacts. For executable replay run python -I -S -B independent_checks.py ORIGINAL_FREEZE corrected_freeze, also with -O and -OO. No copied sources, catalog contents, private notes, or remote-write claims are included.
