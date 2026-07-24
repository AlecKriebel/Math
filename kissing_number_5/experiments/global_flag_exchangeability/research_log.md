# Research log

## 2026-07-24T07:14:53Z

- Derived the exact finite-\(N\) rooted extension-pair square identity.  The
  coefficient for a pair of extensions with union size \(u\) is
  \(\binom{N-2}{u}/\binom{k-2}{u}\).
- Identified \(2109=\binom{38}{3}/\binom43\) as the one-vertex-overlap
  coefficient for a rooted-triangle \(K_7\) flag.  This gives an independent
  global-overlap interpretation of the integer in the factorial Farkas ray.
- Found the continuous polynomial feature
  \(g_{pq}(2-3(g_{ip}+g_{iq}))\).  One exact row rejects all stored direct
  \(K_6\)--\(K_{11}\) extensions and both stored product pseudowitnesses.
- Verified the direct global square on \(D_5\) is \(646060>0\).
- For the continuous rank-five \((h,g)=(4,1)\) counteratom, found the exact
  coarse H/G estimator \(-746187/5\) and the polynomial \(g_{ij}g_{pq}\)
  estimator \(-180485617/2160\).  These reject the pure orbit but do not
  exclude its occurrence inside a repaired global mixture.
- Recorded the precise remaining gap: the fixed pair/triple marginal could
  have a different continuous \(K_6\) lift satisfying the new flag square.

## 2026-07-24T01:35:00-07:00

- Replaced every proof-critical Python `assert` in both verification paths
  with an always-on verification exception.
- Added ordinary and optimized-mode tests for the primary and independent
  checkers.
- Added tamper tests and confirmed that both checkers reject modified input
  under `python -O`.
