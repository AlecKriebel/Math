# The satellite candidate passes the global homology tests

Target: row 1767 / 30003527 / OWR-15575-006. Shared substantive pass 1, 13 October 2026. This supplements the explicit construction and nonmovability proof in SATELLITE_CIRCLE_AUDIT.md. It does not supply a dynamical realization.

Let T_{n+1} ⊂ int T_n be defining solid tori of a dyadic solenoid Σ, with longitudinal winding two. Let C_n ⊂ int T_n\T_{n+1} be the (3,1) satellite in that construction. Put X=Σ∪⋃_{n≥1}C_n. The companion audit proves that X is nonmovable by testing the image of a connected core loop in a single component of a target neighborhood.

## A cofinal neighborhood expansion

For n≥1 choose

P_n = int T_n ⊔ Q_{1,n} ⊔ ··· ⊔ Q_{n-1,n},

where Q_{i,n} is a sufficiently small open tubular neighborhood of C_i. Choose the old tubes successively nested and shrinking to their circles; choose the new tube Q_{n,n+1} inside int T_n and disjoint from T_{n+1}. All tubes at a given level are disjoint from one another and from the central torus. They may be chosen so that P_{n+1}⊂P_n and the family is cofinal among open neighborhoods of X. Cofinality follows from compactness, the Hausdorff convergence of the tail to Σ, and shrinking the finitely many earlier tubes.

Thus P_n is the disjoint union of n open solid tori. Write a_n for its central cohomology generator and b_i for each older circle generator. The maps induced by inclusion P_{n+1}⊂P_n on integral cohomology are

a_n ↦ 2a_{n+1}+3b_n,
b_i ↦ b_i for i<n.

The coefficients are the longitudinal winding numbers of T_{n+1} and C_n in T_n.

## Integral cohomology is free, despite nonmovability

The vector (2,3) is primitive in Z². Explicitly, the vectors (2,3) and (1,1) form a basis, with determinant -1. Consequently each displayed cohomology map is a split injection with a rank-one free cokernel. Start with a basis of H¹(P_1;Z), extend its image by one vector at each subsequent stage, and take the union of the compatible bases. Continuity of Čech cohomology gives

Čech H¹(X;Z) ≅ direct limit H¹(P_n;Z),

which is free abelian of countably infinite rank.

This calculation is compatible with the necessary condition that the integral first Čech cohomology of every isolated invariant compactum of a continuous three-dimensional flow be free. That condition therefore does not rule out X.

On the other hand, X has infinitely many components: each C_n is an isolated clopen component and the remaining component is Σ. Their characteristic functions already give infinitely many independent classes in Čech H⁰(X;F_2). In degree one, reducing the displayed maps modulo two sends a_n to b_n and preserves the old generators; these are again split injections with one-dimensional cokernel. Therefore Čech H¹(X;F_2) is also infinite-dimensional. The finite-type positive theorem does not apply in either degree.

## Even the homology Mittag–Leffler test passes

On H₁ the bonding map sends a central generator to twice the older central generator, and the new satellite generator to three times that same generator. Because gcd(2,3)=1, their images together generate the old central copy of Z; the earlier satellite factors map identically. Thus

H₁(P_{n+1};Z) → H₁(P_n;Z)

is surjective for every n. In degree zero the new central and satellite components both map into the older central component, so the map is also surjective. All groups in higher positive degrees vanish. The entire integral homology inverse system therefore satisfies the Mittag–Leffler condition.

There is no contradiction with the nonmovability calculation. Homology surjectivity permits adding a loop class from the central component to a class from a satellite component. A continuous image of one connected loop must lie in a single component. In the nonmovability proof, no one target component has the required winding subgroup, even though the sum of their subgroups is all of the older central group. This is the precise loss of information in that homological test.

## Exact remaining dynamical problem

If a continuous full flow on R³ could be constructed with X as its isolated maximal invariant set in some compact neighborhood N, then A=X and U=int N would refute the target: invariance forces every B with X⊆B⊆U to equal X. No such flow is constructed or asserted here.

It would not suffice to make Σ and the C_n invariant while leaving the other orbits uncontrolled. Additional compact invariant sets inside N could supply a movable enlargement. Nor could X be a stable attractor, a repeller, or an isolated finite-type set under the positive results used in this pass.

Finally X admits no retraction onto Σ: such a retraction would embed Čech H¹(Σ;Z)=Z[1/2] into the free group Čech H¹(X;Z), which is impossible because every subgroup of a free abelian group is free. Thus the simpler solenoidal-retract obstruction also gives no realization shortcut.
