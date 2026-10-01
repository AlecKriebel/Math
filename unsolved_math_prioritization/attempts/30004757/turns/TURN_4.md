# Author research turn 4: general contact faces and angular compatibility

Date: 2026-10-01. Status: proved structural reduction and conditional asymptotic identity; full target active. Completion estimate: 35% (subjective). This is a different route from the axisymmetric rim blow-up.

## 1. Non-axisymmetric contact-body incidence

Let v=u* be one of Mooney's polyhedral-obstacle solutions in n=3 or 4. Write its obstacle as max_i L_i, with L_i(y)=p_i·y−u(p_i), and put K_i={v=L_i}. Each K_i is compact convex with positive volume. Fenchel equality identifies it with ∂u(p_i), and turn1 gives the exact shared-face formula

    K_i∩K_j={y∈K_i : (p_j−p_i)·y=u(p_j)−u(p_i)}.

The source construction supplies an (n−1)-dimensional shared face for every incident graph edge. For the polytope family, nonadjacent vertices cannot have intersecting contact bodies in these dimensions: at such an intersection the subdifferential of v would contain a polytope face of dimension at least two, contrary to the propagation bound used in Mooney's Lemma 4.2. For the Y-shaped construction, the separate contact-body arrangement in Section 5 gives the prescribed star incidence instead.

Define the open affine chamber

    C_i={y : L_i(y)>L_j(y) for all j≠i}.

In any bounded convex subdomain compactly contained in C_i, the function f_i=v−L_i is a nonnegative convex solution of

    det D²f_i=1_{f_i>0}.

This localization is legitimate. The same equation need not hold outside C_i because another contact body can have f_i>0 and zero MA measure.

## 2. A 2025 dimension theorem sharpens the possible extra faces

Primary input: Jin–Tu–Xiong, *On the singular set of the free boundary for a Monge–Ampère obstacle problem*, arXiv:2506.08387, Theorem 1.1 (q=0). For a nonnegative convex solution of the zero-obstacle equation on a bounded convex domain, every convex subset of the non-exposed part of the free boundary has dimension strictly less than n/2. The paper permits zero boundary values; positive boundary values are not being silently assumed. Its proof uses a section-volume estimate, and its later examples show the dimensional bound is sharp.

Consequently, if an exposed face F of K_i meets C_i, then either F is a singleton or dim F<n/2. Indeed, if dim F≥2, choose a small relative open two-dimensional patch of F inside C_i. Its points lie on nontrivial contact-face segments within a bounded subdomain of C_i, so the patch is in the non-exposed free boundary of f_i. The cited theorem gives a contradiction for n=3 or 4.

Thus any non-singleton exposed face meeting the interior chamber is a **line segment**. Moreover its endpoints must lie on the chamber boundary, by the Caffarelli–Savin localization argument from turn1. They must lie on distinct incident interface hyperplanes: if both endpoints lay on one such plane, the entire segment would lie in that plane and could not meet C_i.

This is a useful restriction on possible additional cone nondifferentiability. Mandatory graph-edge rays correspond to the large shared faces. Any additional exposed face penetrating an affine chamber must bridge two distinct interfaces by a segment. Faces lying wholly in an interface remain outside the scope of the dimension theorem and can inherit unknown rim geometry. Neither those interface subfaces nor bridging segments have been excluded.

The sharpness examples and failure of a strong maximum principle on the non-exposed free boundary in the same 2025 paper also prevent replacing this missing argument by an unsupported “strict convexity propagates” assertion. The theorem is credited; it is not a campaign discovery.

## 3. The angular equation does not select the cone at leading order

Consider a smooth angular patch of a hypothetical cone h on S^(n−1) where

    Q_h=∇²_S h+h I

is positive definite. Suppose, as an explicitly additional hypothesis, that u has an expansion

    u(r,θ)=u(0)+r h(θ)+r^(n+1)b(θ)+remainder,

with the remainder negligible through the appropriately weighted second derivatives. No such expansion is being assumed at singular cone directions.

In an orthonormal radial/tangential frame, the Hessian blocks are

    radial:     n(n+1)b r^(n−1),
    mixed:      n r^(n−1)∇_S b,
    tangential: r^(−1)Q_h+r^(n−1)[∇²_S b+(n+1)b I].

Normalize the radial row/column by r^((n−1)/2) and each tangential one by r^(−1/2). The product of these factors is one. The normalized mixed terms have order r^(n/2), and the tangential correction has order r^n. Hence det D²u=1 forces

    b(θ)=1/[n(n+1)det Q_h(θ)].                     (4.1)

This derives the first compatible radial correction from the angular cone. It does **not** yield an equation determining h itself. It also becomes singular as Q_h degenerates, exactly where the source's transition problem lies.

The atom supplies the volume condition |K|=a for the support body K. In the smooth strictly convex case its familiar support-function form is

    a=(1/n)∫ h det(Q_h) dθ.

For nonsmooth bodies the corresponding surface-area measure must be used; facet contributions must not be discarded without checking. A scalar volume constraint and the pointwise formula (4.1) do not select an arbitrary angular support function. The global equation and normalization can still select it uniquely; this local observation is not a nonuniqueness proof for the full boundary-value problem.

## 4. Exact radial and affine calibrations

The one-atom global radial solution has derivative

    U_R'(r)=(r^n+R^n)^(1/n),

and therefore satisfies det D²U_R=1 away from zero and has atom size ω_n R^n. Near zero,

    U_R(r)−U_R(0)=Rr+r^(n+1)/[n(n+1)R^(n−1)]+O(r^(2n+1)).

This verifies (4.1). For n>2 the potential is asymptotic to r²/2 plus a constant and a decaying term, in agreement with the source normalization.

If B is unimodular, U_R(|Bx|) also has density one and the same atom size, but its cone is R|Bx|. Its asymptotic quadratic form is BᵀB. Thus a mass alone does not determine a universal round cone. This is not a counterexample to uniqueness with a fixed isotropic quadratic asymptote, because that asymptote has changed. No part of the global source question is claimed settled by this affine calibration.

Eight symbolic checks verify the radial determinant, the normalized Hessian leading term, absence of a first-order mixed determinant correction, and an ellipsoid calibration. They neither prove the assumed expansion nor choose the unknown support function.

## 5. Residual and final author route

The new reduction restricts extra free faces in the original dimensions to interface-bridging segments, but does not eliminate them. The angular route only expresses the next coefficient in terms of an already known cone, transferring rather than resolving the central problem.

The last substantive turn will test a different limiting regime: collapse two symmetric atom locations while keeping a fixed radial obstacle-exhaustion normalization. The objective is to obtain a rigorous global family limit and see whether it forces, or obstructs, a universal cone description. This will not be called a full resolution unless it actually determines the finite-separation source cones and their Hessian transitions.

Author turns completed: 4/5. One remains; no final unsolved verdict yet.
