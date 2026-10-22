# Verification contract

The mathematical control script uses only the Python standard library and exact rational arithmetic. It performs **19,141 explicit finite predicates**. Exceptions, rather than Python assertions, enforce failures, so optimized Python does not disable the controls.

The checks cover:

- Laurent-polynomial differential intertwining in exactly three radial variables, with wrong-dimension negative controls
- The weak-test-function total-derivative identity, including a sign-error negative control
- Spherical eigenvalue shifts, the 5/2 endpoint, and the additive-gap distinction
- The degree-three harmonic polynomial which diagnoses the literal notation problem
- Commutants of three normal-coordinate rotations in several finite dimensions, verifying tangential/normal block restrictions
- Star-tree constant-speed and midpoint Lipschitz identities used by the boundary cutoff competitor
- Cartesian slab comparison thresholds
- Finite transverse Fourier/Parseval inequalities and the exact first spectral gap
- Bessel radial coefficient recurrences and wrong-order negative controls

These are diagnostic and reproducibility checks. They do not prove Hardy's inequality, removability, distributional class membership, Sobolev compactness, the imported interior classification, or global spectral optimality. Those analytic claims must be reviewed from the written proofs and credited references. In particular no finite test asserts that the half-ball Y partition is a global sum minimizer.

## Replay

From any working directory:

    python3 -I -B /path/to/packet/check_math.py
    python3 -I -O -B /path/to/packet/check_math.py
    python3 -I -B /path/to/packet/verify_packet.py --replay
    python3 -I -O -B /path/to/packet/verify_packet.py --replay
    python3 -I -B /path/to/packet/test_integrity.py

The output of check_math.py must match check_results.json byte-for-byte. verify_packet.py checks exact flat-directory membership, rejects symlinks and directories, checks file byte counts and SHA-256 digests, and optionally replays the mathematical script. test_integrity.py runs a clean baseline and deliberate mutation/missing-file/extra-file/symlink/wrong-size corruptions in disposable copies under both normal and optimized Python.

The manifest is not self-authenticating. The outer frozen archive and externally reported manifest/proof hashes bind the review target. No script here downloads third-party sources or claims to recreate the historical retrievals; source hashes record the bytes inspected at authoring time.
