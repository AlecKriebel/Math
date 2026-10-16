# E-6322 pass 1: legitimate variations, inverse coordinates, and truncation bottlenecks

Date: 2026-10-16. Scope: the exact frozen target in `recovery_elasticity_1791_20261015/formulation_gate/RESEARCH_TARGET.md`. This note supplies necessary conditions and identifies incomplete routes. It does not prove or disprove E-6322.

## 1. Notation and exact stresses

Write F=Dy, C=cof F, J=det F>0, h(J)=cJ²+dJ⁻², and

W(F)=a|F|⁶+b|C|³+cJ²+dJ⁻².

All matrix norms and inner products below are Frobenius. Let P(F)=DW(F), pointwise on GL⁺(3). The two multiplicative stress contractions are

T(F)=P(F)Fᵀ
=6a|F|⁴FFᵀ+3b|C|(|C|²I−CCᵀ)+(2cJ²−2dJ⁻²)I,

U(F)=FᵀP(F)
=6a|F|⁴FᵀF+3b|C|(|C|²I−CᵀC)+(2cJ²−2dJ⁻²)I.

The energy-momentum tensor is

E(F)=W(F)I−U(F)
=[a|F|⁶−2b|C|³−cJ²+3dJ⁻²]I−6a|F|⁴FᵀF+3b|C|CᵀC.

Derivation: for a left multiplier L=I+tH,

cof(LF)=cof L C,
(d/dt)|₀ cof L=(tr H)I−Hᵀ,
(d/dt)|₀ det L=tr H.

For a right multiplier, cof(FL)=C cof L. These identities give T and U directly, without integrating P by itself.

The bounds |FFᵀ|≤|F|² and |CCᵀ|≤|C|² give, for example,

|T(F)|≤9W(F), |U(F)|≤9W(F), |E(F)|≤12W(F).

Thus T(Dy), U(Dy), E(Dy) lie in L¹ for every admissible y. Positivity of the coefficients is used here and throughout; the constants above work for arbitrary positive coefficients.

## 2. Outer variations are justified in the full admissible class

Let ψ∈C¹_b(R³;R³) have bounded derivative and satisfy ψ(g)=0 on ∂Ω. Compactly supported smooth ψ with this property suffice. For |t|‖Dψ‖∞<1, Ψ_t=Id+tψ is a global orientation-preserving bi-Lipschitz C¹ diffeomorphism. Set y_t=Ψ_t∘y.

Then y_t has exactly the prescribed trace, belongs to W¹,⁶, and

Dy_t=(I+tDψ(y))Dy,
J_t=det(I+tDψ(y))J>0 a.e.

Uniform upper and lower bounds on the multiplier and its determinant imply W(Dy_t)≤K W(Dy) for |t| in a fixed sufficiently small interval. Differentiating the explicit polynomial/power formula produces a difference-quotient domination by another constant times W(Dy). Consequently a global minimizer satisfies

∫Ω T(Dy):Dψ(y) dx=0.

No injectivity of y is needed. No lower bound on J and no L¹ bound on P are used. The exact finite comparison, for any orientation-preserving bi-Lipschitz C¹ target diffeomorphism Ψ fixing the trace pointwise, is

I(y)≤∫Ω [a|A(y)F|⁶+b|cof A(y) C|³+cJ²(det A(y))²+dJ⁻²(det A(y))⁻²] dx,

where A=DΨ. The right-hand side is finite whenever A, A⁻¹ are uniformly bounded on the relevant compact image.

## 3. Inner variations are justified in the full admissible class

Let η∈C¹_c(Ω;R³), φ_t=Id+tη, and y_t=y∘φ_t⁻¹. Extend η by zero outside Ω. For small |t|, φ_t is an orientation-preserving bi-Lipschitz C¹ diffeomorphism of Ω, equal to the identity near its boundary. Composition preserves the full admissible class and trace.

With A=Dφ_t(x), k=det A, change variables from φ_t(x) back to x. Since cof(FA⁻¹)=CAᵀ/k,

I(y_t)=∫Ω [a k|FA⁻¹|⁶+b k⁻²|CAᵀ|³+cJ²/k+dJ⁻²k³] dx.

This is an exact formula. All four terms and their t derivatives are bounded by a fixed multiple of W(F) for small |t|. Minimality gives

∫Ω E(Dy):Dη dx=0.

Again this requires neither topological nor a.e. injectivity of y. The same finite comparison formula holds for every orientation-preserving bi-Lipschitz C¹ material diffeomorphism φ:Ω→Ω which is the identity on the boundary and for which the composition is well-defined; being the identity near the boundary is a convenient sufficient condition.

The identities are concrete instances of Ball (2002), Theorem 2.3, but the calculations and domination above independently verify its stress-growth hypotheses for this exact density.

## 4. What the identities actually control

Let

Q(F)=[a|F|⁶−2b|C|³−cJ²]I−6a|F|⁴FᵀF+3b|C|CᵀC.

Inner stationarity says

∇(3dJ⁻²)=−div Q(Dy)

in distributions, with Q(Dy)∈L¹. The equation by itself is a pressure equation with an L¹ tensor source. Recovering its scalar term through singular integrals does not produce an L∞ bound from an L¹ bound. A proof would have to exploit further special structure of Q or obtain genuinely stronger estimates; none is supplied by this calculation.

Finite energy alone gives

|{x∈Ω:J(x)<ε}|≤ε² I(y)/d.

This measures small-determinant sets but does not make any of them empty. The target conclusion is precisely an eventual empty-set statement up to null sets.

The usual additive weak equilibrium is not justified merely by these formulas. The barrier part of P is

P_barrier(F)=−2dJ⁻³ C.

Its L¹ norm is not controlled by ∫(|F|⁶+|C|³+J²+J⁻²). Outer/inner variations avoid this missing estimate by multiplying P by F or Fᵀ before integrating.

## 5. Explicit finite-energy example with nonintegrable ordinary stress

On B(0,1), set y(x)=|x|^β x, with 3/7≤β<1/2. This has identity boundary trace, is continuous and belongs to W¹,∞, and is an orientation-preserving homeomorphism. For r=|x|>0 the radial and tangential eigenvalues of Dy are (1+β)r^β and r^β. Therefore

J=(1+β)r^(3β),
|Dy|⁶=O(r^(6β)),
|cof Dy|³=O(r^(6β)),
J²=O(r^(6β)),
J⁻²=(1+β)⁻²r^(−6β).

The last expression is integrable in dimension three exactly when β<1/2. The barrier Piola stress has size comparable to r^(−7β); its integral diverges for β≥3/7. The positive-power parts of P are O(r^(5β)), so there is no cancellation repairing |P|∈L¹.

This is NOT a minimizer: affine boundary data have the affine map as the unique global minimizer by strict convexity in F in the polyconvex representation and the null-Lagrangian identities. Its sole purpose here is to show that an L¹ Piola-stress hypothesis cannot be inferred from membership in the full admissible class. It is not a counterexample to E-6322.

## 6. Full-class finite energy does not imply homeomorphism

This construction deliberately concerns topological injectivity, not a.e. injectivity. It is compatible with the degree-one a.e.-injectivity result for these trace data.

Take Ω=B(0,3), write x=(x₁,x₂,z), r=(x₁²+x₂²)^(1/2). Choose h₀∈C∞(R) nondecreasing, h₀(z)=0 for |z|≤1/2, h₀(z)=z for |z|≥1, and h₀′≥0. Such h₀ exists by choosing a smooth nonnegative derivative on (1/2,1) whose integral is 1 and which equals 1 near 1, then extending oddly. Choose 2/3<α<1 and s:[0,∞)→[0,1] continuous, smooth away from zero, equal to r^α near zero, equal to 1 for r≥1, and positive for r>0. Define

y(x₁,x₂,z)=(x₁,x₂,h₀(z)+s(r)[z−h₀(z)]).

This equals the identity outside the compact cylinder r<1, |z|<1, hence near ∂B(0,3). Its derivative has the triangular form

F = [[1,0,0],[0,1,0],[u,v,J]],

where u and v are the transverse derivatives of the third component and

J=(1−s(r))h₀′(z)+s(r)≥s(r)>0 for r>0.

Since |u|+|v|≤K r^(α−1) near the axis and J is bounded,

|F|≤K(1+r^(α−1)).

In cylindrical measure r dr dθ dz, |F|⁶ is integrable because 6(α−1)+1>−1, equivalently α>2/3. The same direct derivative estimate proves the displayed function belongs to W¹,⁶, including across the measure-zero axis. Also J⁻²≤s(r)⁻² is integrable because 1−2α>−1, equivalently α<1. The cofactor-cubic term is integrable by W¹,⁶ (and directly here), and J² is bounded. Thus y is admissible for every positive a,b,c,d.

Nevertheless y(0,0,z)=(0,0,0) for |z|≤1/2: an entire interior segment collapses. In every cylinder around a positive-length subsegment, J=r^α near the axis, so ess inf J=0.

Again this is NOT a minimizer, since the boundary data are affine. It rules out treating every admissible deformation as a topological homeomorphism and shows why a classical inverse-map argument needs an additional theorem. Collapsing a null set does not contradict a.e. injectivity or the area formula.

## 7. Inverse-coordinate algebra: what it does and does not establish

Suppose an independent degree/area-formula argument supplies an a.e. inverse v on D=G(Ω), so that the ordinary change-of-variables identity is valid. Define the measurable matrix field

H(z)=[Dy(v(z))]⁻¹, K(z)=det H(z)=1/J(v(z)).

This definition alone does NOT assert that v is a Sobolev map with weak derivative H. Algebra and change of variables give

I(y)=∫D V(H) dz,

V(H)=a|cof H|⁶/K⁵+b|H|³/K²+c/K+dK³, K>0.

The first two terms are perspective convex functions of (cof H,K) and (H,K), respectively; the last two are convex in K. Thus this transformed formula has a polyconvex representation.

Hölder's inequality yields

∫D |H|^(9/5) dz ≤ [∫D |H|³/K² dz]^(3/5) [∫D K³ dz]^(2/5),

∫D |cof H|^(9/4) dz ≤ [∫D |cof H|⁶/K⁵ dz]^(3/8) [∫D K³ dz]^(5/8),

and K∈L³(D). The inverse-gradient exponent supplied by this direct estimate is 9/5, below the dimension 3. Even after separately proving that H=Dv weakly, these bounds supply neither continuity of v nor an L∞ bound on det Dv. The desired lower bound for J would become an upper L∞ bound for K. No such estimate is established here.

Do not silently replace the original minimization class by a class of inverse homeomorphisms, or claim that the formula alone transfers minimality to every finite-energy map for V.

## 8. Why the attempted truncations do not close the proof

1. Pointwise determinant replacement is not a deformation. Replacing J by max(J,ε) in a formula does not construct any gradient field Dz, preserve its minors, or meet the boundary trace. Pointwise changes to singular values have the same compatibility problem.

2. Interpolation with the smooth extension need not preserve orientation. Even F=diag(−1,−1,1) and A=I have positive determinants, while (F+A)/2 has determinant zero. For rough F with no lower determinant bound, there is no uniform small interpolation parameter justified by pointwise openness of GL⁺(3).

3. Additive test fields need a new admissibility argument. A sufficient pointwise condition is a uniform bound on Dϕ F⁻¹ for y+tϕ, which is not part of the target hypotheses. Selecting a rank-one direction from the local cofactor does not automatically produce a gradient-compatible perturbation.

4. A material diffeomorphism redistributes determinant only through its own Jacobian and distorts F and C simultaneously. The exact comparison in Section 3 shows all three effects. A scalar Jacobian prescription needs a constructed admissible diffeomorphism and quantitative distortion estimates strong enough to pay for the positive-power energy. These have not been obtained from the measurable field J and L¹ energy density.

5. The corresponding infinitesimal idea, choosing div η to detect {J<ε}, leaves Dη in the positive-energy terms. Standard finite-exponent divergence estimates do not turn an L¹ coefficient bound into the uniform product estimates required for a truncation iteration. It is invalid to assume that an arbitrary bounded divergence datum has a solution with the needed uniformly controlled Dη for this purpose.

6. Outer diffeomorphisms are equally legitimate but do not independently control a material point's determinant without controlling how the target-space test field and its derivative pull back through y. Even a.e. invertibility does not make arbitrary measurable determinant-dependent tests C¹ or produce the required domination.

## 9. Precise pass outcome

Established: full-class inner and outer stationarity, their exact stress tensors and finite comparison formulas, energy domination of multiplicative stresses, the distinction from ordinary additive equilibrium, and two explicit admissible-map obstructions to unjustified regularity/inverse assumptions.

Not established: an estimate eliminating low-J sets for a minimizer; a legitimate determinant-truncation comparison with the required cost; unconditional regularity of minimizers; a whole-domain essential Jacobian lower bound; or a compliant minimizer counterexample.

Primary source checked for contextual comparison: J. M. Ball, *Some Open Problems in Elasticity* (2002), §2.4, Proposition 2.2 and Theorem 2.3, pp. 11–13. Public URL: https://people.maths.ox.ac.uk/ball/Articles%20in%20Conference%20Proceedings%20and%20Books/JMB%202002%20re%20Marsden%2060th.pdf . The results in this note are directly derived; the source's general positivity problem is not cited as resolving this particular frozen law.
