# The sharp one-third endpoint separator

Date: 2026-08-08 (America/Los_Angeles)

No literature search or external communication was used.

## Status

The candidate universal endpoint inequality is

\[
 {1\over3}{\rho_{Bd}(G,3/2)\over\rho_{Bd}(K_n,3/2)}
 +{2\over3}{\rho_{dB}(G,3/2)\over\rho_{dB}(K_n,3/2)}
 \leq1.                                                   \tag{1}
\]

This cycle did not prove or refute (1).  It did establish four exact facts.

1. Equation (1) has an exact Green--Poisson reduction with one joint
   occupation term and the same tangent-square loss as the earlier balanced
   reduction.
2. Conditional on the mesoscopic-core establishment lemma now under hostile
   audit, the coefficient is optimal: no fixed affine separator with Bd
   coefficient greater than `1/3` can hold universally.  The rare-state
   algebra for this implication is exact.
3. Inequality (1) is strict for every nonconstant positively weighted
   triangle, by a 24-atom positive polynomial certificate.
4. Statewise, fixed-rank, separately signed Green terms, and an arbitrary
   pointwise common correction are all exactly insufficient.  Thus the open
   step is genuinely a coupled global occupation/flow inequality.

The clique--pendant product counterexamples remain dB suppressors and satisfy
(1).  Nothing here proves no simultaneous amplification at the endpoint.

## 1. Exact normalized drifts

Put `q=2/3`, `P_ij=w_ij/d_i`, and start each continuous type-changing chain
from the uniform singleton law `mu`.  Let

\[
                 (-L_U^T)^\mathsf T z_U=\mu             \tag{2}
\]

define its exact transient Green occupation.  For a mutant set `S` of size
`k`, put

\[
 x_i(S)=\sum_{j\in S}P_{ij},\quad
 A(S)=\sum_{i\in S}(1-x_i),\quad
 B(S)=\sum_{i\notin S}x_i,
\]

and write `c(S)=A(S)-B(S)`.  Direct substitution of the complete-graph
harmonics at fitness `3/2` gives

\[
 {L_B\phi_B(S)\over\rho_B(K_n)}=q^{k-1}c(S),             \tag{3}
\]

\[
 {L_D\phi_D(S)\over\rho_D(K_n)}
 ={q^{k-1}\over n-1}\mathcal D(S).                       \tag{4}
\]

The cancellation is special to the endpoint: the selective factor `3/2`
times the next-rank factor `q` is one.

Put

\[
 B_0(k)={k(n-k)\over n-1},\quad
 C_R={2(n-1)^2\over2n+k-2},\quad
 C_M={3(n-1)^2\over2n+k-3}.                              \tag{5}
\]

The exact tangent identities give

\[
 \mathcal D+C_Mc
 =-(C_M-C_R)(B-B_0)-\mathcal E,                           \tag{6}
\]

where

\[
 \mathcal E=
 C_R\sum_{i\notin S}{(x_i-k/(n-1))^2\over2+x_i}
 +C_M\sum_{i\in S}{(x_i-(k-1)/(n-1))^2\over2+x_i}
 \geq0.                                                   \tag{7}
\]

All formulas follow from the update rules; no sampled fixation value enters.

## 2. The `1:2` Green--Poisson identity

Write

\[
 e_B={\rho_B(G)\over\rho_B(K_n)}-1,\qquad
 e_D={\rho_D(G)\over\rho_D(K_n)}-1.
\]

Dynkin's formula, followed by (6), yields

\[
                  \boxed{e_B+2e_D=\mathsf T_2+2\mathsf C-2\mathsf E}, \tag{8}
\]

where

\[
 \mathsf T_2=\sum_Sq^{k-1}
 \left\{z_B(S)-{2C_M\over n-1}z_D(S)\right\}c(S),       \tag{9}
\]

\[
 \mathsf C=-\sum_S{q^{k-1}z_D(S)\over n-1}
 (C_M-C_R)\{B(S)-B_0(k)\},                              \tag{10}
\]

\[
 \mathsf E=\sum_S{q^{k-1}z_D(S)\over n-1}\mathcal E(S)\geq0. \tag{11}
\]

Consequently (1) is equivalent to the single exact inequality

\[
                         \boxed{\mathsf T_2+2\mathsf C\leq2\mathsf E}. \tag{12}
\]

This is the requested Green--Poisson form.  The `1:2` coefficient enters
twice: algebraically it doubles the dB tangent slope in (9), and the
conditional clique--pendant sharpness calculation below selects the same
coefficient.

## 3. Conditional sharpness of the coefficient

For any fixed positive rational `alpha<1`, take a clique--pendant family in
which the leaf proportion tends to `alpha`.  Conditional on the
mesoscopic-core establishment lemma in the sibling manuscript (currently
under independent hostile audit), the calculation in `AFFINE_SHARPNESS.md`
gives

\[
 x_\infty=1-\alpha+3\alpha\ell(\alpha),\qquad
 y_\infty=1-\alpha,                                      \tag{13}
\]

where

\[
 \ell(\alpha)=
 {8\alpha-3+\sqrt{9+60\alpha-44\alpha^2}\over18\alpha},
 \qquad0<\ell(\alpha)<1,
 \qquad\ell(\alpha)\to1.                                \tag{14}
\]

The crossing coefficient is

\[
 \theta_0(\alpha)={1\over3\ell(\alpha)}\downarrow{1\over3}. \tag{15}
\]

Therefore, if that named lemma survives audit, every putative universal
affine separator with Bd coefficient `theta>1/3` is false.  At the endpoint
coefficient itself the fixed-ray limiting slack is

\[
 1-{x_\infty+2y_\infty\over3}
 =\alpha(1-\ell(\alpha))>0.                              \tag{16}
\]

Moreover

\[
 x_\infty-1=2\alpha+O(\alpha^2),\qquad
 1-y_\infty=\alpha.
\]

Thus the limiting algebra has two units of Bd gain per unit of dB loss.
Subject to the establishment audit, this explains the `1:2` weights without
fitting a decimal constant.

## 4. Exact hostile audit

The verifier checks (8) state by state and after exact Green solves.  Selected
decimal displays of exact rationals are:

| graph | `T_2` | `2C` | `-2E` | `e_B+2e_D` |
|---|---:|---:|---:|---:|
| weighted star | -0.896496 | 0.460856 | -0.347220 | -0.782859 |
| nearest five-edge point | -0.002095 | 0.102482 | -0.112360 | -0.011973 |
| dB-amplifying windmill | 0.161534 | 167.251335 | -167.634742 | -0.221873 |
| affine lower witness | 0.130248 | about `7.251e9` | about `-7.251e9` | -0.138824 |

Across the full ten-graph exact corpus:

- `T_2` can be positive;
- `2C-2E` can be positive;
- a complete fixed-rank contribution can be positive.

Thus (12) cannot be proved by assigning separate signs to its displayed
terms or to each rank.

The exact clique--pendant product witness `G(31,4)` has

\[
 x=1.1218228992\ldots,\qquad y=0.8920029824\ldots,
\]

but its one-third slack is `0.0313903786...>0` exactly.  The stronger product
and balanced arithmetic separators fail there; (1) does not.

## 5. Exact common-potential barrier

A natural stronger certificate seeks an arbitrary transient-set function
`h`, zero at the absorbing states, satisfying

\[
 L_B\left({\phi_B\over\rho_B(K_n)}+2h\right)\leq0,
 \qquad
 2L_D\left({\phi_D\over\rho_D(K_n)}-h\right)\leq0.       \tag{17}
\]

The corrections cancel under the weighted initial average, so (17) would
prove (1).  It is nevertheless infeasible on the four-vertex star with edge
weights `1,10,100`, even when `h` has one independent real value at every
transient subset.  The verifier supplies a seven-atom nonnegative rational
Farkas vector `Lambda` with

\[
 \Lambda^\mathsf T M=0,
 \qquad
 \Lambda^\mathsf T b
 =-{202911350726485\over1421052156585684}<0.             \tag{18}
\]

The same graph has strict positive actual one-third slack.  Hence (18)
refutes the pointwise common-correction architecture, not the separator.

## 6. A complete order-three theorem

For a triangle with positive weights `a,b,c`, exact solution of both six-state
chains gives

\[
 1-{1\over3}{\rho_B(G)\over\rho_B(K_3)}
   -{2\over3}{\rho_D(G)\over\rho_D(K_3)}={N(a,b,c)\over Q(a,b,c)}. \tag{19}
\]

All 127 coefficients of `Q` are positive.  The numerator has a 24-atom
representation

\[
 N=\sum_{(i,j,k),\gamma}\gamma
 \sum_{(x,y,z)\in\operatorname{Perm}(a,b,c)}
 x^iy^jz^k(x-y)^2,                                      \tag{20}
\]

with every displayed coefficient `gamma` positive.  The exact coefficient
table is embedded in `verify_weighted_triangle.py`.  Therefore (1) holds for
every positively weighted triangle, with equality only at `a=b=c`.

This is a class theorem, not a reduction of the all-order problem.

## 7. Precise remaining obstruction

The only surviving target is the global sign (12).  It must use the full
configuration-resolved Green conservation across ranks, or an equivalent
nonpointwise transport/capacity theorem.  Rank totals, statewise tangent
loss, separate Green signs, low-degree common corrections, and local
near-disconnected search candidates are all insufficient.

The universal one-third separator is **OPEN**.  If proved, it immediately
implies the desired endpoint disjunction and hence `R_sim=3/2`.  If refuted,
an exact counterexample must have affine crossing at or below `1/3`; none was
found in this cycle.
