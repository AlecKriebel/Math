# Hard active-contact surgery: numerical report

## Status

**NUMERICAL EVIDENCE ONLY — NOT A CONSTRUCTION CERTIFICATE, AN UPPER
BOUND, OR A RESOLUTION OF \(\tau(5)\).**

Seventeen deterministic nonsymmetric, non-grid trajectories were run for
\(N=41,42,43,44\).  No stored binary64 array had maximum inner product at
most \(1/2\).  Therefore exact-coordinate or directed-interval verification
was not triggered.

The search strictly improved the stored \(N=43\) input

\[
0.5247244770145227
 \longrightarrow
0.5247096018292908.
\]

This is an improvement of `1.487518523191067e-05` over the available input
array, not a new numerical record: round 10 reports a prior comparison value
`0.5247096018290212`, whose coordinates were not stored.  The new trajectory
numerically recovered that same basin to about \(2.7\cdot10^{-13}\).

## Mechanism

No log-sum-exp, \(p\)-norm, or other smooth approximation of the maximum is
used.  At every continuous iteration the program explicitly forms the
worst-edge band

\[
 E_\delta(X)=\{ij:\langle x_i,x_j\rangle\geq
 \max_{k<l}\langle x_k,x_l\rangle-\delta\}.
\]

Writing a tangent displacement in four coordinates per point, it solves the
hard Chebyshev linear program

\[
\begin{aligned}
\text{minimize }&s,\\
\langle x_i,x_j\rangle+
 D\langle x_i,x_j\rangle[d]&\leq m+s
 \qquad(ij\in E_\delta),\\
|d_{ik}|&\leq \rho,
\end{aligned}
\]

then retracts onto \((S^4)^N\) and accepts only after a literal all-pairs
scan.  The movable set alternates between all points and a greedy vertex
cover of the current worst-edge graph.  Separate one-point LP sweeps lower
incident order statistics even when a different edge holds the global
maximum.

Three contact-graph surgery mechanisms challenge each settled basin:

1. The active-contact Jacobian is formed explicitly.  Its nullspace is
   projected away from the ten infinitesimal \(O(5)\) rotations, and
   coordinated multi-point steps are tried along the remaining flex
   directions.
2. Entries above a proposed cap are clipped in the Gram matrix, followed by
   projection onto the PSD rank-five cone, row normalization, and another
   hard active-set settle.
3. Two to four stressed vertices from a graph cover are deleted.  Candidate
   reinsertions come from equal-contact intersections of five selected fixed
   points and fresh unrestricted Gaussian directions, followed by joint
   hard-LP refinement.

No symmetry, antipodality, lattice shell, prescribed graph, rationality, or
finite coordinate alphabet is imposed.

## Best independently recomputed arrays

The decimal maximum and hexadecimal field are exact descriptions of the
maximum returned by the canonical rowwise binary64 dot-product scan.  They
are not exact-real claims.

| \(N\) | best binary64 maximum | binary64 hexadecimal | gap above \(1/2\) | seed |
|---:|---:|:---|---:|---:|
| 41 | 0.5149946525121660 | `0x1.07ad610c4f2cap-1` | 0.0149946525121660 | 2026076642 |
| 42 | 0.5182411558622623 | `0x1.0956e79fbd437p-1` | 0.0182411558622623 | 2026076743 |
| 43 | 0.5247096018292908 | `0x1.0ca6bca7820a7p-1` | 0.0247096018292908 | 2026078844 |
| 44 | 0.5274711925359574 | `0x1.0e10b4430c512p-1` | 0.0274711925359574 | 2026076945 |

All four selected endpoints came from stored near misses.  The best of the
two fresh random paths at each cardinality were respectively

| \(N\) | best fresh-random endpoint |
|---:|---:|
| 41 | 0.5211388482909693 |
| 42 | 0.5273152521007856 |
| 43 | 0.5363573806503068 |
| 44 | 0.5423022512030853 |

At tolerance \(10^{-8}\) below each array's own maximum, the graph and Gram
diagnostics are:

| \(N\) | active edges | component sizes | literal maximizing pair(s) | Gram tail max abs |
|---:|---:|:---|:---|---:|
| 41 | 153 | \(35,1^6\) | `(11,21)` | \(2.98\cdot10^{-15}\) |
| 42 | 173 | \(40,1,1\) | `(1,25),(9,23)` | \(3.97\cdot10^{-15}\) |
| 43 | 169 | \(43\) | `(31,38)` | \(3.71\cdot10^{-15}\) |
| 44 | 182 | \(44\) | `(7,32)` | \(3.42\cdot10^{-15}\) |

The five eigenvalues of \(X^{\mathsf T}X\), recomputed independently, are

```text
N=41  7.892099139799012  7.978755189667489  7.978755189667496
      8.186173294652814  8.964217186213187
N=42  7.897396266328201  8.028965556568084  8.500063220041064
      8.680341958086066  8.893232998976583
N=43  8.397918540964284  8.411148321509100  8.412113667976127
      8.412113667982014  9.366705801568475
N=44  8.591207584335592  8.638240736552042  8.638240736552044
      9.059275580015976  9.073035362544353
```

The consolidated coordinate SHA-256 values are

```text
N=41  f6c22e89efd2fc94d108c1d23782ead87bed2d8e292718d3718a8a6deceee420
N=42  5cd9b961b89b28ec71074feef115d9f6393496ba0c4f9efc4ff1ec4d75416fe1
N=43  03fe9514e83b50160dfee22532cbd4369c6ef62676f0f72c7f669a2425a7200b
N=44  2136e998abb0208276840d6a7cd7cc10cfd7985e0004ec103c38dbf5e46e2af6
```

## Interpretation

The stored \(N=41,42,44\) endpoints survived all hard-LP, nullspace, Gram,
and deletion/reinsertion challenges unchanged.  This is evidence about
these particular basins only.  For example, the \(N=41\) active Jacobian had
24 nonrotational null directions in the first \(10^{-6}\) graph audit, yet
the tested finite steps returned to the old basin or to a worse one.
Consequently neither active-graph rigidity nor numerical stationarity may be
inferred as a universal property.

The \(N=43\) gain came from hard active-edge re-equilibration.  Its final
\(10^{-8}\) graph is connected with degree histogram

```text
5^8 6^12 7^2 9^6 10^8 11^6 12^1.
```

The result remains `0.0247096018292908` above the kissing threshold, so it
does not suggest an exact 43-point construction.

## Artifacts and independent audit

- `surgery_active_search.py`: discovery implementation.
- `surgery_portfolio.json`: first eight stored/random trajectories.
- `surgery_deep_stored_portfolio.json`: four deeper stored-basin challenges.
- `surgery_n43_deep_portfolio.json`: ten-cycle \(N=43\) polish.
- `surgery_deep_random_portfolio.json`: four second-seed random challenges.
- `surgery_best_configurations.json`: consolidated best coordinates and all
  graph/spectral diagnostics.
- `surgery_check_results.py`: independent checker that does not import the
  search program.
- `surgery_best_independent_check.json`: checker output for the consolidated
  artifact.
- `surgery_test_active_search.py`: six unit/regression tests.

The consolidated artifact SHA-256 is

```text
592f5ef1703788f06901fbc8b0b4cbed6e46e2493439bc484995f81a64f1dc1d
```

The checker re-normalizes each array, re-enumerates every pair, identifies
literal maximizing pairs, recomputes Gram spectra, reconstructs all
\(10^{-4},10^{-6},10^{-8}\) graphs, checks component and degree data, checks
coordinate hashes, rehashes every source portfolio, and verifies that the
consolidated selection is the minimum over all 17 stored runs.  It confirms
that no binary64 threshold hit occurred.  This remains a floating-point
integrity check, not interval arithmetic.

## Reproduction

The recorded environment is Python 3.14.6, NumPy 2.5.1, SciPy 1.18.0 on
`macOS-26.5.2-arm64-arm-64bit-Mach-O`.  From the repository root:

```sh
PY=./.venv/bin/python

$PY experiments/four_point_depth_projection/construction_active_search/surgery_active_search.py \
  --n 41 42 43 44 \
  --stored-seed 2026072501 --random-seed 2026072591 \
  --refine-iterations 28 --escape-cycles 2 \
  --random-candidates-per-point 3000 \
  --output experiments/four_point_depth_projection/construction_active_search/surgery_portfolio.json

$PY experiments/four_point_depth_projection/construction_active_search/surgery_active_search.py \
  --n 41 42 43 44 --origins stored \
  --stored-seed 2026073501 --refine-iterations 44 --escape-cycles 5 \
  --output experiments/four_point_depth_projection/construction_active_search/surgery_deep_stored_portfolio.json

$PY experiments/four_point_depth_projection/construction_active_search/surgery_active_search.py \
  --n 43 --origins stored --stored-seed 2026074501 \
  --refine-iterations 100 --escape-cycles 10 \
  --output experiments/four_point_depth_projection/construction_active_search/surgery_n43_deep_portfolio.json

$PY experiments/four_point_depth_projection/construction_active_search/surgery_active_search.py \
  --n 41 42 43 44 --origins random \
  --random-seed 2026073591 --refine-iterations 44 --escape-cycles 4 \
  --random-candidates-per-point 5000 \
  --output experiments/four_point_depth_projection/construction_active_search/surgery_deep_random_portfolio.json

$PY experiments/four_point_depth_projection/construction_active_search/surgery_consolidate.py \
  experiments/four_point_depth_projection/construction_active_search/surgery_portfolio.json \
  experiments/four_point_depth_projection/construction_active_search/surgery_deep_stored_portfolio.json \
  experiments/four_point_depth_projection/construction_active_search/surgery_n43_deep_portfolio.json \
  experiments/four_point_depth_projection/construction_active_search/surgery_deep_random_portfolio.json \
  --output experiments/four_point_depth_projection/construction_active_search/surgery_best_configurations.json

$PY experiments/four_point_depth_projection/construction_active_search/surgery_check_results.py \
  experiments/four_point_depth_projection/construction_active_search/surgery_best_configurations.json \
  --output experiments/four_point_depth_projection/construction_active_search/surgery_best_independent_check.json

$PY -m unittest \
  experiments.four_point_depth_projection.construction_active_search.surgery_test_active_search -v
```

The six tests pass.  The discovery trajectory can vary in its last bits
across BLAS or linear-program solver builds even with fixed seeds; the
checker makes exact claims only about the stored binary64 payload.
