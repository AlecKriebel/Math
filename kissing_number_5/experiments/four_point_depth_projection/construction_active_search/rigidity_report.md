# Active-rigidity soft-mode construction search

Status: **NUMERICAL EVIDENCE ONLY — no exact 41–44 point kissing
configuration was found.**

## Result

The search applied 102 deterministic contact-framework escapes to stored
five-dimensional near misses.  It did not improve the \(N=41\) or \(N=42\)
baselines and did not produce any array whose maximum inner product is at
most \(1/2\).

It did cross contact basins for \(N=43\) and \(N=44\).  Starting only with
the weaker coordinate arrays available in this repository, it recovered the
stronger comparison values that earlier reports quoted without storing their
coordinates:

| \(N\) | input maximum | best recomputed maximum |
|---:|---:|---:|
| 41 | 0.51499465251216603 | 0.51499465251216603 |
| 42 | 0.51824115586226238 | 0.51824115586226238 |
| 43 | 0.52472447701452274 | 0.52470960182901927 |
| 44 | 0.52747119253595742 | 0.52745771232353222 |

The last digits are binary64 diagnostics, not exact-real claims.  All four
values exceed \(1/2\), so none is a kissing configuration.

## Mechanism

For a point cloud \(X=(x_1,\ldots,x_N)\), the search first takes all pairs
within \(10^{-8}\) of its literal maximum.  The corresponding contact row
for \(ij\) is the linear functional

\[
  (u_1,\ldots,u_N)\longmapsto
  \langle u_i,x_j\rangle+\langle x_i,u_j\rangle .
\]

Unit-sphere tangencies \(\langle u_i,x_i\rangle=0\) are included, and the ten
velocities induced by infinitesimal \(O(5)\) rotations are quotiented out.
Singular vectors of this constrained active-contact matrix expose genuine or
nearly singular multi-point modes.  Finite signed steps along those modes
are retracted rowwise to \(S^4\).

The \(N=41\) endpoint has a special structure: its maximum graph consists of
a 35-vertex component and six isolated rows.  In binary64 rank arithmetic,
the 35-point component has 153 active edges and tangent rigidity rank 130,
which is \(4\cdot35-10\).  Thus its only infinitesimal equality flexes are
the ten ambient rotations.  Each of eight deterministic trials deletes 24
contact rows, leaving 129 rows and exposing one non-rotational flex after
rotations are removed.  Both signs at scales \(0.03,0.15,0.40\) were tested.
All 48 escaped clouds returned to the same \(0.514994652512166\) basin.

As a separate diagnostic, `rigidity_stress_probe.py` solves

\[
 B w=0,\qquad \sum_e w_e=1,\qquad w_e\geq t
\]

for the tangent contact-gradient matrix \(B\) of that 35-point core.  HiGHS
found a fully positive numerical equilibrium stress with

```text
153 edges
minimum weight             0.0011269047923961543
equilibrium residual       6.16e-15
tangent gradient rank      130
stress-space dimension      23
```

This helps explain the attraction of the basin.  It is not an exact stress
certificate and proves neither local nor global optimality.

Every escaped cloud is polished by the direct epigraph problem

\[
\begin{aligned}
  \min\ &t,\\
  \langle x_i,x_j\rangle&\leq t &&(i<j),\\
  \lVert x_i\rVert^2&=1 &&(1\leq i\leq N),
\end{aligned}
\]

using analytic Jacobians and SLSQP.  Unlike a log-sum-exp or \(p\)-norm
continuation, the polishing problem contains every literal pair inequality.
The solver is still heuristic: a successful local status is not a
certificate of global optimality.

## Deterministic portfolio

The \(N=41\) edge-deletion seeds are
`2026072301` through `2026072308`.  For the other cardinalities, the search
uses the following singular vectors, counted from the least singular end:

- \(N=42\): tail indices 9, 10, 11 at scales \(0.01,0.08,0.20\).  The last
  eight null modes move the two isolated points, so these are the first three
  modes that challenge the active core.
- \(N=43\): tail indices 1, 2, 3 at scales \(0.01,0.08,0.15\).
- \(N=44\): tail indices 1, 2, 3 at scales \(0.01,0.10,0.30\).

Both signs are used.  The selected \(N=43\) result came from tail mode 1,
negative sign, scale \(0.15\).  The selected \(N=44\) result came from tail
mode 3, positive sign, scale \(0.01\); several other modes reached the same
basin to the displayed precision.

The selected coordinate hashes and contact counts are:

| \(N\) | coordinate SHA-256 | edges within \(10^{-8}\) of max |
|---:|:---|---:|
| 41 | `f6c22e89efd2fc94d108c1d23782ead87bed2d8e292718d3718a8a6deceee420` | 153 |
| 42 | `cebc461adcdceefcaa0e4b97634ce704289c36a3c5da4f9b39f150005e5e80da` | 173 |
| 43 | `d7b1e4515a3d175ea991057e2ff37c6b5c809543eba4f8b1a26078c3042641dd` | 169 |
| 44 | `67ccf8abf6cdee05ec4d2c6328eb97f85631e6cae299d5d78d03e160a126f59f` | 190 |

The complete trial list contains escaped objectives, solver statuses,
singular spectra, deleted edge lists, coordinates, Gram diagnostics, contact
counts, and hashes.

## Reproduction

The discovery environment recorded Python 3.14.6, NumPy 2.5.1, and SciPy
1.18.0 on `macOS-26.5.2-arm64-arm-64bit-Mach-O`.  From the repository root:

```sh
PYTHONPATH=. ./.venv/bin/python \
  experiments/four_point_depth_projection/construction_active_search/rigidity_softmode_search.py \
  --n41-trials 8 \
  --output experiments/four_point_depth_projection/construction_active_search/rigidity_softmode_results.json

./.venv/bin/python \
  experiments/four_point_depth_projection/construction_active_search/rigidity_stress_probe.py \
  --output experiments/four_point_depth_projection/construction_active_search/rigidity_stress_probe.json

/usr/bin/python3 \
  experiments/four_point_depth_projection/construction_active_search/rigidity_verify.py \
  experiments/four_point_depth_projection/construction_active_search/rigidity_softmode_results.json \
  --output experiments/four_point_depth_projection/construction_active_search/rigidity_verification.json

PYTHONPATH=experiments/four_point_depth_projection/construction_active_search \
  ./.venv/bin/python -m unittest -v rigidity_tests
```

The production search took 150.54 seconds.  The standard-library checker
does not import NumPy, SciPy, the optimizer, or the search program.  It
re-normalizes every row using `math.fsum` and `math.sqrt`, enumerates every
unordered pair for all 102 trial arrays, checks the coordinate hashes and
reported maxima, verifies that each selected result is a run minimum, and
checks all threshold flags.  Six regression/tamper tests pass.

`audit_rigidity.md` supplies a separate adversarial audit.  Using independent
orthonormal tangent bases, it reproduces the N=41 quotient rank, all eight
released ranks, the N=43 soft directions, and the N=44 null/near-null
directions; its seven tests pass.  It also records an intentional scope limit:
`rigidity_verify.py` checks coordinate-level integrity but does not itself
validate the stored mode/rank metadata or bind baseline locators to source
hashes.  Consequently its phrase “all checks passed” must not be read as
covering those structural fields.

At verification time the principal SHA-256 hashes were:

```text
rigidity_softmode_search.py   32407ad585c84a23415cb4e55b0fdf4d169d35acc9cfa22d86e9d1d0c840140d
rigidity_softmode_results.json 3dfbaf1cc27c504d53412490031307ee50a6e7065bfdb6fe02789f9c9d495c78
rigidity_verify.py            0244a0c4cf66fc41eedd23d58c66540d218628ebac8b0a76da14f8b8d86d78ca
rigidity_verification.json    2a4ca72f4a0694cdb54152d40ec4ae677694f32aec4e34eb8b7728e4e05004c1
rigidity_stress_probe.json    f27a5dc6e04c7054b6fbea7021c0caa182ac31e91b3f509ebdb9f0ab74493d96
```

## Numerical and logical limits

- Row normalization and all search decisions use binary64 arithmetic.
- SVD ranks use numerical thresholds and do not establish exact rigidity.
- “Active contact” here means a pair within \(10^{-8}\) of the current
  minimax maximum, not a kissing contact at inner product \(1/2\).
- SLSQP success establishes only solver convergence to a local endpoint.
- The standard-library verifier checks integrity of stored binary64 data; it
  is not directed interval arithmetic.
- A failed escape portfolio says nothing about unvisited contact graphs or
  arbitrary 41-point configurations.
- In particular, the rigid 35-point core does not imply that every
  41-point code contains such a core, is rigid, is jammed, or has this graph.
- No exact-coordinate or interval certificate was attempted because every
  candidate remained strictly above \(1/2\).

The experiment therefore supplies reproducible construction evidence and
stored coordinates for two previously unstored comparison basins, but no
lower bound beyond 40 and no upper bound.
