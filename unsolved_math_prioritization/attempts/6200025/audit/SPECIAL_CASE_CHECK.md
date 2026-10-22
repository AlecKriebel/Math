# Direct check for the closed-surface example

This supplementary argument checks the exact finite-dimensional EZ axioms for the example in the frozen note. It is an elementary specialization consistent with the already published GHP conclusion and action, not a claim of a new theorem or historical priority. It does not claim that its compactification topology equals every choice of auxiliary topology in GHP.

## 1. A concrete covering action

Let S be a closed orientable hyperbolic surface of genus at least two. Choose a smooth diffeomorphism f₀ of S in a pseudo-Anosov mapping class. Such a smooth representative exists because surface mapping classes have smooth representatives; the hyperbolicity of its mapping torus depends on the mapping class, not on choosing the singular pseudo-Anosov representative itself.

Write X = H² for its universal cover and H for its deck group. Let f be a lift of f₀ and h = f⁻¹. Choose the induced automorphism φ so that f g = φ(g) f for g in H. Compactness of S makes f and h globally L-bilipschitz for some L ≥ 1, for the lifted hyperbolic metric. They extend to mutually inverse homeomorphisms f_C and h_C of the visual circle C.

On Y = X × R define

    g(x,r) = (g x,r),       t(x,r) = (h x,r+1).

Then t⁻¹ g t = φ(g). The action is free: a nonzero power of t changes the real coordinate, and the H action on X is free. It is proper: only finitely many integer shifts can meet a fixed compact vertical interval, and for each such shift properness follows from the covering action on X. It is cocompact: a compact H fundamental set times [0,1] covers modulo the action. Its quotient is the mapping torus with (x,1) identified with (f₀(x),0), so this is the required covering action for Γ = H ⋊φ Z. In particular Y is a 3-manifold, homeomorphic to R³.

## 2. A compact ball with suspended boundary action

Fix o in X. In polar coordinates x = (R,θ) about o, set

    p(R) = log(log(e+R)),
    F(x,r) = (p(R) cos θ, p(R) sin θ, r) in R³.

At R = 0 the horizontal coordinates are zero. Since p is a homeomorphism [0,∞) → [0,∞), F is a homeomorphism Y → R³. Compactify by the map

    c(v) = v / (1+||v||).

The resulting pair (Ybar,B) is explicitly the closed 3-ball and its sphere. Therefore Ybar is a compact finite-dimensional Euclidean retract, and B is a Z-set: the homotopy z ↦ (1-u)z instantly pushes the closed ball into its interior for u > 0. The usual equivalence of this Z-set condition with homotopical negligibility in an ANR gives the exact form of the original definition.

The boundary is identified with suspension(C) by

    q(z,s) ↦ (sqrt(1-s²) z, s),      z in S¹, -1 ≤ s ≤ 1.

This is a continuous bijection from a compact space to a Hausdorff space, hence a homeomorphism. Its poles correspond to (0,0,±1).

For any fixed quasi-isometry a of X, its radial displacement R' = d(o,a x) satisfies affine upper and lower bounds in R. Elementary logarithm limits give

    p(R') / p(R) → 1 as R → ∞.

Both a deck transformation g and h have this property and continuous boundary maps. Thus, at a non-pole boundary point, their horizontal direction tends to g_C z or h_C z while the ratio of vertical to horizontal size is unchanged in the limit. Adding 1 to r also leaves the limit unchanged. Consequently the extended actions are

    g q(z,s) = q(g_C z,s),       t q(z,s) = q(h_C z,s).

Continuity at a pole requires its own check. A sequence tends to the positive pole precisely when its real coordinate tends to +∞ and its horizontal size p(R) is o(r). If R stays bounded, p(d(o,a x)) is bounded. If R tends to ∞, the displayed ratio tends to 1. These two observations, by taking subsequences if necessary, show that a fixed g or h preserves positive-pole convergence; shifting r by ±1 does also. The negative pole is identical with the sign reversed. Apply the argument to inverses as well. Hence these extensions are homeomorphisms of the entire compact ball.

This verifies whole-group continuity, including poles, without assuming an inverse on X for a merely cellular homotopy equivalence. The two fixed poles are fixed by all g and t, hence by every element of Γ.

## 3. Nullity for every compact set

It remains to check the essential condition that naive product compactifications fail. Let K be any compact subset of X × R. Enclose it in A × [-T,T], with A nonempty and compact and T ≥ 1. Let D ≥ max(1,diam A) and M ≥ max(2,L). Every translate by g tᵏ lies in

    E × [k-T,k+T],       E = g hᵏ A,
    diam E ≤ Dₖ := D M^|k|.

Write a = min{d(o,x): x in E} and Qₖ = (D+1)² M^(2|k|). We show that the diameters of the images under cF tend to zero along any sequence of distinct group elements. It suffices to pass to subsequences with k bounded or |k| → ∞.

First suppose |k| → ∞. If a ≤ Qₖ, every x in E has d(o,x) ≤ Qₖ+Dₖ, so

    p(d(o,x)) ≤ p(Qₖ+Dₖ) = O(log(|k|+2)).

Since r lies in [k-T,k+T], the whole translated set converges uniformly to the pole with the sign of k (take a sign-constant subsequence). Thus its diameter tends to zero.

Now suppose a > Qₖ. Then Dₖ < sqrt(a), and a → ∞. For x,y in E, the difference between their p-radii is at most

    Dₖ / ((e+a) log(e+a)) ≤ Dₖ/a → 0,

by the derivative of p. The hyperbolic cosine law bounds the angular distance between their unit polar directions by

    C exp(Dₖ/2-a),

where C is independent of k, g, x, and y once a ≥ 1. Indeed,

    2 sinh(R_x) sinh(R_y) sin²(θ/2)
      = cosh d(x,y) - cosh(R_x-R_y)
      ≤ cosh Dₖ - 1.

It follows that the Euclidean diameter of the horizontal F-images is bounded by

    Dₖ/a + C p(a+Dₖ) exp(Dₖ/2-a),

which tends to zero, since Dₖ < sqrt(a). The vertical diameter is bounded by 2T. The minimum Euclidean norm of F on the translated set is at least |k|-T, and tends to ∞. Finally, for v,w in R³,

    ||c(v)-c(w)|| ≤ 2||v-w|| / (1+min(||v||,||w||)).

Therefore the compactification diameter tends to zero in this case also.

If k is bounded, pass to a constant-k subsequence. Distinct Γ elements then give distinct g in H, and the proper H action implies a → ∞. The horizontal diameter estimate just given applies with a fixed bound on Dₖ. Meanwhile the minimum F-norm is at least p(a), which tends to ∞. The same inequality for c proves shrinking diameter.

If nullity failed, infinitely many distinct translates would have a common positive lower bound on their compactification diameter. The preceding subsequence argument contradicts that. Thus every compact K has a null family of translates. This proves the missing axiom directly for all compact sets, rather than only for one fundamental tile.

## 4. Consequence and consistency checks

Thurston's mapping-torus hyperbolization theorem makes Γ a closed hyperbolic 3-manifold group. Its canonical boundary is the visual S², with minimal Γ action and no global fixed point. The just-constructed EZ action on S² has two global fixed points. An equivariant function would send either fixed pole to a global fixed point in the target, which is impossible. No continuity hypothesis on that function is needed.

The sphere identification also checks potential homological or local-dimensional objections. Every boundary point, poles included, has a 2-dimensional disk neighborhood. Its local integral homology is Z in degree 2 and zero in the other degrees; its reduced integral cohomology is Z in degree 2 and zero otherwise. This matches the dimension and cohomological constraints for a closed aspherical 3-manifold group. These facts concern the underlying space and do not impose minimality on its Γ action.

## References used

- Guilbault, Healy, Pietsch, *Group boundaries for semidirect products with Z*, Theorem 1.6 and section 7.1: https://doi.org/10.4171/GGD/750
- Thurston, *Hyperbolic Structures on 3-manifolds, II*, Theorem 0.1, Proposition 2.6, section 5, and page 3: https://arxiv.org/abs/math/9801045
- Kapovich, Benakli, *Boundaries of hyperbolic groups*, Proposition 4.2(2), for canonical minimality: https://arxiv.org/abs/math/0202286
- Guilbault, Moran, *Proper homotopy types and Z-boundaries of spaces admitting geometric group actions*, section 3, Remark 4, for the Z-set formulations: https://arxiv.org/abs/1707.07760

This verification is mathematical exposition, not a formal proof-assistant certificate. The finite control script does not certify hyperbolization, extension of quasi-isometries to the hyperbolic boundary, or analytic limits.
