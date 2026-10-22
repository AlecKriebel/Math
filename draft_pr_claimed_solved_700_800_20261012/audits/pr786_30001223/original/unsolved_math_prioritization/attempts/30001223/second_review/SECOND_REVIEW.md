# Second independent adversarial review: ID 30001223

## Acceptance and boundaries

**ACCEPTED. No mathematical correction is required.**

For every odd prime p, over an algebraically closed field of characteristic p,
with q=1, r=2p-1 and lambda=(2p-2,1), the source's Young module F I(lambda)
is simple, whereas I_n(lambda) is not projective for any n >= 2. Thus the
characteristic-3 case lambda=(4,1), r=5 is a counterexample to the unrestricted
bridge in Miyachi's Conjecture 7.

This verdict includes the first audit's direct Schur-functor identification. It
does not assert novelty, external peer review, or publication. It does not refute
the separate De Visscher-Donkin classification of projective-injective modules,
or settle a version restricted to characteristic zero and a nontrivial root of
unity. Both preceding archives were preserved byte-for-byte.

## 1. Frozen inputs and source question

The author archive has 12,753 bytes and SHA-256
e82e3a8349c00e74199090c3463918f5a83b915d85003438fa030adabf797978.
The first audit archive has 18,009 bytes and SHA-256
a795cf78699d7dc0a87bf0b04c15f9ec5f5afb02869ab9cb1432a1824e86c572.
Each archive was authenticated before its code was executed in fresh relocated
directories. The original author's first-execution chronology is not thereby
established; only this review's own verification-before-execution is established.

The three full input corpora and both source PDFs were rehashed independently.
The unique complete problem record, its associated empty report, statement hash,
review hash and catalog rank 824 all match. The dated catalog assessment that the
problem is open is historical metadata, not a fresh literature conclusion.

The primary contribution [M], printed pp. 944-947, was read, including visual
inspection of p. 946. It defines the Young module through F I(lambda), permits a
unit q, and puts the existential rank bound at the partition length. Its index-set
proposal is stronger, rather than an established equivalent formulation. The
characteristic-zero qualification occurs in the later, separate Specht-module
subsection. These points exclude neither q=1 in characteristic p nor n=2.

The relevant structural sections of [DD], printed pp. 1-12, were checked,
including visual inspection of p. 9. They explicitly permit the classical
specialization and set quantum characteristic to p when q=1. Its value is not
the multiplicative order 1 of q.

## 2. Direct identification of the Young-module label

This is the main potential convention failure. A calculation with an ordinary
Specht module alone would be an unnecessarily weak way to settle it.

Take N >= r, E=k^N, and alpha=(r-1,1,0,...,0). Write

H = Sym^(r-1)(E) tensor E.

The symmetric-power injective decomposition in [DD], printed p. 12, says that
the multiplicity of I_N(mu) in H is dim L_N(mu)_alpha. A highest weight mu
admitting alpha must dominate alpha. Since alpha's first two parts already sum
to r, only mu=(r) and mu=alpha are possible. The alpha-weight multiplicity of
L_N(alpha) is one.

The alpha-weight multiplicity of L_N(r) is also one. Indeed, Sym^r(E) is the
costandard module with simple socle L_N(r), and its highest weight line is spanned
by x_1^r. This vector therefore lies in that socle. The coefficient of t in its
translate (x_1+t x_2)^r is r x_1^(r-1)x_2, which is nonzero because p does not
divide r. The alpha-weight space of the entire symmetric power is only one
dimensional, so the multiplicity is exactly one.

Consequently H is I_N(r) direct sum I_N(alpha). The maximal label (r) has no
larger costandard sections in its injective hull, so I_N(r)=Sym^r(E). Multiplication
m:H -> Sym^r(E) has a canonical section delta/r, where

delta(x^a) = sum_j a_j x^(a-e_j) tensor x_j.

The formula is intrinsic, hence GL_N-equivariant, and m delta=r id. Thus ker(m)
is a complement to I_N(r). Krull-Schmidt cancellation gives ker(m)=I_N(alpha)
up to isomorphism. No simplicity of Sym^r(E) in this stable rank was assumed.
That would in fact be an unjustified transfer of the rank-two calculation.

On the multilinear weight, H has r basis vectors: the second tensor factor is
x_j and the first is the product of all other variables. Permutation matrices
permute these basis vectors. Multiplication sends each to x_1...x_r, so F ker(m)
is precisely the augmentation submodule A of the r-dimensional permutation
module. This fixes the source's exact label, with no sign or conjugation ambiguity.

Finally A is simple over k. A nonzero vector in A cannot be constant, because r
is invertible. Subtracting its image under a transposition with unequal coordinates
produces a nonzero multiple of e_i-e_j. Permutations of this difference span A.
This is an algebraically closed field argument, not just an F_p enumeration.

## 3. Rank-two extension and injective hull

Put m=2p-3 and B=Sym^m(k^2), with monomials v_i=x^(m-i)y^i. The subspace W on
indices 0 through p-3 and p through 2p-3 is invariant: it is the image of
E^(F) tensor Sym^(p-3)(E) under multiplication. The monomial ranges are disjoint,
so the map is injective and dim W=2p-4.

Distinct algebraic-torus weights ensure that every nonzero invariant subspace
contains a monomial. Coefficients of unipotent translates can be recovered over
the infinite field k. Any monomial reaches x^m under y -> y+t x. The nonzero
coefficients of (x+t y)^m occur precisely at the indices defining W, by
(1+t)^m=(1+t^p)(1+t)^(p-3) modulo p. Hence W is simple with highest weight (m,0).

The quotient has exactly the two remaining weight lines, at indices p-2 and p-1.
Both root groups connect them, with nonzero coefficient p-1, so the quotient is
simple, with highest weight (p-1,p-2). A complement to W must be the sum of those
two weight lines in B. Translating v_(p-2) by y -> y+t x produces the nonzero
x^m coefficient. Thus the proposed complement is not invariant and the extension
does not split. Its socle and head are the two different simple labels, including
p=3 where their dimensions happen to coincide.

After tensoring by determinant, nabla_2(lambda) therefore has socle L_2(2p-2,1)
and head L_2(p,p-1). The remaining issue is whether this is the genuine injective
hull. The only partition of r strictly dominating lambda is (r). In rank two,
Sym^(2p-1)(E) is simple: all coefficients of (1+t)^(2p-1) are nonzero modulo p,
so the same monomial argument reaches every weight from the highest weight.
It has no composition factor L_2(lambda). Costandard reciprocity consequently
gives I_2(lambda)=nabla_2(lambda), not just an embedding into that injective.

Contravariant duality fixes simple labels and exchanges head and socle. The
different labels above exclude self-duality. The projective-injective result of
[DD], printed pp. 10-11, therefore excludes projectivity of I_2(lambda).

At p=3 this is the four-dimensional module det tensor Sym^3(E), with two-dimensional
socle L_2(4,1) and two-dimensional head L_2(3,2). The dimension comparison with the
six-dimensional projective cover of its head also agrees with reciprocity.

## 4. Every allowed rank is excluded

The audited proof does not assume that arbitrary projectives remain projective
under truncation. Instead, projectivity of the injective I_N(lambda) would make
it an indecomposable tilting T_N(mu). Since its socle label lambda is a composition
factor, mu dominates lambda. The only choices are (r) and (r-1,1), both with at
most two parts.

The exact truncation theorem on [DD], printed p. 9, applies separately to both
displayed labels and gives f I_N(lambda)=I_2(lambda) and f T_N(mu)=T_2(mu).
Thus I_2(lambda) would be an injective tilting and hence projective, contrary to
the rank-two result. This covers every N >= 2, including N below stable Schur
rank and N above it. The Schur functor itself was used only at N >= r.

There is also a direct classical cross-check on this implication. At q=1 the
truncation selects weight spaces whose last N-2 coordinates are zero. The
transpose anti-involution defining contravariant duality fixes the weight
idempotents and restricts to the corresponding transpose anti-involution at
rank two. Thus f(V^o) is naturally (fV)^o. A self-dual I_N(lambda) would therefore
truncate to a self-dual I_2(lambda), again contradicting its distinct head and
socle. This cross-check does not substitute generic preservation of projectivity.

Membership in any proposed sufficient De Visscher-Donkin index set would give a
projective injective. Since no rank works, the stronger bridge fails too. No
claim of completeness for those sufficient sets is needed or obtained.

## 5. Independent support and acceptance checks

The fresh checker uses formal unipotent coefficient graphs and algebraic-torus
weights, rather than either preceding checker's polynomial matrix-rank code.
It finds the simple socle component and simple quotient component, with arrows
from the latter into the former and none back. Thus the weight-closed submodule
lattice has exactly three members: zero, W, and B. It verifies the family for
every odd prime through 97, detects the reducible Sym^3 characteristic-3 negative
control, and checks multiplication-polarization on full monomial bases in three
small ranks. Only the stable-rank test claims a multilinear Schur weight.

These checks use formal coefficient extraction, not just the finite group
GL_2(F_p). Nevertheless finitely many primes are supporting checks, not the proof
of either universal quantifier. The proof is in sections 2-4 above.

Both frozen archives were replayed from authenticated fresh extractions in paths
containing spaces, with an unrelated working directory, in normal and optimized
Python. The first audit's 34 author controls and 28 audit-package controls were
also rerun with both normal and optimized drivers. All passed. The second-review
gate itself validates its exact regular-file inventory and every manifest hash
before running its independent checker. Its own baseline, relocation and mutation
results are recorded separately.

The external archive digest remains the authenticity anchor. An internal manifest
cannot protect against coordinated replacement of itself and all its programs.
No claim is made about malicious runtimes or concurrent filesystem substitution.
No third-party source text, PDFs, corpus contents, or private coordination files
are included in this second-review archive.

## References

[M] Hyohe Miyachi, "Dipper's hypothesis and self-injective endomorphism rings,"
in Representations of Finite Groups, Oberwolfach Reports 6 (2009), report 17,
contribution printed pp. 944-947. https://ems.press/content/serial-article-files/46217
and https://doi.org/10.4171/OWR/2009/17 .

[DD] Maud De Visscher and Stephen Donkin, "On projective and injective polynomial
modules," manuscript dated 12 January 2005; Mathematische Zeitschrift 251 (2005),
333-358. Manuscript printed pp. 7-12 contain the structural facts used here.
https://openaccess.city.ac.uk/id/eprint/969/ and
https://www.staff.city.ac.uk/maud.devisscher.1/Publications/prinjjan12.pdf .
