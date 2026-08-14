# Research log: normalizer-free two-root MP renewal

All times are America/Los_Angeles.  No external communication, graph
enumeration, or kernel search was used.

## 2026-08-13 17:40 PDT — exact renewal scaling and finite-depth obstruction

- Derived the honest full-cycle scaling of the already proved portal
  minimax.  With root occupation fields `B_i,D_i` and
  `Z=r^3[X_B]_+[X_D]_+`, the exact all-portal target is
  `(x.B)(x.eD)>=Z(x.1)(x.e)`; both singleton totals and the renewal crossing
  currents cancel.
- Obtained the normalizer-free positive-diagonal form
  `for every z>0 there exists t>0` such that
  `zB_i+z^-1 e_iD_i >= sqrt(Z)(t+e_i/t)` at every root.
  This is a scaling of the existing minimax theorem, not a new proof of its
  support-two statement.
- Wrote the exact renewal copositivity data
  `d_i=e_i(B_iD_i-Z)` and
  `k_ij=B_i e_jD_j+B_j e_iD_i-Z(e_i+e_j)`.
- Split the pair margin into the Hellinger core and the exact swapped-root
  orientation square.  A positive rational example has exact margin `121`
  while its Hellinger core is `-41`, proving that a Cauchy route which drops
  orientation is strictly too strong at the abstract algebraic level.
- Proved a simultaneous finite-depth theorem for both duals.  Since neither
  dual can lower rank by more than one per update, scaling all genuine atoms
  through rank `m+1` and placing residual mass at rank `m+2` preserves every
  coordinate stationarity equation through rank `m`.  At order `2(m+2)`
  the two pseudo-densities tend to `1/2>p`, while their singleton product is
  `O(epsilon^2)`.  Hence no fixed rank prefix can prove even the diagonal MP
  tests for any `1<r<2`.
- The pseudo-laws are deliberately nonstationary at the first omitted rank;
  this is a proof-route obstruction, not a graph counterexample.
- Added an independent exact replay.  At `m=2`, `s=8`, `r=3/2`, it builds
  both complete-kernel dual rank laws, checks every labelled singleton and
  doubleton pseudo-balance, and verifies strict one-root MP failure.
- Strongest result: the residual universal MP theorem is a full-rank,
  orientation-preserving comparison between two honest root-occupation
  fields and their full signed cycle rewards.  Bounded-rank renewal and
  orientation-dropping Cauchy routes are closed exactly.
- Best-guess completion: **100% for this assigned reduction/obstruction;
  roughly 50% for universal `(MP)` itself.**  Portal optimization and all
  bounded-rank closures are eliminated, but the decisive full-return pair
  inequality remains unproved.
