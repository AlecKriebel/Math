# Independent source-only derivations and controls

These eleven groups were derived from the actual complete manuscript/PDF and general mathematical knowledge before source support code, archived research opinions/results, external mathematical bodies or current peer/root findings. They are checkable analytic deductions, not fresh executable or formal-proof evidence. No new priority or first-resolution claim is made.

## 1. Exact model and the two flatness notions

For a positive metric h, a torsion-free connection is statistical here when C=∇h is symmetric in all three entries. The dual is defined by Xh(Y,Z)=h(∇_X Y,Z)+h(Y,∇*_X Z). For the Levi–Civita connection ∇0, metric compatibility gives C=0 and ∇0*=∇0 by nondegeneracy of h. Thus a restriction excluding zero cubic tensor would be an additional hypothesis, to be checked against the actual printed question later rather than silently imposed.

The source's 1-conformal operation is (h,∇)↦(e^φh,∇−h⊗grad_h φ), not the Levi–Civita connection of the new metric in general. Its precise convention and its relation to the printed question are still foreign-primary interfaces to verify after the seal. In the present derivations that operation is taken literally, with R(X,Y)=∇_X∇_Y−∇_Y∇_X−∇_[X,Y].

## 2. All-center radial integrability without a global distance claim

Let U be a convex neighborhood on which the connecting affine geodesics depend smoothly on q. With initial endpoint p fixed and T=∂uγ, endpoint variation V gives

    dE_p(w)=∫h(∇_V T,T)du=∫h(∇_T V,T)du
            =[h(V,T)]₀¹−∫h(V,∇_T T)du=h_q(w,T(1)).

The equality of covariant derivatives uses zero torsion and commuting variation fields; the vanished integral uses affine parametrization. If T(1)=0, geodesic uniqueness for the zero terminal velocity makes the curve constant, hence q=p. Therefore for q≠p the covector is nonzero and dE_p(T(1))=h(T(1),T(1))>0. The radial hyperplane field is ker dE_p, with smooth regular level sets as local integral hypersurfaces. No transitivity of local leaves, completeness, global distance formula or foliation through the cut locus is assumed.

The argument holds for every center and every admitted convex U, not only a center on the flat factor. On a small product polar chart around p=(north pole,0), E_p=(θ²+t²)/2 and the one-form is θ dθ+t dt. This is an explicit first integral. At p the form vanishes and the hyperplane rank changes; excluding p is essential to the distribution as stated. The q≠p argument itself does not require a coordinate chart avoiding the sphere's polar singularity.

## 3. Curvature-change calculation, including quadratic terms

For ∇0 metric and B(X,Y)=−h(X,Y)V, V=grad_h φ,

    (∇_X B)(Y,Z)=−h(Y,Z)∇_X V,
    B(X,B(Y,Z))=h(Y,Z)h(X,V)V.

Subtracting the swapped terms gives

    Rhat(X,Y)Z=R(X,Y)Z−h(Y,Z)A(X)+h(X,Z)A(Y),
    A(X)=∇_X V−h(X,V)V.

Both derivative and B² terms are needed: omitting B² or reversing its sign gives a different A. Flatness requires the displayed algebraic form of R for some endomorphism A at each point. Allowing arbitrary A is a weaker requirement than the gradient/differential form above, so impossibility for arbitrary A suffices; no nonlinear PDE existence assertion has been substituted for the obstruction.

## 4. Pointwise characterization of that algebraic condition

For Levi–Civita curvature on an orthonormal basis, the proposed form yields R(e_i,e_j)e_j=Ae_i for i≠j. Skew-adjointness of R(e_i,e_j) gives h(Ae_i,e_j)=0. Hence A is diagonal in that basis. Pair symmetry of sectional curvature then gives A_ii=A_jj for every pair. Thus A=K I and the curvature must have the isotropic space-form tensor K(h(Y,Z)X−h(X,Z)Y) at that point. Conversely that tensor admits A=K I algebraically.

This is only a pointwise characterization, not an automatic solution of the differential equation for φ. In dimension two, every Riemannian curvature tensor has that form pointwise, so this algebraic test alone cannot establish 1-conformal flatness or its failure. The manuscript makes no dimension-two counterexample claim. For dimension one curvature is identically zero. For a flat Euclidean model A=0, φ constant is an actual flat-change control.

## 5. The product obstruction and a two-row exact certificate

For S²(1)×R^{n−2}, choose sphere vectors e1,e2 and one Euclidean vector e3 at an arbitrary point. Product curvature gives R(e1,e2)e2=e1 and R(e1,e3)e3=0. Both algebraic right sides would be A(e1). In coordinates these include A¹₁=1 and A¹₁=0; subtracting the two equations gives the exact contradiction 0=1. This is a two-row inconsistency certificate within the complete n²-unknown endomorphism system, before any symmetry/gradient restriction on A.

The same pair of curvature planes exists at every point and in every n≥3, proving nowhere-local failure and excluding every nonempty open subset. Adding Euclidean factors does not change either evaluation. Replacing the unit sphere by any nonzero constant-curvature factor with at least two tangent directions would give A(e1)=K e1 versus 0; the essential contrast is nonzero tangential versus zero mixed curvature, not a numerical accident of radius 1. This last observation is a check of the mechanism, not a proposed broader replacement theorem or follow-up.

## 6. Independent coordinate curvature check

In local coordinates (θ,ϕ,t), h0=dθ²+sin²θ dϕ²+dt². The only nonzero sphere Christoffel symbols are Γ^θ_{ϕϕ}=−sinθ cosθ and Γ^ϕ_{θϕ}=Γ^ϕ_{ϕθ}=cotθ. Direct calculation gives

    ∇_θ∇_ϕ∂ϕ=(sin²θ−cos²θ)∂θ,
    ∇_ϕ∇_θ∂ϕ=−cos²θ∂θ,
    R(∂θ,∂ϕ)∂ϕ=sin²θ∂θ.

Every t-mixed symbol vanishes. At θ=π/2 these coordinate vectors are orthonormal and the two target evaluations are exactly (e1,0). This independently fixes the curvature sign and scale used above. In dimension three Ric=diag(1,1,0), and the displayed projective-Weyl expression gives W(e3,e1)e1=−e3/2. That is an algebraic secondary check; the imported equivalence criterion is not needed by the direct proof and has not yet been read.

## 7. A control against confusing ordinary conformal flatness

The cylinder metric h0 is ordinarily conformally flat in dimension three: F(x,t)=e^t x maps S²×R onto R³\{0}, and F*δ=e^{2t}(g_{S²}+dt²). Nevertheless the Levi–Civita connection of e^{2t}h0 is

    ∇0_XY+dt(X)Y+dt(Y)X−h0(X,Y)∂t,

whereas the source's 1-conformal change with φ=2t is ∇0_XY−2h0(X,Y)∂t. They differ by essential terms. For the latter, A(X)=−4dt(X)∂t, so its sphere-plane curvature is still e1, not zero. An ordinary conformally Euclidean metric therefore does not falsify or prove the statistical flatness claim.

As an actual positive 1-conformal control, on a unit sphere choose a positive hemisphere height u=a·x. Its sphere gradient is a−ux and ∇_X grad u=−uX. For φ=−log u, A=I. The sphere curvature is the matching space-form tensor, so the curvature-change formula really produces Rhat=0 locally. The operation is not an impossible demand for every curved Riemannian structure; it excludes the anisotropic product here.

## 8. Non-self-dual structure: cubic and dual derived directly

For α=dt, h1=e^t h0 and ∇1=∇0+α(X)Y+α(Y)X, differentiation gives

    (∇1_X h1)(Y,Z)=−α(X)h1(Y,Z)−α(Y)h1(X,Z)−α(Z)h1(X,Y).

The tensor is fully symmetric, and C(∂t,∂t,∂t)=−3e^t never vanishes. Torsion is unchanged because the connection difference is symmetric. Solving the defining duality identity, rather than assuming a sign convention, gives

    (∇1)*_X Y=∇0_XY−h0(X,Y)∂t.

For example ∇1_∂t∂t=2∂t while its dual gives −∂t, confirming non-self-duality. These formulas also pass a parameter control: replace t by λt throughout. The cubic becomes −λ times the symmetric α⊗hλ sum, and the dual subtracts λh0⊗∂t. λ→0 returns the self-dual structure smoothly; λ≠0 gives nowhere-zero cubic tensor. Only λ=1 is needed for the original proposition.

## 9. Geodesic reparametrization and every convex neighborhood

For a ∇0-affine geodesic γ(u), a new parameter s satisfies the ∇1-affine equation precisely when s''(u)/s'(u)=2(t∘γ)'(u), so ds/du=C exp(2t(γ(u)))>0. On a compact segment this is finite and bounded away from zero, and may be normalized to s(0)=0,s(1)=1. The reverse conversion exists by the same positive derivative. Thus connecting paths in either model correspond bijectively inside any given U. Uniqueness and smooth endpoint dependence transfer in both directions, not just existence of some unparametrized curves.

For the product LC connection t(γ(u))=t_p+uΔt. Explicitly,

    s(u)=(exp(2Δt u)−1)/(exp(2Δt)−1),  if Δt≠0;
    s(u)=u, if Δt=0.

The inverse is log(1+s(exp(2Δt)−1))/(2Δt), with the smooth Δt=0 limit. Its derivative is strictly positive for either sign of Δt. At the terminal endpoint the velocity is scaled by c=(1−exp(−2Δt))/(2Δt)>0, again with limit 1. The radial one-form for (∇1,h1) is therefore e^{t(q)}c times dE0,p, and has the same kernel. Its leaves are supplied by E0,p, not by an unjustified metric-compatibility argument for ∇1. This covers every center and every admitted convex neighborhood; no global geodesic completeness is asserted.

## 10. All possible dual flattening changes reduce to the forbidden base changes

Since grad_{h1}ψ=e^{−t}grad_{h0}ψ, h1(X,Y)grad_{h1}ψ=h0(X,Y)grad_{h0}ψ. A 1-conformal change of the dual pair gives

    ∇hat=∇0−h0⊗grad_{h0}(t+ψ),
    hhat=e^{t+ψ}h0.

Every local ψ therefore yields exactly a base 1-conformal change with potential t+ψ. Conversely any local potential φ is obtained by ψ=φ−t. There is no unexamined subclass of possible flattening potentials. The base's pointwise impossibility excludes all of them at every point. The original proposition's nowhere-zero cubic and dual-nowhere-flat claims thus follow together, without appealing to the optional projective criterion.

## 11. Limits, falsifiability and remaining interfaces

The exact analytical checks support the full source theorem and non-self-dual proposition under the source's stated definitions. They do not yet authenticate the historical question's wording, whether it includes LC structures, the precise 1-conformal convention in Kurose, or Matsuzoe's credited formula/scale. Those are the decisive actual primary interfaces for the post-seal phase. A mismatch there must be documented as a full-original issue, not silently repaired by a new definition.

No global distribution is claimed at its center or across cut loci; no dimension-two classification, completeness, new curvature theory, priority certificate or first answer is established. The named unread historical sources and live database annotations are source assertions not independently checked here. Finite pointwise linear algebra could test the two-row obstruction and positive flat/space-form controls, but cannot prove every-center first variation or convex-neighborhood transfer. No source support code or expected results have been opened or run. Parent checkpoint hold begins immediately after the source-only seal.
