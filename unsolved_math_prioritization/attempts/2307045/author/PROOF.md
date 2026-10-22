# Equal radial slits and harmonic measure

## Outcome and attribution

The original equal-length radial-slit problem is already resolved by V. N. Dubinin. The minimizing configuration is the regular angular arrangement, unique up to rotation and relabeling. This note gives a precise reduction to his published theorem and a separate elementary calculation of the attained value. It does not claim a new solution or an independent proof of Dubinin's comparison theorem.

The governing problem is Hayman and Lingham, *Research Problems in Function Theory (New Edition)*, arXiv:1809.07200v2, Problem and Update 7.45, printed page 174. The update attributes the solution to Dubinin, reference [201].

## Domain and quantifiers

Fix an integer p >= 1 and a common slit length ell with 0 < ell < 1. Put r = 1 - ell. For angles theta_0,...,theta_(p-1) distinct modulo 2 pi, define

    E_theta = union over k of { t exp(i theta_k) : r <= t <= 1 },
    D_theta = { z : |z| < 1 } minus E_theta,
    U_theta(z) = omega(z, {|z| = 1}, D_theta).

Here omega denotes harmonic measure. Boundary values are 1 on the outer circle and 0 on the open slit sides, with the finite circle/slit junctions irrelevant to harmonic measure. Both sides of every slit count as slit boundary. The point 0 lies in the domain because r > 0. All lengths are individually fixed; this is not optimization over unequal slits of fixed total length.

Let theta_k^* = beta + 2 pi k/p. Then the full answer is

    U_theta(0) >= U_theta^*(0)
               = (4/pi) arctan(r^(p/2))
               = (4/pi) arctan((1-ell)^(p/2)).                 (1)

Equality holds exactly when the unordered set of directions is a rotation of the p-th roots of unity. For p = 1 this simply says that every direction is equivalent by rotation.

## Reduction to the published theorem

Dubinin's Theorem A concerns the same disk with n equal radial cuts from radius r to radius 1, and the harmonic measure W_alpha of the cuts, evaluated at 0. It asserts W_alpha <= W_alpha^*, with equality only for a rotated regular configuration. Set n = p and alpha_k = theta_k.

To translate the boundary target, note that the outer circle and the slit boundary exhaust the boundary. Their overlap consists of finitely many points. Such points have harmonic measure zero here: the slit domain is simply connected and has a locally connected boundary made of finitely many analytic arcs; a Riemann map sends the finitely many prime ends over these junctions to finitely many points of the unit circle. Arc-length harmonic measure assigns them zero mass. Equivalently, planar Brownian motion has probability zero of exiting at any one prescribed boundary point. Consequently,

    U_theta(0) + W_theta(0) = 1.

Subtracting Dubinin's inequality from 1 reverses its direction and gives the first inequality in (1). The same complement identity transfers the equality classification. This checks the potentially consequential difference between maximizing slit-hitting probability and minimizing escape through the circle.

Reference: V. N. Dubinin, *On the change in harmonic measure under symmetrization*, Mathematics of the USSR-Sbornik 52(1) (1985), 267-273, Theorem A on page 267 and its proof in section 3, pages 272-273. Russian original: Mat. Sb. 124(166), no. 2 (1984), 272-279. DOI: https://doi.org/10.1070/SM1985v052n01ABEH002888 . Journal record: https://www.mathnet.ru/eng/sm2051 .

## Elementary calculation of the extremal value

This section is an authored derivation, independent of the comparison theorem. It computes harmonic measure only for a regular configuration.

By a rotation take beta = 0, and let a = r^p. The map z -> z^p maps the regular slit domain onto

    Omega_a = { w : |w| < 1 } minus [a,1).

Although this power map is branched at 0 for p > 1, the pullback of a harmonic function is harmonic there as well. Indeed, locally a harmonic function is the real part of a holomorphic function, whose composition with z^p remains holomorphic. The pullback of the outer-circle harmonic measure in Omega_a has the correct bounded boundary values in the regular slit domain. Uniqueness of the bounded Dirichlet solution with the finitely many junction points disregarded therefore identifies it with U_theta^*. In particular its value at 0 is the value of the one-slit solution at w = 0.

For this one-slit domain use the disk automorphism

    v = T_a(w) = (w-a)/(1-a w).

It maps [a,1) onto [0,1), maps 0 to -a, and preserves the outer circle. One direct identity verifying the disk mapping is

    |1-a w|^2 - |w-a|^2 = (1-a^2)(1-|w|^2).

On the disk cut along [0,1), choose the square root with 0 < arg(v) < 2 pi. Then s = sqrt(v) maps onto the upper half of the unit disk, and v = -a maps to s = i sqrt(a). The two banks of the cut go to the diameter; the outer circle goes to the upper semicircle. Next,

    q = (1+s)/(1-s)

maps that upper half-disk to the first quadrant. In fact

    Re(q) = (1-|s|^2)/|1-s|^2 > 0,
    Im(q) = 2 Im(s)/|1-s|^2 > 0.

The diameter maps to the positive real axis, and the semicircle to the positive imaginary axis. Thus the harmonic function giving the semicircle harmonic measure is (2/pi) arg(q), using the argument in (0,pi/2). At s = i sqrt(a),

    arg((1+i sqrt(a))/(1-i sqrt(a))) = 2 arctan(sqrt(a)),

because 0 < sqrt(a) < 1. It follows that

    U_theta^*(0) = (4/pi) arctan(sqrt(a))
                = (4/pi) arctan(r^(p/2)),

as asserted. These conformal maps establish the value without numerical approximation.

## Degenerate inputs and controls

- ell = 0, equivalently r = 1, gives an uncut disk and value 1; the strict equality classification is then inapplicable.
- ell = 1, equivalently r = 0, removes the evaluation point. The original interior harmonic-measure question is then undefined. The expression in (1) has limit 0 as r decreases to 0; this is a limit, not evaluation at a permitted parameter.
- If repeated directions are allowed in a p-tuple, there are q <= p actual slits. Apply the theorem with q. If q < p, then r^(q/2) > r^(p/2), so its lower bound is strictly larger than the regular p-slit value. Coinciding slits therefore do not improve the minimum.
- For fixed p the extremal value strictly increases with r. For fixed 0 < r < 1 it strictly decreases with p. These are immediate from monotonicity of arctan and powers.
- As an exact normalization check, p = 2 and r = sqrt(2)-1 give value 1/2, since arctan(sqrt(2)-1) = pi/8.

The supplied standard-library script checks finite exact rational identities in the conformal maps and monotonicity of squared power arguments. Its floating-point controls are labeled separately. Neither kind of computation proves Dubinin's global comparison theorem; that input is a published theorem, explicitly cited above.

## Verification limits

The primary collection PDF was freshly downloaded and its Problem/Update 7.45 inspected in text and a rendered page. Dubinin's journal record gives the exact theorem in readable mathematical notation. The web text service supplied all seven pages of the English paper, including its proof, but some formulas are damaged by OCR. Direct PDF downloads and attempted PDF screenshots failed. Accordingly this investigation establishes a source-matched published prior resolution; it does not claim a complete symbol-by-symbol independent audit of the original dissymmetrization argument. The endpoint, complement and explicit-value arguments written here are separate authored mathematics and remain subject to fresh independent review.

Sources: https://arxiv.org/abs/1809.07200v2 ; https://www.mathnet.ru/eng/sm2051 ; https://doi.org/10.1070/SM1985v052n01ABEH002888 .
