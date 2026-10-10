# Problem 6200014: positive consequence of published results

## Claim and status

For a closed topological n-manifold N and a finite simplicial flag, no-induced-square triangulation Delta of N, the homeomorphism type of the boundary of its right-angled Davis complex depends only on the homeomorphism type of N. This includes triangulations inducing different PL structures. A common subdivision is not required.

This is a literature-based resolution, not a new boundary theorem. The crucial recognition theorem belongs to Jacek Świątkowski. The deductions below connect its hypotheses to the precise source problem. This note is AI-assisted and unrefereed; it is not formal verification or a novelty claim.

## Source identification

The target is Kapovich's Problem 14, page 5 of [K], in the 2005 workshop problem list. The surrounding paragraph requires both flagness and no squares. It asks whether the boundary construction is independent of the chosen triangulation as a topological invariant. These hypotheses must not be dropped. The source's preceding common-subdivision observation is weaker than the desired assertion.

## Imported results

A. [PS, Lemma 5.1 and Theorem 5.6, Corollary 5.7(2), pp. 465–466] Flag-no-square is inherited by links. A generalized homology sphere of dimension at least four cannot have that property. Consequently, a triangulated manifold of dimension at least five cannot be flag-no-square. This statement explicitly includes non-PL triangulations.

B. Every simplicial triangulation of a topological manifold in dimensions at most four is PL. For dimension four, [DFL, p. 797] explains the link argument, using the three-dimensional Poincaré theorem. Lower dimensions follow from the classification of one- and two-dimensional links and three-dimensional PL uniqueness.

C. [S, Theorem 2, p. 594; proof p. 609] If a Coxeter nerve is a PL triangulation of a closed connected manifold M, its Davis–Moussong visual boundary is X(M#(-M)) when M is orientable, and X(M) otherwise. Here -M reverses orientation. The tree X is defined using topological manifolds; its uniqueness does not depend on a PL structure [S, Definition 1.1, Theorem 1.2 and Definition 1.3, pp. 595–597]. Equivalently, the orientable expression is the tree for the family {M,-M}.

D. [MS, Theorem 4.1] If corresponding factors of two free products of infinite hyperbolic groups have homeomorphic boundaries, then the free products have homeomorphic boundaries. Iteration gives the finite-factor version.

E. For a right-angled Coxeter group with finite flag nerve, the no-square condition implies word hyperbolicity [PS, Corollary 5.3]. The Gromov boundary agrees with the visual boundary of its Davis complex [S, Remark 5.4].

## Deduction

1. Let Delta_1 and Delta_2 triangulate homeomorphic closed manifolds N_1 and N_2 of dimension n and satisfy the stated conditions. If n >= 5, result A says neither triangulation exists. This case is vacuous. Thus every nonvacuous instance has n <= 4. By B, both triangulations are PL. This is the essential step preventing an illicit extra PL assumption.

2. Suppose the manifolds are connected and n >= 2. The nerve of the right-angled group defined by Delta_i is exactly Delta_i: spherical subsets are the cliques, and flagness identifies cliques with simplices. Apply C to each nerve and E to its boundary. A homeomorphism N_1 -> N_2 identifies the topological manifold families defining the trees. In the orientable case, choose the target orientation to make this homeomorphism orientation preserving; it then identifies both the positive and negative copies. Alternatively, an orientation reversal simply swaps the two family members. Therefore both boundary spaces are homeomorphic to the same tree. No PL equivalence or common subdivision is used.

3. For a connected one-manifold, Delta is a cycle of length m. Flagness excludes m=3 and no squares excludes m=4, so m >= 5. A compact regular right-angled hyperbolic m-gon exists: its interior angle varies continuously from (m-2)pi/m to zero as the radius increases, and pi/2 lies strictly between these values. Reflections in its sides realize the right-angled cycle Coxeter group geometrically on the hyperbolic plane. Hence its boundary is a circle. This handles n=1 independently of tree conventions.

4. A compact n-manifold has finitely many components. For n>=1, each component's nerve defines an infinite hyperbolic group: a closed positive-dimensional manifold cannot be a simplex, so a flag triangulation has two nonadjacent vertices; their generators have infinite dihedral subgroup. The full nerve is a disjoint union, so its Coxeter presentation is the free product of the component presentations. A homeomorphism pairs components, and steps 2–3 identify the corresponding factor boundaries. Applying D repeatedly proves invariance for disconnected N as well.

5. A closed zero-manifold is a finite discrete set. Its simplicial triangulation has exactly one vertex for each point, with no higher faces. Its Coxeter group, the free product of that number of order-two groups, is already determined by N. The empty case is equally independent of any choices.

These cases exhaust the source hypotheses, establishing the claim.

## Hypothesis audit and limitations

- The dimension obstruction uses actual topological manifold links, not arbitrary pseudomanifolds. Hyperbolic Coxeter groups of unbounded virtual cohomological dimension do exist; that does not contradict A.
- “Every triangulation is PL” does not mean that all triangulations induce the same PL structure. Step 2 explicitly avoids that inference, particularly in dimension four.
- Both orientation copies in C are required. Replacing X(M#(-M)) by X(M) for all orientable M is not justified here.
- Arbitrary subdivision need not preserve no squares. The finite controls exhibit an induced square in a barycentric subdivision and in a suspension.
- No equivariance, canonical boundary map, or quasi-isometry classification follows from this conclusion.
- The imported infinite topological theorems are not re-proved or certified by the finite checks. No mathematical gap remains in this deduction conditional on those published results; independent review remains required before accepting the packet.

## References

[K] Misha Kapovich, *Problems on boundaries of groups and Kleinian groups*, 2005 workshop list, Problem 14, p. 5. https://www.math.ucdavis.edu/~kapovich/EPR/problems.pdf

[PS] Piotr Przytycki and Jacek Świątkowski, *Flag-no-square triangulations and Gromov boundaries in dimension 3*, Groups, Geometry, and Dynamics 3 (2009), 453–468. https://doi.org/10.4171/GGD/66

[DFL] Michael W. Davis, Jim Fowler and Jean-François Lafont, *Aspherical manifolds that cannot be triangulated*, Algebraic & Geometric Topology 14 (2014), 795–803. https://doi.org/10.2140/agt.2014.14.795

[S] Jacek Świątkowski, *Trees of manifolds as boundaries of spaces and groups*, Geometry & Topology 24 (2020), 593–622. https://doi.org/10.2140/gt.2020.24.593

[MS] Alexandre Martin and Jacek Świątkowski, *Infinitely-ended hyperbolic groups with homeomorphic Gromov boundaries*, Journal of Group Theory 18 (2015), 273–289. https://doi.org/10.1515/jgth-2014-0043. Theorem 4.1 is also available in the 2013 preprint, https://arxiv.org/abs/1303.6774.
