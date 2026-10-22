# Exact acceptance of EP 810 scoped partial results

## Identified object

Problem 2315, EP-810, selection rank 903. Reviewed author ZIP: RAINBOW_QUADRILATERAL_2315_AUTHOR_SAFE_FREEZE.zip, 15,279 bytes, SHA-256 2cc0a33b99299d2581cdd4bec4c13e804c5d5537953ab2344bcbdbd8ed1d9a5c. Reviewed PROOFS.md: 12,868 bytes, SHA-256 129ffa669d8e12aa759f6b8ade41093dc97160f90f468a2f8a518e961393ea96. No original file was corrected or replaced.

## Accepted statements

1. For every eta>0 there is n0(eta) such that every simple n-vertex graph, n>=n0, with an arbitrary edge coloring in which every C4 subgraph is rainbow has a spanning subgraph with inherited proper coloring after deleting at most eta n^2 edges. No color is added. The threshold is uniform over graphs and palettes. The triangle-removal lemma is an explicitly imported standard theorem.
2. With at most n colors, the arbitrary-coloring and proper-coloring extremal edge counts differ by o(n^2). The original all-sufficiently-large-size positive-density target is equivalent to positive liminf of either normalized extremal count, and to the stated balanced bipartite proper rainbow-C4 version with parts of size s and an available palette of at most s. Both conversions preserve every sufficiently large integer size and a fixed positive density.
3. A linear tripartite (7,4)-free 3-uniform hypergraph projects to a proper rainbow-C4 coloring. The reverse implication fails for the exhibited four-edge path colored a,b,a,b, whose four triples use exactly seven vertices.
4. For two copies of Z/mZ, any edge coloring of the form f_m(a_m x+b_m y+z_m), with both coefficients units, can have every C4 rainbow only on o(m^2) edges, uniformly in the displayed choices. This uses the credited finite multidimensional Szemeredi theorem; no broader algebraic labeling family is covered.
5. Every R-coloring of K_{s,t}, s,t>=2, needs st colors. Therefore a complete uniform t-fold blowup of a fixed h-vertex seed containing an edge cannot meet a palette bound equal to its ht vertices once t>h. Padding preserves validity but alone does not repair arbitrarily separated construction sizes.
6. For an R-colored n-vertex graph with m edges and at most q colors, D=max(1,floor(q/2)) bounds every codegree, and m<=n(1+sqrt(1+4(n-1)D))/4. For q=n this has leading coefficient 1/(2sqrt(2)); no sharpness or vanishing-density conclusion is accepted.

## Explicit exclusions

No positive-density construction for every sufficiently large size, no proof of the original problem's negation, and no universal o(n^2) theorem for arbitrary admissible colorings are supplied. The exact negation of the all-size target is liminf E_R(n)/n^2=0; a universal little-o claim is stronger.

The 2023 source's Question 1.3 literally assumes the minimum palette q_B(G)=s. The accepted reduction uses an available palette at most s. Acceptance does not silently identify these hypotheses or claim that the contextual literature comparison proves their equivalence. Adding unused colors cannot change q_B(G).

No historical novelty, priority, full current-literature clearance, independently accessed tracker-open status, human peer review, or formal proof-assistant certification is claimed. The cited removal and multidimensional Szemeredi theorems are imported with verified statements and hypotheses, not reproved here.

## Disposition

UNSOLVED_SCOPED_PARTIALS_ACCEPTED. Five of five approaches, with their remaining gaps preserved. No mandatory correction found; no correction derivative exists. The original archive remains the authoritative author snapshot, and this acceptance is a separate later review of those exact bytes.
