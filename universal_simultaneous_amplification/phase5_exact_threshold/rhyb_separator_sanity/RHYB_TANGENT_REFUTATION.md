# The dilute-hybrid tangent is not a universal separator

Date: 2026-08-13 (America/Los_Angeles)

No literature search or external communication was used.

## 1. Candidate forced by the hybrid tangency

Let

\[
 P(r)=r^6-8r^5+22r^4-30r^3+21r^2-6r+1,                 \tag{1}
\]

and let `R_hyb` be its unique root in `(3/2,151/100)`.  A leading response
vector is written `(B,D)`, with positive coordinates meaning Bd and dB gain
over the complete reference at that fitness.

The ordinary leaf vector is

\[
                         \ell(r)=\left({1\over r-1},-1\right). \tag{2}
\]

Therefore the unique linear functional of the form `D+qB` that annihilates
leaves is obtained by `q=r-1`:

\[
                         \mathcal S_r(B,D)=D+(r-1)B.        \tag{3}
\]

At `r=R_hyb`, the optimized strong `K_2` response also obeys
`S_r=0`; this is exactly the pair--leaf tangency defining (1).  Hence (3) is
the unique supporting-functional candidate forced by that equality class.

If a matching upper proof at `R_hyb` were a universal affine tangent, it
would assert

\[
                         \mathcal S_{R_hyb}(B_G,D_G)\le0    \tag{4}
\]

for every admissible graph response.  The stored exact corpus refutes (4).

## 2. Stored weak-cut witness

Use the already certified separated two-complete-module family with module
orders `A=2`, `B=20` and internal degree ratio

\[
                         \sigma={19\over137}.               \tag{5}
\]

Let `rho_B(r),rho_D(r)` be its exact weak-cut fixation limits, as derived by
the two-state rare-event trace, and let `rho_B^K(r),rho_D^K(r)` be the
complete-graph baselines of order `22`.  Put

\[
 x(r)={\rho_B(r)\over\rho_B^K(r)},\qquad
 y(r)={\rho_D(r)\over\rho_D^K(r)}.                         \tag{6}
\]

The exact formulas used by the replay are

\[
 \rho_B={2\over22}b_2{z_{BA}\over1+z_{BA}}
        +{20\over22}b_{20}{z_{BB}\over1+z_{BB}},           \tag{7}
\]

\[
 \rho_D={2\over22}d_2{z_{DA}\over1+z_{DA}}
        +{20\over22}d_{20}{z_{DB}\over1+z_{DB}},           \tag{8}
\]

where

\[
 b_m={1-1/r\over1-r^{-m}},\qquad
 d_m={m-1\over m}{1-1/r\over1-r^{1-m}},                   \tag{9}
\]

and the four positive gate odds are the standard exact weak-cut expressions
printed in the verifier.

Consider the normalized tangent score

\[
                         H(r)=y(r)-1+(r-1)\{x(r)-1\}.       \tag{10}
\]

Exact rational algebra gives a positive denominator on `r>1`.  Its numerator
has no root in

\[
 I=\left[{1502856912\over10^9},{1502856913\over10^9}\right], \tag{11}
\]

and is positive at the left endpoint.  Meanwhile Sturm isolation proves
that `P` has exactly one root in `I`.  Consequently

\[
 \boxed{H(R_hyb)>0.}                                      \tag{12}
\]

For orientation only,

\[
 H(R_hyb)=0.0000843654461103002\ldots.                    \tag{13}
\]

This is an exact sign conclusion; the decimal is not used in the proof.
Thus the hybrid tangent (3) is **not** a universal separator at its own
algebraic threshold.

The connected finite rational graph from the stored corpus uses cross
weight `1/500`; it happens to lie on the negative side of (3) at
`R_hyb`.  That does not rescue universality: the weak-cut family is realized
by connected graphs with any positive cross weight tending to zero, and the
strict gap (12) persists for all sufficiently small positive rational cross
weights by continuity of finite absorbing probabilities.

## 3. Exact interpretation

The witness has `x<1<y`: it is not a simultaneous amplifier.  It refutes
only the affine supporting functional.  Therefore it neither raises the
proved lower bound nor disproves the renewed hypothesis

\[
                         R_sim=R_hyb.                       \tag{14}
\]

What it proves is that any matching upper bound at `R_hyb` must be nonlinear
or graph-dependent.  In particular, no proof can simply globalize the
leaf-eliminated tangent inequality `D+(R_hyb-1)B<=0` from the separated
module library.

## 4. Minimal matching-upper theorem

Write the normalized fixation point at `R=R_hyb` as

\[
 X_G={\rho_{Bd}(G,R)\over\rho_{Bd}(K_n,R)},\qquad
 Y_G={\rho_{dB}(G,R)\over\rho_{dB}(K_n,R)}.                \tag{15}
\]

The exact endpoint theorem needed for a matching upper bound is the
nonlinear disjunction

\[
 \boxed{\min\{X_G,Y_G\}\le1\quad\hbox{for every finite
 connected weighted }G.}                                 \tag{16}
\]

For the asymptotic threshold definition, the minimally sufficient sequence
form is instead

\[
 \boxed{\text{every graph sequence has infinitely many }k\text{ with }
                    \min\{X_{G_k},Y_{G_k}\}\le1.}          \tag{17}
\]

Equivalently, no graph sequence is eventually contained in the open
quadrant `{X>1,Y>1}`.  The superficially similar statement
`liminf min(X_k,Y_k)<=1` is **not** sufficient: `X_k=Y_k=1+1/k`
satisfies that limit inequality while strictly amplifying at every index.
This distinction is essential for dilute constructions, whose gains tend to
zero.

The equality class necessarily contains complete/isothermal sequences.  At
the tangent level it also contains the optimized dilute pair--leaf direction
and its zero-density limit.  The weak-cut witness shows that equality cannot
be characterized by a single supporting line; a valid rigidity theorem must
use the full nonlinear pair `(X,Y)` or structural information about the
limiting graph sequence.

## 5. Compactness/tangent-cone reduction target

The proof-first route to (17) is a response-germ theorem rather than a new
separator guess.  Put

\[
 \Delta_k=(X_{G_k}-1,Y_{G_k}-1),\qquad
 \epsilon_k=\|\Delta_k\|_\infty.                         \tag{18}
\]

At the first nonzero scale, compactness gives a subsequential direction
`v_1=lim Delta_k/epsilon_k`.  A valid tangent obstruction must put at least
one coordinate of `v_1` on the nonpositive side.  If that coordinate is
zero, this has not yet ruled out strict amplification: one must pass to the
next smaller response scale and inspect that coordinate again.  Recursively,
for a complete hierarchy

\[
 \Delta_k=\epsilon_{1,k}v_1+\epsilon_{2,k}v_2+\cdots,
 \qquad \epsilon_{j+1,k}=o(\epsilon_{j,k}),               \tag{19}
\]

the first nonzero coefficient in at least one coordinate must be negative
(or that coordinate must vanish exactly).  This is the required
**lexicographic response-cone obstruction**.  A first-order cone statement
alone is insufficient on a zero tangent such as the optimized pair--leaf
ray.

The structural target is correspondingly scale-sensitive.  Exceptional
vertices may have negligible initialization mass but order-one dynamical
influence (the hybrid hub is the canonical example), so they cannot simply
be deleted.  They must remain in the macro chain after exact Schur/trace
elimination of the fast states.  Every trace and mixing error must be
`o(epsilon_k)`, not merely `o(1)` or `o(module density)`.

A precise bulk/dilute dichotomy, the exact bounded-module dual-moment
reduction, and the first missing stationary inequality are recorded in
`../rhyb_compactness_reduction/RHYB_COMPACTNESS_AND_DUAL_MOMENT.md`.
Failure of that dichotomy identifies the only remaining lower mechanisms:
non-dilute correlations, growing modules with nonuniform trace error, or a
positive-density interaction limit.

## 6. Exact replay

Run

```text
PYTHONDONTWRITEBYTECODE=1 ../../../.venv/bin/python -B verify_rhyb_tangent_refutation.py
```

It reconstructs the hybrid root, the stored weak-cut formulas, and the
Sturm/root-isolation certificate proving (12).
