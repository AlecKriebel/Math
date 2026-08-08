# Hidden-target degree conjugation: exact collision obstruction

Date: 2026-08-08 (America/Los_Angeles)

No literature search or external communication was used.

## Result

The proposed target-locked conjugation does **not** survive hiding the source
history.  The labelled source/target degree ratio is exact, and in the
collision-free singleton test below the zero-selective neutral event is
exactly an endpoint diagonal conjugation with one target clock.  The first
selective draw, however, allows the same source to be sampled twice.  This
leaves a degree-dependent collision factor which is invisible to the
endpoint set and hidden target.  On a general initial set, neutral
coalescence can create the same obstruction even earlier.

At `r=3/2`, summing every batch length with probabilities
`(2/3)(1/3)^k` does not cancel this factor.  The weighted path with edge
ratio `1:17` gives an exact counterexample to any identity consisting of

1. the endpoint diagonal `D(A)=product_{i in A} d_i`; and
2. a clock depending only on the initial set and retained target.

This refutes that particular target-locked block identity.  The actual
unbatched `L` process refreshes its event target; a transformation that also
moves the hidden target is not identified with the fixed-target kernel used
here and remains logically possible.  The calculation also does not refute
a larger history- or multiplicity-labelled representation, and it does not
decide the endpoint product inequality.

## 1. Exact labelled ratio

Fix a target `v`.  Symmetry of the weights gives two source laws:

\[
 p_v^C(u)={w_{uv}\over d_v},
 \qquad
 p_v^L(u)={{w_{uv}/d_u}\over t_v},
 \qquad
 t_v=\sum_z{w_{zv}\over d_z}.
\]

The first is the locked dB/reversed-arrow-`C` law.  The second is the
conditional source law after reversing the labelled arrow while retaining
the same target.  Their exact ratio is

\[
 {p_v^L(u)\over p_v^C(u)}
 ={d_v\over t_vd_u}={c_v\over d_u},
 \qquad c_v={d_v\over t_v}.                                \tag{1}
\]

For a labelled locked history with `k` selective samples followed by one
neutral sample, write its sources as `u_0,...,u_k`.  The common geometric
factor `(2/3)(1/3)^k` cancels, so

\[
 {W_L(u_0,\ldots,u_k)\over W_C(u_0,\ldots,u_k)}
 ={c_v^{k+1}\over\prod_{j=0}^k d_{u_j}}.                   \tag{2}
\]

For a singleton initial set `A={v}`, the final set `B` is the set of
distinct sampled sources.  If `n_i` is the number of appearances of source
`i`, then division by the proposed endpoint potential gives

\[
 {W_L/W_C\over D(A)/D(B)}
 ={1\over t_v}c_v^k
   \underbrace{\prod_{i\in B}d_i^{1-n_i}}
               _{\text{collision factor}}.                 \tag{3}
\]

The first two factors depend only on the target and batch length.  The last
factor is one when every sampled source is distinct, but contributes
`d_i^{-1}` the first time source `i` is repeated.  A marked target does not
record it.

## 2. Exact `1:17` path obstruction

Take the path

\[
 0\mathbin{-}^{1}2\mathbin{-}^{17}1,
\]

whose degrees are `(d_0,d_1,d_2)=(1,17,18)`.  Start from `A={2}` and retain
the forced target `v=2`.  Then

\[
 p_2^C=(1/18,17/18),\qquad
 p_2^L=(1/2,1/2),\qquad
 t_2=2,\qquad c_2=9.                                      \tag{4}
\]

With only the final neutral draw, division by `D(A)/D(B)` gives the same
clock `1/2` for both possible endpoints.  Thus the neutral conjugation is
genuine.

Now allow exactly one selective draw before the neutral draw.  For endpoints
`{0}`, `{1}`, and `{0,1}`, respectively, the normalized clocks are

\[
 {9\over2},\qquad {9\over34},\qquad {9\over2}.              \tag{5}
\]

The target-only prediction is `(1/t_2)c_2=9/2`.  It fails only when the
degree-17 source is drawn twice, by the exact collision factor `1/17`.

## 3. The endpoint mixture does not repair it

Let `N>=1` have law

\[
 \Pr(N=m)={2\over3}\left({1\over3}\right)^{m-1}.
\]

The exact union laws of the `N` samples are

\[
 \begin{array}{c|ccc}
 &\{0\}&\{1\}&\{0,1\}\\ \hline
 C/D&2/53&34/37&85/1961\\
 L\text{-oriented}&2/5&2/5&1/5.
 \end{array}                                               \tag{6}
\]

After division by `D({2})/D(B)`, the three endpoint clocks become

\[
 \boxed{{53\over90},\qquad {37\over90},\qquad {1961\over450}.} \tag{7}
\]

They are pairwise distinct.  Hence there is no scalar clock attached to the
initial target-marked state which makes the full geometric kernel diagonally
conjugate through `D(A)`.

Because the failure already occurs with a forced target, changing the rule
for choosing a target cannot repair this example.  Because the factors in
(5) multiply terms with the same positive `2/3`--`1/3` history weights, the
special fitness value does not create a termwise cancellation.

## 4. Precise remaining possibility

A fully source-history-labelled or multiplicity-valued process can retain
the collision factor in (3).  On such a space the labelled ratio (2) is an
exact Feynman--Kac weight.  But projecting that process back to mutant sets
requires controlling the conditional expectation of the collision factor;
it is not a diagonal similarity or a target-only clock identity.

Thus the next viable form of this idea would have to prove one global
collision-weight inequality paired with the forest determinant.  Merely
marking the locked target is insufficient.
