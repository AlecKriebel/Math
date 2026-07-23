# Numerical Construction Search in Dimension 5

> **NUMERICAL EVIDENCE ONLY — NOT A CERTIFICATE.**
>
> These programs use binary64 arithmetic and local nonlinear optimization.
> They neither prove nonexistence nor turn a floating-point point set into an
> exact kissing configuration.

This directory preserves the reproducible construction-search track for
41–44 points on \(S^4\).  The optimized objective is

\[
    \mu(X)=\max_{i<j}\langle x_i,x_j\rangle
\]

subject to \(\|x_i\|=1\).  A kissing configuration would require
\(\mu(X)\leq 1/2\).

## Programs

- `search_spherical5.py`: deterministic multistart discovery using Riesz
  energies, exact or soft hinge losses, log-sum-exp approximations to the
  maximum, random starts, perturbed \(D_5\)+extra starts, deletion starts, and
  \(D_5\) surgery.
- `refine_spherical5.py`: high-temperature log-sum-exp continuation followed
  by a direct epigraph SLSQP minimax step.  It consumes the `.npz` output of
  the search program.
- `analyze_refine_coordinates.py`: user-facing analyzer/refiner for
  comma-separated or whitespace-separated coordinate text.  Every report is
  explicitly labeled numerical only.
- `perturb_benchmark.py`: finite perturb-and-relax challenge of a supplied
  text or `.npz` configuration.
- `slsqp_perturb.py`: direct epigraph-SQP perturbation test, avoiding the basin
  changes that low-temperature continuation can introduce.
- `test_numerical_tools.py`: calibration on the normalized \(D_5\) root
  system and finite-difference gradient tests.
- `RESULTS.md`: seeds, start counts, numerical outcomes, contact graphs,
  spectra, input hashes, and exact replay commands.

## Environment

The reported search was run with:

```text
Python 3.9.6
NumPy 1.24.3
SciPy 1.10.1
```

The repository's discovery requirements may use newer pinned versions.
Floating-point last digits can change across BLAS and optimizer versions.

## Analyze or refine supplied coordinates

From the repository root:

```bash
kissing_number_5/.venv/bin/python \
  kissing_number_5/experiments/random_codes/analyze_refine_coordinates.py \
  kissing_number_5/experiments/input/spherical_codes_5_41.txt
```

Run a local direct minimax refinement and save the JSON report:

```bash
kissing_number_5/.venv/bin/python \
  kissing_number_5/experiments/random_codes/analyze_refine_coordinates.py \
  kissing_number_5/experiments/input/spherical_codes_5_41.txt \
  --refine direct-slsqp \
  --output-json kissing_number_5/experiments/output/n41_direct_slsqp.json
```

For a rougher candidate, use `--refine smooth-slsqp`.  The input must contain
one five-coordinate point per line, or one comma-separated five-coordinate
token per point.  By default, only \(N=41,42,43,44\) is accepted.

The JSON schema has:

- `status`: the numerical-only warning;
- `software` and `input`, including the SHA-256 of the exact input bytes;
- `initial_analysis`;
- optionally `refinement.method`, `refinement.history`, and
  `refinement.analysis`.

Each analysis records the binary64 maximum inner product and its gap above
\(1/2\), norm error, positive Gram/frame eigenvalues, near-contact graph
statistics at the requested tolerance, and a binary64-only feasibility flag.

## Calibration

```bash
kissing_number_5/.venv/bin/python -m unittest -v \
  kissing_number_5/experiments/random_codes/test_numerical_tools.py
```

The \(D_5\) test should report 40 points, maximum inner product \(1/2\) to
binary64 precision, and five positive Gram eigenvalues equal to 8.

