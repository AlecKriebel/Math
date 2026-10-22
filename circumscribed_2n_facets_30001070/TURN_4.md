# Author turn 4: a nonsymmetric two-simplex family in the first open dimension

2026-10-03T06:43:10Z. Turn 4/5. **NO FULL RESOLUTION.** Completion estimate: 5%. This turn investigated an explicit global family with varying anisotropy and face structure, rather than another antipodal reduction.

## 1. An exactly normalized family

Let e=1/sqrt(n)*(1,...,1), J=ee^T, and let Q be any orthogonal matrix with Qe=e. For 0<z<1 put

  a=sqrt(n(1-z)/(n-1)), b=sqrt(nz), H=a(I-J)+bJ,
  U=[I; -Q] H.

The 2n rows of U are unit vectors, since every row of I and Q has squared component 1/n along e and squared component (n-1)/n orthogonal to e. Their sum is zero. For distinct rows they give 2n distinct vertices of an inscribed polytope; their positive spanning follows from full rank and their zero sum with strictly positive coefficients. The polar therefore has exactly 2n genuine facets and is bounded. Their frame operator is 2H^2, which is isotropic exactly at z=1/n. Thus varying z escapes the scoped tight-frame theorem of Turn 2.

The two groups lie on parallel hyperplanes at heights +/-sqrt(z) along e, and each forms a regular (n-1)-simplex. The relative rotation Q and height z can change the convex-hull facet structure. At z=1/n, Turn 2 already proves the desired bound for every Q; a numerical optimum there is not new progress.

## 2. Why looking only at vertices adjacent to the poles fails from n=5

The all-upper-facet vertex is x_+=e/sqrt(z), of squared norm 1/z. Its edge obtained by dropping upper facet i is x(t)=H^{-1}(1-t e_i). A lower facet first becomes active at

  t=2/max_j Q_ji,

where the maximum is positive because each column sums to 1. In particular t>=2. The squared norm along this edge is

  f(t)=1/z-2t/(nz)+t^2[(n-1)^2/(n^2(1-z))+1/(n^2 z)].

For Q=I the edge endpoint is t=2. Its squared norm is

  f(2)=(n-2)^2/(n^2 z)+4(n-1)^2/(n^2(1-z)).

For z>=1/n the quadratic f(t) is increasing on t>=2. It would be tempting to use f(2)>=n to finish this family. That assertion is false when n>=5. In dimension5, at z=3/11,

  f(2)=121/25<5.

However, when Q=I the vertex with two negative signs has squared norm 407/75>5. Thus the small one-edge values are not a counterexample; they show that an edge-only proof misses more distant vertices. Exact rational identities for these values are checked in check_turn_4.py. For n<=4 this particular failure does not occur in z>=1/n, consistent with the known dimensional boundary, but that observation is not a proof of the full low-dimensional literature.

## 3. Exact nonsymmetric example beyond 2^n vertices

To test the family outside the simple cube count, define Q as the product of the four rational Householder reflections I-2vv^T/(v^Tv), with

  v=(1,-2,1,0,0), (1,1,-1,-1,0), (1,0,1,-1,-1), (2,-1,0,-2,1),

in the written order. All v are perpendicular to the all-ones vector. Take

  H=(61/65)I+(18/325)11^T,

so a=61/65, b=79/65, and z=6241/21125. The script verifies rationally that all ten rows of [I;-Q]H are distinct unit vectors with zero sum, while their frame operator is not 2I.

Complete enumeration of the 252 five-row subsets, discarding singular systems and infeasible intersections, produces 34 distinct polar vertices, exceeding 2^5. Their maximum squared norm is

  340657525/23222761 > 5,

at the exactly feasible vertex

  (-15171,5369,5369,5369,-4901)/4819.

This is an exact rejection of one structured potential counterexample, not evidence that all such configurations are safe. The enumeration is small and finite; no large exhaustive search was undertaken.

## 4. Bounded floating-point exploration

For n=5, a circulant orthogonal Q was parameterized by Fourier eigenvalues 1, exp(+/-i theta1), exp(+/-i theta2). A 125-point parameter grid and nine bounded local searches totaling 2111 objective evaluations were performed. The grid reached 42 triangulated facets, so the family explored more than the cross-polytope's 32 simplicial facets. The largest observed centered inradius was 0.44721359549995787, at the cube, versus 1/sqrt(5)=0.4472135954999579. No candidate strict violation was found.

All these optimization results are explicitly non-certifying. Optimizer success, a finite grid, and floating-point hull output do not prove global optimality, equality classification, or even exact face counts in a degenerate case. Only the separate rational example and its enumerated feasible vertices are exact checks.

## Remaining gap

No inequality controls all vertices of every rotated, anisotropic two-simplex configuration, much less all unrestricted 2n-point configurations. The local and moment results exclude particular mechanisms, while this numerical search found no counterexample. The conjecture remains unresolved here. The fifth and final author turn will test a determinant-weighted all-bases identity as a different global mechanism and explicitly separate feasible vertices from merely intersecting supporting planes.
