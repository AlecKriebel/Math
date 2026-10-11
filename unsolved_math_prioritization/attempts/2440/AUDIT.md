# Independent mathematical audit: outerplanar pancyclic excess

## Disposition and exact reviewed objects

**ACCEPT THE RESTRICTED RESULT AFTER THE LOCAL INTERNAL-CANDIDATE CORRECTION.**

The degree-constrained interval-complete weighted-tree theorem, its consequence h_out(n)-log_2 n->infinity, and the construction n=4k^2-19k+31 for every integer k>=3 are accepted unchanged. The star-weak-dual order bound n<=4k^2-19k+34 is accepted after repairing the intermediate substitution and endpoint calculation in the unpublished internal candidate. No published source is alleged to contain this error. The final bound and construction are unchanged.

The candidate-manifest SHA-256 is f00d50b6294f43f960417cfe613342af4480f0ade75a196c4887df9b7fa8abe6. The original candidate-proof SHA-256 is 4001a5a1709aad66225c1c0c19bd9b3737f354d9c92c29af22c92bb9420c54e8. The complete corrected-proof SHA-256 is db0348e038ad88543744a868d31ec1c6790176e3960f4e4c41139e99ba2b98e4. The original independent-audit SHA-256 is ee4239cf3f585681b30bee69d21a65eba83c56986b3965a4882ffb986d1ded9e, and its manifest SHA-256 is 6c16364167599926f9722b5ee11f9b761fcb631de4c9724a25117b3c69a6dd73.

The auditor authenticated all 15 original candidate members, totaling 3,046,357 bytes. Candidate executable code was not read for reuse, imported, or executed. The independent standard-library checker was written from the definitions. It generated labelled trees through edge-set enumeration and found graph cycles through cycle-space parity enumeration, rather than reusing the candidate's reported cycle-search method. The correction was applied to a separate copy and the original candidate remained unchanged.

## Required correction

Put

    F_k(c) = k + 2 + (c(c-1)/2 + 1) 2^(k-c+1).

The four permissible central weights are c=k-2,k-1,k,k+1. Their exact substitutions are

    F_k(k-2) = 4k^2-19k+34,
    F_k(k-1) = 2k^2-5k+10,
    F_k(k)   = k^2+4,
    F_k(k+1) = (k^2+3k+6)/2.

The unpublished internal candidate's third expression, k^2+6, is not the exact substitution. As written in that internal candidate, the claimed four expressions give 13,13,15,12 at k=3, so the internal-candidate sentence asserting their maximum is 13 is false. Although k^2+6 is a looser upper bound, that observation alone does not repair the internal-candidate endpoint argument.

The corrected successive differences are

    2(k-3)(k-4),
    (k-2)(k-3),
    (k-1)(k-2)/2.

All are nonnegative at every integer k>=3; the first is zero at k=3,4. The correct four endpoint values at k=3 are **13,13,13,12**. Thus the required maximum is the first expression for every permitted k. At k=4 the values are 22,22,20,17. This is a local arithmetic repair, not a new hypothesis or an asymptotic restriction.

The source title on the visually inspected first page is *Some Unsolved Problems in Graph Theory and Combinatorial Analysis*. The corrected bibliography restores the omitted word “Some”. This has no mathematical effect.

## Weighted-tree theorem: complete logical audit

### 1. Negating the limit and making the size unbounded

To negate W_i/2^(q_i)->0, one first takes an infinite subsequence on which this ratio is at least some fixed delta>0. The proof's opening contradiction setup is valid with this usual subsequence interpretation. The inherited W_i->infinity condition remains true on every such subsequence.

Interval completeness supplies W_i distinct nonempty connected sums. Hence

    W_i <= B(T_i) <= 2^(q_i)-1.

Consequently q_i->infinity. This step is necessary: large weights alone do not imply a large tree, but the required full initial interval does.

### 2. Centroid and matching count

A tree has a vertex c whose deletion leaves components of size at most floor(q/2). The usual descent to a component larger than q/2 terminates: after moving across an edge, the component on the side just left is smaller than q/2, so the same edge can never be traversed back during this descent. A tree has no other route back.

A connected set avoiding c lies wholly in one component. There are fewer than q such components, each having at most 2^floor(q/2) subsets; therefore the deliberately loose q*2^floor(q/2) bound is valid, including q=1,2.

Rooting at c, every connected set containing c is ancestor-closed. For each edge in a matching, the membership pattern “child present, parent absent” is impossible. Matched endpoint pairs are disjoint, so at most three patterns are available independently on each pair, and at most two choices remain on each other vertex. This gives 3^r*2^(q-2r). Counting some disconnected sets or sets omitting c only overestimates the target family.

After dividing by 2^q, the second term is exactly q*2^-ceil(q/2), which tends to zero. If delta is a positive lower bound on the ratio, eventually (3/4)^r>=delta/2; therefore the integer matching numbers are uniformly bounded on the retained subsequence. No conclusion about the original sequence's matching numbers is needed.

### 3. Bounded core, including endpoints

The endpoints C of a maximum matching form a vertex cover; maximality would already suffice. Outside C the vertices form an independent set. Since a tree of order at least two has no isolated vertices, if t outside vertices have degree at least two, their incident edges number at least |O|+t. There is no double counting of edges in that sum, because O is independent. The tree has |O|+2r-1 edges, giving t<=2r-1. Adding at most 2r nonleaves inside C gives b<=4r-1.

The theorem invokes this lemma only eventually at q>=3. Then b>=1. The vertices of degree at least two induce a connected subtree, since the internal vertices of the unique path between two of them also have degree at least two. Every other vertex is a degree-one leaf adjacent to that subtree: two adjacent leaves would constitute the whole tree of order two, already excluded.

### 4. Finite-coordinate subsequences

Bounded positive integer b permits a subsequence on which b is fixed. Arbitrarily label its core vertices 1,...,b in each tree. The labels need not preserve core topology. For each of the finitely many labelled leaf-count coordinates, pass to a further subsequence where that coordinate is either a fixed nonnegative integer or tends to infinity. An infinite constant subsequence exists if a value occurs infinitely often; otherwise a subsequence tending to infinity exists. Successive extraction over finitely many coordinates preserves all already imposed conditions.

At least one coordinate tends to infinity, because otherwise q=b+sum_v ell(v) would remain bounded. Thus H is nonempty. For v in H,

    w_i(v) >= deg(v)-2 >= ell_i(v)-2 -> infinity.

This is precisely where the degree condition is used. The minus-two endpoint is harmless even when the core is a single vertex. No stronger bound such as w>=deg-1 is assumed.

### 5. The low-sum classification

Let R be b plus the constant leaf counts attached to vertices outside H. After all H vertices are deleted, every leaf attached to H is isolated. All other vertices lie in a universe of at most R vertices. The latter may be disconnected and may include extra excluded core vertices in its counted size, neither of which invalidates the upper bound of 2^R subsets or sums.

Choose a fixed integer M>2^R so large that

    (M^2+1) / 2^(M-2^R) < delta.

Such an M exists because exponential growth dominates a quadratic. Crucially, M is chosen after delta and R are fixed, but before taking a sufficiently late i. Eventually W_i>=M and every H vertex has weight greater than M. Positivity then ensures every connected representative of 1,...,M avoids H; cancellation cannot occur.

At most 2^R different represented values come from the bounded universe. Thus at least t=M-2^R distinct values must each be represented by an isolated leaf attached to H. Choosing one leaf for each such value gives t distinct vertices and total weight U<=Mt<=M^2. The argument does not assume that leaf weights in general are distinct; it deliberately selects leaves realizing distinct values.

### 6. Collision bound and contradiction

For each fixed subset outside the selected t leaves, their contribution is an integer between 0 and U, giving at most U+1 possibilities. Positivity and integrality justify this range bound. Multiplying by the 2^(q-t) outside subsets bounds all subset sums, and therefore also all connected sums. Since the latter contain W distinct positive integers,

    delta <= W/2^q <= (M^2+1)/2^t < delta.

The inclusion of the empty subset in the upper estimate is harmless slack. Every choice and limit has the required order. This proves Theorem 1 without an effective rate; the argument supplies no coefficient-one log-star estimate.

## Polygon dissection and minimizers

A pancyclic graph contains an n-cycle, hence is Hamiltonian and 2-connected. In an outerplane embedding of a 2-connected graph, the outer face has a simple cycle boundary containing all vertices. Thus the graph is an n-gon with k=|E|-n noncrossing interior chords. The argument needs this outer Hamiltonian cycle's existence, not a separate unproved uniqueness assertion.

Adding one chord splits exactly one bounded face. Inductively the weak dual is a tree with q=k+1 vertices. The face boundaries are simple polygons of length at least three. Each chord side is incident with exactly one other bounded face, so deg_T(F)<=|boundary(F)|, giving exactly the required inequality w(F)>=deg_T(F)-2. Counting outer sides once and chord sides twice gives

    sum_F w(F) = n+2k-2(k+1) = n-2.

For any simple graph cycle, its interior consists of bounded faces. Their dual adjacency is connected: a path in the cycle's interior between two face-interior points can avoid vertices and cross only edges interior to the cycle. The induced dual is therefore a subtree, so it has |S|-1 shared edges. In the sum of face perimeters, internal sides are counted twice and the cycle boundary once. The result is L=2+sum_{F in S}w(F).

Only the cycle-to-connected-set direction is needed for the theorem. No assertion that every abstract degree-valid weighted tree is realizable is used. Pancyclicity supplies the values 1,...,n-2, and positivity bounds all other connected sums between 1 and n-2, so interval completeness follows.

For any sequence with graph orders n_i->infinity, Theorem 1 now gives (n_i-2)/2^(k_i+1)->0. Equivalently k_i+1-log_2(n_i-2)->infinity. The difference between this expression and k_i-log_2(n_i) tends to 1, so the claimed divergence is unchanged.

For each integer n>=3 a fan triangulation is pancyclic: its consecutive cycles starting at the fan center have every length 3,...,n. Hence the family defining h_out(n) is nonempty. There are only finitely many simple labelled n-vertex graphs, so the minimum exists. If the asserted limit for these minima failed, one could choose minimizers on an unbounded sequence of orders where the excess gap is bounded, contradicting the result just proved for arbitrary sequences. This establishes the uniform extremal quantifier.

## Star weak duals

For a star with k leaves, q=k+1, and the central weight c satisfies c>=k-2 and c>=1. A connected set is either one leaf, or the center with any leaf subset. Every value below c must therefore be the weight of a singleton leaf. There must be c-1 distinct leaves of weights 1,...,c-1, so c<=k+1. With k>=3, exactly the four candidate values remain.

Their prescribed weights have total S=c(c-1)/2 and leave r=k-c+1 between zero and three free leaves. The collision lemma gives at most (S+1)2^r central sums. There are at most k singleton sums, even if they overlap central sums. Interval completeness then gives n-2<=k+(S+1)2^r. The corrected algebra above completes the upper bound.

For the construction, set c=k-2 and S=(k-3)(k-2)/2, and use leaf weights 1,...,k-3,S+1,2(S+1),4(S+1). There are exactly k leaves, including when k=3 and the initial list is empty. The subset sums of 1,...,k-3 fill 0,...,S by induction on the added consecutive integer; this includes S=0. The last three weights fill the multiples j(S+1), 0<=j<=7. Translating [0,S] by these multiples produces adjacent intervals covering [0,8S+7] without gaps.

Attach one leaf polygon to each of the k sides of a central k-gon, using distinct new vertices. A weight-a leaf adds a vertices and a+1 edges, retaining the old side. The graph is simple, noncrossing, has n=k+sum a and |E|=n+k, and has the intended star weak dual. Choosing the old side or the outer attached path independently on each central side gives simple cycles of lengths k through n. The smaller attached faces give lengths 3 through k-1. At k=3 this latter interval is empty; the central triangle already supplies length 3. Finally n=k+8S+7=4k^2-19k+31.

The lower construction and upper obstruction differ by exactly three vertices at each k>=3. They determine the leading quadratic coefficient in this subclass but do not identify its exact finite extremum.

## Independent supporting finite controls

All controls passed in ordinary Python, Python -O, and Python -OO. The three substantive receipts were byte-identical: 4,625 bytes each, SHA-256 23d20cdcdabd877f3b9effb3b9ded367f55a13ec22924a6cf2e9e998d1df409d. The independent auditor did not execute the candidate checker. During edition preparation both sealed input packages were byte-reauthenticated, without rerunning their mathematical programs.

Coverage included all 1,442 labelled trees of orders 1 through 6; the matching-connected-set bound, nonleaf bound, core connectivity, and leaf attachment at valid endpoints were checked. Weighted-tree checks covered weights 1 through 5 through order 4 and weights 1 through 3 at order 5: 40,780 assignments, 40,375 satisfying the degree constraint, and 14,913 interval-complete degree-valid assignments. All 1,122,150 selected-subset collision inequalities passed. The order-five cases exercise the nontrivial degree-four center condition.

All 5,439 noncrossing polygon dissections of orders 3 through 9 were checked. Face splitting constructed weak duals and weights; an independent cycle-space parity enumeration recovered every simple graph cycle and matched its full length multiset with connected dual sums plus two. Explicit star constructions at every integer k=3,...,11 passed the pancyclicity, excess-k, and 2^k+k simple-cycle-count checks. Exact substitutions and corrected polynomial differences were checked for every integer k=3,...,10,000, including detection of the original internal-candidate endpoint error. The written factorization proves the all-k statement.

Negative controls covered removal of the degree constraint, removal of interval completeness, substitution of arbitrary subset sums for connected sums, loss of integrality in the collision lemma, loops, duplicate edges, and invalid graph endpoints. They demonstrate the role of assumptions and validate rejection paths. They do not replace the universal proof.

No infinite theorem is inferred from these finite samples. The complete written proof and logical audit above establish the universal restricted results; the omitted raw controls are supporting validation only.

## Remaining unrestricted problem

The crossing-chord case has no supplied weak-dual tree representation. Deleting crossing chords need not preserve pancyclicity, and no reduction of unrestricted minimizers to outerplanar minimizers has been proved. A connected graph with n vertices and n+k edges has 2^(k+1)-1 nonzero cycle-space elements, yielding only the standard constant-gap logarithmic cycle-count bound. The missing geometry-imposed degree/weight relation cannot be recovered from that count alone. Neither unrestricted divergence nor the stronger coefficient-one log-star lower bound is accepted as proved.

## Publication and review boundary

This AI-assisted work is unrefereed. Acceptance means an independent internal AI audit of the authored candidate, corrected proof, and separate exact controls. No external human peer review, journal acceptance, or formal proof-assistant certification is claimed. The arithmetic correction concerns an unpublished internal candidate, not a claimed error in published literature.

The complete mathematical proofs and algebraic construction are included. The universal statements rest on those proofs, not on finite enumeration. Raw code, certificates, copied source documents, and private coordination material are not distributed. The omitted finite controls are supporting validation and are not unproved premises of the mathematical results. This edition is a self-contained mathematical proof of the stated restricted results, but is not a computational reproduction package. No novelty, priority, or exhaustive literature-status claim is made. The unrestricted crossing-chord divergence question and the stronger coefficient-one log-star lower bound remain unresolved by this work.

## Sources and historical inspection

- P. Erdős, *Some Unsolved Problems in Graph Theory and Combinatorial Analysis* (1971), Problem 10, printed page 101 / PDF page 5. [Original PDF](https://www.renyi.hu/~p_erdos/1971-25.pdf). The retained source was inspected in text and visually for the title and Problem 10; unrelated problems were not reviewed. It supplies the original unrestricted question whether h(n)-log_2 n tends to infinity, not an explicit statement of the stronger modern log-star lower bound.
- Sean Griffin, *Minimal Pancyclicity*, arXiv:1312.0274v1 (2013). [Abstract](https://arxiv.org/abs/1312.0274), [PDF](https://arxiv.org/pdf/1312.0274). Historical inspection covered the relevant introduction, Claim 1 and its complete lower-bound proof, the binary log-star stopping convention, sections 1.1 and 1.2, and references; PDF page 2 was visually checked. Claim 1 gives the standard lower bound h(n)>=log_2(n-1)-1. The upper construction's full derivation was not used.

These sources provide problem and literature context. They are not external proof dependencies for the weighted-tree lemmas, restricted divergence, star bound, or algebraic construction, all of which are proved here. A bounded earlier search did not establish whether these restricted results were already known. No theorem from an uninspected related paper is invoked. Edition preparation performed no new scholarly-source retrieval, visual inspection, mathematical experiment, or literature search. SOURCES.json records the retained public source identities and the earlier reading scope; historical inspection is not presented as a new inspection.
