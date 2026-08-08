# Active exact lemmas

Last updated: 2026-08-07 restart gate.

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

The no-direct-portal case is proved.  (F) is numerical only and is secondary
to the universal endpoint and fitness-two tasks.
