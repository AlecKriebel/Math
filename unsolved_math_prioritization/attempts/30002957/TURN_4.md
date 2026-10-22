# Turn 4: the planar lower bound is also strict

Substantive author turn **4/5**. For the homogeneous planar model with the simplex-typical convention already proved in turn 1,

                   2/3 < theta_{2,2} < 1.                         (26)

The upper inequality is from turns 1–2. This turn proves the strict lower inequality by a positive-density protected octahedral patch. Set

 h=1/10000,   p=exp(−2500π)(2h)^12,   ρ=p/10000.

A quantitative (extremely weak) version is

 b_{2,2} <= 3−2ρ,          theta_{2,2} >= 2/(3−2ρ)>2/3.             (27)

It does not determine the exact planar fraction.

## 1. A planar Delaunay patch with a triangle deficit

Use the six rational sites

 A=(0,4), B=(−4,−2), C=(4,−2),
 a=(0,−1), b=(1,1/2), c=(−1,1/2).

The outer triangle is ABC. The inner sites a,b,c lie strictly inside it. The seven interior triangles

 ABc, ACb, Abc, BCa, Bac, Cab, abc

have empty circumcircles relative to the six sites, strictly excluding the other three sites. With indices A,B,C,a,b,c=0,...,5 their centers and squared radii are:

 (0,1,5): (−205/32,63/16),       42029/1024;
 (0,2,4): ( 205/32,63/16),       42029/1024;
 (0,4,5): (0,59/28),            2809/784;
 (1,2,3): (0,−19/2),            289/4;
 (1,3,5): (−115/56,−9/7),       13481/3136;
 (2,3,4): ( 115/56,−9/7),       13481/3136;
 (3,4,5): (0,1/12),             169/144.

The smallest squared-distance exclusion margin is 85/14. Every oriented two-by-two determinant for these triangles has absolute value at least 3. The largest absolute center coordinate is 19/2.

The resulting graph is the octahedral graph: every pair is an edge except Aa, Bb, Cc. It has eight graph triangles, exactly the seven displayed interior faces and the exterior cycle ABC. In particular exactly seven graph triangles contain an inner vertex. Removing the three inner vertices changes the triangle count by 7, whereas the general planar upper bound 3n would drop by 9. Each protected patch therefore creates a deficit of 2.

## 2. Uniform perturbation and external protection

Let every coordinate of each site move by at most h. We verify a uniform open neighborhood, not just sampled perturbations.

For any of the seven triples, use the original 2-by-2 matrix A_0 whose rows are the two vertex differences from one endpoint u. Its circumcenter solves A_0 c_0=b_0, where the two entries of b_0 are half the corresponding differences of squared norms. All coordinates of the original sites have absolute value at most 4, their l1-norms at most 8, and all matrix entries have absolute value at most 8. The determinant lower bound gives

 ||A_0^{-1}||_infinity <=16/3.

The perturbed matrix satisfies ||A'−A_0||_infinity<=4h. The perturbed right side differs by at most 17h in maximum norm. Hence Neumann inversion gives ||(A')^{-1}||_infinity<=6 and

 ||c'−c_0||_infinity
   <=6[17h+4h||c_0||_infinity] <=342h.

Thus ||c'||_infinity<=11. The error in the exclusion gap for any other selected site z, using endpoint u of the triple, is at most

 33h + 2(342h)·16 + 2·11·4h =11065h <85/14.                       (28)

The first term bounds the two squared-norm changes, the second bounds the center change paired with z−u, and the third bounds the site perturbations paired with c'. Every displayed circumcircle therefore remains strictly empty of the other selected sites. Its radius is at most 16 sqrt(2), so its whole ball lies in B(0,27 sqrt(2)), hence in B(0,50).

The inner sites remain inside the outer triangle. For each original oriented outer edge and inner site the signed determinant is positive and at least 8; its perturbation changes that determinant by at most 64h+8h²<1. The outer orientation likewise persists. The site boxes are disjoint.

Require one Poisson point in each open coordinate box of side 2h around these six sites, and no other point in B(0,50). This event has probability p. The seven empty-circle witnesses are entirely within the cleared ball, so no external point can spoil them. The general-position Delaunay graph is planar and contains the outer triangle and all seven interior faces. An inner vertex has no neighbor outside ABC: the straight segment to such a neighbor would cross its outer cycle, contrary to planarity. There are no additional Poisson points inside ABC. Therefore the inner vertices have exactly their octahedral neighbors, even in the full infinite process.

## 3. A positive density of additive deficits

Translate the protected event to all centers in 100Z². The open radius-50 balls are disjoint (tangencies have measure zero); independence is available but is not needed. For Q_R=[−R,R]^2, let Z_R count successful centers whose entire radius-50 ball is in Q_R. Then

 E Z_R = p · #{100Z² ∩ [−R+50,R−50]^2},
 E Z_R/|Q_R| -> p/10000 = ρ.                                    (29)

Consider the finite subgraph of the infinite Delaunay graph induced by the Poisson points in Q_R. Let n be its vertex count and t its graph triangle count. Delete the three inner vertices from each of the Z_R protected patches. The patches have disjoint vertex sets, every deleted vertex has only the neighbors described above, and no triangle involving a deleted vertex can run between patches. Thus the remaining planar graph has n−3Z_R vertices and exactly t−7Z_R triangles. The universal bound triangle count <=3 times vertex count, valid also for fewer than three vertices, implies

 t−7Z_R <=3(n−3Z_R),       or       t<=3n−2Z_R.                   (30)

Take expectations, divide by |Q_R|, and use the vertex-inside intensity convergence of turn 1 and (29). This proves b_{2,2}<=3−2ρ. The credited Delaunay face intensity is a_{2,2}=2, yielding (27). Scaling removes the choice of unit Poisson intensity.

## 4. Remaining gap

Both endpoints of the elementary interval are now ruled out by robust local events. The upper bound on the fraction comes from a forced missing face; the lower bound comes from a protected non-extremal planar patch. These are different mechanisms. The constants above are rigorous but have no practical numerical sharpness. Neither the exact planar fraction nor the source's dimensional behavior is obtained. Original unresolved after four substantive author turns. No additional external theorem is needed beyond the planar graph and Poisson ingredients already established/credited.
