# First independent preprint review
Dated 2026-10-04 UTC. The report records an internal AI-assisted adversarial review, zero mandatory findings, and explicitly limited priority evidence.

The final public manifest binds this folder exactly. Before approved closure, the parent PRE_CLOSURE.json supplies its proposed public bindings. The verifier checks existing bytes only; it performs no mathematical rerun, installation, network access, or file write.

Commands from this review's parent folder:
```
python3 -B public/verify_review.py
python3 -B public/verify_review.py --full
python3 -B public/verify_review.py --full --include-external
python3 -B public/independent_literal_controls.py
```

Default checks the curated public namespace and complete native outputs. Full additionally checks all retained private evidence, the immutable source-first gate, analytic freeze, candidate pins, ZIP member bytes, native before/after captures and terminal verification receipts. The explicit external option additionally checks the bound original source, five primary-reference cache PDFs and four current parent candidate files; those external bytes are omitted from this public curation. Private source derivatives and native execution histories are not publicly included.

The original extracted package was removed only after all 69 members were verified byte-equal to the retained unchanged ZIP and native preexecution pins. This was lossless storage recovery; the private verifier reads ZIP bytes in memory. The historical capture helper controls/run_native.py records a completed execution and expects the original extraction path. Do not rerun it against existing captures: reproduce the pinned ZIP independently in a fresh workspace and preserve fresh streams separately. Its exact previously executed package code is retained inside ZIP.

Checksums provide integrity relative to recorded bindings, not independent authenticity, external human peer review, literature completeness, or a global novelty certificate. Finite mathematical controls do not replace the universal proof. No external upload, publication, contact, installation or Git operation is represented by this review.

