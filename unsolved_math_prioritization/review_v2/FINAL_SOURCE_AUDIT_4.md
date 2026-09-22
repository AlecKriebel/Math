# Independent source challenge — shard 4

2026-09-22. All 2,576 shard records have individual reviews, in exact assignment order, with no duplicates (100% desk coverage). This separate bounded audit read the complete cached statements and reports for four provisional leaders, then checked primary sources. It is triage validation, not a proof attempt or exhaustive literature review.

| ID | Recommendation | Five-turn assessment |
| --- | --- | --- |
| 20001753 | Exclude from unsolved queue: exact published theorem located | Original target already answered; no novelty credit |
| 6200089 | Retain as deferred candidate, reduce p_solve from .08 to .03 | Infinite-stabilizer extension is substantive, not automatic Garland application |
| 10600051 | Retain conditional candidate, reduce p_solve from .15 to .03 | Proposed ordinary odd-parity mechanism also forces uniqueness; another certificate is needed |
| 10400226 | Retain candidate, reduce p_solve from .15 to .03 | Missing source remark shows the remaining arithmetic is much narrower and harder than small Seifert matrices |

## 20001753 — Every lattice has a basis of strict Voronoi/facet vectors

**Decisive omitted source.** Engel, Michel, and Senechal, *Lattice Geometry*, IHES/P/04/45 (September 2004), §4.1.2, Theorem 27, printed p. 207 (PDF page 211), states that every lattice has a basis of facet vectors. Printed p. 206 attributes the proof and algorithm to Engel [ENG02]. I downloaded the author-hosted PDF and visually inspected these two pages because its embedded text encoding is corrupt. The theorem exactly matches the source parenthetical “vectors defining facets,” not merely weak Voronoi vectors or a generating set.

Primary source: [Lattice Geometry](https://pagesperso.ihes.fr/~vergne/LouisMichel/publications/LatticeGeometry.pdf). Publication record for the original paper: P. Engel, “On the determination of a lattice basis of facet vectors,” *Rendiconti del Circolo Matematico di Palermo*, Serie II, Supplement 70 (2002), 269–278; confirmed in the [University of Bern 2002 publication list, item 187](https://www.dcbp.unibe.ch/e39507/e86495/e86520/files86525/Publikationen-2002_ger.pdf).

The more recent [Doulgerakis–Laarhoven–de Weger paper](https://link.springer.com/article/10.1007/s10623-022-01119-y) conjectures a basis among **irreducible** vectors, a stronger restriction. Its existence does not justify ignoring the facet-basis theorem. The cached report's general “no proof located” statement is therefore unreliable. This audit confirms the primary theorem's exact statement and proof location, not every proof line or subsequent reception; exclude/known-resolution hold is appropriate before spending five novel-research turns. Suggested p_valid_open=.02 and decision=exclude.

## 6200089 — Property T for a developable triangle of Property T groups

The [current author-hosted Kapovich source](https://www.math.ucdavis.edu/~kapovich/EPR/problems.pdf), PDF p. 22, Problem 89, matches the dataset verbatim in substance. Another archived version numbers it 90; this is version drift, not a different problem.

The standard spectral machinery is real, but its scope must not be enlarged silently. The [Bekka–de la Harpe–Valette text](https://perso.univ-rennes1.fr/bachir.bekka/KazhdanTotal.pdf), Chapter 5, uses compact/open stabilizer hypotheses in its building theorem. [Caprace et al., Hyperbolic generalized triangle groups](https://arxiv.org/abs/2011.09276), §§2–3, relate representation angles to link spectra in their finite local-group setting. Neither inspected result settles arbitrary infinite Property T cell groups.

The proposed route must show why the ordinary link Laplacian controls the relevant coefficient-valued affine cocycles despite infinite stabilizers. Separate fixed points for each stabilizer do not imply a common fixed point. Infinite links also require the exact meaning of normalized spectral gap, domains, and summability. Those are the central problem, not routine technicalities. No exact later solution was found in this short audit. Suggested note: “Finite-stabilizer spectral criteria do not cover arbitrary Property T cell groups; a coefficient-valued link inequality must bridge the infinite-stabilizer gap.” Impact5, p_solve=.03, p_valid_open=.75, proof, defer.

## 10600051 — Nonunique minimal free-link representatives

The [Fenn–Ilyutko–Kauffman–Manturov problem list](https://arxiv.org/abs/1409.2823), item51, is the actual existential target. The cached citation “arXiv:1008.xxxx” is invalid and supplies no literature verification.

The current route invokes parity-certified minimal diagrams plus a crossing-preserving move. Ordinary irreducibly odd parity certificates are too strong: they force a copy of the diagram inside every equivalent diagram, hence uniqueness at the same crossing count; parity axioms also prohibit an all-odd third Reidemeister triangle. Thus that particular mechanism cannot simply produce the requested pair.

A genuinely different graph-valued certificate may remain viable. [Kauffman–Manturov, arXiv:1207.0719](https://arxiv.org/abs/1207.0719), Corollary3.4 and its following discussion (PDF p.12), explicitly distinguish equality of the unoriented resolutions from equality of the original framed diagrams and discuss third Reidemeister moves. This supplies a route worth assessing, but not an already-constructed nonisomorphic minimal pair. Its girth-at-least-five subclass has no triangle for such a move. No resolution was located here.

Before attempts, fix equivalence of representatives as framed-graph isomorphism, clarify components/orientations, and require both a legal equivalence sequence and an independent global crossing-minimality certificate. Do not equate lack of local reductions with minimality. Suggested p_solve=.03, p_valid_open=.65, hybrid, candidate; note the new certificate rather than generic parity.

## 10400226 — Determinant 4k+1 and signature four

The [Ohtsuki source and accompanying Stoimenow remark](https://web.math.ucsb.edu/~bigelow/publications/03.14problem.pdf), Problem12.21, add important information absent from the dataset extraction: any counterexample greater than one must have all prime divisors congruent to1 modulo24 and at least2857. The source also gives families represented by specific elementary symmetric polynomials on positive odd arguments. The question is universal over n, not a request for a few examples.

An explicit Seifert-matrix family is a valid proof-first direction, but it must simultaneously maintain unimodularity of the skew part, determinant n of the symmetrization, and signature four for **every** admissible n, including the residual arithmetic class. Sampling small determinants or repeating the existing pretzel-polynomial construction will miss precisely what remains. No later exact resolution was found in the targeted search; this is not a verified current-open claim.

Suggested p_solve=.03, p_valid_open=.65, impact3, proof, candidate. Suggested note: “Seifert-matrix realization must handle the residual prime-factor class1mod24 beyond established pretzel constructions; determinant and signature constraints must hold uniformly for all n.”

## Audit limitations

No proof or solution has been claimed by this project. Search non-detection does not establish current openness. The clear correction is the lattice theorem; the other three are probability/route downgrades based on exact scope and primary-source obstacles. No parent-owned review or queue files were changed.
