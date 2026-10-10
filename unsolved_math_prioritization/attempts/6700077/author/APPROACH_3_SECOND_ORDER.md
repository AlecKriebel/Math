# Approach 3: transfer through a smooth second-order germ

## Pointwise transfer lemma

Let h be C2 near p and g be continuous and positive definite. Suppose, in local coordinates or an equivalent h-tensor norm,

|g(x)-h(x)| = o(d_h(p,x)^2) as x -> p.

Then their centered ball volumes have the same scalar term:

vol_g(B_g(p,r))
 = omega_n r^n [1-Sc_h(p)r^2/(6(n+2))+o(r^2)].

This is a statement about balls centered at p. By itself it does not assert a locally uniform volumic lower bound in a neighborhood of p.

## Proof

The hypothesis implies that on the h-ball of radius C r, the relative tensor error is e(r)=o(r^2), for any fixed C. Indeed the defining little-o estimate holds uniformly at all points within that ball. Positive definiteness and continuity localize both g- and h-short paths to such a ball, as in Approach 1. The determinant and distance comparisons consequently give

(1-e)^(n/2) vol_h(B_h(p,r/sqrt(1+e)))
 <= vol_g(B_g(p,r))
 <= (1+e)^(n/2) vol_h(B_h(p,r/sqrt(1-e))).

The C2 expansion of h is
vol_h(B_h(p,s)) = omega_n s^n [1-Sc_h(p)s^2/(6(n+2))+o(s^2)].
For s=r(1+O(e)), the leading volume changes by O(e r^n)=o(r^(n+2)), and the scalar term changes by a still smaller amount. Both sides of the sandwich therefore equal the claimed expression up to o(r^(n+2)). QED.

## Sharpness at order two

Let h be Euclidean and g_a = exp(2a|x|^2)h, where a is a real constant. At the center,

Sc(g_a)(0) = -4n(n-1)a.

A direct volume computation verifies the constant. If rho denotes Euclidean radial coordinate and r is g_a-distance from the center, then
r = integral_0^rho exp(a t^2)dt = rho + a rho^3/3 + O(rho^5).
Radial segments minimize from the center, since any path has length at least the integral of the radial coefficient over its radial displacement. Volume is

n omega_n integral_0^rho exp(na t^2)t^(n-1)dt
 = omega_n rho^n [1+n^2 a rho^2/(n+2)+O(rho^4)].

Substituting rho=r-a r^3/3+O(r^5) yields

vol_g_a(B(0,r))/(omega_n r^n)
 = 1 + [2n(n-1)a/(3(n+2))]r^2 + O(r^4).

Thus merely O(|x|^2) contact can change the scalar coefficient by an arbitrary amount. Little-o contact is doing essential work.

## Why a viscosity/contact argument does not yet solve closure

At a fixed scale, relative C0 tensor error e changes normalized volume by order e. The scalar coefficient is obtained only after division by r^2; the corresponding error is order e/r^2. In a convergent sequence, e_j -> 0 need not satisfy e_j=o(r^2) throughout the radius interval in which g_j has its comparison property. For example the scales e_j=j^(-2), R_j=j^(-2) give e_j/R_j^2=j^2. This scale example is an obstruction to an estimate, not an assertion that it is realized by admissible metrics.

The lemma would let a suitable smooth-contact characterization detect lower bounds, but no theorem equating the all-centers volumic condition with such a closed viscosity condition was established. General continuous tensors need not possess smooth second-order germs at every point, and pointwise expansions do not automatically produce continuous positive comparison-radius functions. Those are separate missing steps, not consequences of the displayed estimate.
