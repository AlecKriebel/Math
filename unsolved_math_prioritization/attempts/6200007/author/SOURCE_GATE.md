# Source and prior-work gate

Checked 2026-10-04 UTC. The gate establishes the question's identity and the
scope of the claims below. It does not certify that every relevant paper or
repository branch has been found.

## Primary question

- Catalogue: https://www.unsolvedmath.com/problems/6200007
- Stable identity: 6200007 / AMR-061-0007, rank 548
- Proposer: Misha Kapovich
- Source: https://www.math.ucdavis.edu/~kapovich/EPR/problems.pdf
- Exact locator: Problem 7, printed/PDF page 3
- This author-hosted version is dated 24 October 2007. Its introduction says
  most problems were collected at the AIM workshop in 2005. The catalogue
  year 2005 refers to the collection, not the date printed on this PDF.
- AIM's version, https://aimath.org/WWN/groupboundaries/groupboundaries.pdf,
  is dated 25 May 2007 and labels the same item Question 7, also on page 3.
  The question and accompanying background agree in mathematical content.

The target in our own notation is:

Given a compact metrizable Z and an action G->Homeo(Z) proper on the space
of distinct triples, assume every G-orbit is dense. Must there exist a
Gromov-hyperbolic metric space X, a G-equivariant homeomorphism Z->boundary X,
and a quasi-action of G on X whose quasi-isometry constants and composition
error are bounded independently of the group elements?

The printed clarification of “topologically transitive” means minimality.
We do not weaken it to the existence of one dense orbit. The question does
not require finite generation, a proper or cobounded interior action, a
prescribed metric on Z, or a specific topology or dimension for X. It also
does not restrict X to a tree or to a classical hyperbolic space. Our positive
conditional construction happens to produce an exact isometric action.

The printed statement and surrounding definitions were read directly, and
the author PDF's page 3 was rendered and visually checked. We found no later
update within these two primary lists. That is a bounded source comparison,
not an assertion about all later literature.

## Catalogue recovery and limits

The exact catalogue URL was attempted and returned HTTP 403; the web reader
also could not open it. Identity was independently matched to the public
UnsolvedMath dataset's original statement/provenance fields and then to the
two primary PDFs. The retrieved public dataset revision was
`372682f27c1b0d3d39e75fa63ad7932c7a2e1bde`.

The `problems.json` file at that revision has SHA-256
`37067f43734b76ee886b032469836767c34d892de14397ce6aa71da01500e252`
and 69,291,427 bytes. Dataset URL:
https://huggingface.co/datasets/ulamai/UnsolvedMath/blob/372682f27c1b0d3d39e75fa63ad7932c7a2e1bde/problems.json

The row is labelled open, but generated research classifications/summaries
were not used as mathematical evidence. The corpus and raw row are not
included in this public packet.

## Bounded repository prior-work check

Repository: https://github.com/AlecKriebel/Math

At the observed main commit
`fab787f7df8b481cc95df2be593b6f64a4818585`, the QUEUE.md row was queued, 0/5.
That queue entry alone was not treated as proof of no previous attempt.
Additional checks were made:

- Pull-request searches in all states for `6200007` and `AMR-061-0007`:
  no matching results, including a fresh repeat before freezing
- Commit search for `6200007`: no matching results
- Branch search for `6200007`: no matching results
- Default-branch code search for `6200007`: no matching results
- Direct lookup of `unsolved_math_prioritization/attempts/6200007` and its
  README: both returned not found
- A broader title search returned an unrelated early PR titled
  “Codex/stc jc v1.1.0”; no identity-specific match was found
- Direct repository-qualified pull-request searches for the quoted ID,
  quoted AMR identifier, and the combined words Kapovich/convergence each
  returned total_count=0 and incomplete_results=false on a final check

Conclusion: no earlier identity-matched attempt was found by these checks.
This is not an exhaustive historical-priority search. No remote write was
made during preparation of this author packet. Any later queue update should
change only this problem's status/turn cells to `unsolved | 5/5`, subject to
independent review, leaving other queue contents untouched.

## Primary literature and exact dependency map

### [B98] Brian H. Bowditch, A topological characterisation of hyperbolic groups

J. Amer. Math. Soc. 11 (1998), 643-667. Author version:
https://bhbowditch.com/papers/bhb-topchar.pdf

Used dependencies: the finite-tree crossratio construction (Theorem 2.1),
path quasimetrics and their graph models (Section 3), the triple quasimetric
and boundary identification (Proposition 4.2, Lemma 4.3, Propositions 4.4
and 4.7), and the annulus implications (Section 6). Section 7 distinguishes
finite-orbit systems, which supply (A1)-(A2), from triple cocompactness, used
in Lemma 7.6 to obtain (A3). The relevant arguments and their direct
crossratio dependencies in Sections 2-7 were read, not only the abstract.

This supplies a positive result under additional uniform-convergence
hypotheses and a sufficient annular criterion. It does not establish the
general target. The initial paper's extracted text has a nesting-orientation
inconsistency; we use the explicit consistent convention in [S19] and [A22]
and state it fully in TURN_2.md. We do not rely on a reversed nesting formula.

### [B99] Brian H. Bowditch, Convergence groups and configuration spaces

Geometric Group Theory Down Under (1999), 23-54. Author version:
https://bhbowditch.com/papers/bhb-convergence.pdf

Read Proposition 1.1 and its complete proof through Lemmas 1.2-1.7,
including the finite-kernel convention. This is the credited equivalence of
triple properness and collapsing subsequences used in the compactness
arguments. Elementary hyperbolic boundary facts are standard background,
not novel inputs discovered in this investigation.

### [S19] Bin Sun, A dynamical characterization of acylindrically hyperbolic groups

Algebraic & Geometric Topology 19 (2019), 1711-1745.
https://doi.org/10.2140/agt.2019.19.1711
Author manuscript v4: https://arxiv.org/abs/1707.04587v4

Read the precise main statements and all of Section 6's construction,
including Propositions 6.4 and 6.6 and their proofs. The latter graph step
is reproduced with explicit bounds in Lemma 2.1. Corollary 1.3's conclusion
is group-level acylindrical hyperbolicity. It does not assert a homeomorphism
between the constructed boundary and the prescribed compactum. The full
acylindrical-hyperbolicity proof is not an input to our scoped theorem.

### [A22] Aitor Azemar, Random walks on convergence groups

Groups Geom. Dyn. 16 (2022), 581-612.
https://doi.org/10.4171/GGD/654
Publisher PDF: https://ems.press/content/serial-article-files/30115

Read the introduction and Sections 2.3 and 3.1, including the proofs of the
finite-annulus compactness lemma, Lemma 3.10, Proposition 3.11, and the
boundary map/inverse through Proposition 3.15. Proposition 3.21 and its proof
were also inspected for the full-measure scope. The distinction between
finite and infinite boundary points is essential. Our finite-annulus
lemmas are closely related deductions, and the modular bounded-orbit
argument is presented explicitly rather than mislabelled as a resolution.
No random-walk theorem is needed to prove Theorem 4.5.

### Secondary roadmap, not a proof dependency

Peter Haissinsky, Actions of quasi-Moebius groups, Section 3.4:
https://phaissin.perso.math.cnrs.fr/Doc/actionqmobius.pdf

This helped identify the distinction between a convergence action and a
uniform quasi-Moebius metric realization. Its accounts of other authors'
results are not used as substitute primary proofs. In particular, no
Freedman-Skora example is asserted to be a counterexample to this minimal,
arbitrary-compatible-metric problem.

## Attribution, claims, and publication scope

Finite-star realizations, elementary convergence facts, standard tree
geometry, modular dynamics, and the hyperbolic-plane action are credited
as classical tools. The Bowditch-Sun-Azemar mechanisms are credited where
used. The packet claims checkable scoped deductions and explicit failed
construction tests, with no novelty certification, first-resolution claim,
or human-refereeing claim. The universal problem remains unresolved.

SOURCE_MANIFEST.json records the primary reading copies' byte fingerprints.
It contains bibliographic metadata only. No source PDF, source-image file,
whole-paper extraction, catalogue corpus, or private preparation material
belongs in the public upload.
