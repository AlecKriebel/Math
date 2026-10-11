# Binary-weighted directed-cycle cacti: a certifying halting algorithm

## Status and scope

**Restricted theorem proved; the general Eulerian-multigraph problem is not resolved.**

This note gives a bit-polynomial, indeed strongly polynomial arithmetic, halting algorithm for directed-cycle cacti with independent positive binary-encoded weights on their cycle blocks. It includes every bidirected tree with arbitrary positive, independently chosen binary edge multiplicities. It also includes genuinely directed examples such as directed triangles joined by a weighted bidirected bridge. No uniform global scaling assumption is made.

The result is an authored, self-contained restricted theorem. No priority or literature-novelty claim is made. In particular, the unweighted directed-cactus case is already contained in the coEulerian theory of Farrell–Levine. The present note gives an explicit compressed algorithm and certificates for independently weighted blocks, which generally are not coEulerian. It does not identify fixed-endpoint reachability with halting, and it does not use an expansion of large edge multiplicities.

This AI-assisted work is unrefereed. Acceptance means an independent internal AI audit. No external human peer review, journal acceptance, or formal proof-assistant certification is claimed. The general Eulerian-multigraph target remains unresolved by this work; no novelty, priority, or exhaustive current-literature claim is made.

This edition contains the complete self-contained mathematical proof and full analytical algorithm. It is not a computational reproduction package: executable programs, raw certificate contents, and copied source documents are not distributed. Historical finite checks are supporting validation only; no omitted computational premise is needed for the theorem. Edition preparation made no new mathematical test runs, scholarly-source retrieval, visual source inspection, or literature search.

## 1. Exact class, model, and theorem

A **directed-cycle cactus** is constructed from directed simple cycles of lengths at least two by identifying vertices so that the bipartite incidence graph of cycle blocks and vertices is a tree. Two-vertex cycles consist of the two opposite arcs. Every arc in a block B is given the same positive integer multiplicity w_B; different blocks may have unrelated weights. There are no other arcs. This construction gives a connected, loopless Eulerian directed multigraph.

This is a strict class. For example, a bidirected triangle is not one permitted block, even though its underlying undirected graph is a cactus. The algorithm rejects that graph. The expression “directed-cycle cactus” here always has the stated block meaning.

Input consists of its n by n binary adjacency matrix A, where A_uv counts arcs u to v, and a vector x of nonnegative binary integers. Write

- d_v = sum_u A_vu = sum_u A_uv;
- Delta = diag(d) - A^T;
- a legal firing at v requires x_v >= d_v and replaces x by x - Delta e_v.

We assume n >= 2. Under the literal firing rule, the exceptional one-vertex loopless graph has d=0, and its zero-effect firing is always legal; it never halts. It can be decided separately in constant time.

**Theorem.** On the stated directed-cycle-cactus class, halting can be decided using O(n^2) exact integer arithmetic operations and polynomial intermediate bit length. The algorithm recognizes the class from A and returns independently checkable certificates:

1. If halting, an integer vector y with y_v < d_v and a nonnegative integer vector f such that y = x - Delta f. The vector y may have a negative root coordinate; it is a stabilizing upper-bound certificate, not a claimed reachable endpoint.
2. If nonhalting, a nonnegative vector y = x - Delta f and a legal sequence firing every vertex exactly once and returning to y.

The certificate conditions are exact integer identities and inequalities. A nonhalting certificate additionally includes a sequence whose individual firings and return to its starting configuration can be checked directly. Their validity does not require trusting cactus recognition or elimination. A historical standard-library implementation and separate verifier were used in the supporting controls summarized in Section 8; neither program is distributed here.

## 2. Least action, including signed stable certificates

**Lemma 1.** Let x be nonnegative on a loopless digraph. If f is a nonnegative integer vector and s=x-Delta f satisfies s_v<d_v for every v, then every legal firing sequence from x has firing-count vector at most f coordinatewise. In particular, x halts. No lower bound on s is required.

**Proof.** Suppose a legal sequence first tries to exceed f at vertex v. Just before this firing, its count h satisfies h_v=f_v and h_u<=f_u for all u. Its current number of chips at v is

x_v - d_v h_v + sum_u A_uv h_u
<= x_v - d_v f_v + sum_u A_uv f_u = s_v < d_v.

The proposed firing is illegal, a contradiction. Thus at most sum_v f_v legal firings are possible. A maximal legal sequence therefore ends at a genuinely nonnegative stable state. The certificate s itself need not be that state. ∎

**Lemma 2.** On an Eulerian digraph, two nonnegative integer configurations related by y=x-Delta g for integral g have the same halting status.

**Proof.** Suppose x has a legal terminating sequence with count u and stable endpoint s=x-Delta u. Then s=y-Delta(u-g). Since Delta 1=0, adding a sufficiently large integer multiple of 1 makes u-g nonnegative without changing s. Lemma 1 gives halting of y. Exchange x and y for the reverse implication. If there is any finite terminating legal sequence, Lemma 1 also shows that all legal sequences are finite, so no separate choice-of-order assumption is needed. ∎

## 3. Rooted elimination algorithm

Choose root r=0 in the block incidence tree. Each block B has a unique anchor a_B nearest the root. Rotate its directed cycle to write

(a_B, v_1, ..., v_k, a_B), with common weight w_B.

The v_i are the nonanchor vertices of that block. Each nonroot vertex is a nonanchor in exactly one parent block, although it may anchor several child blocks.

Initialize a working vector b=x. Process blocks from leaves toward the root. At a block B, all descendants of its nonanchor vertices have already been processed. For every v_i set

c_i = d_(v_i) - 1,
z_i = c_i - ((c_i - b_(v_i)) mod w_B),
delta_(B,v_i) = b_(v_i) - z_i.

Here “mod” is the remainder in {0,...,w_B-1}, including for negative inputs. Replace b_(v_i) by z_i and add sum_i delta_(B,v_i) to b_(a_B). Record all deltas. All computations use the integers as encoded, never their expansions.

After all blocks are processed, let y=b. Return HALTS exactly when y_r<d_r.

**Immediate properties.** Each delta is divisible by w_B. Every nonroot vertex v satisfies

 d_v - w_parent(v) <= y_v <= d_v - 1.

Since d_v>=w_parent(v), all nonroot coordinates of y are nonnegative. The root can be negative. Every block operation preserves the total number of chips algebraically.

## 4. Integral Laplacian equivalence

Assign an integer potential F_r=0. Traverse rooted blocks outward. For the block ordered as above, starting with its already assigned F_(a_B), assign

F_(v_i) = F_(v_(i-1)) + delta_(B,v_i)/w_B,

where v_0=a_B. No vertex receives two assignments.

**Lemma 3.** Delta F = x-y.

**Proof.** The Laplacian contribution of block B at nonanchor v_i is w_B(F_(v_i)-F_(v_(i-1)))=delta_(B,v_i). At its anchor it is w_B(F_(a_B)-F_(v_k))=-sum_i delta_(B,v_i).

For a nonroot vertex v, its working value immediately before its parent block is processed equals x_v plus all transfers from its child blocks. Hence its parent-block delta equals x_v-y_v plus those child transfers. In Delta F, the child-block anchor contributions subtract precisely those transfers. The resulting coordinate is x_v-y_v.

At the root, y_r equals x_r plus all child-block transfers, while its total Laplacian contribution is the negative of that sum. The root coordinate is x_r-y_r as well. ∎

Set f=F-(min_v F_v)1. This vector is nonnegative and Delta f=Delta F because the graph is Eulerian. Thus y=x-Delta f is an exact, short integer certificate.

## 5. Decision proof and nonhalting certificate

If y_r<d_r, every coordinate of y is strictly below its firing threshold. Lemma 1, applied to the nonnegative f just constructed, proves that x halts. This argument deliberately permits a negative y_r.

If y_r>=d_r, every coordinate of y is nonnegative. Fire r first. Process the rooted blocks in any parent-before-child order, and within each block fire its nonanchor vertices in directed cycle order. Each vertex is fired once.

When v is considered, its predecessor in its parent cycle has already fired and sent it w_parent(v) chips. Vertex v has not fired yet, and other incoming contributions can only help. Its initial y_v is at least d_v-w_parent(v), so it has at least d_v chips and its firing is legal. The root's firing was legal by assumption. At the end the count vector is 1; Delta 1=0, so the configuration returns to y. This nonempty legal cycle can be repeated indefinitely. Lemma 2 therefore proves that x is nonhalting.

The two cases exhaust all root values, proving the decision theorem. Notice that no possibly enormous path from x to y is computed or assumed legal.

## 6. Bit complexity and recognition

Let N=sum_v x_v and C=sum_v(d_v-1). These values may be numerically exponential in input length, but their bit lengths are polynomial in it.

At every elimination stage, an unfinalized aggregate vertex value is the sum of original chips in a disjoint rooted region minus already fixed stable values in that region. Thus each unfinalized aggregate lies between -C and N. Finalized coordinates separately satisfy 0<=y_v<=d_v-1; they may exceed N. Every stored coordinate lies in [-C,max(N,C)]. Every transfer magnitude is at most N+C. Along a rooted path there are fewer than n potential increments, so |F_v|<=n(N+C), and shifting the minimum preserves a bound 2n(N+C). Consequently all intermediate integers have O(log(n+1)+log(N+C+1)) bits. The same bound, with another O(log(n+1)), covers Laplacian products and verification sums.

Recognition uses biconnected components of the simple underlying undirected support. A two-vertex bridge block must consist of equal positive opposite multiplicities. Every larger block must be a simple undirected cycle whose arcs form exactly one consistently oriented directed cycle of uniform positive weight. Rooting the block incidence tree completes recognition. An iterative Tarjan traversal supplies the biconnected blocks without a recursion-depth limit; the historical implementation used this method.

Reading the adjacency matrix and checking its row and column sums take O(n^2) arithmetic operations. In the recognized class the sum of block sizes is O(n). Block inspection, rooting, elimination, potential construction, and the exact certificate check together use O(n^2) arithmetic operations; the numerical elimination itself uses O(n) arithmetic operations. Integer division/remainder is counted as one arithmetic operation for this strongly polynomial arithmetic claim. Standard exact integer arithmetic makes the resulting bit running time polynomial in the full encoded input length.

No claim is made that individual legal firings can be listed in polynomial time. For example, take vertices 0,1,2 with opposite multiplicity M between 0 and 1, and opposite multiplicity 1 between 1 and 2. Starting at (0,0,M), exactly M successive firings of vertex 2 lead to (0,M,0), which is stable. With M=2^B this legal terminating play has exponential length in B, while the present decision computation remains compressed.

## 7. Why this does not solve the general problem

The proof requires the independent cycle-block potential assignments. It does not extend merely by retaining Eulerian degree balance, global edge gcds, per-vertex residues, or a total-chip threshold.

A precise obstruction is the bidirected triangle with multiplicity q in each direction on each pair of distinct vertices. Its thresholds are (2q,2q,2q). The configurations

x=(2q,q,0), and s=(q,q,q)

have the same total 3q and the same coordinate residues modulo q. The configuration s is stable. The legal order (0,1,2) returns x to itself:

(2q,q,0) -> (0,2q,q) -> (q,0,2q) -> (2q,q,0).

Thus x is nonhalting. Already for q=1, the vector x-s=(1,0,-1) is not in the triangle's Laplacian lattice: for its unit-weight Laplacian, every image vector has all coordinates congruent modulo 3. This explains the lost global lattice obstruction when a whole bidirected block is wrongly treated as a unit-weight directed cycle. Taking q=2^B gives the same obstruction with binary-large multiplicities.

The algorithm explicitly rejects this input class. The example disproves the indicated residue/total shortcut, not every conceivable extension of the algorithm. In particular, it provides neither hardness nor a general polynomial-time algorithm for arbitrary Eulerian multigraphs.

## 8. Historical supporting verification

The historical candidate controls compared its solver and certificates with independently generated, complete finite state spaces for 177 small weighted cactus graphs: 1,208 fixed-total state spaces and 53,422 initial configurations (15,693 halting; 37,729 nonhalting). This included 3,328 accepted halting certificates whose canonical root was negative, specifically guarding the signed-certificate distinction. They also checked 96 root/label permutations, five large-binary inputs with integers up to 8,193 bits, 15 rejecting input/certificate mutations, the excluded triangle recurrence, and the exponential-length terminating-play family.

Those finite-state controls did not use the elimination recurrence and had no arbitrary simulation cutoff. Their first-active legal transition system was exhaustively classified by exact repeated-state detection. The standalone mathematical proof above, not these finite controls, supplies the universal claim.

Recorded normal, -O, and -OO candidate runs passed with the same exhaustive outcome digest:

    5c7dd9cb8e45f2ab3650b67b58563bfc6642fb856389b7449cc6a585ef65e5b0

The independent audit used a distinct all-legal-transition finite-state oracle and independently written normalization, lattice, certificate, and recognition checks. It reproduced the same graph, state-space, configuration, halting, nonhalting, and signed-root counts. Its 71,257 legal transitions, 359 reduced-Laplacian checks, 4,841 complete small-matrix recognition comparisons, and further controls are described in AUDIT.md and VERIFICATION.json. Its separate exact and recognition outcome digests were respectively ad1748d7b9a105d30bbb312d2efe349b06615df39451be1cf7ce277b63b8035f and 11fb751272b6184cb630b7414ed1d90d8d392b5889151b85983d387fceb712ef. Distinct serialization explains the different candidate and audit digests; the shared coverage and outcome totals agree.

The audit read the candidate's implementation statically and did not execute or import it. Its historical independent checks used explicit exceptions, with agreement in normal, -O, and -OO modes. No candidate or audit mathematical program was executed during this edition's preparation. The omitted programs and raw certificates are not premises of the complete written proof.

## 9. Source context and limits

The exact broad question is Problem 22 in Hujter–Kiss–Tóthmérész, while their Theorem 11 concerns prescribed-endpoint reachability. Their Proposition 21 gives the co-NP certificate side; the source also records NP membership. These results do not themselves compute the required endpoint. The 1992 simple-Eulerian firing bound depends numerically on edge multiplicities before the simple-graph restriction. Farrell–Levine's coEulerian theorem is a different class.

Relevant public sources:

1. Bálint Hujter, Viktor Kiss, Lilla Tóthmérész, *On the complexity of the chip-firing reachability problem*, arXiv:1507.03209v4, 2016; published in Proc. Amer. Math. Soc. 145 (2017), 3343–3356. https://arxiv.org/abs/1507.03209
2. Anders Björner, László Lovász, *Chip-firing games on directed graphs*, J. Algebraic Combin. 1 (1992), 305–328. Retained author manuscript: http://www.cs.elte.hu/~lovasz/morepapers/abacus.pdf
3. Matthew Farrell, Lionel Levine, *CoEulerian graphs*, arXiv:1502.04690v3, 2015; published in Proc. Amer. Math. Soc. 144 (2016), 2847–2860. https://arxiv.org/abs/1502.04690
4. EGRES Open, *Complexity of the halting problem for Eulerian multigraphs*, retained revision 2388. https://oldlemon.cs.elte.hu/egres/open/Complexity_of_the_halting_problem_for_Eulerian_multigraphs

This work does not certify that no later paper contains this restricted algorithm or resolves the broad question. Its acceptance claim is confined to the self-contained restricted theorem; historical exact controls provide supporting validation only. SOURCES.json records source identities and the limited historical reading and visual inspection.
