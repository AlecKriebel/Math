# Reproducible finite controls

Use Python3.14.6 with NumPy2.3.4 and SymPy1.14.0 (recorded replay versions). From the extracted archive root, install verification/requirements.txt in a disposable environment and run:

    python verification/run_checks.py --output verification_run.json

All seven programs execute in temporary working directories; the archived originals and scripts are unchanged. The first four run unchanged original programs, check their pinned script bytes and compare every JSON field against the root replay, allowing at most 1e-12 absolute/relative drift in floating numbers. They report 301+625+482+748=2156 exact assertions, alongside explicitly illustrative floating tables in the first two programs. These counts are program-reported checks, not independent proof obligations.

The new ball program performs 1244 rational/integer controls without floating eigenvalue calculations. The kernel program checks symbolic differentiation, expansions, scaling and 427 complete integer shells through squared radius512, plus illustrative static Gaussian and dynamic refinement tables. The final spectral program illustrates a defective cluster with norm-convergent Riesz projections while full resolvent norms do not converge. Its finite matrices and contour quadrature are not proof certificates.

The executable controls do not prove Hilbert-space completeness, continuum or mesh limits, Fredholm continuation, source coverage, historical priority or the existence of a finite effective index in the compact-support construction. Those conclusions require the written proof and source reading. The analytic support index is existential and is not computed. PACKAGE_FILES.json verifies archive bytes, not mathematical truth. Historical manifests may contain absolute provenance paths; execution here uses only archive-relative paths and temporary directories. No network access is needed for the checks.
