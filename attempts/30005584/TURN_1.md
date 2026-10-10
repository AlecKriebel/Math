# Turn 1: what a symmetry-degree comparison would actually require

Original target remains unresolved. This turn attacks the proposed transfer from the new cohomogeneity-one degree to the unrestricted Ricci-expander degree. It proves a precise conditional transfer statement and a proper equivariant **gradient-map counterexample** to transferring degree merely from symmetry, properness and an isolated symmetric fiber. The counterexample is finite dimensional; it is not a Ricci soliton or a counterexample to the original question.

## 1. The available geometric input and normalization

Rajan's published Theorem 1.1 computes a degree of absolute value one for the SO(3)×SO(2)-invariant family on S¹×R³. The local parameters are (a₀,−f₀), and the target coordinates are asymptotic slopes (a′∞,b′∞). Section 9's argument with these ordered coordinates gives degree −1, with the paper's degree convention stated up to sign. This must not be equated to the canonically normalized integer of Bamler–Chen without an orientation comparison.

Rajan uses Ric_g+Hess_g f+g=0, whereas Bamler–Chen use Ric_g+Hess_g f+(1/2)g=0. Put g_B=2g_R and f_B=f_R. Since a constant metric scaling leaves the Levi-Civita connection and the (0,2) Ricci tensor unchanged, the equations match. In arclength r_B=√2 r_R, the profiles satisfy a_B(r_B)=√2 a_R(r_B/√2), and similarly for b. Thus the limiting slopes, hence the link coordinates (a′∞,b′∞), are unchanged. Initial data transform by a₀,B=√2 a₀,R and f₀,B=f₀,R/2; both parameter scaling factors are positive, so they do not repair an orientation sign by themselves.

For the product link h=a²g_S¹+b²g_S², Scal_h=2/b². The four-dimensional cone has scalar curvature r⁻²(2/b²−6), so b≤1/√3 is precisely the nonnegative-scalar cone range. Bamler–Chen Lemma 3.19 then supplies nonnegative scalar curvature for a gradient AC soliton asymptotic to such a cone. Consequently, once a symmetric solution is placed in the exact AC moduli category, scalar curvature on the soliton is not an additional unidentified restriction over this range. The main unresolved transfer concerns all solutions, full regularity, and normal directions.

## 2. A finite-dimensional transfer lemma

Let a connected compact Lie group G act smoothly on oriented d-manifolds M,N, and let f:M→N be a G-equivariant C¹ proper map. The same proof works for a defined localized degree on a G-invariant neighborhood of the compact fiber, with the usual boundary exclusion and local properness hypotheses. Let y∈N^G be a **regular value of the full map**.

The fiber f⁻¹(y) is finite. Since G is connected, every orbit in this finite discrete fiber consists of one point. Thus every preimage belongs to M^G. The fixed-point loci are smooth submanifolds; one may use a G-invariant metric obtained by averaging and its exponential charts. At a preimage p, the isomorphism Df_p intertwines the representations on the tangent spaces. It restricts to an isomorphism on the invariant tangent subspaces T_pM^G→T_yN^G and on their invariant complementary normal spaces. For an integer fixed-locus degree, assume the relevant fixed-locus components are oriented, and orient their normal spaces so that the product orientations give the ambient orientations. Modulo 2 no such extra orientations are needed. Then

sign det(Df_p) = sign det(Df_p|fixed) · sign det(Df_p|normal).

It follows that the local/global ambient degree is the sum of the fixed-locus signs weighted by their normal signs. In particular:

1. Modulo 2 the ambient degree equals the degree of the entire fixed-locus map over y.
2. If all normal signs are +1, the integer degrees agree.
3. If all normal signs are one common sign, the integer degrees agree up to that sign.

The same statement is not valid upon replacing full regularity by regularity of f|M^G. The next example fails even modulo 2, and even though the full fixed-target fiber contains only one point and that point is fixed.

This elementary lemma is not automatically a theorem about the Bamler–Chen singular gradient locus. Applying it there requires an equivariant localized finite-dimensional reduction, compatible orientations, and identification of the whole fixed locus. Alternatively, at an actual full regular cone their Theorem 1.9 already gives the unrestricted index sum, as used in Section 4.

## 3. Proper equivariant gradient maps with different ambient and fixed degrees

Let V=Sym₀(3,R), the five-dimensional real space of trace-free symmetric 3×3 matrices, with the Frobenius inner product. SO(3) acts by conjugation. Define

q(A)=A²−(tr(A²)/3)I.

This is a smooth SO(3)-equivariant map V→V. It is the gradient on V of the cubic invariant function tr(A³)/3: its differential at A applied to a trace-free symmetric B is tr(A²B)=〈q(A),B〉.

Write s=tr(A²)=||A||². The Cayley–Hamilton identity for a trace-free 3×3 matrix is

A³−(s/2)A−det(A)I=0.

Multiplying by A and taking traces gives tr(A⁴)=s²/2. Therefore

||q(A)||²=tr(A⁴)−s²/3=s²/6=||A||⁴/6.

In particular q is proper, and q⁻¹(0)={0}. It is an even map on the odd-dimensional space V. The map τ(A)=−A has degree (−1)⁵=−1, while q∘τ=q. Multiplicativity of degree under proper composition gives deg(q)=−deg(q), hence

**deg(q)=0.**

Now use the actual symmetry group G=SO(3)×SO(2). Set

E=R²⊕V⊕R²,

where the first R² is trivial, SO(3) conjugates V, and SO(2) rotates the last R². This action is effective. Its fixed subspace is exactly the first R², because a conjugation-invariant symmetric matrix is scalar and trace zero, and the rotation representation has no nonzero fixed vector. Define

F(u,A,z)=(u,q(A),z).

This is a proper equivariant gradient map, with potential

Φ(u,A,z)=|u|²/2+tr(A³)/3+|z|²/2.

Its full degree is zero, by the same orientation-reversing symmetry (u,A,z)↦(u,−A,z). Its fixed-locus map is the identity R²→R², of degree one. For every fixed target (u₀,0,0), the entire fiber is the single fixed point (u₀,0,0). Nevertheless the derivative has the five-dimensional kernel V there, because Dq₀=0. Thus every target in the fixed slice is regular for the fixed map but critical for the full map.

This example simultaneously rules out the following general implications:

- Properness plus equivariance plus fixed-locus degree one implies nonzero full degree.
- The absence of nonsymmetric points in the chosen fiber suffices for equality of degrees.
- Sard's theorem for the ambient map supplies a regular value inside a prescribed symmetric target slice.
- Being a gradient map removes these obstructions.

It does not show that any of these failures occurs in Ricci-expander moduli. Rather it identifies a genuine hypothesis that a successful argument in that setting must prove.

An exact regular-point check illustrates the sign cancellation. In coordinates

A=[[a,c,d],[c,b,e],[d,e,−a−b]],

at A₀=diag(1,2,−3), the two-dimensional diagonal block of Dq has determinant −28/3, and the three off-diagonal factors are 3,−2,−1. Thus det(Dq_A₀)=−56, while det(Dq_(−A₀))=+56. Their images agree. The global degree proof above does not assume that these are the only preimages of that target.

Even if full regularity is imposed, fixed degree alone does not determine the **sign** of the ambient integer. On R²⊕R³⊕R² with the analogous effective SO(3)×SO(2) action, the maps (u,v,z)↦(u,v,z) and (u,v,z)↦(u,−v,z) are proper equivariant gradient diffeomorphisms. Both fixed maps have degree one; their ambient degrees are +1 and −1.

## 4. A precise conditional route back to the unrestricted expander problem

Let X=S¹×D³. To use the new restricted computation at a symmetric cone γ with nonnegative scalar curvature, the following are sufficient inputs:

(A) γ is regular for the **full** Bamler–Chen projection on the gradient/nonnegative-scalar locus, meaning every relevant full Einstein operator has zero kernel.

(B) The connected group G acts continuously on this compact fiber through its action at infinity, and the G-fixed fiber is identified bijectively with Rajan's parameter fiber. This includes proving that invariant solutions have the standard cohomogeneity-one action/profile, with no additional fixed components or inequivalent symmetry lifts, and verifying the AC gauge and normalization.

(C) The restricted parameter map is regular at that fiber and has the degree already computed by Rajan; in a valid equivariant reduction full regularity would imply restricted regularity. This implication should be established in the actual moduli model, not just borrowed from Section 2.

Under (A)–(C), the full fiber is finite by properness and regularity. Connectedness of G forces all its elements to be fixed. Bamler–Chen's mod-2 regular-value formula and Rajan's degree of absolute value one then yield

deg_exp(S¹×D³) ≡ 1 (mod 2).

This would already imply nonzero unrestricted degree and hence existence over every admissible cone by Bamler–Chen, but would not alone establish the exact integer 1.

For an integer identification, one must also compare normal orientations or normal negative-mode parity. If the full self-adjoint Einstein operator preserves a G-invariant decomposition and its negative eigenspace splits as E⁻_fixed⊕E⁻_normal, then

index_full = dim(E⁻_fixed)+dim(E⁻_normal).

Thus even normal negative multiplicity and a consistent comparison of the restricted orientation with the Bamler–Chen convention would suffice. It is not a consequence of G connectedness: SO(3) has the nontrivial real three-dimensional representation, so nontrivial normal representations need not have even dimension. The last linear example realizes precisely this odd-normal-sign phenomenon.

The dissertation's expectation that nonsymmetric solitons should make no net contribution does not provide (A), (B) or the needed normal information. Its p.66 statement explicitly leaves equality of the two degrees unproved. No result of this turn fills those analytic and geometric gaps.

## 5. Boundary connected sum and current status

No connected-sum law is established here. In particular, no multiplication or addition law follows from the existence of a degree, from a restricted ODE count, or from the elementary disjoint-union additivity of Brouwer degree. The target changes when links are joined by a neck, and the corresponding moduli spaces need a gluing/compactness analysis. That is a distinct unresolved part of the original target.

This is substantive author turn 1 of the allowed five if the original problem remains unresolved. The exact finite-dimensional obstruction, scalar/normalization reconciliation and conditional transfer criterion are partial results. They require independent review before any partial-result PR; no final unsolved outcome is being proposed at turn 1.
