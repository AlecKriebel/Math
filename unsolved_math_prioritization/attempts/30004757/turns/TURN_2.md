# Author research turn 2: reduced PDE and an exact local edge model

Date: 2026-10-01. Status: partial construction and reduction; full target active. Completion estimate: 25% (subjective). No novelty claim. The model below is not asserted to be the source's normalized global two-mass solution.

## 1. Radial partial Legendre transform

Write an axisymmetric smooth strictly convex potential as u(ρ,z), where ρ=|x'|>0. Its real Monge–Ampère equation is

    (u_ρ/ρ)^(n−2) (u_ρρ u_zz − u_ρz²) = 1.

Put p=u_ρ>0 and F(p,z)=pρ−u(ρ,z). Then

    F_p=ρ,  F_pp=1/u_ρρ,
    F_zz=−(u_ρρ u_zz−u_ρz²)/u_ρρ.

Consequently the exact transformed equation is

    F_zz + (F_p/p)^(n−2) F_pp = 0,                 (2.1)

or, equivalently,

    ∂_z(p^(n−2) F_z) + (1/(n−1))∂_p(F_p^(n−1))=0.

It is the Euler equation of the local energy with density

    p^(n−2) F_z²/2 + F_p^n/[n(n−1)].

The transform does not turn this into a uniformly elliptic equation at the relevant boundary: F_p=ρ→0. For n=3 the equation is p F_zz+F_p F_pp=0. Standard uniformly elliptic boundary regularity cannot be invoked there.

## 2. An exact separated local solution

Fix n=3 or 4, R>0, and λ>0. Seek

    F(p,z)=a(z)b(p).

Equation (2.1) holds if

    a''=−λa^(n−1),
    (b')^(n−2)b''=λp^(n−2)b.                    (2.2)

Choose a even, positive on (−L,L), zero at ±L, with a'(L)=−d<0. Such a exists by the elementary energy identity

    (a')²/2 + λa^n/n = λa(0)^n/n.

The first positive zero is finite. Varying a(0)>0 sets any prescribed L>0.

There is a local positive branch b on R<p<R+ε satisfying

    b(R)=b'(R)=0,
    b(p)=C(p−R)^α[1+O(p−R)],
    α=n/(n−2),
    C^(n−2)=λR^(n−2)/[α^(n−1)(α−1)],           (2.3)

with corresponding differentiated asymptotics through order two. In particular, b'>0 and b''>0 on that interval.

Here is a local existence argument rather than just a balance of powers. Set x=p−R, b=Cx^αw(x), and D=x d/dx. The equation for w is

    (αw+Dw)^(n−2)
      [α(α−1)w+(2α−1)Dw+D²w]
    = α^(n−1)(α−1)(1+x/R)^(n−2)w.

Writing y=(w−1,Dw), this is x y'=A y+g(x,y), where g is analytic near (0,0), g=O(x)+O(|y|²)+O(x|y|). For n=3 the eigenvalues of A are −1 and −6; for n=4 they are −1 and −4. Both matrices are diagonalizable. The integral equation

    y(x)=∫_0^x (x/t)^A g(t,y(t)) dt/t

is a contraction on a sufficiently small interval in a suitable ball for the norm sup |y(x)|/x. Indeed, the kernel is bounded by a constant times t/x, the inhomogeneous term is O(t), and the nonlinear Lipschitz constant on that ball is O(t). The map preserves the ball and contracts after reducing ε. Its solution has y=O(x), is smooth for x>0, and satisfies the displayed equation. This proves (2.3) and the derivative assertions. No convergence of a merely formal power series is assumed.

For 0<ρ<a(z)b'(R+ε), invert ρ=a(z)b'(p), and define

    U(ρ,z)=pρ−a(z)b(p).

The inverse exists because b''>0. Its Hessian in (ρ,z) is positive definite, and its transverse eigenvalues are p/ρ>0. Substitution into (2.1) proves det D²U=1 exactly. Extending U continuously by zero at ρ=0 gives a convex local potential with a singular affine axis segment. Its subgradient along each interior point of that segment is the transverse disk of radius R, which has n-dimensional volume zero. Thus the extension introduces no Dirac mass along the interior segment.

This is a local edge model. It does not define a finite convex potential in a full neighborhood of z=±L, does not prescribe compact subgradient bodies at those endpoints, and does not satisfy the global isotropic quadratic normalization. It is consequently not a solution of the full atomic-vertex problem.

## 3. Edge and endpoint-sector asymptotics

For z in a compact subinterval of (−L,L), the Legendre transform of (2.3) gives

    U(ρ,z)=Rρ+f(z)ρ^(n/2)+o(ρ^(n/2)),
    f(z)=(2/n)[αCa(z)]^(−(n−2)/2).

The exponent n/2 agrees with the edge model discussed by Mooney in Remark 4.6. That exponent is not a new discovery here. This derivation also shows f(z) diverges like (L−z)^(−(n−2)/2) near an endpoint in the separated model. An expansion valid for fixed z must not simply be substituted into a simultaneous endpoint limit.

The simultaneous limit can instead be computed directly. For ρ>0 and t>0 with ρ/(dt)<b'(R+ε), take the physical point (rρ,L−rt). Since a(L−rt)/r→dt, its rescaled potential converges to

    T(ρ,−t)=ρp−dt b(p),  where d t b'(p)=ρ.      (2.4)

This follows from strict monotonicity of b' and the exact formula for U, not an interchange of the preceding asymptotic expansion. T is one-homogeneous in (ρ,t) and smooth for ρ>0 in this sector. As ρ/t↓0,

    T(ρ,−t)=Rρ+A ρ^(n/2)t^(−(n−2)/2)
             +o(ρ^(n/2)t^(−(n−2)/2)),
    A=(2/n)(αCd)^(−(n−2)/2)>0.

In dual variables this sector corresponds to a contact-body boundary with height d b(p), vanishing at its disk rim to order α. Thus the candidate rim exponents are 3 in n=3 and 2 in n=4. The potential exponents transverse to the inward cone ray are respectively 3/2 and 2.

These conclusions are exact for the constructed local model and conditional as predictions for the source solutions. There is no uniqueness or matching theorem identifying (2.4) with a source tangent cone.

## 4. Why this does not close the global source question

The decisive missing step is a boundary estimate or uniqueness principle proving that the global two-mass solution has the separated model's rim behavior. The partial Legendre equation is degenerate precisely where this estimate is needed. Equality of an atom's mass, the disk radius, and the affine edge does not supply Cauchy data that force separability.

Even a two-mass matching theorem would leave the general polyhedral/Y-shaped target. The reduction identifies a plausible model and its exact local equation; it is not a reduction to a theorem already proved in the cited literature.

`verify_reduction.py` independently checks 20 symbolic identities: the transform on a nontrivial polynomial calibration, divergence form, separation, exponents, and both indicial polynomials. Its PASS is an algebra check, not a proof of the missing matching theorem.

## 5. Next substantive route

Investigate local free-boundary comparison and normalized blow-up compactness at the crease, using the explicit model as a possible barrier. In particular, first decide whether contact-body boundary normals at the disk rim must be perpendicular to the disk. Without that step, smoothness away from the inward ray cannot be inferred from interior-chamber free-boundary theorems.

Author turns completed: 2/5. Three remain. Full target remains active; no final unsolved verdict or publication.
