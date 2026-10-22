# Complete exact examples and how to read them

[EXACT_GEOMETRY_EXAMPLES.json](EXACT_GEOMETRY_EXAMPLES.json) supplies every coordinate as a canonical rational string. Each triangle lists three vertices; it denotes their closed filled convex hull. An explicitly named half-plane root denotes y<=0 instead. Every example gives its complete whole-edge family and strict common witnesses. No source document, dataset, solver log, or program is embedded.

## Two rooted models

The root-1 and root-5 five-vertex models use eta=1/1000. Their coordinates are the exact thin-segment triangles and centroid dilation in [the proof](ROOTED_BLOCK_PROOF.md). Every nonempty subfamily is checked, including those containing the unbounded root. The minimum oriented-inequality slacks are 1/62500 and 1/125000 respectively. Each has the six stated maximal faces and seventeen nonempty faces.

## Three complete wedge examples

The root-1 two-copy and root-5 two-copy examples have nine triangles each. Each gives all triangle vertices, twelve whole edges, twelve strict witnesses, and three complete incidence orders. Their common root degrees are six and four. All 511 nonempty subfamilies are checked for each.

The root-5 four-copy example supplies all seventeen rational triangles, twenty-four whole edges, and all strict witnesses. Its full nerve follows from the checked nonedge pairs and triples plus common witnesses for every declared edge, by the accepted covered linear Sperner criterion. This explicitly illustrates that the dimension-four threshold is compatible with a triangle representation. An empty order list means no three-order certificate is claimed for this example. The proved uniform four-order construction is in [the complete dimension proof](ROOT5_DIMENSION_PROOF.md).

## Actual recursive insertions

The two insertion examples begin with one root-1 block, attach a root-5 block at a nonroot triangle, then attach a root-1 block at a newly introduced triangle. Each lists the old coordinates, new coordinates, private point, side index, positive rational scale, model root, resulting whole edges, and all strict witnesses. The old triangles are compared exactly before and after insertion; the second example's old family is the first example's complete result. The nine-triangle stage is checked on all 511 nonempty subfamilies. The thirteen-triangle stage is checked on all pairs and triples, and every whole edge. These auxiliary recursive examples make no incidence-dimension assertion.

## Complete finite realizer certificates

[EXACT_CERTIFICATES.json](EXACT_CERTIFICATES.json) is preserved byte for byte from the accepted realizer packet. Its two examples are the root-5 wedges with two and three blocks. It gives all vertex permutations, all full expanded incidence orders, a witnessing order for every ordered pair of distinct vertices, and an edge-before-vertex witness for every missing incidence. The edition separately checks every listed witness, complete inventory, canonical expansion, and all 420 and 930 ordered pairs of the full incidence posets.

The geometric check enumerates intersections of independent boundary lines and tests all inequalities with exact fractions. A nonempty bounded planar polyhedron has an extreme point with two independent active constraints; all subfamilies containing a triangle are bounded. A singleton half-plane is handled directly. Closed boundaries and strict witnesses are distinguished. The checks recompute formulas and whole-edge relationships, rather than trusting stored verdicts. The independent mathematical review uses a different exact elimination method with rational primal and Farkas certificates.

Finite exact checks certify these examples. The all-k geometric and order conclusions depend on the complete written proofs and their independent review, not extrapolation from those finite checks.
