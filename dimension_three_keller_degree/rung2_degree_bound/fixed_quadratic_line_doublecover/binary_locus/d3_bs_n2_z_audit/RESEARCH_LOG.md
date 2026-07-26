# Research log — hostile `D3-BS-N2-Z` audit

All timestamps are UTC.  No commit or push was performed by this audit
agent.

## 2026-07-26T09:31Z

- Stopped the earlier repeated-factor component probe and switched
  completely to the bounded hostile audit requested by the root agent.
- Read the candidate `d3_construction_search/NOTE.md` and treated every
  displayed normalization, pivot, and branch split as a claim to break.
- Reconstructed the \(E_7\) syzygy blocks directly from
  \[
  (-2p^3q^2,-4p^5,8p^5q).
  \]
  Obtained nullities \(0,1,3\) for the \(r^2,r^1,r^0\) blocks and
  recovered the claimed four-parameter tangent.

## 2026-07-26T09:36Z

- Implemented a fresh PARI/GP weighted-determinant expansion retaining
  every binary \(U_0,V_0,T_0\), every coefficient of \(A,B\), and all
  nine entries of \(L\).
- Recovered exactly the division-free ladder
  \[
  c=0,\quad b+k=0,\quad a^2b=0,\quad bu_2+6au_3=0.
  \]
- Checked the source-\(r\) scaling and confirmed that it covers exactly
  the two nonzero charts without sacrificing \(\det L\ne0\).
- Replayed Chart I and all three Chart II branches through the decisive
  \(E_4/E_3\) identities.

## 2026-07-26T09:39Z — fail-closed incident

- A temporary pivot-discovery block introduced a GP parenthesis error.
  GP emitted syntax diagnostics and “skipping file” but later printed
  the literal success marker.
- The strict wrapper rejected the run because it checks interpreter
  diagnostics before accepting the marker.  This is a concrete
  regression case showing that marker-only wrappers are unsafe.
- Removed the temporary block and retained a synthetic forged-log test
  plus a sign-corrupted decisive-\(E_3\) run.

## 2026-07-26T09:43:34Z

- Added explicit unit-coefficient checks for all six general \(E_6\)
  pivots and full-rank checks for every chart-specific lower pivot
  block.
- Independently verified the rank-six origin solve
  \(A_r=0,\ B_r=2\ell_8q\), and checked both structural automorphism
  exits.
- Final strict marker:
  `D3_BS_N2_Z_HOSTILE_STRICT_PASS`.
- Verdict: **PASS** for the full frozen-family counterexample
  exclusion; no implication for the global quartic row.
