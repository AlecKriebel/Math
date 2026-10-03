# Kirby Problem 5.17: convexity, cohomology, and the remaining Weinstein gap

**Problem:** 3024 / KP-5.17. **Outcome:** unresolved after five substantive attempts. No proof or counterexample to the general question is claimed. The elementary results below, including the explicit examples, carry no claim of historical novelty.

## 1. Exact target and conventions

Fix a symplectic manifold (W, ω). Given two Weinstein structures (ω, Z₀, φ₀) and (ω, Z₁, φ₁), must a Weinstein homotopy connect them? This is the question in [K3, Problem 5.17, printed pp. 315–316], proposed by Y. Eliashberg and scribed by L. Starkston. The endpoints have the **same actual symplectic form**, not merely diffeomorphic underlying manifolds or cohomologous forms. [E17, Problems 1.4–1.5] asks the corresponding completed-manifold question and its symplectomorphism-pullback special case.

The K3 remarks discuss a path of boundary-outward Liouville fields that all admit gradient-like functions. Its displayed interpolation has Z₂ in both summands. We explicitly use the intended endpoint interpolation (1−t)Z₀+tZ₁, rather than silently treating that printed formula as a valid interpolation.

For the self-contained arguments we use the Morse version of the definition in [CE13, pp. 1–3]. A Liouville field satisfies L_Z ω = ω, equivalently dλ = ω for λ = ι_Z ω. “Gradient-like” means, for a Riemannian metric and some positive function δ,

    dφ(Z) ≥ δ (|Z|² + |dφ|²).                         (1)

On a compact Weinstein domain, φ is constant at its maximum on the boundary, with nonzero outward derivative, and Z points outward. On an open manifold, φ is exhausting and Z is complete. Weinstein homotopies can have the standard birth–death singularities; our constructed homotopies are Morse throughout. For open examples below all critical points stay in a fixed compact subset over a compact parameter interval, and their critical values stay bounded, so the usual admissibility at infinity is satisfied.

Ordinary Weinstein homotopy may vary ω along the path. Our elementary affirmative constructions keep ω fixed, which is stronger for those examples. No claim is made that an arbitrary ordinary homotopy can be converted to a fixed-ω homotopy **while preserving both prescribed endpoints on the same compact domain**.

## 2. Attempt 1: use affine convexity to prove uniqueness

### 2.1 What convexity proves

If dλ₀=dλ₁=ω, then λ_t=(1−t)λ₀+tλ₁ also has derivative ω. The associated field is Z_t=(1−t)Z₀+tZ₁. If both endpoint fields point outward on a compact boundary, their positive normal components interpolate to positive normal components. Thus the space of boundary-outward primitives of a fixed ω is convex.

A sufficient extra hypothesis is a **common** Morse Lyapunov function φ. Suppose (1) holds for both fields with a common positive lower bound δ on a compact domain. Then

    dφ(Z_t) ≥ δ ((1−t)|Z₀|²+t|Z₁|²+|dφ|²)
             ≥ δ (|Z_t|²+|dφ|²),                    (2)

by convexity of squared norm. Boundary and Morse conditions are unchanged, so this is a fixed-form Weinstein homotopy. This is the relevant convex-cone principle of [CE13, Lemma 3.1], with its elementary proof included here. It does not supply a common φ for arbitrary endpoints.

### 2.2 Exact compact counterexample to the affine-path shortcut

There are Weinstein endpoints whose affine midpoint has a nonconstant periodic orbit. This disproves the shortcut, not the problem.

Let W = (R/2πZ) × [−2,2], with coordinates (q,p) and ω=dp∧dq. For s∈{−1,+1}, set

    a=1/8,  b=1/2,  k=8/9,
    w_s(q)=a+s b sin q,
    U_s(q)=−s(7/18) cos q+(1/18) sin(2q),
    Z_s=p(1−w_s'(q)) ∂p+w_s(q) ∂q,
    λ_s=p(1−w_s') dq−w_s dp,
    φ_s=p²/2+(1−p²/4)U_s(q).                         (3)

Direct differentiation gives

    U_s'=w_s(1−k w_s),  dλ_s=dp∧dq,
    dφ_s(Z_s)=p²(1−U_s/2)(1−w_s')
                +(1−p²/4)w_s²(1−k w_s).           (4)

The following bounds hold everywhere:

    −3/8 ≤ w_s ≤ 5/8,  |w_s'|≤1/2,  |U_s|≤4/9,
    4/9 ≤ 1−k w_s ≤ 4/3,  7/9 ≤ 1−U_s/2 ≤ 11/9.

As |p|≤2, both terms in (4) are nonnegative. More quantitatively,

    dφ_s(Z_s)
      ≥ (7/18)p²+(4/9)(1−p²/4)w_s²
      ≥ (199/576)p²+(4/9)w_s²
      ≥ (1/3)(p²+w_s²).                             (5)

For the flat metric dp²+dq²,

    |Z_s|²+|dφ_s|²
      ≤ (9/4+121/81)p²+(1+16/9)w_s²
      ≤ 4(p²+w_s²).

Thus (1) holds with δ=1/12. On p=±2, φ_s=2; in the interior,

    2−φ_s=(1−p²/4)(2−U_s)>0.

The normal component of Z_s is strictly outward on both boundary components. Also φ_p=p(1−U_s/2), so the critical points are precisely p=0, w_s=0. There are exactly two: sin q=−s/4. At these points the Hessian in (p,q) coordinates is diagonal with entries 1−U_s/2>0 and U_s''=w_s'=±√15/8. Both points are nondegenerate, one of index zero and one of index one. Consequently both endpoints in (3) are Weinstein structures on the same compact symplectic annulus.

But their mean field is

    Z_mid=p∂p+(1/8)∂q.                              (6)

The circle p=0 is a nonconstant periodic orbit, of period 16π. A function satisfying (1) would increase strictly along that orbit and return to its starting value after one period, which is impossible. Therefore the midpoint admits no gradient-like function at all.

This failure already occurs with **exact primitive difference**:

    λ_+−λ_−=−d(p sin q).                             (7)

Moreover, the two endpoints are nevertheless Weinstein homotopic. The symplectic rotations f_t(q,p)=(q+πt,p) preserve W. Pulling (λ_+,φ_+) back by f_t gives a Weinstein homotopy to (λ_−,φ_−). All identities and bounds persist under translation of q. Hence this pair is explicitly not a counterexample to KP-5.17.

For comparison in every real dimension 2n, the same fields on T*S¹, with exhausting functions ψ_s=p²/2+U_s(q), can be multiplied by the standard Weinstein structure on C^(n−1). The functions ψ_s+|z|² are exhausting; their only critical points have index zero or one; the fields are complete because the q component is bounded and the p,z equations grow at most linearly. The affine midpoint still has the periodic orbit p=z=0. This shows that the affine-path shortcut also fails for these subcritical endpoints when n≥2.

**Attempt outcome:** common-Lyapunov convexity is proved, and an explicit periodic-orbit obstruction rules out the unconditional affine argument. A different path may and here does exist.

## 3. Attempt 2: exploit exactness and continue small perturbations

Write λ₁−λ₀=β. This is closed. If H¹(W;R)=0, de Rham theory gives β=dF. It is tempting to conclude that the Hamiltonian correction ι_Yω=dF is harmless. Equation (7) and the periodic midpoint show why exactness alone does not make affine interpolation Weinstein.

Here is the valid local statement. Let (W,ω,Z,φ) be a compact Weinstein domain. Suppose dF is supported in a compact set K disjoint from Crit(φ) and from the boundary; set ι_Yω=dF. If K is empty the claim is immediate. Otherwise put

    m=min_K dφ(Z)>0,  B=max_K |dφ(Y)|.

If B>0 and |u|≤m/(2B), then

    dφ(Z+uY) ≥ m/2 on K.                            (8)

If B=0 the same positivity holds for any fixed bounded interval of u. Outside K the field and function are unchanged. On K, compactness gives a bound for |Z+uY|²+|dφ|² uniform over the chosen u interval, so (8) implies (1) there; the unchanged Weinstein inequality applies off K. Since d(λ+u dF)=ω, boundary conditions and critical points are unchanged. This proves a genuine fixed-form Weinstein homotopy for sufficiently small supported exact perturbations.

The global continuation inference does not follow. A bound m for one Lyapunov function need not remain positive when one leaves its allowed interval; K may also cease to avoid critical points of a proposed new function. Local neighborhoods in a space need not place all points in the same connected component. Example (3) supplies a concrete exact segment where a periodic orbit actually interrupts continuation along that segment.

Even the vanishing of H¹ therefore removes only the closed-versus-exact distinction. To complete this approach one would need a global continuation theorem, permitting Lyapunov functions and birth–death points to change while preserving the Weinstein condition. We have not proved such a theorem or a simply connected counterexample.

**Attempt outcome:** a quantitative supported-perturbation theorem, with the exact global continuation gap isolated.

## 4. Attempt 3: use primitive cohomology as an obstruction

The class [λ₁−λ₀] lies in H¹(W;R), but it is not forced to vanish by a fixed-form Weinstein homotopy. The following explicit family tests and rejects that proposed obstruction.

On T*S¹, fix 0<ε<1 and any c∈R. Define

    λ_c=(p−c)dq+ε d((p−c)sin q),
    Z_c=(p−c)(1+ε cos q)∂p−ε sin q∂q,
    φ_c=(p−c)²/2+ε cos q.                           (9)

Then dλ_c=dp∧dq and

    dφ_c(Z_c)=(p−c)²(1+ε cos q)+ε² sin²q.          (10)

The right side dominates (1−ε)((p−c)²+ε² sin²q). The sum |Z_c|²+|dφ_c|² is at most

    ((1+ε)²+1)(p−c)²+2ε² sin²q,

so (1) holds with a uniform positive constant. The functions are exhausting. The q equation is bounded and the p−c equation has bounded linear coefficient, proving completeness. There are exactly two Morse critical points p=c, q=0,π, of indices one and zero, respectively.

For any c₀,c₁, let c(t)=(1−t)c₀+tc₁. Formulas (9) give a fixed-form Weinstein homotopy. The critical values are ±ε, and all critical points for this path are in a compact set. Nevertheless

    λ_c₁−λ_c₀=−(c₁−c₀)dq−ε(c₁−c₀)d(sin q),
    [λ_c₁−λ_c₀]=−(c₁−c₀)[dq].                     (11)

The integral around the q-circle is −2π(c₁−c₀), nonzero when c₁≠c₀. Taking products with C^(n−1) supplies the same observation in every even dimension.

This does not rule out every sophisticated obstruction involving H¹ or behavior at infinity. It does rule out the simple claim that different primitive cohomology classes cannot be joined by a Weinstein homotopy. It also distinguishes unrestricted homotopy from a homotopy constrained to have exact primitive differences at every time or to be fixed near infinity.

**Attempt outcome:** primitive cohomology alone does not separate components; explicit complete homotopies change it.

## 5. Attempt 4: pull back by symplectic isotopy, or use Moser transport

There is an elementary affirmative case. If f_t is a smooth family of symplectomorphisms of a compact W with boundary, f₀=id, and f₁=f, then

    λ_t=f_t*λ,  φ_t=f_t*φ,  Z_t=(Df_t)^−1 Z∘f_t   (12)

is a fixed-form Weinstein homotopy. Pullback preserves the Liouville identity, gradient-like inequality (with the pulled-back metric), Morse property, and outward boundary condition. This covers the identity component of the relevant symplectomorphism group. K3's proposed difficult special case deliberately allows f outside that component, so assuming such an f_t would assume away its obstruction.

What about deriving f_t by Moser's method? For any fixed-form path λ_t, define Y_t by ι_Y_t ω=−dot λ_t. If its flow h_t exists on the whole region under consideration, then Cartan's formula gives

    d/dt(h_t*λ_t)=h_t*(dot λ_t+ι_Y_tω+d(λ_t(Y_t)))
                  =d(h_t*(λ_t(Y_t))),              (13)
    L_Y_t ω=−d(dot λ_t)=0.

This produces symplectic transport and an exact endpoint relation. On a compact manifold with boundary Y_t need not be tangent to that boundary; on an open manifold completeness also needs justification. Even when both issues are absent, (13) does not generate Lyapunov functions for the intermediate λ_t. Pulling a periodic orbit back by h_t does not destroy its periodicity. Exact symplectic identification and Weinstein homotopy are therefore not interchangeable steps of this argument.

**Attempt outcome:** the symplectic-isotopy case is proved; the general Moser argument stops at transport of primitives, not at a Weinstein path. No nontrivial mapping-class obstruction has been certified.

## 6. Attempt 5: formal invariants and flexible lifting

The shared symplectic form already kills the most immediate almost-complex obstruction. Here is the explicit standard argument. Given two ω-compatible almost complex structures J₀,J₁, let g_i(u,v)=ω(u,J_i v), and interpolate positive metrics g_t=(1−t)g₀+t g₁. Define A_t by

    g_t(A_tu,v)=ω(u,v),  B_t=(−A_t²)^(1/2),
    J_t=A_t B_t^−1.                                (14)

A_t is invertible and skew-adjoint; B_t is smooth, positive, self-adjoint, and commutes with A_t. Consequently J_t²=−1, J_t is g_t-orthogonal, and

    ω(u,J_t v)=g_t(B_tu,v)

is positive definite. At the endpoints A_i=J_i and B_i=1. Thus (14) is a compatible homotopy. In particular, Chern classes of compatible almost complex structures cannot distinguish the two endpoints on this fixed (W,ω).

In dimensions 2n>4, [CE13, Theorems 5.4, 5.6 and 6.1] supplies Weinstein homotopies for **flexible** structures in the same almost-symplectic class. For domains the negative boundary is empty, so the relative negative-boundary hypothesis is vacuous; the constant path η_t=ω supplies the formal class. Theorem 6.1 supplies the index-bounded Morse homotopy. This is a genuine known affirmative special case. The output homotopy can vary its symplectic form; nothing here upgrades that theorem to an endpoint-preserving fixed-form assertion for arbitrary compact domains.

The relevant proof in [CE13, §§5.3–5.4] reduces to elementary pieces and uses the parametric loose-isotropic/Legendrian extension. This step needs flexibility; it cannot be reused for unrestricted critical handles merely because (14) exists. A fixed ω does not assert that arbitrary critical attaching links are loose. We have neither produced a substitute for that lifting step nor proved that arbitrary Weinstein endpoints can first be made flexible within their Weinstein homotopy classes.

The fixed-complex-structure result mentioned in [K3, Remark (2)] is another restricted case. We do not use the unavailable full book's Proposition 11.22 as an independently checked general theorem. The abstract of Iida's August 2026 preprint [I26] concerns nonsymplectomorphic exact forms on one smooth four-manifold, so that announced result cannot be substituted for two structures with identical ω. Its proof is not used here.

**Attempt outcome:** compatible formal data agree, and the flexible case is covered by a theorem with a checked hypothesis boundary. The nonflexible lifting step remains missing.

## 7. Precise remaining question

For arbitrary Weinstein endpoints on one fixed (W,ω), we have not constructed a path of Weinstein structures joining them, nor any invariant proving that such a path cannot exist. For the stronger boundary-outward fixed-form route, the precise missing assertion is path-connectedness of the subset of primitives λ with dλ=ω whose associated Liouville fields admit admissible generalized-Morse Lyapunov functions. Convexity of all primitives does not establish that assertion. Nor does failure of the affine segment refute it. The ordinary homotopy problem remains unresolved here as well.

The exact verifier checks the algebraic identities and rational inequalities in the explicit examples. It does not establish the universal assertion, exhaust symplectic manifolds, verify external h-principle proofs formally, or replace the arguments concerning periodic orbits, completeness, and global homotopy.

## References

- [K3] R. I. Baykur, R. C. Kirby, D. Ruberman (eds.), *K3: Kirby's Problems in Low-Dimensional Topology*, author preliminary version, Problem 5.17, printed pp. 315–316. https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf
- [CE13] K. Cieliebak and Y. Eliashberg, *Flexible Weinstein manifolds*, arXiv:1305.1635 (2013), especially pp. 1–3, Lemma 3.1, Theorems 5.4, 5.6, 6.1 and proofs in §§5.3–5.4. https://arxiv.org/abs/1305.1635
- [E17] Y. Eliashberg, *Weinstein manifolds revisited*, arXiv:1707.03442v2 (2017), pp. 1–5. https://arxiv.org/abs/1707.03442v2
- [CE12] K. Cieliebak and Y. Eliashberg, *From Stein to Weinstein and Back*, AMS Colloquium Publications 59 (2012). Mentioned for K3's attribution; full-book text not successfully retrieved in this investigation. https://doi.org/10.1090/coll/059
- [I26] N. Iida, *Stein structures not determined by the contact boundary*, arXiv:2608.09361v2 (2026). Abstract-level scope check only; no proof result imported. https://arxiv.org/abs/2608.09361v2
