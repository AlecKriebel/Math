# The corrected approximation dependency in the free-H4 application

This is a hypothesis audit of the established prior resolution, not a new author-search turn. Bowen's published Theorem4.1 should not be invoked with its original incomplete random-net continuity proof. ABBG, arXiv1811.02520v3 §2.3, pp16–18, explains the problem and replaces it by Theorem2.9, proved in §2.4. The replacement uses finitely many Poisson stages and a uniform small completion error. We use that theorem as the credited analytic input. The account below verifies its application without assuming that intersections with a reentrant boundary are convex.

## 1. The hypothetical Følner sequence

Suppose the uniform free-group Cheeger gap in H4 were false. The smoothing step in Bowen's Lemma7.3 and the residual-cover step in Lemma7.2 yield complete quotients E_i=H4/Γ_i and positive-volume compact connected subsets K_i such that:

- Γ_i is free, hence H_2(E_i;Q)=0;
- for every fixed R, vol(N_R(∂K_i))/vol(K_i) tends to zero;
- the covering radius along K_i tends to infinity.

These are the precise inputs extracted from Bowen §7, preprint pp27–35. Residual finiteness removes the finitely many short conjugacy classes meeting a compact set; passage to the chosen subgroup preserves freeness. The fixed-radius boundary estimates are preserved by the finite covers. The smoothing constants depend only on curvature and dimension, fixed here. We rely on these stated prior lemmas, not on the flawed approximation theorem, for this reduction.

Put M_i=N_10(K_i), with the ambient metric restricted to M_i and ambient Riemannian volume restricted to it. Use the extended metric-measure space (M_i,vol,E_i), as in ABBG. Its volume is asymptotic to vol(K_i): the extra region lies in N_10(∂K_i). Also

    N_R(∂M_i) ⊂ N_{R+10}(∂K_i).

For the inclusion, a point on ∂M_i lies at distance10 from K_i and thus from its boundary; apply the triangle inequality. Therefore all fixed-radius boundary-to-volume ratios still vanish. Covering radii along M_i also tend to infinity. The volumes tend to infinity: otherwise the boundary estimate at increasingly large fixed R, together with the diverging covering radius, would force embedded hyperbolic R-balls inside a uniformly bounded-volume K_i. More explicitly, if K_i had no point farther than R from its boundary, its whole volume would lie in N_R(∂K_i), contradicting that ratio tending to zero; an interior point farther than R supplies the embedded ball.

## 2. All volume and convergence hypotheses

Fix the ABBG parameters r_0=1, r_1=2, r_2=4, r_3=5. A ball of radius1/2 in M_i has a uniform positive volume lower bound for all sufficiently large i. If p∈M_i is at distance at least1/4 from a nearest q∈K_i, move1/4 toward q; the radius1/4 ball there lies both in M_i and in B_{E_i}(p,1/2). If dist(p,K_i)<1/4, use the radius1/4 ball at q instead. These balls are embedded for large i, giving v_min=vol_{H4}(B(1/4)). Open-ball endpoint equalities can be handled by using radius1/8 instead, with the same conclusion.

For every r>0, vol(B_{M_i}(p,r))≤vol_{H4}(B(r)); quotient balls have at most the universal-cover volume. Thus the replacement theorem's stronger all-radius upper-bound requirement is satisfied, not merely a single-radius bound.

Each M_i is compact and path connected. Its measure is non-atomic, fully supported, and gives zero mass to metric spheres, since the distance is the ambient distance and ambient spheres have volume zero. Full support also follows from the inward-ball argument. Thus it is a special finite-volume mm-space. Outside a fraction tending to zero near the boundary, any fixed-radius pointed ball of the pair (M_i,E_i) is exactly the corresponding hyperbolic ball, because the covering radius diverges. Hence the extended spaces BS-converge to the pointed pair(H4,H4). These facts verify the topological, measure and convergence inputs of ABBG Theorem2.9.

## 3. Uniform control of the nerve for EVERY allowed net

Take any [4,5]-weighted (1,4)-net S_i in M_i, and let U_i be the union of its ambient open balls. These balls cover M_i. For large i, all of them and their finite nonempty intersections are strongly convex in E_i; their radii are bounded and the local covering radius diverges. Thus their nerve K_i^U is homotopy equivalent to U_i.

Extend this to a locally finite good cover of E_i using small strongly convex balls contained in E_i\M_i. This is possible because U_i is an open neighborhood of the compact M_i; after leaving a sufficiently small positive neighborhood of M_i, choose a locally finite refinement in the complement. Every added ball can be chosen to have radius at most1. The resulting full nerve K_i is homotopy equivalent to E_i, so b_2(K_i)=0.

Let K_i^V be the subcomplex on the added vertices together with those original vertices whose balls meet an added ball. Every mixed simplex lies in K_i^V, so K_i=K_i^U∪K_i^V. The intersection consists only of original net vertices whose radius-at-most5 balls leave M_i; such centers lie in N_5(∂M_i).

Because the centers are1-separated, their ambient radius1/2 balls are disjoint (up to null boundaries) and embedded. The number of intersection vertices is at most

    vol(N_6(∂M_i))/vol_{H4}(B(1/2))=o(vol(M_i)).

Any two adjacent original vertices are at distance at most10, so packing gives a uniform degree bound Δ, independent of the net and of i. The number of2-simplices in the intersection is at most its vertex count times binom(Δ,2). Mayer–Vietoris therefore gives

    b_2(K_i^U)≤b_2(K_i)+b_2(K_i^U∩K_i^V)
                ≤o(vol(M_i)).

This is uniform for ALL permitted nets and weights. In particular ABBG's nerve-approximation hypothesis holds with B_i=1, since vol(M_i) tends to infinity. We do not claim that balls cut by ∂M_i form a convex good cover; every nerve here uses AMBIENT balls, exactly as allowed by the extended-space theorem.

## 4. The interleaving contradiction

Fix a torsion-free cocompact residually finite lattice Λ in Isom(H4), and take a nested normal tower Λ_j with trivial intersection. The compact quotients Y_j=H4/Λ_j have injectivity radius tending to infinity and BS-converge to H4. Lück approximation and positivity of the middle L²-Betti number give

    b_2(Y_j)/vol(Y_j) → b_2^(2)(Λ)/vol(H4/Λ)>0.

For each Y_j regarded as (Y_j,vol,Y_j), the same parameters, lower volumes and all-radius upper bounds work for large j. Every allowed weighted net has a convex-ball good cover of the entire Y_j, so its nerve has exactly b_2(Y_j). Take B_j=b_2(Y_j)+1 to ensure positivity; the error1/vol(Y_j) vanishes.

Now interleave (M_i,vol,E_i) and (Y_j,vol,Y_j). This one sequence satisfies every hypothesis of ABBG Theorem2.9 with common constants and the same extended BS-limit. The theorem says its B/volume ratios converge. Along the first subsequence they tend to zero, and along the second to the positive constant above, a contradiction.

This verifies the replacement theorem in the exact free-H4 application. The conclusion is the uniform Cheeger gap used in PRIOR_RESOLUTION.md. It preserves Bowen's result with the later ABBG repair credited; it does not claim the original general metric-measure theorem was correct without qualification, nor that we have supplied a new independent proof of all background analytic theorems.
