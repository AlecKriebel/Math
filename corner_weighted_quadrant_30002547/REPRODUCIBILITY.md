# Reproducibility and evidentiary limits

## Environment and isolation

The included checker programs require Python 3.10 or later and only the standard library. The recorded replay used the Python version in REPLAY_VERIFICATION.json. Each checker was copied by an explicit allowlist into a new temporary directory and run with `python -I`, without importing local research files or consulting preexisting outputs. Every subprocess exited with code zero and no stderr.

Run `python3 -I run_checks.py` from any directory to repeat that process. It prints a new JSON report to stdout and does not alter this package. The fresh timestamp may differ; the exact mathematical output is deterministic. Run `python3 -I verify_manifest.py` to verify the recorded package bytes before replay.

No included program downloads files, contacts external services, changes a repository, or publishes data.

## Exact controls

1. **check_transfer_and_mirror.py**
   - Checks all 16 direction-pair reverse-negation identities.
   - Checks 660 ordered mirror pairs through input length 4, including weight addition, confinement, return, length, and injectivity.
   - Exhaustively checks the negative local-block coefficient for lengths 1 through 8.
   - Computes exact coefficient polynomials Q_n(a) through half-length 8. Its complete output is also saved as transfer_and_mirror_checks.json.

2. **check_signed_pencil.py**
   - Uses two distinct recurrences: direct last-direction dynamic programming and contracted diagonal macrosteps.
   - Compares exact rational coefficients through step length 14 at a=-1, -3/4, -1/2, -1/4, and 0.
   - All comparisons agree. At a=-1 the first eight coefficients are 1, 2, 6, 22, 92, 424, 2108, 11134.

3. **verify_attempt_3.py**
   - Verifies both shuffle-family formulas for n=1 through 40 using integer dynamic programming.
   - Independently exhausts all 54,810 words for the explicit n=13 (P2) counterexample, checking coordinates and adjacent letters directly.
   - Confirms the exact histograms, the a+1 coefficients [210,-182,13741], the marked-corner derivative identity, and the exact examples -42 and -6919/100.

4. **check_transition_and_mirror.py**
   - Independently rechecks the mirror construction with the proof's H=ceil(n^(2/3)) through input length 6, using an integer definition of H. The pair counts are [4,16,64,572,6304,78248], totaling 85,208.
   - Uses eight finitely supported rational test vectors, including boundary support, and five rational parameter pairs to verify the quadratic-pencil square factorization and derivative rearrangement.
   - Checks the critical transition factorization, a rational upper-branch critical comparison, exact central-binomial norm identities through degree 80, and the formal critical recurrence through truncation degree 20.
   - Checks the 16 entries of M^2 as exact polynomials, the no-initial-seam endpoint identity through lengths 2 to 41, and the a=-1 arbitrary-word coefficient formula through length 80.
   - These checks never infer an infinite operator spectrum from a finite matrix.

## What the computations establish

The computations exactly confirm the tested combinatorial encodings, finite identities, boundary conventions and explicit counterexample counts. In particular, no floating-point estimate, fitted exponent, ratio extrapolation or numerical eigenvalue is used as evidence of radius equality.

The all-parameter nonnegative radius, signed complex-disk invertibility, finite Abel limit, transition-point derivative divergence, projection formula, and all-length blocking obstruction are justified by the complete mathematical proofs and their independent audits, not by a finite sweep. The finite tests do not by themselves establish a limit, a radius, an infinite-dimensional range condition, or a statement for all real parameters.

## Integrity and reproducibility record

REPLAY_VERIFICATION.json gives the exact stdout, exit code, stderr and SHA-256 of every replayed checker. MANIFEST.json records every public package file other than itself, including these results and the verifier. The manifest deliberately excludes its own bytes to avoid circular hashing. The package publisher can additionally record the manifest's SHA-256 as the package identity.

SOURCE_VERIFICATION.json contains public source titles, URLs, PDF byte counts and SHA-256 values from the inspected sources. Those PDFs and their extracted text are not distributed here. The source hash record is retrieval verification metadata, not a replay dependency or a claim that a remote PDF will never change.
