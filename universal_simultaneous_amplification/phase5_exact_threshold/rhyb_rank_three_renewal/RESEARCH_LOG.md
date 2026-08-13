# Research log: rank-three renewal reduction

All times are America/Los_Angeles.  No external communication or graph search
was used.

## 2026-08-13 -- exact rank-two/three stationary correction

- Derived the stationary triple-to-doubleton entrance currents directly from
  the two OR-dual update maps.  The Bd rate is a reversed-column sum and the
  dB rate is the exact geometric transform `g_r(P_kC)`.
- Proved that the old singleton balance is only the first block row of the
  killed rank-one/rank-two system.  The second row supplies a nonnegative
  rank-three current, and Schur elimination reconstructs all singleton and
  doubleton atoms from that current.
- Proved the alternating low/high excursion representation.  A common
  stationary crossing current times the two killed Green rewards gives total
  mass, mean rank, and portal-weighted singleton mass exactly.
- Homogenized BDM in these cycle variables.  The resulting rank-three
  excursion repayment inequality (RTER) is exactly equivalent to BDM, not a
  claimed proof of it.  It is the minimal legal target after the pseudo-law
  obstruction.
- Schur-traced the full three-copy product-chain forcing onto ranks one and
  two.  The traced generator is conservative, its unnormalized low-sector
  stationary law is exact, and all higher ranks reappear through positive
  Green-corrected time/rank rewards and the triple-to-double return kernel.
  This gives a precise low-sector Poisson certificate sufficient for BDM.
- Proved why the pseudo-law cannot occur for a fixed module: small low-rank
  mass forces small high-rank entrance and hence small high-rank occupation.
  Along a degenerating sequence the only escape is divergence of the killed
  high-rank Green norm, identifying the precise compactness uniformity needed.
- An exact rational weighted-four-path replay validates every block,
  entrance, Schur, Palm, and reward identity.  It performs no graph screen
  and asserts no sign for the open RTER inequality.
- The replay separately validates the `K_2` low-only boundary symbolically:
  both stationary laws, arbitrary-portal singleton sources, normalized mean
  ranks, and the exact hybrid-sextic discriminant.  No renewal current is
  spuriously assigned when the high block is empty.
- Independent hostile review validated every algebraic identity and found one
  boundary-scope ambiguity.  It is now explicit that RTER itself does not
  apply to any order-three module because the dB high block is empty, whereas
  the stochastic low-sector trace does apply rule by rule.  Weighted paths
  are covered by their direct theorem; arbitrary positive triangles remain a
  separate BDM case.  The proof now also names high-block transience as the
  reason the return kernel is stochastic.
- Best-guess completion of the exact-threshold program: **74%**.  The
  first-level relaxation is now structurally repaired, but the cross-rule
  excursion comparison, equality-scale analysis, and global compactness
  remain open.
