# Independent mathematical audit: one common color

## Decision and exact scope

**ACCEPT** the theorem and its symbolic proof in [THEOREM.md](THEOREM.md). The proof is byte-identical to the independently accepted text; its distributed-file identity is recorded in MANIFEST.json.

Let G be a finite simple graph with maximum degree at most three, with no proper three-edge-coloring, such that G minus any one edge has a proper three-edge-coloring. For every assignment of exactly three colors per edge with nonempty total intersection, G is list-edge-colorable exactly when the assignment is nonconstant.

No correction to the candidate's mathematical argument is required. This audit accepts only that restricted theorem. It neither resolves the empty-intersection case nor asserts historical novelty. The proof is symbolic; bounded executable checks below are supplementary. The source-history statements in the candidate are outside this independent mathematical audit.

## Full symbolic audit

1. **Nonempty graph and component reduction.** The graph has an edge because an edgeless graph is three-edge-colorable. Some component is not three-edge-colorable. An edge in any other component would violate the deletion hypothesis. Hence all edges lie in one component, with any remaining vertices isolated. The line graph on the edges is connected, so a nonconstant assignment has incident edges bearing different lists.

2. **Permissible label for arbitrary deletion coloring.** Fix any edge e and any proper coloring of G−e using labels from a three-element set. An endpoint with original degree three sees exactly two distinct labels after deleting e, forbidding just one choice of the matching label. At most two such endpoints exist, so at least one of the three labels remains permissible. Degree-two or lower endpoints impose no constraint. Nothing in this argument requires every label to occur globally.

3. **Covering and residual degree.** A permissible label's color class is a matching avoiding e. Each original degree-three vertex away from e sees all three labels; each degree-three endpoint sees the chosen label by construction. All such vertices are covered. At vertices of original degree at most two, removing matching edges cannot create degree above two. Thus the residual graph has only paths, cycles, and isolated vertices.

4. **Exactly one odd residual cycle, through e.** Deleting e from the residual leaves a proper edge-coloring in the two other fixed labels. Consequently any odd residual cycle must contain e. Components of a maximum-degree-two graph are disjoint, so there is at most one such cycle. If none existed, the entire residual could be two-edge-colored, and coloring the matching with the third label would three-edge-color G. The hypothesis rules this out. This reasoning applies to every permissible label from every deletion coloring, not merely some favorable choice.

5. **Local overlap, including degree-two endpoints.** Choose incident edges e and f with distinct reduced lists. Each associated critical cycle passes through their shared endpoint v and uses exactly two incident edges there. Since degree(v)≤3, these two pairs share an edge g. Were both cycles list-constant, their constant values would both equal the list on g, forcing the distinct lists on e and f to agree. Therefore at least one cycle is nonconstant. At degree two the two incident pairs coincide, so this case is covered. The proof needs no assertion of global connectivity among critical cycles.

6. **Two-list path/cycle lemma.** A path is greedily colorable. For a nonconstant cyclic assignment, adjacent unequal two-element lists permit a first color absent from the last edge's list; sequential greedy coloring then automatically closes the cycle. Equal lists permit alternating colors on even cycles and cannot color an odd cycle. The equal cardinalities are sufficient for the asserted nonempty set difference.

7. **Assembly and converse.** Removing a globally common color c from each exact-three list leaves exact-two lists and preserves whether the assignment is constant. Color the selected matching with c. Its residual paths and even cycles are two-list-colorable, and its unique odd cycle is nonconstant by Step 5. Residual colors exclude c, so they cannot conflict with matching edges. Conversely, a constant exact-three assignment would give an ordinary three-edge-coloring, which is prohibited.

8. **Claim boundaries.** No restriction on order, palette size, or number of exceptional lists enters the argument. The reduction consumes deletion colorings for at most two incident edges; the candidate does not claim to find those deletion colorings efficiently. Over a fixed four-color palette, any two or three distinct triple types have a nonempty intersection; all four types have empty intersection and remain outside this theorem. A hypothetical nonconstant uncolorable exact-three assignment must therefore have empty total intersection, without implying that one exists.

An arbitrary degree-three-covering matching does **not** acquire the unique-odd-cycle property merely by covering those vertices. The proof validly uses the specifically selected color class of a deletion coloring. The candidate preserves this distinction.

## Independent bounded validation

A separately written Python implementation uses the author packet's seven explicit graph fixtures as shared inputs. It does not call or reuse the candidate's C++ implementation. The raw fixture collection is excluded from this prose edition.

The checker independently confirms all seven graphs are simple, subcubic, non-three-edge-colorable, and three-edge-colorable after every edge deletion. It exhausts every labeled deletion coloring and every permissible matching label on these fixtures, rather than selecting only one coloring per deletion.

Results:

- 1,020 labeled deletion colorings and 1,236 permissible-label instances checked
- 170 distinct edge/matching witnesses checked for degree-three coverage and a unique odd cycle containing the deleted edge
- 818 adjacent-edge pairs of distinct witnesses checked for a shared edge at the common endpoint
- 3,384 nonconstant common-color assignments checked: all 2,184 on the seven-edge fixture using reduced two-lists from three noncommon colors, plus 200 deterministic pseudorandom assignments on each of the other six fixtures using two-lists from eleven noncommon colors
- 18,606 full constructive colorings validated edge by edge, exercising every available witness pair for each selected incident-list transition; the second-cycle branch was used 48 times
- A separate backtracking coloring oracle also validated each of the 2,184 exhaustive seven-edge assignments
- All fixtures rechecked after adding three isolated vertices, with identical deletion-coloring and matching-witness counts
- 9,828 independent two-list coloring-oracle cases on cycles of lengths three through eight, verifying the exact cycle obstruction

Negative and boundary controls all pass:

- Constant exact-three lists are uncolorable on a critical fixture.
- Constant lists can be colorable if non-three-colorability is dropped.
- Nonconstant common-color assignments can be uncolorable if deletion-criticality is dropped, including a connected subcubic example.
- At degree four, two cycles through a vertex need not share any edge, showing why the local subcubic overlap argument cannot be extended unchanged.
- A constant odd cycle with two-element lists is uncolorable.
- Nonconstant two-element lists with a common color need not be colorable on a critical fixture, so the exact-three-list hypothesis cannot simply be replaced by exact-two.
- Using all four triple types on a four-color palette has empty total intersection and is outside the theorem.

These finite checks do not exhaust all graphs, assignments, or palettes. Their function is to independently exercise the construction, arbitrary-choice claims, and hypothesis boundaries. The symbolic proof establishes the unbounded theorem.

## Distribution and reproduction boundary

The complete symbolic audit and all substantive mathematical conclusions are preserved here. [THEOREM.md](THEOREM.md) is byte-identical to the accepted proof; MANIFEST.json identifies the actual distributed proof and audit files. The independent checker verified the accepted proof's identity before checking the shared fixtures. Its separately recorded audit inventory included the report, implementation, results and exact inputs.

Executable implementations, raw fixture and coloring collections, raw results, copied source documents, excluded-input identities and private coordination records are not distributed. The computational suites cannot be rerun or their omitted records reconstructed from this prose alone. Computational reproduction requires fresh implementation and fresh input generation. The symbolic proof is complete without those finite checks.

## Frozen author packet and replay

All twelve inventoried author files were checked against their recorded lengths and hashes, and the accepted proof and shared-fixture pins remained unchanged. This confirms input byte identity; it does not enlarge the mathematical or source-history scope of this acceptance. Only identities of actual distributed files appear in this edition's manifest.

The frozen author C++ checker was also rebuilt independently with `g++ -O2 -std=c++17` and rerun. Its output was an exact byte match to the frozen author result, reproducing all 2,644,056 successful assignment runs. The raw replay output was preserved in the audit packet and is not distributed here. This replay is additional corroboration, separate from the independently written Python checks.
