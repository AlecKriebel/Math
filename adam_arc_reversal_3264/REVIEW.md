# Independent audit: Ádám’s arc-reversal conjecture

Date: 2026-10-20 UTC. Target: queue row 1819, ID 3264, OPG-46432.

## Verdict and attribution

**The unrestricted target is already disproved.** The relevant published result is Carsten Thomassen, *Ádám’s conjecture*, Journal of Combinatorial Theory, Series B 161 (2023), 15–20, Theorem 1; DOI https://doi.org/10.1016/j.jctb.2023.01.005. The accepted manuscript is available at https://backend.orbit.dtu.dk/ws/portalfiles/portal/308267535/Adam_final_.pdf.

I inspected the full accepted manuscript and independently reconstructed its finite combinatorial mechanism. The audit below also supplies an exact-arithmetic certificate for one parameter instance of the published construction: **1,530 vertices and 80,520 arcs**. This is an audit of an existing theorem, not a new disproof, a smallest-example claim, or a claim about tournaments.

The graphs are loopless simple oriented graphs: no parallel arcs and no pair of opposite arcs. They are strongly 2-connected and self-reverse. Every individual arc reversal fails to reduce the number of simple directed cycles. Exterior arcs strictly increase it in the certified instance, while some interior arcs preserve it. The property is not that every reversal is acyclic, nor that every reversal strictly increases the cycle count. The circulant-isomorphism conjecture sharing Ádám’s name is unrelated.

## 1. The cycle/path identity

For an arc u→v, remove it and write H for the resulting graph. Reversal changes the cycle count by

    number of simple u→v paths in H − number of simple v→u paths in H.

Cycles not containing the changed arc cancel. Each remaining cycle is identified uniquely with its path after deleting that arc. Directed cycles are counted once up to cyclic rotation, not once per starting vertex.

## 2. Base graph and independent counts

The base B_m has vertices x_i,y_i for indices modulo m, with arcs

    x_i→x_(i+1), x_(i+1)→y_i, y_i→y_(i+1), y_(i+1)→x_i.

Our code uses zero-based indices, so its even index corresponds to the manuscript’s odd index. Base graphs B_6 and B_10 are the manuscript’s D12 and D20.

Exhaustive simple-path/cycle search reproduced:

- D12 cycle counts by length: length 4: 18; length 6: 4; length 10: 36.
- D12 cycles destroyed at a fixed arc: lengths 4,6,10 have counts 3,1,15.
- D12 cycles created by reversing that arc: lengths 6,8,12 have counts 1,5,1.
- D20 cycle counts: lengths 4,10,14,18 have counts 30,4,140,100.
- D20 cycles destroyed at a fixed arc: counts 3,1,49,45 at those lengths.
- D20 cycles created: lengths 6,12,16,20 have counts 1,9,35,1.

In particular D20 itself is not a counterexample: its total is 274, and reversing an arc loses 98 cycles while creating 46. The expansion is essential. The D12 enumeration exactly reproduces the paper’s parallel-arc polynomials, including the total 37,769,728 and post-reversal total 38,113,600 when each arc has multiplicity four. That auxiliary multidigraph is not the simple-oriented counterexample.

## 3. Expansion and exact counting, without asymptotic notation

Expand each of the ten even-indexed manuscript vertices of D20 into an acyclic gadget. Its ordered layers have sizes d,1,1,…,1,d, with k singleton middle layers. Put every forward arc between distinct layers and no arcs within an endpoint layer. Each gadget vertex inherits the original exterior neighbors. The ten odd-indexed base vertices remain singletons.

Contracting any directed cycle gives a closed base trail with no repeated arc, each odd-indexed vertex visited at most once, and each even-indexed vertex visited at most twice. Conversely, such a trail lifts to a simple directed cycle by choosing nonempty, pairwise disjoint increasing gadget paths. Fixing the least odd-indexed vertex as the start eliminates cyclic overcounting. The ordering of two visits to a gadget determines which is the first and second path.

Let A count one nonempty gadget path and B count an ordered pair of disjoint nonempty gadget paths. Direct counting gives the exact formulas

    A = (d+1)^2 2^k − 1,
    B = (d^2+d+1)^2 3^k − 2(d+1)^2 2^k + 1.

For B, each middle vertex chooses first path, second path, or neither. At either endpoint layer the choices are neither, one chosen endpoint on either path, or two distinct endpoints: 1+2d+d(d−1)=d^2+d+1. Inclusion-exclusion removes an empty first or second path.

If a trail visits a gadgets once and b gadgets twice, its lift count is exactly A^a B^b. Exhaustive enumeration gives the following complete list of (a,b):multiplicity:

    (0,2):10, (0,5):10,
    (2,0):30, (2,1):30, (2,2):40, (2,3):40, (2,4):30,
    (5,0):4, (5,1):20, (5,2):20,
    (7,0):140, (7,1):200, (9,0):100.

Thus the exact total is the sum of these 13 monomials. The maximum 2^a 3^b is 512, and the largest value at a+2b=10 is 324. This independently verifies the separation of exponential growth rates used in the manuscript.

## 4. Exterior-arc audit and explicit parameter certificate

To avoid relying solely on the manuscript’s cycle-injection description, count cycles through a specified exterior arc directly. Let its endpoint be a fixed vertex in the gadget’s initial d-vertex layer. Replace the appropriate factor A or B by

    A0 = (d+1)2^k,
    B0 = d(d^2+d+1)3^k − (d+1)2^k.

Here the first path starts at that fixed vertex; if there are two visits, the second path may use any of the other d−1 initial-layer vertices or none. Subtract the configurations with an empty second path.

For a fixed singleton middle vertex i (1≤i≤k), the corresponding local counts are

    Ai = (d+1)2^(k−i),
    Bi = (d+1)(d^2+d+1)2^(i−1)3^(k−i) − (d+1)2^(k−i).

For a fixed vertex in the final layer they are

    Afinal = 1,
    Bfinal = d(d+1)2^k − 1.

The script checks all these local counts are bounded by A0,B0 at the selected parameters. It separately enumerates contracted trails through each of the twenty odd-to-even base arcs, tags whether its endpoint is visited once or twice, and computes the exact destroyed-cycle count. All twenty maximal counts agree. The reverse isomorphism covers the even-to-odd arcs as well.

For every checked base arc u→v, removing it leaves a Hamiltonian u→v path. Reversing an expanded exterior arc therefore creates at least

    G = d^18 512^k

cycles: use the specified endpoint vertex as a singleton in its gadget, and in each of the other nine gadgets choose one initial endpoint, an arbitrary subset of middle vertices, and one final endpoint. This lower bound does not require counting all newly created cycles.

For d=64, k=24, exact integer arithmetic verifies F<G, where F is the largest number of cycles destroyed at any exterior arc. The ratio F/G is approximately 0.9363491067. The exact integers, total cycle count, and positive margin are recorded in `certificate.json`. Vertex count is 10+10(k+2d)=1530. Arc count is

    40(k+2d) + 10[ k(k−1)/2 + 2dk + d^2 ] = 80520.

This is a finite exact-count certificate based on exhaustive base-trail enumeration and proved gadget formulas. It is **not** a brute-force enumeration of all cycles of the 1,530-vertex graph, nor is such enumeration needed.

## 5. Interior arcs and structural properties

For an interior forward arc p→q, each old cycle using consecutive vertices p,q is sent injectively to a new cycle by exchanging their positions and using q→p. The predecessor of p either lies outside the gadget or in an earlier layer, so it also reaches q; likewise p reaches the old successor of q. All other vertices and arcs are unchanged. Reversing two consecutive singleton middle vertices even produces an isomorphic graph, by exchanging their labels. This establishes nondecrease for all interior arcs and explains the necessary non-strict statement.

The base graph remains strongly connected after any single vertex deletion; the script checks this directly. After expansion, each gadget vertex still has two distinct exterior predecessors and two distinct exterior successors. Deleting one odd vertex leaves access through the other neighbors and the strongly connected surviving base. Deleting one gadget vertex leaves that gadget nonempty and permits base routes through surviving vertices. Hence the constructed graph is strongly 2-connected.

A reverse isomorphism is obtained by exchanging x_i and y_i at every expanded even layer, leaving odd vertices fixed, and reversing each gadget’s internal layer order (with arbitrary corresponding endpoint bijections). Exchanging one endpoint’s track turns each exterior base arc into the reverse of the corresponding arc; reversing layer order handles all interior arcs.

## 6. Reproduction and limitations

All authored code is in `check_counts.py`, using only Python’s standard library. Running it prints the base enumeration. To reproduce the finite certificate, import and call `certificate()`; to run the small explicit-graph validation, call `small_expansion_crosscheck()`. Saved outputs are `counts.json`, `certificate.json`, and `small_crosschecks.json`. Direct cycle enumeration of three small explicitly built expanded D12 graphs agreed exactly with the trail formula: (d,k)=(1,0): 10,710 cycles; (2,0): 2,798,720 cycles; (1,1): 805,522 cycles. These are formula-validation cases, not claimed counterexamples.

The independent enumeration supplements a published proof. It is not a formal proof-assistant verification. The exact finite certificate depends on the transparent trail-enumeration algorithm and the gadget-count formulas derived above. No claim is made that the selected parameters minimize order. No tournament resolution follows: these graphs have many missing adjacencies, including the independent endpoint layers. The appropriate disposition of the catalog’s unrestricted statement is **already disproved by Thomassen (2023)**, not a new open problem obtained by silently imposing the tournament restriction.

Only authored audit/code and public bibliographic information belong in a publication artifact. The downloaded third-party manuscript and extracted text are not part of this authored deliverable.
