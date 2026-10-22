# Independent audit of the finite parameter certificate

Date: 2026-10-20 UTC.

## Verdict

**PASS.** The authored certificate correctly verifies the instance d=64, k=24 of Carsten Thomassen's published construction in *Ádám’s conjecture*, Journal of Combinatorial Theory, Series B 161 (2023), 15–20, Theorem 1, https://doi.org/10.1016/j.jctb.2023.01.005.

This is an exact finite-parameter audit within the existing construction, not a new disproof, a minimum-order result, or a tournament result. It does not claim that every arc reversal strictly increases the cycle count. No primary-source text is reproduced here.

## Independently reproduced results

The separate standard-library program `independent_audit.py` does not import `check_counts.py`. It uses a different search representation: two-step transitions between the ten unexpanded vertices, with each transition labelled by its intermediate gadget. It independently constructs the full expanded graph and records results in `independent_audit.json`.

All checks passed:

- Exactly 674 canonical closed trails, with exactly the 13 (a,b) coefficients stated in REVIEW.md.
- Exact destroyed-cycle counts at all 20 unexpanded-to-gadget base arcs agree, and agree with the saved certificate.
- A Hamiltonian path avoiding the selected base arc exists for each of those 20 arcs.
- The bounds for every possible endpoint layer hold at d=64, k=24.
- The exact cycle total, F, G, and positive difference G−F agree with `certificate.json`.
- F/G = 0.9363491066658967 (displayed approximation only; the inequality uses integers).
- The materialized graph has exactly 1,530 vertices and 80,520 arcs, with no loops, parallel arcs, or antiparallel pair.
- The specified reverse-isomorphism permutation carries its entire arc set to its reverse.
- Two reachability searches for each possible deleted vertex verify strong connectivity after all 1,530 single-vertex deletions.
- Direct enumeration of nonempty increasing paths and disjoint ordered path pairs verifies all local formulas in each of 15 small gadgets: d in {1,2,3}, k in {0,1,2,3,4}, and every possible starting layer.

The certified strict lower bound on the cycle increase for any exterior arc is

    2175319727782869386982943830076378031958434912728947187141829384383034833348993757510373950730688.

## Completeness and counting multiplicity

The base is bipartite between unexpanded vertices and gadgets. A cycle in the expansion must use an unexpanded vertex, because each gadget is acyclic and there are no gadget-to-gadget arcs. Its contraction alternates between these two parts. Unexpanded vertices occur at most once. Consequently no base arc can repeat, and each gadget occurs at most twice because it has only two distinct exterior predecessors. Every passage through a gadget is a nonempty increasing path.

Conversely, a closed contracted trail with those restrictions, together with disjoint increasing paths for the visits to each gadget, lifts to exactly one simple directed cycle. Exterior adjacencies are complete to the corresponding gadget, so every such local choice is realizable. Distinct choices yield distinct cycles. Choosing the least unexpanded vertex as root counts cyclic rotations once. Even if a gadget is visited twice, the two visits occupy distinct positions after this root, so their path assignments are ordered; no division by two is appropriate. There is no reversal quotient for directed cycles.

The independent compressed search enforces distinct unexpanded vertices and the least root. Its complete transition list derives directly from the separately constructed base arc set. A repeated base arc cannot arise under these constraints. Hence it enumerates the same objects without relying on the original search's used-arc bookkeeping.

## Local formulas and exterior arcs

For one visit, endpoint choices contribute (d+1)^2 and middle choices contribute 2^k, followed by removal of the empty path. For two labelled visits, each endpoint layer contributes d^2+d+1 and each middle vertex has three choices; inclusion-exclusion removes empty paths. This proves A and B.

For a first path starting at a fixed initial-layer vertex, the other path has d possible initial choices (another endpoint or none). At the final layer both paths have d^2+d+1 choices, and middle vertices have three choices. Removing an empty second path gives B0. The analogous counts with the first path starting at singleton layer i, or at a final-layer vertex, give exactly Ai, Bi, Afinal, and Bfinal in REVIEW.md. Thus the local endpoint comparison proves the exterior maximum without depending on the paper's exterior-cycle injection.

For a specified exterior arc, mark its unique occurrence in the contracted cycle. At the marked gadget, call the path entering through this arc the first path. This relabelling of the two visits is bijective and justifies substituting A0 or B0 regardless of where the marked visit lies relative to the canonical root.

A Hamiltonian base path from the unexpanded endpoint to the gadget endpoint, avoiding the original base arc, lifts after reversal to a new cycle. Use only the specified vertex in the endpoint gadget, and choose an initial endpoint, an arbitrary middle subset, and a final endpoint in each of the other nine gadgets. These independent choices give exactly d^18 2^(9k) distinct cycles in this subfamily. This establishes G as a lower bound, not as the entire created-cycle count. Since every exterior destroyed count is at most F and F<G, the strict conclusion follows. The reverse isomorphism transfers it to gadget-to-unexpanded arcs.

## Interior arcs and structure

For an interior arc p→q, any destroyed cycle has consecutive vertices p,q. Exchanging these positions gives a cycle with q→p after reversal. If the predecessor lies within the gadget it is in a strictly earlier layer than p; otherwise it is an exterior predecessor adjacent to every gadget vertex. Either way it reaches q. The symmetric argument makes p reach the old successor. The vertex set is unchanged and remains simple. Swapping the two marked vertices back is an inverse on the image, proving injectivity. Unaffected cycles stay unaffected, so total cycles do not decrease. Consecutive singleton middle layers can be exchanged to exhibit an isomorphism after their connecting arc is reversed, explaining equality cases.

The reverse permutation fixes unexpanded vertices, exchanges the x and y gadgets at each expanded base index, reverses gadget layers, and preserves an arbitrary corresponding endpoint index. This is a bijection; the independent full-arc-set test verifies it exactly.

The structural argument for strong 2-connectivity is also sound: deletion of an unexpanded vertex leaves a strongly connected base remainder, while deletion inside a gadget leaves a nonempty substitute for that base vertex. Complete inherited exterior adjacency allows routes to and from every remaining gadget vertex. The independent all-deletions graph test additionally checks this property for the certified instance.

## Reproduction and scope

Run:

    python3 independent_audit.py

The program compares exact results against `certificate.json`. Its searches and explicit graph checks are finite, reproducible computational evidence supporting the mathematical reduction; they are not a proof-assistant formalization or brute-force cycle enumeration of the large expanded graph. No external publication was performed as part of this audit.
