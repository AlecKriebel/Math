# Continuous-flow obstruction audit

Date: 13 October 2026. Target: row 1767 / 30003527 / OWR-15575-006.

This is one complementary component of substantive pass 1. It does not increment the pass count separately. No counterexample or full affirmative solution is claimed.

## 1. Main established obstruction

**Proposition.** If K is an isolated invariant compactum of a continuous full flow on R³, then its integral first Čech cohomology group Ȟ¹(K; Z) is free abelian. The rank need not be finite.

The same argument applies in an orientable boundaryless 3-manifold. It does not require differentiability, absence of equilibria, connectedness, or finite generation of the cohomology of K.

### Dynamical input and source scope

Use J. J. Sánchez-Gabites, *Using an invariant knot of a flow to find additional invariant structure*, arXiv:2403.18805v1 (27 March 2024), Proposition 5(iii) and §5.4:

- https://arxiv.org/abs/2403.18805
- https://arxiv.org/html/2403.18805v1

The needed inputs are a tame compact 3-manifold isolating block N with compact surface entry set E = Nⁱ, and the isomorphism Ȟ*(N,K; Z) ≅ Ȟ*(E,L; Z), where L = n⁺ is compact in E. The paper works with continuous flows and establishes existence of such blocks without a finite-cohomology assumption. These are source-dependent inputs; the algebraic deduction below is written out independently. It is a corollary of the cited machinery, with no novelty claim.

### Three algebraic and topological facts

1. For any compact metric space X, Ȟ¹(X; Z) is torsion-free. Indeed, use a polyhedral expansion and continuity of Čech cohomology. Each finite-polyhedral H¹ is torsion-free by the universal coefficient theorem, and a direct limit of torsion-free abelian groups is torsion-free.

2. If L is a compact subset of a closed orientable compact surface S, then Ȟ¹(L; Z) is free abelian. Alexander-Lefschetz duality and the homology sequence of (S,S\L) give an exact segment

   H¹(S; Z) → Ȟ¹(L; Z) → H₀(S\L; Z) → H₀(S; Z).

   The image of the first arrow is finitely generated and torsion-free, hence free. The image of the middle arrow is a subgroup of the free abelian group H₀(S\L; Z), hence free. Thus Ȟ¹(L; Z) is an extension of a free group by a free group; it splits because the quotient is free. The empty L case is immediate. For our L take S = ∂N.

3. Let F be free abelian and J a finitely generated subgroup. Every generator of J uses only finitely many basis elements of F, so J lies in a finite-rank direct summand F₀. Hence F/J is a direct sum of a free abelian group and a finite torsion group. Every subgroup of a group of this form has the same form: project to the free factor, and split over the resulting free image.

### Proof of the proposition

All cohomology below is integral Čech cohomology. On the compact manifolds it agrees with ordinary cohomology.

The compact surfaces E and S = ∂N, and the compact 3-manifold N, have finitely generated cohomology. By Fact 2, H¹(L) is free. In the exact segment

H¹(E) → H¹(L) → H²(E,L) → H²(E),

the cokernel Q of H¹(E) → H¹(L) is free abelian plus finite torsion by Fact 3. The image of H²(E,L) → H²(E) is a subgroup of the finitely generated free group H²(E), so it is finite-rank free. Consequently the extension

0 → Q → H²(E,L) → image[H²(E,L) → H²(E)] → 0

splits, and H²(E,L) is free abelian plus finite torsion. The dynamical input identifies this group with H²(N,K).

Now use the exact segment

H¹(N) → H¹(K) → H²(N,K).

Let C = image[H¹(N) → H¹(K)] and D = image[H¹(K) → H²(N,K)]. The group C is finitely generated; as a subgroup of the torsion-free H¹(K), it is finite-rank free. By Fact 3, D has the form F ⊕ T with F free and T finite. Thus

0 → C → H¹(K) → F ⊕ T → 0.

Lift a basis of F to split off F. The remaining group G, the preimage of T, is finitely generated since C and T are finitely generated. It is torsion-free as a subgroup of H¹(K). Therefore G is finite-rank free. We obtain H¹(K) ≅ F ⊕ G, proving the proposition.

### Consequences for attempted counterexamples

A nontrivial generalized solenoid has integral first Čech cohomology equal to a rank-one noncyclic subgroup of Q: the direct limit of Z under multiplication by its successive covering degrees. This group is not free abelian. Therefore:

- No such solenoid can be an isolated invariant compactum for a continuous flow on R³.
- This remains true if every point of the solenoid is an equilibrium. Dropping C¹ regularity or allowing stationary dynamics does not rescue the isolated-solenoid construction.
- More generally, an isolated invariant compactum K cannot admit a retraction onto a nontrivial solenoid: the induced cohomology map would embed the solenoid's nonfree rank-one group into the free group H¹(K), whereas subgroups of free abelian groups are free.

This proposition does not say all isolated invariant sets are movable. Freeness of one cohomology group is not the required homotopy-theoretic movability condition.

## 2. A genuine all-enlargements obstruction criterion

Let A be a nonmovable invariant compactum, let N be compact with A ⊂ int N, and put M = Inv(N). Suppose A is a retract of M. Then U = int N is a counterexample neighborhood: every compact invariant B with A ⊆ B ⊆ U lies in M, and the retraction M → A restricts to a retraction B → A. A retract of a movable compactum is movable, a contradiction.

For completeness, the last preservation statement follows directly from the ambient definition in R³. Extend a retraction r:B→A coordinatewise to a continuous map r̃:R³→R³. Given O⊃A, choose a neighborhood P⊃B with r̃(P)⊂O. Movability of B gives Q⊃B whose inclusion into P can be homotoped into each prescribed neighborhood W⊃B. Choose a fixed small neighborhood V⊂Q of A so that the straight-line homotopy from x to r̃(x) stays in O for x∈V; this is possible because r̃ fixes A. For any target neighborhood T⊃A, choose W⊂r̃⁻¹(T) and compose the homotopy Q→P with r̃. Concatenating with the straight-line initial homotopy deforms V into T within O. Hence A is movable.

This criterion correctly excludes every allowed B, including disconnected B and B=A. It is only a criterion: this pass did not realize a suitable nonmovable retract A of M by a flow. If M is itself isolated and A is a solenoid, Section 1 rules out the criterion's retraction hypothesis. Merely postulating a family of nearby solenoids is not a construction.

## 3. Why an arbitrary wild equilibrium set is insufficient

For the identity flow, every compact A⊂R³ has the desired enlargement in every open U⊃A: choose a sufficiently fine cubical grid and take the union B of the finitely many closed grid cubes meeting A. Then A⊂B⊂U, B is invariant, and B is a finite polyhedron, hence movable. The same proof applies when the flow is stationary on an open neighborhood of A. Thus a nonmovable set of equilibria alone is not a counterexample.

A less trivial attempted construction can be analyzed exactly. For any nonempty compact A, put

F(x) = min(1, dist(x,A)) e₃.

This is a bounded globally Lipschitz vector field, so it has a unique continuous full flow; its equilibrium set is exactly A. On the vertical line over q∈R², write A_q for the compact fiber. Each bounded component (a,b) of R\A_q is one full trajectory, and [a,b] is its compact invariant closure. Every unbounded component yields an orbit unbounded in at least one time direction. Consequently every compact invariant B containing A is A together with a selection of whole bounded fiber-gap intervals, subject to closedness. The construction therefore generates additional candidate enlargements which must be analyzed; specifying its zero set does not establish the all-enlargements negation.

## 4. Periodic points do not provide confined periodic orbits

K. Kuperberg, *Periodicity generated by adding machines* (2013), printed pp.140–147:

- Publisher: https://trim.imath.kiev.ua/index.php/trim/en/article/view/310
- Proceedings PDF: https://www.imath.kiev.ua/~topology/publications/proceedings.2013.6.6.pdf

The theorem on pp.142–144 ensures that periodic points accumulate on an adding-machine Cantor set for an arbitrary planar homeomorphism, without stability. It does not ensure that each prescribed neighborhood contains a whole periodic orbit; the stronger assertion is Question 8 on p.146. Page 145 also states a circle-approximation movability assertion and asks invariant-enlargement questions. The circle assertion is not used as a certified lemma here: the companion SATELLITE_CIRCLE_AUDIT.md gives a homology obstruction to its unqualified topological reading. The printed hypotheses and questions were text- and visually checked.

The logical gap is material. A periodic point p inside U may have an iterate outside U. Suspension then produces a periodic trajectory passing near the solenoid but leaving the prescribed flow neighborhood. Such a trajectory cannot be used in B⊆U. Nor does pointwise accumulation alone imply compactness or Hausdorff convergence of the union of complete periodic orbits. No inference from the weaker theorem to the required invariant enlargement is justified here.

## 5. Current outcome and remaining claims

No flow/A/U triple excluding all movable enlargements was constructed. The isolated-solenoid family is excluded for continuous flows by Section 1, not merely unconstructed. The arbitrary-equilibrium and periodic-point routes have precise defects described above.

The full target still requires either an invariant movable enlargement for arbitrary compact invariant A and arbitrary U, or a concrete realization satisfying an all-enlargements obstruction such as Section 2. Infinite-rank free cohomology is not itself a movability theorem and does not close the remaining isolated-invariant cases.

## Verification metadata

The 2013 proceedings PDF was retrieved on 13 October 2026 from the public Institute of Mathematics URL above. Size: 16,393,363 bytes. SHA-256: faa28bfeca574bd2a37340858a09011ff25ac717ecdc7d80b5eebc93363c2499. Printed pages 142, 145, and 146 coincide with one-based PDF pages 142, 145, and 146 and were rendered and visually inspected. Relevant pp.140–147 were text-extracted and read. The article landing page reports publication on 26 June 2013; the PDF header and modern site disagree on volume numbering, so no volume is normalized here.

The Sánchez-Gabites arXiv HTML was directly read for Proposition 5, Definition 6, Proposition 15, and the surrounding block-existence argument in §5.4. Full proof verification of every cited classical theorem is not claimed. The complete authored deduction used here is in Section 1.
