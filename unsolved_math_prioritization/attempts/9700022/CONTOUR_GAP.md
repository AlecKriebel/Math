# Exact contour formulation and the remaining gap

**Review status.** Accepted as rigorous partial results by the accompanying independent AI-assisted mathematical audit. Finite-time hegemony remains OPEN. This manuscript and audit are unrefereed; no external human peer review, journal acceptance, or formal proof-assistant certification is claimed. No novelty or bibliographic priority is claimed.

## 1. Suppressed mergers: an exact finite-state identity

Fix a finite initial cell-adjacency graph G and a nonempty set F of its original edges. Let S_F consist of connected partitions in which the endpoints of every edge of F remain in distinct blocks. For pi in S_F, let

k_F(pi) = #{unordered current block pairs {A,B}: some edge of F joins A to B}.

This counts **distinct current pairs**, rather than original edges or appearances in a contour list. Let Q^F be the generator that performs every unit-pair merger except those k_F(pi) forbidden pairs. Let Y be the resulting suppressed process, initially at singleton cells. It never leaves S_F.

### Proposition 6 (killed-generator identity)

For any bounded function g on S_F, the original unit-pair chain X satisfies

E[g(X_t) 1{all F edges still separate at t}]
= E^F[g(Y_t) exp(−integral_0^t k_F(Y_s) ds)].

### Proof

Because mergers are irreversible, the event on the left is equivalent to not yet leaving S_F. The generator of the chain killed on departure from S_F has all allowed off-diagonal rates equal to those of Q^F. Its diagonal has an additional negative k_F(pi), the total forbidden-merger rate. It is therefore Q^F − diag(k_F). The finite-state Feynman–Kac formula gives the asserted identity. Equivalently, condition on the suppressed path and retain it until an independent exponential killing clock accumulates integrated rate k_F. QED.

For g = 1 this also gives the coarse bounds

exp(−|F|t) <= P(all F edges survive to t) <= exp(−t),

since 1 <= k_F <= |F|. These inequalities are far too weak for the desired contour sum. In particular the independent-boundary expression exp(−|F|t) is a **lower**, not an established upper, bound for the survival event. One must not substitute it as a Peierls upper bound.

The exact finite-state statement is sufficient for the algebra and the computational checks here. An infinite-volume version requires a well-defined suppressed process or a justified limiting argument; no such justification beyond the local construction interval is silently assumed.

## 2. Applying the identity to a hexagonal circuit

Take the initial tessellation to be regular hexagons of side length 1. Let C be a simple circuit of initial tessellation edges enclosing a point b in the interior of an initial cell. Choose a finite cell domain large enough to include all cells on and inside C and the exterior cells meeting C. Let F be the dual initial adjacency edges crossed by C.

The suppressed chain never merges a region inside C with a region outside C. Its two side processes have independent unit-pair dynamics. For a suppressed state pi, write I(pi) for the number of distinct exterior regions incident to C, and J(pi) for the number of distinct interior regions incident to C. Let H(pi) be the bipartite simple graph with these regions as vertices and with an edge for each distinct interior/exterior current pair represented along C. Then k_C(pi) is exactly |E(H(pi))|.

Define g_C(pi) to be 1 if the region containing b includes every initial cell incident to the interior side of C, and 0 otherwise. Under suppression, g_C = 1 is precisely the event that the b-region has C as its **outer** boundary. The region may have holes. It cannot escape the disk without crossing a forbidden edge, and, since it is connected and contains every inner boundary cell, C is its outer boundary. Proposition 6 consequently expresses the probability of this outer-boundary event exactly as

p_C(t) = E^C[g_C(Y_t) exp(−integral_0^t |E(H(Y_s))| ds)].

Using the outer boundary is essential: the boundary of a finite empire need not be one circuit if the empire has holes. A contour proof for finite empires must account for those holes or formulate its event with the outer boundary as above.

### Proposition 7 (a valid planar incidence bound)

For a simple circuit C in the hexagonal tessellation, H(pi) is connected in every suppressed state. Hence

k_C(pi) >= I(pi) + J(pi) − 1.

### Proof

Traverse C one initial edge at a time. At each vertex there are only three initial cells. For the two C-edges incident to that vertex, at least one of their interior and exterior cell labels is the same; after mergers that common label remains the same current region. Thus successive edges of the bipartite incidence graph share a vertex. The cyclic list visits every edge of H and every incident region. The graph is connected, and every finite connected graph on I + J vertices has at least I + J − 1 edges. QED.

This yields the valid finite-volume bound

p_C(t) <= exp(t) E_inside[g_C(Y_t) exp(−integral_0^t J(Y_s) ds)]
                    E_outside[exp(−integral_0^t I(Y_s) ds)].

The factorization uses the independence of the two suppressed side processes; g_C depends only on the inside. This is an exact reduction followed by a proved inequality, but no contour-length-uniform summable bound for these expectations has been established. The side-count processes generally are not the linear-rate pure-death chains in the source heuristic. Regions meeting nonconsecutively can be adjacent through paths away from C, and distinctness/adjacency changes are not encoded by the counts alone.

## 3. An initial repeated-label witness

Represent the centers of the regular hexagonal cells by axial coordinates (q,r) with neighbor differences

(1,0), (0,1), (−1,1), (−1,0), (0,−1), (1,−1).

Let S = {(0,0),(1,0),(2,0)}. These are three collinear hexagons. Their union is a simply connected polyhex, and its outer boundary C is a simple circuit.

There are 3*6 − 2*2 = 14 boundary edges: two shared sides are internal. Thus 2n = 14 and n = 7. The distinct interior regions touching C at time zero are exactly the three cells of S, so J_0 = 3. The distinct exterior neighbors are

(−1,0), (−1,1), (0,−1), (0,1), (1,−1),
(1,1), (2,−1), (2,1), (3,−1), (3,0),

so I_0 = 10 = n + 3. The middle hexagon occurs on two disconnected arcs of C, whereas the two end hexagons each occur on one arc. Counting *interior occurrences* gives 4 = n − 3; counting distinct current interior regions gives 3.

Accordingly, the simultaneous claims that J counts distinct regions and that J_0 = n − 3 for every circuit cannot both hold. If J counts occurrences instead, it does not decrease according to a rate-J, unit-step death chain after a merger involving repeated labels. This is already a witness at time zero to the source's explicitly stated assumption (a) in section 3.1. It does not refute the hegemony conjecture.

The recorded author and independent checks verified the coordinate/edge enumeration using exact arithmetic, without floating-point geometry. Programs and raw outputs are not distributed in this proof-only edition; the explicit analytic witness above is retained in full.

## 4. A time-scale correction to source equation (9)

This is a correction to the **idealized chain**, independently of whether it models the geometry.

Let (I,J) start at (a,b), write N = a+b, and use the source's fictitious nonnegative-state transition rates:

(i,j) -> (i−1,j) at rate i;
(i,j) -> (i,j−1) at rate j;
(i,j) -> cemetery at rate i+j.

Let (I*,J*) have the same death rates i,j but no killing. For these definitions the correct equality is

P(I_t=i,J_t=j, alive) = 2^(i+j−N) P(I*_(2t)=i,J*_(2t)=j).

The source's displayed equation (9), with t on the right instead of 2t, is not correct literally. This can already be seen in the initial state: the two sides as printed are exp(−2Nt) and exp(−Nt).

### Proof of the corrected identity

Give each of N labeled tokens independent rate-1 removal and rate-1 killing clocks. A killing clock that rings before its token's removal sends the entire process to the cemetery. A token remains at t with probability u = exp(−2t), and is removed without killing by t with probability (1−u)/2. Therefore

P(I_t=i,J_t=j, alive)
= binom(a,i) binom(b,j) u^(i+j) [(1−u)/2]^(N−i−j),

which is exactly 2^(i+j−N) times the two independent death-chain probabilities at time 2t. QED.

For i+j > 0 this also yields the exact occupation integral

integral_0^infinity P(I_t=i,J_t=j, alive) dt
= 2^(i+j−N−1) binom(a,i) binom(b,j)
  * (i+j−1)! (N−i−j)! / N!.

Equivalently it is 2^(i+j−N−1) times the occupation integral of the unit-rate non-killed chain. Thus correcting the time variable only introduces a common factor 1/2 in the transient-state integrals used by the heuristic. It does **not** change whether the corresponding series converges.

The artificial state (0,0) is absorbing and has positive limiting probability 2^(−N); its infinite occupation time must not be included in a finite transient-state integral. The source sum uses positive exterior counts. We make no geometric claim from a fictitious state with zero exterior regions.

## 5. Exact missing statement

A valid solution by this route needs a uniform estimate for the actual p_C(t), with contour repetition and nonconsecutive adjacency retained, strong enough that the sum of integral_0^infinity p_C(t) dt over enclosing circuits is finite, or another argument implying hegemony. The suppressed formula does not supply that estimate automatically. The two-count chain does not become valid after the time-scale correction. No such missing estimate is claimed in this packet.
