# What Davis--Huang proves, and what it does not

Checked 2026-10-24 20:28 UTC against the author's complete 41-page PDF,
*Bordifications of hyperplane arrangements and their curve complexes*,
DOI [10.1112/topo.12184](https://doi.org/10.1112/topo.12184).
Local source hash and retrieval details are in SOURCE_MANIFEST.json.

**Answer:** the audited results do not recognize parabolic centers under an
arbitrary isomorphism of finite-index subgroups. They identify two constructions
associated with a specified arrangement and identify centralizers of its already
specified local Hopf circles. Their use of the word "algebraic" does not supply
the missing invariance.

The exact dependency is visible in the following definitions and theorems.

1. Definition 1.11 (PDF p9) defines a parabolic subgroup using a chosen flat E,
   the normal arrangement A_(V/E), a small-disk inclusion in M(A), and a path to
   a basepoint. Thus the family Par(G) enters through the arrangement geometry.
2. Example 1.12 identifies these subgroups with pure spherical Artin parabolics
   in the Coxeter case. The central cyclic subgroup is the Hopf fiber of the
   normal arrangement complement. Lemma 1.7, invoked there, identifies this
   cyclic subgroup with the parabolic center in the aspherical case.
3. Lemma 1.13 (PDF p9) uses the integral meridian basis of H1(M(A)) to prove that
   two such cyclic subgroups that are **conjugate in G** have the same flat type.
   It is not a statement about arbitrary abstract automorphisms or finite-index
   isomorphisms. An arbitrary automorphism need not preserve that chosen meridian
   basis or the collection of its flat-indicator vectors.
4. Definition 1.14 (PDF p9) takes **the centers of the previously defined proper
   irreducible parabolics** as the vertex set of C_alg. Edges are commuting
   independent pairs, and the complex is the flag completion. This is a group
   operation applied to a selected family, not an intrinsic group-only
   characterization of membership in that selected family.
5. Proposition 5.11 (PDF pp38--39) proves injectivity of the chosen face
   fundamental group and identifies its image with the centralizer/normalizer
   of the local normal-arrangement Hopf center. Its product has normal and
   restricted arrangement factors. Proposition 1.31 (PDF p19) likewise starts
   with the given vertices to describe stabilizers of their simplices.
6. Theorem 5.12 (PDF p39) identifies C_alg with the nerve of the boundary faces
   in the universal cover of the chosen bordification, describes the action and
   quotient, proves the wedge-of-spheres statement, and identifies face groups
   and stabilizers. It does not assert that an arbitrary abstract isomorphism
   sends those boundary-face groups to boundary-face groups in a different
   arrangement or finite cover.

Consequently the implication needed in 21.128,

    arbitrary finite-index isomorphism => preservation of the chosen Hopf lines,

is still an additional mathematical theorem to prove. If such a theorem were
proved, the centralizer formulas in Davis--Huang would become useful for comparing
the resulting links and factors; the formulas cannot establish that implication
by themselves.

The A3 puncture-swap test in RESULTS.md additionally rules out strengthening
Lemma 1.13 from internal conjugacy to preservation of parabolic rank under every
finite-index isomorphism of central quotients. It does not rule out preservation
of an unlabeled enlarged family of twist lines.

Status: **scope audit complete; intrinsic recognition not obtained**. Best guess
completion toward the original discovery goal remains 10%; this audit closes an
unsupported shortcut rather than resolving the original problem.
