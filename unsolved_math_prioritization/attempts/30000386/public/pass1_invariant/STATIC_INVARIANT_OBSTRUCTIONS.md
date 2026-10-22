# Two static invariants that fail to encode online safety

Status: exact obstructions to specified proof routes, not a Devil win
from the initial state and not a disproof of the conjecture.

## 1. Static future vertex-cut capacity cannot refresh from 8 to 9

In the directed spacetime graph, the successors of `(p,n)` are
`(p+v,n+1)` for `v in {-1,0,1}^2`. For a fixed finite set of already
announced future bombs, let the capacity of a nonbomb vertex be the
minimum number of additional future vertices whose deletion meets every
infinite directed path from it. The current vertex cannot be deleted.

Suppose the only relevant bomb is `(p,n+2)`. The capacity at `(p,n)` is
exactly 9, while every one of its nine successors has capacity exactly 8.

For the upper bounds, delete all nine immediate successors of `(p,n)`;
at any successor `(q,n+1)`, one of its nine immediate successors is the
existing bomb, so deleting the other eight suffices.

For the lower bounds, first consider any noncentral successor indexed
by `v in {-1,0,1}^2 \ {(0,0)}`. Use the ray whose position at time
`n+k`, `k>=1`, is `p+kv`. These eight rays are pairwise vertex-disjoint
after `(p,n)`, and avoid `(p,n+2)`. For the ninth path, use positions
`p` at time `n+1`, `p+(1,0)` at time `n+2`, and `p+(k-1,0)` at time
`n+k` for every `k>=2`. It is legal, avoids the bomb, and is disjoint
from the eight rays. Thus at least nine additional vertices are required
to hit all these paths.

For a successor `(q,n+1)`, its eight nonbomb immediate successors can
each start a disjoint ray obtained by translating the eight distinct
king increments from `q`; more explicitly, use the ray with increment
`v` for each `v in {-1,0,1}^2` except the increment `p-q`. There are no
further bombs, and these eight rays are mutually disjoint after the
root. Thus its capacity is at least eight.

Hence the tempting update claim
`capacity >=8 implies some next position has capacity 9`
is false even with one pending bomb. The example can occur after a legal
announcement: choose any `n>=1`, have the Angel at `p` at that time, and
announce `(p,n+2)` in round `n`. If capacity is evaluated before the next
Angel move, its relevant root is `(p,n)` as above.

## 2. Safe endpoints at each deadline need not form a joint safe path

At a state `(p,n)`, preload the following 17 distinct pairs:

- eight bombs at time `n+1`, on `p+{-1,0,1}^2` except `p`;
- nine bombs at time `n+2`, on all of `p+{-1,0,1}^2`.

Each deadline considered in isolation has a safe reachable endpoint:
`p` at time `n+1`, and every point of the outer ring
`p+[-2,2]^2 \ (p+[-1,1]^2)` at time `n+2`.
Nevertheless, every two-step path dies. The only safe first move is to
stay at `p`; all nine moves from there at the second time are bombed.

This is a legal reachable history, for example with `n=17`: keep the
Angel at `p=0` through round 17 and announce these 17 future pairs one
per round. No earlier move is lethal. The example is not a claim that
the Devil can force the Angel to enter this history.

Thus a multi-time extension of a one-deadline endpoint argument needs a
joint path or transition invariant, not merely a separate nonempty set
of safe endpoints for each deadline.
