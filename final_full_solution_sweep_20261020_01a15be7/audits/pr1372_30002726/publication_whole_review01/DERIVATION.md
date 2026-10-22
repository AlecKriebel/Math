# Independent reconstruction and attempted falsification

22 October 2026. Reviewer's universal argument, separate from the finite checker.
Claim: variable-threshold beta(G)>=t is NP-complete for finite loopless
2-vertex-connected graphs; NP-hardness remains on simple cones over connected
bipartite bases with a specified apex. beta counts the initial circuit and
one-edge open ears, and stops at the first even ear. All-odd prefixes, total odd
ears, closed ears, fixed thresholds and arbitrary binary matroids differ.

## Structural equivalences

An odd circuit is factor-critical. Adding an odd open path preserves that
property: deleting an old vertex uses an old near-perfect matching and pairs
the new even-length list of internal vertices; deleting an internal vertex
pairs vertices toward the two ends, leaving an old vertex to be deleted in
the old near-perfect matching. One-edge ears add edges only. Every prefix is
2-vertex-connected, and each ear increases m-n+1 by one. Thus a prefix of
length q gives a 2-connected factor-critical subgraph of cyclomatic number q.
The converse uses the explicitly imported classical Lovasz theorem in the exact
form authenticated by Benchetrit--Sebo Theorem3.2. I did not read the 1972 proof.

An open decomposition of a 2-connected subgraph H extends to G: any component
C outside V(H) has at least two distinct neighbors in H, since a sole neighbor
would be a cut vertex of G. A path between such neighbors through C supplies
the next open ear. Repeat until spanning and add all still missing edges as
one-edge ears. This proof uses finiteness, and does not require the extension
ears to be odd. Adding all induced missing edges to H preserves its matchings
and 2-connectivity and increases cyclomatic number. Hence beta is the maximum
of m(H)-n(H)+1 over induced 2-connected factor-critical H (zero if none).

For G=z*B with B bipartite, a qualifying H cannot lie wholly in B: an odd
bipartite graph with at least three vertices is not factor-critical, as deleting
a vertex in its smaller side prevents equal side sizes. Thus H=z*B[S]. Deleting
z shows B[S] has a perfect matching. Its connectivity is equivalent to
2-connectivity of H: deleting z leaves B[S], and deleting another vertex leaves
a universal apex. Conversely, for connected B[S] with perfect matching M,
deleting z leaves M; deleting u leaves a perfect matching formed by matching
z to u's mate and using the other edges of M. Such a base has at least two
vertices. H's cyclomatic number is exactly |E(B[S])|. Empty selections do not
produce spurious positive witnesses.

## Set Cover, with all exceptional inputs

U is explicitly listed, as are n sets A_j and integer s. Negative budgets give
the fixed NO triangle with threshold2. Empty U and nonnegative s give fixed
YES triangle with threshold1. Nonempty U with no sets, an uncovered element,
or s=0 gives NO; a covered instance with s>=n gives YES. Each fixed graph is
a cone over K2. Remaining instances satisfy m,n>=1, union A_j=U, 1<=s<n.
Empty and repeated individual sets remain allowed. No succinct encoding of
an exponentially large universe is assumed.

Write T=sum_j(1+|A_j|), k=T+n+3, M=(m+1)k^2 and F=M-ks. Thus k>T, k>s,
k^2>ks+T and F>0. Build m+1 disjoint K_{k,k} blocks, distinguished right
vertices q_i, and a left connector c_j adjacent to q_0 and all q_i with i in
A_j. Every set touches the root block, and coverage joins every element
block to it; the base is connected and simple. Its cone is in the promised
subclass, with the intended universal vertex explicitly supplied.

For a YES cover, take an inclusion-minimal subcover J of size r<=s. Each
j in J has an element private to it within J, and these elements are distinct.
Omit one left vertex from each private element block, retain all right
vertices and all remaining block vertices, and choose exactly connectors J.
Match each connector to its distinct private q_i, each resulting K_{k-1,k-1}
internally, and every unchanged block internally. The selection is connected
because J covers U and each connector meets q_0. Its induced edge count is
M-kr+sum_{j in J}(1+|A_j|)>=F. There is an actual disjoint covering matching;
balance alone is not invoked as sufficiency.

For ANY feasible induced connected selection at threshold F, let a_i,b_i
count omitted left/right block vertices and r the chosen connectors. If one
block has no internal edge, its loss is k^2; all connector edges combined
contribute at most T. Then E<=M-k^2+T<F, a contradiction. In particular every
block is nonempty and contains an edge, even if its distinguished q_i was
omitted. A perfect matching implies only the necessary global balance
sum(a_i-b_i)=r. Its block loss is
d_i=k(a_i+b_i)-a_i*b_i and
d_i-k(a_i-b_i)=b_i*(2k-a_i)>=0 for every 0<=a_i,b_i<=k.
Consequently E<=M-kr+T. With E>=M-ks this gives k(r-s)<=T<k, so the integer
r is at most s. The element block and distinct root block both retain edges;
connectivity requires the former to have an external edge. Such edges exist
only through retained connectors corresponding to sets containing that
element. Thus those r sets cover U. No whole-block optimality, retained q_i,
matching-from-balance, or undisclosed connectivity lemma is used.

Explicit source length L gives k=O(L), O(L^2) vertices and O(L^3) edges. The
threshold is polynomially encoded even if the source budget was binary; all
large-budget cases were handled before graph construction. A certificate
lists an induced H, witnesses for every perfect matching of H-v, and its
cyclomatic value; graph connectivity/2-connectivity and each matching are
polynomially checkable. Nonpositive thresholds are trivial on valid inputs.
Thus the full variable-threshold decision problem, rather than merely a
special case or a numerical conjecture, has the claimed complexity.

## Materially independent finite falsification mechanism

The new independent_matching_orbits.py imports no claimant or preparation
checker. It generates endpoint sets of matchings, checks their existence with
Ryser permanents, and tests connectivity by exact Kirchhoff determinants
using fraction-free Bareiss elimination. For general induced factor-critical
tests it enumerates pair partitions, independently of recursive bipartite
matching. Its separate ear-certificate validator reads actual complete
decompositions and rejects missing, repeated/nonexistent or closed ears.

For the full-size gadgets it exhausts twin-orbit representatives of every
perfectly matchable partial block selection. Let a,b be the retained side
sizes and q the retained distinguished-right flag. All left vertices have
only their internal block neighbors; thus b-a is either0 or1. A deficit1
requires q, and exactly one connector must match q. The chosen connectors
must match bijectively to precisely the deficit blocks. An exact permanent
counts these connector-block matchings. Remaining complete bipartite blocks
match internally; non-distinguished twin choices contribute their exact
binomial multiplicity. A quotient graph retains block components and chosen
connectors for connectivity. Single isolated retained right vertices are
separate components and included correctly; any retained left vertices with
b=0 make matching impossible. This establishes why the finite orbit
enumeration is complete, including partial blocks and omitted q_i.

Results:230 connected bipartite cases;4322 Ryser endpoint checks;1619 orbit
versus physical permanent checks;58 quotient versus physical determinant
checks;191 balanced nonmatchable selections;280737 matching-feasible orbits
across14 actual-k set families and26 cover decisions. A too-small k=2 gives
a false cover implication (connected optimum12, threshold10), so the large-k
inequalities are essential. Complete k=3 orbit enumeration independently
gives connected optimum25 versus disconnected27. The published H3 has
initial-prefix optimum2 versus maximum TOTAL odd ears4; the source's bound
is only at least3, not equality3. K2,2-cone certificates distinguish omitted
initial-circuit and one-edge counts. Malformed certificates, the stronger
false omission bound and other boundary mutations are rejected.

All normal/-O/-OO complete independent outputs agree. These finite results
are debugging and falsification evidence, not the universal proof, a
literature-priority certificate or proof-assistant verification.
