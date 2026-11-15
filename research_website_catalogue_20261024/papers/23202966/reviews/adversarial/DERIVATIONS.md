# Checkable local derivations and adversarial controls

The independently sealed paper-first reconstruction in INITIAL.md contains the full source, fooling-set and pullback arguments. This later note makes their dependencies and finite checks explicit. No external exponential theorem is proved by the computations below.

## Uniform certificate for the source and ordinary interpretation

Let B_j be the set of states U(p,0) reached after j complete blocks, starting with B_0={U(p,0):p in H}. For a block encoding R, the exact transition relation from U(p,0) to U(q,0) after b consumed bits is R(p,q). Indeed, U's only transition out of its row-counting family chooses a 1 in row p; every choice at p h+q preserves q until the block ends. Failure to choose an edge blocks at the final bit of row p. Therefore, by induction, B_j consists of endpoints of length-j relation paths starting anywhere in H. B_j is nonempty exactly when R_1...R_j is nonempty. Between boundaries all reachable U states have t>0 or V states, and none can accept on the right marker. This proves full-word, not promised-alignment, recognition.

The ordinary source removes the marker-initial state and isolated final state and substitutes a final start i_0. For every nonempty bitword c v, the successor set after the first bit is the union over p of the U(p,0) successor sets. This is exactly the marked source after its left-marker move followed by bit c. No transition returns to i_0. Finality of U(p,0), tested only after all bits are consumed, is equivalent to the marked final marker move. Empty input accepts at i_0. The independent control's source computation starts from the set of U(p,0) states and tests the boundary condition after full consumption, so it tests the common body computation of both variants; it does not construct two separate state-labelled machine objects.

## Uniform certificate for the cubic lower bound

There are h^3 indices (p,t). For matching indices the concatenation of x and y is enc(P_p I P_p). For different offsets, its length differs from 3b by a nonzero integer of absolute value below b. For matching offsets and different vertices its product is P_p I P_r=empty. These explicit equations establish every off-diagonal rejection for every h, not merely the sampled h values. State collisions at the input cut are impossible by run splicing. For a marked right-only run, early acceptance would survive one-bit extension and contradict the malformed-length rule, ensuring the cut is reached.

## Uniform certificate for the pullback

Write pi((q,t),j)=(q,(j-1)b+t+1) at body cells, with all phases projected to their corresponding markers. For each allowed direction d, the following equality is exact at every body cell:

pi(body_successor((q,t),j,d)) = binary_successor(pi((q,t),j),d).

At either marker the same equality holds because the marker row is independent of phase and inward motion resets to 0 or b-1 as appropriate. Outward moves are disabled on both sides. The scanned binary symbol is the relation's adjacency bit at t. Thus the labelled transition relation is both preserved and lifted from every fibre of pi. From the initial configuration, induction gives a bijection of possible transition-label histories up to the harmless multiple marker phases; accepting states and transition counts are preserved. This is sufficient for nondeterministic finite reachability and for deterministic targets. An infinite nonfinal path cannot create a finite accepting path in either direction. The empty-word case follows from the same marker equations, with adjacent distinct markers.

## Fresh finite controls, staged before native-code exposure

The source of independent_controls.py was written from the manuscript and the independent mechanisms above, fully displayed/read, then run before any native scientific code or expected result was opened. The result and receipt files were staged before native exposure. **There was no separate immutable pre-exposure seal of those result files.** The preceding INITIAL proof/exposure/input seal is immutable and earlier; these are distinct chronology claims.

The ordinary unoptimized control run exited 0, retained its complete 547-byte stdout and zero-byte stderr, and checked:

- 11,238 source-word comparisons: all binary words through length 12 for h=2, all through length 10 for h=3, plus 500 seeded varied-length words for each h. A decoded relation reachability oracle is independent of the U/V state simulation.
- 20,514 complete fooling cross comparisons for h=2,3,4,5, using the relation oracle rather than accepting-run state assumptions.
- 351 local movement/projection cases for h=2,3, relation lengths 0,1,2, every compressed cell, every phase, and every direction, including disabled moves and all marker phases.
- 109,200 target acceptance comparisons: 200 seeded deterministic/nondeterministic target profiles of 1–4 states, every h=2 relation word through length two, and both zero-step and positive-run acceptance. Reachability is bounded by the complete configuration graph rather than a time cutoff.

Two deliberately incorrect alternatives were falsified. A wrong phase reset on a rightward internal block crossing was detected for h=2, relation-word length 2, first body cell, phase 3, right move: required expanded position 5 but mutant projects to 8. A malformed-word-ignoring alternative accepted the one-bit word 0 by truncating it to the accepted empty word, while K_2 rejects it. These are controls on the checking mechanism, not defects in the published construction.

Weaknesses: source state transitions are a literal manuscript implementation, and target pullback tests share the manuscript's intended phase rules. The independent relation oracle, geometric movement projection and deliberately broken variants provide cross-checks, but no finite suite proves universal correctness. Many randomly generated targets accept trivially because their initial state is final under zero-step semantics; others have no accepting runs. Counts are comparisons performed, not counts of nontrivial distinguishing instances. The local lifting proof is essential.

## Selected native checker replay and limits

After the above staging, the complete native binary_compiler.py, full README, complete clean_reproduction.py runner, and the complete expected JSON objects were read. The exact selected code SHA256 is 013a096ca48a8a8123d6f28adf32b6e6d517ef7bd9d125450e6950ee772b49d0. A byte-identical isolated own copy was run once normally and once with Python -O, without the optional file-output argument. Each run exited 0; each whole stdout was exactly 398 bytes with SHA256 3e30d8164277a55c920028e08bcb7cc4d45da2f90ad9c9de958a03afdcbfbe9c, byte-identical to the original expected receipt. Each stderr was empty. Full typed comparison of the complete expected object, including all keys, key order, types, Python version 3.14.6, scope string, counts, and the complete state-count mapping, had no differences.

The normal run meaningfully checked 1,534 source words, 288 exhaustive partial one-state deterministic targets, 128 seeded two/three-state nondeterministic targets, 227,136 pullback comparisons, and the finite fooling families. Its `fooling_pairs=100` counts family members summed for h=1,2,3,4, not pairwise crossings. The expected source-state mapping is 1:3, 2:13, 3:41, 4:96, 5:187, 6:323, 7:513, 8:766. h=1 is an extra implementation check outside the paper's stated h>=2 theorem.

Most native scientific assertions are Python assert expressions. Optimization removes them, including the calls inside the assertion expressions. Therefore the optimized run's same printed success/counts are **not** an independent successful scientific check. It demonstrates reproducible program output under optimization and exposes this limitation. The normal run retains assertions and is the meaningful native replay. No assertion was added or changed in the native program.

The runner was read but not executed: it also runs archived audit/upstream algebra scripts and builds a PDF, beyond this selected replay's scope. No source helper, builder, archived review checker, upstream algebra script, Lean build, or formal axiom/comparator check was executed. The recorded clean-reproduction receipt's TeX SHA256 effc61c3809b0290f4b9a063c7a7dbc389e512d38e81683d0bea0cee42f19aa5 differs from the currently deposited main.tex SHA256 b6aa5b342c1b4a919d1f938f26f0b5f5242d7bbaac9e74540899621ff6441910. That historical build receipt therefore does not certify a build of the current TeX bytes, even though its selected checker SHA matches. This is a reproducibility/provenance qualification, not a discovered contradiction in the current proof or the inspected PDF/TeX mathematical content. The current PDF and current full TeX were read directly; no fresh PDF build is claimed.
