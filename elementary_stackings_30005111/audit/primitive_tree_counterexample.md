# Primitive closed walk without a stacking

## Result

If backtracking is permitted and “primitive” means “not a repetition of a shorter closed walk,” not every primitive closed walk admits a projection-preserving embedding into `G × R`.

Let `G` be the path `A—O—B`. Give its edges the names `a = OA` and `b = OB`. Take the length-ten closed walk

`W = O A O B O A O B O A O`.

Its five leaf excursions spell the cyclic word `ababa`. The walk is primitive: it traverses the directed edge `O→A` three times and `O→B` twice, so any repetition exponent would divide both 3 and 2.

## Elementary obstruction lemma

Consider two excursions from `O` to the same leaf and back. Suppose a stacking exists. Let the two endpoint heights at `O` of one excursion be `p,q`, and those of the other be `r,s`.

At every interior point of the edge, each excursion contributes two points. Points belonging to different excursions never coincide, so the vertical order of any pair of their strands is constant along the edge interior. At the leaf, the first pair converges to its single leaf-visit height, and the other pair converges to a different leaf-visit height. Thus both strands of the first excursion lie below both strands of the second, or vice versa. By continuity at `O`, either

`max(p,q) ≤ min(r,s)` or `max(r,s) ≤ min(p,q)`.

Consequently, the height intervals spanned by two excursions to the same leaf have disjoint interiors. An equality can occur only at a shared domain visit to `O`.

## Contradiction

Let the five distinct visits to `O` have respective heights `h0,h1,h2,h3,h4`, cyclically. They are all distinct because the supposed lift is an embedding.

The three `a` excursions have endpoint pairs

- `(h0,h1)`;
- `(h2,h3)`;
- `(h4,h0)`.

The first and third excursion intervals have disjoint interiors and share `h0`. Hence `h4,h0,h1` are strictly monotone. Their union is the interval between `h4` and `h1`.

The second `a` interval must be disjoint in its interior from both intervals in that union. Its endpoints are distinct from `h4,h0,h1`, so the entire interval between `h2` and `h3` lies strictly above or strictly below the interval between `h4` and `h1`.

The two `b` excursions have endpoint pairs `(h1,h2)` and `(h3,h4)`. Each joins one of these separated height intervals to the other. Therefore their height intervals overlap in a nonempty open interval. This contradicts the obstruction lemma for leaf `B`.

Thus `W` has no stacking.

## Exact finite test for an arbitrary finite walk

For each graph vertex, assign distinct real heights to its distinct preimages in the domain circle. For each occurrence `i` of an edge, orient its parametrization consistently with a fixed orientation of that graph edge, and write `L_i,R_i` for its endpoint heights.

A stacking exists if and only if these vertex heights can be chosen such that, for every two distinct occurrences `i,j` of the same graph edge,

`(L_i − L_j)(R_i − R_j) ≥ 0`.

Necessity follows because strands cannot reverse vertical order along an edge. Equality is allowed when two occurrences share a domain vertex, as occurs at immediate backtracking.

For sufficiency, the two weak endpoint orders have no inversion and therefore admit a common total refinement. Pick distinct midpoint heights in that total order, then interpolate linearly from the left endpoints to the midpoint and from the midpoint to the right endpoints. Different strands are disjoint in the interior. Endpoint equalities occur only at common domain visits, since the vertex heights were distinct for distinct visits. The resulting continuous lift of the finite circle is injective, hence an embedding.

This test also handles loop edges by treating their two incidences as left and right endpoints of the edge parametrization while using the same height variables for the graph vertex.

## Independent computation

`check_star.py` exhaustively tests all central-height permutations using the interval criterion. It checks every primitive binary excursion word of length 2 through 6. There are no counterexamples below five excursions; `ababa` has zero valid orders among all `5! = 120` possibilities. The proof above is independent of this finite computation.
