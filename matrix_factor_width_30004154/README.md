# Exact factor-width partial results

Catalogue row 1834; ID 30004154; source OWR-16938-002. Status: **UNSOLVED, five approaches completed**. The unrestricted structural problem is not solved. Generic SDP feasibility was already known. No novelty or exhaustive literature certification is made.

Accepted results: rational singular and strictly positive-definite spectral-test counterexamples; a rank-two spectral-counterexample family for every k >= 3; complete real rank-two membership and two/three-term classification; finite-ray LP at the full-spark critical width; failure of scalar Schur-complement closure. The symmetric slice and chordal sufficient conditions are credited known results. The repeated-row all-k family is not full-spark.

Read RESEARCH.md, LOW_RANK.md and AUDIT.md for mathematical arguments. SOURCE_GATE.md and SOURCE_METADATA.json record public provenance and the limited inspection of the 2026 Shaked-Monderer paper (January 2027 issue). Its full overlap remains unverified. No copied source texts, datasets, PDFs, unreviewed external conjectures, or private coordination material are included.

Python 3 and SymPy are required. From this directory:

    python -B verify_manifest.py
    python -B run_checks.py
    python -B test_corruption_controls.py

run_checks.py executes all three exact scripts in ordinary and optimized (-O) modes and compares complete stdout bytes with frozen results. test_corruption_controls.py mutates actual certificate coefficients and executes the validators without a manifest gate, and separately tests manifest tampering. These computations verify finite certificates and samples, not replace the uniform mathematical proofs.

AUDIT.md records the prior independent mathematical review. PACKAGE_AUDIT.md records separate independent acceptance of package normalization and test controls. MANIFEST.json is not self-hashed; pin its external SHA-256 to authenticate the snapshot. A malicious coherent rewrite of a package and its manifest is not prevented by an untrusted manifest alone.
