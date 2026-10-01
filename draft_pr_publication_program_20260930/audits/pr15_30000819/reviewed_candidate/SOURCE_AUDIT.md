# Source and scope audit

Original audit2026-09-30; acceptance update2026-10-01 UTC. This is a bounded audit; priority of the explicit quartic formula is unconfirmed. Positive prior evidence now verifies existential F(V).

## Original source

Christian Haase, *What else is known?*, Oberwolfach Report 39/2007,
pp. 2313--2317, target on p. 2316:
https://doi.org/10.4171/owr/2007/39.

The full relevant contribution was read from the original PDF:
https://oa.tib.eu/renate/bitstreams/29b4c7a6-7c9e-42dd-8780-60d49fb0675c/download.

The report's workshop dates are 12--18 August 2007. The dataset source
description includes a 2008 parenthetical; that does not change the actual
report number or question. Page 2314 identifies very ampleness with
finiteness of the hole set. Page 2316 permits an arbitrary subset of lattice
points generating the embedding, rather than all points of the polytope.
It asks for a bound by normalized volume and explicitly connects this with
Eisenbud--Goto and Herzog's multiplicity question.

The dataset's wording, in terms of normalized volume, permits a much weaker
arbitrary function. The original wording does not justify treating a
quartic bound as proof of the sharper linear-volume question. This is the
source-interpretation limitation in the package; it does not change the known status of the formulated existential target.

## Dataset provenance and previous research

The selected record was taken directly from the authorized pinned local
dataset, revision 37e53eabe540fb458758e198be61634bd02ee008, under the current
user instruction allowing this route before the original literature.
Numeric ID 30000819 is unique. Its code OWR-1595-012 has exactly one
matching numeric record and no research-results entry. The selected record
is preserved verbatim as source_record.json.

Repository AGENTS.md, queue AGENTS.md, README/policy, queue row, and selected
shortlist review were read. Queue rank at start: 33, status queued, turns
0/5. All-state PR searches by numeric ID and holes/semigroup subject found
none; branch search by numeric ID found none. Repository code search found
only the selected queue-review material. Thus no prior/invalidated
mathematical attempt was identified. No related-target group includes this
ID, and a dataset scan found no duplicate semigroup-hole question.

## Sources supporting the coarse bound

### Sturmfels, 1996

*Equations Defining Toric Varieties*, arXiv:alg-geom/9610018:
https://arxiv.org/abs/alg-geom/9610018.

The original paper was retrieved. Read the configuration and normalization
definitions, Theorem 1.4 (degree equals intrinsic normalized volume), and
the full Section 4 proof of Theorem 4.5, including Lemma 4.6 and (4.4).
Its bound is reg(I_A)<=n*degree*codimension, with reg of the ideal rather
than the quotient ring. The circuit-degree bound and regularity bound
are classical dependencies. Arbitrary homogeneous configurations are
covered; normality and inclusion of every lattice point are not required.

### Tran, 2018 revision

*On k-normality and Regularity of Normal Toric Varieties*,
arXiv:1708.04340v2, 4 February 2018:
https://arxiv.org/abs/1708.04340.

Read the introduction's distinction between general regularity bounds and
the sharper Eisenbud--Goto question, the main k-normality bound, the
volume-dependent estimate for smooth polytopes, and Proposition 4.5's
regularity/normality relation. These do not remove the chosen-generator
issue by fiat and do not establish the sharp general target. Their
specialized bounds are not claimed as new here.

### Standard commutative-algebra inputs

The normalization of a positive affine semigroup algebra is finite and is
Cohen--Macaulay by Hochster's theorem. Regularity is read from graded local
cohomology, and for a nonzero homogeneous ideal I, reg(I)=reg(Q/I)+1.
These standard inputs are stated explicitly in the proof. The finite-hole
normalization quotient is identified with H^1 of the original semigroup
ring to check the two-degree offset carefully.

## Bounded current-literature search

Queries included highest-hole/volume, very-ample semigroup holes, toric
regularity bounds by degree, k-normality and volume, and current toric
Eisenbud--Goto counterexamples. The located general counterexamples to
Eisenbud--Goto are not automatically toric or very-ample finite-hole
examples. No such inference is used.

The search located classical n-dependent bounds and later specialized
polytope bounds. It did not establish novelty of the coarse corollary or
find a resolution of the sharper h<=V interpretation. Accordingly this
current audit preserves the original interpretation limitation, while positive CCMPV evidence below establishes already_solved for the formulated numeric target. It does not create a stronger residual target. No outside individual was contacted.

## Independent source cross-check

The reviewer additionally checked Beck--Delgado--Gubeladze--Michałek,
*Very ample and Koszul segmental fibrations*, arXiv:1307.7422,
Proposition 2.1, for the finite-hole equivalence with the intended
normal toric point-configuration setting. This avoids conflating the
question with very ample line bundles on arbitrary nonnormal varieties.

## Current positive prior result and two-reading assessment

CCMPV, *Regularity of prime ideals*, Corollary5.3, published online11June2018 and print2019, gives a regularity constant depending only on multiplicity for nondegenerate homogeneous prime ideals over an algebraically closed field. Theorem5.2 alone also takes height; Corollary5.3 is the correct dimension-independent locator. For distinct selected degree-one lattice generators, I_A is homogeneous prime, has no linear forms, and degree/multiplicity V in the intrinsic generated lattice. Finite nonempty holes give h<=reg(I_A)-2, so the old theorem already implies some F(V). No complete-configuration or projective-normality assumption is inserted. [Published source](https://doi.org/10.1007/s00209-018-2089-y), [primary deposited manuscript](https://par.nsf.gov/servlets/purl/10303748).

The original OWR prints by-normalized-volume wording without the formula h<=V. The sharper reading is contextual inference from Eisenbud-Goto/Herzog, not an exact printed inequality. The dataset's existential F(V) reading is already_solved by the positive prior corollary. We assign already_solved to the formulated numeric target because of this published existential corollary. Unknown intended numeric strength and unproved sharper variants remain separate qualifications; neither is substituted for the target or attributed to the author as an established intended inequality. No new resolution, priority for the quartic formula, paper, DOI or tracker row is claimed. The pinned historical source record stays unchanged.

See PRIORITY_SCOPE_UPDATE.md and the independent full primary report for the hypothesis-by-hypothesis subsumption certificate, source hashes, source-year2007 and version/page locators. Current bounded searches located no checkable proof or counterexample for the general sharp selected-configuration assertion; this is not proof of current worldwide open status.
