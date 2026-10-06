# Four bounded approaches

Problem GRAPH-005 (1392); investigation date 2026-10-06.

The source/history preflight was completed before the approaches. The inherited problem/report pair had an empty report object. Its background held generic dated literature triage, not a substantive proof attempt. Matching GitHub searches returned no earlier investigation; this is bounded search evidence rather than an exhaustive-history assertion.

1. **Direct palette simulation.** Tested the proposed idea of ignoring or merging the new color. A fixed palette projection can turn a properly colored edge into an improper one. Additional Bob moves therefore require an invariant, not an appeal to extra options for Alice. Hollom's ordered-game result is a further warning about vertex-order-independent transfers. Outcome: no general proof; no purported ordinary-game counterexample.

2. **Color-independent defensive scheduling.** Reserve Alice's earliest moves for vertices of degree at least the palette size. The exact bound $2h_q-1\leq q$ gives a complete winning strategy. Its contrapositive supplies necessary high-degree conditions for a monotonicity counterexample. Outcome: proved sufficient condition and necessary restrictions; it does not cover all graphs winning at a smaller palette.

3. **Permanent safe-part structure.** In complete multipartite components, touched parts stay colorable forever. Constructed a synchronized shadow game with componentwise color-count domination, handling every legal real Bob move and preserving global turn order across components. Outcome: a full monotonicity theorem for disjoint unions of complete multipartite graphs, including singleton parts. No novelty claim.

4. **Minimal-order exclusion.** Combined ordinary colorability, the reservation lemma, and a universal-vertex clique obstruction. Outcome: every graph on at most five vertices satisfies the requested implication for every positive palette size. This is an exhaustive proof by palette cases, not a computational search.

Stopped after these four approaches with a bounded partial result. No general theorem, general counterexample, least counterexample order, or complete characterization of winning graphs is claimed. No fifth approach or executable search was run.
