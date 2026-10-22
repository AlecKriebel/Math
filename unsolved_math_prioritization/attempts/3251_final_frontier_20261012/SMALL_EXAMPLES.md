# Small authored examples

These are explicit mathematical illustrations of accepted results, not an additional research pass. Their exact graph, coloring and arithmetic claims are checked in the edition validation.

## Two node rank three tree

Let the two base bags be {0,1,4} and {2,3,4}, with prescribed core X={0,1,2,3}. For each x in X attach two triangles, each with x and two fresh private vertices. There are 21 vertices, 10 maximum triangles and 30 edges. The original high-incidence core is exactly X. The unique unmarked component is the two-node tree, with S={0,1} and T={2,3}.

The two forbidden core assignments, in order 0,1,2,3, are (0,0,1,1) and (1,1,0,0). Exactly 14 of 16 core assignments extend. For the first assignment the first triangle forces vertex 4 to color 1 and the second forces it to color 0. For any other assignment at least one of the two choices of vertex 4 works; each support triangle is completed by a private vertex opposite its attachment. The induced core is two disjoint edges. Both bad prescriptions make those maximum core edges monochromatic, so they are not core divisions.

## Rank four repeated leaves

Use A={0,1,2}, B1={3,4}, B2={5,6}, B3={7,8} and low vertices z1=9,z2=10,z3=11,z4=12. The low graph has edges {9,10}, {9,11}, {10,11}, {10,12}, {11,12}. Attach the four blocks to their specified ports and add one support K4 for each A vertex and two for each B vertex, using fresh private vertices.

This graph has 58 vertices, 20 maximum K4s and nine core vertices. The five base bags are {0,1,2,9}, {3,4,9,10}, {5,6,10,11}, {7,8,11,12}, {0,1,2,12}. The forbidden core assignment is (0,0,0,1,1,0,0,1,1) or its complement. Exactly 510 of 512 core assignments extend. The only core triangle is A, and it is monochromatic in each bad assignment. The graph itself is divisible by mixing every block and then completing supports.

The edges {9,11} and {10,12} lie in no maximum K4. Removing both produces the induced five-cycle 0,9,10,11,12,0. This illustrates why the actual graph, rather than an assumed odd-hole-free maximum-clique shadow, is essential.

## Eight vertex critical boundary

Take the complement of the seven-cycle on vertices 0 through 6 and add a universal vertex 7. It has clique number four, chromatic number five, seven maximum K4s, and all eight vertices are in the original high-incidence core. Each rim vertex has maximum-clique incidence three, and vertex 7 has incidence seven. Deleting any vertex lowers the chromatic number, so the graph is 5-critical. It is odd-hole-free.

Color vertex 7 with one color and all rim vertices with the other. Every maximum K4 is mixed. Thus this eight-vertex critical core boundary example is divisible; it does not exclude the eight-core possibility for a larger indivisible graph. Universalness inside an induced core cannot be promoted to universalness in the whole graph.

## Necessary bound arithmetic

At k=4 the retained core bound is eight, and the imported Folkman total-order bound is 19. Clique and edge cutsets in a minimal target counterexample require at least 22 and 24 total vertices. At k=5 the final core bounds are 12 and 13, the latter when its clique number is four. Every cutset side has at least 17 vertices; a clique cutset requires at least 29 total vertices and an edge cutset at least 32. These are necessary implications, not constructions or optimality claims.
