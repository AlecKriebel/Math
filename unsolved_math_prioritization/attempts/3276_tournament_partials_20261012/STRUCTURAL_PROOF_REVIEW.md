Editorial note: The complete authored text is preserved below. Only references to undistributed operational artifacts, their identities, locations and replay directions have been replaced with descriptive prose. Mathematical arguments, evidence counts, corrections and limitations are retained. This prose edition identifies its distributed files and public scholarly sources. Historical conditions in the source record are distinguished from current dependency status in ACCEPTANCE_AND_DEPENDENCIES.md.

# Independent mathematical review: recovered structural partial

This report is reconstructed after the execution workspace reverted to an older snapshot. The earlier local author packets and unfinished audit were no longer present. Historical hashes are not evidence that their bytes survived. Acceptance is bound only to the freshly reconstructed author edition and audit hashes recorded in the final report and manifests. This is recovery of the same research pass, not an additional substantive pass.

## Exact target and credited dependencies

The target concerns every nonempty finite tournament with arcs colored from a palette of three colors: either a directed cyclic triangle is rainbow, or one vertex reaches every other vertex by monochromatic directed paths. The color can depend on the destination. A transitive rainbow triple is not the forbidden configuration, and an incoming sink is not the outgoing source being asserted.

The source is Agelos Georgakopoulos and Philipp Sprüssel, [On 3-coloured tournaments, arXiv:0904.1967v2](https://arxiv.org/pdf/0904.1967v2). Its Lemma 2.1 explicitly credits Shen for the distinguished-cycle reduction. Lemma 2.7 is the switch lemma. Proposition 2.8 already rules out strict even two-color alternation. Proposition 2.4 and Theorem 3.1 supply the separate incidence-core hypotheses. These are credited dependencies, not new results of this packet. The core deduction is reviewed conditionally on the source theorems; this report does not certify the entire source proof of Theorem 3.1 or the unrestricted conjecture. No novelty or priority claim is made.

## Distinguished cycle and switch direction

In an induced-subtournament-minimal counterexample D, define an auxiliary arc y -> x only for distinct x,y when x cannot reach y monochromatically. This must be an actual tournament arc, since x -> y would itself be a monochromatic path. Every vertex has an incoming auxiliary edge, so a directed cycle exists. Its vertices still fail to reach their respective predecessors inside its induced subtournament; deleting vertices cannot create paths, and the absence of a cyclic rainbow triangle is hereditary. That induced subtournament is a counterexample. Minimality therefore makes the cycle spanning.

If x had a second failed target y besides its cycle predecessor, y could not be its successor because of the actual cycle edge. The auxiliary chord y -> x closes a proper directed cycle along xCy, contradicting minimality. Consequently the predecessor is the unique failed target. The cycle with this property is unique up to rotation; this does not assert uniqueness of all Hamilton cycles in the tournament. Self-pairs are explicitly excluded, so no convention about positive versus zero-length paths affects this argument. The distinguished cycle has length n >= 3.

Index its vertices by Z/nZ, with actual cycle edge i -> i+1 of color w_i. If w_i=a differs from w_(i+1)=b, then i+2 must reach i because i is not its predecessor. It cannot do so in a, because appending i -> i+1 would reach the forbidden predecessor of i+2. It cannot do so in b, because prefixing i+1 -> i+2 would let i+1 reach its predecessor. It therefore reaches i exclusively in the third color c. If the direct arc pointed i+2 -> i, its color would be c and the three vertices would make a cyclic rainbow triangle. Hence the actual direct chord points i -> i+2.

The forced backward edge in the relaxation represents a monochromatic path, not an actual tournament arc. Confusing those notions reverses the source lemma's direct chord.

## Exact forced-graph characterization

For each color c, construct F_c with edges i -> i+1 when w_i=c and i+2 -> i when w_i,w_(i+1) are the two distinct other colors. Each edge represents actual c-reachability in a hypothetical minimal counterexample. Concatenating the represented paths gives a monochromatic walk, from which repeated vertices can be removed to obtain a path between distinct endpoints. Thus any F_c path from x to x-1 excludes the cycle word.

The two step types cannot occur consecutively in the same walk. A +1 step u -> u+1 requires w_u=c; a following -2 step requires w_u != c. A -2 step u -> u-2 requires w_(u-2) != c; a following +1 step requires w_(u-2)=c. Hence every nonempty walk consists of only one step type.

At n=3 the arithmetic destinations of +1 and -2 coincide. One edge can have both generator labels, as happens for color 0 on edge 0 -> 1 for word 012. The adjacent-step contradictions still hold: an edge with both labels can have no preceding or following same-color edge. Such a single edge does not reach its predecessor. No unjustified disjointness of the two generator sets is assumed.

A pure forward walk first reaches x-1 after n-1 steps, precisely when w_x,...,w_(x+n-2) are all c. A pure backward walk reaches x-1 only if 2k=1 modulo n. Even n has no such solution. For odd n its first positive solution is m=(n+1)/2, and all later solutions require the same initial m steps. Their existence is exactly the condition that, for j=1,...,m, the pair w_(x-2j),w_(x-2j+1) consists of the two distinct colors other than c. The pairs cover all integer positions from x-(n+1) through x-1, hence every cyclic position. Thus c is absent from the entire word.

Conversely either explicit condition supplies the required walk. This establishes the exact characterization of the relaxation for all n >= 3. It does not characterize realizable tournament completions.

Every word using all three colors survives: n-1 equal entries would leave room for only one other color, and the backward condition requires an absent color. This is a complete obstruction to extracting more three-color exclusions from these generators and their monochromatic transitive closures alone. In particular periodic 012 words survive, as does the rainbow cyclic word 012 at n=3. Other tournament constraints reject some such words; the relaxation deliberately omits those constraints.

## Binary spacing, parity, and sharpness boundary

For a word using exactly two colors, forward failure occurs exactly when one used color appears once and the other n-1 times. At even n there is no backward failure, so the word passes exactly when both used colors occur at least twice. Strict even alternation therefore survives the relaxation although the stronger source Proposition 2.8 excludes it.

At odd n, let c be the absent third color and m=(n+1)/2. Its forced graph has only -2 edges. Since gcd(2,n)=1, all possible such edges form one directed n-cycle. An edge starting at x is missing precisely when w_(x-2)=w_(x-1). These starts are a uniform translation of nonswitch positions t with w_(t-1)=w_t; translation preserves cyclic distances in step -2 order.

If consecutive missing edges have distance d in that order, the intervening run has exactly d-1 surviving edges. A predecessor is reachable precisely when a run has at least m edges. Therefore avoiding third-color predecessor reachability is equivalent to every cyclic gap being at most m, including the last-to-first gap. Equality is allowed. A sole missing edge has gap n, not zero.

A closed binary word changes color an even number of times, so the number r of nonswitches is odd and positive for odd n. If r=1 then its gap n exceeds m. Thus a surviving odd binary word must have at least three nonswitches, as well as the spacing bound and the used-color multiplicity bound. Three nonswitches alone are not sufficient: for example 0010011 has a step-order gap 5 at n=7 and fails the third-color test. A monochromatic word passes the absent-color test vacuously but fails the forward condition; it is outside the exactly-two-color classification.

The lower bound is sharp only for the relaxation: 00011 at n=5 survives, and 000(10)^(k-1) at n=2k+1>=7 has nonswitches {0,1,2}, step-order gaps k,k,1, and at least two entries of each used color. These color words are not counterexample tournaments.

## Incidence deletion and the precise retention argument

Repeatedly delete any vertex that, in the current induced tournament, has fewer than three incident colors, fewer than two incoming colors, or fewer than two outgoing colors. Call a vertex set stable when every one of its vertices satisfies all three retention requirements inside the set.

Fix a stable set S. Its vertices retain all their existing color witnesses while the ambient set contains S. At the first attempted deletion from S, that vertex would satisfy every retention requirement and could not be deleted, a contradiction. Thus every stable set survives every deletion schedule. The terminal set is itself stable (the empty set is permitted) and contains all stable sets. It is the unique largest stable set and is independent of deletion order. This is vertexwise witness preservation. A superset of a stable set need not be stable, because its new vertices may fail the requirements.

A minimal counterexample is stable by the credited Proposition 2.4 and Theorem 3.1, so it survives inside the terminal core. For a nonempty tournament T without a cyclic rainbow triangle, if the target is known for every order at most b and its core has at most b vertices, a minimal counterexample inside T would contradict that finite premise. Empty core suffices without computation. Nonemptiness of T is essential for a universal-source conclusion. Neither a source of the core extending to T nor merely checking the core itself is asserted.

The specialization b=8 depends on a separate computer-assisted finite result. This structural audit does not itself enumerate all tournaments through eight. The prior finite acceptance was read before rollback, but its historical artifact hash must not be described as currently verified unless recovered. The final acceptance report states exactly which current or historical dependency is available.

## Fresh independent checks and unresolved frontier

The reconstructed audit compares independently indexed set/BFS and Boolean-matrix closures on all 29,511 labeled words of lengths 3 through 9, including exact start/color failure sets. It separately checks all 43,688 binary words of odd lengths 3 through 15 against cyclic gaps, parity, and one-repetition exclusions. All three-color words must survive and even binary multiplicities are checked.

Hostile controls reverse switch direction, reuse an incident color, force repetitions instead of switches, omit the wrap switch, merge colors, target the successor, and cross either gap boundary. Invalid lengths, palettes, Boolean and floating colors, and gap domains are rejected explicitly. Core tests compare three deletion schedules against exhaustive stable-subset unions in 801 deterministic sampled tournaments of orders 1 through 9, examining 102,002 subsets. Fixed controls refute substituting degrees for distinct-color counts, omitting the third-incident-color requirement, or assuming stable supersets must be stable. These fixtures make no rainbow-free source-existence claim.

These computations corroborate and test the implementation; the proofs establish the all-size deductions. The relaxation excludes no genuinely three-color word, and surviving binary words have no realization guarantee. No general order-nine tournament claim, unrestricted conjecture resolution, novelty certification, or source-proof certification is made.
