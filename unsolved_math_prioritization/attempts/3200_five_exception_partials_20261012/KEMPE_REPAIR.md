# One explicit Kempe repair of the failed fixed-coloring example

This supplements Section 6 of FIVE_CYCLE.md with a checked repair, not another general theorem.

Keep the edge order E=[04,41,02,03,12,13,23], exterior set F={e3,e4}, exterior color 3 on F, and the ordinary coloring

φ(e0)=0, φ(e1)=1, φ(e2)=1, φ(e5)=0, φ(e6)=2.

In G−F, the connected component of the edges of ordinary colors 0 and 2 that contains e0 is the single edge e0. Its two neighboring edges in G−F are e1 and e2, both of color 1. Therefore exchanging colors 0 and 2 on that component changes only e0 from 0 to 2 and preserves properness.

Now apply the global permutation 0↦2, 1↦0, 2↦1. The full edge-color sequence, including color 3 on F, is

(e0,e1,e2,e3,e4,e5,e6)=(1,0,0,3,3,2,1).

The exceptional edges e0,e1,e3,e4,e6 all receive colors from {0,1,3}, and the two common-list edges e2,e5 receive colors from {0,1,2}. Direct endpoint checks confirm properness.

Thus this example distinguishes an obstructed global permutation from a successful Kempe change followed by a global permutation, while keeping the same exterior set. It does not show that one Kempe change always suffices for five exceptions.
