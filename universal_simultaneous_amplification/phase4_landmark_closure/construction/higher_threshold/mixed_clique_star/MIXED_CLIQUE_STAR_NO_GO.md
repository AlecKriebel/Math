# Arbitrary mixtures of clique satellites: an exact cross-sum no-go

Date: 2026-08-02 (America/Los_Angeles)

## Status

The theorem below is **PROVED for the stated separated growing-center
regime**.  It allows arbitrarily many satellite sizes, internal scales, and
asymptotic proportions.  It is not a universal obstruction: nonclique
satellites, nonstar macrographs, and nonseparated dynamics remain open.

No literature search or external contact was used.

## 1. Model and theorem

Take a clique center whose size tends to infinity and a collection of weakly
attached clique satellites.  A satellite may have any order `l>=2`, any
positive internal edge weight, and any positive common attachment weight to
the center.  The cross edges tend to zero sufficiently rapidly that every
hit component becomes monomorphic before the next type-changing cross event.
The center occupies a vanishing fraction of the vertices, its inverse
invasion probability is negligible compared with the number of satellites,
and all satellites are eventually swept after successful center
establishment.  Satellite orders and the mixture of satellite types may
depend on the population parameter, subject only to these separation and
negligible-center hypotheses.

For fixed fitness `r>=sqrt(2)`, let `R_B` and `R_D` be the limiting fixation
contributions, after local establishment and center handoff, of a uniformly
chosen vertex in the satellite population.  Then

\[
 \boxed{R_B+R_D\le 2\left(1-{1\over r}\right).}       \tag{1}
\]

Consequently no such mixed-clique star can asymptotically amplify both Bd and
dB at the same fixed `r>=sqrt(2)`.  In particular, arbitrary mixtures of
clique satellites cannot improve the proved simultaneous interval beyond
`3/2`.

The claim is a leading separated-limit theorem.  A diagonal finite family is
covered whenever its trace error and center-reversal error are `o(1)`; (1)
then holds with `o(1)` on the right.  This does not control strict gains which
themselves vanish faster than those errors.

## 2. One satellite type

Fix a clique satellite of order `l>=2`.  Write `z>0` for the center internal
weighted degree divided by the satellite internal weighted degree, after the
common attachment factor has been cancelled.  Direct solution of the two
clique count chains gives

\[
 a_l^{\rm Bd}={ (r-1)r^{l-1}\over r^l-1},\qquad
 b_l^{\rm Bd}={r-1\over r^l-1},                    \tag{2}
\]

\[
 a_l^{\rm dB}={l-1\over l}
 { (r-1)r^{l-2}\over r^{l-1}-1},\qquad
 b_l^{\rm dB}={l-1\over l}
 {r-1\over r^{l-1}-1}.                            \tag{3}
\]

Here `a` is forward fixation of one invader and `b` is reverse fixation at
relative fitness `1/r`.  Summing the weak cross-component replacement rates
directly under the two update rules and then sending the center order to
infinity gives the two complete handoff contributions

\[
 B_l(z)={ (r-1)r^{l-1}z\over1+(r^l-1)z},           \tag{4}
\]

\[
 D_l(z)={ (r-1)r^{l-1}\over z+C_l},\qquad
 C_l={rl(r^{l-1}-1)\over l-1}.                    \tag{5}
\]

These expressions include both isolated-satellite establishment and the
probability that the satellite establishes the center.  They are not
branching approximations.  Failed introductions are trace self-loops.

For reference, writing `p=1-1/r`, equations (4)--(5) give

\[
 B_l(z)\ge p\iff z\ge1,
 \qquad
 D_l(z)\ge p\iff
 z\le {r(l-r^{l-1})\over l-1}<1.                 \tag{6}
\]

The last strict inequality follows from strict convexity of `r^{l-1}` at
`r=1`.  Thus no single satellite type amplifies both rules.  The rest of the
proof is needed because a mixture of types could in principle average two
opposite tradeoffs.

## 3. A common affine certificate

Put

\[
 A_l=(r-1)r^{l-1},\qquad a_l=r^l-1.
\]

From (4)--(5),

\[
 B_l(z)+D_l(z)
 =A_l\left\{{z\over1+a_lz}+{1\over z+C_l}\right\}. \tag{7}
\]

When `r>=sqrt(2)` and `l>=2`, both `a_l>1` and `C_l>1`.  The derivative in
`z` vanishes at the unique point

\[
 z_*={C_l-1\over a_l-1},                           \tag{8}
\]

is positive before that point, and is negative afterwards.  Hence (8) is
the global maximum.  Substitution gives

\[
 \max_{z>0}(B_l+D_l)
 =A_l{a_l+C_l-2\over a_lC_l-1}.                   \tag{9}
\]

The difference between the cross-multiplied right side of the desired
bound and (9) factors exactly as

\[
\begin{aligned}
 &2(a_lC_l-1)-r^l(a_l+C_l-2)\\
 &\quad={ (r-1)^2(r^l-2)\over l-1}
 \left(r^{l-2}+2r^{l-3}+\cdots +(l-2)r+(l-1)\right).
                                                               \tag{10}
\end{aligned}
\]

Every factor is nonnegative for `r>=sqrt(2)`, and the last factor is
strictly positive.  Dividing (10) by the positive denominators in (9)
proves

\[
 B_l(z)+D_l(z)\le2p                              \tag{11}
\]

for every `l` and `z`.

## 4. Arbitrary mixtures

Let `omega_j` be the fraction of satellite vertices belonging to type `j`.
Uniform initialization and the rare-component trace give

\[
 R_B=\sum_j\omega_jB_{l_j}(z_j),\qquad
 R_D=\sum_j\omega_jD_{l_j}(z_j),\qquad
 \sum_j\omega_j=1.                               \tag{12}
\]

Equation (11) is the same affine inequality for every order and scale.
Averaging it in (12) proves (1).  If both rules exceeded their large-complete
limits `p`, their sum would exceed `2p`, contradicting (1).

The proof deliberately uses only the separated trace hypotheses stated in
Section 1.  It supplies no reduction from arbitrary graphs to mixed clique
stars and is therefore recorded as a class theorem, not as Alternative O.

## 5. Verification

`verify_mixed_clique_star.py` independently checks:

1. the Bd and dB clique fixation formulas from their one-count recurrences;
2. the handoff expressions (4)--(5) from the finite-center trace formulas;
3. the derivative optimizer (8)--(9);
4. the polynomial factorization (10) for symbolic `l=2,...,12` and exact
   rational spot checks through order 40.

The factorization for general `l` is also immediate by multiplying the
finite geometric-arithmetic sum in (10); the finite symbolic checks are an
independent implementation audit, not the proof of universality.
