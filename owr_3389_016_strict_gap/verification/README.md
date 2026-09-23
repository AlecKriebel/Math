# Exact finite verification

Run from the package root with Python 3.10 or later; no third-party packages are needed:

```sh
python3 verification/verify.py
```

The script writes deterministic `results.json` next to itself. Use `--output PATH`
to choose another location. All eigenvalues, coefficients, identities, margins,
and comparisons use `fractions.Fraction`; no floating-point tolerance is used.
A failed check raises an error and exits unsuccessfully, including under `python3 -O`.
The recorded run passes 7,016 checks over 1,312 box/`J` cases, including 600 zero
gaps and 12 cases where `E_(J+1)` is still the ground energy. An optimized
`python3 -O` run produces byte-identical JSON.

The checks cover:

- The coefficients and completed square of
  `Q(t) = mean((t-E)^2 - (4/n)(t-E)E) = (t-M1)^2-D`,
  where `M1=(n+2)mean(E)/n` and
  `D=M1^2-(n+4)mean(E^2)/n`.
- Internal ordered-pair cancellation, zero contributions at a repeated threshold,
  the full moment expansion, and the sign of the nonnegative spectral remainder.
  Explicit symmetric rational matrices are used, with empty lower/upper blocks,
  repeated eigenvalues, and thresholds both at and between spectral levels.
- Exact spectra of intervals and boxes in dimensions 1–4, including rational
  anisotropic lengths and disjoint identical copies. Eigenvalues have `pi^2`
  scaled out: `E=sum((m_i/L_i)^2)` for positive integer indices. All `J` in each
  reported range are checked, including zero gaps and ground-state multiplicity.
  Ground energies and multiplicities, known square/hypercube prefixes, and
  independent closed-form interval formulas also check the enumeration.
- Independent enumeration after multiplying all lengths by `7/3`; energies
  scale by `(3/7)^2`, and `D` and the strict-gap margin by `(3/7)^4`.
- Deliberate wrong-second-moment and wrong-sign mutations, which must be detected.

**Completeness of every box spectrum is certified.** After enumerating all
`1 <= m_i <= K`, every omitted mode has energy at least

```text
min_i ((K+1)^2/L_i^2 + sum_{h != i} 1/L_h^2).
```

The script increases `K` until the last required eigenvalue is strictly below
this bound. Thus the first `J+1` values include all required multiplicities.
The output records the cutoff, last required eigenvalue, omitted-mode lower
bound, tested `J` range, and smallest normalized positive margin for each box.

**Scope:** these are checkable finite algebra and model-spectrum checks, not a
proof for arbitrary bounded open sets. The synthetic matrices are not claimed
to realize a Dirichlet Laplacian. Indeed, the script explicitly checks the
finite-dimensional trace obstruction to imposing the coordinate first-moment
sum rule on every row. The analytic sum rules, infinite-series convergence,
domain arguments, and strictness argument require the accompanying proof.
