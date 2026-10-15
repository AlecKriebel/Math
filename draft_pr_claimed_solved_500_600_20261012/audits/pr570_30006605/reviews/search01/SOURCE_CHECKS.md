# Primary-source checks — search01

Inspected 2026-10-15 UTC. Read-only scholarly retrieval only; no person contacted.
No full source PDF/text is included in the authored integrity seal. Cached PDFs,
local renders and extracted text reside only under `scratch/sources/`.

## Original question

Primary record: [MFO, Median Geometry and Applications, OWR 8/2026](https://publications.mfo.de/handle/mfo/4442).
Primary PDF: [official report](https://publications.mfo.de/bitstream/handle/mfo/4442/OWR_2026_08.pdf?isAllowed=y&sequence=1).
DOI [10.4171/OWR/2026/8](https://doi.org/10.4171/OWR/2026/8).
Printed pp. 504-506 were visually inspected from local page renders, in addition
to checking the browser's extracted text. The browser screenshot endpoint failed;
local Poppler rendering supplied the visual check.

Ducoffe's definition on p. 504 uses nonnegative real multiplicative vertex
profiles, finite support, and centers among vertices. Page 505 asks for an
almost-linear algorithm on median graphs of bounded cube-dimension amid an
n-vertex finite complexity discussion. Page 506 discusses arbitrary edge lengths
as a separate extension. The candidate explicitly answers this finite graph
algorithmic interpretation. The broader definition allows infinite graphs, whose
encoding is not specified in that algorithmic question.

The empty-support radius convention is implicit in the OWR definition. The
candidate's full-V maximum makes it zero; ESA p. 133:6 explicitly makes every
vertex a center in this case, confirming the intended optimization convention.

Downloaded PDF SHA-256:
`92d33ad86e2ba37d8df828c147e73b40e32206e7090cc6d74c34e5eba47f7c51`.

## Credited generic search prior

Primary record: [Ducoffe, ESA 2026, Beyond Trees](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ESA.2026.133).
Primary PDF: [published paper](https://drops.dagstuhl.de/storage/00lipics/lipics-vol388-esa2026/LIPIcs.ESA.2026.133/LIPIcs.ESA.2026.133.pdf).
DOI [10.4230/LIPIcs.ESA.2026.133](https://doi.org/10.4230/LIPIcs.ESA.2026.133).

Printed p. 133:6 was visually inspected in full, including the proof of Lemma 2.
It gives a general decision-to-optimization reduction using weighted row
midpoints, with O((T(n,m)+n) log n) running time. The credit in the candidate is
substantively accurate. Its pinpoint can be tightened from pp. 133:6-133:7 to
p. 133:6, an optional editorial matter. The candidate independently proves a
slightly slower comparison-only search that avoids real division/floor.

Downloaded PDF SHA-256:
`d51056c90b9d5bfb41b2554ee5e33f994fb33149d6b56b2d56f694a6528c5816`.

## Imported additive oracle

This review deliberately treats the BDH additive-eccentricity theorem as an
explicit interface assumption. It neither infers that interface from an abstract
nor certifies the entire published proof. A separate independent family handles
its full applicability/proof audit. No findings were requested from that family.
The exact needed interface is recorded in REPORT.md and VERDICT.json.

No historical-priority conclusion is drawn from this source check.
