# A Hopf-product counterexample to the weaker tautness formulation

Problem identifier: 2999 (KP-4.123). Date: 2026-10-06.

## Scope and conclusion

The two form conditions relevant to this problem are different. Write E for the tangent two-plane bundle of an oriented foliation of a closed oriented smooth four-manifold M.

- (W): a smooth two-form ω is positive on E, and dω(v,w,z)=0 whenever v,w lie in E and z lies in TM.
- (C): a smooth **closed** two-form Ω is positive on E.

Condition (W) is the condition printed in K3, Problem 4.123, Remark (1), page 292 [K3]. Condition (C) is the condition in the paragraph immediately preceding Question 7.12 in Kronheimer's original survey, author-PDF page 49 / printed page 47 [K98]. The original survey explicitly takes M to be closed. The construction below is closed as well, so does not depend on any ambient compactness omission in the abbreviated problem statement.

**Theorem.** There is a closed oriented smooth four-manifold with a smooth coorientable two-dimensional foliation satisfying (W), all of whose leaves are closed tori homologous to an embedded sphere. Consequently the genus-minimization statement with hypothesis (W), as literally printed, is false. The same example admits no form satisfying (C), and therefore is not a counterexample to Kronheimer's original closed-form question.

The counterexample uses the zero homology class. A variant explicitly restricted to nonzero homology classes is not refuted here. No novelty claim is made. This is an elementary formulation audit; it does not settle the original closed-form problem or the S²×S² subquestion.

## 1. The manifold and foliation

Let

M = S³ × S¹,

where S³ is the unit sphere in C² and S¹ is the unit circle in C. Let h:S³→CP¹ be the Hopf fibration, h(z₁,z₂)=[z₁:z₂], and let q=h∘pr₁:M→CP¹. This is a smooth submersion. Its connected fibers are

L_b = h⁻¹(b) × S¹ ≅ S¹ × S¹.

These fibers define a smooth nonsingular rank-two foliation F. Every leaf is embedded, compact, connected, and without boundary. The normal quotient TM/E is q*TCP¹, which is oriented. Thus F is coorientable. The product M is a closed oriented smooth four-manifold.

Use real coordinates (x₁,y₁,x₂,y₂) on C². The Hopf generator is

R = −y₁∂x₁ + x₁∂y₁ − y₂∂x₂ + x₂∂y₂.

On the S¹ factor use coordinates (u,v), u²+v²=1, and generator

T = −v∂u + u∂v.

Their commuting flows are the two circle actions, and E is spanned by R and T. Neither vector vanishes. Orient E by the ordered pair (R,T); choose the compatible total orientation, using the complex orientation on CP¹ for the quotient.

## 2. A globally defined form satisfying (W)

Define global forms by restricting the following ambient polynomial forms to the spheres and pulling them back to M:

α = x₁dy₁ − y₁dx₁ + x₂dy₂ − y₂dx₂,

η = u dv − v du,

ω = α∧η.

On S³, α(R)=1. On S¹, η(T)=1 and dη=0; also α(T)=η(R)=0. Hence

ω(R,T)=1,

so ω restricts to a positive area form on every leaf.

In ambient R⁴, put Q=x₁²+y₁²+x₂²+y₂². Then

dα = 2(dx₁∧dy₁ + dx₂∧dy₂),

i_R dα = −dQ.

Since dQ vanishes on TS³, the restriction satisfies i_R dα=0. Also i_T dα=0. On M we have dω=dα∧η. For every z∈TM,

dω(R,T,z) = −dα(R,z)η(T) = 0.

Every pair of vectors in E is a linear combination of R and T. Alternating bilinearity therefore gives dω(v,w,z)=0 for all v,w∈E and z∈TM. This proves (W) globally, not just near a selected leaf.

The form is not closed. At the point (x₁,y₁,x₂,y₂;u,v)=(1,0,0,0;1,0), the vectors U=∂x₂, V=∂y₂, T=∂v are tangent to M, and

dω(U,V,T)=2.

As a second geometric check, each Hopf fiber is a great circle in the round S³. In the product of the round metrics on S³ and S¹, each L_b is the product of two geodesics and is therefore totally geodesic, hence has zero mean curvature. Thus the construction also has the geometric minimality property associated with (W). Zero mean curvature is not being identified with homological area minimization.

## 3. An explicit lower-genus homologous surface

For b₀=[1:0], the Hopf fiber is C={(z₁,0):|z₁|=1}. It bounds the smooth embedded hemisphere

D = {(x₁,y₁,x₂,y₂)∈S³ : y₂=0, x₂≥0},

which is a two-disk with boundary C. Thus the compact embedded oriented three-manifold D×S¹ in M has boundary L_b₀=C×S¹, with a suitable orientation. In particular,

[L_b₀]=0 in H₂(M;Z).

This also follows from the integral Künneth theorem: H₂(S³×S¹;Z)=0. There is no torsion summand because the integral homology groups of both spheres are free abelian.

Choose a smooth coordinate four-ball in M, and inside it a small embedded three-ball B³ in a coordinate three-plane. Its boundary S=∂B³ is a smooth embedded two-sphere, and [S]=0. Consequently S and L_b₀ are integrally homologous. Their genera are

g(S)=0 < 1=g(L_b₀).

The leaf L_b₀ therefore is not smoothly genus-minimizing in its homology class. Both the competitor and the leaf are connected and oriented, so no convention concerning disconnected representatives or the empty surface is needed. The same argument applies to every fiber, either by unitary symmetry or by H₂(M;Z)=0.

## 4. Why this cannot answer the closed-form question

Suppose Ω were a closed two-form on M that were positive on E. The oriented leaf L_b₀ would have ∫L_b₀ Ω>0. But Stokes' theorem on D×S¹ gives

∫L_b₀ Ω = ∫D×S¹ dΩ = 0,

a contradiction. No alternative choice of a globally closed positive form can repair this example.

The obstruction is not merely that the particular ω in Section 2 is nonclosed. It proves that the entire foliation fails (C). Hence a claim that this construction refutes the original Question 7.12 would be invalid.

## 5. The remaining mathematical boundary

For a foliation satisfying (C), positivity can supply area calibration after a suitable metric choice, but an area comparison does not itself provide a genus inequality. If the positive closed form is additionally nondegenerate, the leaf is symplectic and the symplectic Thom theorem applies [OS00]. Existence of a symplectic form positive on the leaves is an additional hypothesis; it is not proved from (C) here.

The exact unresolved step is to derive a genus obstruction for an arbitrary (C)-foliation not already known to admit a compatible symplectic form, or to construct a counterexample that actually satisfies (C). Neither is supplied by the Hopf product. The literal K3 formulation must therefore be distinguished from the original problem before assigning a solved status.

## References

[K3] R. İ. Baykur, R. C. Kirby, D. Ruberman, K3: A New Problem List in Low-Dimensional Topology, author's preliminary version, Problem 4.123, p. 292. https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf

[K98] P. B. Kronheimer, Embedded surfaces and gauge theory in three and four dimensions, Surveys in Differential Geometry III (1998), 243–298; Question 7.12 and its preceding paragraph, author PDF p. 49 / printed p. 47. https://people.math.harvard.edu/~kronheim/jdg96.pdf

[OS00] P. Ozsváth and Z. Szabó, The symplectic Thom conjecture, Annals of Mathematics 151 (2000), 93–124, Theorem 1.1. https://doi.org/10.2307/121113 ; preprint: https://arxiv.org/abs/math/9811087
