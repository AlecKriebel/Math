# What the genus-one calculation does and does not refute

This supplements the independent audit of problem 30004711. It does not alter the frozen candidate report or introduce a new volume theorem.

## Precise answer

On the same spin stack, with the same forgetful map and the standard complex orientation, the compactified algebraic calculation gives integral c1(F)=-1/16 and integral c1(F^dual)=+1/16. Consequently an actual torsion-induced Euler form that extends as the Euler form of a connection on F, respectively F^dual, would have the corresponding integral. Under that extra hypothesis it cannot equal the Theta integral 1/8. Thus the coefficient-one formula together with this stronger, representative-level extension assertion is inconsistent in genus one.

The bundle extension nu=F|S, however, is strictly weaker than that hypothesis. The OWR conjunction of an open Euler-integral formula and a bundle extension does not by itself determine the open integral.

## Why normalization of the Euler class is insufficient

For (g,n)=(1,1), S is noncompact of real dimension two. Let e_0 be an Euler form extending over the compactified spin stack and representing the prescribed compactified class. Let e_tau be the Euler representative occurring in the torsion formula. Even if these represent exactly the same ordinary class on S, they need only satisfy

e_tau-e_0=d alpha

for a one-form alpha on S. On a compact exhaustion S_R, Stokes' theorem gives

integral_(S_R) e_tau = integral_(S_R) e_0 + integral_(boundary S_R) alpha.

If both total integrals exist, the limit of the boundary term is their difference. There is no reason for it to vanish merely because both Euler forms have the standard Chern-Weil normalization. Changes of connection have precisely this exact-form transgression property.

In particular, restriction to a noncompact curve loses the compactified top-degree class. Boundary divisors can distinguish extensions that have the same open restriction. An integral of an ordinary Euler cohomology class on S, without a specified representative and adequate boundary behavior, is not a determined number. The Weil-Petersson exponential does not fix this in genus one, since only its degree-zero term can contribute.

## The exact missing comparison

It would suffice to prove either:

1. The torsion-induced representative e(nu), with fully specified orientation and spin-stack conventions, is the canonical Euler representative to which Norbury's compactification theorem applies; or
2. Its integral equals the compactified integral of the class +c1(F) or -c1(F), with no residual boundary/current correction.

A smooth extension of the actual connection to the stated oriented bundle would be a sufficient special case. A bundle isomorphism on the open space is not.

Therefore:

- With only the displayed open Euler formula and bundle extension: no numerical contradiction has yet been proved.
- With the additional canonical representative/compactified-class integration identification: Vhat=-1/16 for F, or +1/16 for F^dual, contradicting V^Theta=1/8.
- Neither conclusion identifies OWR's intended torsion measure with the later normalized N. That requires its own verified convention map.

Here the sign alternatives concern the uniform standard complex orientation or its dual. Arbitrary independent sign changes on parity components constitute a further change of conventions; they are not silently included.
