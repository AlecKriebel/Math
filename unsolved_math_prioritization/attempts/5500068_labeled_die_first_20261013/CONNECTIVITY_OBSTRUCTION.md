# Local orientation and degree feasibility does not imply a complete path

This explicit completely labeled rectangle separates a local constraint model from the global Hamilton-path requirement. It is not a claimed complexity classification or a new literature claim about uniqueness.

## Model and instance

Coordinates are `(x,y)`, with x increasing rightward and y increasing downward. The board has width 4 and height 5. Start at the bottom-left corner s=(0,4). The die's full initial orientation, in the order `(top,bottom,north,south,east,west)`, is

`q0=(1,6,2,5,3,4)`.

All statements about chirality use this explicit tuple rather than an ambiguous handedness name. The labels, top row first, are

```
1 4 1 4
2 2 2 2
6 3 6 3
5 5 5 5
1 4 1 4
```

The two 2×5 halves each admit the cycle word `N^4 E S^4 W`, starting at their own bottom-left corner in q0. The word returns to the same full state: N^4 and S^4 are identities, as is EW. Its trace visits each of the ten cells once before closing. Let q(v) be these induced orientations in the two halves.

## Exact possible edges

The die-parity projection for this board has 25 edges in the candidate parity and zero in the other parity. Of these:

- 20 are the two disjoint 10-cycle edges and respect q(v).
- One is the middle bridge `(1,2)—(2,2)` and respects q(v).
- Four further projected edges are `(1,0)—(2,0)`, `(0,2)—(1,2)`, `(2,2)—(3,2)`, and `(1,4)—(2,4)`.

Each of those four further edges is incident, at BOTH ends, to a full orientation with no other usable edge. For direct verification, the two end orientations are:

- Top and bottom seam: `(4,3,5,2,6,1)` and `(1,6,5,2,4,3)`.
- Middle rung of either half: `(6,1,2,5,4,3)` and `(3,4,2,5,6,1)`.

Applying the four roll permutations and reading adjacent labels verifies the degree-one assertion. None of the eight involved endpoints is s. Thus no full-coverage path beginning at s can use one of these four edges: both of its endpoints would have to be global path endpoints, while one global endpoint is already s.

The only possible graph for such a path is therefore two 10-cycles joined by their middle bridge. This graph is connected.

## Complete proof of nonexistence

Any Hamilton path from s must cross the bridge to reach the right half. A simple path cannot cross the same bridge twice. Therefore it must cover the whole left 10-cycle before crossing, ending that first segment at `(1,2)`.

A Hamilton path using only edges of a cycle is the cycle with one edge deleted, so its two endpoints must be adjacent in that cycle. But s=(0,4) has cycle neighbors `(0,3)` and `(1,4)`, neither of which is `(1,2)`. Contradiction.

This argument also rules out selectable initial orientation. The only state at s with even one compatible edge in the candidate parity is q0, and the other parity has no usable edges. Thus the starting state is forced by the labels.

## A feasible local degree certificate

Prescribe the final cell t=(0,3). Select all right-half cycle edges, and select all left-half cycle edges except `s—t`. Give every cell the induced orientation q(v).

Every selected edge is a valid roll between its endpoint states. The selected degree is one at s and t and two everywhere else. The candidate graph is connected. Yet the selected graph is one path plus one disjoint 10-cycle, and the preceding proof shows that no connected solution exists.

Thus endpoint degrees, orientation consistency, and connectedness of the candidate graph are insufficient. An exact formulation needs connectedness of the selected edges, or an equivalent global condition. The [exact authored certificate](EXACT_AUTHORED_CERTIFICATE.json) supplies all induced states and all 25 candidate state edges. The [certificate guide](CERTIFICATE_GUIDE.md) gives direct roll checks; the [independent review](INDEPENDENT_STRUCTURE_REVIEW.md) confirms the graph decomposition and all four selectable start states. The complete graph argument above proves this particular counterexample without relying on exhaustive search.
