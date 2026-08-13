# Regular-module reduction of the minimal stationary product

Date: 2026-08-13 (America/Los_Angeles)

No external communication or broad graph search was used.

## Status

For a connected regular weighted module, the portal-general minimal product
reduces exactly to one vertexwise statement about the dB dual:

\[
 \boxed{
 \pi_D(\{i\})\ge r^2[\rho_D-p]_+
 \quad(i\in V),\qquad p={r-1\over r}.}                 \tag{VDR}
\]

This note verifies that algebraic reduction and gives two exact structural
forms of `(VDR)`:

1. a singleton-versus-mean-rank form; and
2. a one-hole/collision-budget form.

The first-level singleton balance alone cannot prove the inequality: an
explicit normalized pseudo-law keeps every singleton equation while moving
arbitrarily much probability to rank three and violating `(VDR)`.  Hence a
valid proof must use a genuine higher-rank stationarity equation.  No graph
counterexample was found or claimed, and the universal regular sign remains
**OPEN**.

## 1. Exact regular Bd law

Let `G` have order `s>=2` and scale its common weighted degree to one.  Its
request kernel `P` is symmetric and doubly stochastic.  For the Bd dual,
the weighted-adjoint potential vanishes and the reversible reference law is

\[
 \pi_B(A)={ (r-1)^{|A|}\over r^s-1},
 \qquad \varnothing\ne A\subseteq V.                  \tag{1}
\]

Thus every Bd singleton atom is the same number

\[
 u={r-1\over r^s-1},                                  \tag{2}
\]

and its stationary density is

\[
 \rho_B={1\over s}\sum_A|A|\pi_B(A)
 ={(r-1)r^{s-1}\over r^s-1}.                         \tag{3}
\]

The key cancellation is

\[
 \boxed{\rho_B-p={u\over r}.}                         \tag{4}
\]

It holds for every `s` and every `r>1`.

## 2. Portal-general MP is exactly vertexwise dB repayment

Regularity also makes the physical portal laws equal.  If `x>=0` is a
nonzero portal load, then

\[
 \gamma_i=\alpha_i={x_i\over\sum_jx_j}.               \tag{5}
\]

Consequently

\[
 q_B=u,\qquad
 q_D={\sum_i x_i v_i\over\sum_i x_i},
 \qquad v_i=\pi_D(\{i\}).                             \tag{6}
\]

The Bd excess is positive by (4), so substituting (4)--(6) into

\[
 q_Bq_D\ge r^3[\rho_B-p]_+[\rho_D-p]_+               \tag{MP}
\]

and cancelling `u>0` gives

\[
 {\sum_i x_iv_i\over\sum_i x_i}
 \ge r^2[\rho_D-p]_+.                                \tag{7}
\]

Since nonnegative portal loads may concentrate at a single vertex, (7)
holds for every portal if and only if `(VDR)` holds at every vertex.
Conversely, averaging `(VDR)` with weights `x_i/sum_j x_j` proves (7), so
this is an equivalence, not a strengthening.

The statement is automatic whenever `rho_D<=p`.  On the active branch it is
equivalently

\[
 \boxed{
 s\pi_D(\{i\})\ge r^2\{m-sp\},
 \qquad m=\mathbb E_{\pi_D}|A|.}                     \tag{8}
\]

This already shows that the regular MP problem is much weaker than proving
that the complete graph maximizes dB fixation.

## 3. Exact singleton/hole form

Put

\[
 H_{vi}=h_r(P_{vi})={rP_{vi}\over1+(r-1)P_{vi}},
 \qquad T_i=\sum_vH_{vi}.                             \tag{9}
\]

For a random stationary dB-dual set `A`, write `C=V\setminus A` and

\[
 W(C)=\sum_{i,v\in C}{H_{vi}\over1+T_i},\qquad
 \sigma=\sum_i{1\over1+T_i}.                         \tag{10}
\]

Stationarity of each occupancy indicator gives the exact hole identity

\[
 \mathbb E|C|=\sigma+\mathbb EW(C),                  \tag{11}
\]

and hence

\[
 \boxed{
 s(\rho_D-p)={s\over r}-\sigma-\mathbb EW(C).}       \tag{12}
\]

Therefore `(VDR)` is exactly

\[
 \boxed{
 \pi_D(\{i\})\ge {r^2\over s}
 \left[{s\over r}-\sigma-\mathbb EW(C)\right]_+.}  \tag{13}
\]

Equation (13) exposes the entire active deficit: dB can exceed `p` only if
the deterministic one-hole budget `sigma` and the stationary two-hole
collision budget `E W` together fall below `s/r`.

There is also an exact local entrance identity.  Since one dB update can
land at singleton `{i}` only from a singleton `{j}` or a doubleton
`{i,j}`, stationarity gives

\[
 \boxed{
 v_i=\sum_jg_r(P_{ji})\{v_j+b_{ij}\},\qquad
 g_r(z)={z\over r-(r-1)z},}                           \tag{14}
\]

where `b_ij=pi_D({i,j})`.  On a regular graph `P_ji=P_ij`; thus the
left of (13) is fed by the same symmetric conductances as its hole budget.
Equations (13)--(14) are the smallest natural singleton/hole formulation of
the remaining theorem.

## 4. Why first-level balance cannot close the theorem

The higher-rank term in (13) is not replaceable using only (14), positivity,
and normalization.  Fix the complete kernel on `s=8`, and let
`(v_i^0,b_{ij}^0)` be the genuine dB singleton and doubleton atoms at the
chosen `r`.  Because (14) is homogeneous in these atoms, for every
`epsilon in (0,1)` the arrays

\[
 v_i^{\epsilon}=\epsilon v_i^0,\qquad
 b_{ij}^{\epsilon}=\epsilon b_{ij}^0                 \tag{15}
\]

still satisfy every singleton equation.  Put all residual probability on
one rank-three state.  This produces a normalized nonnegative pseudo-law;
it need not satisfy the rank-two/rank-three equations.

As `epsilon` tends to zero,

\[
 \rho^{\epsilon}\longrightarrow {3\over8}.           \tag{16}
\]

For every `r` in the exact isolating interval

\[
                         {3\over2}<r<{151\over100},
\]

one has

\[
 {3\over8}-{r-1\over r}>0,                           \tag{17}
\]

while `v_i^epsilon` tends to zero.  Hence for all sufficiently small
`epsilon`,

\[
 v_i^\epsilon<r^2\{\rho^\epsilon-p\}                 \tag{18}
\]

at every vertex.  Thus no proof based only on (14), nonnegativity, and
normalization can prove `(VDR)` at `R_hyb`.  At least one actual
higher-rank stationarity equation, or an equivalent killed-Green/tree
identity, is logically necessary.

This is a proof-route obstruction, not a graph counterexample.

## 5. Exact class checks and the remaining theorem

The verifier checks the reduction symbolically in `s,r`, verifies (1)--(4)
directly on one noncomplete regular rational `K_4`, and rebuilds the exact
dB dual on that graph.  It checks `(11)--(14)` and a strict instance of
`(VDR)` at `r=3/2`.  It also constructs the rank-three pseudo-law in Section
4 exactly and verifies its strict violation.

For order two, `(VDR)` is elementary and strict.  For order three, every
regular connected weighted graph is the complete triangle, so it follows
from the exact count chain.  The first genuinely nonhomogeneous class is
regular order four; the replay gives finite evidence there, not an
all-parameter theorem at `R_hyb`.

The proof-first regular target is now precise:

> Use a rank-two/rank-three return equation to compare the singleton entrance
> current (14) with the full hole deficit (13).

A separate dB maximizer theorem, an arbitrary-start regeneration inequality,
or a profile induction would be stronger than required and is not assumed.

## 6. Replay

Run

```text
PYTHONDONTWRITEBYTECODE=1 ../../../.venv/bin/python -B \
  verify_regular_reduction.py
```

The replay uses exact arithmetic only.  It proves identities and the stated
finite class checks; it does not assert the open universal sign.
