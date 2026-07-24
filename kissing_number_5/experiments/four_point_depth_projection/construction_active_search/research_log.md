# Research log

All times are America/Los_Angeles (PDT), 2026-07-23.

## 22:44–22:51 — Input audit

- Created this dedicated construction-search directory.
- Recursively inventoried stored \(N=41,\ldots,44\), five-coordinate arrays.
  Found 312 occurrences and 276 distinct normalized binary64 arrays.
- Excluded six-dimensional compression artifacts by an explicit
  shape-\((N,5)\) rule.
- Recomputed the initial best values as
  \(0.51499465251216603\),
  \(0.51824115586226238\),
  \(0.52472447701452274\), and
  \(0.52747119253595742\).

## 22:51–23:03 — Alternating low-rank Gram search

- Implemented diagonal/off-diagonal corrections alternating with PSD
  rank-five spectral projection.
- Ran 80 deterministic restarts, five correction schedules, 5,000 iterations
  each: 400,000 spectral iterations total.
- Added independent verification, seven regression/tamper tests, and a full
  deterministic replay.
- No restart beat a stored baseline or reached \(1/2\).

## 22:52–23:08 — Hard active-contact surgery

- Implemented hard Chebyshev tangent LPs, vertex-cover moves, contact
  nullspace escapes, Gram completion, and graph-guided reinsertion.
- Ran 17 deterministic trajectories spanning stored and fresh random starts.
- Recovered the strong \(N=43\) basin at
  \(0.5247096018292908\); no \(N=41,42,44\) improvement.
- Consolidated coordinates and ran an independent graph/spectrum/hash audit
  plus six tests.

## 22:56–23:09 — Rigidity-guided soft modes

- Found that the \(N=41\) maximum graph has a 35-vertex active core and six
  isolated points.  Binary64 rigidity rank on the core is
  \(4\cdot35-10=130\), leaving only rotations among equality flexes.
- Numerically found a strictly positive equilibrium stress on all 153 core
  edges, with minimum normalized weight
  \(0.0011269047923961543\) and residual \(6.16\cdot10^{-15}\).
- Exposed non-rotational modes by deleting 24 active rows.  Eight edge
  selections, two signs, and three scales produced 48 \(N=41\) escapes; all
  returned to the \(0.514994652512166\) basin.
- Tested 18 soft-mode escapes at each of \(N=42,43,44\).
- Recovered \(N=43\) at \(0.52470960182901927\) and \(N=44\) at
  \(0.52745771232353222\), thereby storing coordinates for both stronger
  comparison basins.

## 23:09–23:15 — Independent verification and documentation

- Added a standard-library verifier that imports neither the search nor
  NumPy/SciPy.  It checked every unordered pair in all 102 rigidity trials,
  coordinate hashes, selected minima, and threshold flags.
- Confirmed that the best arrays still contain respectively
  171, 208, 214, and 214 pairs above \(1/2\).
- Added six rigidity regression/tamper tests; all pass.
- Recorded the exact distinction between numerical diagnostics and exact
  spherical-code certificates.  Since every endpoint is above \(1/2\), no
  exact or interval candidate verification was triggered.
