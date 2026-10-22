# An admitted deformation with no uniformly positive single-direction repair

E-6322, shared pass 4, 16 October 2026.

## 1. Precise conclusion and its limit

There exists an identity-trace, orientation-preserving C^1 homeomorphism y of the unit ball, with finite frozen energy, such that for every fixed unit target direction e there is no map v satisfying all of

v in W^{1,6}(B_1;R^3),  Tr v=Id,
v-y is parallel to e almost everywhere,
det Dv>=delta almost everywhere for some delta>0.        (1)

In particular, one cannot complete the pass-4 mixed-moment theorem by asserting that every admitted map has a uniformly positive-Jacobian endpoint in some fixed one-component slice.

The conclusion concerns a fixed target direction and a lower bound on the entire original ball. It does not rule out endpoints whose rank-one gradient differences have a varying target direction, nor does it by itself exclude repairs with a positive lower bound only on a smaller region.

The example is not a minimizer. With its affine identity trace, strict convexity in the gradient and the null-minor identities make the identity the unique minimizer. Thus this is an obstruction to a class-level repair lemma, not a counterexample to E-6322 or an impossibility theorem for a minimizer-specific repair construction.

## 2. The radial finite-energy map

Choose

1/6<kappa<=1/2,
L(r)=log(e/r),
s(r)=r^{1/2}L(r)^kappa,
y(x)=s(|x|)x for x!=0,  y(0)=0.

The radial target radius is

R(r)=r s(r)=r^{3/2}L(r)^kappa.

Its derivative is

R'(r)=s(r)[3/2-kappa/L(r)]>0.

Since R(0)=0 and R(1)=1, y is a radial homeomorphism of B_1 onto itself with identity complete trace. Its tangential stretches are s(r), and its radial stretch is s(r)q(r), where

q(r)=3/2-kappa/L(r),  1<=q(r)<3/2.

Consequently

J_y=s(r)^3q(r)=r^{3/2}L(r)^{3kappa}q(r)>0

away from the origin. The gradient tends to zero at the origin, so y is C^1 there and has bounded gradient. All positive energy terms are integrable. The remaining integral is comparable to

integral_0^1 r^2 J_y(r)^{-2} dr
asymp integral_0^1 dr/[r L(r)^{6kappa}],

which is finite because 6kappa>1. This verifies every full-class condition for any positive finite coefficients a,b,c,d, with G=Id.

## 3. Its projection-volume density is unbounded

Let z=y(x), let R=|z|, and put K(z)=det D(y^{-1})(z)=J_y(y^{-1}(z))^{-1}, away from the origin. The explicit inverse formula gives

K(z)=1/[R L(r)^{2kappa}q(r)].                            (2)

Set ell=log(e/R). From the definition of R,

ell=(3/2)L-1/2-kappa log L.

For L>=1 and kappa<=1/2,

L<=ell<=(3/2)L.

Therefore constants depending only on kappa give

K(z) asymp 1/[|z|(log(e/|z|))^{2kappa}].                (3)

The pushforward of Lebesgue volume on the original ball by the two-coordinate map (y_1,y_2) has density

rho(z_1,z_2)
=integral_{-sqrt(1-|z'|^2)}^{sqrt(1-|z'|^2)} K(z',t) dt,
where z'=(z_1,z_2).

This follows directly by change of variables through the radial homeomorphism. For h=|z'| sufficiently small, restrict the integral to 2h<=t<=1/2 and use (3):

rho(z') >= c integral_{2h}^{1/2} dt/[t(log(e/t))^{2kappa}].                (4)

The right side tends to infinity as h decreases to zero, because 2kappa<=1. For 2kappa<1 its growth is of logarithmic power type; for 2kappa=1 it is log-log. This lower bound holds on positive-measure annuli, so rho is essentially unbounded, not merely infinite on the central fiber.

The map and its inverse Jacobian are radial. The same conclusion holds for projection onto e-perpendicular for every unit target direction e.

## 4. A positive-Jacobian repair would bound the unchanged marginal

Suppose v satisfies (1), and write pi_e for orthogonal projection onto e-perpendicular. Then pi_e v=pi_e y. The full-trace degree/area-formula baseline for the frozen class applies to v: J_v>=delta>0, its trace is Id, and it is W^{1,6}, so it is almost-everywhere one-to-one onto B_1 and the usual integral change-of-variables formula holds. No pointwise homeomorphism of v is assumed.

For any nonnegative continuous compactly supported test function f on e-perpendicular,

integral_{B_1} f(pi_e y(x)) dx
=integral_{B_1} f(pi_e v(x)) dx
<=delta^{-1} integral_{B_1} f(pi_e v(x)) J_v(x) dx
=delta^{-1} integral_{B_1} f(pi_e z) dz
<=2delta^{-1} integral_{e-perpendicular} f.

The factor 2 is the maximal chord length of the unit ball in direction e. Hence the unchanged projection-volume density would satisfy

rho_e<=2/delta almost everywhere,

contradicting (4). This proves the impossibility for every fixed direction.

## 5. Consequence for the current proof route

The mixed-moment theorem gains inverse-cube integrability if a feasible endpoint raises the determinant uniformly. This example shows why such an endpoint is not merely an available scalar extension: fixing two components fixes an entire projection-volume marginal, and that marginal may already forbid any uniform determinant lower bound for the third-component repair.

A full minimizer might have better marginals, but that improvement has not been proved. To use this route without circularity, one would need a genuine minimizer-specific marginal estimate or a coupled repair that changes more than one component while retaining admissibility. Neither the existence of the original smooth trace extension nor the pass-3 midpoint coercivity alone supplies that missing step.
