# E-6322 final exact certification

16 October 2026. Fifth and final shared research pass. The coefficient family, admissible class, full smooth diffeomorphic traces, and boundary-inclusive conclusion remain exactly those in the frozen target.

**Status: unresolved after five passes.** This report independently certifies auxiliary comparison identities, a restricted critical-axis exclusion, and the precise scope of several negative controls. It supplies neither a determinant lower bound for every full-class global minimizer nor a compliant global-minimizer counterexample.

Throughout, a,b,c,d>0,

\[
W(F)=H(F)+dJ^{-2},\quad H(F)=a|F|^6+b|\operatorname{cof}F|^3+cJ^2,\quad J=\det F>0.
\]

## 1. Full mixed-minor comparison

Let y be a full-class global minimizer, and let v∈W¹,⁶ have the same full trace. Put F=Dy, G=Dv, J_v=det G and

\[
M_1=\operatorname{cof}F:G,\qquad M_2=\operatorname{cof}G:F.
\]

The exact cubic identity is

\[
J_t=\det((1-t)F+tG)
=(1-t)^3J+t(1-t)^2M_1+t^2(1-t)M_2+t^3J_v.
\]

Assume J_v,M₁,M₂≥0 a.e. Then J_t≥(1−t)³J>0 for 0<t<1, and y_t=(1−t)y+tv is an admissible finite-energy comparison even when v itself has infinite barrier energy. For 0<t≤1/2,

\[
\left(\frac{J_t^{-2}-J^{-2}}t\right)^+
\le J^{-2}\frac{(1-t)^{-6}-1}{t}
=J^{-2}\sum_{k=1}^6(1-t)^{-k}\le126J^{-2}.
\]

Its pointwise derivative at zero is

\[
6J^{-2}-2M_1J^{-3}.
\]

The positive density need not be convex along this full-matrix segment. That is unnecessary: since H is C¹ on all matrices and has degree six, its directional difference quotients are bounded in absolute value by C(|F|+|G|)⁶, which is integrable. Reverse Fatou applied to minimality therefore gives

\[
M_1J^{-3}\in L^1,\qquad
2d\int_\Omega M_1J^{-3}
\le\int_\Omega DH(F):(G-F)+6d\int_\Omega J^{-2}.
\]

When rank(G−F)≤1, the minors are affine along the segment and

\[
M_1=2J+J_v,\qquad M_2=J+2J_v.
\]

Substitution recovers exactly the earlier one-row comparison with source coefficient 2d∫J⁻².

### A minimizer-specific exclusion of the earlier radial repair obstruction

For the pass-4 radial map y=s(r)x, s=r¹ᐟ²[log(e/r)]^κ with 1/6<κ≤1/2, let q=3/2−κ/log(e/r). The principal stretches are sq,s,s and J=s³q. Choose v=id. All three endpoint mixed quantities are positive, and

\[
M_1=s^2(1+2q),\quad M_2=s(q+2),\quad
M_1J^{-3}=s^{-7}(1+2q)q^{-3}.
\]

The latter has radial integral comparable to

\[
\int_0 r^{-3/2}[\log(e/r)]^{-7\kappa}\,dr=\infty.
\]

Thus the mixed-moment necessary condition itself excludes this map from minimization. The pass-4 impossibility of a uniformly positive **one-component** repair for this map cannot be promoted to an obstruction to all minimizer comparisons. This is a substantive compatibility limitation, not a failure of the mixed comparison theorem.

The unproved step for arbitrary minimizers is the existence of useful competitors with the displayed mixed-minor signs and a favorable first positive-density cost. A smooth prescribed trace extension does not supply those signs automatically.

## 2. Exact cost threshold for compensated inverse repairs

Let v be an actual inverse minimizer, H=Dv, K=det H, and

\[
V(H)=X(H)+dK^3,\qquad
X(H)=a|\operatorname{cof}H|^6/K^5+b|H|^3/K^2+c/K.
\]

Assume a rank-one endpoint difference H_e−H is furnished by a proved admissible inverse comparison mechanism, with finite segments for t<1 and the domination needed to differentiate at zero. Set K_e=det H_e. The controlled relative-minor hypotheses in pass 4 are one sufficient mechanism, not an automatic property.

Suppose K−K_e=q≥0 on a donor set A, K_e−K=p≥0 on a recipient set B, and the difference is zero elsewhere. Determinant conservation and affine determinant interpolation give

\[
\int_Aq=\int_Bp=m.
\]

Indeed, any admissible t∈(0,1) has ∫K_t=|Ω|=∫K, so K_t=(1−t)K+tK_e already forces ∫K_e=∫K, without requiring an admissible endpoint.

If m>0, K≥λ on A, and K≤κ on B, differentiated minimality yields

\[
3d(\lambda^2-\kappa^2)m
\le3d\left[\int_AK^2q-\int_BK^2p\right]
\le\int_D DX(H):(H_e-H).
\]

Consequently, a family of repairs with cost at most C₀m would forbid levels

\[
\lambda>\sqrt{\kappa^2+C_0/(3d)}.
\]

The conditional conclusion requires one κ and one C₀ uniform across high levels, and a repair with m>0 whenever the chosen high-level donor has positive measure. None of those existence/cost hypotheses has been established for arbitrary minimizers. The estimate isolates the needed cost per transferred volume; it does not construct the repair.

### Why baseline energy does not estimate the cost of every chosen repair

In an interior cube let w(x)=A(x₁)b(x₂,x₃) be smooth, compactly supported, nonzero, and choose ε small enough that |ε∂₁w|≤1/2. Set

\[
\xi_N=-\varepsilon w\sin(Nx_2)e_1,\qquad
 y_N=id+(\delta/N)w\sin(Nx_2)e_1.
\]

The maps id+tξ_N are genuine smooth triangular diffeomorphisms for 0≤t≤1: their Jacobians are 1−tε∂₁w sin(Nx₂)≥1/2, and they equal id outside the cube. The y_N have uniformly bounded energy and J_N→1 uniformly, while

\[
Dy_N=I+s_N e_1\otimes e_2+O(N^{-1}),\qquad s_N=\delta w\cos(Nx_2).
\]

For the pure shear F=I+s e₁⊗e₂, with E₊=H(F)I−FᵀDH(F),

\[
(E_+)_{12}=-[6a(3+s^2)^2+3b\sqrt{3+s^2}]s.
\]

Thus

\[
\int E_+(Dy_N):D\xi_N\ge cN-C.
\]

The O(N⁻¹) gradient error gives only an O(1) contribution against Dξ_N=O(N), and the leading cos² integral has a strictly positive limit. By contrast the barrier inner-variation term is bounded because div ξ_N is bounded and J_N is uniformly positive. This also diagnoses nonstationarity of y_N. They are **nonminimizers** with identity trace. The example excludes a universal baseline-energy estimate for this chosen oscillatory repair, while leaving minimizer-specific repair estimates open.

At the actual identity minimizer, the same smooth triangular map φ_N=id+ξ_N also produces a genuine finite comparison y_t=φ_N⁻¹ for t=1. Its determinant density is uniformly bounded above and below, but its energy cost grows at least cN⁶−C. Indeed, for A=I+e₁⊗g with g=∇ξ_{N,1},

\[
\det A=1+g_1,\qquad
\operatorname{cof}A=\begin{pmatrix}1&0&0\\-g_2&1+g_1&0\\-g_3&0&1+g_1\end{pmatrix},
\]

and the transformed sixth-power contribution is a|cof A|⁶/(1+g₁)⁵. Here g₂ has size N on a fixed positive-measure oscillatory set, while 1+g₁∈[1/2,3/2]. Thus determinant-density control alone does not bound the finite cost of every prescribed repair even when the baseline is a true minimizer. This is not a lower bound on the cost of the best repair, and its first variation at identity remains zero.

## 3. Complete classification of universally orientation-safe graph derivatives

For fixed real 3×3 matrices A,B, consider

\[
\det(A+BH)>0\quad\text{for every }H\in GL^+(3).
\]

This holds **if and only if** exactly one of the following occurs:

1. A=0 and det B>0;
2. B=0 and det A>0.

Sufficiency is immediate. If B is invertible and A≠0, choose u with B⁻¹Au≠0. An orientation-preserving isomorphism H can send u to −B⁻¹Au: complete the source and target nonzero vectors to equally oriented bases. Then (A+BH)u=0, contradicting strict positivity. Thus invertible B forces A=0 and then det B>0.

It remains to exclude rank B=r∈{1,2}. Orientation-preserving orthogonal changes put B=diag(σ₁,…,σ_r,0,…,0), with each σ_i>0. The bottom 3−r rows of A must be independent; otherwise every A+BH is singular. Choose an r-frame Q completing those fixed bottom rows to a basis. Its sign can be chosen so that det[diag(σ_i)Q;A_bottom]<0. The first r rows of a positive-determinant H may be any independent frame, because the remaining rows can always be chosen to complete it with positive orientation. Take the first r rows to be tQ and fix such a completion. Then det H>0 for all t>0, whereas the leading t^r coefficient of det(A+BH) is negative. For large t its determinant is negative. This contradiction proves the classification.

Explicit controls include A=I and B=diag(1,0,0) with H=diag(−2,−1,1), producing determinant −1; and A=I, B=diag(1,1,0), H=diag(−2,1,−1), producing determinant −2. Both H have positive determinant.

For a smooth graph transformation u(z)=Φ(z,v(z)), its derivative has the form A+BH with A=D_zΦ and B=D_xΦ. If universal orientation safety is demanded at every (z,x) in a connected product domain, continuity prevents switching between the two classified branches. Under the strong collar condition Φ(z,x)=x for every x whenever z is in a target boundary collar, the material branch A=0 is selected. Independence of z and the collar values then force Φ(z,x)=x everywhere. Hence the only such **universally** safe graph recipe is the identity.

This is a matrix-universal restriction. It does not prohibit maps tailored to the actual H=Dv of one minimizer, and does not decide whether any particular nonuniversal cutoff has finite dual energy.

## 4. A repaired critical-axis family still fails stationarity

Let ρ²=x₁²+x₂², r²=ρ²+z² and

\[
y_\perp=r^{m-1}x_\perp,\qquad
 y_3=z\rho^2r^{\beta-3}+zr^{\beta+\delta-1},
\]

where m>1/2, β>2m, γ=2m+β−3>0 and δ>0. Put t=z²/r². Exact cylindrical differentiation gives

\[
J=r^\gamma\left\{(1-t)[m+(\beta-3m)t]
+r^\delta[m(1-t)+(\beta+\delta)t]\right\}.
\]

The assumptions imply J≈r^γ(sin²θ+r^δ)>0 off zero. The positive energy is integrable since the first two rows scale like r^(m−1), the third has higher degree, and 6m−3>0. Near either pole, the angular area measure is comparable to θdθ, and

\[
\int_0^{c}\frac{\theta\,d\theta}{(\theta^2+\varepsilon)^2}
=\frac1{2\varepsilon}-\frac1{2(c^2+\varepsilon)}\asymp\varepsilon^{-1}.
\]

Thus the barrier is integrable exactly when 2γ+δ<3. The full boundary trace is the permitted smooth global diffeomorphism

\[
G(x_1,x_2,z)=(x_1,x_2,z(1+\rho^2)),\qquad \det DG=1+\rho^2.
\]

The leading weighted profile U has a critical axis: U vanishes on that axis and its leading determinant vanishes there. Thus the previous nondegenerate angular-tangent theorem does not apply directly. Nevertheless its third-row stress exponent gap is η=4γ>0, so stationarity of the original map would force the limiting barrier-only equation on every open patch ρ>0.

Since div(cof DU)₃=0, this equation says that J_U is constant along the fibers of (U₁,U₂). Fix a nonzero target cylindrical radius q=ρr^(m−1). Direct substitution gives

\[
J_U=q^2\left[(\beta-2m)r^{\beta-3}
 -(\beta-3m)q^2r^{\beta-2m-3}\right].
\]

On a nonconstant open fiber, the two differentiated powers are distinct because m>0. Constancy requires

\[
(\beta-2m)(\beta-3)=0,\qquad
(\beta-3m)(\beta-2m-3)=0.
\]

The assumption β>2m forces β=3 from the first equation, and the second then forces m=1. This gives γ=2, incompatible with the finite-energy inequality 2γ+δ<3. Hence no map in this repaired family with the stated finite-energy parameters is stationary, let alone a minimizer.

For the concrete choice m=3/4, β=9/4, δ=1/4, one has γ=3/4 and 2γ+δ=7/4<3. It is an admissible smooth-trace example, but the leading fiber derivative is already −(9/16)q²r^−7/4, so the nonstationarity is explicit. This excludes this family only; it is not a theorem classifying all angularly degenerate tangents.

## 5. Balanced full-system tangents exclude angular zeros

Let sorted positive weights α₁=m≤α₂≤α₃ satisfy s=Σα_i>3 and the balance relation s+3m=6. Suppose componentwise weighted rescalings of a local minimizer converge strongly in W¹,∞ on a fixed annulus to U_i(z)=|z|^(α_i)φ_i(z/|z|), with C² angular profile and det DU nonnegative and not identically zero. Put

\[
L_r=\operatorname{diag}(r^{\alpha_i-m}),\qquad
\Pi=\operatorname{diag}(\mathbf1_{\{\alpha_i=m\}}).
\]

Since H is homogeneous of degree six and 12−2(s+3m)=0,

\[
r^{-6(m-1)}W(\operatorname{diag}(r^{\alpha_i-1})P)
=H(L_rP)+d(\det P)^{-2}.
\]

The normalized positive density converges in C² on bounded matrix sets to H₀(P)=H(ΠP). This density is C² on all matrices, including rank-deficient ones; the function |cof P|³ is C² at zero. On any compact patch where det DU>0, strong gradient convergence makes the approximating gradients uniformly bounded and uniformly positive in determinant. Full additive first variations are therefore legitimate there. In physical variables the componentwise variation has amplitude r_k^(α_i)φ_i, so it becomes an arbitrary full-vector variation of the rescaled map. No component equation is lost by normalization.

Passing the weak stresses gives

\[
\operatorname{div}\{DH_0(DU)-2d(\det DU)^{-3}\operatorname{cof}DU\}=0
\]

on every positive-determinant patch. Write F=DU,J=det DU. Piola and Fᵀcof F=JI imply

\[
\nabla(J^{-2})=\frac1{3d}F^T\operatorname{div}DH_0(F).
\]

The right side is uniformly bounded on the closed annulus because U is C² and H₀ is globally C², regardless of whether J approaches zero. A segment beginning in {J>0} and ending at its first zero would force J⁻² to diverge along a finite-length interval while its derivative stays bounded, a contradiction. By polygonal continuation in the connected annulus, the nonempty positive set therefore fills the annulus.

Now m<1 and α₃>m, so H₀ is independent of the third row. The resulting third equation is the barrier-only equation. The earlier positive-angular-Jacobian ray argument excludes this homogeneous profile because its Jacobian degree s−3 is positive. Thus such a balanced tangent is impossible even without assuming strict angular positivity in advance.

This improves the controlled-profile exclusion only. It does not establish strong W¹,∞ annular tangents, the balance relation, a nontrivial limiting determinant, or a C² profile for arbitrary minimizers. A limit whose determinant vanishes identically is not covered.

### Subcritical extension with a dense positive set

A further narrow extension applies when s+3m<6, α₂>m, and the same strong W¹,∞ annular tangent has a C² homogeneous profile with J≥0 nontrivial and {J>0} dense. The first-row positive strain term dominates on each positive patch: its other relative stress exponents are 2(α₂−m), 3(α₂−m), 2s−6m and 2(6−s−3m), all strictly positive. Hence U₁ is scalar 6-harmonic on the positive patches. Its scalar divergence is continuous because U is C²; density extends the equation to the entire annulus.

The earlier homogeneous scalar argument excludes m<3/5 and 3/5<m<1. At the remaining critical value m=3/5, the spherical energy identity forces φ₁=c constant. Then

\[
j(\theta)=cm\,\theta\cdot(\nabla_{S^2}\phi_2\times\nabla_{S^2}\phi_3),
\qquad
\int_{S^2}j=cm\int_{S^2}d\phi_2\wedge d\phi_3
=cm\int_{S^2}d(\phi_2d\phi_3)=0.
\]

Stokes on the closed sphere contradicts continuous j≥0 nontrivial. This critical step does not assume positive degree. The density of the positive set is essential to the stated argument; it supplies no equation on an open zero-determinant region otherwise.

## 6. Pressure-modulus endpoint calculations

The positivity lane's conditional pressure argument compares a Jacobian-zero lower blow-up with pressure mean oscillations. The relevant modulus expression is

\[
\omega(r)^2\left[1+\int_r^R\frac{\omega(t)}t\,dt\right].
\]

For ω(r)=[log(e/r)]^−α and 0<α<1, its leading order is [log(e/r)]^(1−3α). It tends to zero when α>1/3. At α=1 the expression is O(L^−2 log L), and for α>1 it is O(L^−2α), where L=log(e/r). These computations verify the logarithmic exponent in that conditional criterion, not a modulus for actual minimizers.

The scalar pressure equation alone does not force bounded pressure at α=1/3. On a ball let

\[
p(r)=L(r)^{2/3},\qquad
q(r)=r^{-2}\int_0^r\tfrac23sL(s)^{-1/3}\,ds,\qquad Q=q(r)n\otimes n.
\]

Then q′+2q/r=−p′, so div(pI+Q)=0 off zero. Its small-sphere flux is O(r²L^(2/3))→0, proving the same equation distributionally across zero. L'Hôpital gives q∼(1/3)L^−1/3. The tensor Q is continuous, with modulus O([log(e/h)]^−1/3), while p is unbounded but has every finite Lebesgue moment. The formal determinant p^−1/2=L^−1/3 has the same critical logarithmic modulus.

This is an **abstract tensor-pressure example**. No deformation gradient producing this Q through the constitutive law is supplied. It certifies a limitation of the scalar pressure/modulus argument only.

## 7. Terminal unresolved flags

1. No proof gives the required global essential positive Jacobian bound for every coefficient choice, smooth domain, permitted nonaffine trace and full-class global minimizer. No actual such minimizer with essential infimum zero has been constructed.
2. No unconditional gradient modulus, uniform Dini estimate, or logarithmic modulus above the conditional threshold has been obtained for all minimizers. Conditional regularity results cannot supply their own hypotheses.
3. The mixed-minor comparison needs compatible endpoints with nonnegative mixed minors and useful positive-density cost. The fixed trace extension does not guarantee those properties.
4. Compensated inverse repair needs an actual admissible family with uniformly controlled cost per transferred volume. The exact threshold estimate does not establish existence or the uniform cost.
5. Structured natural-exponent graph comparisons have a proved transported inverse-class mechanism conditional on finite energy. Generic arbitrary W¹,⁹/⁵ additions and the associated minor-identification/closure step remain unresolved; no general claim is imported from matrix growth alone.
6. Exact weighted cores, nondegenerate C¹ annular tangents, the displayed repaired critical-axis family, balanced strong W¹,∞ tangents with C² profile and nontrivial determinant, and the stated unique-minimum subcritical tangents with dense positive set are excluded. Neither existence of those tangents for arbitrary minimizers nor exclusion of all angularly degenerate, irregular or boundary-only degenerations has been proved.
7. The singular admissible maps and the signed oscillatory stress sequence are explicitly nonminimizing or nonstationary. Affine-blend failures demonstrate inadmissibility of particular comparison paths. The genuine identity-minimizer example instead demonstrates the high finite cost of one chosen admissible comparison; it does not exclude better repairs or violate its positive Jacobian bound. The abstract pressure example is nonconstitutive, and the universal graph obstruction is quantified over all matrices. None falsifies E-6322.
8. Symbolic identities, finite quadratures and sample checks do not establish full-class global minimality, an unproved compactness theorem or a universal regularity estimate.

## 8. Reproduction and sealed earlier passes

Run `python research_elasticity_1791_pass5_20261016/exact/verify_final.py` from the workspace root. The script verifies the new exact identities, checks the recorded SHA-256 hashes of all twelve pass-1–4 exact artifacts, and reruns all four earlier scripts in temporary directories. It requires byte-identical verification output and never modifies the earlier sealed files. Its local output is `verification.json`.

The earlier scripts contain 150 exact symbolic checks and 14 quadrature comparisons, plus explicitly labeled finite boundary samples. These auxiliary checks are not independent proof instances of the benchmark. The fifth-pass count and complete reproducibility result are recorded in the output manifest. The current run has 51 new exact checks, bringing the five-pass exact-check total to 201; the separate 14 quadrature comparisons are unchanged.
