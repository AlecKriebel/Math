# Independent scope reconstruction after actual primary reading

Written 2026-11-15 UTC, after the immutable INITIAL_SEAL and before opening the
deposited SOURCE_PROOF_REPAIR or any archived verdict/report. This continues my
own eight-family reconstruction. No current sibling findings were read.

## 1. Exact category and original claim

Theorem 1 concerns every finite nonempty connected simple unit-edge median graph
given by adjacency lists, promised median, with an arbitrary finite nonnegative
real profile. The output is a vertex center, the exact minimum radius, and every
vertex center, deterministically in O(n log^5(2n)) exact operations. The profile
interface compares only k w(u), 0 <= k <= n-1. It is a comparison/word-operation
claim, not an encoding-independent bit bound, recognition algorithm, arbitrary
edge-length theorem, or continuous/infinite-center claim. The complete abstract
also makes a proof-repair and a bounded credit claim; both are assessed here.

## 2. Threshold equivalence, including zeros

Let D=n-1 and define b(u) as the largest bounded integer k with k w(u)<=R.
For R>=0, k=0 exists. Nonnegative w makes the predicate monotone. A binary search
therefore uses O(log(2n)) comparisons and returns b=D for w=0. For each integer
distance d in [0,D], w(u)d<=R iff d<=b(u) iff d+D-b(u)<=D. Conjoining over u
gives the exact equality of complete feasible sets in the manuscript. This is a
deduction for every bounded integral metric; medianity is needed for the fast
additive oracle, not for this equivalence. No convexity/Helly assertion is used.

R<0 gives the empty feasible set since all radii are nonnegative. For n=1 the
only radius is zero. For an all-zero profile every vertex is optimal. For
singleton positive support, its supporting vertex is the unique zero-radius
center. Distinct vertices are still possible centers when their own weight is
zero. On P3 with profile (1,0,1), the middle vertex is the unique center, radius
1. With (1,0,2), both middle and right endpoint are centers, radius 2. These two
examples respectively detect deleting zero-weight vertices and replacing <= by
<. With a two-vertex edge of length 1/2 and equal weights, radius 1/2 is not in
the proposed integer candidate rows; the unit-edge restriction is load-bearing.

## 3. Complete optimization invariant and all-center output

Every vertex radius is an attained maximum among the n^2 conceptual values
k w(u); taking a minimum does not change that membership. B=D max w(u) is
feasible at every vertex. Maintain B feasible and either B=rho or an active row
copy of rho. A feasible pivot q must be saved as an incumbent before deleting
all values >=q. If rho<q its active copy survives; if rho=q the incumbent saves
it. An infeasible pivot has q<rho and deleting all <=q cannot lose rho. This
proves the invariant until no active values remain, when necessarily B=rho.
The saved witness is then a center. A final threshold call returns every x with
r_w(x)<=rho, exactly the full center set. The proof handles duplicate candidate
values, equality, zero rows and a feasible initial bound that is not itself a
realized vertex radius.

For a nonempty active row of length L, its lower middle has at least L/2 entries
on each weak side. Weight each middle by its entire active row length, not by
one. A weighted median has >=M/2 total length on both weak sides. At least half
the corresponding row entries are removed on either decision outcome, so at
least M/4 entries disappear, inclusive of ties. M starts n^2 and shrinks by
factor <=3/4 until zero: O(log(2n)) oracle calls. Binary searches and sorting
cost O(n log(2n)) per query, hence O(n log^2(2n)) profile comparisons. This is a
slightly slower comparison-only implementation of the credited Ducoffe method.

## 4. Additive interface and independent gate identities

The actual BDH v1 body states its input as an arbitrary nonnegative integer
arrival profile, and computes *all* max_y[d(x,y)+a(y)] values, not merely the
unweighted center or a single eccentricity. Our transformed a lies in [0,n-1].
The actual all-eccentricity proof is in Sections 3-4, not its separate distance
oracle. It supplies preprocessing from an adjacency graph; no embedding is an
input promise. The final SODA chapter was not obtained (ordinary GET returned
403); I make no assertion about errors surviving in the final chapter.

For a gated part H with gate g_H(x), every y in H satisfies
d(x,y)=d(x,g_H(x))+d(g_H(x),y). Consequently the maximum arrival distance into H
is d(x,g_H(x))+E_H(g_H(x)). This directly justifies the balanced merge and the
update for vertices in remaining slices. For a slice S and complement K in a
current gated graph, set A(z)=max_{y in K:g_S(y)=z}[d(z,y)+a(y)] at boundary gates
(and keep original a elsewhere). Then for x in S, arrival distances from K are
represented by max_z[d(x,z)+A(z)]. Taking the maximum with the original-profile
eccentricity on S gives the full answer. Two calls are safe even when the fiber
profile overwrites a large original boundary weight with a smaller open-fiber
value. No assertion that the second profile dominates the first is required.

Here is a shorter independent reason for the wide-ladder residual rule. If
I(v0,v) and I(v0,u) intersect at a vertex other than v0, a first edge on a
geodesic from v0 to their median belongs to a class adjacent to v0 separating
both v and u from v0. Thus disjoint ladder sets force that median to be v0,
so v0 lies on I(v,u). For a farthest arrival vertex u at v0, triangle inequality
then gives E(v)=d(v,v0)+E(v0). This argument needs median intervals and the
signature/first-edge characterization; it does not depend on the numerical
balance constant. It validates extending this structural step to f(s)>=2.

## 5. Existing appendix repair, not a new repair supplied by this review

The deposited paper already changes the literal preprint balance parameter to
f(s)=2 ceil(log2 s). The question is whether that *existing* appendix proves its
claimed interface, not whether an unsupported source can now be repaired.
Actual primary definitions make halfspaces gated, slices intersections of
halfspaces, and the unique-majority lemma valid for any f>=2. The gate/fiber
identities above likewise use no 2 ln(s)-specific fact. A ladder is a pairwise
orthogonal incident class family and hence spans a cube: ell<=log2 s. Each slice
is inside a minority of size <s/f. Keeping both profile calls therefore yields
total child volume 2 sum|S_i| <= 2 ell s/f <= s. In the balanced case the two
children partition the vertices and neither exceeds s(1-1/f). An unbalanced
child is smaller than s/f, which is <=s(1-1/f) since f>=2. These are exact
integer checks; the chosen L is the bit length of s-1, so no logarithm primitive
is necessary to select the cut.

For s>=3, f(s)<=4 log2 s =lambda ln s with lambda=4/ln2. Along a root-N
nonterminal path, every factor of shrinkage is at most
1-1/(lambda ln N). After h steps,
s_h<=N exp[-h/(lambda ln N)]. At ceil(lambda(ln N)^2) steps it would be <=1;
the direct s<=2 base case must already have occurred. This uses the ROOT size
in every denominator, avoiding the reversed varying-size product comparison.
Per-level volume is at most N. Local BFS, class/halfspace processing and all
ladder merges require O(s log^2(2s)), so total O(N log^4(2N)). Every arrival
update adds an induced-subgraph distance <=N-1 to a prior label. Starting at
<=N-1, at O(log^2 N) levels all labels are O(N log^2(2N)), fitting O(log(2N))
bits. This validates the required word-operation interface for these calls.

The primary's majority uniqueness uses f>=2; its residual eccentricity identity
uses median geometry; its large residual size and recursion-volume estimates
use ell/f<=1/2. All remain true under the deposited f. No objective, graph,
needed call, or independent structural theorem has been discarded.

## 6. Succinct exact falsifier of the literal old estimate

The actual v1 defines log=ln on page 4, has the reversed product comparison on
printed page 13, and uses ell<=log(s) in the child-volume step on page 24 despite
the actual cube bound log2(s). The manuscript's succinct witness tests that
literal estimate, not the final SODA text or algorithm correctness.

Take the 30-cube, attach t=17,000,000,000 leaves at each of the 30 unit vectors
and z=488,926,258,176 at zero. N=2^30+30t+z=10^12. Attaching a pendant vertex
preserves medianity: if a triple includes it, its adjacent attachment point
replaces it when the median is elsewhere; a repeated leaf is trivially the
median. Thus the construction is a finite median graph. Every cube cut's
minority has m=2^29+t=17,536,870,912 vertices; all leaf cuts have minority 1.
The exact Taylor sum through j=11 of 7^j/j! is 2,959,911,103/2,851,200>1000;
therefore ln N<28. Since 56m=982,064,771,072<N, every cut is unbalanced for
the literal 2 ln N rule. The majority intersection is zero.

Put arrival N-1 at the cube antipode and zero elsewhere. Its distance at zero
is N-1+30, strictly above any other arrival distance (at most 30), so it uniquely
defines the wide ladder of all 30 cube classes. The union of their minorities
is 2^30-1+30t=511,073,741,823. Disjoint slices partition that union regardless
of class order. Two calls per slice have total volume
1,022,147,483,646>N, falsifying exactly the literal intermediate bound. The
deposited f(N)=80 classifies these coordinate cuts balanced and prevents that
case. No giant graph was allocated; the construction, gates, sizes and exact
integer/Taylor certificate suffice. This does not establish a failure of the
final asymptotic bound without the appendix, nor any error in the final SODA
chapter; the paper itself carefully limits the claim in those ways.

## 7. Combined complexity, exact input model and scope conclusion

The repaired imported all-arrival algorithm has T(n)=O(n log^4(2n)); each
threshold budget costs O(n log(2n)) comparisons and one T call; the implicit
search needs O(log(2n)) calls and a final call. Thus O(n log^5(2n)) exact
operations is the full original result. Adjacency reading is absorbed since
median m<=n log2 n. For rational p/q with B-bit components, cross products
k p_u q_v versus j p_v q_u have O(B+log n) bits, including a harmless factor
two in B. Their arithmetic/comparison bit cost and input reading must be paid.
No floating precision, empirical timing, continuous interpolation, radius
unimodality, arbitrary real encoding, or dimension cap enters the deduction.

No substantive gap in the full original theorem or the *already deposited*
appendix remains in this scope review. This is mathematical verification using
credited classical primary interfaces; it is not human peer review or a
proof-assistant certificate. The finite controls are falsification attempts,
not the proof of a universal or asymptotic statement. Absolute firstness and a
worldwide claim that the problem remained open on October 14 are not verified
and are not claimed by this manuscript.
