# Turn 1: try to recover the full polynomial from the reduced invariant

**Result:** exact description of the lost information; no construction of
the full requested polynomial. This is the first substantive proof attempt.

The route is to use a known or topologically constructed one-variable
two-loop specialization, then recover the two-variable invariant from
theta symmetry. The obstruction can be determined exactly, rather than
being left as a dimension heuristic.

## 1. The invariant ring

Put

R = Q[x^±1,y^±1,z^±1]/(xyz-1),

and let G=S3 × C2 act by permutations and simultaneous inversion. Set

a=x+y+z, b=xy+yz+zx,
u=a+b, v=ab, D=(a-b)^2=u^2-4v.

**Proposition 1.** R^G=Q[u,v].

Proof. A symmetric Laurent polynomial becomes a symmetric ordinary
polynomial after multiplication by a sufficiently high power of xyz.
That power is 1 in R. The elementary-symmetric-polynomial theorem therefore
gives R^S3=Q[a,b], since the third elementary symmetric polynomial is 1.
There is no relation between a and b: the symmetric polynomial ring before
setting the third generator to 1 is Q[a,b,c]. Inversion interchanges a and
b. Taking invariants under that interchange gives Q[a+b,ab]. ∎

This is the Laurent analogue of the source's even-symmetric power-series
description. It uses simultaneous inversion, not independent changes of
the signs of exponents.

## 2. Exact kernel of the reduced specialization

Define r:R^G→Q[t^±1] by r(F)=F(t,1,t^-1). Along that locus,

a=b=s=t+1+t^-1, u=2s, v=s^2.

**Proposition 2.** ker(r)=(D) inside Q[u,v]. Its image is Q[s].

Proof. Divide any F(u,v) by the monic polynomial v-u^2/4, treating v as
the division variable. This gives

F(u,v)=(v-u^2/4)H(u,v)+J(u).

The specialization is J(2s). Since s is transcendental over Q inside
Q[t^±1], it vanishes only if J=0. Conversely D vanishes on the locus.
The image contains s=u/2, which proves the image assertion. ∎

There is also a useful multiplicative form:

D=(x-1)^2(y-1)^2(z-1)^2.

Indeed (x-1)(y-1)(z-1)=a-b after xyz=1. This explicitly exhibits a
nonzero invariant polynomial invisible to the specialization. For example
D(2,3,1/6)=25/9, whereas D(t,1,t^-1)=0 identically.

If Delta is fixed and normalized, the denominator
Delta(x)Delta(y)Delta(z) is a nonzero invariant. The same ambiguity occurs
for rational theta coefficients F/[Delta(x)Delta(y)Delta(z)]: adding
D H to the numerator does not change the reduced specialization, at any
point where it is defined.

## 3. Does cabling or low-order calibration remove it?

For every nonzero integer p,

D(x^p,y^p,z^p) is divisible by D(x,y,z) in R.

For p>0 this follows by factoring t^p-1=(t-1)(1+...+t^(p-1)); for p<0
the extra monomials are units. Thus repeatedly replacing all three
variables by a common power and then setting one variable to 1 still
annihilates the entire ideal (D). This does **not** assert a general
satellite formula: it identifies exactly why the common-power part of
such a reconstruction cannot recover the missing information.

In logarithmic variables x=e^h, y=e^k, z=e^(-h-k),

D = h^2 k^2(h+k)^2 + terms of total degree at least 7.

The expression is unchanged by (h,k)→(-h,-k), so in fact the next possible
total degree is 8. Consequently agreement of finitely many sufficiently
low Taylor coefficients also fails to detect D. The normalization at the
unknot evaluation x=y=z=1 is preserved by adding it.

## 4. What this proves, and what it does not

This is an obstruction to proving equality from the reduced invariant and
theta symmetry alone. It is **not** a pair of knots with identical reduced
invariants and different P_K^theta, and does not assert that every
polynomial in (D) is realizable by an actual knot. Additional topological
constraints may rule out some or all such ambiguities in a restricted
class; Ohtsuki's special genus-one formula is one reason not to conflate
the ambient polynomial ring with the set of realized values.

The route fails at recovery of the D-multiple. Next, try a genuinely
two-dimensional collection of topological data: Casson–Walker invariants
of all cyclic branched covers. Their algebraic residue transform must be
tested for injectivity before it can be used as a reconstruction theorem.

**Remaining full-target gap:** obtain a topological quantity controlling
the transverse D-part, and prove its equality, with exact normalization,
to the source's theta-diagram coefficient.
