# Original scope, related results and read limits

The exact source is Itai Benjamini's *Coarse Geometry and Randomness*, author
manuscript dated30 October 2013, Problem 9.6 on printed/PDF page 64. Relevant
pages 1,5,9,32,33,63–65 were read; definition9/context63/question64 were visually
checked. Definition 1.25 permits both multiplicative and additive metric
distortion and a strict C-net condition. Pages32–33 define ordinary common-p
independent bond percolation, rooted survival and p_c. Page63 puts uniqueness
in the supercritical context. The short problem sentence itself has no
p-quantifier. Transitivity is separately imposed on nearby theorems, not a
standing condition for the question. The published chapter record is
https://doi.org/10.1007/978-3-319-02576-6_9, dated14 October 2013, pages 69–84;
no byte identity or identical pagination between that chapter and the
30October author manuscript is asserted. The manuscript archive returned503
in the earlier source review; an exact-byte primary local copy was recovered
read-only. Its entire 1101523-byte identity was rehashed for this preparation.
The entire 115-page book was not read. Exact identities are in SOURCE_PROVENANCE.json.

The note's chosen target is explicitly declared: for every admissible graph
and each fixed p_c(G)<p<=1, the infinite cluster is almost surely unique.
The example supplies p_c<=9/10 and positive-probability multiplicity at 19/20
on one deterministic degree-four graph roughly isometric to Z². This is a
full negative answer to that declared interpretation; it is not a claim to
recover a uniquely intended missing quantifier. It also disproves a stronger
all-parameter at-most-one assertion. No critical example is needed, and no
simultaneous-in-p statement, exact cluster count or almost-sure multiplicity
is inferred. A question only about sufficiently high p is weaker and is not
refuted by this argument.

The proof uses familiar bounded subdivision and independent series-path
reduction, elementary dual parity, path counts and product independence.
The contribution presented is the explicit opposite-quadrant deterministic
example with fully checkable constants and source-scope qualification.
No new general percolation mechanism or exclusive historical priority is claimed.

Benjamini–Schramm, *Percolation beyond Z^d, many questions and a few answers*,
ECP1(1996),71–82, https://emis.de/ft/41630, Example 1/Proposition 1,
printed 78–79, gives an enhanced binary tree roughly isometric to a hyperbolic
sector with a supercritical nonuniqueness interval. Its exponential geometry
is different from square-lattice coarse geometry, and the paper's stated
planar model is site percolation. Lemma 1 proves uniqueness sufficiently near
one for bounded-face planar tilings. Original intro/model and the selected
example/lemma text were read, not all proofs of the paper.

Benjamini–Kozma, *Uniqueness of percolation on products with Z*, ALEA10(2013),
15–25, https://alea.math.cnrs.fr/articles/v10/10-02.pdf, Theorem 1,
gives critical nonuniqueness on a subexponential-growth product graph.
Its introduction also warns that uniqueness need not be monotone outside
appropriate symmetry assumptions. Printed 15–16 and selected context were
read. Neither a lattice rough-isometry conclusion nor a full-supercritical
negative on a Euclidean-coarse graph is substituted for the actual statement.
The full proof was not audited.

Teixeira, *Percolation and local isoperimetric inequalities*, PTRF165(2016),
963–984, DOI10.1007/s00440-015-0653-5, Theorem 1.4, yields site uniqueness
above some p*<1 under a local isoperimetric inequality of dimension >1 and
polynomial volume bounds. The site-model statement and adjacent discussion
were read in arXiv1409.5923v1. The margin's2014 version date and generated
title's2021 date are separate fields; no new version is inferred. No p*=p_c
identity or blanket uniqueness transfer to a bond model is supplied by that
statement. The full proof was not audited.

Candellero–Teixeira, *Percolation and isoperimetry on roughly transitive graphs*,
AIHP54(2018),1819–1847, DOI10.1214/17-AIHP857, Theorem 1.8, supplies
high-marginal uniqueness for its site laws under rough transitivity,
growth/isoperimetry and decoupling hypotheses. Relevant definitions and the
complete theorem statement were read from arXiv1507.07765v3 selected text;
the complete proof was not audited. Rough transitivity is not silently
replaced by graph-automorphism quasi-transitivity. The high-density threshold
is not identified with p_c.

Hutchcroft–Tointon, *Non-triviality of the phase transition for percolation on
finite transitive graphs*, JEMS27(2025),4283–4346, DOI10.4171/JEMS/1453,
Theorem 1.8, is a bond result under a uniform finite-exhaustion isoperimetric
condition with dimension >6+2sqrt(7). It proves uniqueness for p>=1-epsilon.
Its Theorem 1.10 separately needs a uniform large-set connection hypothesis.
Printed 4290–4292, including these statements and adjacent discussion, were
read, not the full64-page proof. Root survival alone is not substituted for
that uniform premise, and neither lower endpoint is assumed to equal p_c.

Hilário–Sá–Sanchis–Teixeira, *Percolation on stretched lattices: a static
renormalization approach*, PTRF195(2026),451–496,
DOI10.1007/s00440-026-01470-4, Section 2 explicitly formulates independent
conditional coarse probabilities as powers of p. This established series
method is credited. Remark 5's full-supercritical uniqueness concerns the
annealed random-environment law and uses its translation invariance,
ergodicity and finite energy. It is not a deterministic-environment theorem
for every angular pattern. The primary published HTML's Section 2/Remark 5
and metadata were inspected; other proofs were not audited. The journal
publication date is28 February 2026, separate from the June issue date.

The adopted earlier independent review additionally compared HPS uniform
connection hypotheses, a coordinate-sublattice defect model, sprinkling with
everywhere/uniformly densely percolating input, and the quasi-transitive
restriction in Lyons–Peres. This preparer read the review's adjudication of
those leads, rather than independently auditing those whole papers. None is
imported as a premise here. These limits are distinct from a proof gap: the
counterexample's graph, parity, component and probability arguments are
self-contained.

Fresh read-only GWS checks inspect the entire43-column numeric tab 1254632077
in value/formula views with metadata before/after. Exact aliases had no hit.
The three semantic leads and native claim descriptions were read: ordinary
finite-energy dependent lattice percolation with internal threshold one,
near-one oriented flow, and a designed traffic-tree model. They are distinct
from ordinary iid percolation on this deterministic graph. The native Zenodo
numeric search's curriculum record is also unrelated. Exact nonuniqueness,
rough-isometry/percolation and bounded-subdivision/percolation phrase searches
returned no exact result. Search outputs are bounded and not global absence
certificates. Read-only local STATE identifies the current own pending PR,
not an earlier publication. No provider, row or state was modified.

The unpublished proof source is PR1348,
https://github.com/AlecKriebel/Math/pull/1348,
head 4222445c0fe52b32a6dbab7ee5ad791b5d044b08, PROOF SHA256
731c8569a73f275c857991a4f97b47ee6debc2d3d46bb2399134021f65804f60.
Its complete 14070-byte construction and 10629-byte source adjudication were
read by immutable blob, never executed. The note's date is22 October 2026;
the prior project proof does not become an earlier published solution by
being cited. Problem 10000037 / AMR-099-0037 / sourceProblem 9.6 is one family.
Original-question and dependency DOIs are not counterexample DOIs.

No earlier full-target publication or matching solution DOI was authenticated
in these bounded checks and the adopted independent source review. This is
not exclusive firstness, exhaustive historical novelty, author-discovery
priority or current openness certification. Unindexed, unpublished, folklore,
alternate-terminology and uninspected editions remain limitations. No outside
person was contacted. Two new whole-package independent reviews remain to be
assigned by root; preparation QA is not a substitute for them.
