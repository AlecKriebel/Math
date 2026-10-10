# Turn 5: uniform scalar coercivity and a local nonspherical Schur criterion

**Final substantive author turn; original target remains unsolved at 5/5.** The new result strengthens Turn 4's per-soliton scalar inverse bound to a uniform explicit bound across the symmetric family. It then bounds each nonspherical Schur error by a local potential. The remaining base-tensor inequality and the global degree comparison are not established. No boundary-connected-sum formula or unrestricted degree value is claimed.

## 1. Exact scalar identity from the soliton equation

Retain all geometric, weighted-domain and source hypotheses of Turns 3–4. Write the normalization temporarily as

Ric_g + Hess_g f + λg = 0,  λ>0,

g=a²dθ²+g_B,   g_B=dr²+b²g_S²,   B=R³.

The Bamler–Chen normalization is λ=1/2. Here a is positive and smooth on the entire base, including its origin; the circle does not collapse. Define

ℓ=log a,  F₁=f−ℓ,  dμ=a e^(−f)dvol_B,

A=a′/a,  H=−Δ_(F₁)+2|dℓ|².

The circle-circle component of the soliton equation is

−a⁻¹Δ_B a + a⁻¹〈df,da〉 + λ = 0.

Consequently

Δ_f^B a=λa,   Δ_(F₁)ℓ=λ.                         (1)

In radial variables this is also immediate from the actual ODE

A′=λ−A²−2AB+Af′,   B=b′/b,

since Δ_(F₁)ℓ=A′+(A+2B−f′)A. Thus (1) does not require an unproved bound on a″ or b″. Although B=b′/b is singular in radial notation at zero, (1) is an identity of smooth functions on the base, so it extends through zero.

For any real constant c and the smooth positive function w_c=a^(−c), the chain rule gives

(Hw_c)/w_c = cλ+(2−c²)|dℓ|².                     (2)

Taking c=√2 supplies an exact positive formal solution

w=a^(−√2),   Hw=√2 λ w.                          (3)

This is a positive supersolution/ground-state transform input; it is not asserted to be an L² eigenfunction.

## 2. Uniform coercivity on the actual weighted form domain

For compactly supported smooth q on B, the weighted integration-by-parts identity from (3) yields

∫(|dq|²+2|dℓ|²q²−√2 λq²)dμ
    = ∫w² |d(q/w)|²dμ ≥ 0.                      (4)

For completeness, write q=wv, expand |dq|², and combine the cross term with v²|dw|² as 〈dw,d(wv²)〉. Its integral is −∫(Δ_(F₁)w)wv²dμ. Equation (3) then gives (4). Compact support removes the boundary term, and smoothness and positivity of w at the origin preclude a fictitious inner boundary condition.

The scalar H is the Friedrichs operator of the closed form identified in Turn 4. Compactly supported smooth functions are a core. Passing to a core approximation proves

H ≥ √2 λ I,   ||H⁻¹|| ≤ 1/(√2 λ).               (5)

These constants are independent of the two initial parameters of the Rajan family. In the target normalization, H≥1/√2 and ||H⁻¹||≤√2. No compactness uniform over that family is invoked. This is a genuine improvement over Turn 4, which only gave a positive gap for each fixed soliton.

The exact transform identity also extends to the form domain, if its right side is interpreted via the closure. For a form-Cauchy sequence q_j, (4) applied to differences shows that d(q_j/w) is Cauchy in L²(w²μ). On every compact set, w and w⁻¹ are smooth and bounded, so distributional convergence identifies the limit with d(q/w).

There is no nonzero L² eigenvector at the displayed threshold. Equality in (4) would force q/w to be constant on the connected base. But w is not in L²(μ): on the conical end, a is comparable to r, b is comparable to r, and f is bounded above, so the radial density w²a b²e^(−f) is bounded below by a positive multiple of r^(3−2√2). Its integral diverges. Compact resolvent from Turn 4 therefore implies that, for each fixed soliton, its first eigenvalue is strictly greater than √2λ. The uniform assertion is only the non-strict lower bound (5); no uniform positive improvement above it is claimed.

As a secondary coefficient check, the published monotonicity a′,b′≥0 and f′≤0 yields

A′≤λ−A²,  A(0)=0,

hence 0≤A(r)≤√λ tanh(√λ r)≤√λ by scalar differential comparison. The equality of the initial values causes no problem: subtract the comparison solution and use an integrating factor for the inequality (A−y)′≤−(A+y)(A−y). This gradient bound does not bound the full Hessian ℓ pointwise and is not a substitute for a tensor estimate.

## 3. Spherical modes give a stronger local resolvent bound

Let j≥0 be a spherical harmonic degree and Λ_j=j(j+1). On scalar functions of this degree, H reduces to the radial operator

H_j=−p⁻¹(p∂_r)′+2A²+Λ_j/b²,

where p=a b²e^(−f). Integrating the same ground-state identity over S² gives

〈q,H_jq〉 = √2 λ||q||² + ∫w²|∂_r(q/w)|²dμ
                         + ∫(Λ_j/b²)|q|²dμ.     (6)

This identity holds coefficientwise for all 2j+1 harmonics and extends from the smooth core by closure. In particular H_j≥V_j as quadratic forms, where

V_j(r)=√2 λ+Λ_j/b(r)².                           (7)

For j>0 the potential diverges at the polar-coordinate origin, but V_j⁻¹ is bounded and tends to zero there. The actual smooth degree-j functions have their usual regular origin behavior; no new Dirichlet condition is imposed. An origin cutoff in the smooth base has vanishing form error, as in the earlier turns, and (6) supplies the required angular integrability.

For every scalar L² function z of degree j,

0≤〈z,H_j⁻¹z〉≤∫|z|²/V_j dμ.                     (8)

One must not justify (8) by pretending that H and multiplication by V commute. Instead use the variational identity

〈z,H_j⁻¹z〉=sup_q [2 Re〈z,q〉−〈q,H_jq〉]
           ≤sup_q [2 Re〈z,q〉−∫V_j|q|²dμ]
           ≤∫|z|²/V_j dμ.

The supremum for the first expression is over the form domain and follows by completing the H_j form square. The last inequality is the pointwise scalar square; it needs no claim that V_j⁻¹z belongs to the H_j form domain. This is valid also for real-valued functions, with Re omitted.

## 4. Consequence for the genuine coupled normal form

Use Turn 4's notation

ℛ(S)=〈Hess_B ℓ,S〉,

Q₀(S)=∫[|∇^B S|²−2〈Rm_B(S),S〉+2|S(dℓ,·)|²]dμ,

Q_eff(S)=Q₀(S)−4〈ℛ(S),H⁻¹ℛ(S)〉.

The map ℛ is SO(3)-equivariant, so it sends a tensor in the degree-j isotypic subspace either to zero or to scalar harmonics of that same degree. H and its inverse preserve the scalar degree. Equation (8) therefore proves the explicit **local lower bound**

Q_eff(S) ≥ T_j(S),

T_j(S):=Q₀(S)−4∫ |〈Hess_B ℓ,S〉|²
                         /(√2 λ+j(j+1)/b²) dμ. (9)

For arbitrary S, (5) gives the less refined bound

Q_eff(S)≥Q₀(S)−[4/(√2 λ)]||ℛ(S)||².              (10)

Both estimates have explicit constants and act on the actual remaining tensor sector. In the target normalization, the coefficient in (10) is 4√2. The stronger correction in (9) is suppressed near the core for j≥1 and in high spherical degree. The boundedness of ℛ for each fixed soliton and the uniform positive lower bound of V_j make every expression well-defined on the tensor form domain.

A concrete sufficient normal-stability criterion now follows: if, for some degree j≥1, one establishes

T_j(S)≥ε_j||S||² for all S in that tensor sector,  ε_j>0,

then Q_eff has no negative or zero mode there. The exact Schur correspondence in Turn 4 gives the same conclusion for the associated coupled circle-even sector. Establishing this inequality for all nonspherical sectors would remove their index and kernel contribution. It has **not** been established for the Rajan profiles in this work.

The failure of the automatic inference is concrete even at the algebraic level: a two-block form with Q₀=1, H=2 and ℛ=1 obeys an explicit positive scalar lower bound but has effective value 1−4/2=−1. This finite form is only a logical countercontrol to an invalid block-positivity inference, not a Ricci-soliton counterexample. The actual unresolved estimate is exactly (9), involving base curvature, tensor angular derivatives and Hessian ℓ.

## 5. Why this does not compute the original degree

This turn attempted to control the remaining nonspherical sector by an exact soliton-derived scalar transform, rather than assuming a family-wide spectral gap. It succeeds in making the inverse estimate uniform and the correction local. It does not establish the sign of the resulting tensor form. Scalar nonnegative curvature of the four-dimensional soliton does not by itself imply the needed curvature-operator or tensor-form inequality; indeed the known family has mixed sectional curvatures K_(1α)=−(a′/a)(b′/b)<0 away from the core.

Further independent gaps remain even after a hypothetical proof of every inequality (9): the kernels of nonzero circle Fourier modes have not been excluded; the entire unrestricted fiber over a symmetric cone has not been classified as the known standard symmetric family; full regular symmetric targets have not been produced; and the restricted orientation has not been identified with the canonical ambient sign. The finite-dimensional examples in Turn 1 show why symmetry alone cannot fill these gaps.

Finally, nothing here gives the required proper gluing/degree comparison for boundary connected sum. The source asks both for such a relation and for the unrestricted degree of D³×S¹. Neither question is settled. The completed five-turn manuscript is a scoped partial result, pending full independent review. The recently published cohomogeneity-one degree is credited to Rajan and remains distinct from the unrestricted target.

## Verification and source use

The exact certificate checks (1)–(4), the spherical potential identity, the normalization constants, the differential-comparison residual and the variational scalar square. It also tests exact rational positive block matrices and a negative coupled countercontrol. These are algebra checks, not a proof of the analytic domain closure or an estimate of unknown soliton profiles. The analytic proof above and the pinned spectral theorem supply those stated domain conclusions. All new deductions use the already pinned complete primary inputs; the current-source search did not identify a full degree comparison theorem that closes the remaining gap.
