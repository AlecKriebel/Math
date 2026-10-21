# Geodesic root-gap coding: unresolved checkpoint

Row 1844; problem ID 30005529; status UNSOLVED; turns 5.

This package records five partial avenues, not a solution or impossibility theorem. The original authored REPORT.md is byte-identical to its verified input (SHA-256 134658711b21c05418be33b8108d35081074076920d27e3cdf5e6b8f7f1b5fdb). The mathematical audit is sanitized only to use package-relative references. No copied source documents, corpus contents, or private coordination files are included.

Accepted scope: same-sheet tangency and failed geodesic-time sliding; local transverse construction without global coding; endpoint reconstruction with external horizontal sorting; finite collisions confined to m <= D(D^2-1); clock/Palm normalization and exceptional cusp-state caveats. Arnoux–Schmidt formulas remain researcher-primary-checked but not independently source-certified background, not dependencies of new accepted theorems. See CLAIM_LEDGER.json.

Reproduce from this directory with Python 3.12 and SymPy 1.14.0:

    python verify_package.py
    python -O verify_package.py
    python mutation_tests.py

The verifier checks exact inventory, all hashes, AST transformation provenance, and complete JSON results plus complete stdout under normal and optimized Python. Scripts run in temporary directories and never rewrite expected results. Finite checks are implementation evidence, not substitutes for proofs. AST provenance contains authored Python, not scholarly source text. Mutation tests change actual arithmetic and matrix inputs, and exercise undeclared, missing, corrupted, and nested-manifest inventory controls. Only the root MANIFEST.json is excluded from self-hashing.
