# Minimal foliations in closed hyperbolic three manifolds

Problem 2816, KP-3.18, K3 Problem 3.18. Research date: 2026-10-06.

**Result: unsolved, 3 of 5 approaches used.** This package proves scoped necessary conditions and identifies exact gaps. It supplies neither a closed hyperbolic example nor a general nonexistence theorem. The conditions proved here are elementary consequences of classical differential geometry; no novelty or priority is claimed.

The exact K3 question is recovered in `SOURCE_AUDIT.md`. `PROOF.md` gives complete arguments for a curvature-balance obstruction, a compact-product-neighborhood obstruction, and failure of a particular hyperbolic-space foliation to descend to a compact quotient. `APPROACHES.md` records why none settles the unrestricted question.

Run `python3 check_calculations.py` for the supplementary exact algebra and coordinate computations. It requires SymPy; it was tested with Python 3.12.14 and SymPy 1.14.0. Run `python3 verify_release.py` for local file-integrity validation. Both retain explicit checks under Python optimization. Integrity validation only compares against this package's manifest; its authenticity must be established from an independently trusted external digest.

The calculations do not certify the mathematical proofs or construct a foliation. Their expected output is `calculation_results.json`. This is an AI-assisted, unrefereed mathematical investigation. Independent review is still required. The publication-safe package contains authored exposition, programs, and public verification metadata, without source PDFs, source extractions, or dataset records.
