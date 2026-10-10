# Independent audit of the odd two-torsion theta partial program

9 October 2026. Target 30001576 / OWR-4427-011.

## Disposition

**Accept the stated partial mathematical results, with the explicit interface
clarifications in `PROOF_INTERFACE_ADDENDUM.md`. The all-genus conjecture
remains unresolved.** No substantive mathematical counterexample or error
in the frozen partial propositions was found. The finite checker has a
coverage gap, repaired by an independent supplementary checker. The original
files are preserved byte-for-byte.

The frozen program used five of five proof approaches. This audit does not
add a sixth approach, assert novelty, certify an all-genus proof, or prove
an all-genus counterexample. It is an acceptance of the bounded partial
results and their limitations only.

## 1. Identity and scope of the frozen object

The supplied archive has 15,342 bytes and SHA-256
`faab5c1f34ad8e5f0892fb01c3797bfc427eb3e40d2f8d2f4684ab86e8596c05`.
Its eleven members are exactly the public packet, including a manifest of
the other ten files. All ten declared file hashes and byte counts match.
No source bodies appear among the archive members. The full original file
set was snapshotted before the audit and rechecked afterward.

The original OWR 39/2010 report, printed p.2324, defines the interior locus
using a singularity at an odd two-torsion point, equivalently multiplicity
at least three, and asks pure codimension g. It includes decomposable ppav.
Its empty genus-one and genus-two cases are vacuous. The stronger
reducedness conjecture in Grushevsky–Hulek, arXiv:1103.1857v2, Conjecture 2.2,
and the compactified gradient-zero locus are separate questions. This scope
is accurately maintained by the packet.

Primary sources:
- https://ems.press/content/serial-article-files/46295
- https://arxiv.org/abs/1103.1857v2

## 2. Level cover, equations, and finite dimension transfer: accepted

The principal level-eight subgroup is contained in the theta subgroup
Gamma(4,8); level eight is torsion-free, so the level moduli space is smooth.
The frozen phrase that one level moduli space is contained in the other
should be read as a subgroup inclusion inducing a finite cover, not a
subspace inclusion; the optional patch makes this literal interface precise.
Theta parity makes all even-order z derivatives of an odd characteristic
vanish at zero. Thus the g gradient coordinates cut out exactly the
multiplicity-at-least-three condition on support. Bundle changes of frame
preserve the ideal. The gradient's rank-g vector-valued modular-form
interpretation is also present in Grushevsky–Hulek, arXiv:1103.1858v2, §2.

The height theorem applies locally on the smooth cover. A component of a
finite union of finite images is the image of a component upstairs; finite
morphisms preserve that component's dimension. This proves the upper bound
g on the codimension of every component downstairs. Automorphism points
cause no failure: unramifiedness of the map to the coarse space is not
used. The stack has the same local dimensions. This argument asserts no
reducedness of the gradient scheme.

## 3. Components contained in the decomposable locus: accepted

The proof uses the finite collection of product images indexed by factor
dimension. When both factors have dimension at least two, the image has
dimension at most `N_a+N_(g-a)=N_g-a(g-a)`, and the elementary inequality
`a(g-a)>=g` suffices. It does not need a finite or injective product map.

For an elliptic factor, total odd parity gives exactly the two stated
possibilities. An odd elliptic theta function has a simple zero; an even
elliptic theta constant cannot vanish. Therefore the product-map preimage
is precisely `A_1 x (theta_null,h union I_h)`. Each even theta constant and
each odd gradient is nonidentically zero: move the characteristic by a
symplectic transformation and evaluate on a suitable elliptic product.
A finite union of proper closed zero loci cannot cover the irreducible
base. The source locus has dimension at most `N_h-1`, so its product image
has dimension at most `N_h=N_g-g`.

Together with the height upper bound, this proves the conclusion for
components actually contained in the decomposable locus. No arbitrary
product family is promoted to a component. A generically indecomposable
component remains outside this reduction. The known elliptic theta-null
component is consistent with Grushevsky–Salvati Manni, arXiv:0805.4148v1,
Theorem 6, but the dimension proof does not import that classification.

## 4. Cubic contraction and first-order rank: accepted

Direct differentiation of the defining Fourier series gives denominator
`2*pi*i*(1+delta_ab)` in the symmetric period coordinates. At a gradient
zero the Jacobian is the cubic contraction map, up to invertible diagonal
column rescaling. The annihilator of the cubic is the kernel of the dual
map. Trivial annihilator therefore gives full rank g and smooth
codimension g by the implicit function theorem.

At a general smooth point of a reduced component of codimension c, every
gradient-equation differential annihilates the component tangent space.
Jacobian rank is consequently at most c even if the ambient gradient
scheme is nonreduced. The cubic annihilator has dimension at least g-c,
so the cubic uses at most c essential variables. The zero cubic is
included. Rank deficiency alone proves neither excess dimension nor
failure of the conjecture. The product cubic with a nondegenerate
quadratic factor has the claimed full rank.

## 5. Three-odd-factor slice: accepted with exactly the stated local scope

An independent coefficient derivation confirms the heat scaling, parity,
normalization, signs in the three eliminated equations, coefficient three
on mixed terms, and residual coefficient `gamma_j-3*beta_j^2`. The
addendum supplies an all-genus weighted graph classification and the full
third jet of the first equation, including repeated-edge factorials.

Holomorphic implicit elimination is valid with diagonal parameters. The
nonzero coefficient condition can be made uniform on a sufficiently small
parameter neighborhood; the fourth-order remainder is bounded uniformly
there. The maximum-norm contradiction proves the actual germ of the
common zero set is diagonal inside the slice. The local intersection
inequality has the correct direction and applies to each irreducible germ
through the point. The slice codimension is `g(g-3)/2`, giving the desired
component dimension `N_g-g`. The g=3 case needs no residual equations.

The Fourier leading term is `32*pi^4*q`, so the coefficient condition holds
on a nonempty open part of the diagonal. The supplementary check also
recovers the next term `-256*pi^4*q^2`. At these points the full equation
Jacobian has rank exactly three. For g>3 the conclusion is pure local
codimension only. It does not imply smoothness of the entire gradient
scheme or reducedness, and it does not put arbitrary global components
through this diagonal locus.

## 6. The two imported dimension interfaces: accepted, now explicit

The rank-one induction uses the relative singular locus S, not the
singular locus of the total theta divisor defined additionally by second
derivatives. Ciliberto–van der Geer's Theorem (2.4) gives the required
`N_h-1` dimension. The other boundary type is a relative theta divisor over
`I_h`, also of dimension at most `N_h-1` under the lower-genus hypothesis.
The boundary Cartier step should be read on a sufficiently fine level
cover, followed by finite dimension descent. This removes any unnecessary
coarse-quotient Cartier assumption.

The rank-one boundary intersection hypothesis is indispensable. Mere
noncompleteness does not guarantee intersection with that open stratum.
The low-genus import is Grushevsky–Hulek, arXiv:1103.1858v2, Theorem 1.2;
Theorem 1.3 only bounds certain additional boundary components. Neither is
an unrestricted higher-genus boundary classification.

The spin-Jacobian dimension is the r=2 case of Teixidor's theorem, where r
is projective dimension. The addendum makes the citation and the genus-five
endpoint explicit. Finite spin marking and Torelli preserve dimension, so
`N_g-(3g-6)=g+(g-3)(g-4)/2>g` for g>=5. This natural family cannot itself
supply an excess-dimensional component. Each irreducible family component
must be contained in some larger gradient-locus component; the argument
need not place all family components in one common irreducible component.

## 7. The 2023 source and its finite-jet lemma

The exact v2 Theorem 5, Lemma 23, and Proposition 24 were inspected, using
the locally retained PDF and public versioned source. The exact theorem
speaks about components containing the diagonal; the broader introductory
phrasing is not a substitute for that hypothesis. Proposition 24 uses the
same three-odd-factor slice and cites Lemma 23. The theorem's assertions
are broader than the packet's independently justified generic-point claim.

The packet's criticism of Lemma 23 is mathematically sound and appropriately
limited. In an Artinian jet quotient each equation image is nilpotent, so
literal algebraic independence gives no positive count. If independence
instead refers to polynomial representatives, `u` and `uv` are independent
but generate the height-one ideal `(u)`. This invalidates that proposed
criterion, not the theta-specific conclusion. The convergent zero-set proof
supplies the needed local dimension argument here. No allegation of a false
theta theorem or resolution of its smoothness claim follows.

Public version record: https://arxiv.org/abs/2307.05238v2

## 8. Executable validation and adversarial controls

The original checker has no assert statements and writes only to stdout.
Its normal, -O, and -OO runs all reproduce the frozen result SHA-256
`3bf3b5c5b185aba040a4afe1e1d34d662038e027a77beefb43c243dad2136dbe`.
No assertion-disabled or file-writing repair is needed.

One meaningful surviving mutation was found: removal of all repeated-edge
factorials still passes the original checker. The compared first jets only
have degree at most two, and the compared residual cubics contain distinct
edges. The original code is correct, but those tests do not validate its
factorial implementation. Other original mutations involving parity,
a mixed coefficient, elimination sign, and the residual cubic coefficient
are rejected.

`independent_checks.py` uses ordered operator words with coefficient `1/d!`,
not the original multiset enumeration. It checks the entire third jet in
genera 3 through 8, eliminated cubics, exact Fourier coefficients, symbolic
dimension identities, and cubic flattening ranks. Six adversarial controls
alter factorials, heat scaling, cross-term multiplicity, elimination sign,
residual coefficient, or Fourier coefficient. Each is required to fail in
normal, -O, and -OO modes. Checks use explicit exceptions and remain active
under optimization.

Actual read-only probes run at UID/EUID 1000, with directory mode 0555 and
input files mode 0444. Attempts both to create a file there and to append to
the original checker are denied. Both checkers then run normally in that
working directory in all three optimization modes, and their input hashes
remain unchanged. `CHECKER_PROBES.json` records the outcomes.

These are finite exact sanity checks. The all-genus local proof is the
convergent argument, not an extrapolation from those checks. There is no
computational certificate for the global conjecture.
