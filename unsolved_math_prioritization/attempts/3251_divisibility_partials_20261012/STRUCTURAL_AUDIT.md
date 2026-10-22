> Edition note: This complete authored text preserves the mathematical arguments and substantive audit findings. Original operational references and identities of material not distributed here have been replaced with descriptive prose. The independent audits are AI mathematical reviews, not human peer review or formal proof verification.

# Independent acceptance: structural reductions and clique-separator compatibility

## Verdict and frozen scope

**ACCEPTED as a partial mathematical continuation. The unrestricted odd-hole-free 2-divisibility conjecture is not resolved.** No mathematical correction is required to the frozen proof. The initial checker used optimization-sensitive Python assertions; that implementation defect was corrected before the accepted freeze. The accepted checker uses explicit failures in all interpreter modes.

The review verified a frozen author snapshot consisting of the complete proof, the original checker, its finite results, source metadata, and their manifest, against a separately supplied fixed anchor. All recorded payload hashes and lengths matched. Those original artifacts and their byte identities are not distributed in this prose-only edition. The complete authored proof is preserved in STRUCTURAL_PROOFS.md, with only operational references edited.

The reviewed snapshot did not inventory or certify deliberately excluded source captures or interpreter caches. Both the reviewed snapshot and its audit had complete, fail-closed inventories. No frozen author file was edited, and the audit did not perform a new mathematical research round.

The exact target is a finite simple graph with at least one edge, with no induced odd cycle of length at least five, admitting a partition whose two induced clique numbers are both smaller than the original clique number. This is not perfect divisibility. The edge exception and maximum-cardinality meaning of “maximum clique” are essential.

## Mathematical audit

### 1. Color grouping and initial reductions

If `omega(G)=k>=2` and `chi(G)<=2k-2`, group a proper coloring into two sets of at most `k-1` stable classes. A clique has at most one vertex in each class, so each part has clique number at most `k-1`. This implication is correct for a single graph; hereditary 2-divisibility requires applying it separately to all nonedgeless induced subgraphs.

For `k=2`, a shortest odd cycle in a nonbipartite triangle-free graph is induced and has length at least five. Therefore an odd-hole-free graph of clique number two is bipartite. For `k=3`, the cited Chudnovsky–Robertson–Seymour–Thomas four-color theorem gives the result by grouping colors in pairs. Thus the stated smallest-counterexample restriction `k>=4` is valid with that published theorem as an external input.

The direct antihole partition is also correct: in the original odd cycle, the two consecutive blocks induce paths of orders `q` and `q+1`, with independence numbers `ceil(q/2)` and `ceil((q+1)/2)`, both less than `q` for `q>=3`. In the complement each vertex has only two nonneighbors, excluding holes of length greater than five; a selected induced five-cycle would be closed under both neighbors in the original longer cycle, impossible. The hereditary bound `chi<=2^(k-1)` follows by induction and disjoint palettes, with empty parts harmless.

### 2. Minimal indivisibility and the local matching

The minimal-obstruction notion correctly quantifies over every proper nonedgeless induced subgraph. A smallest odd-hole-free counterexample has this property by heredity.

If removing a vertex decreased `omega`, that vertex and the remainder would immediately form a division. Therefore deletion preserves the threshold `k`. Every division of `G-v` is blocked in both colors: otherwise inserting `v` in an unblocked color would divide `G`. The obstruction in each color is a `(k-1)`-clique inside `N(v)`. These cliques are disjoint because the color classes are disjoint, yielding two maximum cliques intersecting exactly at `v` and degree at least `2k-2`.

The chromatic bound `chi>=2k-1` is the contrapositive of color grouping. In an optimal proper coloring the vertices in singleton classes form a clique, since two nonadjacent singleton vertices could have their classes merged. With `q` classes and at most `k` singleton classes, `n>=2q-k>=3k-2`. This argument applies to arbitrary graphs, not only critical graphs.

The matching lemma is correct. In the bipartite nonedge graph between the two neighborhood cliques, any subset `X` of one side together with the vertices on the other side outside its nonedge neighborhood forms a clique in `N(v)`. Its order is at most `k-1`, so the nonedge neighborhood has size at least `|X|`. The alternating-path proof supplied in the manuscript establishes the necessary perfect matching without a hidden structural assumption.

The elimination-order corollary uses a fixed original threshold `k`. Start below that threshold and insert vertices backwards. Failure of both choices would exhibit the excluded disjoint neighborhood cliques. A `(2k-3)`-degenerate graph provides such an order. This is a one-step division criterion, as stated, not an unqualified hereditary conclusion for every smaller threshold.

### 3. Core, connectedness and modules

The maximum-clique edge core is a spanning constraint graph. Every maximum clique is wholly inside one core component; if a core vertex separates the core, every maximum clique lies in one of the resulting blocks together with that vertex. Proper-induced-subgraph minimality supplies the necessary colorings, and a global color swap aligns the single shared vertex. This proves connectedness and absence of cut vertices for the core. These properties pass from a spanning subgraph to the original graph: deletion of a vertex cannot disconnect a supergraph of a connected graph.

Disconnected complement gives a nontrivial complete join. The clique numbers of its two nonempty sides add to `k`, so using one color for each side divides the graph.

The module argument handles both required cases. For a module containing an edge, a maximum clique meeting the module must meet it in a maximum clique of the module: every outside vertex in that clique is complete to the whole module, so a larger inside clique would enlarge the global clique. A division inside the module makes every such crossing maximum clique bichromatic. Maximum cliques outside the module are covered by the other proper induced graph. For a stable module, replacing its vertices by one representative preserves the clique number and all clique constraints; copying the representative's color lifts a division. This correctly avoids attempting to divide an edgeless module.

Deleting original edges outside maximum cliques can create odd holes. The manuscript explicitly retains this limitation, so no invalid transfer of odd-hole-freeness to the core occurs.

### 4. Clique-precolor extension

Lemma 6 is valid as stated, including its more general form without the hypothesis `omega(H)=k`. In a proper coloring with `q<=2k-2` classes, the precolored clique occupies distinct classes. If `a` classes must be red and `b` blue, the unused capacities are `k-1-a` and `k-1-b`; their sum is at least `q-a-b`. Assigning all remaining classes within those capacities gives a valid extension. Nonnegativity follows precisely from admissibility of the boundary coloring. Thus every side with `chi<=2k-2` permits all admissible clique-boundary colorings.

### 5. Exact separator criterion and numerical bounds

Fix the global threshold `k=omega(G)`, including for sides with a smaller clique number. A maximum clique cannot use vertices from two distinct components of `G-C`. It follows that a whole-graph division exists exactly when the feasible restriction sets of all sides have a common boundary coloring. This is an exact equivalence; it does not assert that independently chosen local divisions can be aligned.

For a minimal indivisible graph, each side's feasible set is nonempty and invariant under swapping colors. Removing one entire component produces a boundary coloring feasible for every other side. It cannot be feasible for the removed side. These witnesses belong to distinct swap orbits: if two shared an orbit, invariance would contradict their distinct excluded-side properties.

For a nonempty separator of size `s<k`, all `2^s` assignments are admissible and swapping acts freely, leaving `2^(s-1)` orbits. At `s=k` the two constant assignments form exactly one forbidden orbit, leaving `2^(k-1)-1`. Hence the asserted component-count bounds follow.

A side with `chi<=2k-2` would permit every admissible restriction by Lemma 6, contradicting its excluded witness. Therefore every side has `chi>=2k-1`. Applying the singleton-class bound with its own clique number at most `k` gives at least `3k-2` vertices per side. Since the separator was counted in every side, the total bound is exactly `n>=s+t(3k-2-s)`.

The component-active-clique claim is also correct: if no maximum clique met one component, any valid coloring of the remainder could be extended arbitrarily over that component.

For `s=1`, the orbit count rules out `t>=2`. For `s=2<k`, there are exactly two orbits (equal and different boundary colors), so a minimal obstruction has exactly two components and their nonempty feasible sets must consist of opposite single orbits. At `k=4`, every side has at least ten vertices, giving `n>=2+2(10-2)=18`. For any clique separator at `k=4`, `s<=4` and `t>=2`, giving at least sixteen vertices. All arithmetic is correct.

### 6. Stopping points and external mathematical inputs

The two shared-triangle colorings correctly show that arbitrary local divisions need not agree after a global swap. Two maximum cliques meeting at one vertex correctly exhibit a blocked deletion coloring even in a chordal, hence perfect, graph. Neither example is a counterexample to divisibility. In particular, the local matching obstruction alone does not imply an odd hole.

The induced `P5` conclusion uses Chudnovsky–Sivaraman's `(P5,C5)`-free theorem. The optional odd-antihole conclusion uses the Strong Perfect Graph Theorem after excluding perfectness and odd holes. These are external theorem dependencies, not new proofs supplied by this audit. The source-frontier audit and frozen bibliographic metadata support these accurately delimited uses. Full proofs of the CRST decomposition theorem and SPGT were not independently re-audited here.

Hoàng's [arXiv:2506.12660v2](https://arxiv.org/abs/2506.12660v2) states general clique-cutset exclusion as Conjecture 4.7. The manuscript correctly treats it as conjectural; no general clique-cutset gluing theorem has been used. The inspected literature does not establish the unrestricted target. No novelty claim is certified.

## Independent computational verification

The independent checker does not import the author's program. It computes clique data by direct pair tests, chromatic number by enumerating set partitions, all feasible two-colorings by direct subset enumeration, connected components by set search, and all local clique-pair matchings explicitly. The independent and author programs were each run under normal Python, `-O`, and `-OO`.

Every run gives exactly:

- 33,868 labeled simple graphs on zero through six vertices: `1+1+2+8+64+1024+32768`.
- 33,861 nonedgeless graphs, excluding one edgeless graph at each of the seven orders.
- 2,012,232 admissible nonempty-clique precolor instances in the author's stated `chi<=2omega-2` universe.
- 206,970 clique-separator identities, counted per graph and nonempty clique separator.
- 63,242 eligible module-coloring constructions.
- 120 blocked deletion colorings for the 12 labeled minimal indivisibles of order five.
- Zero minimal-indivisible clique-separator instances.

The 12 minimal indivisibles are the labeled five-cycles; these are not odd-hole-free. Thus the critical-separator numerical bounds have no nonvacuous instance in this finite universe. Their validity rests on the written proof. The 120 count includes color-swapped labeled colorings and is not a count of distinct graphs.

Additional independent adversarial cases include 6,060 admissible precolorings of cliques (including the empty clique) in complete graphs of order `2k-2`, for `k=2,3,4,5`; these test Lemma 6 when `omega(H)` can exceed `k`. Also checked: all four boundary assignments for two `K4` graphs sharing an edge; blocked extension in two `K4` graphs sharing one vertex although the graph itself divides; direct antihole splits at orders 7, 9, 11 and 13; and 34 abstract swap-orbit set-system cases confirming the combinatorial orbit count. These are regression tests, not an additional theorem or a larger-order conjecture search.

## Integrity controls and reproducibility

The input verifier requires both an input root and an external pin. Its expected manifest digest is hardcoded from the author's direct frozen pin. It rejects missing files, incorrect bytes or hashes, unexpected files or directories, symbolic links (including the manifest, payload, root and pin), malformed manifests, and mismatched stored result scope or counts. The complete inventory includes the manifest itself; the manifest is never silently exempted from file-type checking.

There are 24 controls in each of the three interpreter modes: one pristine positive and 23 required failures. Negative cases include a same-length proof mutation, same-length manifest mutation, missing mandatory inputs, extra entries, dangling manifest symlink, and an injected false mathematical check in the author program. Both the author and independent mathematical negative controls fail without emitting a result artifact in every mode. No correctness condition relies on a Python `assert` statement.

A separate review-bundle verifier checked the external review seal, its caller-supplied SHA-256 pin, the exact full review inventory, all file hashes and sizes, and all file types. Final post-seal validation records were kept outside the sealed review bundle, avoiding any alteration after sealing.

The original reproducibility procedure ran the independent checker and the frozen author checker over the same zero-through-six-vertex scope in normal Python, -O, and -OO, comparing exact counts rather than elapsed time. The frozen-input verifier checked the original snapshot and external pin; adversarial controls ran in a writable copy of the audit bundle in all three modes. Those executable tools and original records are outside this prose-only distribution. Their checked scope, outcomes, and limitations are retained here in full.

**Final acceptance:** the frozen proof's authored reductions and separator statements are mathematically sound, the bounded finite results reproduce independently, and the explicit limitations are necessary and correctly stated. Acceptance does not establish unrestricted 2-divisibility, general clique-cutset exclusion, novelty, or independent verification of entire cited source proofs.
