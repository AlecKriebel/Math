# Numerical N41 probes from the thirteen exact K40 completions

## Status

**NUMERICAL EVIDENCE ONLY — NOT A CERTIFICATE.**

No run found a 41-point spherical code.  The best recomputed maximum inner
product was

\[
0.5213989457472671>1/2.
\]

Failure of these local optimizers is not an obstruction, and none of the
stored floating-point coordinate arrays is claimed as an exact
configuration.

## Portfolio

The exact classification certificate supplies thirteen K40 starts: two
stored completions are \(D_5\) and eleven are \(L_5\).  Two distinct
symmetry-breaking challenges were run from every labeled completion, with a
different deterministic seed for each of the 26 runs.

1. **Insert and release.**  With all 40 exact points fixed, a multistart
   epigraph solve searched for a point minimizing its maximum inner product
   with the K40.  The resulting K41 was perturbed independently in every
   tangent space, and then all 41 points were released.
2. **Replace one by two and release.**  A seed-dependent vertex was deleted,
   two points were inserted sequentially by fixed-core epigraph solves, all
   41 points were independently perturbed, and then every point was
   released.

The unrestricted release used log-sum-exp stages with
\(\beta=24,64,160,400,1000\), followed by a literal minimax epigraph SLSQP
solve with all 41 norm equalities and all 820 pair inequalities.  Tangent
perturbation amplitudes ranged from 0.02625 to 0.04375.  These smooth and
floating-point choices are discovery mechanisms only.

For direct insertion into an intact \(D_5\) or \(L_5\), every multistart run
returned a fixed-core maximum between
0.6324555320336760 and 0.6324555320336770.  This numerical value resembles
\(\sqrt{2/5}\), but this experiment does not certify a covering-radius
theorem.  In the replacement mode, the first insertion can simply recover
the deleted point with maximum approximately \(1/2\); the second insertion
returns to the same approximately 0.63246 bottleneck.

## Outcomes

All 26 final epigraph solves reported success, but their independently
recomputed maxima remained above \(1/2\).  Rounded to twelve decimal places,
the outcomes landed in three recurring local basins:

| Maximum inner product | Runs |
|---:|---:|
| 0.521398945747 | 9 |
| 0.522069260997 | 4 |
| 0.524778240204 | 13 |

The best run was the insert-and-release challenge from L5-classified atom
41, with seed 1,315,585.  For context, the repository's pre-existing N41
numerical benchmark has recomputed maximum
0.514994652512166 and file SHA-256
`c54b38d8216bf76a79c57119fc46245811188e1de05c840c68a33cec9b7fe1b0`.
Thus the fresh K40-seeded portfolio did not improve the existing near miss.

The recurrence of three basins across relabelings and across both surgery
modes is a useful search diagnostic, not mathematical evidence that those
basins are globally optimal.

## Reproduction and checking

The result file
`n41_probe_results.json` records package versions, all parameters, every
random seed, solver histories, input/final diagnostics, and all final
coordinates.  Its SHA-256 is

```text
2049ff1827e1f30298bf9a289be9773e498dd1f0dc4c5adb24f7a104c1c99465
```

Reproduce the portfolio:

```text
PYTHONPATH=. .venv/bin/python experiments/centered_quarter_k6_rank/k11/maximal_extension/construction_probe/search.py experiments/centered_quarter_k6_rank/k11/maximal_extension/construction_probe/n41_probe_results.json
```

Independently recompute all stored input, perturbed-start, and final
coordinate diagnostics:

```text
PYTHONPATH=. .venv/bin/python experiments/centered_quarter_k6_rank/k11/maximal_extension/construction_probe/check_results.py
PYTHONPATH=. .venv/bin/python -m unittest -v experiments/centered_quarter_k6_rank/k11/maximal_extension/construction_probe/test_results.py
```

The checker validates the numerical-only status, source hash, complete
13-atom by 2-mode portfolio, coordinate hashes, norms, all pair maxima,
violation counts, quantiles, and Gram spectra.  It also checks continuity of
the optimization history and rejects altered coordinates, best-run
metadata, and file hashes.  The checker remains active under `python -O`.
