# Construction Round 4: asymmetric contact surgery

## Status

**NUMERICAL EVIDENCE ONLY — NOT A CONSTRUCTION CERTIFICATE OR AN UPPER
BOUND.**

This independent 36-run portfolio found no 41-, 42-, 43-, or 44-point code
with maximum inner product at most \(1/2\).  In fact, no run reached
\(0.51\), so the requested exact-reconstruction analysis for a candidate at
or below that threshold was not triggered.

All final binary64 coordinates are released in
[`results/contact_surgery_portfolio.json`](results/contact_surgery_portfolio.json).
Its SHA-256 is

```text
c41781a5f1d33f24738620811646412d7b255bec94b913404bfeba19fd91036f
```

## Mechanism

Every run starts with the exact 40-point \(D_5\) root code, deletes 7--12
individual oriented roots, and sequentially inserts enough maximin-hole
points to reach the requested size.  Deleting individual roots, rather than
unoriented pairs, deliberately breaks antipodal symmetry.

After all coordinates are released, the program repeats the following
basin-hopping move:

1. use high-temperature contact weights to identify stressed points;
2. remove one point, or two points on every sixth move;
3. solve a multistart maximin-hole problem against the remaining cloud;
4. reinsert the new point or points;
5. release all coordinates through a log-sum-exp continuation;
6. accept improvements and occasional uphill moves under a cooling schedule.

A direct epigraph SLSQP solve equalizes the active contacts only after the
macro search.  Thus this round differs from the round-3 Riemannian
augmented-Lagrangian portfolio: its main exploration mechanism changes the
point set by deletion and reinsertion, allowing contact-graph topology
jumps rather than following one continuous multiplier path.

## Results

| \(N\) | runs | best seed | macro moves | best maximum inner product | gap above \(1/2\) |
|---:|---:|---:|---:|---:|---:|
| 41 | 9 | 2026072320 | 24 | 0.5155570516153124 | 0.0155570516153124 |
| 42 | 9 | 2026072326 | 30 | 0.5199641730896711 | 0.0199641730896711 |
| 43 | 9 | 2026072323 | 30 | 0.5247244770145403 | 0.0247244770145403 |
| 44 | 9 | 2026072319 | 24 | 0.5274711925359574 | 0.0274711925359574 |

The closest output is still more than \(0.0155\) above the kissing
threshold.  Therefore interval verification or exact coordinate recovery
would have no useful target.

The 41-point run returned the familiar unrestricted numerical basin rather
than a new D5-like code.  At \(10^{-8}\) below its own numerical maximum,
its active graph is connected with 155 edges and degree histogram

\[
5^1\,6^3\,7^{14}\,8^{18}\,9^5.
\]

The other best active graphs have:

| \(N\) | active edges | degree histogram | component sizes |
|---:|---:|:---|:---|
| 42 | 163 | \(0^4\,6^4\,7^8\,9^{14}\,10^{12}\) | \(38,1,1,1,1\) |
| 43 | 172 | \(5^8\,6^6\,7^8\,10^{20}\,12^1\) | \(43\) |
| 44 | 182 | \(6^4\,7^4\,8^{16}\,9^{16}\,10^4\) | \(44\) |

The four numerical rattlers at \(N=42\) are another warning that neither
maximality, jamming, nor rigidity may be assumed in an upper-bound proof.
All active graphs here use a tolerance relative to the run's own maximum;
they are not exact contact graphs at \(1/2\).

## Reproduction

The recorded environment was Python 3.9.6 on macOS arm64, with NumPy 1.24.3
and SciPy 1.10.1.  The requirements are pinned in
[`requirements.txt`](requirements.txt).  Run the tests:

```sh
python -m unittest \
  experiments.construction_round4_surgery.test_contact_surgery -v
```

The portfolio used three deterministic batches:

```sh
python -m experiments.construction_round4_surgery.contact_surgery \
  --n 41 42 43 44 --seeds 2026072318 --moves 14 \
  --output /tmp/contact-surgery-14.json

python -m experiments.construction_round4_surgery.contact_surgery \
  --n 41 42 43 44 \
  --seeds 2026072319 2026072320 2026072321 --moves 24 \
  --output /tmp/contact-surgery-24.json

python -m experiments.construction_round4_surgery.contact_surgery \
  --n 41 42 43 44 \
  --seeds 2026072322 2026072323 2026072324 2026072325 2026072326 \
  --moves 30 --output /tmp/contact-surgery-30.json
```

Elapsed times and solver ulps are platform-dependent.  Recompute every
stored maximum, coordinate hash, negative-pair count, and active graph:

```sh
python -m experiments.construction_round4_surgery.check_portfolio \
  experiments/construction_round4_surgery/results/contact_surgery_portfolio.json
```

This checker is a binary64 integrity tool, not a proof verifier.  The
search and checker use no directed rounding, and a solver's local optimum
cannot establish a global lower bound.
