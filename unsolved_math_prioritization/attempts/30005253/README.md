# Monotonized asymptotic risk: reviewed partial investigation

Problem **30005253 / OWR-11695855-006**, rank **627**.

**Status: unsolved, five substantive approaches exhausted. No full-resolution or novelty claim.**

The source asks for a statistical optimality principle without fixing its comparison class. This investigation proves a restricted selector theorem, a pointwise-versus-uniform counterexample, and a full data-conditional Gaussian shrinkage comparison. These partial statements do not settle the broad source question.

Read [ADDENDUM.md](ADDENDUM.md) first for four accepted scope clarifications. The frozen [author packet](author/README.md) and the [complete independent audit](audit/AUDIT.md) remain unchanged. The audit includes its immutable input copy, exact verifier, source citations and numerical sanity checks. Source PDFs, extracted full texts and catalogue corpora are excluded.

## Verify the final layout

Python 3 standard library:

```sh
python -B RELEASE_CHECKS.py
```

The checker strictly verifies the complete manifest and the original/audit bindings, compares both copies of the frozen input, repeats the original and independent exact controls byte-for-byte, and executes negative controls for tampering, missing or unexpected files, malformed or duplicated manifest entries, unsafe paths and symlinks.

Optional NumPy numerical sanity check, 1,800 fits:

```sh
OPENBLAS_NUM_THREADS=1 python -B audit/gaussian_sanity.py --output /tmp/risk-gaussian-replay.json
```

These floating-point simulations are sanity checks only. They are separate from the exact controls and analytical proofs. Small numerical differences across library versions are possible.
