# Compound activation for the four hard H_w switches

## 1. Scope and failed first attempt

This note replaces the false activation step in
*hard333_hw4_fractional_return.md*.  It retains the fractional-population
common-factorial endpoint, but it does not use a pointwise linear
Perron--Frobenius inequality before a mixed carrier is present.

The replacement is a candidate, not a certified theorem.  The finite
geometry, the exact counterexample, and an exhaustive four-node directed
graph contraction are frozen and tested.  The stochastic trace estimates,
service window, endpoint theorem, and recurrence flags all remain false.
The exact four-pair fingerprint is

```text
4b24d4d3437351daf8e1d9b0e84e3d38e5e77147141a44fd9b68f6e1bba68716
```

To see the defect in the first attempt, use the resistance-two support in
the relabeling below and orient the unit-rate cycle

\[
                  2C\to YC\to2Y\to XY\to2C.          \tag{1.1}
\]

At \((X,Y,C)=(n-2,0,2)\), only \(2C\) is enabled.  For every fixed positive
linear form \(R=v_YY+v_CC\),

\[
 \mathcal L_TR=2(v_Y-v_C)=O(1),                       \tag{1.2}
\]

whereas the formerly claimed lower bound
\(cXR-KR^2\) is \(\Theta(n)\).  Thus the old equation (3.1) is false for an
exact selected row and cannot be repaired by choosing different positive
linear weights.

## 2. Universal pure/mixed geometry

Let \(X\) be the dormant species, \(Y\) the other nonservice species, and

\[
                              M=Y+C.                  \tag{2.1}
\]

After relabeling, every top support contains the three pure-transverse
complexes

\[
                         2Y,\quad YC,\quad2C.          \tag{2.2}
\]

The resistance-two rows contain the unique mixed complex \(XY\); the
resistance-one rows contain \(XC\).  The complex \(2X\) is absent.  Thus
pure-to-pure reactions preserve \(M\), a pure-to-mixed reaction lowers it
by one, and a mixed-to-pure reaction raises it by one.  The top linkage
preserves total population exactly.

For resistance one, a single physical \(0\to C\) seed enables \(XC\).
Every outgoing mixed edge is directed to a pure complex and raises \(M\).
For resistance two, two physical seeds enable \(2C\), but an ignition word
may temporarily lower \(M\).

## 3. Exhaustive ignition topology

There are twelve possible directed arcs on four labeled complexes.  The
executable enumerates all \(2^{12}\) simple digraphs and retains the 1,606
which are strongly connected.  Starting from

\[
                         (X,Y,C)=(4,0,2),              \tag{3.1}
\]

it performs exact state-space breadth-first search until \(M=3\).  The
result is

\[
\begin{array}{c|c|c}
\text{graph type}&\text{number}&\text{shortest ignition}\\ \hline
\text{no loss of }M&1420&2\text{ reactions}\\
\text{one-unit temporary loss}&186&3\text{ reactions}.
\end{array}                                           \tag{3.2}
\]

No strongly connected orientation requires a larger loss or a longer
shortest word.  One sparse orientation which genuinely requires the dip is

\[
 2Y\to2C,\quad2Y\to YC,\quad2C\to XY,\quad
 YC\to2Y,\quad XY\to2Y.                               \tag{3.3}
\]

Its word and transverse-mass path are

\[
 2C\to XY\to2Y\to2Y,\qquad 2\to1\to2\to3.            \tag{3.4}
\]

The enumeration proves only the finite directed-cut premise.  It does not
replace the rate comparison below.

## 4. The contracted activation target

Fix an orientation and positive rates.  Constants may depend on them, but
not on \(n\).  Localize at \(M\le\varepsilon n\).

When a mixed carrier is enabled, its propensity contains one factor of
\(X\).  Pure clocks have total order at most \(CM^2\), and the lower death
clock has order at most \(CM\).  Contract the finite pure subgraph until its
first mixed cut, then contract the mixed excursion until its return to a
pure complex.  Strong connectivity and (3.2) exclude a closed unsuccessful
phase.  The quantitative lemma needed for the embedded level chain is

\[
 \mathbb P\{M\text{ reaches }m+1\text{ before a lasting loss}\mid M=m\}
 \ge1-{C\over m}-C{m\over n},                         \tag{4.1}
\]

with a block duration dominated by clocks whose effective successful-cut
rate is at least \(cm(m-1)\).  The first error charges a lower death before
the quadratic pure cut.  The second charges a slow pure/mixed competition
while the carrier population is still small.  The one-unit dip in (3.4)
must be retained inside the block; treating every top reaction as
nondecreasing in \(M\) would be false.

Choose a fixed \(K\) large and then \(\varepsilon\) small.  Equation (4.1)
would dominate the embedded levels from \(K\) to \(\varepsilon n\) by a
uniformly upward-biased walk.  Reaching \(K\) from the one- or two-seed
state is a finite positive-probability trial, because \(K\) is fixed and
every ignition word has length at most three.  Consequently the target
activation statement is

\[
 \inf_{n\ge n_*}\mathbb P\{M\ge\varepsilon n
       \text{ in one localized trial}\}\ge p_*>0.     \tag{4.2}
\]

The number of physical seeds is then compound geometric.  The stopped
birth counting-process martingale, rather than a conditional-Poisson
assertion, should give

\[
 \sup_n\mathbb E e^{sK_{\rm birth}}<\infty.            \tag{4.3}
\]

Summing the contracted holding times, retaining every lower clock, gives
all fixed activation-duration moments.  A lower death during an attempt is
kept in the physical population accounting and is favorable.

## 5. Deterministic service after activation

The top reaction graph is weakly reversible with one linkage class.  The
normalized top ODE is conservative on the unit simplex.  The permanence
theorem of Boros and Hofbauer applies to every positive trajectory of such
a system; see [*Permanence of Weakly Reversible Mass-Action Systems with a
Single Linkage Class*](https://doi.org/10.1137/19M1248431), SIAM Journal on
Applied Dynamical Systems 19 (2020), 352--365.

The remaining boundary point is elementary but must be stated.  Strong
connectivity forces every non-dormant boundary trajectory into the relative
interior: a missing-species face which contains an enabled top source has a
directed cut to a complex outside that face.  The only service-zero
invariant point is the dormant \(X\)-vertex, and the activation shell
\(M\ge\varepsilon\) is separated from it.  Permanence therefore implies

\[
                    \int_0^\infty C_z(t)\,dt=\infty    \tag{5.1}
\]

for every normalized activation state \(z\).  Continuity and compactness
then give, for every prescribed \(D_0\), a finite \(T(D_0)\) such that

\[
 \inf_{M(z)\ge\varepsilon}
       \int_0^{T(D_0)}C_z(t)\,dt>D_0.                 \tag{5.2}
\]

Independent replay must check carefully that the boundary-to-interior
argument is uniform over all four supports; permanence itself starts from
a positive state.

## 6. Full-chain service and fractional return

After activation, run every physical clock for time \(T/n\).  The top
density process converges uniformly to the ODE on the fixed fluid horizon.
The lower birth has \(O(n^{-1})\) expected firings, while the \(C\to0\)
death compensator is the scaled integral in (5.2).  Counting-process
exponential martingales should therefore produce one macroincrement \(Z\)
and duration \(S\) satisfying

\[
 \mathbb E(Z\mid\mathcal F_0)\le-a,\qquad
 \mathbb E e^{\theta Z^+}\le C,\qquad
 \mathbb ES^p\le C_p                                  \tag{6.1}
\]

for every fixed \(p\), with all activation births and all preactivation
deaths included exactly once.

Repeat macroepisodes at their strong-Markov endpoints and stop when

\[
                    n_J\le\rho n_0
                    \quad\hbox{or}\quad n_J\ge2n_0.   \tag{6.2}
\]

The conditional moment generating function following from (6.1) gives an
exponentially small upper exit and polynomial moments of \(J\) and the
physical duration.  One must prove a uniform integer endpoint order
\(p>8\).

For arbitrary fixed \(\ell\), choose \(K_\ell\) so that

\[
 F_\ell(x)=K_\ell+\sum_i\log(x_i!)+\ell\mathbin\cdot x\ge1,
 \qquad W_\ell=F_\ell^4.                              \tag{6.3}
\]

The deterministic factorial envelope

\[
 \log(n!)-n\log3\le\sum_i\log(x_i!)\le\log(n!)       \tag{6.4}
\]

shows that the lower branch of (6.2) has

\[
 W_\ell(X_\tau)-W_\ell(x)
 \le-c(n_0\log n_0)^4.                               \tag{6.5}
\]

The upper branch, including its random overshoot, is event-weighted by its
exponential probability.  This is the proposed common-\(W_\ell\) endpoint;
no additive total-population power is used.

## 7. Audit gate

Before any flag changes, an independent audit must verify:

1. the quantitative pure/mixed contraction (4.1) for every sparse strong
   orientation and arbitrary positive rate vector;
2. the finite trial from the one- or two-seed phase, including the 186
   orientations which require a temporary mass dip;
3. the compound-geometric birth tail and all activation-duration moments
   with every lower clock retained;
4. the boundary-to-interior hypothesis needed before applying the
   single-linkage permanence theorem;
5. the lattice-uniform density limit and stochastic compensator moments;
6. the conditional stopped-sum bounds through one integer order \(p>8\);
   and
7. the factorial envelope on both stopping branches, including the random
   upper overshoot.

Until all seven items pass hostile replay, the four pairs remain unresolved
and every analytic, recurrence, and global flag stays false.

## 8. Reproduction

```text
PYTHONPATH=src python3 -B src/hard333_hw4_compound_activation_repair.py
PYTHONPATH=src python3 -B -m unittest \
  tests/test_hard333_hw4_compound_activation_repair.py -v
```

The frozen geometry-row hash is

```text
47b6fae4896567c500f52bf82adc0fbce9923e91cb4c4fae2a22733928d275ed
```

the exact 1,606-digraph profile hash is

```text
2a136e64a12be64577c5852ed30e027d057b529ffefa5dc82abd67a8a39f1230
```

and the payload hash is

```text
d62253d0663d7df818feebf9e2afa2e287c22490b1d1bda700ddf80352b30064
```
