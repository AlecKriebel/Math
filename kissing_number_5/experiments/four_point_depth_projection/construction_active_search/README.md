# Nonsymmetric active-set and low-rank construction search

This directory is a self-contained numerical construction program for
\(N=41,42,43,44\) points on \(S^4\).  It deliberately challenges both fresh
random configurations and all useful stored five-dimensional near misses.
Nothing here is an upper-bound proof.

## Outcome

No run found a point set with maximum inner product at most \(1/2\).

| \(N\) | strongest stored/recovered binary64 value |
|---:|---:|
| 41 | 0.51499465251216603 |
| 42 | 0.51824115586226238 |
| 43 | 0.52470960182901927 |
| 44 | 0.52745771232353222 |

The \(N=43\) and \(N=44\) coordinates in
`rigidity_softmode_results.json` recover stronger comparison basins that
were documented elsewhere but whose coordinates were absent from the
repository.  They remain far above the kissing threshold and are numerical
evidence only.

## Independent mechanisms

1. `gram_search.py` performs alternating projections between diagonal-one
   half-space Gram constraints and the PSD rank-five cone, with Dykstra
   memory, weighted corrections, over-relaxation, and seeded block
   perturbations.  It ran 400,000 projection iterations over 80 restarts.
   See `gram_report.md`.
2. `surgery_active_search.py` uses literal active-contact Chebyshev LPs,
   vertex-cover moves, contact-nullspace steps, rank-five Gram completion,
   and graph-guided deletion/reinsertion.  Seventeen deterministic
   stored/random trajectories were consolidated.  See `surgery_report.md`.
3. `rigidity_softmode_search.py` forms the active-contact rigidity matrix,
   removes rotations, follows genuine or soft multi-point modes, and exposes
   new flexes by deleting contact rows from the rigid \(N=41\) core before a
   direct all-pair epigraph solve.  It ran 102 deterministic escapes.  See
   `rigidity_report.md`.

The first method found no endpoint better than its input.  The second
recovered the strong \(N=43\) basin.  The third independently recovered that
basin and the strong \(N=44\) basin.  The agreement is a useful implementation
check, not evidence of global optimality.

## Verification entry points

```sh
./.venv/bin/python \
  experiments/four_point_depth_projection/construction_active_search/gram_verify.py

./.venv/bin/python \
  experiments/four_point_depth_projection/construction_active_search/surgery_check_results.py \
  experiments/four_point_depth_projection/construction_active_search/surgery_best_configurations.json \
  --output experiments/four_point_depth_projection/construction_active_search/surgery_best_independent_check.json

/usr/bin/python3 \
  experiments/four_point_depth_projection/construction_active_search/rigidity_verify.py

PYTHONPATH=experiments/four_point_depth_projection/construction_active_search \
  ./.venv/bin/python -m unittest -v rigidity_tests
```

The verifiers reconstruct pairwise products and hashes from stored
coordinates rather than trusting solver objectives.  They verify binary64
artifacts only.  No exact-coordinate or interval certificate exists because
no threshold candidate was found.

The deterministic commands, seeds, software versions, diagnostic
definitions, and limitations for each mechanism are in its report.  The
chronological record is `research_log.md`.  `audit_rigidity.md` documents an
independent structural audit and the exact coverage limit of the
coordinate-level rigidity verifier; `comparison_rigidity_surgery.md`
cross-compares the independently recovered endpoint basins.
