# Construction round 7: D6 dimension-compression homotopy

## Status

**NUMERICAL EVIDENCE ONLY — NOT A CONSTRUCTION CERTIFICATE OR AN UPPER
BOUND.**

Twenty independent paths began with feasible 41--44 point codes on
\(S^5\), forced the sixth covariance eigenvalue to zero, and then polished
the resulting points on \(S^4\).  No path remained below maximum inner
product \(1/2\).  All 20 encountered a positive threshold barrier at the
same homotopy stage.

This is evidence about one compression mechanism, not evidence that every
six-to-five-dimensional deformation must cross the same barrier.

## Exact and random six-dimensional starts

For each \(N=41,42,43,44\), four starts are subsets of the 60 normalized
\(D_6\) roots

\[
\{(\epsilon_i e_i+\epsilon_j e_j)/\sqrt2:
  1\le i<j\le6,\ \epsilon_i,\epsilon_j\in\{-1,1\}\}.
\]

The four selection rules are:

- a uniform asymmetric subset;
- randomly selected antipodal pairs, with one extra point for odd \(N\);
- a random-height asymmetric slice;
- the best of 180 random subsets under a covariance-diversity score.

The result file stores the four integer labels
`[i,j,epsilon_i,epsilon_j]` for every selected point.  The independent
checker reconstructs each coordinate and checks every pair exactly: its
inner product is an integer numerator divided by two, and the numerator is
at most one.  Thus all 16 D6 starts are exact feasible \(S^5\) codes even
though their displayed binary64 maxima can be
`0.5000000000000001`.

One additional start at each cardinality is a completely released random
six-dimensional code.  Its independently recomputed maxima are:

| \(N\) | random \(S^5\) start maximum |
|---:|---:|
| 41 | 0.3911697853735066 |
| 42 | 0.4000000025529210 |
| 43 | 0.4059666990264317 |
| 44 | 0.4082482914962547 |

These random coordinates have large binary64 margins below \(1/2\), but
they are numerical rather than exact algebraic certificates.

## Compression homotopy

For an \(N\times6\) unit-row matrix \(X\), the search minimizes

\[
\operatorname{LSE}_{\beta}
   \{\langle x_i,x_j\rangle:i<j\}
+\mu\,\frac{\lambda_{\min}(X^{\mathsf T}X)}N.
\]

The gradient of the second term uses a bottom covariance eigenvector
\(q\):

\[
\frac{2\mu}{N}(Xq)q^{\mathsf T},
\]

followed by tangent projection onto \((S^5)^N\).  The continuation uses

```text
mu:    0, .01, .03, .1, .3, 1, 3, 10, 30, 100, 300
beta: 36, 54, 81, 122, 183, 275, 412, 618, 927, 1390, 2085
```

At five stages a second candidate is made by compressing along a random
combination of the bottom two eigendirections and adding a tangent
perturbation.  Both candidates are relaxed, and the lower homotopy
objective continues.  Accepted branch counts range from zero to four per
path, so the run did not merely trace a single fixed collapse axis.

After the last stage the bottom covariance eigenvector is discarded.
Every row is renormalized in its five-dimensional orthogonal complement,
then relaxed by high-temperature smooth-max continuation and a direct
epigraph SLSQP solve.  Previous round-5/6 coordinates are never read by
this program.

Every selected-stage coordinate matrix, spectrum, maximum, branch
decision, and solver history is stored.

## Repeatable numerical barrier

All 20 paths behaved in the same coarse way:

| collapse weight | range of \(\lambda_6/N\) over all paths | range of maximum inner product |
|---:|---:|---:|
| 1 | 0.0625659 -- 0.1198314 | 0.4001688 -- 0.4520211 |
| 3 | \(1.98\cdot10^{-6}\) -- 0.0104472 | 0.5108276 -- 0.5716524 |
| 10 | \(3.81\cdot10^{-9}\) -- \(1.61\cdot10^{-6}\) | 0.5241111 -- 0.5539101 |
| 300 | 0 -- \(1.42\cdot10^{-12}\) | 0.5224443 -- 0.5439494 |

Every path first crossed above \(1/2\) at weight 3.  First-crossing ranges
by cardinality were:

| \(N\) | first-crossing maximum range |
|---:|---:|
| 41 | 0.5108275846 -- 0.5483233968 |
| 42 | 0.5486955539 -- 0.5716523778 |
| 43 | 0.5520225841 -- 0.5573926915 |
| 44 | 0.5654225879 -- 0.5712274139 |

The later relaxation reduces some of the spike, but never returns to
\(1/2\).  The last six-dimensional spectra have
\(\lambda_6/N\le1.42\cdot10^{-12}\), including several values rounded to
zero by the eigensolver.  Immediate rank-five projection changes the
maximum only in the displayed last bits, showing that the positive gap is
already present before projection rather than caused by dropping a
substantial coordinate.

## Final five-dimensional results

| \(N\) | best final maximum | gap above \(1/2\) | source | seed | \(10^{-8}\) active edges |
|---:|---:|---:|:---|---:|---:|
| 41 | 0.5207137808832133 | 0.0207137808832133 | antipodal-pair D6 subset | 1015667700 | 155 |
| 42 | 0.5254288787731305 | 0.0254288787731305 | uniform D6 subset | 17257302 | 159 |
| 43 | 0.5284653908755059 | 0.0284653908755059 | uniform D6 subset | 1871898867 | 163 |
| 44 | 0.5331536680973610 | 0.0331536680973610 | covariance-diverse D6 subset | 894992812 | 167 |

No final point set is feasible, and none improves the established
round-5/6 numerical records.

## Post-search comparison

Only after the compression portfolio was written,
`compare_prior_basins.py` read the round-5 and round-6 endpoints.  It
compares sorted full pair-inner-product vectors, an
isometry-and-relabeling invariant descriptor.  None of the 20 round-7
endpoints matches a previous numerical distance distribution at tolerance
\(10^{-7}\).  The smallest descriptor RMS distances are:

| \(N\) | minimum RMS distance to a prior basin |
|---:|---:|
| 41 | 0.0111602581 |
| 42 | 0.0109874580 |
| 43 | 0.0142278466 |
| 44 | 0.0116480483 |

Thus this homotopy reached numerically different, generally worse local
basins rather than merely reproducing the round-5 active cores.

## Artifacts

| file | SHA-256 |
|:---|:---|
| [`compression_portfolio.json`](results/compression_portfolio.json) | `902a65a6d87f0662d785280ba08cc8852996225a404a93f8ba587a00556b3de2` |
| [`posthoc_prior_comparison.json`](results/posthoc_prior_comparison.json) | `884ae4e52e6f6a124e5c805f9e83470a734cd1efcd73a8637578c1556806e126` |

The portfolio contains 20 paths and took 46.81 seconds on macOS arm64 with
Python 3.14.6, NumPy 2.5.1, and SciPy 1.18.0.  Seeds are derived
deterministically from master seed `2026072370` and stored on every path.
Elapsed-time and platform fields make whole-file hashes
platform-dependent even with fixed seeds.

## Reproduction

From the repository root:

```sh
python3 -m venv /tmp/kissing5-round7-venv
/tmp/kissing5-round7-venv/bin/pip install \
  -r kissing_number_5/experiments/construction_round7_d6_compression/requirements.txt

PY=/tmp/kissing5-round7-venv/bin/python
MOD=kissing_number_5.experiments.construction_round7_d6_compression

$PY -m $MOD.compress_d6 \
  --n 41 42 43 44 --seed 2026072370 --iterations 150 \
  --output \
  kissing_number_5/experiments/construction_round7_d6_compression/results/compression_portfolio.json
```

Run the post-search comparison:

```sh
$PY -m $MOD.compare_prior_basins \
  --round7 \
  kissing_number_5/experiments/construction_round7_d6_compression/results/compression_portfolio.json \
  --round5 \
  kissing_number_5/experiments/construction_round5_population/results/population_portfolio.json \
  kissing_number_5/experiments/construction_round5_population/results/population_targeted_n43_n44.json \
  --round6 \
  kissing_number_5/experiments/construction_round6_bundle/results/bundle_portfolio.json \
  --output \
  kissing_number_5/experiments/construction_round7_d6_compression/results/posthoc_prior_comparison.json
```

Verify the released coordinates and histories independently:

```sh
$PY -m $MOD.check_compression \
  kissing_number_5/experiments/construction_round7_d6_compression/results/compression_portfolio.json

$PY -m unittest \
  kissing_number_5.experiments.construction_round7_d6_compression.test_compress_d6 \
  -v
```

The checker imports no search code.  It recomputes every stored norm,
pairwise maximum, active graph, Gram spectrum, covariance spectrum,
selected-stage sixth-eigenvalue fraction, and projection diagnostic.  For
the 16 D6 starts it additionally reconstructs every point from integer
labels and checks all pair inequalities exactly.  These checks establish
artifact integrity only; they neither certify a new kissing configuration
nor exclude an unsearched compression path.
