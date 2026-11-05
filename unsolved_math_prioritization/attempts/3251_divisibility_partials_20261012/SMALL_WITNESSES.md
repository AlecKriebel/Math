# Small authored mathematical witnesses

These finite objects specify authored examples used by the complete proofs and substantive audits. They are not a downloaded dataset or a replacement for those proofs.

## Fano triples

On vertices 0 through 6 use: {0,1,2}, {0,3,4}, {0,5,6}, {1,3,5}, {1,4,6}, {2,3,6}, {2,4,5}. Every pair occurs once, so the shadow is K7. All 128 colorings have a monochromatic triple. This cannot be the maximum-triangle family of a graph.

## The chordal G(5,4) witness

The core cycle is (0,1,2,3,4), and the fan chords are {0,2} and {0,3}. The five attached maximum cliques are:

{0,1,5,6}, {0,4,13,14}, {1,2,7,8}, {2,3,9,10}, {3,4,11,12}.

Its full edge set is the union of all pairs in those five cliques and the two fan chords. Explicitly:

{0,1}, {0,2}, {0,3}, {0,4}, {0,5}, {0,6}, {0,13}, {0,14}, {1,2}, {1,5}, {1,6}, {1,7}, {1,8}, {2,3}, {2,7}, {2,8}, {2,9}, {2,10}, {3,4}, {3,9}, {3,10}, {3,11}, {3,12}, {4,11}, {4,12}, {4,13}, {4,14}, {5,6}, {7,8}, {9,10}, {11,12}, {13,14}.

A perfect-elimination order is (5,6,7,8,9,10,11,12,13,14,1,2,3,4,0). Color core vertices 0 through 4 red and vertices 5 through 14 blue. Each maximum clique has two vertices of each color. Removing the two fan chords gives the maximum-clique shadow; its core induces a five-cycle. Thus the graph is chordal and divisible while its shadow is not odd-hole-free.

## Rank-six Hall witness

On vertices 0 through 11 use the six edges:

{0,1,2,3,4,5}, {2,3,4,5,6,7}, {4,5,6,7,8,9}, {6,7,8,9,10,11}, {0,1,8,9,10,11}, {0,1,2,3,10,11}.

Every vertex has incidence three. For any subfamily F, incidence counting gives 6|F|≤3|union F|, hence |union F|≥2|F|. There are 64 subfamilies. A direct red/blue representative choice, one pair per displayed edge in the same order, is (0,1), (2,3), (4,5), (6,7), (8,9), (10,11), with the first representative red and the second blue. All representatives are distinct and lie in their designated edges.

## Three-sun incidence triangle

Let the core triangle be {0,1,2}, with vertices 3,4,5 adjacent respectively to {0,1}, {1,2}, {0,2}, and no other added edges. The four maximum triangles are {0,1,2}, {0,1,3}, {1,2,4}, {0,2,5}. Eliminating 3,4,5 first gives a perfect-elimination order. The last three clique rows restricted to core vertices form a strong odd incidence cycle.

## A sufficient criterion that is not necessary

Label the six edges of K4 by a={0,1}, b={0,2}, c={0,3}, d={1,2}, e={1,3}, f={2,3}. Its vertex stars become hyperedges {a,b,c}, {a,d,e}, {b,d,f}, {c,e,f}. Every hypergraph vertex has incidence two. The full family has six vertices and four edges, violating the Hall union bound 6≥8. Nevertheless, coloring a,b,e,f red and c,d blue makes every hyperedge bichromatic.

## Odd-length Euler-circuit branch

Take a dual multigraph on real vertices A,B,C with one AB edge, three AC edges, and three BC edges. Its degrees are 4,4,6 and its Euler circuit has seven edges. The corresponding hypergraph on vertices 0 through 7 has edges {0,1,2,3}, {0,4,5,6}, {1,2,3,4,5,6}, with vertex 7 isolated. There is no auxiliary incidence. Starting an odd Euler circuit at a real vertex may leave that start with an unequal pair of color counts; the degree bound still leaves both positive. For a direct check, color {0,1,4} red and the remaining vertices blue. Every hyperedge meets both colors.
