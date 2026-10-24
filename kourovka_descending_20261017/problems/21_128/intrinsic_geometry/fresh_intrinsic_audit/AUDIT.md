# Fresh independent adversarial audit of the intrinsic geometry route

Audit checkpoint: 2026-10-24 20:41 UTC. Auditor did not author the mathematics or
producer code. Completion of the requested mathematical audit: 100%, including
the new intrinsic graph, resonance obstruction and final FAMILY_REPORT.md. This
is an audit completion estimate, not a probability of solving 21.128.

Core verdict: **PASS with explicitly limited scope**. No complete solution,
intrinsic recognition theorem, or originality conclusion follows.

## Mathematical checks

1. The spectrum of abstract commensurability classes of stable element
   centralizers is invariant under abstract commensurability. Directedness by lcm,
   invariance under nonzero powers, and exact intersection with finite-index
   subgroups prove this directly. The vector-space factorial-chain proof of power
   stabilization in linear groups is correct and asserts only existence.
2. The finite-index identity for virtual centers is correct. The map
   L/VZ(L) -> H/VZ(H) is injective and finite-index when L has finite index in H.
   No incorrect replacement by ordinary centers in arbitrary groups is made.
3. The maximal rank-three parabolic normalizer and pure quotient centralizer
   proofs survive review. I read actual Ajbal--Godelle Theorem 1.3, Definition 2.3,
   Proposition 2.4, and Proposition 3.1(i)(a),(ii). The central global Garside
   element allows positive ribbons to be used; every elementary ribbon from a
   maximal X remains in X because the global Garside conjugation is trivial.
   Monoid support proves the intersection with the global center is trivial.
   The Coxeter fixed line excludes a compensating odd global Garside factor in
   the pure intersection. Length kills every possible commutator in the global
   pure center. These points are essential to the exact equality in Q.
4. The finite-index double-centralizer and virtual-center formulas for these
   designated P_X images are correct. A subgroup of finite index in P_X also has
   finite index in A_X, so it contains powers of every standard generator. The
   cited centralizer-of-even-powers result suffices for all nonzero powers by
   passing to an even multiple. These calculations establish forward formulas;
   they do not classify arbitrary element centralizers in Q_F4.
5. I independently read Davis--Huang Definitions 1.11 and 1.14, Lemma 1.13,
   Proposition 5.11, and Theorem 5.12. The selected local arrangement parabolics
   and Hopf circles are inputs, not intrinsically recognized outputs. In
   particular Lemma 1.13 concerns conjugation inside the given group, with its
   fixed meridian coordinates. It cannot imply arbitrary finite-index
   isomorphism invariance of the selected family.
6. The A3 puncture-swap test is valid. In PMod(S_0,5), cutting along the three-
   finite-puncture curve gives centralizer P3=F2 x Z; the two-puncture complement
   contributes the same boundary twist, not another independent center. A sphere
   puncture swap changes which side contains the distinguished capped puncture
   and sends this to the centralizer of a rank-one parabolic twist. All disk
   rank-two irreducible parabolics have the former finite-puncture type, which
   cannot be internally commensurable with the latter twist-center subgroup.
   Abstractly these groups are isomorphic, so this is not a noncommensurability
   result for 21.128.
7. The cited rank-one F4 restriction is genuinely an omitted profile in any list
   containing only rank-three parabolics. Amend--Hoge--Roehrle Lemma 3.3(iii) and
   Table 3 give both F4 mirror-orbit restrictions, their lattice isomorphism,
   exponents (1,5,7), and nonsupersolvability. These properties are not thereby
   commensurability invariants. The exact certificate below only selects one
   mirror; the source, rather than that single certificate, covers the other F4
   mirror orbit.

## Exact computation and completeness

I inspected all three scripts and ran verify_incidence.py into my own
reproduction.json, without overwriting any author's output. It returned PASS.
The verifier does not import either producer and uses Q(sqrt(5)) Gaussian
elimination instead of the producer's Q(phi) wedge canonicalization.

* Simple roots have full rank, the exact negative adjacent Gram entries for
  F4/H4 and orthogonal nonadjacent entries, and reflection closure reaches
  exactly every listed projective root. Thus this checks identification of the
  Coxeter arrangement, rather than merely checking an arbitrary list of vectors.
* Every rank-two flat is closed, distinct, and the flats partition all unordered
  root pairs. Every rank-three flat is closed and distinct. Independent triples
  number 1920 in F4 and 33300 in H4. Summing their disjoint coverage by listed
  rank-three flats gives those exact totals, proving completeness of the list.
* F4 has 24 mirrors, 122 rank-two flats, and 120 rank-three flats. H4 has 60,
  722, and 1320 respectively. The ambient central Betti numbers are
  (1,24,190,552,385) and (1,60,1138,7140,6061); the projective Euler
  characteristics are -240 and -5040.
* The selected restrictions have 13 and 31 mirrors. Their central Betti numbers
  are (1,13,47,35) and (1,31,239,209), with projective Euler characteristics
  24 and 180. Restrictions were reconstructed from all ambient mirrors by the
  independent verifier; no floating point decisions occur.
* I wrote a separate check_boundary_profiles.py, importing neither producer nor
  verifier. In the already verified complete lattice, restricted lines at a
  rank-two normal flat are in bijection with rank-three normal flats containing
  it. It verifies every entry of rank2_boundary_profiles.json: F4 profiles
  (normal mirrors, restricted lines, flat count) are (2,6,72), (3,6,32),
  (4,4,18); H4 profiles are (2,12,450), (3,12,200), (5,10,72).

The Möbius recurrence and division of the central Poincare polynomial by 1+t
justify the derived Betti numbers. Pair/triple partition arguments prove the
finite census completely, not just for a random sample. None of these finite
numbers alone proves abstract commensurability or noncommensurability.

## Reproduction and scope limitations

INPUT_MANIFEST.json fixes hashes of the audited input files. reproduction.json
and boundary_profiles_verification.json preserve exact outputs. All six cached
primary PDF hashes checked against centralizer_recognition/SOURCE_MANIFEST.json.
The source quotations were read as mathematical evidence, not as instructions.

The central mathematical gap remains an intrinsic classification or recognition
of all relevant stable centralizers, including the restricted-arrangement profile
and nonparabolic elements. Renaming that missing result is not a new mechanism.
No solution or priority gate is passed by this audit.

## New graph and biorderability delta

INTRINSIC_GRAPH.md passes. Vertices are internal commensurability classes of
infinite cyclic subgroups, not an unsupported selected parabolic family. The
existence of commuting independent powers is representative-independent. Every
cyclic subgroup meets a finite-index subgroup in finite index; cyclic
intersections are the same actual subgroups in either ambient group. These facts
prove the claimed vertex and edge bijection even in groups with torsion. The
stable-centralizer decorations are justified by the earlier exact intersection
formulas. Multiplicity of selected conjugacy classes is correctly excluded.

I read Marin's actual Theorem 3 in the cached 2007 primary paper, printed p1889:
every pure spherical Artin group is residually torsion-free nilpotent and
biorderable. I also read Soroko arXiv:2009.10471v4 Proposition 3, which explicitly
records pure biorderability and the genuine central direct splitting, embedding
the quotient into the pure group. Thus Q_T is biorderable, and the implication to
unique roots, C(g^m)=C(g) for m nonzero, and VZ(J)=Z(J) for every subgroup J is
correct. This strengthens the allowable centralizer invariant but does not
classify its vertices.

## New resonance obstruction delta

RESONANCE_PRODUCT_OBSTRUCTION.md passes after the author added the explicit
space-to-group degree-one cup-product bridge. The classifying map induces an
H1 isomorphism and injects group H2 into space H2, so both zero and nonzero cups
of degree-one classes can be checked in the complement. This follows from the
universal-cover spectral sequence and needs no unproved K(pi,1) assertion.

The finite-index argument is valid without any alleged general resonance
invariance. Rational restriction is injective in H1 and H2 by transfer. If a
finite-index subgroup U were F_r x F_s, r,s>=2, its resonance is the union of its
two factor H1 subspaces: an element with both components nonzero has only its
own span as the cup kernel. Every isotropic Wi of dimension at least two must
therefore inject into one of those two factors. The three pairwise nonzero cross
cups force each pair of Wi into different factors, which is impossible for
three Wi. A finite-index subgroup of a direct product contains a finite-index
product of its intersections with the factors, so the proof excludes abstract
commensurability, not just an actual product subgroup of a prescribed index.

I independently read Orlik--Solomon Theorem 5.2 in the cached original primary
paper, printed p185. Its cohomology presentation and rank-two circuit relations
justify the algebra used. Passing between rational and complex coefficients is
faithful for these rational meridian classes, so there is no field mismatch.
The Hopf coefficient-sum map identifies the projective H1 subspace, and its
pullback on cohomology is injective by the central C*-factor splitting.

I inspected resonance_product_obstruction.py, reproduced its exact certificate
in resonance_reproduction.json, and independently wrote verify_resonance.py.
The latter imports neither the producer nor its verifier and expands every
exterior pair, reducing circuits to each rank-two flat's anchor basis. It checks
all local basis cups vanish and verifies the claimed cross coefficient +1 for
all three pairs in both arrangements. Its output is resonance_verification.json.
The witnessed dimensions are (3,3,3) for the 13-plane restriction and (5,2,2) for
the 31-plane restriction.

The precise accepted conclusion is: neither projective restriction group is
abstractly commensurable with a product F_r x F_s, r,s>=2. This is not a proof of
strong indecomposability against all possible factors, nor a comparison with
the H3 projective pure group. The full centralizer classification and original
21.128 remain unresolved, and the publication gate stays closed.

## Terminal assembly review

The final FAMILY_REPORT.md has now been read in full and passes. Its exact
arrangement counts agree with the reproduced certificates. Its separate basis
files agree with the corresponding complete reflection model fields, and the
author's independent_verification.json equals the fresh output after removing
elapsed wall time. Its local dihedral calculation is correct: F_(m-1) has an
index d/(m-2) subgroup of rank d+1 when d is the lcm of m-2 and m'-2; in particular
F3 and F4 have index-three/index-two F7 subgroups. This illustrates why the
stated ordinary resonance dimensions do not survive finite-index passage.
All listed rank-two boundary profiles have two nonabelian free factors after
the center quotient and hence have the same abstract commensurability class.

The missing Marin/Soroko references in the earlier draft were repaired before
this terminal audit: RESULTS.md now proves the unconditional biorderability
consequence and SOURCE_MANIFEST.json records both actual PDFs with cache
provenance and correct hashes. I independently verified these copied hashes
against the primary caches already read. No substantive objection remains to
the bounded results in the final reviewed package.

Final verdict: **PASS for the stated partial lemmas, exact certificates and
explicit limitations. Overall 21.128 remains unsolved.** There is no complete
original resolution to publish. INPUT_MANIFEST.json freezes the actual final
mathematical inputs; PRIMARY_CHECKS.json records source custody, and
OUTPUT_MANIFEST.json freezes this auditor's artifacts. Any later mathematical
change requires a delta review rather than inheriting this verdict silently.
