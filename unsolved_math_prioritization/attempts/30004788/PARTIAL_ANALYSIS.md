# Iwahori restriction: known dependence and reconstruction obstructions

Status: partial analysis only. No general block model or novelty claim is made.

Current audited derivative, 8 October 2026. This file adds categorical and
normalization clarifications to the preserved original; it is not a new proof
attempt or a solution of the full problem.

## 1. Object and conventions

Let F be a non-Archimedean local field, G=GL_(n+1)(F), and H=GL_n(F), embedded
by h -> diag(h,1). Representations are smooth and complex. Write I_H for an
Iwahori subgroup of H and H_n for its complex Hecke algebra, with volume(I_H)=1.
The requested object is

    M(pi) = (Res_H pi)^(I_H),

This is the Hecke module corresponding, under the Iwahori type equivalence,
to the [T,1] Bernstein component of Res_H pi. The group representation and its
Hecke module are objects in equivalent categories, not literally the same
vector space. The Hecke module is generally infinite-dimensional. It is not the restriction of the finite-dimensional space
pi^(I_G) along an affine-Hecke inclusion.

Here “unramified generic” means irreducible, Whittaker-generic and spherical
under K_G=GL_(n+1)(O_F). Such representations are irreducible normalized
principal series of unramified characters. Steinberg products are interpreted
as normalized parabolic products of unramified twists of p-adic Steinbergs;
this working interpretation should be stated because the original question
does not specify it. These products need not be K_G-spherical. Reducible
standard modules and their generic constituents must also be distinguished.

Prasad's question is in the epilogue on p.2119 of OWR39/2021. Its preceding
tempered/projective conjecture is a different question. The finite Steinberg
of GL_n(F_q), inflated to K_H, is also a different object from St_n(F).

Source: [Prasad, Homological branching: recent results and beyond](https://yhzhumath.github.io/OWR_2021_39.pdf), pp.2118–2120.

## 2. A known negative answer to independence

Prasad's published Theorem 1 characterizes GL_2-invariant forms on irreducible
admissible GL_3 representations over a non-Archimedean local field: their
Weil–Deligne parameter must have a trivial one-dimensional summand whose
two-dimensional quotient corresponds to a generic GL_2 representation.

Choose a nontrivial unramified unitary character xi of F*; for example, set
xi to be trivial on O_F* and xi(varpi)=-1 for a uniformizer varpi. Then

    pi_0 = 1 x 1 x 1,        pi_1 = xi x xi x xi

are normalized GL_3 principal series. Each is irreducible: every ratio of
inducing characters equals 1, whereas the reducibility ratios are |.| and
|.|^(-1), neither of which is 1. Both are generic and K_G-spherical; their Weil-Deligne monodromy is zero. Their
parameters are 1⊕1⊕1 and xi⊕xi⊕xi. For pi_0 the complementary parameter
1⊕1 gives the irreducible generic GL_2 principal series 1 x 1. The parameter
of pi_1 has no trivial summand. Consequently

    Hom_GL2(pi_0,1) != 0,        Hom_GL2(pi_1,1) = 0.

These are maps from the restricted representation onto the trivial
representation, not embeddings of that representation into the restriction.
Let e_s denote the Bernstein projection for s=[T,1]. The trivial GL_2
representation lies in s: its normalized cuspidal support is the unordered
pair { |.|^(-1/2), |.|^(1/2) }, which consists of unramified characters.
Orthogonality of Bernstein blocks gives

    Hom_H(Res_H pi,1) = Hom_H(e_s Res_H pi,1).

Any nonzero map here is surjective. Exactness of I_H-invariants over C
(obtained by compact averaging) and the Iwahori type equivalence transport
this to the corresponding Hecke-module quotient. Thus M(pi_0) and M(pi_1)
cannot be isomorphic.

The GL_3 central characters are 1 and xi^3. Equality of those characters is
not required by the question or by Prasad's criterion. The center of the
embedded GL_2 is not the center of GL_3. Nontrivial unitarity excludes
xi=|.|^s for every real s, including s=0; xi^2=1 in the explicit choice
introduces no reducibility, since the inducing-character ratios remain 1.
The GL_2 complementary parameter 1+1 in the criterion is generic and is
different from the trivial target representation. This is an application of a 1993 theorem, not a new counterexample.

Source: [Prasad, On the decomposition of a representation of GL(3) restricted to GL(2) over a p-adic field](https://doi.org/10.1215/S0012-7094-93-06908-6), Duke Math. J.69 (1993),167–177, Theorems1–2, pp.169–172.

## 3. Rank-one extension check

The known projectivity classification and Gelfand–Graev identification imply
that for an irreducible generic GL_2 representation, its restriction to GL_1
is the regular smooth compact-induction model. Its unramified block is
A=C[t,t^(-1)]. Thus n=1 is an exception to an unqualified nonprojectivity claim.

An elementary warning comes from the exact sequence

    0 -> A --p(t)--> A -> A/(p(t)) -> 0,

where p has nonzero constant term. The middle module is always A, although
the embedding and quotient depend on p. At p=(t-a)^2 the quotient is cyclic
with nonzero nilpotent t-a, rather than a direct sum of two characters.
For a=2, multiplication by t in the basis (1,t) is

    T = ((0,-4),(1,4));     (T-2I)^2=0,     T-2I != 0.

Hence derivative characters or associated graded data do not specify the
extension. This is particularly important at repeated inducing parameters.

Source for the representation-theoretic rank-one statement: [Chan, Homological branching law](https://arxiv.org/abs/1905.01668), Theorems3.7–3.8. The displayed algebra calculation is self-contained.

## 4. Six orbit charts in rank two

Let V=span(e1,e2,e3), U=span(e1,e2), L=span(e3), and H=GL(U). A complete
flag is a line ell inside a plane P. The following ordered bases give six
H-orbit representatives; a flag uses the first one and first two vectors.

1. (e3,e1,e2)
2. (e1,e3,e2)
3. (e1,e2,e3)
4. (e1+e3,e1,e2)
5. (e1+e3,e2,e1)
6. (e1,e2+e3,e2)

Their orbit dimensions are respectively 1,1,1,2,3,2. To check completeness,
first separate ell=L, ell subset U, and a mixed line. If ell=L there is one
orbit. If ell is in U, distinguish P=U, L subset P, and neither, giving three
orbits. For a mixed line normalize ell=span(e1+e3). A plane containing L is
span(e1,e3); otherwise P intersects U in a line independent of e1, which may
be normalized to span(e2). This gives two more orbits.

For a basis matrix g, the stabilizer condition is that
g^(-1) diag(h,1) g is upper triangular. This gives Borel stabilizers in the
first three cases. In cases4–6 the stabilizers are respectively

    ((1,b),(0,d)),       diag(1,d),       ((a,b),(0,1)),

with the indicated diagonal entries nonzero. This also verifies the dimensions.

The unique open orbit is case5. A Mackey filtration of a principal-series
restriction has locally closed orbit layers, but identifying those layers does
not specify which sections extend across their boundaries. No boundary-gluing
calculation or finite H_2-module presentation is supplied here.

## 5. Why quotient multiplicities do not determine a module

Set R=C[u,v], I=(u,v), and J=(u^2,v). Both modules are torsion-free of rank1.
For every maximal ideal m other than (u,v), both localizations equal R_m,
so each has a one-dimensional quotient by m. At m=(u,v), both minimal
generating sets have size2. Thus

    dim_C Hom_R(I,R/m) = dim_C Hom_R(J,R/m)

for every maximal m. Nevertheless I and J are not isomorphic. Their free
presentations have relation columns (-v,u) and (-v,u^2), so their first
Fitting ideals are (u,v) and (u^2,v). These differ: u is not in (u^2,v).
Fitting ideals are preserved by isomorphisms, which proves the assertion.

The same example works in C[x,x^(-1),y,y^(-1)] after u=x-1 and v=y-1.
Localizing at 1+u and 1+v does not change the distinction at the origin.
This is an algebraic obstruction to a reconstruction strategy, not an assertion
that either ideal occurs as a p-adic restriction module.

Chan's current quotient-branching theorem is therefore not, merely by knowing
the dimensions of maps to irreducibles, a full restricted-module model.
Source: [Chan, Quotient branching law I](https://arxiv.org/abs/2212.05919), v3,
6 August 2026, Theorem4.1. No complete audit of that long proof is claimed.

## 6. A conditional lattice reduction

Here is a purely algebraic useful reduction. Let H be an algebra with central
domain Z, let K=Frac(Z), and let P subset M be H-modules. Assume:

- P is Z-torsion-free
- Every nonzero H-submodule of M meets P
- Some nonzero f in Z and integer N>=0 satisfy f^N(M/P)=0

Then M is Z-torsion-free. Indeed, the Z-torsion submodule of M is an
H-submodule and cannot meet P nontrivially. Localization is therefore injective.
Moreover f^N M subset P implies

    P subset M subset f^(-N)P subset K tensor_Z P.

This identifies a bounded region in which a lattice must lie; it does not choose
the lattice. In the restriction problem, applying this idea requires checking
the central annihilator and then finding the actual H_n-stable lattice. Those
steps have not produced a general model here. No proposed uniform denominator
bound is asserted as a theorem.

## 7. Steinberg resolutions and compact data

The elementary Steinberg exact sequence for GL_2 is

    0 -> 1 -> Ind_B^GL2(1) -> St_2 -> 0,

with unnormalized induction. Its middle term lies at a reducibility parameter
when rewritten using normalized induction. Higher Steinberg resolutions and
their parabolic products similarly require singular principal series and the
maps between them. A model only for irreducible spherical generic inputs
does not automatically provide these singular specializations or differentials.

There is also a direct obstruction to reconstructing the answer from compact
types. By Iwasawa decomposition and the triviality of unramified characters
on units, every GL_3 unramified principal series restricts to K_G as
Ind_(B intersect K_G)^K_G(1). Hence pi_0 and pi_1 in section2 have identical
entire K_G-restrictions, while their GL_2 Iwahori blocks differ. Even all compact
types are insufficient without the action of translations outside K_G.

The finite-hyperspecial questions studied in [Wang, 2603.22931v2](https://arxiv.org/abs/2603.22931v2)
and [Wang, 2604.09138v3](https://arxiv.org/abs/2604.09138v3), both with a
characteristic-zero local-field hypothesis in the inspected PDFs, do not supply these
translation operators or the infinite-dimensional restricted module.

## 8. Remaining problem and exact-check limits

The missing deliverable is a proved full H_n-module presentation, with its
parameter-dependent extension data, and a compatible treatment of the specified
Steinberg products. The observations above do not provide it.

The accompanying checker verifies elementary matrix identities, the six flag
stabilizer dimensions, the monomial-ideal obstruction, and a finite polynomial
support identity. It does not prove p-adic branching theorems, module
isomorphisms, completeness of literature searches, or a general block model.
