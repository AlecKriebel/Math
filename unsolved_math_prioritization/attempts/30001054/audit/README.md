# Scope-correction audit package

Read SCOPE_CORRECTION.md first. The gate is NEEDS_SCOPE_CORRECTION, not unconditional acceptance of the original affirmative classification.

Run:

    python3 witness_check.py
    python3 -O witness_check.py
    python3 test_witness.py
    python3 verify_audit.py

Commands resolve their bundled inputs relative to the script and work after relocation. To independently check downloaded primary-source bytes, use:

    python3 verify_audit.py --sources-dir /directory/containing/pdfs

The filenames there must be owr.pdf, hp.pdf, gp.pdf, and interval.pdf. Fetch them from SOURCES.json; PDFs are deliberately absent from this safe package.

The optional --author-zip argument checks the separately supplied historical author archive against its declared frozen identity. It does not recover missing bytes or validate the author's mathematical conclusion.

The normal and optimized finite tests are distinct from a proof of the imported representation theorem. The manifest checks all other package members. Authentication requires the external audit ZIP hash in the accompanying receipt; a freely rewritten local manifest is not an external trust anchor.

Only authored audit text/code, the authored finite witness, results, and public verification metadata are bundled. Source PDFs, extracted source text, corpus contents, and private coordination material are excluded.
