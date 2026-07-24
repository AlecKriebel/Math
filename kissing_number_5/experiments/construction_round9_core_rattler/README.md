# Construction round 9: unrestricted core/rattler challenge

## Status

**NUMERICAL EVIDENCE ONLY — NOT A CONSTRUCTION CERTIFICATE OR AN UPPER
BOUND.**

No 41-, 42-, 43-, or 44-point code with maximum inner product at most
\(1/2\) was found.  The best \(N=41\) value remains

```text
0.5149946525121668
```

and is about `0.0149946525121668` above the kissing threshold.  This is far
too large to be a rounding ambiguity, but it is not a lower bound on any
unsearched configuration.

The portfolio used no symmetry, antipodality, lattice, tight-frame, or
prescribed-contact-graph constraint.  Its final coordinates and all
intermediate audit data are in
[`results/core_rattler_portfolio.json`](results/core_rattler_portfolio.json).

## Results

The inherited inputs were the best arrays in the round-6 portfolio.  Changes
of \(10^{-14}\) or less after SQP are reported faithfully but treated as
solver-last-bit changes, not new numerical records.

| \(N\) | inherited maximum | round-9 stored best | gap above \(1/2\) | best label | \(10^{-8}\) active components |
|---:|---:|---:|---:|:---|:---|
| 41 | 0.5149946525121668 | 0.5149946525121668 | 0.0149946525121668 | inherited | \(35,1^6\) |
| 42 | 0.5182411558622642 | 0.5182411558622623 | 0.0182411558622623 | delete/reinsert 8 | \(40,1^2\) |
| 43 | 0.5247244770145403 | 0.5247244770145227 | 0.0247244770145227 | delete/reinsert 3 | \(43\) |
| 44 | 0.5274711925359574 | 0.5274711925359574 | 0.0274711925359574 | inherited | \(44\) |

The repository's public-code comparison records
`0.5247096018290212` for \(N=43\) and `0.5274577123235323` for \(N=44\).
Those coordinate arrays were not present among the stored round-6 inputs.
They remain better than the round-9 outputs; this experiment therefore makes
no global numerical-record claim.

The five positive Gram eigenvalues of the stored best arrays are:

```text
N=41  7.884359361782769  7.992145992231188  7.992145992231196
      8.167199729535618  8.964148924219227
N=42  7.897396266328203  8.028965556568084  8.500063220041064
      8.680341958086070  8.893232998976590
N=43  8.398831498874179  8.411565372183214  8.411565372183517
      8.411565372184372  9.366472384574730
N=44  8.591207584335590  8.638240736552044  8.638240736552046
      9.059275580015976  9.073035362544351
```

The largest absolute numerical eigenvalue outside the top five is
`3.99e-15`.

## What was new in this round

### Complete floating-point one-point cap insertion

For a fixed point set \(P\) whose convex hull contains the origin in its
strict interior,

\[
 \min_{\|y\|=1}\max_{p\in P}\langle p,y\rangle
\]

is the radius of the largest origin-centered ball contained in
\(\operatorname{conv}(P)\).  If the hull facets have outward unit equations
\(\langle n_j,z\rangle\le b_j\), this radius is
\(\min_j b_j\).  Thus a scan of every convex-hull facet normal solves the
one-point insertion problem globally.

The search implements this reduction with Qhull and then recomputes every
support value by a literal binary64 dot-product scan.  All 956 recorded facet
audit entries (including repeated beam-path prefixes) had the origin strictly
inside the hull.  The largest discrepancy between a facet distance and its
recomputed support was
`9.99e-15`.

This completeness statement is only about the mathematical reduction and
the returned floating-point hull.  Qhull arithmetic is not directed interval
arithmetic.  Moreover, choosing a sequence of several insertions remains a
width-5 beam heuristic with four facet choices per state; it is not a global
solution of the multipoint replacement problem.

### Deletion/reinsertion, block moves, and all-coordinate release

For each \(N=41,42,43,44\), every block size 2 through 8 was tested.  Deletion
sets rotate among:

- high active-gradient stress;
- contact-connected high-stress clusters;
- mixtures of contact-free/low-degree rows and stressed core rows.

Each replacement uses complete one-point facet scans, a multipoint beam,
joint movable-block log-sum-exp continuation, direct block epigraph SQP, and
then releases all \(N\) rows through temperature continuation, an
active-constraint bundle method, and direct all-pairs epigraph SQP.

The portfolio also used four-replica threshold-energy exchange at
temperatures

```text
2e-5, 8e-5, 3.2e-4, 1.28e-3
```

with asymmetric 2--8 vertex moves, 320 sweeps, and two fresh Gaussian starts
per cardinality.  This targets a different landscape from ordinary
log-sum-exp continuation.

### The 35-core plus six-rattler structure

At tolerance \(10^{-6}\), the inherited \(N=41\) active graph has 153 edges,
one 35-vertex component, and six isolated vertices.  The next inactive
core-pair value is separated from the maximum by

```text
0.006872737556740893.
```

An exact bitset branch-and-bound computation on this *finite extracted graph*
finds:

```text
maximum independent-set size = 9
minimum vertex-cover size     = 26
branch nodes                  = 1473
```

Consequently, locking the undeleted coordinates while replacing only 2--8
core vertices cannot lower the inherited maximum: at least one old active
edge must remain.  This explains why cap replacement by itself repeatedly
looks inert.  Improvement can occur only after the subsequent all-coordinate
release changes the 35-point core.

This is an exact statement about the stored integer graph, not a theorem
about an unknown extremal spherical code.  The graph was extracted from
floating coordinates, although its active/inactive gap makes the extraction
numerically well separated.

The all-coordinate challenges did not break the basin:

- a scale-0.12 tangent quake of all 35 core vertices returned to the identical
  active edge set and maximum;
- scales 0.25, 0.50, and 0.90 reached different active graphs (Jaccard
  similarities `0.2614`, `0.1984`, and `0.1282`) but worse maxima
  `0.5196238`, `0.5155656`, and `0.5192270`;
- five independently optimized random 35-point cores reached maxima from
  `0.4795333` to `0.4840402`, but after six insertions and full release their
  best 41-point value was only `0.5185085142027626`;
- an asymmetric 35-root subset of \(D_5\), followed by six insertions and
  full release, reached `0.5220692609969378`;
- replica exchange from two fresh asymmetric 41-point Gaussian clouds reached
  `0.5175227330746383` and `0.5168567486087297`; the inherited replica
  returned to `0.5149946525121682`.

The larger quakes therefore genuinely left the persistent contact basin,
but only for worse basins.

## Numerical rigor and threshold policy

Every accepted or reported configuration is normalized and then checked by
scanning all \(\binom N2\) pairs.  “Complete” and “exact” in the search log
refer only to combinatorial facet enumeration or literal binary64 scans, not
to exact real arithmetic.

If a floating candidate had reached a recomputed maximum at most \(1/2\), the
search would have marked it

```text
THRESHOLD HIT — UNVERIFIED; EXACT/INTERVAL RECONSTRUCTION REQUIRED
```

and the independent checker would reject the portfolio unless a separate
exact or directed-interval certificate were attached.  That trigger did not
fire.  Therefore no exact-coordinate reconstruction was attempted and no
lower-bound construction is claimed.

## Reproduction

From the `kissing_number_5` directory:

```sh
python3 -m venv /tmp/kissing5-round9-venv
/tmp/kissing5-round9-venv/bin/pip install \
  -r experiments/construction_round9_core_rattler/requirements.txt

PY=/tmp/kissing5-round9-venv/bin/python

$PY -m experiments.construction_round9_core_rattler.core_rattler_search \
  --input experiments/construction_round6_bundle/results/bundle_portfolio.json \
  --output /tmp/core_rattler_portfolio.json \
  --n 41 42 43 44 --seed 2026072390 \
  --hole-samples 2048 --hole-starts 4 \
  --search-iterations 180 --replica-sweeps 320 --random-starts 2 \
  --beam-width 5 --facet-choices 4 --core-random-starts 5
```

The released run took 161.76 seconds on macOS arm64 with Python 3.14.6,
NumPy 2.5.1, and SciPy 1.18.0.  Fixed seeds do not guarantee identical last
bits across BLAS, Qhull, or SQP implementations.

Run the independent checker and tests:

```sh
$PY -m experiments.construction_round9_core_rattler.check_results \
  experiments/construction_round9_core_rattler/results/core_rattler_portfolio.json

$PY -m unittest \
  experiments.construction_round9_core_rattler.test_core_rattler_search -v
```

The checker does not import the discovery code.  It independently recomputes
all norms, pairs, quantiles, Gram spectra, active graphs, connected
components, and finite-graph independence/vertex-cover results.  The six
tests also check analytic gradients and the complete facet scan on the
five-dimensional cross polytope.

## Artifact hashes

```text
55aa13f81cc305d5007f840875623547625167b1e6f762092f3f80f7154e5f9c  results/core_rattler_portfolio.json
e65d1a16d5a29128e7f2ae9c12ecbd129d3e742f16a646bdc3e91dedaaf8da17  core_rattler_search.py
17c49974d4a21d2fca21482c110155249109aee2aaf295a9f4997b0cdae5fd08  check_results.py
e5666fea829d5e9b2030cae507d946261fb18e36166f2cef81e1af3f52a33d22  test_core_rattler_search.py
56b0f6a2aefb16d057a33511ef52b3eeae35b7debe92536121fa5749d460a5cd  requirements.txt
```
