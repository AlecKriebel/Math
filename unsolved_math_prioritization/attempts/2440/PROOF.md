# Outerplanar pancyclic excess diverges beyond the logarithm

## Status and scope

This is a corrected, independently internally audited restricted-class result for EP 1016 / 2440. It does not settle either the original unrestricted divergence question or the stronger coefficient-one iterated-logarithm lower bound. The principal result is

    h_out(n) - log_2 n -> infinity as n -> infinity.

The complete proof is self-contained. A separate star-weak-dual argument gives an order bound within three vertices of an explicit quadratic construction for every integer k>=3. The local arithmetic correction changes an intermediate substitution in the unpublished internal candidate from k^2+6 to k^2+4, with corrected polynomial differences and the k=3 endpoint; it changes neither final theorem nor any hypothesis. AUDIT.md explains the repair.

A graph is simple and undirected. Pancyclic means that, on n vertices, it contains a simple cycle of every length 3,4,...,n. Its excess is k=|E|-n. Let h(n) be the minimum excess over all such graphs, and let h_out(n) be the minimum over the outerplanar ones. These are different extremal functions. An upper or lower statement about h_out does not automatically transfer to h.

Use log*=min{j>=0: log_2 iterated j times on x is <2}; this is Griffin's stopping convention. The original 1971 question explicitly asks whether h(n)-log_2 n tends to infinity. It does not explicitly state the modern quantified lower bound h(n)>=log_2 n+log* n-O(1). Neither unrestricted assertion is proved here.

## 1. Weighted trees

A weighted tree consists of a finite nonempty tree T with q vertices and positive integer vertex weights w(v). Write

    W = sum_v w(v),
    S(T,w) = {sum_{v in A} w(v): A is nonempty and T[A] is connected}.

Call it interval-complete if S(T,w)={1,2,...,W}. All its connected sums are automatically between 1 and W.

### Theorem 1 (degree-constrained weighted trees)

For every sequence of interval-complete weighted trees (T_i,w_i) with W_i tending to infinity and

    w_i(v) >= deg_{T_i}(v)-2  for every vertex v,

one has W_i/2^{q_i} tending to zero.

The positivity and integrality of the weights, interval completeness, and degree constraint are all hypotheses. The conclusion need not hold when one of the latter two conditions is dropped; supporting negative controls are summarized in AUDIT.md.

### Lemma 1 (connected-set count)

Let B(T) be the number of nonempty connected vertex subsets of a tree on q vertices, and let r be its maximum matching size. Then

    B(T) <= 3^r 2^{q-2r} + q 2^{floor(q/2)}.

Proof. Choose a centroid c, so that every component of T-c has at most floor(q/2) vertices. Such a vertex exists: starting at any vertex, move into a component of size greater than q/2 if there is one. The size of the component behind the move is less than q/2, so this procedure cannot return across that edge and must stop.

The connected subsets avoiding c lie in individual components of T-c. Their number is at most q 2^{floor(q/2)} (a deliberately loose bound).

Root T at c and fix a matching of size r. A connected subset containing c cannot contain the child endpoint of a matching edge without its parent endpoint. Thus, on each of the r pairwise disjoint matched pairs, at most three of the four membership patterns are possible. There are at most 3^r 2^{q-2r} subsets satisfying these conditions, even before imposing the other connectivity conditions or insisting that c is present. Summing the two bounds proves the lemma. QED.

### Lemma 2 (bounded matching gives a bounded nonleaf core)

For a tree on at least three vertices, the number b of vertices of degree at least two is at most 4r-1, where r is the maximum matching size.

Proof. The endpoints C of a maximum matching form a vertex cover: an edge outside C could be added to the matching. Put a=|C|=2r and O=V(T)\C. The set O is independent. If t vertices in O have degree at least two, then the number of edges incident to O is at least |O|+t. Since the whole tree has |O|+a-1 edges, t<=a-1. At most a additional nonleaf vertices belong to C. Thus b<=2a-1=4r-1. QED.

### Lemma 3 (a small-weight subset forces collisions)

For any q positive integer weights, if t of them have sum U, the number of distinct sums of arbitrary subsets of all q weights is at most

    (U+1) 2^{q-t}.

Proof. First specify the subset of the other q-t weights. The selected t weights can contribute only an integer between 0 and U. There are at most U+1 possibilities. Collisions between different outside subsets only reduce the total. QED.

### Proof of Theorem 1

Suppose instead that a sequence with W_i tending to infinity has W_i/2^{q_i}>=delta for a fixed delta>0. Interval completeness implies W_i<=B(T_i)<=2^{q_i}-1, so q_i tends to infinity.

By Lemma 1,

    delta <= (3/4)^{r_i} + q_i 2^{-ceil(q_i/2)}.

The second term tends to zero. Hence the matching sizes r_i are bounded, and by Lemma 2 the nonleaf-core sizes b_i are bounded. Pass to an infinite subsequence with b_i=b fixed, and label the b core vertices. (For large i, q_i>=3 and b>=1.) The induced subgraph on the nonleaves is connected: every internal vertex of a path between two nonleaves is itself a nonleaf. Thus every other vertex is a leaf adjacent to a core vertex.

For each labelled core vertex v, let ell_i(v) be its number of leaf neighbors. Repeatedly pass to subsequences so that, for every v, either ell_i(v) is a fixed finite integer or ell_i(v) tends to infinity. This is possible for any sequence of nonnegative integers: either some value occurs infinitely often, or a subsequence tends to infinity. There are only b coordinates.

Let H be the set of core vertices in the second category. It is nonempty because q_i tends to infinity. At each v in H, the degree constraint gives

    w_i(v) >= deg(v)-2 >= ell_i(v)-2 -> infinity.

Let R be b plus the sum of the fixed leaf-neighbor counts at the other core vertices. This is a fixed finite integer. Excluding all vertices in H leaves two types of connected vertex subsets:

1. single leaves formerly adjacent to H;
2. subsets of the at most R vertices consisting of the core and the leaves adjacent to core vertices outside H.

Including H in this count of R vertices is harmless; those vertices themselves are excluded from the subsets being counted. In particular, type 2 yields at most 2^R different sums.

Choose a fixed integer M>2^R so large that

    (M^2+1) / 2^{M-2^R} < delta.

For sufficiently large i, W_i>=M and every vertex in H has weight greater than M. Therefore the connected sets representing 1,...,M avoid H. At most 2^R of these different values can come from type 2. Consequently at least t=M-2^R different values in {1,...,M} occur as weights of individual leaves adjacent to H. Select one leaf for each of t such values. Their total weight U is at most Mt<=M^2.

By Lemma 3, all subset sums, and hence all connected sums, take at most (M^2+1)2^{q_i-t} different values. Since the latter include W_i different positive integers,

    delta <= W_i/2^{q_i} <= (M^2+1)/2^t < delta,

a contradiction. QED.

This proof gives qualitative divergence only. The subsequence step is not a claimed effective log* estimate.

## 2. Outerplanar pancyclic graphs

### Lemma 4 (polygon dissection model)

Let G be a cycle on n vertices with k pairwise noncrossing chords drawn inside it. Its bounded faces have a weak dual tree T with q=k+1 vertices. Give each face F weight w(F)=|boundary(F)|-2. Then

    w(F)>=1,   w(F)>=deg_T(F)-2,   sum_F w(F)=n-2.

Every simple cycle of length L gives a connected vertex subset of T whose total weight is L-2.

Proof. Adding a noncrossing chord splits one face into two. Inductively there are k+1 bounded faces and their adjacency graph across chords is a tree. Every face boundary is a simple polygon with at least three sides, and each adjacent face uses one of its sides, proving the first two inequalities. Counting boundary-edge incidences gives sum_F |boundary(F)|=n+2k, hence the total weight is n+2k-2(k+1)=n-2.

The faces inside any simple cycle form a connected set in the weak dual: its interior is a disk partitioned by chords, and two face interiors can be joined inside that disk by a curve avoiding all vertices and crossing edges transversely. If S is the set of those faces, its induced dual is a tree and has |S|-1 internal shared edges. Thus

    L = sum_{F in S} |boundary(F)| - 2(|S|-1)
      = 2 + sum_{F in S} w(F).

No sufficiency assertion about arbitrary abstract weighted trees being realizable is needed. QED.

An outerplanar Hamiltonian graph has precisely this form in an outerplane embedding: its Hamiltonian cycle is the outer polygon. Indeed the graph is 2-connected, so the outer-face boundary is a simple cycle containing every vertex; all remaining edges are noncrossing chords. The elementary plane-graph fact used here is that a repeated vertex on a face-boundary walk separates incident blocks and is a cut vertex, which 2-connectivity excludes. Equivalently, the result may be read directly for Hamiltonian graphs admitting a chord drawing with no crossing pairs.

### Corollary 1 (restricted divergence)

    h_out(n) - log_2 n -> infinity as n -> infinity.

Proof. For any sequence of outerplanar pancyclic graphs, Lemma 4 gives interval-complete weighted trees with W=n-2 and q=k+1 satisfying Theorem 1. Hence

    (n-2)/2^{k+1} -> 0.

Taking base-2 logarithms gives k+1-log_2(n-2)->infinity, equivalently k-log_2 n->infinity. The restricted minimum exists for every n>=3: a polygon labelled 0,...,n-1 with all fan chords from 0 has the cycles 0,1,...,L-1,0 for every 3<=L<=n. Applying the result to minimizers proves the claim. QED.

## 3. A sharper obstruction and construction for star weak duals

The following calculation isolates the simple independent-shortcut construction: a central polygon with one polygon attached along each selected boundary edge. Its weak dual is a star. This is a subclass of the preceding theorem.

### Proposition 1 (quadratic upper bound on order)

If a pancyclic graph with k>=3 excess edges has star weak dual, then

    n <= 4k^2 - 19k + 34.

Proof. The dual has one central weight c and k leaf weights a_1,...,a_k. Since the center has degree k, c>=k-2. The connected sums are the singleton leaf weights and c plus arbitrary subset sums of the leaf weights. To represent 1,...,c-1, there must be c-1 distinct leaves with exactly those weights. Thus c<=k+1. Fix these leaves. Their total is S=c(c-1)/2; there remain r=k-c+1 leaves, with 0<=r<=3. By Lemma 3 applied to the leaves, the number of central sums is at most (S+1)2^r. Adding at most k singleton-leaf sums gives

    n-2 <= k + (c(c-1)/2+1)2^{k-c+1}.

For c=k-2,k-1,k,k+1, the four resulting upper bounds on n are respectively

    4k^2-19k+34,  2k^2-5k+10,  k^2+4,  (k^2+3k+6)/2.

For every integer k>=3 they are in nonincreasing order: the first successive difference is 2(k-3)(k-4), the second is (k-2)(k-3), and the third is (k-1)(k-2)/2>0. The first difference is zero for k=3,4 and nonnegative thereafter. At k=3 the four bounds are 13,13,13,12. Thus the first bound is the maximum for every k>=3. QED.

### Proposition 2 (matching quadratic construction up to three vertices)

For every integer k>=3 there is an outerplanar pancyclic graph with k excess edges and

    n = 4k^2 - 19k + 31.

Proof. Put c=k-2 and S=(k-3)(k-2)/2. Use a central k-gon and attach a polygon along each of its k edges. Choose the k leaf weights to be

    1,2,...,k-3, S+1, 2(S+1), 4(S+1),

where the initial list is empty for k=3. A leaf of weight a means replacing that edge on the outer boundary by a path of a+1 edges while retaining the original central edge. This adds exactly a vertices and a+1 edges. The resulting graph is simple, outerplanar, has n=k+sum a vertices and exactly n+k edges.

The first k-3 weights have all subset sums from 0 through S. The last three weights have subset sums j(S+1), j=0,...,7. Together, all leaf subset sums fill 0,...,8S+7. Choosing, for each central side, its original edge or its attached outer path gives simple cycles of every length k,...,k+8S+7=n. The attached faces of weights 1,...,k-3 supply lengths 3,...,k-1. Thus the graph is pancyclic. Finally n=k+8S+7=4k^2-19k+31. QED.

These two propositions determine the leading constant 4 for the maximum order in this subclass, without identifying its exact finite extremum. The construction is a proof/check device here, not a claimed improvement over known unrestricted constructions or a claim of novelty.

## 4. Why the unrestricted problem remains

The weak-dual tree proof requires one noncrossing polygon dissection. A Hamiltonian graph with crossing chords need not have this representation. Selecting a noncrossing subset discards chords and can destroy pancyclicity, so the restricted theorem cannot be applied after such a deletion.

Nor does a raw cycle-space bound establish the result. For any connected graph with n+k edges the cycle space has 2^{k+1} elements, giving only the familiar constant-gap logarithmic bound. The proof above needs the geometry-imposed relation between a face's weight and dual degree, and the entire initial interval of attainable lengths. It is not valid for arbitrary weighted subset sums or arbitrary graphs.

The precise remaining task is to handle unrestricted Hamiltonian chord systems well enough to prove either (a) h(n)-log_2 n->infinity, or (b) the stronger h(n)>=log_2 n+log* n-O(1). No such argument is supplied. No general asymptotic lower bound beyond the known cycle-count bound is claimed.

## 5. Supporting finite verification

The separately authored exact checkers exercised the graph/dual correspondence, matching and collision inequalities, explicit constructions, endpoints, and malformed inputs. The independent checks passed in normal, -O, and -OO modes with byte-identical substantive receipts. Their aggregate coverage and evidence identities appear in VERIFICATION.json. The independent auditor derived the checker from the mathematical definitions without reusing or executing candidate code. Those checks support the definitions and implementation; the complete universal proof above does not depend on the omitted code or certificate contents.

## Publication and review boundary

This AI-assisted work is unrefereed. Acceptance means an independent internal AI audit of the authored candidate, corrected proof, and separate exact controls. No external human peer review, journal acceptance, or formal proof-assistant certification is claimed. The arithmetic correction concerns an unpublished internal candidate, not a claimed error in published literature.

The complete mathematical proofs and algebraic construction are included. The universal statements rest on those proofs, not on finite enumeration. Raw code, certificates, copied source documents, and private coordination material are not distributed. The omitted finite controls are supporting validation and are not unproved premises of the mathematical results. This edition is a self-contained mathematical proof of the stated restricted results, but is not a computational reproduction package. No novelty, priority, or exhaustive literature-status claim is made. The unrestricted crossing-chord divergence question and the stronger coefficient-one log-star lower bound remain unresolved by this work.

## Sources and historical inspection

- P. Erdős, *Some Unsolved Problems in Graph Theory and Combinatorial Analysis* (1971), Problem 10, printed page 101 / PDF page 5. [Original PDF](https://www.renyi.hu/~p_erdos/1971-25.pdf). The retained source was inspected in text and visually for the title and Problem 10; unrelated problems were not reviewed. It supplies the original unrestricted question whether h(n)-log_2 n tends to infinity, not an explicit statement of the stronger modern log-star lower bound.
- Sean Griffin, *Minimal Pancyclicity*, arXiv:1312.0274v1 (2013). [Abstract](https://arxiv.org/abs/1312.0274), [PDF](https://arxiv.org/pdf/1312.0274). Historical inspection covered the relevant introduction, Claim 1 and its complete lower-bound proof, the binary log-star stopping convention, sections 1.1 and 1.2, and references; PDF page 2 was visually checked. Claim 1 gives the standard lower bound h(n)>=log_2(n-1)-1. The upper construction's full derivation was not used.

These sources provide problem and literature context. They are not external proof dependencies for the weighted-tree lemmas, restricted divergence, star bound, or algebraic construction, all of which are proved here. A bounded earlier search did not establish whether these restricted results were already known. No theorem from an uninspected related paper is invoked. Edition preparation performed no new scholarly-source retrieval, visual inspection, mathematical experiment, or literature search. SOURCES.json records the retained public source identities and the earlier reading scope; historical inspection is not presented as a new inspection.
