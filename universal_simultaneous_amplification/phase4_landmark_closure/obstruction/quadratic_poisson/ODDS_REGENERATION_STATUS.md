# Stationary regeneration for the component-odds conjecture

Date: 2026-08-02 (America/Los_Angeles)

## Status

The stationary-regeneration reduction below is **PROVED**.  The proposed
arbitrary-start stopped-count lemma is **FALSE**, with an exact symmetric
four-vertex counterexample.  The component-odds inequality itself remains
**OPEN**:

\[
 \frac{p_i}{1-p_i}\stackrel{?}{\le}
 2\sum_vP_{vi}p_v.                                      \tag{1}
\]

Here `p_i` is the stationary occupancy marginal of the exact geometric-union
dB dual at fitness `r=2`.  If (1) holds, summing over `i` and using the row
stochasticity of `P` gives

\[
 \sum_i\frac{p_i}{1-p_i}\le2\sum_i p_i.
\]

Convexity then implies `n^{-1} sum_i p_i <= 1/2`.

## 1. Exact stationary interval reduction

Use independent rate-one target clocks, retaining null rings at holes.  Fix
a vertex `i` and inspect the open interval between two consecutive rings of
its clock.  Immediately after the first ring, `i` is a hole: if it was
occupied, its geometric burst removes it, and if it was already a hole the
ring is null.  Until the next ring, no event can remove `i`.  Moreover, since
`P_ii=0`, the evolution of the outside set `V\{i}` is autonomous during this
interval.

Let `N_i` be the total *raw multiplicity* of samples equal to `i` in all
outside bursts during the interval.  Then

\[
 i\text{ is occupied before the next ring}
 \quad\Longleftrightarrow\quad N_i\ge1.
\]

The clock rings see the stationary law, so this gives exactly

\[
 p_i=\Pr(N_i\ge1),\qquad 1-p_i=\Pr(N_i=0).              \tag{2}
\]

A burst from occupied `v` has mean raw `i`-multiplicity `2P_vi`.  The mean
length of a clock interval is one.  Renewal reward, or direct resolvent
calculation, therefore gives

\[
 \mathbb E N_i=2\sum_vP_{vi}p_v.                        \tag{3}
\]

Consequently (1) is equivalent to the single stopped-count inequality

\[
 \boxed{\Pr(N_i=0)\bigl(1+\mathbb E N_i\bigr)\ge1.}     \tag{4}
\]

The exact verifier constructs the post-`i`-clock outside law `eta_i`.  If
`u_i(Y)` and `g_i(Y)` are respectively the zero-count probability and mean
count before an independent `Exp(1)` kill from outside start `Y`, it checks

\[
 1-p_i=\sum_Y\eta_i(Y)u_i(Y),\qquad
 2\sum_vP_{vi}p_v=\sum_Y\eta_i(Y)g_i(Y)                 \tag{5}
\]

over exact rationals.

## 2. Exact retraction of the arbitrary-start lemma

It is tempting to strengthen (4) to

\[
 u_i(Y)\bigl(1+g_i(Y)\bigr)\ge1
 \quad\text{for every outside start }Y.                 \tag{6}
\]

This is false even for a connected undirected symmetrically weighted `K_4`.
In edge order `(01,02,03,12,13,23)`, take

\[
 (89,21,1,34,1,2),qquad i=2,qquad Y=\{0,1,3\}.
\]

Direct solution of the two stopped resolvents gives

\[
 u_2(Y)=\frac{61559471798429}{132695120588194},
\]

\[
 g_2(Y)=\frac{512569127916482706}{462926484050395051},
\]

and hence

\[
 u_2(Y)(1+g_2(Y))-1
 =-\frac{1377091010169587489700398984141}
 {61428085624535837699389186627894}<0.                 \tag{7}
\]

Thus only the special stationary post-clock mixture in (5) can prove (4).
An earlier discovery report said that (6) survived broad exact tests through
five vertices.  Equation (7) retracts that claim: those tests did not
establish the stated lemma.

## 3. Sound unbatched first-marginal comparison

Let `nu` be the stationary law of the unbatched process in which every
occupied `v`

* neutrally moves to one row-`P` sample at rate one, and
* selectively retains itself and adds one row-`P` sample at rate one.

Put `a_vi=E_nu[x_v(1-x_i)]`.  The exact coordinate balance is

\[
 p_i^{\rm un}=2\sum_vP_{vi}a_{vi}.                      \tag{8}
\]

If one instead applies the batched dB generator to `nu`, its `i`-coordinate
drift is

\[
 \sum_v\frac{2P_{vi}}{1+P_{vi}}a_{vi}-p_i^{\rm un}
 =\sum_v\left(\frac{2P_{vi}}{1+P_{vi}}-2P_{vi}\right)
 a_{vi}\le0.                                            \tag{9}
\]

This is an exact, graph-independent first-marginal fact.  It does **not** by
itself prove that the batched stationary law is dominated by `nu`: one-step
super-invariance fails for general upward events, and marginal drift need not
remain ordered under iteration.  A valid stationary comparison principle is
still required.

## 4. Verification

Run

```text
python3 verify_odds_regeneration.py
```

The script uses only `fractions.Fraction`.  It builds both exact generators,
solves their stationary systems, constructs both stopped resolvents, verifies
(5) at all four targets, verifies the strict counterexample (7), and checks
(8)--(9) coordinate by coordinate.

