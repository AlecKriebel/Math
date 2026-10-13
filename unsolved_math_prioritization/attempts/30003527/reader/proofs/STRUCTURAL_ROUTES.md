# Enlargement routes and their precise limits

Target: row 1767 / 30003527 / OWR-15575-006. Shared substantive pass 1, 13 October 2026. These are elementary reductions and partial constructions; none resolves the unrestricted target.

## 1. The maximal invariant core is compact, but need not be movable

For compact N define Inv(N)={x∈N:φ(t,x)∈N for every t∈R}. It is an intersection of closed subsets of N, hence compact, and the group law makes it invariant. If A is invariant and A⊂N, then A⊂Inv(N). Thus any compact neighborhood N⊂U supplies an invariant enlargement. The missing assertion is movability.

Isolation is not automatic. For the identity flow, Inv(N)=N for every compact neighborhood N, so Inv(N) meets ∂N. Nevertheless the original question is affirmative for that flow: a sufficiently fine finite union of closed grid cubes meeting A is an invariant finite polyhedron inside U. Therefore a reduction demanding isolated enlargements would exclude an elementary positive case.

If Inv(N) is isolated and its Čech H⁰,H¹ over F₂ are finite-dimensional, the coefficient-bridge and spine argument supplies a valid movable enlargement B=Inv(N). No finite-dimensionality bound for arbitrary Inv(N) has been established.

## 2. Finite-time cores do not furnish movability maps

The compact sets

N_T = {x∈N:φ(t,x)∈N for all |t|≤T}

are decreasing with T and intersect to Inv(N). For every neighborhood W of Inv(N), some N_T is contained in W, by compactness and the finite-intersection property. This supplies cofinal set-theoretic approximants. It does not supply a homotopy from a fixed neighborhood of Inv(N) to N_T. For a saddle, shifting every point forward may expel the unstable part, while shifting backward may expel the stable part. A continuous, globally compatible way to make those opposing choices is additional information, not a consequence of the shrinking-intersection argument.

Similarly, a finite-time saturation φ([-T,T],P) of a small polyhedral neighborhood P of A is compact, but generally not invariant. Its full saturation need not stay in U or be bounded. These operations therefore do not complete the requested construction.

## 3. A genuine sufficient trapping criterion

Suppose K is compact invariant and has the following property: for every O⊃K there is an open V⊃K with compact closure such that φ([0,∞),cl V)⊂O and φ([T,∞),cl V)⊂W for some T depending on each W⊃K. Then K is movable: use H(x,s)=φ(sT,x). This directly covers a compact asymptotically stable attractor under the usual uniform attraction of compact subsets of its basin; reversing time covers repellers. It works in every Euclidean dimension.

Neither one-sided stability without attraction nor arbitrary invariance supplies the terminal uniform-attraction clause. No argument here upgrades all invariant compacta to sets satisfying this criterion.

## 4. A compatible satellite construction really does work

Let A=⋂T_n for nested solid tori T_{n+1}⊂int T_n. Suppose D_n⊂int T_n\T_{n+1} is a tame core circle of T_n and D_n→A in Hausdorff distance. Put B=A∪⋃_{n≥m}D_n. If all A,D_n are invariant under the given flow, B is compact and invariant. If the selected tail lies in U, B is a candidate enlargement in U.

Here movability can be proved rather than inferred merely from Hausdorff convergence. Given O⊃B, choose j with T_j⊂O and j≥m. Choose k>j. In T_j, the inclusion T_k→T_j is homotopic to a map into the core circle D_j: compose the inclusion with a deformation retraction T_j→D_j and restrict the homotopy to T_k. The finitely many circles D_m,…,D_{k-1} are disjoint from T_k and have pairwise disjoint small tubular neighborhoods inside O, each retracting onto its circle. The union V of int T_k with those tubes is a neighborhood of B. Use the core homotopy on int T_k and the tube retractions on the disjoint remaining domains. The endpoint lands in D_m∪···∪D_{k-1}⊂B, hence in every neighborhood W of B. This verifies movability exactly.

The (3,1)-satellite example shows why the core hypothesis cannot simply be dropped. A periodic point near A does not furnish such an invariant core circle, does not ensure confinement of its full orbit to U, and does not verify the needed winding compatibility.

## 5. Remaining full-target obstruction

For arbitrary A,U, no method above either produces an invariant movable B inside U or excludes every possible such B. The current strongest concrete next candidate is the nonmovable solenoid-plus-(3,1)-satellites compactum: it has free first Čech cohomology and surjective homology bonding maps, so it survives the structural tests proved in this pass. Its realization as an isolated invariant set remains wholly unproved. This is an exact realization gap, not a technical detail to be suppressed.
