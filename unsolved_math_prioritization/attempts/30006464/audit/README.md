# Short cusp coefficient detection independent audit

The frozen partial report for problem 30006464 passes independent review, subject to the harmless zero-dimensional convention stated in PRECISION_ADDENDUM.md. The original all-forms positive-epsilon problem remains unresolved after five approaches.

Read AUDIT.md for findings, PRECISION_ADDENDUM.md for endpoint and constant details, and AUDIT_RESULTS.json for actual replay coverage. AUTHOR contains the 12 original files, unchanged. GRAM_ZERO_DIMENSION.patch and CORRECTION.json bind the operative d=0 correction, which was applied to a separate copy and actually replayed.

Python 3.10 or newer, standard library only:

    python3 -I -B verify_audit.py
    python3 -I -B test_audit.py

Optional independent complete-input verification, supplying files explicitly:

    python3 -I -B verify_inputs.py catalog.json problems.json research_results.json

The latter prints only public identity metadata and match results. Input datasets and third-party source PDFs are deliberately excluded from this archive. SOURCE_CHECKS.json records only public bibliographic and inspection metadata. Finite computations are not analytic proof certification, human peer review, or a claim of novelty.
