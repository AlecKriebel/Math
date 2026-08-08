# Exact Green--Poisson reduction for the balanced endpoint separator

Date: 2026-08-07 (America/Los_Angeles)

No literature search or external contact was used.

## Status

The identity below is **PROVED** for every finite connected loopless
undirected weighted graph.  It does not prove the balanced separator.  It
reduces that separator to one explicit joint Green-occupation inequality and
exactly refutes the tempting statewise, fixed-rank, separately signed, and
first-change-weighted shortcuts.

The balanced conjecture

\[
 {\rho_{\rm Bd}(G,3/2)\over\rho_{\rm Bd}(K_n,3/2)}
 +{\rho_{\rm dB}(G,3/2)\over\rho_{\rm dB}(K_n,3/2)}
 \le2                                                     \tag{1}
\]

remains **OPEN**.

## 1. Continuous changing generators and Green measures

Put `q=2/3`, `P_ij=w_ij/d_i`, and let `mu` be uniform on singleton
sets.  Self-loops may be deleted and all remaining rates at one state may be
multiplied by a common positive number without changing fixation.  We use
the following continuous type-changing generators.

For Bd, define for `v notin S` and `v in S`, respectively,

\[
 a_v(S)=\sum_{u\in S}P_{uv},\qquad
 b_v(S)=\sum_{u\notin S}P_{uv}.
\]

Then

\[
 L_B f(S)=\sum_{v\notin S}{3\over2}a_v(S)\{f(S+v)-f(S)\}
 +\sum_{v\in S}b_v(S)\{f(S-v)-f(S)\}.                 \tag{2}
\]

For dB put

\[
 x_v(S)=\sum_{u\in S}P_{vu}.
\]

Symmetry of `w` makes this exactly the mutant incident-weight fraction at
the dying target `v`.  Thus

\[
 \begin{aligned}
 L_D f(S)
 &=\sum_{v\notin S}{3x_v\over2+x_v}\{f(S+v)-f(S)\}\\
 &\quad+\sum_{v\in S}{2(1-x_v)\over2+x_v}\{f(S-v)-f(S)\}.
 \end{aligned}                                         \tag{3}
\]

Let `L_U^T` denote the transient restriction.  Connectivity makes
`-L_U^T` a nonsingular M-matrix.  Define the exact Green occupation vector

\[
 \boxed{(-L_U^T)^\mathsf T z_U=\mu.}                   \tag{4}
\]

Thus `z_U(S)` is the expected continuous time spent in `S` before
absorption, averaged over the initial singleton.

## 2. Exact normalized Poisson formula

The complete Bd and dB harmonics at fitness `3/2` are

\[
 \phi_B(k)={1-q^k\over1-q^n},\qquad
 \phi_D(k)={n-(n+k/2)q^k\over n(1-q^{n-1})}.           \tag{5}
\]

For either rule, Dynkin's formula gives

\[
 \rho_U(G)-\rho_U(K_n)
 =\sum_{\varnothing\ne S\ne V}z_U(S)L_U\phi_U(S).     \tag{6}
\]

For `k=|S|`, define

\[
 A(S)=\sum_{i\in S}(1-x_i),\qquad
 B(S)=\sum_{i\notin S}x_i.
\]

Because `sum_i x_i=sum_{j in S}t_j`, one has

\[
 A-B=k-\sum_i x_i.                                    \tag{7}
\]

Direct substitution of the increments in (5) into (2)--(3) gives the two
particularly simple normalized drifts

\[
 \boxed{{L_B\phi_B(S)\over\rho_B(K_n)}
       =q^{k-1}\{A(S)-B(S)\},}                         \tag{8}
\]

\[
 \boxed{{L_D\phi_D(S)\over\rho_D(K_n)}
       ={q^{k-1}\over n-1}\,\mathcal D(S),}            \tag{9}
\]

where

\[
 \mathcal D(S)=
 (n+k/2-1)\sum_{i\notin S}{x_i\over1+x_i/2}
 -(n+k/2-3/2)\sum_{i\in S}{1-x_i\over1+x_i/2}.        \tag{10}
\]

The cancellation in (8)--(9) is special to `q=2/3`: the selective factor
`3/2` times the next-rank factor `q` is exactly one.

## 3. Insert the exact dB tangent-square bridge

Set

\[
 B_0(k)={k(n-k)\over n-1},
\quad C_R={2(n-1)^2\over2n+k-2},
\quad C_M={3(n-1)^2\over2n+k-3}.                       \tag{11}
\]

With `alpha=k/(n-1)` and `beta=(k-1)/(n-1)`, put

\[
 \mathcal E(S)=
 C_R\sum_{i\notin S}{(x_i-\alpha)^2\over2+x_i}
 +C_M\sum_{i\in S}{(x_i-\beta)^2\over2+x_i}.         \tag{12}
\]

The previously proved tangent identities give

\[
 \mathcal D+C_M(A-B)
 =-(C_M-C_R)(B-B_0)-\mathcal E.                        \tag{13}
\]

Combining (6), (8), (9), and (13) proves the promised identity.  If

\[
 e_B={\rho_B(G)\over\rho_B(K_n)}-1,
 \qquad
 e_D={\rho_D(G)\over\rho_D(K_n)}-1,
\]

then

\[
 \boxed{e_B+e_D=\mathsf T+\mathsf C-\mathsf E,}        \tag{14}
\]

where

\[
 \mathsf T=
 \sum_Sq^{k-1}\left\{z_B(S)-{C_M\over n-1}z_D(S)\right\}
                     \{A(S)-B(S)\},                   \tag{15}
\]

\[
 \mathsf C=
 -\sum_S{q^{k-1}z_D(S)\over n-1}
       (C_M-C_R)\{B(S)-B_0(k)\},                      \tag{16}
\]

\[
 \mathsf E=
 \sum_S{q^{k-1}z_D(S)\over n-1}\mathcal E(S)\ge0.    \tag{17}
\]

Therefore the balanced separator is equivalent to the single explicit
Green inequality

\[
 \boxed{\mathsf T+\mathsf C\le\mathsf E.}             \tag{18}
\]

This is not a relabeling of the signed-cut obstruction alone.  The new term
`T` is the exact mismatch between the Bd Green occupation and the
rank-dependent multiple of the dB Green occupation selected by the sharp
tangent slope.

## 4. What the exact hostile witnesses prove cannot work

The independent verifier solves (4) over `QQ` and checks every equality in
(8)--(18).  The following values are decimals of exact rationals.

| witness | `T` | `C` | `-E` | `e_B+e_D` |
|---|---:|---:|---:|---:|
| weighted star | -0.578602 | 0.230428 | -0.173610 | -0.521783 |
| separated path | -0.497667 | 0.288308 | -0.285143 | -0.494502 |
| nearest five-edge point | -0.000832 | 0.051241 | -0.056180 | -0.005772 |
| weakly completed star | -0.144249 | 0.192331 | -0.147452 | -0.099370 |
| exact dB-amplifying windmill | -0.044018 | 83.625667 | -83.817371 | -0.235722 |
| affine lower-multiplier witness | -0.021026 | `3.625736977e9` | about `-3.625736977e9` | -0.155561 |

These examples give four exact route closures.

1. **No statewise sign.**  On the weighted star, state `{0}` contributes
   exactly `11/144>0` to `T`.  Other states contribute positively to
   `C-E`.  Thus neither integrand is pointwise nonpositive.

2. **No fixed-rank sign.**  The complete rank-one contribution on the same
   weighted star is positive (`1.84797...`), while rank three supplies the
   compensating negative mass.  On the nearest five-edge graph, the complete
   rank-two contribution is positive (`0.03722...`).

3. **No separate aggregate signs.**  The path

       4 --(1033)-- 0 --(1)-- 3 --(6)-- 1 --(1269)-- 2

   has, exactly,

\[
 \mathsf T=3.452073311169\ldots>0,\quad
 \mathsf C-\mathsf E=-3.983684719192\ldots,
\]

   and total `-0.531611408022...`.  Hence even the attractive aggregate
   conjecture `T<=0`, which held on the original ten hostile witnesses, is
   false.

4. **The exact singleton tradeoff does not choose the coefficient.**  One
   natural graph-sensitive proposal chooses `lambda(G)` so that

\[
 \lambda\{\bar q_B-q_B(K_n)\}
 +(1-\lambda)\{\bar q_D-q_D(K_n)\}=0,                 \tag{19}
\]

   where `q_U` is the exact probability of reaching two mutants before
   extinction.  On the rationalized nearest five-edge graph this gives
   `lambda=0.9654023168...`, but

\[
 \lambda x+(1-\lambda)y=1.00020063624\ldots>1         \tag{20}
\]

   exactly.  Establishment-level balancing therefore does not yield a
   fixation separator.

## 5. An exact vertex-bilinear product-chain Farkas barrier

There is also an exact obstruction to a natural attempt to couple the two
rules pointwise.  Let `Q_B` be the additive Bd dual generator on nonempty
sets and `Q_D` the recurrent proper-set block of the geometric-union dB
dual.  The normalized fixation sum is the normalized sum of their stationary
mean ranks.  If `F_0(A,B)` denotes the sum of the two complete-graph radial
Poisson solutions, a sufficient proof would be

\[
 (Q_B\otimes I+I\otimes Q_D)(F_0+\psi)(A,B)
 \mathrel{\ge}{|A|\over m_B(K_3)}+{|B|\over m_D(K_3)}-2              \tag{21}
\]

at every product state.  Integrating (21) under the actual product
stationary law would prove the balanced separator.

Even allowing a fully vertex-labelled bilinear correction

\[
 \psi_C(A,B)=\sum_{i,j=0}^2 C_{ij}{\bf1}_{i\in A}{\bf1}_{j\in B},    \tag{22}
\]

with arbitrary real `3 by 3` matrix `C`, (21) is infeasible on the weighted
path whose leaves `0,1` attach to center `2` with weights `1,17`.
Writing the 42 inequalities as `M vec(C)<=b`, the exact verifier supplies a
ten-atom probability vector `Lambda` for which

\[
 \Lambda^\mathsf TM=0,
 \qquad
 \Lambda^\mathsf Tb=
 -{2914284766335459263489\over11053845274742764346205}<0.           \tag{23}
\]

This is a literal rational Farkas contradiction.  It is stronger than a
failed numerical optimization and allows arbitrary vertex dependence within
the bilinear class.  It does **not** exclude nonlinear vertex-sensitive
potentials or an aggregate capacity argument.  Nor is the path a fixation
counterexample: its exact balanced slack is

\[
 2-x-y={236336950\over700859439}>0.                                \tag{24}
\]

Thus the obstruction is specifically to enforcing the global conclusion by
a pointwise radial-plus-bilinear product-chain drift inequality.

## 6. The precise remaining obstruction

The balanced conjecture is now reduced to (18), but every decomposition of
its left side into an independently signed state, rank, cut, dispersion, or
occupation-mismatch term is exactly false.  Positive terms can be cancelled
only across both rules and across different mutant ranks.

There is one exact cross-rank structure still available.  Let `U_U(S)` and
`D_U(S)` be the total up and down rates of (2) or (3).  Equation (4) implies
the rank-cut flow law

\[
 \sum_{|S|=k}z_U(S)U_U(S)
 -\sum_{|S|=k+1}z_U(S)D_U(S)=\rho_U(G),
 \qquad1\le k\le n-1.                                 \tag{25}
\]

Thus a successful proof of (18) must couple the graph-sensitive within-rank
geometry in (15)--(17) to the cross-rank Green flows (25), or use an
equivalent global path-reversal/capacity theorem.  Merely averaging the
sharp statewise bridge at one fixed rank cannot work.  Section 5 further
shows that the first vertex-sensitive coupling must be nonlinear,
nonpointwise, or richer than a degree-`(1,1)` Boolean correction.

This coupled Green-flow inequality is the **SPECIFIC MINIMAL OBSTRUCTION**
left by this cycle.  It remains open; no universal theorem is claimed.

## 7. Verification

Run the three compact exact route obstructions:

```bash
.venv/bin/python universal_simultaneous_amplification/phase4_landmark_closure/threshold/endpoint_hostile_exact/verify_balanced_poisson.py
```

Run all ten original hostile witnesses and the additional mismatch path:

```bash
.venv/bin/python universal_simultaneous_amplification/phase4_landmark_closure/threshold/endpoint_hostile_exact/verify_balanced_poisson.py --all
```

The implementation uses FLINT rational linear algebra for the transposed
Green systems, checks the tangent-square bridge state by state, and checks
the Poisson identity exactly rather than from sampled fitness values.

Run the exact vertex-bilinear product-chain Farkas certificate:

```bash
.venv/bin/python universal_simultaneous_amplification/phase4_landmark_closure/threshold/endpoint_hostile_exact/verify_vertex_bilinear_farkas.py
```

This implementation rebuilds both dual generators from their atomic update
rules, solves the complete radial Poisson equations over `QQ`, verifies all
nine annihilation identities, and separately verifies that the witness graph
obeys the balanced fixation inequality.
