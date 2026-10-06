# Independent audit: original vertex-coloring game, problem 1392

Audit date: 2026-10-06. Queue rank: 880. Accepted status: **PARTIAL**.

## Verdict

The six-member author freeze is accepted unchanged as a bounded mathematical partial. No proof correction is necessary. All strategy claims, including the complete-multipartite real/shadow simulation for arbitrary interleavings of components, are valid under the stated original Alice-first rules. The reservation lemma and the exclusion of counterexamples on at most five vertices are deductive proofs, not computational evidence. The note does not resolve the general problem and claims neither novelty nor a least counterexample.

The original archive has 11,070 bytes and SHA-256 `1040dbf33688acffa32ef332cab8bfd6f72c8edf49ddb62bdbde73816261a4a7`. Its original external manifest has SHA-256 `9ac8c6a1723b1a138231eb4155b235556e5d865ad6c083bca6292453618ed25c`. Every member was checked against both that manifest and the supplied authored directory. The audit archive includes exact, unchanged copies under `author/`; it is not a corrected author derivative.

## 1. Identity, corpus, and history checks

The catalog and complete problem corpus each have 15,458 records. The exact numeric identifier 1392 selects one record in each; the catalog record has rank 880. Its statement and complete-record/report-pair digests match the author preflight. The three entire input files, not excerpts or reconstructed records, were hashed and parsed. Their public verification metadata is recorded separately in `INTEGRITY_REPLAY.json`; no input contents are included.

An important identity collision was checked: `GRAPH-005` occurs twice in each record corpus. The other numeric identifier is 1329. Selecting by problem number alone can select the wrong problem and yields a different pair hash. This audit selected 1392, independently reproduced the expected complete pair hash, and checked the catalog's corresponding stored digest. The report mapping has no `GRAPH-005` key; the specified `reports.get(problem_number,{})` therefore returns an absent-key default empty object. It is not an existing substantive report that was overlooked. The entire target record, including its complete background, was inspected; it contains generic dated literature triage and no earlier mathematical proof attempt.

The pair was serialized exactly as Python's default `json.dumps([complete_problem_record, reports.get(problem_number,{})], sort_keys=True).encode()`. This retains all record fields and the default spaces and ASCII escaping. No projection, changed separators, Unicode-normalized reconstruction, or statement-only digest was substituted.

A fresh bounded repository check reproduced the author preflight's substantive conclusion. Issues/PR search returned no matches for `1392`, `GRAPH-005`, the phrase `Coloring Game`, and `monotonicity`. Commit searches for the first two identifiers returned none; `coloring` returned six unrelated subjects. Default-branch indexed-code searches for the problem number and full title returned none. Branch searches returned no relevant branch; the three unrelated `coloring` results were inspected and the continuation page exhausted. These are search results at audit time, not a certificate of complete repository history. The public problem page could not be fetched by the web tool; the original full-record hashes provide the verified problem identity.

## 2. Original rules and source boundaries

The audited game is on a finite simple undirected graph, with Alice first and a shared fixed palette. A turn colors one previously uncolored vertex while preserving properness. No pass, recoloring, vertex-order restriction, or connected-play restriction is permitted. Alice seeks a full coloring; the appearance of an uncolorable vertex is an irreversible Bob win. Allowing further legal moves elsewhere after that event gives the same winner because forbidden colors cannot disappear and there are only finitely many vertices.

Zhu's original introduction was independently inspected through indexed pages 1–2: it confirms the first player, the proper vertex-coloring move, and the two outcomes. Direct PDF opening failed again. No Zhu PDF was acquired or hashed by this audit. The distinction from the marking game is substantive: an ordering/back-degree strategy is not inferred from an arbitrary coloring strategy. A separately indexed author definition corroborates the same original game and the marking-game distinction. Source links: [Zhu's original paper](https://www.math.nsysu.edu.tw/~zhu/papers/game/planar.pdf), [Zhu's definition page](https://www.math.nsysu.edu.tw/~zhu/definitions/def-gamechi.htm).

The [published Hollom article](https://doi.org/10.1016/j.dam.2024.01.007) was freshly downloaded from its Cambridge repository PDF endpoint. All 361,650 bytes reproduce the pinned SHA-256. The repository identifies it as published and peer reviewed; the eight-page PDF identifies the journal, volume, pages, and DOI. Its introduction and Question 1.1 expressly retain the original question as unresolved there. Its Section 3 construction establishes the invoked ordered 3-to-4 obstruction; Figure 1 and both relevant strategy proofs were inspected. The unrestricted statement of Theorem 1.4 in that source is broader than the range justified by its displayed proof. This package prudently invokes only the verified 3-to-4 case. Arboricity and connected-game results are not transferred to the original game. The proof here has no mathematical dependence on their formulas or other variant-specific theorems.

The [Obszarski–Turowski–Zięba v2 paper](https://arxiv.org/abs/2304.12073v2) was also freshly downloaded: all 173,181 bytes reproduce the author's pin. Its Section 1.3 supports permanent color availability inside a touched part and the fixing-move viewpoint. Its stronger formulas are for its stated special classes; no formula is used to infer the new note's union/singleton scope. This is attribution and a priority safeguard, not a substitute for the audited proof.

The [2026 singleton multipartite article](https://doi.org/10.1016/j.disc.2026.115291) was checked at publisher-indexed abstract/metadata level only. Its December 2026 issue date was not mistaken for an online publication date; no full-text conclusion was inferred. The [tree paper](https://doi.org/10.1007/s40314-026-03919-7) has verified publisher HTML stating online publication on 2026-09-28 and a 2027 volume assignment. Neither source is evidence of a general palette-monotonicity solution. A fresh bounded literature search found no verified later general resolution; this does not prove that no unindexed resolution exists.

## 3. Proposition 1 and the reservation lemma

### 3.1 Colorability and maximum degree

A winning Alice strategy produces a complete legal play against every Bob reply. In particular, one such play provides a proper coloring with the given palette. This establishes ordinary colorability as a necessary condition, without asserting the converse. If every vertex has degree less than q, it cannot see all q colors among its neighbors. Every uncolored vertex therefore remains playable; a turn removes one uncolored vertex, so play finishes. The empty graph already satisfies Alice's terminal objective.

### 3.2 Priority strategy, with all move times checked

Let H consist of vertices of degree at least q, and let h be its size. If h=0, the preceding argument applies. For h>0, Alice always colors an uncolored member of H when one remains. Her j-th turn is global move 2j−1. Bob coloring members of H can only reduce the number that Alice must handle; he cannot create a new member of H, because H is defined from the original graph's degrees.

Before move 2h−1, at most 2h−2≤q−1 vertices have been colored. An uncolored vertex cannot yet have q differently colored neighbors, since this would require q distinct colored vertices. Thus no Bob move or earlier Alice move can have caused a loss before the last required priority move, and the selected high-degree vertex has a legal color. This covers every Bob vertex/color choice, not only choices inside H. If all vertices are colored sooner, Alice has already won.

On the move that exhausts H, any uncolored vertex has degree less than q, independently of the number or arrangement of colors used. Such vertices remain safe after that move and forever thereafter. This addresses the boundary case 2h−1=q: the q-th move can introduce the q-th color but cannot block a remaining low-degree vertex. Arbitrary legal colors on Alice's priority moves therefore suffice. No strategy in a different game is invoked.

### 3.3 Contrapositive and rounding

For a failure at q=k+1, the reservation condition must fail: 2h−1>k+1, or h>(k+2)/2. As h is integral this is precisely h≥floor((k+2)/2)+1. A one-color winning graph is edgeless, so k≥2 in any counterexample. Proper k-colorability follows from successful play. Failure at k+1 also requires maximum degree at least k+1. All claimed necessary conditions are therefore correct; none is sufficient for a counterexample.

## 4. Theorem 4: full synchronized strategy audit

### 4.1 Structural facts and invariants

Inside one complete multipartite component, vertices of different parts are mutually adjacent. Properness forces every used color to belong to exactly one part of that component. A color may be reused in another component; there is no need for a global color allocation.

Once a part has a colored vertex, that vertex's color is legal for every remaining vertex in the same part for the rest of the game. Any vertex in another part is adjacent to that colored witness and can never receive its color. Thus a touched part remains safe, even if Bob introduces additional colors into it. Conversely an untouched part sees exactly the component's used colors. It is blocked exactly when all palette colors have been used in that component. When every part is touched, the component remains safe regardless of subsequent new colors.

The simulation maintains more than a numerical inequality:

1. Both partial colorings are proper and color exactly the same vertices.
2. The two histories have the same length and the same next player. Shadow Alice has followed the fixed winning k-color strategy throughout.
3. Corresponding parts have the same touched status, hence corresponding components have the same secured status.
4. In every unsecured component, real and shadow color counts satisfy r≤s<k≤q. No count condition is imposed on secured components.

All four properties hold in the initial state, including k=1. They are local by component except for the synchronized move counter and fixed global shadow strategy.

### 4.2 Alice in a previously touched part

Use the vertex selected by the shadow winning strategy. It is uncolored in the real game because the colored vertex sets agree. The real move reuses an existing color of that part; legality is permanent by the structural fact above. Its real component color count does not increase. The shadow count either stays fixed or rises by one, since the shadow strategy may reuse or introduce a color. Thus r≤s is preserved if the component was unsecured. The touched status does not change.

The shadow move is the prescribed move of a winning strategy after a reachable shadow history, so it cannot create a lost shadow state. For an unsecured component this implies s<k after the move. A previously secured component stays secured, and reusing its part color requires no comparison of counts. This explicitly covers Alice moving in a secured component while some other component remains unsecured.

### 4.3 Alice in an untouched part

The component is necessarily unsecured before the move. Since r≤s<k≤q, at least one real color has not appeared in that component. Giving it to the chosen vertex is legal. In the shadow game every legal color for that untouched part is also new to its component. Therefore both counts rise by exactly one, preserving r≤s.

If other parts remain untouched, the winning shadow strategy excludes a post-move loss, hence s<k. If this was the last untouched part, both components become secured simultaneously. Their counts may now reach their palette sizes, but that creates no blocked vertex: every remaining vertex belongs to a touched part. The inequality is correctly dropped in this case. A singleton part becomes fully colored on the same first touch and obeys exactly this argument.

### 4.4 Bob in a previously unsecured component

Observe any legal real Bob move, including moves that reuse a color, introduce a color into a touched part, or touch a previously untouched part. Copy its vertex to the shadow game and assign a color unused in that shadow component. This color exists because s<k before the move. Being unused in the component makes it legal at every vertex there. Legality does not require a color map from the real palette or agreement with Bob's real color.

The shadow count rises by one. The real count rises by either zero or one. Thus r′≤s′ follows from r≤s. The same vertex is colored, so touched and secured statuses continue to agree. The resulting shadow history is a legal Bob reply after a history consistent with the winning strategy. A legal reply that immediately blocks a vertex cannot exist at such a history: otherwise Bob could choose it and defeat that strategy. Therefore the new shadow state is non-lost. If the component remains unsecured, s′<k; if it is secured, permanent safety applies instead.

The potentially delicate boundary is s=k−1 with Bob playing in a touched part while another part is untouched. The fresh shadow color would be legal at Bob's chosen vertex but would block that untouched part. This contradicts reachability after a winning shadow strategy. Consequently that purported synchronized Bob-turn situation cannot occur. The argument does not silently redefine legal moves to exclude losing moves; it uses the universal property of the fixed winning strategy. Similarly, when Bob touches the last untouched part, exhaustion of the shadow palette is harmless because the component becomes secured.

Even if the real rules declare a loss immediately after Bob's move, the proof may analyze the paired shadow reply as a mathematical construction. The paired post-state establishes that the real move cannot in fact cause that loss. No extra real turn or delayed-loss rule is assumed.

### 4.5 Bob in a previously secured component

Every part there is touched in both games. Copy Bob's vertex and reuse any color already in its shadow part. This is legal and keeps the shadow component secured. His real move can use any legal real color, including one new to that component. Neither count matters once secured. Other components and their count inequalities are unchanged.

### 4.6 Global alternation and termination

The proof never runs separate per-component games or inserts local passes. A Bob move in a safe component still consumes a Bob move in the single shadow history, and the next Alice vertex is chosen by the original global strategy at exactly that history. Thus arbitrary interleaving, differing component sizes, and parity do not invalidate the construction.

After every paired move, a real untouched part retains a color because r≤s<k≤q; a touched part retains its witnessed color. No real uncolored vertex is blocked. Both games gain exactly one colored vertex each turn, so after at most |V| paired moves both are fully colored, possibly ending on either player's move. When no vertices exist, no move is needed. Isolated vertices are singleton components, and complete graphs are multipartite with singleton parts. The proof also covers a disjoint union initially presented with edgeless multipartite blocks, since their connected components are isolated vertices.

This proves W_k(G) implies W_q(G) for all q≥k in the stated class. The proof does not assume a monotone formula for the game chromatic number, componentwise independence of the winner, or a universal fixed projection of palettes. Its structural invariant is unavailable for arbitrary graphs. Acceptance of this theorem is therefore consistent with the unresolved general question.

## 5. Theorem 5: every palette and order boundary

For an empty graph the conclusion is immediate. Otherwise assume at most five vertices and W_k(G).

- k=1: proper one-colorability forces no edges, so two colors win.
- k=2: a proper two-coloring gives a global bipartition. Choose the smaller side A, with |A|≤2. Every vertex outside A has degree at most |A|≤2, so all degree-at-least-three vertices lie in A and h_3≤2. Hence 2h_3−1≤3. The bipartition may include isolated vertices and disconnected components; no connectedness assumption is used.
- k=3 and at most four vertices: maximum degree is at most three, so four colors win.
- k=3 and five vertices: degree-at-least-four means universal. Three universal vertices and any fourth vertex would form a four-clique. Proper three-colorability prohibits this, so h_4≤2 and 2h_4−1≤3≤4.
- k≥4: the larger palette k+1 is at least five, strictly greater than maximum degree, which is at most four.

The cases cover every positive integer palette size. The claimed order-six lower bound for a counterexample follows, but existence at six or any higher order does not. No graph enumeration is needed or represented as performed.

## 6. Approaches, scope, and acceptance boundary

The four recorded approaches are accurately labeled. Fixed palette merging is not a legal-state map in general: two merged colors may occur on opposite ends of an edge. The priority strategy proves only a sufficient winning condition. The multipartite proof supplies its own rigorous invariant. The order-five exclusion is a bounded consequence. None proves that all smaller-palette wins satisfy the reservation hypothesis, and none supplies a general counterexample.

The audit independently reviewed each mathematical claim and every strategy transition, rather than substituting examples or games played against a heuristic opponent. There was no game-state search. Integrity scripts were used solely to hash, parse, compare, and package files and provenance metadata. These are distinct from executable mathematical certificates and are not included in the safe release.

No author file was changed. Consequently no correction patch or corrected derivative is needed; creating a vacuous patch would suggest a defect that was not found. The separate acceptance report pins the unchanged accepted input, states all accepted and excluded claims, and records the replay result. The safe archive excludes third-party PDFs, extracted source text, corpus records, private coordination material, and executable files. This audit performed no publication or repository mutation.
