# A reversible three-species mass-action continuum without a common factor

## Abstract

We give a reversible mass-action system on three species with one linkage
class, ten complexes, twenty directed reactions, and positive integer rate
constants.  Its stoichiometric subspace is all of \(\mathbb R^3\).  The unique
positive compatibility class therefore contains an entire positive algebraic
ellipse of equilibria.  Nevertheless, the three coordinate polynomials of the
mass-action vector field have greatest common divisor \(1\) over
\(\mathbb Q[x,y,z]\).  The equilibrium continuum is a height-two component of
the steady-state ideal, rather than a hypersurface shared by the vector-field
coordinates.  In fact, the steady-state ideal is radical: over the algebraic
closure its variety is the conic together with fifteen reduced isolated
points.  We also prove that three is the smallest possible number of species
and that, for three species and one linkage class, stoichiometric rank two
would force a common factor.

## Theorem

There is a reversible mass-action system on species \(X,Y,Z\) with:

- one linkage class;
- ten complexes and ten reversible pairs (twenty directed reactions);
- positive integer rate constants;
- stoichiometric subspace \(S=\mathbb R^3\);
- a compact positive real algebraic curve of equilibria; and
- \(\gcd(F_1,F_2,F_3)=1\) in \(\mathbb Q[x,y,z]\).

Its steady-state ideal is radical of dimension one and has exactly two minimal
primes over \(\mathbb Q\): the conic prime and one maximal ideal of degree
fifteen.

In particular, with

\[
x_0=\left(\frac32,\frac12,1\right),
\]

the compatibility class \(P(x_0)=\mathbb R_{>0}^3\) contains infinitely many
distinct positive equilibria and a connected positive-dimensional algebraic
continuum.

## The exact network

Index the complexes as follows.

| index | exponent vector | complex |
|---:|:---:|:---|
| 0 | \((0,0,0)\) | \(0\) |
| 1 | \((0,0,1)\) | \(Z\) |
| 2 | \((0,0,3)\) | \(3Z\) |
| 3 | \((0,1,1)\) | \(Y+Z\) |
| 4 | \((0,3,0)\) | \(3Y\) |
| 5 | \((1,0,1)\) | \(X+Z\) |
| 6 | \((1,1,0)\) | \(X+Y\) |
| 7 | \((1,1,1)\) | \(X+Y+Z\) |
| 8 | \((2,1,0)\) | \(2X+Y\) |
| 9 | \((3,0,0)\) | \(3X\) |

For every row below, both displayed directions are reactions.  The third
column is the rate in the left-to-right direction, and the fourth is the rate
in the right-to-left direction.

| indices | reversible pair | \(\kappa_{i\to j}\) | \(\kappa_{j\to i}\) |
|:---:|:---|---:|---:|
| 0,1 | \(0\rightleftarrows Z\) | 845740 | 7732494 |
| 0,4 | \(0\rightleftarrows 3Y\) | 702464 | 3920 |
| 0,6 | \(0\rightleftarrows X+Y\) | 437290 | 4380128 |
| 1,7 | \(Z\rightleftarrows X+Y+Z\) | 1405575 | 5600 |
| 2,4 | \(3Z\rightleftarrows 3Y\) | 706384 | 900816 |
| 2,7 | \(3Z\rightleftarrows X+Y+Z\) | 1518755 | 6873328 |
| 2,9 | \(3Z\rightleftarrows 3X\) | 3920 | 896896 |
| 3,4 | \(Y+Z\rightleftarrows 3Y\) | 3863552 | 3920 |
| 5,9 | \(X+Z\rightleftarrows 3X\) | 3863552 | 15680 |
| 8,9 | \(2X+Y\rightleftarrows 3X\) | 4346496 | 658560 |

This table is also supplied as `network.csv`, with one row per directed
reaction.

## Mass-action vector field

Directly summing

\[
\kappa_{y\to y'}x^y(y'-y)
\]

over the twenty directed reactions gives \(F=(F_1,F_2,F_3)\), where

\[
\begin{aligned}
F_1={}&-3380608x^3+4346496x^2y-6878928xyz-4380128xy\\
&+7727104xz+1530515z^3+1405575z+437290,\\[2mm]
F_2={}&658560x^3-4346496x^2y-6878928xyz-4380128xy\\
&-2722048y^3+7727104yz+3637907z^3+1405575z+2544682,\\[2mm]
F_3={}&2706368x^3+13746656xyz-3863552xz+2706368y^3\\
&-3863552yz-5168422z^3-7732494z+845740.
\end{aligned}
\]

The field is visibly not identically zero; for example,

\[
F(1,1,1)=(807316,-2353772,-622888).
\]

## Graph and stoichiometry

Every undirected edge in the table occurs in both directions, so the network
is reversible.  The underlying graph is connected.  For example, starting at
complex 0 one reaches 1, 4, and 6; from 1 one reaches 7; from 7 one reaches 2;
from 2 one reaches 9; and 4 and 9 lead to the remaining vertices 3, 5, and 8.
Thus there is exactly one linkage class.  The graph has ten vertices and ten
undirected edges, so it has one undirected cycle.

Three reaction differences are

\[
0\to Z=(0,0,1),\qquad
0\to3Y=(0,3,0),\qquad
0\to X+Y=(1,1,0).
\]

Their determinant is \(-3\).  Hence

\[
S=\mathbb R^3.
\]

There are no conservation laws, and every positive compatibility class is the
whole positive orthant.

## The positive algebraic equilibrium continuum

Define

\[
L=z-x-y+1
\]

and

\[
Q=7x^2-2xy-16x+7y^2-16y+16.
\]

The ideal \(\mathfrak p=(L,Q)\) is prime of height two.  Indeed, eliminating
\(z\) using \(L\) leaves the plane conic \(Q=0\).  Its homogenized symmetric
matrix is

\[
\begin{pmatrix}
7&-1&-8\\
-1&7&-8\\
-8&-8&16
\end{pmatrix},
\]

whose determinant is \(-256\).  Thus the projective conic is nonsingular and
irreducible, even over the algebraic closure.

An exact parametrization is

\[
\begin{aligned}
d(t)&=t^2-t+1,\\
x(t)&=\frac{t^2+3}{2d(t)},\\
y(t)&=\frac{3t^2+1}{2d(t)},\\
z(t)&=\frac{t^2+t+1}{d(t)}.
\end{aligned}
\tag{1}
\]

Direct expansion gives

\[
L(x(t),y(t),z(t))=Q(x(t),y(t),z(t))=0.
\]

The positivity is exact:

\[
d(t)=\left(t-\frac12\right)^2+\frac34>0,
\qquad
t^2+t+1=\left(t+\frac12\right)^2+\frac34>0,
\]

and the other two numerators are \(t^2+3\) and \(3t^2+1\).  Thus every point
in (1) is positive for every real \(t\).  On the open interval
\(I=(-1,1)\),

\[
z'(t)=\frac{2(1-t^2)}{d(t)^2}>0,
\]

so the parametrized points are pairwise distinct.  The image of \(I\) is
connected and one-dimensional, and it contains
\(x(0)=(3/2,1/2,1)=x_0\).

In fact the entire real conic is positive.  On \(L=0\), write
\(s=x+y=z+1\) and \(a=x-y\).  The equation \(Q=0\) is equivalently

\[
4\bigl(a^2+(z-1)^2\bigr)=(z+1)^2.
\]

It follows that \(1/3\le z\le3\) and
\(|a|\le(z+1)/2\), which implies \(x,y,z>0\).  Its real locus is therefore a
compact positive ellipse.

## Exact vanishing identities

The continuum is not certified merely by sampling.  For the following
polynomials \(A_i,B_i\), exact expansion gives

\[
F_i=A_iL+B_iQ\qquad(i=1,2,3).
\tag{2}
\]

They are

\[
\begin{aligned}
A_1={}&1530515x^2-3817898xy+1530515xz+4666074x\\
&+1530515y^2+1530515yz-3061030y\\
&+1530515z^2-1530515z+2936090,\\
B_1={}&-264299x+218645y-156175,\\[1mm]
A_2={}&3637907x^2+396886xy+3637907xz-7275814x\\
&+3637907y^2+3637907yz+451290y\\
&+3637907z^2-3637907z+5043482,\\
B_2={}&613781x+130837y-156175,\\[1mm]
A_3={}&-98\bigl(52739x^2-34794xy+52739xz-66054x\\
&\qquad+52739y^2+52739yz-66054y\\
&\qquad+52739z^2-52739z+131642\bigr),\\
B_3={}&-98(3589x+3589y-8767).
\end{aligned}
\]

Combining (1) and (2) proves \(F_i(x(t))=0\) identically for every real
\(t\), and hence in particular on \((-1,1)\).

## No common factor and the steady ideal

An exact multivariate gcd computation over \(\mathbb Q\) gives

\[
\gcd(F_1,F_2)=\gcd(F_1,F_3)=\gcd(F_2,F_3)=1.
\]

Consequently

\[
\gcd(F_1,F_2,F_3)=1.
\]

As an independent factorization check, each coordinate is, up to a nonzero
rational constant, an irreducible cubic in \(\mathbb Q[x,y,z]\).  The verifier
performs both the gcd calculation and the exact factorization.

Let

\[
K=(F_1,F_2,F_3)\subset\mathbb Q[x,y,z].
\]

Identity (2) says \(K\subset\mathfrak p=(L,Q)\), where \(\mathfrak p\) is a
height-two prime.  Thus \(\operatorname{ht}K\le2\).  On the other hand, in the
UFD \(\mathbb Q[x,y,z]\), a height-one prime containing \(K\) would be
generated by a nonconstant irreducible divisor of all three \(F_i\).  The gcd
calculation rules this out, so \(\operatorname{ht}K\ge2\).  Therefore

\[
\operatorname{ht}K=2,
\qquad
\dim\mathbb Q[x,y,z]/K=1.
\]

Moreover, \(\mathfrak p\) is a minimal prime of \(K\), so the positive conic is
an actual irreducible steady-state component.  At
\((3/2,1/2,1)\), the exact Jacobian \(DF\) has rank two.  Hence the component is
smooth and reduced locally at that point.

The full radical can also be determined exactly.  Put

\[
D=y^2-yz-y+\frac7{16}z^2-\frac18z+\frac7{16}.
\]

Modulo \(L\), this is \(Q/16\), so
\(\mathfrak p=(L,D)\).  The unique reduced lexicographic Gröbner basis of
\(K\), for \(x>y>z\), has the exactly verified form

\[
G_0,\qquad D H,\qquad D R,
\]

where \(G_0\) is monic linear in \(x\), \(H\) is linear in \(y\) with
nonzero constant leading coefficient, and \(R\in\mathbb Q[z]\) is an
irreducible polynomial of degree fifteen.  Define

\[
\mathfrak q=(G_0,H,R).
\]

Its reduced lexicographic basis is triangular of the form
\(x+r_x(z),y+r_y(z),R(z)\), so \(\mathfrak q\) is maximal of degree fifteen.
The exact verifier checks that \(D\notin\mathfrak q\), hence
\(\mathfrak p+\mathfrak q=(1)\), and reduces every product of a generator of
\(\mathfrak p\) with a generator of \(\mathfrak q\) to zero modulo the
Gröbner basis of \(K\).  Since also \(K\subseteq\mathfrak p\cap\mathfrak q\),
these checks certify

\[
K=\mathfrak p\mathfrak q=\mathfrak p\cap\mathfrak q=\sqrt K.
\]

Because \(R\) is separable in characteristic zero, over the algebraic closure
the second component consists of fifteen distinct points.  Thus the full
complex steady-state variety is the nonsingular conic, disjoint from fifteen
reduced isolated points.  The large coefficients of \(G_0,H,R\) are not
printed; the verifier derives them canonically from the displayed \(F_i\) and
checks this decomposition using exact rational arithmetic.

## Why this is not a disguised common-factor example

The mechanism is genuinely height two:

\[
F_i\in(L,Q),
\]

but no nonconstant polynomial divides all coordinates.  In particular:

- the stoichiometric class is three-dimensional, not a lower-dimensional
  plane on which the field vanishes identically;
- every species occurs in the reactions and the reaction differences span all
  three coordinate directions;
- the three coordinate polynomials are linearly independent and pairwise
  coprime;
- the field is not identically zero—for example, \(F(1,1,1)\ne0\) at a point
  off the conic; and
- the Jacobian has rank two at a point of the conic, so two independent steady
  equations cut out the local equilibrium curve.

Thus the continuum does not come from an absent species, a duplicated
coordinate, a zero vector field on a class, or multiplication of a smaller
field by one common polynomial.

## Minimality and structural obstructions

### Three species are necessary

No system on one or two species can satisfy the continuum-plus-gcd-one target.
For one species, a positive-dimensional equilibrium set forces the single
coordinate polynomial to vanish identically.  For two species:

- if \(\dim S=1\), all reaction vectors are collinear, so
  \(F=v\,f(x,y)\) for a fixed vector \(v\) and one scalar polynomial \(f\);
  any equilibrium makes \(f\) a common nonconstant factor, unless the whole
  field is zero;
- if \(\dim S=2\), the compatibility class is open in \(\mathbb R^2\).  A
  positive-dimensional semialgebraic common-zero set implies
  \(\dim\mathbb Q[x,y]/(F_1,F_2)\ge1\).  Unless both coordinates vanish, a
  height-one prime contains the steady ideal.  Factoriality of
  \(\mathbb Q[x,y]\) then gives a nonconstant irreducible polynomial dividing
  both coordinates.

The construction therefore attains the minimum possible number of species.

### Why full stoichiometric rank is necessary here

Suppose a three-species network has one linkage class and
\(\dim S=2\).  Choose a primitive integer vector \(w\) spanning
\(S^\perp\).  Connectivity of the complex graph implies that
\(w\cdot y=d\) is the same integer for every complex.  Consequently, under

\[
T_\lambda(x_1,x_2,x_3)
=(\lambda^{w_1}x_1,\lambda^{w_2}x_2,\lambda^{w_3}x_3),
\]

every coordinate satisfies

\[
F_i(T_\lambda x)=\lambda^d F_i(x).
\]

The torus action therefore preserves the equilibrium set.  Its infinitesimal
direction at a positive point \(p\) is
\((w_1p_1,w_2p_2,w_3p_3)\).  Its inner product with the compatibility-class
normal \(w\) is

\[
\sum_i w_i^2p_i>0.
\]

Hence this scaling direction is transverse to every positive compatibility
class.  Choose a smooth one-dimensional semialgebraic stratum of an equilibrium
continuum in one class.  The torus-action map on this stratum has differential
rank two by transversality, so its equilibrium image has semialgebraic
dimension two.  It follows that
\(\dim\mathbb Q[x,y,z]/(F_1,F_2,F_3)\ge2\).  Either the dimension is three, in
which case every \(F_i\) is zero, or a height-one prime contains the steady
ideal.  Since \(\mathbb Q[x,y,z]\) is a UFD, that prime is generated by a
nonconstant irreducible polynomial dividing every \(F_i\).  Thus a
one-linkage, rank-two construction necessarily has a nonconstant common
factor (or the zero field).  Rank one is already excluded by collinearity.  The
full rank \(S=\mathbb R^3\) of the example is therefore forced under the
one-linkage requirement.

### Complex and reaction counts

For a one-linkage, weakly reversible, full-rank three-species network, four
complexes cannot give an equilibrium continuum.  With four complexes, the
incidence Laplacian has rank three, and the map from its image to the
stoichiometric subspace is an isomorphism.  A positive equilibrium must
therefore be complex-balanced.  Two such equilibria would have proportional
monomial vectors; because the complex differences span \(\mathbb R^3\),
taking logarithms forces the concentrations to be identical.  Thus at least
five complexes are necessary.

The present construction uses ten complexes and ten reversible pairs.  It has
maximum complex degree three and deficiency

\[
10-1-3=6.
\]

The proved lower bound is five complexes.  No claim that ten complexes or ten
reversible pairs is globally minimal is made.

## Post-solution priority note

This construction and its exact verifier were completed before any literature
search.  A subsequent targeted primary-source audit found that Boros, Craciun,
and Yu explicitly asked whether a weakly reversible mass-action system could
have infinitely many positive steady states without a common factor.  Their
examples, including their reversible connected example, use a common-factor
hypersurface.  The construction above answers that published question by a
height-two component.

The latest closely related generic-geometry work revisits the earlier
common-factor example and proves that infinitely many compatible steady states
cannot persist on an open set of rate constants and totals.  That result does
not exclude an exceptional exact parameter choice such as the integer point
used here.  No prior example with the conjunction proved here was found in the
targeted audit through 2026-08-01; this is a conservative search report, not an
exhaustive priority claim.  Full citations and scope are recorded in
[`PRIORITY_AUDIT.md`](PRIORITY_AUDIT.md).

## Exact verification

Run

```text
.venv/bin/python weakly_reversible_continuum_no_common_factor/verify_construction.py
```

from the repository root.  The verifier reconstructs \(F\) from the raw
reaction list and checks, using exact rational polynomial arithmetic:

1. distinct nonnegative complexes and positive integer rates;
2. reverse support for every reaction;
3. graph connectivity and one linkage class;
4. stoichiometric rank three, maximum complex degree three, and deficiency six;
5. equality with the displayed vector field;
6. the identities \(F_i=A_iL+B_iQ\);
7. irreducibility of the conic;
8. direct rational-parametrization substitution;
9. the positivity and injectivity certificates;
10. all pairwise and total gcd assertions;
11. exact irreducibility of the primitive coordinate cubics; and
12. Jacobian rank two on the equilibrium curve; and
13. the complete radical decomposition into the conic prime and a degree-15
    maximal ideal.

Every asserted construction property is reconstructed from exact data; no
floating-point result is used as evidence for the theorem.
