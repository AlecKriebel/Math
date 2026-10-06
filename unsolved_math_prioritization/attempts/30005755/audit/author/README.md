# TF equivalence and canonical decomposition cones

Problem 30005755, OWR-14298157-005. Status: scoped partial results; the full target is not solved here.

The main proof supplies a finite torsion-witness criterion and applies it to a 12-dimensional wild algebra and weight eta=(1,1,-1). In that example the exact TF class is {(a,b,-b): a,b>0}, the cone from all positive multiples is its closed two-dimensional cone, and the cone from eta alone is only a ray.

- PROOF.md contains complete scoped arguments, assumptions, and the exact remaining gap.
- SOURCE_REVIEW.md distinguishes the primary target from known and newly reported literature results.
- verification.py and expected_results.json give exact reproducible linear-algebra and module-dimension checks. They do not claim to computationally verify all modules.
- source_metadata.json records public-source hashes, byte counts, and identity checks.
- RESEARCH_LOG.md records five substantive approaches and their outcomes.
- manifest.json authenticates the frozen authored files. verify_manifest.py checks it.

Run `python3 verification.py --check expected_results.json` and `python3 verify_manifest.py` from this directory. Only the Python standard library is required. Mathematical validity also requires reading the proof and its stated external decomposition theorems.

No third-party PDFs, extracts, images, raw corpora, or private coordination material are included. No novelty, journal acceptance, or full-resolution claim is made.
