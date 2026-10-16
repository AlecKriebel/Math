# Portable independent audit: problem 30000403

Verdict: PASS, with nonblocking notes. The author-stage status remains claimed_solved, 3/5, with an independent AI audit; this is not human peer review or formal certification.

Read AUDIT_REPORT.md for the complete mathematical review and CORRECTIONS.md for the separate recommendations. AUDIT_MANIFEST.json binds every audit payload file and the exact frozen author inputs. Source documents and private material are deliberately excluded.

Requirements: Python 3.12 and SymPy 1.14.0 reproduce the recorded environment. The verifier itself uses only the standard library unless --replay is supplied.

Standalone audit integrity:

    python verify_audit.py

Check the frozen author inputs too, where AUTHOR_ROOT contains packet/, AUTHOR_FREEZE.json and author-packet.zip:

    python verify_audit.py --author-root AUTHOR_ROOT

Reproduce all author and independent controls, without modifying the author packet:

    python verify_audit.py --author-root AUTHOR_ROOT --replay

The independent audit controls can also be run directly:

    python independent_checks.py

All scripts are read-only with respect to the author inputs. No network is needed. Counts and finite checks are evidence for the reviewed calculations, not a mechanical proof of the universal theorem. See the report for source-access and novelty limits.
