# Sources and scope: directed linear k-cut

Problem 30003993 / OWR-16633-010. Historical source inspections: 10 October 2026.

## Original target

Chandra Chekuri, “Open Problem: Approximation and Integrality Gap for Linear
k-Cut,” Oberwolfach Report 50/2018, printed p. 3013 (PDF p. 45), asks whether
the natural distance LP for the ordered-terminal edge-deletion problem has a
uniform constant integrality-gap bound or admits unbounded gaps. The exact
source statement was read and visually inspected in the independent audit.
[Original report](https://ems.press/content/serial-article-files/46772).

The accepted construction is in that original model: finite simple directed
graphs, distinct ordered terminals, unit edge costs, and every forbidden
lower-to-higher terminal path, including paths with internal terminal visits.
It proves exact integral optimum C_k-k^2 and LP feasibility of cost C_k/3.
The resulting lower bounds tend to 3; actual gaps have liminf at least 3.
Neither actual-gap convergence to 3 nor the original dichotomy is proved.

## Previously reported bounds

Kristóf Bérczi, Karthekeyan Chandrasekaran, Tamás Király and Vivek Madan,
“A tight sqrt(2)-approximation for linear 3-cut,” Mathematical Programming
184 (2020), 411–443, reports general-k bounds ceil(log2 k) above and
2(1-1/k) below. The ceiling is essential when quoting this source. Its tight
sqrt(2) theorem concerns three terminals, and it treats general k as open.
The independent audit read and visually inspected PDF pp. 2, 4, 5, 7 and 30
of the author-hosted journal version, including node/edge definitions and
the distance relaxation.
[Journal-version PDF](https://karthik.ise.illinois.edu/pubs/linear-3-cut.pdf),
[DOI](https://doi.org/10.1007/s10107-019-01417-9).

## Related earlier work

Manuel Aprile, Matthew Drescher, Samuel Fiorini and Tony Huynh,
“A Tight Approximation Algorithm for the Cluster Vertex Deletion Problem,”
discusses gap 3 for the general induced-P3 covering LP, with a random-graph
example. The introduction and PDF p. 4 were inspected via web extraction.
This earlier gap-3 context is credited. No result from it is a premise of the
self-contained interval-weight construction and directed-edge conversion here.
[Primary PDF](https://researchmgt.monash.edu/ws/portalfiles/portal/367152543/341613069_oa.pdf),
[DOI](https://doi.org/10.1007/978-3-030-73879-2_24).

Dibyayan Chakraborty, L. Sunil Chandran, Sajith Padinhatteeri and Raji R. Pillai,
“s-Club Cluster Vertex Deletion on Interval and Well-Partitioned Chordal
Graphs,” supplies related algorithmic context. Only its primary abstract
and bibliographic metadata were inspected; it is not used to prove the
linear-cut construction.
[arXiv record](https://arxiv.org/abs/2210.07699).

## Evidence and limitations

[SOURCE_METADATA.json](SOURCE_METADATA.json) preserves recorded public URLs,
source titles, two mutually corroborated PDF hashes and sizes, inspection
coverage and bounded search queries. Those historical records were verified
against frozen accepted files during edition preparation. The source PDF bodies
were not newly retrieved, rehashed or inspected for this edition. No new
literature search was performed. No PDF hash is asserted for the two related
context sources.

Bounded searches found no resolution or matching theorem. That is not exhaustive
current-status or novelty clearance. No novelty, priority or worldwide firstness
is claimed. The original question remains unresolved by this partial theorem.
This AI-assisted manuscript and audit are unrefereed; acceptance is not external
human peer review, journal acceptance or formal proof-assistant certification.
The complete universal proof and audit do not rely on omitted programs,
generated certificates, datasets or raw outputs. Copied source documents,
extracted source text/images and private coordination material are excluded.
