# Triangle stripe family: target 5500058 / AMR-054-0058

Partial result, 2026-10-11. The universal three-color triangle conjecture is
unresolved by this work. Novelty is not established.

## Review and distribution status

AI-assisted and unrefereed, with an independent internal AI mathematical audit.
Acceptance is scoped to the stated partial theorem; it is not external human
peer review or formal proof-assistant certification. This is not a computational
reproduction package. The proof is self-contained. Programs, raw expanded cases,
datasets, copied source documents and source-derived images are not distributed.
Source hashes authenticate bytes, not correctness, novelty, or current status.
Editorial preparation performed no new mathematical program runs, scholarly
source-body inspection, or literature survey.

## Result

The fixed coloring c(X,Y)=floor(400Y/77) mod 3 of the entire Euclidean plane
avoids monochromatic congruent copies, including reflected copies, of every
triangle (0,0),(1,0),(x,y) in the closed real rectangle
849/1000 <= x <= 851/1000, 349/1000 <= y <= 351/1000.
All real parameter values, all points on stripe boundaries, and all Euclidean
isometries are covered. The general sufficient criterion is retained in full.

This is an independently authored, self-contained partial reconstruction.
Its elementary geometric proof uses half-open stripes, a least-width area
bound, a six-vertex projection hexagon and exact rational bounds. The largest
rectangle squared-norm bound is 9508390661/9744080000 < 122/125, with positive
margin 235689339/9744080000 below one. Exact failed-stripe examples illustrate
why changing a width or triangle without proof is unsafe; those failures say
nothing about the existence of other three-colorings.

## Read the eight files

- PROOF.md: complete sufficient criterion, continuum corollary, center certificate and negative isometry example
- AUDIT.md: complete independent mathematical audit and bounded historical verification
- ACCEPTANCE.md: scoped acceptance, correction and unresolved gap
- ACCEPTANCE.json: decision and bindings for the distributed proof, audit and acceptance report
- SOURCES.json: public source/version identities, retrieval and inspection history, and limits
- VERIFICATION.json: qualified original-inventory authentication and aggregate historical checks
- MANIFEST.json: exact membership and hashes of the other seven files
- README.md: this scope and reading guide

The manifest excludes its own hash to avoid self-reference; the reviewed
publication payload pins it independently. Original proof/audit hashes identify
the accepted mathematical versions; the public file identities are separate.

## Prior work and limits

The center is outside Aichholzer and Perz's two specified 2019 three-color
criteria. Mundinger et al. (ICML 2025) announce additional stripe regions that
appear to overlap this example. A plotted region does not establish exact
containment of our rectangle or identity of constructions. The arXiv v3 and
published PMLR copies have distinct hashes and byte counts, preserved in
SOURCES.json. The published statement that separate triangle papers were in
preparation is historical, not a claim that they remain unpublished today.
Figure 8's numerical threshold is not an all-points proof. The December 2025
Axenovich–Liu–Sagdeev discussion is dated context, not exhaustive present status.

The full target allows a different arbitrary whole-plane three-coloring for
each triangle. This edition supplies a particular sufficient family; it does
not resolve all triangles, establish novelty, optimize stripe widths globally,
or certify other theorems in the cited works.

## Evidence and distribution boundary

The 42-member creator inventory was authenticated with its explicit exclusion
of generated __pycache__ directories; this is not a claim about every regular
file. The 14-member independent-audit inventory was also authenticated. Hashes
and counts verify bytes, not historical claims beyond the stated audit scope.
Original evidence contains source documents, programs and raw results that are
not distributed. The complete proof and mathematical audit remain readable
without those files. No new mathematical tests or source inspection are claimed
for editorial preparation; its checks concern exact file identity, editorial
preservation, additions-only packaging, and repository-tree integrity.

Primary comparisons:
- https://www.eurocg2019.uu.nl/papers/10.pdf
- https://proceedings.mlr.press/v267/mundinger25a.html
- https://arxiv.org/html/2512.15516v1#S1.SS4
