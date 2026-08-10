# Exact failure of activation-plus-target charging

Consider the two-linkage, bimolecular weakly reversible network (all rates
one)

\[
A\rightleftarrows2A,
\qquad
0\longrightarrow A+B\longrightarrow B\longrightarrow0.
\]

At population `(n,0)`, suppose the actual current target is `2A`.  Condition
on the slower channel `0->A+B`, and then append the honest current-target
path episode `A+B->B->0` with one final ordinary jump.

The activation increment of the residual factorial potential is

\[
\log(n(n-1))=2\log n+o(1).
\]

Immediately after activation, the source `2A` has probability tending to one.
A deviation through `2A->A` has reward `-\log n+o(1)`, while the probability
of following `A+B->B` is `O(1/n)`.  Therefore the appended target episode has
expected reward

\[
-\log n+o(\log n),
\]

and the combined conditioned block satisfies

\[
J_n=\log n+o(\log n)>0.
\]

The executable verifier `src/activation_pair_counterexample.py` confirms the
sign and the ratio `J_n/log n -> 1` numerically at deterministic integer
points.  The asymptotic estimate above is analytic; the numerical values are
regression checks only.

By contrast, the episode begun **before** selecting a future channel, from
the already carried target `2A`, has negative expected reward.  Hence the
correct decomposition must retain the preceding current-target episode and
all activation probabilities in one unconditioned trace.

This is not a physical recurrence counterexample.  It invalidates only the
claim that an activation jump can be conditioned upon and then charged to the
subsequent target episode.
