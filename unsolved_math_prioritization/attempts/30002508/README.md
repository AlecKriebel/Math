# Nyman–Beurling cutoff distances: audited partial results

Problem 30002508 / OWR-12866-018. **Status: unsolved, five approaches completed.**

The frozen author packet proves left-continuity, positive distance at each finite cutoff, strict increase of the approximation spaces, explicit rational lower-bound witnesses, and strict improvement from cutoff 1. The independent audit verifies these partial results and additionally proves right-continuity at cutoff 1.

Neither right-continuity at arbitrary interior cutoffs nor strict decrease between arbitrary cutoffs greater than 1 has been established. No novelty claim is made.

- [Frozen proofs](author/PROOF.md)
- [Independent audit and endpoint strengthening](audit/AUDIT.md)
- [Release addendum: source qualification and mathematical scope](RELEASE_ADDENDUM.md)
- [Exact original controls](author/verify_controls.py)
- [Independent controls](audit/independent_controls.py)
- [Final-layout verification](verify_release.py)

Run `python3 verify_release.py` from this directory or by absolute path. The verifier checks a strict complete-file manifest, reproduces the original and independent controls, checks original-input bindings, and rejects deliberate manifest mutations.

All author and audit files are preserved byte for byte. Source documents and dataset corpora are not included. The manifest authenticates the complete packet relative to its recorded hashes; it is not a mathematical proof certificate.
