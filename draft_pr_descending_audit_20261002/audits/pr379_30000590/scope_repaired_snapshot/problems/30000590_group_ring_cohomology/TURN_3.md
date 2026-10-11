# Author turn 3: product cohomology and the integral torsion boundary

**Original unresolved, 3/5 turns.**
The construction route here is a direct product. Integral Kunneth and
Bockstein sequences isolate the exact possible failure. They are standard
homological machinery and are credited as such; no general product closure
without the stated hypotheses or new counterexample is claimed.

For a type-FP group A set M_i=H^i(A;ZA), with its natural right action.
For B set N_j=H^j(B;ZB). “Finitely generated” below always means over the
specified group ring, not as an abelian group.

## 1. The product theorem and exact obstruction

If A,B are type FP, then A×B is type FP. There is a natural short exact
sequence of right Z[A×B]-modules

    0 → direct sum_(i+j=n) (M_i tensor_Z N_j)
      → H^n(A×B;Z[A×B])
      → direct sum_(i+j=n+1) Tor_1^Z(M_i,N_j) → 0.       (1)

All sums are finite. The right action on each tensor/Tor term comes from
the separate commuting A and B actions. An abelian-group splitting of (1)
is not asserted to be equivariant and is not used.

Suppose now that A and B already satisfy the finite-generation property
in the question. Then:

**Theorem.** A×B satisfies that property if and only if every
Tor_1^Z(M_i,N_j) is finitely generated as a right Z[A×B]-module.
In particular, the answer is affirmative for A×B if all M_i, or all N_j,
are torsion-free as abelian groups.

### Proof of the chain model and finiteness implication

Choose finite projective resolutions P_*,Q_* of the trivial modules for A,B.
Their tensor product over Z, with the usual total differential, is a finite
projective resolution for A×B. The terms are projective over ZA tensor_Z ZB:
a tensor of two summands of finite free modules is again such a summand.
Exactness follows from the ordinary tensor-product resolution argument over
Z, since these complexes are free as abelian groups and both have homology
Z concentrated in degree0.

Let C^*=Hom_ZA(P_*,ZA) and D^*=Hom_ZB(Q_*,ZB). Finite projectivity gives the
termwise natural isomorphism of product-group cochains with Tot(C^* tensor_Z D^*).
It is immediate for finite free modules and passes to their direct summands.
Every term of C,D is free as an abelian group, since it is a direct summand
of a free abelian group. The integral cochain Kunneth sequence gives (1).

One can see why there are precisely these two terms without any Noetherian
assumption on group rings. Over Z, boundaries and cycles are free abelian.
The short sequence from cycles into C^i onto the next boundary splits as
abelian groups. Consequently C decomposes, noncanonically, into the two-term
free resolutions B^i→Z^i of its cohomology M_i, placed in degrees i−1,i.
Tensoring such resolutions gives tensor products in degree i+j and Tor_1
in degree i+j−1; higher Tor over Z vanishes. The usual canonical tensor
map and quotient identification yield the natural short exact sequence,
so all group actions preserve it even though the chosen splittings need not.

If M_i has finitely many ZA-generators and N_j has finitely many ZB-generators,
the pairwise tensors of these generators generate M_i tensor_Z N_j over the
product group ring. Thus the left term U_n of (1) is finitely generated.
If the right term V_n is finitely generated, lift its generators and adjoin
generators of U_n to obtain finite generation of the middle. Conversely a
finitely generated middle has a finitely generated quotient V_n. A finite
direct sum is finitely generated iff each summand is. This proves the exact
criterion. Finally torsion-free abelian groups are flat over Z, so the
corresponding Tor groups vanish and give the stated sufficient condition.

It would be invalid to deduce finite generation of Tor only from finite
generation of M_i,N_j over their non-Noetherian group rings. Sequence (1)
identifies that missing assertion; it does not prove it.

## 2. Field coefficients have no product obstruction

Fix a field k. For groups of type FP over k, let M_i^k=H^i(A;kA) and
N_j^k=H^j(B;kB). The same finite projective model gives the canonical
right k[A×B]-module isomorphism

    H^n(A×B;k[A×B]) ≅ direct sum_(i+j=n) M_i^k tensor_k N_j^k. (2)

**Theorem.** Total group-ring cohomology for A×B is finitely generated over
k[A×B] if and only if the total cohomologies for A and for B are finitely
generated over kA and kB respectively.

The forward direction needs detection as well as Kunneth. First, each
factor has some nonzero group-ring cohomology. Otherwise its finite dual
projective cochain complex would be acyclic. A bounded acyclic complex of
projectives is split/contractible, as follows by splitting the surjection onto
the last projective and inducting. Dualizing would make the original finite
resolution complex contractible, contrary to its degree-zero homology k.

Choose one nonzero N_j^k. If the product cohomology is finitely generated,
each summand M_i^k tensor_k N_j^k of (2) is finitely generated over k[A×B].
Write a finite generating family as finite sums of simple tensors. Let M_0
be the kA-submodule generated by all first tensor coordinates appearing in
those sums. The full product-group orbit of these generators stays in the
image of M_0 tensor_k N_j^k. Therefore

    (M_i^k/M_0) tensor_k N_j^k=0.

A nonzero vector space is faithfully flat over a field, so M_i^k=M_0. Hence
M_i^k is finitely generated. Interchanging the factors proves the other
claim. There are finitely many nonzero degrees. The reverse direction is
the elementary tensor-generator argument already used above.

This is a statement for one fixed field, not a deduction of integral
finiteness from all fields and not the predecessor PD-over-fields problem.

## 3. Integral PD factors cannot manufacture a counterexample

If B is an integral Poincare duality group of dimension d, its group-ring
cohomology is concentrated in degree d and equals an infinite cyclic
orientation module Z_w. Formula (1) reduces to

    H^(i+d)(A×B;Z[A×B]) ≅ M_i tensor_Z Z_w.             (3)

In particular, A×B satisfies the original finite-generation property if
and only if A does. On the right, B acts only through multiplication by
+1 or −1, so a finite set generates over the product group ring exactly
when its first coordinates generate over ZA. This credits the standard PD
input and proves a construction obstruction: adjoining any integral PD
factor only shifts the same modules. It neither repairs nor produces the
missing finiteness. No assertion about recognizing integral PD from field
coefficients is involved.

## 4. Bockstein identifies fixed-torsion kernels

For m≥2, multiplication by m on ZA gives an exact sequence of coefficient
bimodules

    0→ZA --m--> ZA→(Z/m)A→0.

Its natural right-equivariant long cohomology sequence yields

    0→M_i/mM_i → H^i(A;(Z/m)A) → M_(i+1)[m]→0,         (4)

where M[m]={x:mx=0}. Since the terms are killed by m, finite generation as
right ZA-modules and as right (Z/m)A-modules are the same question.

If M_i is finitely generated, (4) implies the exact equivalence

    H^i(A;(Z/m)A) finitely generated
      iff M_(i+1)[m] finitely generated.                (5)

The first implication is passage to a quotient. The converse uses the finite
generation of M_i/mM_i and lifts generators as before. A type-FP integral
group also has a finite projective resolution over (Z/m)A by reduction:
the integral resolution is free over Z and resolves the flat Z-module Z,
so reduction preserves its exactness. Thus all relevant degree ranges are
finite, and (5) can be applied to total cohomology.

For a particularly transparent Tor term, if an abelian module N is killed
by a prime p, there is a natural isomorphism

    Tor_1^Z(M,N) ≅ M[p] tensor_Fp N.                    (6)

Indeed the formula holds for N=Fp by the two-term resolution of Fp, and both
sides commute with arbitrary direct sums of Fp-vector spaces; naturality
makes the resulting isomorphism independent of a basis. It is equivariant
for any commuting group actions on M,N. Consequently, if M[p] and N are
finitely generated over their respective group rings, this Tor term is
finitely generated over the product group ring.

The formulas do not assert that all torsion is killed by one fixed prime,
or that all positive cases in the source have equivariant decompositions
into such pieces. An abelian or associated-graded splitting is insufficient
for those stronger conclusions. Nor does control for each m establish an
unproved global finite-generation assertion about integral cohomology.

## 5. A degree/sign control for the Tor route

Take two purely algebraic cochain complexes

    C: Z --m--> Z,      D: Z --n--> Z,

in degrees0,1, with m,n positive. Their only individual cohomology is Z/m
and Z/n in degree1. The tensor total complex is

    Z --(m,n)--> Z² --(−n,m)--> Z.

Writing g=gcd(m,n), its cohomology is Z/g in both degrees1 and2, and zero
in degree0. The kernel of the last differential is generated by (m/g,n/g),
and the preceding image is g times that generator. The last cokernel is
Z/(m,n). Thus the lower degree is exactly the Tor term in (1), while the
upper degree is the tensor term. Ignoring Tor or shifting its degree the
wrong way would miss a whole cohomology group.

These small complexes are not asserted to be dual group resolutions. This
is a control for the algebraic construction, not a counterexample to the
group-ring finite-generation question. The finite checker verifies the signs, torsion degrees,
fixed-modulus kernels and finite tensor-coordinate generation argument.

## 6. Remaining gap after the product route

The product method is fully positive over fields and under the integral
flat-cohomology condition. General integral products reduce to the actual
Tor modules of the factors. To exploit this for a counterexample, one would
need genuine FP groups with the requisite non-finitely-generated torsion
kernel/Tor module. No such factor has been found. The known Coxeter and
Bestvina–Brady formulas cannot simply be treated as arbitrary module
realization theorems.

The original remains unresolved3/5. The next route should seek geometric
or finite-support control of integral cocycles, or a genuinely realizable
nonascending incidence kernel, rather than repeat an unsupported field-to-
integral assertion.
