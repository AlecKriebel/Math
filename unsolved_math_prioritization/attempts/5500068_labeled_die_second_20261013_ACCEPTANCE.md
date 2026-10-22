# Independent acceptance of the second labeled-die mathematical edition

Date: 2026-10-13. TOPP Problem 68, row 1758, identifier 5500068 / AMR-054-0068.

## Verdict and exact accepted object

**Accepted without an outstanding correction in the reviewed scope.** The ten-file second edition preserves the complete accepted cycle-rank algorithm proof, the four complete no-hole gadget proofs, and the substantive underlying independent mathematical audit. Its extracted foundations supply the mathematical prerequisites actually used. Its exact small authored certificates passed a separate recomputation, including adversarial checks of selection semantics and negative controls against incomplete or corrupted certificates.

The reviewed public manifest is `PUBLIC_MANIFEST.json`, SHA-256 `435cde5cb0a694e2f7944cea92af4019c342382abe11f44f952e30bd172a24b5`. This report accepts that exact edition. It does not by itself assert any later modified edition has passed review.

The unrestricted complexity classification remains unresolved. The accepted algorithm is fixed-parameter tractable in surviving cycle rank, not an unrestricted polynomial-time algorithm. There is no hardness proof, new general uniqueness claim, worldwide novelty certificate, or completed no-hole reduction. Across the first and second editions there are exactly two newly documented substantive passes; the prior lifetime count is unknown. This review and the preparation of inspectable certificates add no research pass.

## 1. Proof-preserving editorial changes

Every public mathematical file was read in full. The three complete second-pass documents were compared against the already accepted authored reports. The recorded transformations were checked in both directions against complete bytes, and the retained originals were compared directly with the accepted inputs.

- `CYCLE_RANK_KERNEL.md`: three replacements add a foundations link, replace implementation references with the public verification/certificate explanation, and make the De Biasi Figure 4 attribution explicit. The algorithm, propagation rules, kernel inequalities, affine completeness and soundness arguments, and complexity analysis are preserved.
- `NO_HOLE_GADGETS.md`: four replacements change verification and source-boundary references and add public crosslinks. All four statements, their proofs, and their interface limitations are preserved, including the center-in-gadget qualification.
- `INDEPENDENT_MATHEMATICAL_ACCEPTANCE.md`: eight replacements remove packaging/API references, identify the public proof/certificate context, and clarify attribution and scope. The substantive kernel and gadget proof challenges and all bounded check outcomes are preserved. The text clearly identifies this as acceptance of the underlying results; it does not falsely present the earlier audit as a completed review of the new edition.
- `FOUNDATIONS.md`: the extraction keeps the die convention, phase parity, unique-state-edge fact, color rule, no-projected-square argument, and checkerboard-area obstruction. The complete source text is reversibly retained. The omitted first-pass singleton/domino proof is not an unproved dependency of the kernel bound: the new bound only uses the directly established fact that an ambiguous nonterminal has four distinct surviving physical incident edges. Full propagation is proved inside the new kernel report. Links to the unchanged first edition supply the fuller structural context.
- `SOURCE_IDENTITIES.json`: byte-identical to the accepted first-edition source identities. It does not represent new retrieval or a new literature search.

These are proof-preserving editorial changes, rather than shortened substitutes for the complete second-pass proofs. The ten-file manifest is complete and its byte lengths and hashes match. All 28 local Markdown crosslinks resolve either within this edition or to the stated unchanged first-edition files. The first edition's entire public file set and manifest were checked unchanged.

## 2. Independent challenge of the kernel argument

The branch conditions are essential and are present: fixed initial state, distinct final cell with fixed final state, exact degrees one at the two terminals and two elsewhere, propagation to a fixed point, and rejection of disconnected candidate graphs and forced cycles. A forced terminal-to-terminal path is accepted only if spanning; otherwise it rejects. The one-cell case is separated.

The unique-state-edge property prevents a single physical adjacency from supporting two states. Each forced edge pins its endpoint states, so the forced components in a surviving unresolved branch form disjoint paths and isolated vertices. Contracting a forced forest removes the same number of vertices and edges. Retaining every optional edge, with parallel identities and loop incidences, preserves `k = |E| - N + 1` exactly.

The fixed-point degree argument was challenged at isolated cells, chain ends, terminals, and loops. A fixed-state isolated nonterminal of degree two would have forced both edges. An ambiguous isolated cell has four distinct incident edges. Each nonsaturated chain end needs at least two optional incidences because a sole remaining continuation would already be forced. The two terminal components are distinct and each has degree at least two. Hence `2m >= 3n - 2`, giving `n <= 2k` and `m <= 3k - 1`. A nontrivial unresolved zero-rank kernel cannot occur; the earlier cases handle it. The search-size bound counts combinatorial records, while the reconstruction chain record and coordinate bit lengths are acknowledged separately.

For a connected multigraph, each non-tree edge gives a fundamental even-degree vector, including a singleton loop vector. Eliminating non-tree edges from an even-degree set leaves an even-degree forest, necessarily empty. Thus the affine terminal-path coset has exactly `2^k` distinct members, and every possible solution appears. Exact node degrees, physical port quotas, full-state consistency, and selected connectedness are each checked separately. After expansion these imply one spanning open path with the prescribed states. Conversely every physical solution survives and induces one accepted affine member. This establishes soundness and completeness without silently assuming pinned orientations everywhere.

An explicit `O(k^2)` basis and Gray-code updates permit `O(k 2^k)` candidate work with polynomial decision space. The report correctly distinguishes this per-branch bound from the fixed- and selectable-start enumeration of endpoint/state branches. No claim bounds general surviving `k` by a constant or logarithm.

## 3. Independent challenge of the gadget arguments

**Adjacent neutral detours.** The terminal equality permits taking the direct first edge and then reversing the original traversal. Each visited cell keeps its identical full state, so relabeling cannot eliminate the alternate endpoint while preserving the stated neutral traversal. The claim is local and correctly leaves open globally enforced endpoint exclusion. The two-port principle requires a proper region, only the two allowed accesses, and both global endpoints outside it.

**Rigid ribbons.** The periodic field is closed under every label-compatible move from the specified state. The four-residue horizontal calculation identifies exactly the permitted rungs. The two bottom corners are leaves; odd-row vertices force all vertical edges; saturation eliminates intermediate rungs; top and bottom matchings leave exactly the serpent. The north-first case uniquely fixes the initial state, while the east-first case immediately has no permitted unvisited continuation. This establishes selectable-start uniqueness, not just existence of one displayed path. The word calculation gives terminal state `W(q)`, equal to the longer straight displacement only for widths divisible by four. Boundary isolation and supplied entry states remain explicit embedding obligations.

**Pair-copy collars.** Same-pair cross-edges are impossible in every orientation. Translating the alternating along-rail pair sequence by one cell reverses its phase, independent of opposite-label signs. Two interior collar cells for length at least four then have at most one usable outward edge each. They are not board corners, so a corner-rooted Hamilton path cannot make both its final endpoint. The phase and geometry restrictions are preserved.

**Compatible eight-cycles.** Bounding-box area and Pick's formula leave area three or four. The three-face case has checkerboard imbalance one in magnitude and fails the phase-cycle condition modulo three; the four-face case is the two-by-two unit-face square. Its four center-arrival states are distinct, so any simultaneous center state has compatible degree at most one. The filled rectangle includes the center, which cannot be the initial corner, so it must be the final endpoint. A center uniquely determines its eight-cycle. The gadget corollary explicitly includes the enclosed center in the endpoint-free gadget; a ring-only subset does not satisfy that premise. Label-only projected cycles are never treated as simultaneous compatible full-state cycles.

## 4. Independent authored-certificate recomputation

A separate checker used coordinate transformations of labeled face normals and did not import the edition's preparation or validation programs. It checked complete record sets, rather than merely replaying the examples that happened to be listed:

- All 24 rotations, all 96 directed rolls, and consistent phase parity
- Every visit of the 4-by-3 ribbon and its reverse; all 17 physical adjacencies; all eight parity/residue rung records; all four initial yaws and first-move continuations; exhaustive label-compatible path search yielding exactly one selectable-start path
- Both ten-cell adjacent-cap routes, their identical cell-to-state fields, neutrality of the intended endpoint, and distinct migrated endpoint
- The closed eight-cycle, actual center geometry, all four boundary-to-center demands, their distinctness, and all 24 possible center states
- All sixteen distinct four-cell collar sign assignments, all cross-edge prohibitions, all 48 along-collar edge records and their opposite phases
- All eight affine candidates of the authored loop/parallel graph, compared with direct enumeration of all sixteen edge subsets; exact path selections are precisely its three singleton parallel edges
- Every degree, port, state, loop and selected-connectivity outcome in the five abstract semantic records representing six audit checks

The semantic challenge reproduced the intended distinctions. The path-plus-disjoint-cycle passes local degree/port/state tests but fails selected connectedness. The same-chain-end selection has correct contracted degrees and connectedness but fails port quotas. Its opposite-end replacement passes. The singleton with conflicting tags fails state agreement. The selected-loop record rejects and also fails terminal degree, exactly as disclosed; no false independence claim is made for that example.

Nine negative controls were also rejected: an omitted orientation, altered ribbon label, invalid center, duplicate collar assignment, duplicate affine candidate, and attempted waivers of selected connectivity, port requirements, state agreement, and loop rejection. These controls establish that the checker detects the specified missing or false certificate conditions. They do not enlarge the mathematical theorem.

Both the edition's validator and this independent checker were run on actually restored edition bytes in normal, `-O`, and `-OO` modes. Within each checker all three outputs were identical and successful. Optimization does not remove the checks.

## 5. Attribution, public boundary, and remaining limits

The producer and independent aggregate outcomes in `VERIFICATION_SUMMARY.json` agree with their accepted records. The distinction between producer tests, independent tests, and this edition's authored examples remains clear. The broader previously accepted board searches and source-board computations were not rerun as a new research exercise in this editorial review.

The 270-cell aggregate is attributed to the two already known De Biasi Figure 4 witnesses in *Rolling a Cube can be Tricky*, May 2012 Version 0.03. Its 278 candidate edges, 259 forced edges, 11 kernel nodes, 19 optional edges, cycle rank nine, 512 parity candidates, 92,378 tested ten-edge subsets, three local degree completions and two connected completions concern **one shared endpoint/initial/final-state branch**. The edition does not claim a count for all branches or discovery of a new nonuniqueness construction. The source-derived arrays and routes are absent. The source aggregate cannot be independently reconstructed from the edition alone, and the guide says so.

Buchin et al. receive explicit credit for the parity reduction. The full and short source versions and date-qualified publication-status observations remain distinct. General contraction and binary-cycle-space methods carry no novelty claim. Abstract tagged graphs are explicitly not asserted to be realizable propagated die boards, and no surviving ambiguous-state rectangle is asserted.

The public files contain the authored proofs, acceptance, explanatory guide, small authored certificates, and permitted public-source/verification metadata. They contain no programs, copied third-party source documents or text, source-board arrays or routes, private coordination material, operational artifact identities, or raw execution streams. Public file hashes identify the published files, not a substitute for mathematical correctness.

The review found no unresolved proof-preservation, certificate, scope, attribution, dependency-closure, or publication-boundary defect in the accepted ten-file edition. Its exact source status remains bounded by the prior accepted source audit, and its general problem remains open.
