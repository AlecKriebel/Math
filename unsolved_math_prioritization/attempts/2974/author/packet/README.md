# Fixed manifold Lefschetz pencil analysis

This packet records an unresolved five-approach analysis of problem 2974 / KP-4.98. REPORT.md contains the target, the credited 2026 ruled-surface result, complete elementary deductions, a conditional monodromy theorem, and the exact remaining geometric gaps. No universal solution is claimed.

## Reproduce the finite checks

Run with Python 3.9 or newer, using only the standard library:

    python -B verify.py
    python -B -O verify.py
    python -B -OO verify.py

The checker writes JSON only to standard output. It neither downloads nor modifies files. These checks are compatible with a read-only packet and read-only current directory. Runtime checks use explicit exceptions and remain active under optimization.

For integrity verification against the separately supplied external freeze manifest, use both options:

    python -B verify.py --manifest /absolute/path/FREEZE_MANIFEST.json --manifest-sha256 TRUSTED_SHA256

Supply the manifest hash from a separately trusted handoff. Integrity verification checks the pinned manifest hash, the exact file inventory, regular-file status, file sizes and SHA-256 hashes. A replaced checker or a replaced trust anchor is outside that trust model. Hashes do not authenticate authorship or prove mathematics.

## What the checks cover

- The explicit equal-genus T4 pairs and divisor families
- Adjunction, critical-point and blowup-invariant arithmetic
- Exact finite semidirect-product models of the kernel-lattice formula
- Content invariance under explicit unimodular basis changes
- Positivity of the stated fiber-sum and base-change defects

The general group lemma is a written proof. The finite models are illustrations and error checks; they are not a proof over all groups. Nothing here computationally verifies a mapping-class factorization, smooth total-space equivalence, holomorphic-pencil existence, the cited theorems, or the original universal question.

Only authored analysis, generated checks and public reference metadata are included. Third-party PDFs, text extracts, images, corpus records and private work are excluded.
