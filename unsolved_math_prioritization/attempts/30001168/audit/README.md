# Independent audit: weighted Yamabe heat comparison, 30001168

The audit accepts the dimension-three counterexample in the unchanged author
freeze, with scope and qualifications recorded in AUDIT.md. It does not
resolve the separate n>=4 monotonicity problem 30001169, establish novelty,
or claim human peer review.

The author/ directory is byte-identical to the eight members of the supplied
frozen author ZIP. Its historical pending-audit wording is intentionally
preserved. No correction to its proof was required.

Run with Python 3 and its standard library only:

    python -I -B verify_audit.py
    python -I -B -O verify_audit.py
    python -I -B run_audit_controls.py

The independent certificate uses another exact exponential enclosure,
another square-root implementation, 200 rather than 100 cells, and four
rather than three explicit spherical modes. The audit remains an analytic
review plus rational certificates, not a formal proof-assistant verification.

Only authored proof/audit/code/results and public verification metadata are
included. No PDFs, extracted source text, dataset records, source corpora,
private sources, or coordination records are included.
