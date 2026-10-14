# Fixed-schedule reachability does not provide an online strategy

Status: exact partial lemma, for independent audit. It does not solve the
two-dimensional Time-Bomb conjecture.

## Statement in one spatial dimension

Fix a complete, nonadaptive announcement sequence
`(q_r,t_r), r=1,2,...`, with `q_r in Z`, positive integer `t_r`, and at
most one announcement in each round. The Angel starts at zero and has
increments in `{-1,0,1}`. An announcement is effective only if `r<t_r`.
There exists an infinite legal path avoiding every effective announced
pair. The path is allowed to depend on the complete sequence.

For `n>=1`, let

`F_n = {q_r : r<n and t_r=n}`,

and write `b_n=|F_n|`. Duplicate pairs are counted once. Since each member
of the disjoint union of `F_1,...,F_n` has a distinct announcement witness
in rounds `1,...,n-1`,

`sum_{j=1}^n b_j <= n-1`.

Define all safe reachable positions recursively:

`R_0={0}`,
`R_n=(R_(n-1)+{-1,0,1}) \ F_n`.

For every nonempty finite subset `A` of the integers,

`|A+{-1,0,1}| >= |A|+2`.

Indeed, the sum contains `A`, `min(A)-1`, and `max(A)+1`, with the last
two points distinct and outside `A`.

Induction therefore gives

`|R_n| >= 1+2n-sum_{j=1}^n b_j >= n+2` for every `n>=1`.

At the induction step the previous set is nonempty by the preceding
bound. All these sets are finite, lying in `[-n,n]`.

Form the tree of finite safe paths rooted at the empty path. It has
branching at most three, and it has a node at every depth because every
`R_n` is nonempty. The finite-branching infinite-tree lemma supplies an
infinite branch. This is the required path.

## Application and quantifier boundary

The same statement holds in two dimensions: restrict the path to a fixed
horizontal line and retain only announcements on that line. The effective
announcement budget can only decrease.

The statement has the order `for every fixed schedule, there exists a
path`. It does not choose a path from the history available at each move.
In particular, a schedule realized against one path cannot simply be
reused against a different path when the Devil is adaptive: the latter
path may produce different announcements.

Consequently, even strong global reachable-set growth, or the existence
of arbitrarily long paths against every frozen schedule, is not an
online winning-strategy invariant. Combining this lemma with an
independently certified one-dimensional online Devil win would give a
strict separation between the two quantifier orders in the same game
family. This file does not rely on an unverified finite-search result for
that separation.

## Scope of proof

No source theorem beyond the elementary finite-branching infinite-tree
lemma is used. All timing and counting conventions are those in
`CONSTRUCTION_CONTRACT.md`. There are no preloaded bombs in the statement.
