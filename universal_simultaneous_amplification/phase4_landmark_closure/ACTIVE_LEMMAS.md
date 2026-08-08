# Active exact lemmas

Last updated: 2026-08-08 stationary determinant and flow audit.

## A. Endpoint product at `r=3/2`

For every finite connected loopless undirected weighted graph `G` on `n`
vertices, prove or refute

\[
 \rho_{\rm Bd}(G,3/2)\rho_{\rm dB}(G,3/2)
 \le \rho_{\rm Bd}(K_n,3/2)\rho_{\rm dB}(K_n,3/2).       \tag{A}
\]

It is proved for all positive weighted triangles and locally at the complete
graph in the audited finite orders.  Exact finite and weighted searches have
not found a violation, but (A) is **OPEN**.

The exact dual form is

\[
 m_Bm_D\le m_B^Km_D^K,
\]

where fixation is stationary dual mean divided by `n`.  A sufficient
arithmetic strengthening is

\[
 {m_B\over m_B^K}+{m_D\over m_D^K}\le2.                \tag{A1}
\]

Any product-chain certificate for (A1) must retain graph-sensitive vertex
information within ranks: dependence only on the two ranks and their overlap
is exactly impossible on the three-path.

An exact intermediate orientation problem is now isolated.  For the Bd dual
`L`, its reversed-arrow partner `C`, `M=(L+C)/2`, `K=(L-C)/2`, and
`Q_s=M+sK`, prove

\[
 m(s)+m(-s)\le2m(0),\qquad 0\le s\le1.                \tag{A2}
\]

With midpoint conductance Laplacian `H`, incidence matrices `A,B`, edge
current diagonal `J_e`, group inverse `H#`, and the exact transfer objects
`X,u` defined in `obstruction/endpoint_product_variational/RESEARCH_LOG.md`,
(A2) is equivalent to

\[
 \boxed{1_E^T X(I-s^2X^2)^{-1}u\le0.}                 \tag{A3}
\]

The determinant reduction and the skew-ground-state Dirichlet identities
are proved.  Generic PSD, individual Taylor coefficients, single-tree
reversal, transient domination, and rank-tail domination are exactly false.
Even (A2) would settle only the orientation factor; the separate geometric
batching comparison would remain.

## B. The weaker endpoint separator

The theorem actually needed for `R_sim=3/2` is only

\[
 \min\left\{
 {\rho_{\rm Bd}(G,3/2)\over\rho_{\rm Bd}(K_n,3/2)},
 {\rho_{\rm dB}(G,3/2)\over\rho_{\rm dB}(K_n,3/2)}
 \right\}\le1.                                         \tag{B}
\]

This remains **OPEN** even if (A) is false.  Candidate separators may be
nonlinear or graph-dependent before yielding the graph-independent
disjunction.

The strongest surviving affine candidate is the balanced normalized mean

\[
 {1\over2}\left\{
 {\rho_{\rm Bd}(G,3/2)\over\rho_{\rm Bd}(K_n,3/2)}+
 {\rho_{\rm dB}(G,3/2)\over\rho_{\rm dB}(K_n,3/2)}
 \right\}\le1.                                        \tag{B1}
\]

Exact endpoint witnesses force any fixed affine multiplier to lie in
`(177/2000,7/12)`.  The balanced value survives every exact test, but is
not proved.

## C. Exact endpoint drift bridge

For a mutant set `S` of size `k`, let

```text
x_i = sum_(j in S) P_ij,
T_S = sum_i x_i,
B(S) = sum_(i notin S) x_i,
B_0(k) = k(n-k)/(n-1).
```

The proved identity is

\[
 \mathcal D(S)+C_M\{A(S)-B(S)\}
 =-(C_M-C_R)\{B(S)-B_0(k)\}-\mathcal E(S),             \tag{C}
\]

with `C_M-C_R>0` and `E(S)>=0`.  The exact remaining obstruction is to
control the signed row-cut deviation after the correct occupation or
stationary averaging.  It is not pointwise nonnegative.

Combining this bridge with the two exact transient Green measures gives

\[
 e_B+e_D=\mathsf T+\mathsf C-\mathsf E,
 \qquad \mathsf E\ge0.                                \tag{C1}
\]

Thus (B1) is exactly the global inequality

\[
 \boxed{\mathsf T+\mathsf C\le\mathsf E}.             \tag{C2}
\]

Neither its statewise terms, its fixed-rank sums, `T` by itself, nor
`C-E` by itself has the required sign.  A ten-atom exact Farkas law also
excludes every vertex-labelled bilinear *pointwise* correction on the
weighted `1:17` three-path.  The surviving proof obligation must use the
cross-rank Green-flow conservation law or an equivalent global
capacity/path-reversal theorem.

The signed fields in `T+C` lie exactly in the first two nonconstant
eigenspaces of every rank-`k` Johnson graph.  Exact Johnson inversion turns
`T+C` into a within-rank Dirichlet pairing.  This does not close the sign:
scalar rank-flow constraints fail exactly on `P_3`, and the full
rank-labelled degree-two Green relaxation fails exactly on a seven-vertex
graph while its true fixation score remains below baseline.  In block form,
the missing information is the high-mode Schur feedback (writing
`mathcal A=-L_U^T` and `H=I-Pi`)

\[
 \Pi\mathcal A H(H\mathcal A H)^{-1}H\mathcal A\Pi,
\]

(with the notation fixed in `threshold/green_flow_separator/`), not another
low-degree observable.

## D. Fitness-two finite-baseline sign

Let `Pi` be the exact stationary geometric-union dB dual law at fitness two.
The proved Green comparison is

\[
 \rho_{\rm dB}(G,2)-\rho_{\rm dB}(K_n,2)
 =\mathcal L(G)-\mathcal V(G),\qquad \mathcal V(G)\ge0. \tag{D}
\]

The single exact open sign is

\[
 \boxed{\mathcal L(G)\le\mathcal V(G).}                \tag{D1}
\]

It is equivalent—not merely sufficient—to dB complete-graph maximality at
fitness two.  Proving (D1) gives the fallback universal bound
`R_sim<=2`.

The auxiliary symmetric complete-flow pairing `S` obeys exact circulation
and Dirichlet formulas, but the proposed split `L<=S<=V` is false.  A
complete-support undirected order-six rational graph has `L-S>0` exactly
while retaining `L-V<0`.  Thus only the direct difference `V-L`, including
its cancellation between symmetric and antisymmetric currents, remains a
valid target.

There is now a direct event-flow form.  If `T_P,T_K` are the uncentered
actual and complete dual event kernels, `r_AB=T_P(A,B)/T_K(A,B)`,
`c_AB=Pi_K(A)T_K(A,B)`, `g=Pi/Pi_K`, and `Q_K psi=F`, then sourcewise event
normalization and actual stationarity give exactly

\[
 \mathcal L=
 \sum_{A,B}c_{AB}g(A)(1-r_{AB})\{\psi(B)-\psi(A)\}.   \tag{D2}
\]

Thus (D1) is a compensated transport-cost bound by `V`; neither factor in
(D2) has a separate pointwise sign.

## E. Weaker fitness-two density signs

Each of the following remains **OPEN** and currently yields only the weaker
ceiling `rho_dB(G,2)<=1/2`:

\[
 E_\Pi Z\le E_\Pi S_1,
\]

equivalently `E|A|^2 <= (n/2)E|A|`;

\[
 H(C\mid B)\ge I(V;B);
\]

and

\[
 I_2(V;B)\le2.
\]

The complete finite baseline is strictly below `1/2`, so none alone proves
`R_sim<=2` without a finite-size stability argument.

## F. Direct-portal resolvent separation (class problem)

For the fixed-finite-rank blade model with direct portal edges, the candidate
map inequality is

\[
 S^{D,h}(J_r(s))<J_r(S^{B,h}(s)).                       \tag{F}
\]

The no-direct-portal case is proved.  In the direct case, `Q=2,T=1` is now
also proved impossible for every `r>=3/2`, with arbitrary positive unequal
portal loads and an arbitrary positive portal edge.  The exact separator is

\[
 T_B+{81\over200}T_D<0,\qquad 3/2\le r\le2.          \tag{F1}
\]

The remaining direct-portal problem begins at three portals, multiple blade
types, or growing portal rank.  No statement in this section is universal
over arbitrary graphs.

A second exact theorem closes one growing-rank subregime.  If `Q_s->infinity`,
`Q_s=o(s)`, the portal graph is `H`-regular with maximum edge weight tending
to zero, and blade incidence is exchangeable across portal identities, then
the limiting portal episode is a scalar branching process.  Bd establishment
can exceed `1-1/r` only when `B+H>1`; throughout that regime dB establishment
is strictly below `1-1/r`.  If `B+H<1`, Bd is strictly below it.  This holds
for every `r>1` and includes complete portal graphs and degree-diverging
regular expanders.  Fixed-degree networks, portal-dependent incidence, and
singular scaling remain outside the theorem.

## G. Endpoint batching covariance

Let `K_R` be the post-neutral refreshed-target event chain and `K_D` the
locked-target dB burst chain at `r=3/2`.  Let `tau_R(A),tau_D(A)` be their
rooted in-arborescence cofactors, `beta_C=tau_R/Z_R`, and

\[
 \zeta(A)={Z_R\tau_D(A)\over Z_D\tau_R(A)},\qquad
 f(A)=|A|^{-1},\qquad c=R_Cf.
\]

The exact open batching comparison is equivalent to

\[
 \boxed{
 \operatorname{Cov}_{\beta_C}(\zeta,f)
 \ge R_n^{-1}E_{\beta_C}c-E_{\beta_C}f.}             \tag{G}
\]

All quantities in (G) are positive tree or coverage weights, but neither
side has a separate sign.  The rootwise integrand has both signs already on
`K_4`, so a proof must transport mass between different arborescence roots.

## H. Rank-weighted posterior reflection at fitness two

For the stationary fair-geometric dual, let `e_v(B)` be the effective-target
posterior excess, `k=|B|`, `h=n-k`, and

\[
 J(B)=\sum_{v\notin B}(e_v-k/h)^2,
 \qquad
 G(B)=\sum_{v\notin B}{1\over1+e_v}-{h^2\over n}.
\]

The sharp pointwise arithmetic--harmonic lemma proves

\[
 J(B)\le n c_{n,k}G(B),                              \tag{H}
\]

where `c_(n,k)` is the exact piecewise coefficient recorded in
`obstruction/r2_posterior_reflection/POSTERIOR_REFLECTION.md`.  Hence the
finite complete baseline would follow from the sole stationary sign

\[
 \boxed{E_\Pi[c_{n,|B|}G(B)]\le m_K-E_\Pi|B|.}       \tag{H1}
\]

The active-channel Brier decomposition of (H1) is exact.  Centered Cayley
contraction, constant-coefficient splitting, targetwise positivity, and
reversible edge-pair positivity are all exactly false; cancellation is
nonlocal even on a tree.
