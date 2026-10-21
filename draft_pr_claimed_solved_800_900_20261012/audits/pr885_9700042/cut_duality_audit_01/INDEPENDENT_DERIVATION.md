# Independent finite directed-cut derivation

Timestamp: 2026-10-15T13:53:55Z. This derivation was written after the frozen primary contract and candidate C1/C4, but before any earlier audit or author clarification.

## 1. Precise primal/dual dictionary

Use the SOURCE_CONTRACT model. Set N=n-2. A bounded face with primal lower-left corner (i,j) is represented by dual vertex (i,N-j), so Q_N={0,...,N}^2. A dual east step from (x,y) crosses the primal north edge ((x+1,N-y),(x+1,N-y+1)); a dual north step crosses the primal east edge ((x,N-y),(x+1,N-y)). Its cost is the capacity of that edge. A reverse dual step has cost zero. These crossing primal edges are precisely the edges interior to the boundary of the square. The remaining boundary edges cannot be bichromatic in an allowed cut, except

e_L=((0,n-2),(0,n-1)), e_B=((n-2,0),(n-1,0)).

Both forced edges point from S to T. Their capacities contribute separately. For n=2 there is one bounded face, N=0, no interior dual edge, and the identity below reduces to V_2=c_L+c_B.

## 2. Every directed cut supplies the requisite dual path

Color an arbitrary allowed cut side A as source-colored, its complement as sink-colored. Thus S subset A and A intersect T is empty; interior colors can be arbitrary. Draw the dual crossing of every bichromatic primal edge. Add an external start stub crossing e_L into face (0,0) and an external end stub crossing e_B out of face (N,N). Orient each drawn arc with the source-colored primal endpoint on its right, in the physical (unreflected) embedding.

At each bounded face, clockwise traversal of its four primal vertices changes colors as often from source to sink as from sink to source. Equivalently, directed interface indegree equals outdegree. Degree four causes no obstruction: it has two incoming and two outgoing arcs. One may choose either unused outgoing continuation on entering; no fixed crossing or smoothing convention is needed for reachability. The external start has outdegree minus indegree one; the external end has indegree minus outdegree one. There are no other external arcs because the prescribed boundary colors change only twice.

The end is reachable from the start. Otherwise the set of vertices reachable from the start would have no outward arc, whereas the sum of outdegree minus indegree over that set is +1; summing arc incidences would then give a nonpositive number. Choose a directed start-to-end walk, remove loops, and delete its stubs. This produces a simple dual corner path. Its forward dual arcs cross outward primal edges, while its backward arcs cross inward primal edges. Its cost plus c_L+c_B is at most the total directed cut capacity, because it uses a subset of the cut's outward edges exactly once, and capacities are nonnegative. Disconnected islands, holes, and additional contours add no negative capacity and do not invalidate this argument.

## 3. Every simple dual path supplies an allowed cut

Embed Q_N inside the primal square and append the e_L/e_B half-edge stubs. A simple corner-to-corner dual path, including these stubs, is a simple arc with distinct endpoints on the square boundary and otherwise lies in the square's interior. Complete it by the boundary arc adjacent to S. The Jordan separation theorem gives a source side containing all S and no T. The path crosses primal edges transversely at their midpoints, never primal vertices. Thus the only bichromatic primal edges are its crossings and the two stubs. The outward ones are exactly the forward dual crossings and e_L,e_B. The corresponding directed cut has capacity c_L+c_B+cost(P).

Nonnegative dual costs permit removing any repeated-vertex cycle without increasing cost, so a minimizing walk can be chosen simple. Integral max-flow/min-cut (auxiliary S/T arcs may have capacity larger than the total number of primal edges) therefore gives the exact identity

V_n = c_L+c_B+T_N,

where T_N is the least dual corner-path cost. Neither inequality restricted arbitrary primal cuts to a monotone class.

## 4. Reward and cycle bookkeeping

For a corner path P, let b be its total west/south steps, f its east/north steps, and k the number of its marked forward traversals. Net coordinate displacement gives f-b=2N. Hence cost(P)=f-k=2N+b-k and

D_N=2N-T_N=max_P(k-b),  (2n-2)-V_n=2-c_L-c_B+D_N.

Every closed dual walk has equal forward and backward counts, while k cannot exceed its forward count. Its reward k-b is at most zero. Deleting cycles cannot lower reward. In particular a maximizer can be simple, its marked edges are distinct, and 0<=D_N<=2N. The upper bound is also immediate from nonnegative minimum cost. A monotone path supplies nonnegative reward. These arguments also apply inside any translated rectangle, with 2N replaced by the sum of its side lengths.

## 5. The marked-list prerequisite

Choose any simple nonnegative-reward path. Then b<=k. Mark the starting vertex of each of its k distinct marked forward edges, in path order; append both corner vertices. Negative variation in either marked-coordinate subsequence is at most b: deleting intermediate terms cannot increase total negative variation, by max(a-c,0)<=max(a-b,0)+max(b-c,0). For each coordinate the number of admissible lists is bounded by the C1 stars-and-bars quantity

A(N,k)<=sum(t=0..k) C(k+1,t) C(k,t) C(N+2k-t,k-t).

Indeed t strictly negative increments have chosen positions and positive magnitudes whose sum is at most k. The other increments are nonnegative with total N+B. Once all increments are specified the coordinate list is unique; dropping the box constraint only enlarges the count. There cannot be k+1 negative increments because the endpoint displacement is N>=0. The ratio of the last binomial to C(N+2k,k) is (k)_t/(N+2k)_t <= [k/(N+2k)]^t. Keeping the equal-index terms inside the product of two binomial expansions gives

A(N,k)<=C(N+2k,k)(1+sqrt(k/(N+2k)))^(2k+1).

Each ordered edge list is fixed by two coordinate lists and k orientation bits. No injectivity of full paths into lists is needed: many paths can share one list because the union bound concerns existence of a closed list. Invalid or repeated-edge lists must be discarded before assigning probability q^k; the candidate explicitly does this. A genuine simple path always supplies an admissible distinct-edge list. This proves the bound for K_N^+, not merely for D_N. The case k=0 needs no probability-tail use; k>=1 suffices in C4.

## 6. Completion used in C4

For a segment with backward count b_j and coarse allowance a_j=(floor(b_j/h)+1)h, each coordinate stays between its starting coordinate minus b_j and ending coordinate plus b_j. The stated rectangle therefore contains the entire segment, and its lower corner is coordinatewise below the segment start while its upper corner is above the end. Both monotone padding walks exist on the integer lattice. The resulting walk may touch or overlap itself; cycle deletion is legitimate by the reward argument above, and cannot reduce reward. Its original marked forward edges are sufficient positive witnesses under every assignment to other edge states. If a segment has negative reward, threshold zero has the empty witness. Simplicity of the original global path makes the original marked witness sets pairwise disjoint; padding is used for existence, not as additional required marks.

The rectangle width-plus-height is exactly tau_j+2h+4a_j. For each nonlast bad segment (b_j>=h), its contribution is at most (m+10)b_j. The last segment contributes at most L+6h+4b_last. Adding gives the candidate bound (m+10)B_N+L+6h, because m+10>=4. The last segment requires no unstated lower bound on tau_j.

For sparse finite rectangles, a global mark count Z<=M and pairwise marked starting-coordinate gaps greater than M force the ordered marked starts of every nonnegative-reward simple path to increase strictly in both coordinates: a decrease would require more than M backward steps. Conversely such a chain can be connected monotonically through the actual marked edges because every relevant coordinate gap exceeds 1. No orientation is lost on this event. This is a valid deterministic stability claim, not an assertion that all sparse configurations have the property.

## 7. Exact connection to the asymptotic target

The identity and 0<=c_L,c_B<=1 give

E[D_N]/(2N) -> 1-v(1-q)

for each fixed q, using only the source-stated L1 convergence and n=N+2. Boundary contributions vanish as N grows. The finite geometry alone does not control q -> 0. C1's counting argument gives only its stated e/2 normalized upper bound. C4 additionally needs its verified external Poisson estimates, finite-scale convergence with moments, BK product control, skeleton entropy, and the stated order of parameters to produce the sharp upper bound. This audit does not replace those probability checks with finite tests.

The lower-bound concatenation is deterministic: embed successive side-ell dual squares diagonally. Their vertex sets intersect only at the concatenation corners and their edge sets are disjoint; concatenated maximizing simple paths form a simple large-square path. Thus D_{k ell}>=sum D_ell^(j), pathwise. Expectations and the fixed-q limit give g(q)>=E[D_ell]/(2ell). No independence is necessary for this expectation inequality, although disjoint edges also give independence under the model.
