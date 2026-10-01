# Author research turn 3: anisotropic crease blow-up and its explicit model

Date: 2026-10-01, resumed after an independent review on another target. Status: exact model and conditional reduction; original problem still active. Completion estimate: 30% (subjective). This turn attacks the missing rim-matching step rather than treating a model as a global solution.

## 1. The only scaling preserving both the disk curvature and MA density

Use the two-mass dual potential v and its separating plane z=0. Let the shared disk have radius R>0, and center local coordinates at q=(R,0,…,0,0), a point of its rim. Write the variables as (x,y,z), with y∈R^(n−2). Set α=n/(n−2) and

    v_ε(x,y,z)=ε^(−α)
      v(R+εx, sqrt(ε)y, ε^α z).

The coordinate determinant is ε^(n/2+α). The determinant multiplier for the Hessian is therefore ε^(n+2α−nα)=1. This is an exact Monge–Ampère scaling, not an approximate density normalization. The obstacle remains |z|.

On z=0 the rescaled contact disk is exactly

    2Rx+|y|²+εx²≤0.

Its limiting rim is the paraboloid x+|y|²/(2R)=0. Rotational symmetry shows that if these functions have a finite locally uniform limit, it must take the form

    v_∞(x,y,z)=V(s,z),  s=x+|y|²/(2R).

A determinant calculation gives

    det D²v_∞ = (V_s/R)^(n−2)(V_ss V_zz−V_sz²).       (3.1)

This follows by a determinant-one row/column shear removing the first derivatives of s in the y-block. The remaining y-block is (V_s/R)I.

If the full family has a unique nontrivial limit, rescaling ε once more forces

    V(λs, λ^α z)=λ^α V(s,z).

Neither local boundedness, nontriviality, nor uniqueness has been proved for the actual source potential. Subsequence extraction alone does not imply this homogeneity.

## 2. Exact classification within the homogeneous symmetric model class

The following construction is valid for every integer n>2. It is an explicit global solution of the *limiting two-plane obstacle problem*. It is not an entire source potential with finitely many atoms.

Define

    c0 = R^(n−2)/[α^(n−1)(α−1)],
    I_n = ∫_0^1 (1−t²)^(-(n−1)/n) dt,
    B0 = [sqrt(2c0/n) I_n]^(2/(n−2)),
    η0 = sqrt(2 B0^n/(n c0)).

The integral is finite. For |η|<η0 put

    B(η)=[B0^n−(n c0/2)η²]^(1/n),
    φ'(η)=∫_0^η c0/B(t)^(n−1) dt,
    φ(η)=B(η)+ηφ'(η).

Then extend φ by |η| for |η|≥η0. The chosen B0 makes φ'(η0)=1, and B(η0)=0 gives φ(η0)=η0. Thus φ and φ' match at both endpoints. Inside the interval,

    φ−ηφ'=B>0,
    φ''=c0/B^(n−1)>0.

The divergence of φ'' at the endpoints is integrable, so φ is C¹ across them. It lies strictly above |η| inside and equals |η| outside.

Set

    V(s,z)=s^α φ(z/s^α),  s>0,
    V(s,z)=|z|,           s≤0.

Writing η=z/s^α and B=φ−ηφ', direct differentiation gives

    V_s=αs^(α−1)B,
    V_ss V_zz−V_sz²=α(α−1)s^(−2)Bφ''.

Substitution into (3.1) gives det D²v_∞=1 in

    {s>0, |z|<η0 s^α}.

Elsewhere v_∞=|z|. Convexity follows from V_s≥0, the positive semidefinite two-variable Hessian, and the matching gradients at the joining curves; composing with s=x+|y|²/(2R) preserves convexity. At the remaining crease, |z| is a global supporting obstacle. All subgradients on the contact boundary lie on the one-dimensional segment between the two obstacle gradients. Its n-dimensional measure is zero. Consequently the identity holds in the Alexandrov sense globally:

    M_{v_∞}=1_{v_∞>|z|} dx dy dz.

Within the assumed class (even in z, anisotropically homogeneous, with a single central noncontact interval and C¹ matching to |z|), the profile is unique. Indeed the PDE reduces to

    B^(n−1)φ''=c0,
    (B^n)'=−n c0 η.

Evenness fixes the integration center, and the endpoint slope fixes B0. This is a conditional model-class uniqueness statement, not uniqueness of source blow-ups.

## 3. Agreement with the independent edge-model calculation

The limiting dual contact bodies have the local shape

    z≥η0[s_+]^α,   z≤−η0[s_+]^α.

Thus their rims are tangent to the separating plane. For n=3 the free boundary opens cubically; for n=4 it opens quadratically. For an actual source limit, such a tangential rim would put every other support direction in an interior affine chamber. That would make local higher-order free-boundary estimates relevant; those estimates and matching would still need to be checked.

These coefficients agree with turn2's separated model when its physical endpoints are normalized to ±1. To check this without a numerical fit, write

    J_n=∫_0^1(1−t^n)^(-1/2)dt=(2/n)I_n.

The energy identity for a''=−λa^(n−1), together with endpoint distance one, determines its endpoint derivative d. Combining it with turn2's C gives dC=η0. `verify_rim_model.py` checks this identity exactly for n=3,4, as well as the Hessian determinant and scaling identities. All 12 checks pass.

The model belongs to the familiar Pogorelov-type mechanism. Its convex dual, on its natural restricted domain, has the structure

    R|b|²/(2a) + a^(n/2) f(c),   a>0, |c|<1,

where f solves an elementary second-order ODE. This identifies the construction with a classical ansatz family; no novelty is asserted. Its dual is not finite on all R^n, which prevents using it directly as an answer to the source problem.

## 4. Attempted comparison and the exact failure

The next desired claim would be that v_ε converges to the model above. The following tempting steps are not valid without additional estimates.

1. **Euclidean blow-up is insufficient.** Ordinary convex differentiability gives v(q+rX)/r→|z|. Because α>1, this does not bound ε^(−α)v(R+ε,0,0). A finite anisotropic blow-up requires a substantially sharper growth estimate.
2. **A determinant balance is not a growth estimate.** The fact that α preserves MA density merely identifies a candidate scale. It does not rule out degeneration or unboundedness on that scale.
3. **The explicit model cannot yet be placed as a two-sided barrier.** It equals the obstacle on top and bottom contact regions. On a proposed comparison cylinder, it is not known that the actual contact body already lies there. Claiming the necessary boundary ordering would assume the very tangency-to-the-plane conclusion being proved.
4. **One-plane regularity does not cross the crease.** In one affine chamber v−z solves the usual zero-obstacle equation. Across z=0 the other contact body has v−z>0 but zero MA measure. The hypotheses of the zero-obstacle theorem fail there.
5. **Homogeneity is not automatic.** A convergent subsequence can have different dilation limits. A monotonicity formula, quantitative improvement of shape, or a uniqueness argument is still missing.

A local section-volume heuristic also predicts α: a cap of radial width ε, transverse widths sqrt(ε), and axial height h has volume of order ε^(n/2)h, which balances the Alexandrov height scale h^(n/2) at h≈ε^α. However, proving that the actual sections have these widths and remain inside the cap is exactly the missing geometric estimate. This heuristic is recorded as unsuccessful, not as a proof.

## 5. Residual target and next route

This turn produces and checks the candidate model that a successful crease analysis should recover, and isolates the quantitative gap. The route is blocked at the growth/compactness and matching step; it cannot be reopened merely by restating the same scaling argument.

The full polyhedral/Y-shaped target remains active. Next substantive route: investigate non-axisymmetric contact-body faces and the angular Hessian equation, including whether the mass and normalization can select the cone or whether additional free boundary data inevitably remain. Author turns completed: 3/5; two remain.
