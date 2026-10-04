# PR66 graph audit: prior-opinion-exposed, conditional pass

Reviewed head: `78f4a7fadac0fd24e147a617956cb409eb6a579e`.
Original candidate: 9,121 bytes; SHA256 `fc2be9794873073e6482e8dfe93ccfd6c5d6f8674c2058ba0a8fc900d906d698`.
Target: original `source_record.json`, AMR-103-0033 / 10400033, Willerton's Conjecture 2.11: every classical knot diagram with n crossings satisfies `|v3| <= floor(n(n^2-1)/24)` in the stated trefoil-one normalization.

## Verdict and boundary

No defect found in the arrow-pattern-to-graph map, random-completion domination, tournament identity, floor, parity refinement, or n=0,1,2 handling. No graph repair is required. The strongest universally verified result is the **formal graph theorem stated below**. Applying it to the actual knot invariant remains conditional on the imported formula (4) and its normalization being correct. The source-formula family is checking that dependency separately. Finite Jones replay is calibration evidence, not certification of that identity for every classical diagram. Priority and current literature status are unknown in this review.

This review is **prior-opinion-exposed**. The original SOURCES.md and README.md were mistakenly included in an input batch before the first saved conclusion; their last paragraphs contain historical review-success summaries. The FIRST_CONCLUSION files preserve this disclosure and their original timestamp/hash. No historical review proof or code, historical verdict JSON, sibling mathematical conclusion, or ROOT mathematical verdict was inspected. The report must not be counted as a pristine independent pre-opinion vote. Its deductions and executed independent programs remain directly checkable.

## Formal theorem and proof

Let A be any finite collection of n directed chords with distinct endpoints on an oriented circle, with arbitrary signs epsilon_i in {-1,1}. Let P and T be exactly the cyclic directed-arrow types encoded in the candidate:

    P = {(3,0),(5,1),(2,4)}, coefficient 1/2
    T = {(3,0),(1,4),(5,2)}, coefficient 1.

An occurrence is one unordered three-element chord subset up to positive cyclic endpoint relabeling. Define Q by summing the products of the three signs with these coefficients. Then, without any realizability or knot-invariance assumption,

    |Q| <= M(n),
    M(n) = n(n^2-1)/24   if n is odd,
           n(n^2-4)/24   if n is even.

Both expressions are integers in their respective parity classes, and M(0)=M(1)=M(2)=0. Consequently `|Q| <= floor(n(n^2-1)/24)` for all n>=0.

1. **Unique edge direction.** An intersecting pair has alternating endpoints. Starting at tail(c), either their order is tail(c),tail(d),head(c),head(d), or tail(c),head(d),head(c),tail(d). In the first case tail(d) is on c's positive tail-to-head arc while tail(c) is outside d's; in the second case these memberships exchange. Thus exactly one of c->d and d->c is chosen. A positive cyclic relabeling preserves this order and direction. Reversing the circle reverses every edge. Nonintersecting pairs receive no fixed edge.

2. **Pattern map.** In P, write c=(3,0), a=(5,1), b=(2,4). Exactly c-a and c-b intersect, with b->c->a. In T, write c=(3,0), a=(1,4), b=(5,2); all pairs intersect with c->b->a->c. No converse is needed. Their intersection counts distinguish P from T, so a subset cannot contribute to both. A cyclic isomorphism may admit several embeddings, but the defined sum assigns the subset its coefficient once; T's rotational automorphisms never multiply it.

3. **Domination.** Fairly and independently orient the absent pairs to obtain a finite random tournament. A T subset is cyclic with probability 1. A P subset is a directed path with one absent pair, so precisely one of that pair's two directions closes the cycle; probability 1/2. Every other subset has a nonnegative probability. Thus the sum of local cyclic probabilities is at least N_T+N_P/2. The arbitrary-sign triangle inequality gives `|Q| <= N_T+N_P/2`. Linearity of expectation equates the local probability sum with E C. No independence among triple indicators is needed, and no signs enter the random graph construction.

4. **Exact tournament count.** For any tournament, every transitive triple has exactly one source pointing to both other vertices. Hence

        C = binom(n,3) - sum_i binom(d_i,2),
        sum_i d_i = n(n-1)/2.

   With mu=(n-1)/2, expansion gives

        C = n(n^2-1)/24 - (1/2) sum_i (d_i-mu)^2.

   This is an identity, not an approximation or random-model assumption. For odd n, nonnegativity of the variance gives M(n). For even n, every integral d_i differs from the half-integer mu by at least 1/2; the variance sum is at least n/4, giving the stated M(n). The candidate's weaker floor bound is applied to each integer C before averaging; it never falsely assumes E C is integral.

5. **Arithmetic and boundaries.** For odd n, the consecutive even neighbors n-1 and n+1 give a factor 8, and one of n-1,n,n+1 gives a factor 3. For n=2k, the refined value is k(k-1)(k+1)/3, an integer. The difference between the target floor and M(n) for even n is floor(n/8). For n<3 there are no selected triples and Q=0; n=0 does not require defining a mean degree.

The tournament maximum equals M(n) for every n, so no extra hidden loss is needed. For n=2k+1, direct edge i->j when the nonzero residue (j-i) modulo n lies in {1,...,k}. Every vertex has degree k and the variance vanishes. For n=2k, delete one vertex from the regular tournament on 2k+1 vertices. Among the remaining vertices, k have degree k and k have degree k-1, so every squared deviation is exactly 1/4. The cases n=0,1,2 agree with these constructions. This establishes the all-n extremal identity independently of finite enumeration.

## Exact executed checks

`independent_graph_checks.py` uses restricted-growth double-occurrence endpoint words, event necklaces with first-appearance label normalization, and adjacency bitsets. It does not import any original verifier. This differs from the original sorted modular arrow-pair canonicalizer and matrix representation.

- All 32,055 directed chord diagrams through n=5, including the empty diagram.
- All 995,573 sign assignments over those diagrams.
- Every one of the 33,868 tournaments through n=6, including n=0.
- Exact local completion probabilities, circle rotation/reversal, single-arrow graph switching, degree and variance identities, and parity bounds.
- Extremal constructions checked through n=100, with the universal construction proof above supplying the all-n result.
- 1,494,879 exact assertions passed. Counts measure bounded diagnostics, not proof strength.

The n=3 local histogram gives 40 no-edge types and 48 one-edge types with probability 1/4; 12 two-edge source/sink types with probability 0; six uncounted directed paths and six P types with probability 1/2; six transitive complete types with probability 0; and two T types with probability 1. This confirms that extra paths provide slack rather than overcounting.

`completion_dependence_checks.py` independently enumerated every one of the 761 partially oriented complete graphs through n=4 and all 4,166 associated completions. In every case global average cyclic count exactly equals the sum of local probabilities and obeys the extremal bound. Its two explicit overlapping-path examples have individual cyclic probabilities 1/2 but joint probabilities 1/2 and 0, respectively, versus marginal product 1/4. Dependence is real and does not invalidate linearity of expectation.

Byte-identical copies of the original controls were run in `original_replay/`. The original graph verifier passed 42,684 assertions on 1,814 directed chord diagrams and 1,099 tournaments; the original Jones verifier passed 183 assertions on 59 classical braid closures. Both exited zero with empty stderr. The original graph verifier shares its canonicalizer and signed evaluator with the Jones script; the independent implementation above checks that coupling with a separate representation. Original bounded tests omit n=0 and do not directly assert the variance identity; the independent tests and proof cover both. These are coverage limits, not discovered author failures.

Two initial replay invocations failed because my runner's default cwd was the audit root while the scripts lived in `original_replay/`. Both failed commands, full stderr, exact cwd/argv/PID/UTC/exit, and hashes are preserved in the ledger. The corrected invocations passed. No failure was relabeled or erased.

## Custody, gaps, and completion

`ACTUAL_COMMANDS.jsonl` records actual executed child argv, PID, cwd, UTC start/end, exit, timeout status, output paths, bytes, and SHA256 hashes. The first bootstrap has its separate truthful receipt. Full stdout/stderr bodies are retained, including launch failures. `ORIGINAL_REPLAY_MANIFEST.json` authenticates the copied candidate and controls. A bounded final manifest records this folder's artifacts and its explicit receipt cutoff.

No original file, shared native artifact, Git index/ref/branch, PR, editor state, or publication record was mutated. No outside human contact occurred. The original 1/5 attempt ledger is preserved. This was completed-candidate verification, with no central proof search or additional proof-attempt turn.

Graph-family review completion estimate: 100%. Strongest result: a universal proof of the precise formal arrow bound and exact tournament maximum. Remaining target-level gap outside this family: independently establish the imported classical v3 formula, normalization, exact target source correspondence, and any publication/priority conclusions. No graph counterexample or required graph repair found.
