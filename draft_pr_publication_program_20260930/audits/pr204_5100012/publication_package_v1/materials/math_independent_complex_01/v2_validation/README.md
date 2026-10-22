# Validation kit v2

This directory resolves a bounded validation-code hardening issue. No theorem issue was found. The universal mathematical result remains the Jacobi proof reviewed in the sealed parent COMPLEX_AUDIT.md; the early projective route was not completed and is not the basis for clearance.

The original five content artifacts and parent manifest remain byte-for-byte intact. Parent manifest SHA256:
4ca9a0a74d59acd78865252388696b7e8b71a8ed71d1c0669b0a078413ae6071

The parent code compared residuals using "if value > tolerance"; NaN comparisons can be false. V2 applies mp.isfinite and real-value checks before using or reporting vertices, side vectors, feet, areas, products, predictions, residuals, traces, parameters and coefficients. Both C_A and C_T must be strictly positive. Every upper-bound check uses fail-closed "if not(value <= tolerance)". The six wrong-parity controls must have positive measured spread >1e-30. The repeated-list control constructs the actual primitive six-vertex list and its duplicated twelve-entry list, checks area/pedal/product scaling, and requires a positive product spread across its two phases.

The valid runs contain five exact symbolic checks, 27 configurations and 81 phases, six enforced wrong-parity spread controls, and two repeated-list phases. Each complete run executes 9679 finite-value guard calls in 63 categories. These are floating-point, noninterval diagnostics; the universal theorem is established by the written proof.

guard_controls.py passed one complete ordinary run and one complete -O run. Their mathematical outputs and guard counts agree. In EACH mode the driver authenticated these three actual failures at the intended check:

- First contact identity target changed from1 to2: nonzero exact polynomial rejected.
- First numerical original-area prediction multiplied by2: actual residual approximately4.95785 rejected.
- NaN inserted into the first actual numerical area residual: rejected as nonfinite.

Thus there are two full accepted runs and six authenticated mutation rejections. This is bounded mutation coverage at the first identity/residual, not an exhaustive mutation campaign. The finite guards for all other categories are exercised during valid runs; they were not each independently mutated.

Run with a Python environment containing SymPy1.14.0 and mpmath1.3.0. No installation or dependency download is performed. PR204_RUNTIME_PACKAGES optionally points to a directory containing the two packages. Otherwise the verifier searches ancestor-relative paths for the already existing sibling runtime; if none exists it uses normally installed packages. No fixed user-home path is embedded. All calls disable bytecode, including optimized subprocesses.

To repeat the bounded controls from this directory:
python3 -B guard_controls.py

For a standalone diagnostic without the sealed parent custody fixture:
python3 -B verify_complex_v2.py

The local controls driver requires and verifies the sealed parent manifest and all five parent content hashes both before and after its runs. The standalone verifier checks that manifest pin whenever the parent manifest is present and explicitly reports absence in a standalone context.

controls_output.json records the complete rejection outcomes and hashes of both successful full outputs. AUTHORED_MANIFEST_V2.json is the exact new allowlist, excluding itself to avoid recursive hashing. No priority, novelty, publication or tracker action is implied.
