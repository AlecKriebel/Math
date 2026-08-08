# Universal r=2 collision closure: research log

Date: 2026-08-07 (America/Los_Angeles)

## Scope

This branch attacks the exact finite inequality

\[
\rho_{\rm dB}(G,2)\le \rho_{\rm dB}(K_n,2)
\quad\Longleftrightarrow\quad
\mathcal L(G)\le\mathcal V(G)
\]

for every connected loopless undirected weighted graph.  It retains the
finite complete-graph correction.  The weaker half-density targets
`M >= I` and `I_2 <= 2` are tracked separately and are not treated as
equivalent to the Green--collision sign.

## 2026-08-07 restart

- Replayed the exact reduction note and reconstructed the geometric-union
  dual: an occupied target is removed and replaced by the distinct sites in
  a geometric number of row-kernel samples.
- Frozen exact counterexamples that any new local inequality must survive:
  the weighted path `(1,2)` has `L>0`; the regular weighted `K_4` with edge
  weights `(1,1,2,2,1,1)` has a positive level residual; the statewise
  complete-Poisson domination fails on the path; pairwise stationary
  correlation and bounded-degree additive-potential shortcuts fail.
- Initial task: search for a genuinely stationary two-particle/capacity or
  likelihood-stability identity that bounds the *weighted aggregate* Green
  residual, rather than its levels or states separately.

## 2026-08-07 likelihood/Fisher audit

- Corrected a structural premise: the complete proper dual `Q_K` is
  stationary under `Pi_K` but is not reversible.  Rank-changing transitions
  are one-way; only same-rank swaps reverse.
- Proved the directed Bregman identity
  `I_K(g)=-<g,Q_K log g>_K>=0` and the stationarity identity
  `I_K(g)=E_Pi[(Q_P-Q_K)log g]`.  Reversibility is unnecessary.
- Implemented the sharp scalar edgewise Fenchel/Young bound.  It closes on
  the regular weighted `K_4`, but its numerically optimized right side is
  about `1.01745 V` on the frozen weighted path.  Therefore this direct
  one-parameter entropy absorption is nonclosing.

## 2026-08-07 symmetric-flow reduction

- Introduced the exact symmetric pairing
  `S=<g,(Q_K+Q_K^*)psi/2>_K` and proved
  `S=-(1/2) sum c_AB Delta g Delta psi`.
- The frozen witnesses satisfy exactly
  `2/135 < 1/45 < 8/135` on the path and
  `L=S=207/22960 < 247/22960` on the regular weighted `K_4`.
- Exact rational random screening through five vertices, including
  near-singular undirected weights, found no violation of the stronger split
  `L<=S<=V`.  This is evidence only.
- Derived the exact current decomposition: same-rank swaps cancel from
  `L-S`; each one-way rank-changing edge contributes
  `c_AB(g_A+g_B)(psi_B-psi_A)/2`; a cycle decomposition turns `L-S` into a
  weighted sum of oriented polygon areas in the `(g,psi)` plane.
- Found an exact positive-support directed five-vertex kernel with `L>S`.
  This proves that stationarity alone is insufficient and isolates
  reversibility of the underlying undirected vertex kernel as essential.
- A floating-point optimizer initially reported an extreme undirected
  `L>S` candidate at a weight ratio around `10^16`; exact rational replay
  reversed the sign.  This is a saved conditioning warning, not a graph
  counterexample.
- The symmetrized statewise comparison remains false: on the weighted path,
  exact residuals include `-13/990` and `-4/495`.  Hence `S<=V` is still a
  stationary aggregate problem.
- Expanded the circulation exactly over original vertex pairs using
  `b_uv=2/(n-1)-P_uv-P_vu` and centered pair Poisson kernels `eta_uv`:
  `L-S=sum b_uv E_Pi[Q_a eta_uv]`.  A termwise edge sign is false.  On the
  undirected path `(1,4)`, pair `{0,1}` contributes `+4/13365`, although the
  total is `-8/891`.  Cross-edge cancellation is essential.
- Tested a second natural repair: solve `Q_K phi=Q_s psi` and compare
  `v(A)` with `(Q_K-Q_P)phi(A)`.  It too fails statewise on both frozen
  witnesses (for example, residual `-8/605` on the path).  No local
  conditional-square factorization has survived exact screening.

## 2026-08-08 exact refutation of the symmetric split

- A well-conditioned six-vertex optimization produced `L-S>0`.  Exactified
  it to the complete-support undirected integer graph with lexicographic edge
  weights
  `(3,300,2,5,1,3,3,1,300,1,1,1,20,1,1)`.
- Full exact 62-state replay proves `L-S>0` (approximately
  `0.000549607481817`) while `L-V<0` (approximately `-0.108444295487`).
  Thus the stronger split `L<=S<=V` is **EXACTLY FALSIFIED**, but the graph
  is not an r=2 amplifier.
- Per project direction, all further work pivots to the direct sign `L-V`.
  `S` will be used only if it participates in an exact compensating
  cancellation, not as a separate inequality target.

## 2026-08-08 bounded direct `L-V` cycle

- Searched the actual gap from the exact n=6 split witness using 400 nearby
  perturbations, 800 broad complete-support samples, 900 connected sparse
  samples, and local optimization from the eight strongest candidates.
- No `L-V>0` candidate appeared.  The complete graph was the numerical
  maximizer; the closest nonbaseline local point had gap about `-1.23e-7`
  and was itself converging to complete.  This is numerical evidence only.
- Replaced the discarded `S` split by a direct actual-flow identity.  With
  uncentered event kernels `T_P,T_K`, ratio `r=T_P/T_K`, complete event flow
  `c=Pi_K T_K`, and likelihood `g=Pi/Pi_K`, sourcewise centering gives
  `sum_B T_K r=sum_B T_K=|A|`, while actual stationarity makes
  `c g r` balanced.  Consequently
  `L=sum_AB c_AB g_A (1-r_AB) Delta psi_AB` exactly.
- The direct target is now the single transport-cost inequality
  `E_Pi v >= sum c g (1-r) Delta psi`, retaining both sourcewise centering
  and global conservation.  The verifier constructs the event kernels and
  checks every identity over exact rationals.
- **OPEN minimal obstruction:** prove that the ratios induced by one
  reversible vertex kernel make this compensated work no larger than the
  explicit subset-mass tangent cost `V`.  Statewise domination is already
  exactly false, so the conservation constraint is essential.
