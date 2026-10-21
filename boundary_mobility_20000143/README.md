# Boundary mobility: accepted partial surface refinements

Problem ID 20000143, queue rank 1858. Date: 2026-10-21.

Broad-question status: **UNSOLVED**. Six substantive mathematical approaches completed; the broad question remains unresolved. No historical conversation-turn count is certified by this package.

REPORT.md preserves the accepted mathematical proof sections. MATHEMATICAL_AUDIT.md records independent review. SOURCE_STATUS.md and PUBLIC_SOURCE_METADATA.json distinguish published inputs from the scoped authored refinements. The original AIM endpoint was unavailable: canonical wording and item identity remain corpus-only, not live-certified. No verbatim canonical problem quotation is supplied. No novelty or full broad-question resolution is claimed. Lehmann's known classifications, exponents, blowup mechanism and cited Schubert rigidity are credited.

The accepted scope includes exact product boundary counts, all-m mixed-face bounds with residual terms and liminf, the thin strip, mc_Q(P²)=4, and quadric all-m lower bounds. The unequal-bidegree obstruction applies only to the stated scaling regime of the construction, not arbitrary families or a global upper bound.

Run from this directory with Python 3 (standard library only):

- python -B check_exact.py
- python -B -O check_exact.py
- python -B verify_package.py
- python -B -O verify_package.py
- python -B mutation_checks.py
- python -B -O mutation_checks.py

check_exact.py replaces removable assert statements with equivalent explicit AssertionError guards. It deterministically rewrites CHECK_RESULTS.json with the identical expected output. Tests compare the complete stdout and result JSON, not only a PASS label; mutations test actual arithmetic and every guard in both interpreter modes. Exact-integer finite tests are sanity checks, not proofs of geometry. The written arguments and explicitly cited geometric inputs supply those proofs.

package_manifest.json recursively inventories every public file except itself, including the verifier and mutation program. It is an integrity check, not an authenticity signature. Only the root manifest is excluded; nested manifests, extra files, symlinks and unsafe paths are not exempt. Manifest hash and complete upload inventory are frozen separately in the verification receipt. No copied PDFs, dataset contents, private extracts, their fingerprints, or private coordination files are included.
