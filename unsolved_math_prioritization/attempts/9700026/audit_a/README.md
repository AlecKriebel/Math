# City ODE counterexample audit

ACCEPTED without repair as a refutation of the literal alpha > 1 clause of the 2007 associated-city ODE conjecture. The intended stochastic model and the remaining restricted dynamical questions are not resolved.

- AUDIT_REPORT.md: full independent mathematical and source audit, including a supplementary local Lipschitz and uniqueness proof.
- ACCEPTANCE.json: exact input pins and bounded acceptance verdict.
- author/: unchanged eight-file author package.
- AUTHOR_SAFE_FREEZE.zip and AUTHOR_EXTERNAL_MANIFEST.json: exact original freeze and manifest, renamed locally without changing bytes.
- verify_audit.py: independent rational checks and artifact bindings.
- verify_sources.py: optional private full-corpus and source-PDF pin replay; it prints verification metadata only.
- AUDIT_TEST_RESULTS.json and SOURCE_CHECK_RESULTS.json: execution and tamper receipts.
- SOURCE_AUDIT_METADATA.json: public pins and observation history.
- MANIFEST.json: audit member hashes and sizes.

From this directory run:

    python verify_audit.py
    python -O verify_audit.py
    python -I verify_audit.py
    python -I -O verify_audit.py
    python verify_audit.py --self-test
    python author/verify.py
    python author/verify.py --self-test

With the separately authorized complete inputs, run:

    python verify_sources.py CORPUS_DIRECTORY PDF_DIRECTORY

The corpus directory must contain catalog.json, problems.json, and research_results.json; the PDF directory must contain cities-notes.pdf and cities-2012.pdf matching the published pins. Source files and dataset contents are deliberately absent. No installation, network access, or third-party Python package is needed for these checks.

This is an AI-assisted independent audit, not human peer review or a formal proof certificate. Mathematical acceptance is the reasoned verdict in the report; computations support exact constants and artifact provenance.
