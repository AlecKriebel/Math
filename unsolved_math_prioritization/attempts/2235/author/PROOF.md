# Exact literal resolution of Erdős Problem 655

## Scope and attribution

This is an independently written verification of a known counterexample, not a new discovery. The maintained tracker credits Zach Hunter for noticing that its literal statement admits regular polygons. Erdős had already identified the same obstruction in a related, explicitly restricted pinned-distance problem in 1988, printed p.35. The exact minima below also appear in the unsigned April 22, 2026 overview linked from the tracker forum, Theorem 3.1. Sources and inspection limits are recorded in SOURCES.json and REPORT.md.

Throughout, X is a set of n distinct points of the Euclidean plane, n >= 1. Distances are positive distances between distinct points. Let d_X(x) be the number of distances from x to X minus {x}, let D(X) be the number of distances determined by all unordered pairs, let M(X) = max_{x in X} d_X(x), and let S(X) = sum_{x in X} d_X(x).

Call X admissible when, for each x in X and radius r > 0, at most two points of X lie at distance r from x. This is precisely the centered-circle restriction in the literal target. No prohibition on four concyclic points is added.

## Theorem

For every integer n >= 1, among admissible n-point planar sets,

min D(X) = min M(X) = floor(n/2),

and

min S(X) = n floor(n/2).

Consequently there do not exist c > 0 and an integer N such that every admissible n-point planar set, for every n >= N, determines at least (1+c)n/2 distinct distances.

## Proof of the universal lower bounds

Fix x in X. Group the n-1 other points by their distance from x. Admissibility makes each group have size at most two. Thus 2 d_X(x) >= n-1. Since d_X(x) is an integer,

d_X(x) >= ceil((n-1)/2) = floor(n/2).

The identity follows separately for even n = 2m and odd n = 2m+1. The set of distances counted by d_X(x) is contained in the global set, so D(X) >= d_X(x). Taking a maximum and a sum gives all three lower bounds. This reasoning also covers n=1 with each count zero.

## Construction and exact distance calculation

For n >= 2 put

p_j = (cos(2 pi j/n), sin(2 pi j/n)),  0 <= j < n,

and X_n = {p_0,...,p_{n-1}}. Distinct indices in this range give distinct points. For two distinct indices i,j, put a = (j-i) modulo n in {1,...,n-1} and k = min(a,n-a). Directly expanding the squared Euclidean norm gives

|p_i-p_j|^2 = 2 - 2 cos(2 pi a/n) = 4 sin^2(pi a/n).

Since sin(pi a/n) > 0 and sin(pi a/n) = sin(pi k/n), the distance is

r_k = 2 sin(pi k/n),  1 <= k <= floor(n/2).

Sine is strictly increasing on [0,pi/2]. Therefore these floor(n/2) numbers are pairwise distinct. Every such r_k occurs, for instance between p_0 and p_k. No other distance occurs. Hence D(X_n) = floor(n/2).

From any p_i, points at distance r_k have indices i+k and i-k modulo n. There are exactly two unless n is even and k=n/2, in which case these indices coincide and there is exactly one. There are no other equal-distance indices, by the strict increase just established. Thus X_n is admissible and each vertex has exactly floor(n/2) distances. This proves M(X_n)=floor(n/2) and S(X_n)=n floor(n/2). For n=1 choose any singleton. The constructions attain all the lower bounds.

Given arbitrary c>0 and N, choose any integer n >= max(N,2). Then

D(X_n) = floor(n/2) <= n/2 < (1+c)n/2.

The admissible X_n violates the proposed conclusion for that n, proving the quantified negation, in fact for every n>=2. This completes the proof.

## Boundary between this theorem and other problems

For n>=3 the vertices are in strictly convex position. The tangent line at each vertex supports the disk and meets it only at that vertex, so all vertices are extreme. Also, a line intersects the unit circle in at most two points, so no three vertices are collinear. Adding either of these restrictions does not remove the counterexample. For every n>=4, however, the construction has four concyclic points and fails the no-four-concyclic restriction. It therefore proves nothing against the historical no-four-concyclic pinned question or the tracker’s general-position variant.

If an alternative convention counts the zero self-distance, X_n has floor(n/2)+1 global distance values. The same eventual claim is still false: choose n>2/c. The theorem’s exact minima use only positive pairwise distances, as explicitly defined above.

## Why the degree-bound heuristic cannot produce an excess

For each occurring distance r_k the graph on X_n joining pairs at that distance has degree two at every vertex, except that the antipodal graph for even n has degree one. All these graphs coexist in the plane using ordinary straight-line segments, with crossings allowed. They partition the edges of the complete graph. Thus geometric compatibility alone cannot turn the degree-at-most-two hypothesis into any fixed positive proportional excess over n/2. Any repaired argument needs an additional hypothesis excluding this construction.

## Verification status

The argument above is the complete proof. The integer-polynomial controls in verify.py check finite instances without floating-point tolerance. Their results are regression evidence, not a substitute for the all-n argument and not a Lean or other proof-assistant certificate. No resolution of a repaired problem, no novelty, and no independent human peer review is claimed.
