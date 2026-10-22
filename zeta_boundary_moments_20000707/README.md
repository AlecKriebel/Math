# Second zeta moments near the boundary

Problem ID 20000707; AIM 8.1; queue row 1862. Status: UNSOLVED. Five approaches. Classification: PARTIAL_EXPOSITORY.

This package preserves authored proofs of classical consequences, a conditional implication, a coefficient calculation and exact missing-increment reduction, fixed-X renormalization, and an explicit logical countermodel. It does not prove a growing-window transition theorem or resolve the broad AIM question. It claims neither novelty nor global openness.

The compact-weight endpoint constant is conditional on the Ivić announced mean estimate, not certified unconditional and not RH-conditional. The transition leading term ζ(2σ_T) is retained exactly. Numerical diagnostics are not analytic proofs.

Read RESEARCH.md, MATHEMATICAL_AUDIT.md, and SOURCE_STATUS.md. Public-source metadata records prior retrieval and inspection limitations; no third-party papers, dataset contents, or private source extracts are included.

## Reproduction

Python 3 with SymPy and mpmath:

    python checks.py
    python -O checks.py
    python verify_integrity.py
    python -O verify_integrity.py

checks.py prints the complete results and does not modify the package. The optional --symbolic-only flag skips the numerical diagnostic, not the explicit symbolic guards. CHECKS_NORMAL.json and CHECKS_OPTIMIZED.json contain complete captured outputs. AST_PROVENANCE.json records the complete original and transformed ASTs and each assertion-to-explicit-guard conversion, with the original checker hash. The package checker uses no assertions. MUTATION_RESULTS.json records deliberately incorrect mathematics and inventory tampering rejected in both execution modes. These tests are reproducibility checks, not substitutes for the written mathematical proof.

MANIFEST.json inventories every other package file, recursively. It is the only excluded file; its hash and the complete inventory including it are frozen in the separate audit receipt. Verification rejects symlinks, unsafe paths, extra or missing files, and nested manifests.
