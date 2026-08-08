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

## 2026-08-08 direct transport-cost closure audit

- Rewrote every tangent-remainder atom exactly in burst-hit coordinates.  If
  `p=h(x)` and `p0=h(k/(n-1))`, then
  `2(x-a)^2/[(1+a)^2(1+x)]=(p-p0)^2/(2-p)`.  Thus `V` is a weighted
  one-sided chi-square cost, not an unspecified quadratic remainder.
- Proved the statewise cancellation
  `v(A)-U_s Z(A)=sum c_k(p0-p_vC)`.  Combining it with the stationary
  coupon-union identities collapses the full direct residual exactly to
  `V-L=rho_K-E_Pi|A|/n` and to the explicit coefficient identity (20) in
  `DIRECT_STATIONARY_FLOW_REDUCTION.md`.  The sharp scalar obstruction is
  now: the stationary geometric-union dual must have mean size at most the
  complete dual mean `(n-1)2^(n-2)/(2^(n-1)-1)`.
- Hostile-tested the most direct compensated log-sum idea.  For the
  normalized actual and complete event rows, the full event KL has the exact
  Pinsker lower bounds `8051/18000` on the path and `65753/774900` on the
  regular weighted `K4`.  Both already exceed `V` exactly.  Hence a proof
  cannot charge the full event KL to `V`; it must exploit signed balance or
  project to the hit marginals.  This closes the generic full-KL absorption
  route, not all compensated entropy arguments.
- Refuted the corresponding graph-independent rescaled event-chi sandwich
  exactly.  The regular weighted `K4` forces
  `alpha>=L/Chi~=0.042318852`, while the rational six-vertex split witness
  forces `alpha<=V/Chi~=0.025064992`.  The verifier checks the crossing over
  exact fractions.  State-dependent compensation remains open.
- A floating Hellinger-constant screen likewise crossed by `n=4`
  (`sup L/H^2` about `0.1259`, `inf V/H^2` about `0.08086`).  This is only
  numerical evidence against a graph-independent scalar sandwich and is not
  used as an exact refutation.
- Extended the direct numerical falsification pass by 1,200 full and 1,000
  sparse six-vertex samples and by 1,000 full and 700 sparse seven-vertex
  samples, with local polishing of the strongest candidates.  No positive
  gap appeared; polished full-support points converged to `K_n`.
- Added an independent exact finite screen: 54 connected weighted
  three-vertex graphs, 624 connected weighted four-vertex graphs, 48 seeded
  sparse/extreme five-vertex graphs, and the frozen six-vertex split witness.
  Every exact gap satisfies `V-L>=0`.  This is finite validation only.
- **FINAL STATUS OF THIS BOUNDED CYCLE:** no admissible `L>V` counterexample
  and no universal proof.  The sharper sole sign is the stationary-size
  inequality above, equivalently the conserved-flow/hit-cost inequality.

## 2026-08-08 rank-refined posterior collision cycle

- Reopened the exact stationary target experiment with
  \(e_v(B)=\nu_v(B)/\Pi(B)\) and
  \(\sum_{v\notin B}e_v(B)=|B|\). Defined the exact posterior collision
  excess
  \(J(B)=\sum e_v^2-|B|^2/(n-|B|)
  =\sum(e_v-|B|/(n-|B|))^2\).
- The first rank-envelope choice
  \(E[(n-k)\sum e_v^2/k]\le m_K\) is **EXACTLY FALSE**. The unweighted path
  has \(14/9>4/3\), and the regular weighted \(K_4\) has
  \(2514/1435=12/7+54/1435\).
- Isolated a new finite-baseline two-replica sign with explicit weights
  \(a_k=1/n\), \(b_k=k-k^2/[n(n-k)]\):
  \[
  E[k+J(B)/n]\le m_K,
  \qquad\text{equivalently}\qquad
  EJ(B)\le n(m_K-Ek).
  \]
  Its sharp pointwise lower envelope is \(k\), so it proves the exact
  complete-baseline inequality rather than only half density. It is stronger
  than, not equivalent to, the desired theorem.
- Expanded the Cayley identity
  \(\nu_v=((\sigma_v+\nu_v)/2)A_v\) into an exact two-replica
  coincident-output sum. The sole remaining sign is that this collision
  energy, after subtracting the rankwise uniform minimum, is paid by \(n\)
  times the complete-law mean deficit.
- Exact slacks are \(1/6\) on unweighted \(P_3\), \(1/5\) on weighted
  \(P_3(1,2)\), and \(8/615\) on the regular weighted \(K_4\); the \(n=6\)
  split witness is also exactly positive (approximately \(3.13798935\)).
- Exact corpus replay found no violation among 54 connected \(n=3\) graphs,
  624 connected \(n=4\) graphs, 48 fixed sparse/extreme \(n=5\) graphs, and
  the \(n=6\) split witness. Full/sparse/directed numerical searches through
  \(n=7\) also found no violation; the smallest optimized ratio
  \(n(m_K-Ek)/EJ\) was about \(1.43016\).
- **FINAL STATUS:** no proof or counterexample. The new sole scalar
  two-replica obstruction is the finite collision-reflection inequality in
  POSTERIOR_RANK_COLLISION_REDUCTION.md; it strictly improves the earlier
  half-density-only \(I_2\le2\) target in relevance to the required baseline.
