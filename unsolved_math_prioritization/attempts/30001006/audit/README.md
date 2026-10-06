# Rank 817 independent audit packet

Read AUDIT_REPORT.md for the verdict and scope. ESTIMATE_SUPPLEMENT.md gives explicit constant choices and the CK 3-jet proof. The author freeze is an external authenticated input and is not edited or embedded here.

Verdict: accept the closed scalar/Weyl cone PDE/ODE equivalence for n ≥ 4 and d > 0. The general threshold n_0 = 12 and global algebraic extrema remain unresolved here.

Run `python -B independent_checks.py` and compare its output to independent_results.json. Run `python -B verify_audit.py --expected-manifest HASH`, using the audit receipt's manifest SHA-256 as the external trust anchor. Run test_audit_integrity.py for normal/optimized and relocated replays plus selected mutations.

The verifier, interpreter, and external trust anchor must be trusted. Computing a local manifest hash is useful only for regression tests, not authentication. The checks do not certify geometric existence or the mathematical proof.

The packet contains only authored audit prose/code/results and public verification metadata. It contains no PDFs, source extracts, screenshots, corpus records, dataset contents, private sources, or private coordination. No publication or remote mutation occurred.
