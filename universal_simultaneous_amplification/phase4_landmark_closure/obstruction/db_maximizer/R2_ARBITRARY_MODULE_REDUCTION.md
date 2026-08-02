# Conditional `r=2` reduction for arbitrary weak satellite modules

Status: **THE REDUCTION THEOREM IS PROVED.  THE TWO MODULE INVARIANTS ARE
OPEN.**  This note isolates a precise global principle that would extend the
clique-satellite obstruction to arbitrary fixed modules.

## 1. Module quantities

Let `H` be any finite connected undirected weighted graph on `m>=2` vertices,
with weighted degrees `delta_v`.  Define exact singleton fixation values

\[
 \alpha_v=\rho_{\rm dB}(H,2\mid\{v\}),\qquad
 \beta_v=\rho_{\rm dB}(H,1/2\mid\{v\}),
\]

and put

\[
 B_H=\sum_v\alpha_v,qquad
 C_H=\sum_v{\alpha_v\over\delta_v},\qquad
 D_H=\sum_v{\beta_v\over\delta_v},\qquad
 R_H={C_H\over D_H}.
\]

The proposed module invariants are

\[
 \tag{M1} B_H\le {m\over2},
\]

and, whenever `2*B_H-m+1>0`,

\[
 \tag{M2}
 R_H\le {B_H\over2B_H-m+1},
 \quad\hbox{equivalently}\quad
 (2B_H-m+1)C_H\le B_HD_H.
\]

Both are scale invariant.  Cliques satisfy (M1) strictly and (M2) with
equality.  Exact and numerical tests are recorded below, but no universal
proof of either invariant is claimed here.

## 2. Conditional theorem

Fix `c>=3`.  Take a unit-weight clique core `K_c` and any fixed collection of
connected weighted modules `H_j`.  Join every core vertex to every vertex of
`H_j` by an edge of weight `epsilon*b_j`, where `b_j>0`, and put no edges
between distinct modules.  If every `H_j` satisfies (M1)--(M2), then, at
fitness two,

\[
 \limsup_{\epsilon\downarrow0}\rho_{\rm dB}(G_\epsilon,2)
 \le {n-1\over2n}<\rho_{\rm dB}(K_n,2).
\]

Thus a proof of (M1)--(M2) for all finite weighted modules would extend the
proved clique-satellite theorem to arbitrary fixed weak satellites.

## 3. Exact rare-event reduction

Use the core notation

\[
 T=2^{c-2},\qquad
 \alpha_c={(c-1)T\over c(2T-1)},\qquad
 \beta_c={\alpha_c\over T},\qquad
 A=c\alpha_c,qquad d={A\over2T}.
\]

Fix one module `H=H_j`, of size `m`, and suppress the common factors
`epsilon*b_j` and `1/n`.  If the module is mutant and the core resident, the
effective rate at which it establishes a mutant core is

\[
 {2cm\alpha_c\over c-1}.
\]

The adverse rate is

\[
 {c\over2}\sum_v{\beta_v\over\delta_v}={cD_H\over2}.
\]

Indeed, a mutant module vertex `v` is replaced from the resident core at
leading probability `c*epsilon*b_j/(2*delta_v)`; the introduced resident then
fixes inside `H` with probability `beta_v`.  Hence the first directional odds
are

\[
 z_H={4m\alpha_c\over(c-1)D_H}.
\]

If the core is mutant and the module resident, the favorable module-fixation
rate and adverse core-loss rate are respectively

\[
 2cC_H,
 \qquad
 {cm\beta_c\over2(c-1)}.
\]

The two directional odds therefore have exact product

\[
 z_H\,{4(c-1)C_H\over m\beta_c}=16TR_H.
\tag{1}
\]

Put `y_H=z_H/(16*T*R_H)`.  Across several modules the adverse core-loss rates
are proportional to `m_j*b_j`; thus the probability that some module becomes
mutant before the core is lost is `1/(1+y_*)`, where `y_*` is the weighted
harmonic mean of the `y_(H_j)`.  A locally mutant module establishes the core
before being lost with probability `z_H/(1+z_H)`.

Exactly as in the clique proof, separation of time scales and deletion of
all later failures give

\[
 \limsup_{\epsilon\downarrow0}n\rho_{\rm dB}(G_\epsilon,2)
 \le {A\over1+y_*}
 +\sum_j B_{H_j}{z_{H_j}\over1+z_{H_j}}.
\tag{2}
\]

## 4. Continuous scalar lemma from (M1)--(M2)

Write `s_H=m/2-B_H`.  The full local-establishment budget exceeds `(n-1)/2`
by

\[
 d-\sum_js_{H_j}.
\]

By (M1), every `s_H>=0`.  Choose a module with `y_H<=y_*`.  It is enough to
prove, for every `y>0`,

\[
 {Ay\over1+y}+{B_H\over1+16TR_Hy}\ge d-s_H.
\tag{3}
\]

If the right side is nonpositive, this is immediate.  Otherwise set

\[
 e={1\over2}-s_H=B_H-{m-1\over2}.
\]

Then `1/2-d<e<=1/2`.  By (M2), `R_H<=B_H/(2e)`, and because `m>=2`,
`B_H>=(1/2)+e`.  The function `B/(1+constant*B)` is increasing in `B`, while
the left side of (3) is decreasing in `R_H`.  Consequently its module term
is at least

\[
 f_e(y)={e+1/2\over1+8T(e+1/2)y/e}.
\]

Put `delta=1/2-e`, so `0<=delta<d`.  Apart from the core term, the required
gap is

\[
 g(\delta)=f_{1/2-\delta}(y)+\delta.
\]

Let `kappa=8Ty`.  In the variable `e`,

\[
 f_e(y)-e
 =-{e(2e\kappa+\kappa-1)\over2e\kappa+2e+\kappa},
\]

and its derivative is

\[
 -{\kappa(2e+1)\{2e\kappa+2e+\kappa-1\}
    \over(2e\kappa+2e+\kappa)^2}.
\]

The braced affine factor is increasing in `e`.  As `delta` increases and `e`
decreases, `g'(delta)` can change sign only from positive to negative.  Thus
`g` has no interior minimum on `[0,d]`; its minimum occurs at an endpoint.

At `delta=0`, (3) is precisely the already proved pair inequality

\[
 {Ay\over1+y}+{1\over1+16Ty}\ge d.
\]

At `delta=d`, the right side of (3) is zero, while its left side is
nonnegative.  This proves the continuous scalar lemma and hence the
conditional theorem.

## 5. Stationary-dual interpretation

Let `Pi` be the stationary law of the exact dB branching--coalescing dual of
`H` at fitness two.  Boolean duality and type complementation give

\[
 \alpha_v=\Pr_\Pi(v\in A),\qquad \beta_v=\Pi(\{v\}).
\]

Therefore

\[
 B_H=E_\Pi|A|,qquad
 C_H=E_\Pi\sum_{v\in A}{1\over\delta_v},\qquad
 D_H=\sum_v{\Pi(\{v\})\over\delta_v}.
\]

In this language (M2) is the stationary inequality

\[
 \{2E|A|-m+1\}
 E\sum_{v\in A}{1\over\delta_v}
 \le
 E|A|\sum_v{\Pi(\{v\})\over\delta_v}.
\tag{4}
\]

For a weighted-regular module, (4) reduces to

\[
 \Pi(|A|=1)\ge2E|A|-m+1.
\]

This is the precise higher-order stationary principle exposed by the macro
reduction.

The conjectured complementary-level inequality at `r=2`,

\[
 k\Pi(|A|=k)\le(m-k)\Pi(|A|=m-k),\qquad k>m/2,
\]

would imply (M1): after pairing levels it gives
`E|A|^2<=(m/2)E|A|`, and Jensen then gives `E|A|<=m/2`.  It does not by itself
imply the degree-weighted singleton inequality (4).

## 6. Verification status

- **PROVED:** the conditional reduction and scalar endpoint argument.
- **EXACTLY COMPUTED:** (M1)--(M2) on the rational small-graph library in
  `verify_r2_module_invariants.py`.
- **NUMERICALLY OBSERVED:** (M1)--(M2) on every connected unweighted graph
  through seven vertices and tens of thousands of heterogeneous weighted
  samples through eight vertices.
- **OPEN:** universal proofs of (M1) and (M2).

No item in the computational audit is used as a proof of the open module
invariants.
