# Source, scope, and bounded prior-work review

## Exact source

The complete catalog target and all its fields were reviewed. The absent
research-results entry was represented by `{}`, not null, when recomputing
the review hash. It matches the queued catalog hash exactly; byte counts
and SHA-256 values are in `SOURCE_METADATA.json`.

The live numeric [UnsolvedMath page](https://www.unsolvedmath.com/problems/30000432)
returned HTTP 403 in the download attempt, and web opening failed. No live
page text was inspected or claimed. The imported record is matched instead
to the official [OWR report](https://ems.press/journals/owr/articles/1194),
DOI [10.4171/OWR/2006/12](https://doi.org/10.4171/OWR/2006/12).
Its printed page 692, PDF page index 39, was text-inspected and visually
inspected. The question is Problem 2, attributed to Günter M. Ziegler, in
the open problems collected by Günter Rote. The record identifier ending
001 is a catalog identifier, not the report's printed problem number.

The selected outer face is a triangle: the source states n vertices and
3n−6 edges. The question concerns equal bounded-face areas, not arbitrary
area assignments and not equal areas for the exterior face. It allows
ordinary straight-line drawings with collinear nonfacial triples. Prescribing
the exterior triangle's nondegenerate shape is equivalent by an affine map.

## Primary literature and precise evidence levels

* Moritz Firsching, [Optimization Methods in Discrete Geometry](https://refubium.fu-berlin.de/bitstream/handle/fub188/7447/FirschingDiss.pdf?isAllowed=y&save=y&sequence=1),
  dissertation dated 2015, defense 28 January 2016. Chapter 3.2, particularly
  Proposition 45 and Theorems 50–52, pp.56–63, was text-inspected. Theorem 50
  proves existence through 11 vertices. Theorem 51 reports 100,000-digit
  closeness for 12; Theorem 52 reports numerical results for 13–15. Conjecture
  53 retains the general assertion. The author's current
  [project page](https://firsching.ch/equiarea) advertises algebraic solutions
  through 12. Those coordinate datasets were not independently audited here;
  the website description is not promoted to a verified 12-vertex theorem.
  Proposition 45's weighted octahedron obstruction is reconstructed and
  credited in `PROOFS.md`. Its stellated equal-area obstruction is not
  4-connected. The dissertation's finite enumeration was not rerun.
* Linda Kleist, [Drawing Planar Graphs with Prescribed Face Areas](https://www.ibr.cs.tu-bs.de/users/kleist/paper/presAreasJOCG.pdf),
  Journal of Computational Geometry 9(1), 2018,
  [DOI 10.20382/jocg.v9i1a9](https://doi.org/10.20382/jocg.v9i1a9).
  The introduction and negative-results discussion were text-inspected.
  Non-area-universality is a stronger-assignment obstruction and cannot
  substitute for a negative equal-area answer. The paper credits Ringel's
  1990 *Equiareal graphs*; Ringel's original chapter was not retrieved here.
* Linda Kleist, [On the Area-Universality of Triangulations](https://arxiv.org/abs/1808.10864),
  2018 author manuscript, with its [author-hosted PDF](https://www.ibr.cs.tu-bs.de/users/kleist/paper/polyMethod_GD.pdf).
  Related work, the accordion definition, and Theorem 2 were text-inspected.
  An accordion inserts ℓ degree-four vertices into a selected octahedron
  edge; it is the cycle bipyramid with m=ℓ+4. Theorem 2 establishes area
  universality exactly for odd ℓ. Thus odd m already has an affirmative
  equal-area consequence. Even m being non-area-universal says nothing
  against its equal-area realizations. No publication-status claim beyond
  the identified author manuscript is needed for this dependency.

Searches using the exact title, “4-connected” with “equiareal”, Ziegler's
name, and equal-area/accordion terminology located no full later resolution.
This is a bounded negative search as of 5 October 2026, not certified current
openness. The partial results are not claimed to be new.

## Actual prior attempt check

Read-only searches of AlecKriebel/Math's default-branch code, pull requests,
and branches by the exact target ID and catalog number found no matching
actual investigation. Broader triangulation-title results concerned distinct
targets. Available local work and prior conversation context likewise
provided no verifiable matching proof or computation. Generic queue rows
and desk-review notes were not treated as substantive prior attempts.
Search absence is bounded evidence, not a complete repository-history audit.

## Approach ledger

1. Paired-face geometry gives the explicit infinite family and complete
   labeled classification; general triangulations lack the shared-apex pairing.
2. Continuation/degree encounters a genuine interior singularity and opposite
   Jacobian signs at the two octahedron equal-area solutions.
3. Equal-neighbor harmonic placement gives unequal areas; a general variable
   weight selection theorem remains missing.
4. Weighted inductive strengthening is false by a credited exact positive
   octahedron assignment; a restricted realizability invariant is missing.
5. Reflection-equivariant symmetrization is impossible for even cycle sizes;
   averaging can destroy equal areas. Unrestricted variational existence
   remains unproved.

All five are genuine scoped derivations and obstructions. Literature/source
checking and finite replay do not add author approaches. None resolves the
original problem; the disposition is **unsolved, 5/5**.
