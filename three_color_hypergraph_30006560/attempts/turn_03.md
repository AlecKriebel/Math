# Attempt 3: Test a color-preserving compression toward a common core

Verdict: the natural simultaneous shift preserves all color counts but can destroy every successful set. This rules out this particular proof route; it does not disprove the original inequality.

## The proposed reduction

Attempt 1 solves hypergraphs with a common (r−3)-core, while Attempt 2 identifies overlaps between different cores as the difficulty. A natural next step is to move edges toward earlier vertices using ordinary set-system compression.

Fix distinct vertices i,j. For a hyperedge e containing j but not i, put e'=(e\{j})∪{i}. Replace e by e', retaining its color, only when e' is absent from the entire original hypergraph. Otherwise retain e. Leave all other edges unchanged. Decisions use the original family, so this defines a simultaneous operation.

This transformation preserves simplicity and each individual color count. To check this, two moving edges cannot share a target, since adjoining j and removing i recovers the original edge. A target absent from the original family cannot collide with a stationary original edge. Thus there is a color-preserving bijection from old hyperedges to new hyperedges.

The hoped-for additional property was that the number T of successful sets never decreases. If true, repeated shifts might support an extremal reduction to a concentrated family. That property fails.

## A four-edge counterexample for every r≥3

Choose an (r−3)-set A disjoint from {0,1,2,3}. Include exactly these four hyperedges:

Red: A∪{0,2} and A∪{1,3}.
Green: A∪{1,2}.
Blue: A∪{2,3}.

All edges contain A, so successful r-sets correspond to rainbow triangles of the displayed four-vertex graph. There is exactly one: A∪{1,2,3}. Therefore (R,G,B,T)=(2,1,1,1).

Apply the shift i=0,j=1. The red edge A∪{1,3} moves to A∪{0,3}, since its target is absent. The green edge A∪{1,2} cannot move, since its target A∪{0,2} is already red. The other two edges remain. The resulting graph after removing A has red edges 02,03, green edge 12, and blue edge 23. Its only graph triangle is 023, which has two red edges and one blue edge. Thus T'=0, although all three color counts are unchanged.

The obstruction is precisely the interaction between a blocked move in one color and a permitted move in another. Compressing the three color classes separately does not repair it: separate compression would move the green edge onto the red edge A∪{0,2}, creating a multicolored hyperedge outside the ordinary simple one-color-per-edge problem.

## Why four edges are minimal for this failure

If there are at most two edges, no successful set exists. If there are exactly three edges and a successful set S exists, those three edges are differently colored faces of S and there is only one successful set, because any two determine their union S.

For a shift of those three edges, consider the locations of i,j relative to S.

- If j is absent from S, nothing moves.
- If i,j are both in S, the only possible moving face is S\{i}. If it moves, its target is S\{j}; when that target is already present the move is blocked, and when it is absent the moved edge remains a face of the same S. The other two faces stay in S and retain their colors. Thus S stays successful.
- If j∈S and i∉S, every face containing j moves, and the possible face S\{j} stays. No moving target was originally present because it contains i. All three resulting edges are distinct colored faces of (S\{j})∪{i}, which is therefore successful.

The case i∈S,j∉S was included in the first bullet. Thus a successful three-edge family cannot lose its successful set. The four-edge example is minimal by number of present edges for this particular simultaneous shift.

## Remaining route

Any useful compression argument must coordinate the colors more carefully, and it must justify why changes of colors or edge collisions are allowed. Neither a monotone replacement rule nor a common-core reduction is obtained here. Since edge concentration fails at this basic step, the next attempt treats successful sets as a load that can be distributed fractionally among their red faces, avoiding a direct geometric compression.
