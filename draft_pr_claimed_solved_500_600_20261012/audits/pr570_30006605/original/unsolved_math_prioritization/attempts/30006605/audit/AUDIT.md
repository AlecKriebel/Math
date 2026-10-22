# Independent adversarial audit: weighted centers of median graphs

Problem 30006605, OWR-14299911-007, rank 598. Audit completed 2026-10-04 UTC.

## Verdict

**PASS within the stated model.** No blocking mathematical error or missing reduction step was found. The frozen candidate proves a deterministic O(n log^5(2n)) algorithm for a center, its optimum multiplicative radius, and the complete center set of a finite nonempty connected simple median graph with unit edges and nonnegative finite vertex weights, given by adjacency lists and equipped with exact comparisons of small-integer multiples of those weights.

This is an affirmative answer to the finite algorithmic interpretation of the target question, and the conclusion actually applies without a cube-dimension bound. The recommended queue disposition is **claimed_solved**, retaining the proof's model and attribution qualifications. This audit does not establish historical novelty, formal verification, independent human peer review, or a practical implementation of the fast median-graph oracle.

The input is promised to be median. No recognition algorithm or extra preprocessing certificate is part of the conclusion. An arbitrary real-number input is interpreted through the stated exact-operation model, not as an encoding-free Turing-machine input.

## Frozen object and independence

The reviewed object is the author's `bundle` in this problem's local research folder. The following hashes matched before and after the audit:

- `SHA256SUMS`: caf2e6e5806e8a8cc9359b3abd9cfa2626ba51cf5db88934b588389f53935f44
- `PROOF.md`: b0b948da64c113dfff1349a2aae48389531c2a8bd719dcdd2ab9483a6fc37d76

Every file named in the author manifest passed `sha256sum -c SHA256SUMS`. Nothing in that bundle was edited. All audit outputs are separate. The review inspected the proof, controls, frozen outputs, primary-source PDFs/text, current official metadata, and the exact upstream problem record. The fresh control program imports no author functions. No remote writes, publication, or third-party communications were performed.

## 1. Exact problem and scope

The official Oberwolfach report defines a nonnegative multiplicative vertex profile and asks for a vertex minimizing its weighted maximum distance. Its p. 505 asks the bounded-cube-dimension almost-linear-time question. The surrounding finite complexity discussion concerns n-vertex graphs. The general introductory definition also permits infinite graphs with finite-support profiles, but provides no finite encoding for an infinite graph. The candidate explicitly limits its algorithm to the finite input setting; it neither silently supplies nor claims an infinite-input algorithm.

The all-zero profile is consistently extended to radius zero everywhere, agreeing with Ducoffe's later explicit all-zero convention. Empty graphs, disconnected graphs, nonunit edge lengths, continuous centers, and implicit infinite inputs are excluded. These are scope boundaries, not unhandled cases inside the theorem.

## 2. The decisive imported theorem

The BDH public full text expressly defines additive eccentricity as max_u(d(x,u)+a(u)), with arbitrary nonnegative integer vertex weights. Its Theorem 1 applies to every finite connected median graph and gives O(n log^4 n) time. Algorithm 1 takes the graph and weights; its Theta-class and halfspace work is included in the analysis. No embedding, bounded dimension, pairwise-distance matrix, or supplied decomposition is an additional input hypothesis. The candidate supplies integers between 0 and n-1, entirely inside this interface. [BDH full text](https://arxiv.org/abs/2410.10235v1)

The published SODA identity, authors, page range 1679–1704, DOI, and publication date were independently checked on the publisher's site. The mathematical interface was checked in the public full version rather than inferred from the unweighted wording of the abstract. [Official SODA entry](https://epubs.siam.org/doi/10.1137/1.9781611978322.52)

The deterministic qualifier is supported by the concrete recursive algorithm: its searches and tie choices can be fixed by input order. Its imported Theta-class computation uses LexBFS, not a randomized success event. The latter dependency was checked in the primary ICALP account. [Theta-class preprocessing](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ICALP.2020.10)

This review validates the dependency's identity, hypotheses, output interface, and relevant algorithmic model. It does not claim a fresh independent proof or implementation of every lemma inside the published BDH theorem.

## 3. Threshold conversion

Let D=n-1. For R>=0 define b(u) as the greatest k in {0,...,D} satisfying kw(u)<=R, and set a(u)=D-b(u). For every vertex pair the distance d is an integer in [0,D]. Thus

    w(u)d <= R  iff  d <= b(u)  iff  d+a(u) <= D.

The first equivalence uses only nonnegativity of w(u) and monotonicity of its integer multiples. Taking the conjunction over u proves equality of the entire feasible sets, not merely agreement of their emptiness. Hence the additive labels can supply any witness and, at the optimum, all centers by one scan.

Adversarial boundary checks:

- If w(u)=0, every k is allowed, so b(u)=D and the constraint is vacuous.
- If R=0 and w(u)>0, b(u)=0, requiring the center to coincide with that support vertex.
- If R is exactly a candidate kw(u), the non-strict inequality includes k. Values just below it exclude k.
- If R/w(u) exceeds D, capping at D loses no graph constraint.
- R<0 is infeasible because every weighted radius is nonnegative.
- For n=1, D=0 and the unique vertex has radius zero for every finite weight.

No metric convexity, Helly property, local search, or tree-product representation enters this identity. It is valid on every finite connected unweighted graph; medianity is used only to accelerate the additive computation.

## 4. Implicit candidate search and exact ties

An optimum radius is attained at a vertex, and the corresponding maximum is attained at some demand vertex. Therefore it belongs to the multiset of n rows (0,w(u),...,Dw(u)). Enumerating that quadratic multiset is unnecessary: a pair of interval endpoints per row describes the active candidates.

For each nonempty interval of length L, the lower middle entry has at least L/2 active entries on each non-strict side. Sorting at most n such midpoints and taking the first cumulative selection weight reaching M/2 produces a valid weighted median, even when many midpoint values coincide. The cumulative mass strictly below the selected entry is less than M/2, so the mass at or above it is at least M/2; the opposite non-strict mass is at least M/2 by construction.

The strict pruning convention is essential and is implemented correctly:

- A feasible pivot q is saved as an incumbent before discarding all entries >=q.
- An infeasible pivot q permits discarding all entries <=q.

Thus either the incumbent already equals the optimum or an optimum candidate survives. On the feasible branch the rows whose midpoint is >=q contribute at least M/2 of the selection weight, and at least half their entries are discarded. On the infeasible branch the symmetric <=q rows do the same. In either case at least M/4 entries disappear, including singleton rows and flat zero rows.

After t iterations M_t <= n^2(3/4)^t. Since M is an integer, termination occurs after at most floor(log_(4/3)(n^2))+1 iterations. One further additive-oracle call extracts all centers. The exact constant is immaterial, but explicitly confirms the O(log(2n)) oracle count.

The initial incumbent D max_u w(u) is genuinely feasible at any vertex. The saved witness remains valid if a feasible pivot equals that incumbent. When the active set is exhausted, the invariant forces the incumbent to equal the optimum. This also handles singleton support and tied optimum values without assuming positive weights or strictly increasing rows.

## 5. Runtime and arithmetic

Each threshold profile takes O(n log(2n)) comparisons, using bounded integer binary search rather than division or an arbitrary-real floor operation. Sorting midpoints and pruning intervals have the same per-round bound. Over all rounds, operations involving the original input weights total O(n log^2(2n)).

Every feasibility call includes an entire O(n log^4(2n)) additive computation. Recomputing all of BDH's preprocessing on every call is already affordable; no unproved shared-preprocessing promise is needed. With O(log(2n)) calls, the total is O(n log^5(2n)). Reading adjacency lists is absorbed because finite median graphs have O(n log n) edges. Outputting up to n centers is absorbed as well.

All weight-dependent comparisons can be represented as kw(u) versus jw(v), with k,j in [0,D], together with zero comparisons. The incumbent and output radius can be retained as a symbolic pair (u,k). Arbitrary exact reals are legitimate in this model; finite-precision floating point would not certify these comparisons.

For rational inputs p/q with positive denominators and at most B bits, cross multiplication uses O(B+log n)-bit integers, up to constant factors. The O(n log^2(2n)) count is a count of input-weight comparisons, not a claim of the same bound for all bit operations. Reading rational encodings and paying their arithmetic costs are necessary. The frozen proof expressly withholds a uniform full bit-complexity theorem; this qualification is correct and must be retained.

## 6. Reproducibility and independent falsification

The author program was rerun unchanged. Its output is byte-for-byte identical to `CONTROL_RESULTS.json`: 10,626 optimization cases, 145,644 full feasible-set checks, 36,829 pruning steps, and the documented tree checks. The exact author case digest remains 59bd9887a91c84c1ef9dc47b52dedaccb55804387d6e5872dee795ae8b2ca9fa.

The separate `independent_controls.py` was written for this audit and passed:

- All 772 connected labelled simple graphs through five vertices.
- All 180,102 resulting graph/profile pairs for profiles over {0,1,2}.
- 2,500,246 full feasible-set comparisons, using exact rational threshold values at and between candidate values, plus negative and above-maximum thresholds.
- All 42,874 nonempty triples of nondecreasing rows of lengths 0 through 4 over {0,1,2}, checking arbitrary ties and unequal active-row lengths rather than only arithmetic-progression rows.
- 298,602 total implicit-search cases and 787,145 checked constant-factor contractions, including the graph cases and arbitrary-row cases.

The independent threshold reference enumerates allowed integer distances and uses direct graph distances, rather than borrowing the author's binary-search routine. Its search uses separate bisect-based interval code. The independent graph-case digest is 149f54c4fe0a6d8d2a8fbac7279b487056ace3cd2cd00b543e65f24b5862a437.

These are exact finite controls. They intentionally use explicit reference rows and quadratic distance storage where useful. They neither implement nor benchmark the fast BDH algorithm and do not replace the universal argument above.

## 7. Attribution, novelty, and correction disposition

Ducoffe's published ESA 2026 Lemma 2 is genuinely a general decision-to-optimization reduction with O((T+n)log n) time. The author correctly credits its weighted-median mechanism. The candidate's slightly weaker comparison-only variant is separately proved, so its correctness does not depend on constant-time real division in the earlier lemma. [ESA primary source](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ESA.2026.133)

No source located in this bounded review explicitly states the exact all-median consequence. That is not evidence sufficient to certify novelty. The threshold observation and resulting combination should be presented as a rigorously supported candidate result with honest prior credit, without a historical-priority claim.

No mandatory proof correction was identified. `CORRECTIONS.md` records two optional precision improvements: state the promised adjacency-list input at the theorem itself, and tighten the ESA lemma pinpoint to p. 133:6. Neither changes the mathematics or the acceptance verdict. The finite-input scope, exact-operation qualification, imported theorem, no-benchmark warning, and priority caveat are already substantive parts of the correct claim and should not be removed in summaries or publication.

## Reproduce

Run `python3 independent_controls.py` from this audit folder and compare the JSON to `INDEPENDENT_CONTROL_RESULTS.json`. Run the frozen author's `controls.py` and compare it with `AUTHOR_CONTROLS_RERUN.json` and the original frozen `CONTROL_RESULTS.json`. `SHA256SUMS` fingerprints all separate audit artifacts except itself. Hashes establish object identity, not a cryptographic signature or formal certification.
