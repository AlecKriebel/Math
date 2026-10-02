# Full independent five-turn review request

Problem 30000417 / OWR-1189-007. Proposed unsolved 5/5. All five genuine author turns are frozen; please do not undertake a sixth author search while auditing them.

## Source and scope

Read the entire Kohl contribution, OWR 7/2006 printed pp. 414–417, especially Definition 1 and Theorem 6/Conjecture 2 on p. 416. Visually verify **floor**, not catalog ceiling, and the n>=3 context. Lists are arbitrary natural-number sets, list cardinality is the parameter, and absolute separation d applies at both path distances 1 and 2. Kohl's 2006 dissertation pp. 100–102 supplies the credited boundary and restricted-list cases. Raw PDFs are in the sibling sources directory and their hashes are in SOURCE_MANIFEST.json. The neighboring all-trees question is outside scope.

## Proof obligations

Read all five TURN_n.md files completely:

- Turn 1: exact gap compression preserves all >=d comparisons, not just order; finite bound and reachability induction; credited n=3 and d=1 proofs; nonexhaustive exploration is not a completeness claim
- Turn 2: strict weighted-path deficit bound; modulo-three removal leaves precisely an ordinary path, including boundaries; common-label interval deletion; exact floor/ceiling arithmetic and smallest/largest-label hypotheses
- Turn 3: all initial six-list pairs, every next-list transition and full closure at palettes 6/7/8; rank expansion is only a one-way feasibility implication; no empty state entails all lengths; explicit P6 five-list obstruction; the failed robust-row invariant is not mistaken for a counterexample
- Turn 4: variable anchors have no mutual original constraints; unary/pair costs account for every remaining vertex exactly once; Bellman recurrence and complexity; local minima delete at most d labels even when adjacent anchor labels differ; all three optimum costs in the 42-vertex certificate equal 4, while its direct valid labeling really works
- Turn 5: optimized row-contribution lookup is exactly the same transition relation, full nine-label closure completes with no cap in Python, and the full state-set hash matches the separately written packed C++ check; the ten-label cooccurrence graph is complete, forcing any single global cardinality-preserving recoding to be injective; the d=3 obstruction is below the proposed size and does not refute the source

The strongest completed computational theorem is **all n, d=2, six-element lists, union size<=9**. Its conclusion is not restricted to n<=43: 43 is only the largest shortest prefix depth in the archived C++ state graph. Conversely the proof does not allow an unbounded union or general d. No minimality claim is made for the 42-vertex method counterexample or the recoding example.

## Replays and resources

From this directory, for t=1,...,5:

    python verify_turn<t>.py > /tmp/pathlabel-turn<t>.json
    cmp TURN_<t>_CHECKS.json /tmp/pathlabel-turn<t>.json

The scripts use only Python 3 standard library. `verify_turn4.py` imports the frozen local `anchor_solver.py`. Turn 5 may take around two minutes and several hundred megabytes; it has no state cap. The C++ cross-checks are optional independent implementations, with compiler requirements stated in TURN_3_LOG.md and TURN_5.md. A CAPPED exploratory outcome is never a proof.

The authoritative nine-label state-set SHA-256 is 1e684d75b22798311196274b81cbaae77fe4154a5b691998ddabfc3a6819f791 (numeric ascending 81-bit relations in 11 little-endian bytes). The eight-label hash is 3ea7f8e4f654d66687a1496695f6a63b310fc41dbf00b234f10115dd5c4d9563. Check the complete transition semantics and closure, not just these checksums or counts. The hashes bind computed certificates; the written induction explains their mathematical use.

Verify FINAL_FROZEN_MANIFEST.json, every TURN_n_MANIFEST.json and both source PDF hashes. All historical author files are unchanged. No raw PDFs, imported records, generated large state binaries or private queue files are public packet content.

Please return a scoped PASS/FAIL with exact mandatory corrections, a portable independent report and an integrity manifest. Acceptance should leave the genuine original as unsolved 5/5. A catalog-transcription counterexample, a restricted-palette theorem or an obstruction to a proposed proof method must not become a full-resolution claim. Novelty is not certified.
