# Percolation GFF maximum independent audit

Problem 30005140, rank 791, OWR-10252936-003. Audited 5 October 2026.

Verdict: the stated finite-network and conditional partial results pass independent review. The full all-p>1/2 almost-sure quenched maximum-convergence target remains unresolved after the five approaches. This is not a manuscript-readiness or novelty certification.

Read AUDIT.md for the analytic assessment and CORRECTIONS_AND_CLARIFICATIONS.md for the review-hash completion and normalization details. The author/ directory preserves all 11 frozen author files byte for byte. Their original pending-audit labels are historical.

## Reproduce the public checks

With Python 3 and the standard library, run from the package root:

    python code/verify_manifest.py
    python author/verify.py
    python author/verify_manifest.py
    python code/independent_math.py

The author replay contains 168 assertions with complete results equality. The independent replay contains 15,108 assertions, including 4,096 exhaustive finite box-edge patterns. The counts are assertions, not independent theorems or tests of the infinite-volume conjecture.

Optional source-identity replay requires externally supplied source files, deliberately excluded here:

    python code/verify_inputs.py --catalog CATALOG --problems PROBLEMS --research RESEARCH --pdf-dir PDF_DIRECTORY --author-zip AUTHOR_ZIP

The PDF directory uses the basenames recorded in SOURCE_AUDIT.json. This command emits only identity outcomes. It does not repeat the mathematical or literature audit.

SOURCE_AUDIT.json records independent PDF retrieval, public URLs, hashes, byte counts, inspection locators, and search limitations. PROVENANCE_AUDIT.json binds the complete supplied datasets, exact statement digest, recovered review digest, and upstream manifest. PRIOR_ARTIFACT_AUDIT.json records bounded read-only repository checks.

No source PDFs, extracts, images, raw corpora, private coordination files, or repository response bodies are included. No remote write was performed.
