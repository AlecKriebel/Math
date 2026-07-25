# Construction round 6: Riemannian active-bundle search

## Status

**NUMERICAL EVIDENCE ONLY — NOT A CONSTRUCTION CERTIFICATE OR AN UPPER
BOUND.**

This 26-trajectory search found no 41-, 42-, 43-, or 44-point spherical
code with maximum inner product at most \(1/2\).  Its best values reproduce
the inherited round-5 basins but do not improve them.  In particular, the
best \(N=41\) value is still about `0.0149946525` above \(1/2\).

The released binary64 points are near misses, not exact configurations.
Nothing here excludes a better unsearched basin.

## Search mechanism

This round targets the nonsmooth minimax objective directly:

\[
    \Phi(X)=\max_{i<j}\langle x_i,x_j\rangle,\qquad
    X\in(S^4)^N.
\]

Each trajectory has three parts.

1. A Riemannian log-sum-exp continuation with inverse temperatures
   `24, 72, 216, 648, 1944, 5832` enters a contact basin.
2. At the current point, the program forms a bundle of the largest pair
   functions.  If
   \(a_e=f_e(X)-\Phi(X)\) and \(g_e\) is the exact product-sphere tangent
   gradient of pair \(e\), it solves the proximal model

   \[
       \min_d \max_e(a_e+g_e^\mathsf Td)
                  +\frac{\lVert d\rVert^2}{2\mu}.
   \]

   Its simplex dual is solved by an away-step Frank--Wolfe active-set
   algorithm.  The tangent proposal is accepted or rejected against the
   *actual*, nonsmooth maximum after a product-sphere retraction, and the
   trust radius is updated from predicted/actual decrease.
3. Four deterministic tangent facet-escape kicks of sizes
   `0.006, 0.016, 0.035, 0.07` are applied.  Low-contact-degree rows move
   farther.  Every escaped basin is continued even when it is uphill, so
   later phases can cross a different active-contact complex.

This is not the inverse-chord population method of round 5 and does not use
the final SLSQP epigraph polish from that round.  The bundle model is an
ordinary floating-point optimization model; “exact maximum” means that
acceptance is evaluated with `max` over every pair, not that the computation
uses exact arithmetic.

## Portfolio

The fixed master seed is `2026072360`.  For each cardinality, initialization
uses the best coordinate array found independently in each supplied round-4
or round-5 input, an asymmetric tangent perturbation of the best inherited
array, a D5 configuration with maximin sampled insertions, and two fresh
asymmetric Gaussian starts.  A redundant inherited input is retained when
two source files happen to encode the same basin; this checks that source
parsing and normalization do not change the result.

The run used 220 L-BFGS iterations per smooth stage, 36 nonsmooth bundle
iterations per phase, and four facet escapes.

| \(N\) | trajectories | best maximum | gap above \(1/2\) | best trajectory seed | \(10^{-8}\) active edges |
|---:|---:|---:|---:|---:|---:|
| 41 | 6 | 0.5149946525121669 | 0.0149946525121669 | 38979917 | 153 |
| 42 | 6 | 0.5182411558622642 | 0.0182411558622642 | 327880762 | 172 |
| 43 | 7 | 0.5247244770145402 | 0.0247244770145402 | 1240425587 | 172 |
| 44 | 7 | 0.5274711925359574 | 0.0274711925359574 | 1794435750 | 182 |

The best-point diagnostics are:

| \(N\) | \(10^{-8}\) degree histogram | component sizes | pairs below \(-1/2\) | min convex active-gradient norm |
|---:|:---|:---|---:|---:|
| 41 | \(0^6,8^{18},9^{10},10^6,12^1\) | \(35,1^6\) | 114 | \(3.31\cdot10^{-8}\) |
| 42 | \(0^2,3^1,6^4,7^4,8^7,9^{12},10^8,11^3,12^1\) | \(40,1^2\) | 121 | \(1.15\cdot10^{-7}\) |
| 43 | \(5^8,6^6,7^8,10^{20},12^1\) | \(43\) | 119 | \(8.20\cdot10^{-8}\) |
| 44 | \(6^4,7^4,8^{16},9^{16},10^4\) | \(44\) | 148 | \(1.66\cdot10^{-7}\) |

The convex-gradient norms are numerical Clarke-stationarity diagnostics,
not rigorous lower bounds on possible descent.

## The \(N=41\) basin

The best result remains the 35-point active core with six numerical
rattlers.  Its four escape endpoints had maximum inner products

```text
0.5149975050471463
0.5149968439759895
0.5150022910520059
0.5149962329122209
```

and were therefore all rejected as records.  At tolerance \(10^{-6}\),
successive endpoint contact-graph Jaccard similarities were

```text
0.862745, 1.000000, 0.963235, 0.963235, 0.916667
```

starting with the inherited seed.  Thus finite perturbations repeatedly
return to a very similar 35-point contact core, although the exact
tolerance graph is not completely invariant.  This is evidence for a
persistent local basin only; it does not imply that every 41-point search
must enter it.

The separate four-point-supported hyperplane probe accounts for all
\(\binom{41}{4}=101270\) supports: 100971 full-rank supports were evaluated
and 299 numerically rank-deficient supports were retained as skipped.
The minimum observed strict side has 11 points.  The split histogram
contains 3523 instances classified as `11/19/11` and two as `11/18/12` at
tolerance \(10^{-10}\).  The latter are selected as the stored
closed-side diagnostic (`11 + 18 = 29`); their next nonboundary dot product
is only about \(1.03\cdot10^{-10}\), so the distinction is explicitly
numerical.  In either classification the near miss does not challenge the
rigorous necessary open-halfspace occupancy of seven for a hypothetical
41-code.

## Artifacts

| file | contents | SHA-256 |
|:---|:---|:---|
| [`bundle_portfolio.json`](results/bundle_portfolio.json) | 26 trajectories, every best coordinate array, Gram spectrum, pair quantiles, contact graphs, bundle histories, deterministic seeds | `d5f0e950027b9aa05105663069d003e6ebf0bc8f7366a93f63c9fc318eb4ec86` |
| [`halfspace_depth_n41.json`](results/halfspace_depth_n41.json) | numerical four-point hyperplane enumeration bound to the portfolio hash | `71f47f8563d2eccdfe289c32b802c8622be643243202fc3ef2bb4ac52b7ab9fe` |

The recorded run took 222.05 seconds on macOS arm64 with Python 3.14.6,
NumPy 2.5.1, and SciPy 1.18.0.  Whole-file output hashes include elapsed
time and platform metadata; fixed random seeds do not promise identical
last bits across BLAS implementations.

The inherited inputs and their recorded hashes are:

```text
c41781a5f1d33f24738620811646412d7b255bec94b913404bfeba19fd91036f  construction_round4_surgery/results/contact_surgery_portfolio.json
37ee2140585c18a329a00f79038a0d7bf9e9df51d7685405410ade2d32d58e82  construction_round5_population/results/population_portfolio.json
ab26f6cd16a769bec4137983f766c9ba4af544ed0ad3b0491ed7563447ba3c81  construction_round5_population/results/population_targeted_n43_n44.json
```

## Reproduction and independent integrity check

From the repository root:

```sh
python3 -m venv /tmp/kissing5-round6-venv
/tmp/kissing5-round6-venv/bin/pip install \
  -r kissing_number_5/experiments/construction_round6_bundle/requirements.txt

PY=/tmp/kissing5-round6-venv/bin/python
MOD=kissing_number_5.experiments.construction_round6_bundle.bundle_search
BASE=kissing_number_5/experiments

$PY -m $MOD --n 41 42 43 44 --seed 2026072360 \
  --inherit \
    $BASE/construction_round4_surgery/results/contact_surgery_portfolio.json \
    $BASE/construction_round5_population/results/population_portfolio.json \
    $BASE/construction_round5_population/results/population_targeted_n43_n44.json \
  --random-starts 2 --smooth-iterations 220 \
  --bundle-iterations 36 --escapes 4 \
  --output /tmp/bundle_portfolio.json \
  --depth-output /tmp/halfspace_depth_n41.json
```

Run the independent checker, which does not import the search implementation:

```sh
$PY -m kissing_number_5.experiments.construction_round6_bundle.check_bundle \
  kissing_number_5/experiments/construction_round6_bundle/results/bundle_portfolio.json \
  --depth \
  kissing_number_5/experiments/construction_round6_bundle/results/halfspace_depth_n41.json

$PY -m unittest \
  kissing_number_5.experiments.construction_round6_bundle.test_bundle_search \
  -v
```

The checker independently recomputes row norms, every pairwise inner
product, maxima and minima, Gram eigenvalues, pair quantiles, deep-negative
counts, active edge lists, contact degrees, connected components, and edge
hashes.  It also checks that the depth artifact is hash-bound to the
portfolio and re-enumerates the full \(\binom{41}{4}\) numerical split
histogram.  These are binary64 integrity checks only and do not certify
feasibility or nonexistence.
