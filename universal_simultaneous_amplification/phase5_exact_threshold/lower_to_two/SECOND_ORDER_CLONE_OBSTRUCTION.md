# Universal second-order obstruction at the portal-clone manifold

Date: 2026-08-08 (America/Los_Angeles)

No literature search or external communication was used.

## Theorem

Fix an order `s`.  In the strong integrated finite-gadget normal form, start
at the portal-clone equality point and take an arbitrary differentiable
one-sided perturbation

\[
 x_i(\varepsilon)=1+\varepsilon\xi_i+O(\varepsilon^2),
 \qquad
 a_{ij}(\varepsilon)=\varepsilon A_{ij}+O(\varepsilon^2),
\]

where `A` is symmetric, loopless, and entrywise nonnegative.  Put

\[
 \alpha_i=\sum_j A_{ij},\qquad c_i=\xi_i+\alpha_i,
 \qquad E_2=\sum_{i<j}A_{ij}^2.
\]

For every fixed fitness `r>1`, the full population response, including the
uniform-singleton subtraction and ordinary-core Poisson term, is

\[
 \boxed{B_H(\varepsilon)=O(\varepsilon^3),}
\]

\[
 \boxed{
 D_H(\varepsilon)=
 -{\varepsilon^2\over r}
 \left\{\sum_i c_i^2+2(r-1)E_2\right\}
 +O(\varepsilon^3).}
\]

Thus every nontrivial first-order departure from the clone manifold points
strictly into dB suppression at second order.  Equality in the displayed
quadratic requires `A=0` and `xi=0`.  Higher-order terms in the parameter
path do not change the quadratic because the first differential of both
responses vanishes at the clone point.

This closes the entire **fixed-order second-order portal-clone escape**, with
arbitrary portal asymmetry and arbitrary positive internal matrix.  The
remainder is not uniform when gadget order grows, so this theorem does not
exclude growing-rank or nonseparated limits.

## Local-chain coefficient extraction

Let `u_U^epsilon(i)` be the probability that the limiting local chain,
started from mutant singleton `i`, produces a surviving core lineage.  Write
`p=(r-1)/r`.  Expanding the exact killed chains defined by the update rules
gives

\[
 u_B^\varepsilon(i)
 =p-{r-1\over r^2}c_i\varepsilon
 +{r-1\over r^3}
 \left\{c_i^2+(r-1)\sum_jA_{ij}c_j\right\}\varepsilon^2
 +O(\varepsilon^3),                                      \tag{1}
\]

and

\[
 u_D^\varepsilon(i)
 =p+{r-1\over r^2}c_i\varepsilon
 -{(r-1)^2\over r^3}
 \left\{c_i^2+\sum_jA_{ij}c_j
 +(r-1)\sum_jA_{ij}^2\right\}\varepsilon^2
 +O(\varepsilon^3).                                      \tag{2}
\]

For completeness, these formulas follow by writing the killed harmonic
system as

\[
 Q_U(\varepsilon)u_U(\varepsilon)=b_U(\varepsilon)
\]

on all nonempty gadget subsets.  At `epsilon=0` the chain has only mutant
recoveries and successful marks; for a set of size `k`, its solution is
`1-r^{-k}`.  Coefficient comparison gives

\[
 Q_0u_1=b_1-Q_1u_0,
 \qquad
 Q_0u_2=b_2-Q_1u_1-Q_2u_0.
\]

For a nonempty mutant set `X`, direct substitution in the first coefficient
equation gives

\[
 u_{B,1}(X)=-{r-1\over r^{|X|+1}}\sum_{i\in X}c_i,
\]

\[
 u_{D,1}(X)={r-1\over r^{|X|+1}}
 \left\{\sum_{i\in X}c_i
 +(r-1)\sum_{\{i,j\}\subseteq X}A_{ij}\right\}.       \tag{2a}
\]

These identities solve the first coefficient system because removal of a
mutant deletes its `c_i` term and every internal edge incident to it, while
an internal type change adds or deletes exactly the corresponding endpoint
and cut-edge terms.  The singleton row of the second coefficient equation
can reach only singleton and two-mutant states, so inserting (2a) gives
(1)--(2).  In a second internal event the chain either returns along the
first edge or uses an edge incident to the newly reached vertex; the former
supplies `sum_j A_ij^2` and the latter supplies `sum_j A_ij c_j`.  This is
an all-order derivation because no other gadget vertex can enter a singleton
equation through second order.

The independent verifier reconstructs these systems directly from the Bd
and dB event definitions with all generic order-three labels left symbolic.

## Cancellation in the full response

Let `U_k` denote the sum over singleton coefficients of order `epsilon^k`.
From (1),

\[
 U_1^B=-{r-1\over r^2}\sum_i c_i,
 \qquad
 U_2^B={r-1\over r^3}
 \left\{\sum_i c_i^2+(r-1)\sum_i\alpha_i c_i\right\}.
\]

Substitution into the exact integrated response formula yields

\[
 [\varepsilon]B_H
 ={r^2U_1^B\over(r-1)^2}+{\sum_i c_i\over r-1}=0,
\]

and

\[
 [\varepsilon^2]B_H
 ={r^2U_2^B\over(r-1)^2}
 +{r\sum_i\xi_i[u_1^B(i)]\over(r-1)^2}
 -{\sum_i\alpha_i c_i\over r-1}=0.                    \tag{3}
\]

Likewise, (2) gives

\[
 U_1^D={r-1\over r^2}\sum_i c_i,
\]

\[
 U_2^D=-{(r-1)^2\over r^3}
 \left\{\sum_i c_i^2+\sum_i\alpha_i c_i
 +2(r-1)E_2\right\}.
\]

The linear dB term cancels.  The quadratic term is

\[
 {r^2U_2^D\over(r-1)^2}
 -{r\sum_i\alpha_i[u_1^D(i)]\over(r-1)^2}
 +{\sum_i\alpha_i c_i\over r-1}
 =-{1\over r}\left\{\sum_i c_i^2+2(r-1)E_2\right\}. \tag{4}
\]

Equations (3)--(4) prove the theorem.

## Consequence for the lower-to-two program

A density or scale matching that approaches a fixed-order clone module
cannot generate a favorable second-order vector: its first possible dB
motion is strictly negative.  Any construction reaching fitness two must
therefore use at least one mechanism outside this normal form, such as a
gadget order growing fast enough to destroy the fixed-order remainder,
correlations between different gadgets, or local/core dynamics without the
integrated one-gadget trace.
