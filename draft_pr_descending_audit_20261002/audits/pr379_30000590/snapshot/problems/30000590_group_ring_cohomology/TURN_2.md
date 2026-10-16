# Author turn 2: ascending HNN extensions do not create the bad kernel

**Original unresolved, 2/5 turns.**
This turn tests a group-specific construction using Bass–Serre resolutions.
It proves closure under ascending HNN extensions and finite free products,
and writes an explicit group-ring presentation in the Baumslag–Solitar case.
The tree/normal-form and Mayer–Vietoris mechanisms are classical; no
historical novelty or unrestricted solution is claimed.

Call a type-FP group A good when H*(A;ZA) is finitely generated as a right
ZA-module. This is only temporary terminology for the property in the
question. It does not assert that every type-FP group is good.

## 1. Ascending HNN theorem

Let A be good and let phi:A→A be an injective endomorphism. Then

    G=<A,t | t^(−1) a t=phi(a) for every a in A>          (1)

is type FP and is good. Injectivity is needed for the embedded base group
and the Bass–Serre tree. Surjectivity of phi is not required.

The height homomorphism chi:G→Z sends t to1 and A to0. For q≥1 there is a
right ZG-module identification

    H^q(G;ZG) ≅ coker(1−T : H^(q−1)(A;ZG)→H^(q−1)(A;ZG)), (2)

and H^0(G;ZG)=0. The endomorphism T is defined below; it shifts coefficient
height by exactly one. The fact that 1−T is injective uses finite height
support and does not assume T is injective.

### Finite projective resolutions and the tree sequence

The HNN Bass–Serre tree has one vertex orbit and one edge orbit, both with
stabilizer abstractly A. Its augmented cellular sequence is the exact
sequence of left ZG-modules

    0→ZG tensor_ZA Z→ZG tensor_ZA Z→Z→0.                (3)

The two attaching maps are induced by the identity embedding and by phi
with the stable-letter transport. Induce a finite projective ZA-resolution
of Z to resolve each of the two permutation modules. Induction is exact
and preserves finitely generated projectives because ZG is free over ZA.
Lift the edge boundary map to these resolutions. Its mapping cone resolves
Z, has finitely generated projective terms, and has length at most n+1 if
the base resolution has length n. Thus G is type FP.

Applying the corresponding cochain construction, or taking the long exact
Ext sequence of (3) and the induction adjunction, gives the right-equivariant
Mayer–Vietoris sequence

    ...→H^(q−1)(A;ZG) --(1−T)--> H^(q−1)(A;ZG)
       →H^q(G;ZG)→H^q(A;ZG) --(1−T)--> H^q(A;ZG)→...
                                                               (4)

All commuting right ZG-actions are preserved. The Bass–Serre tree and the
normal form ensuring that A embeds are standard graph-of-groups inputs;
Davis's *Infinite group actions on polyhedra*, graph-of-groups discussion
and AppendixA, give the contractible-tree model. The cohomological sequence
and finite-resolution consequence needed here follow from (3) as above.

### Formula for the transport and its grading

On the usual inhomogeneous A-cochains with values in the left A-module ZG,
put

    (Tf)(a_1,...,a_q)=t f(phi(a_1),...,phi(a_q)).         (5)

This also applies in degree0. The relation a t=t phi(a) shows directly that
T commutes with the cochain differential: in the first term, multiplication
by a_1 on t is replaced by t phi(a_1); the remaining terms use that phi is
a homomorphism. Multiplication on the right of coefficient values commutes
with (5). Formula (5) is the second incidence map in (4), with an irrelevant
possible global choice of edge orientation fixing the sign.

Write (ZG)_k for the subgroup spanned by elements of height k. It is a left
ZA-submodule, and

    ZG=direct sum_(k in Z) (ZG)_k.

Since A has a projective resolution with every term finitely generated,
cohomology commutes with this direct sum. Hence

    H^q(A;ZG)=direct sum_(k in Z) H^q(A;(ZG)_k).         (6)

Every individual class has finite height support. Formula (5) sends the
k-summand into the (k+1)-summand; the same statement follows on cohomology
by representing a homogeneous class with coefficients in (ZG)_k.

If u is nonzero, let k be its lowest nonzero height. The k-component of
(1−T)u is u_k, since u_(k−1)=0. Thus 1−T is injective. This argument requires
neither T-injectivity nor a completion of the direct sum. It would fail for
an infinite product or a formal series with support unbounded below, neither
of which is the coefficient module here. Sequence (4) now gives (2).

Finally, finite projective base cochains and the left-ZA freeness of ZG give

    H^i(A;ZG) ≅ H^i(A;ZA) tensor_ZA ZG                 (7)

as right ZG-modules. One can see this termwise for finitely generated
projectives, then use exactness of tensoring with the free left ZA-module
ZG. Since A is good, each module in (7) is finitely generated, and so are
the cokernels in (2). There are only finitely many degrees. This completes
the theorem.

The special identity incidence map is essential. For a general nonascending
HNN extension, both incidence maps may have kernels. The lowest-height
argument then exposes a potentially nonzero kernel of one incidence map
rather than proving injectivity. Such an extension is not settled here.

## 2. An explicit infinite-index example

Take A=<a> infinite cyclic and phi(a)=a^m, with m≥1. Thus

    G_m=<a,t | t^(−1)a t=a^m>.

For m>1 this is a genuinely ascending, non-surjective case. The two-term
resolution of the infinite cyclic base gives

    H^0(A;ZG_m)=0,
    H^1(A;ZG_m)=ZG_m/(a−1)ZG_m.

A 1-cocycle f is determined by f(a)=v, and
f(a^m)=(1+a+...+a^(m−1))v. Hence (5) induces left multiplication by

    t S_m,       S_m=1+a+...+a^(m−1)

on the displayed quotient. It is well-defined because

    t S_m(a−1)=t(a^m−1)=(a−1)t.                        (8)

It follows from (2) that H^i(G_m;ZG_m)=0 for i≠2 and

    H^2(G_m;ZG_m)
       ≅ ZG_m / [(a−1)ZG_m + (1−t S_m)ZG_m].           (9)

This is a cyclic right-module presentation with two relations. For m=1 it
reduces to the usual trivial Z-module in degree2 for Z². For m>1, replacing
the module by an abelian group of finite rank is not justified by (9).
The example illustrates that infinite-index ascending behavior does not by
itself force a failure of group-ring finite generation.

## 3. Finite free products preserve the property

If A and B are good, then G=A*B is type FP and is good. The Bass–Serre tree
now has two vertex orbits with stabilizers A,B and one edge orbit with
trivial stabilizer. Inducing the two finite resolutions and using the tree
mapping cone proves type FP. For q≥2, right-equivariant Mayer–Vietoris gives

    H^q(G;ZG) ≅ [H^q(A;ZA) tensor_ZA ZG]
                   direct sum [H^q(B;ZB) tensor_ZB ZG]. (10)

In degree1 it gives an extension whose quotient is the sum of the two
induced H^1 modules and whose submodule is a quotient of ZG=H^0(1;ZG).
Both ends are finitely generated; lift finitely many quotient generators
and adjoin generators of the submodule to prove finite generation of the
middle. Degree0 is the elementary invariant module from turn1. Induction
extends the statement to any finite free product.

Together with turn1's finite-index equivalence, this rules out constructions
that only iterate these operations starting from known good groups. It does
not assert closure under arbitrary amalgams, arbitrary subgroups or arbitrary
direct products with torsion in group-ring cohomology. Those require separate
kernel or Tor controls.

## 4. Precise obstruction for the next route

For a general graph of type-FP groups, the tree resolution still makes the
fundamental group type FP when the edge and vertex resolutions are finite.
The right-equivariant cohomology sequence identifies the possible new
failure with kernels of maps between induced vertex and edge cohomology
modules. Finite generation of those terms alone does not force finite
generation of a kernel; turn1's noncoherent-ring example shows the logical
problem. In the ascending case the grading removes this kernel, so that
route is closed without a counterexample.

The original remains unresolved2/5. Next consider coefficients/torsion or
nonascending incidence maps whose kernels may genuinely escape the finite
module presentations. Every prospective counterexample must still realize
a group of finite-length type FP and its actual right action, not merely
an abstract module map.
