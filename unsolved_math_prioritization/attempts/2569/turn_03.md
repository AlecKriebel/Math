# Attempt 3: can modular padding hide a quaternionic Schur obstruction?

The previous attempt isolates a possible obstruction when the rational Schur index exceeds the p-adic one. The simplest test is the quaternion group Q_8 at an odd prime. Its faithful complex character chi has degree two and rational values, but rational Schur index two: the corresponding rational simple component is the Hamilton quaternion division algebra. Over a finite field k of odd characteristic that algebra splits, so kQ_8 has a faithful absolutely simple module W of dimension two.

A tempting counterexample family is G=Q_8 x P, where P is a nontrivial p-group and p is odd. The hope is that modular composition factors from P would conceal the missing factor of two and make the positive-monoid condition hold even though projective rational descent fails.

This fails uniformly, for a representation-theoretic reason that requires no character-table database.

## Restriction obstruction

Every rational QG-module, restricted to Q_8, has even multiplicity of chi after scalar extension to C. Indeed, every rational Q_8-module is a sum of four one-dimensional rational simples and copies of the four-dimensional rational quaternionic simple, whose complex character is 2 chi. Reducing modulo p and using p not dividing |Q_8| shows that every element in the rational reduction monoid for G, after restriction to Q_8, has even multiplicity of W. Restriction is exact, unlike the coinvariant operation rejected in Attempt 1.

On the modular side, kP is local. The module

    E = W tensor_k kP

is the projective cover of the simple W inflated to G. One way to see this is to use the component M_2(k) tensor kP of kG; a minimal-column module is projective and has simple top W. On restriction to Q_8,

    E restricted to Q_8 = W^{direct sum |P|}.

Since |P| is odd, this restriction contains W an odd number of times. Consequently [E] cannot belong to the rational reduction monoid. This supplies a mod-two separating functional, not just a failure to find a decomposition.

The same character obstruction proves nonsemiperfectness: the p-adic projective character of E is chi tensor the regular character of P. Its constituent chi tensor 1_P occurs once, violating rational Schur-index divisibility. The descent criterion in Attempt 2 therefore rules out a Z_(p)G-lift of E.

For the cyclic subfamily P=C_(p^a), the composition vector at the faithful simple is p^a, whereas every rational reduction vector has an even coordinate. For p=3,5,7,11 and a=1,2,3 the exact checker records this parity separator. The uniform argument, not the finite list, proves the family statement.

Outcome: adding a central odd p-group cannot manufacture a counterexample from the basic quaternionic obstruction. The monoid condition detects that obstruction before lattice lifting is attempted. A surviving example would need less transparent restriction behavior, or characteristic two, where the rational quaternionic component meets the modular radical instead of surviving as a semisimple p-prime-to-order component.
