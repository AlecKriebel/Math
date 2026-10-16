# PRIMARY_SOURCE_ACCESS
Audit: PR203 / 5100011 / k203,a. Accessed 2026-10-16, beginning 07:56:27 UTC. Exact plan predates favorable project material; independent findings frozen 08:00:43 UTC. Scope is provenance and statement overlap, not proof verification.

## Positive full-target object
Alper Ferudun, *Pedal Areas of Periodic Elliptic Billiard Trajectories with Respect to an Arbitrary Point*, v1.0, dated 15 October 2026.
- Original record: https://zenodo.org/records/23400541
- Original metadata: https://zenodo.org/api/records/23400541
- Original PDF: https://zenodo.org/api/records/23400541/files/AMR-050-0011-paper.pdf/content
- Public canonical reading URL: https://eulersolve.org/papers/amr-050-0011/paper.pdf?v=5c54d3e2e525
- DOI registration metadata: https://api.datacite.org/dois/10.5281/zenodo.23400541
- Pages 1–2 define the two ellipses, least period, signed shoelace areas and feet to original side LINES. Theorem A, p.2, asserts A A_M=C0+C2(M dot M) for every point, any winding, and least N divisible by four. Section1.4, p.4, covers reversal and distinguishes repeated lists. Section4, pp.9–11, gives the pole/zero argument. Page14 Table2 includes a star family with a radial zero and negative products. These establish full statement overlap with this audit's target. No nonzero-pedal hypothesis is imposed.
- Access: actual 183271-byte original PDF fetched and text-extracted in memory; relevant definitions, theorem, conventions, proof architecture, examples, priority note and bibliography inspected. Not accepted solely from search snippets/abstract. SHA256 5c54d3e2e525d794fec25be6ec1a929eaccc95e2332b0ae6ee0ed780e46098a0; record MD5 a4b37cdde9f8c9b0e2c3185d7715933a matches fetched bytes.
- The browser tool could parse EulerSolve's PDF, but its DOI/Zenodo HTML/API opens returned internal errors. A direct in-memory HTTP API/PDF fetch succeeded. A later direct EulerSolve HTTP fetch returned403; do not call that failed fetch independent byte verification of the website copy. The URL cache prefix agrees with the deposited SHA prefix. No PDF is copied into this audit.

## Early statement, versions and literal conventions
Reznik–Garcia–Koiller:
- https://arxiv.org/abs/2004.12497 — original version-history record.
- https://arxiv.org/pdf/2004.12497v1 — *Forty New Invariants*, p.2 signed areas; p.3 §3.3 pedal definition; p.4 TABLE2 k203,a.
- https://arxiv.org/pdf/2004.12497v11 — *Eighty New Invariants*, pp.3–4 conventions/definitions; p.6 TABLE3 k203,a.
- https://armj.math.stonybrook.edu/pdf-Springer-final/021-0174.pdf — *Fifty New Invariants*, pp.343–344 definitions/status-column explanation; p.346 TABLE3.
The row records A A_m, N congruent0 modulo4, all M, detected4/20, with '?' in the proof column. It is an earlier experimentally reported claim, not a proof. The printed table does NOT say primitive/least period. This audit's least-period restriction is explicit; it must not be put inside a purported literal quotation. A repeated primitive6 trajectory listed twice does not satisfy the target. The historical '?' does not establish present-day open status.
Actual v1 PDF was opened through the primary arXiv URL. Supplied v11 and journal PDFs were text-extracted in memory and hashes verified; no new full-text files/renders created.

## Centered specialization and complementary outer result
Ferudun, *Center-Pedal Area Products in Elliptic Billiards*, v1.0:
https://zenodo.org/records/23085904 ; original PDF https://zenodo.org/api/records/23085904/files/main.pdf/content .
Theorem1 p.1 asserts the ORIGINAL-orbit product only for M=O, least N odd or divisible4. The setting and conventions are on p.1; p.2 develops a reflection telescope. This overlaps the central specialization, not all M. Actual original78322-byte PDF read in memory, SHA2568ba41a5466bc289a9f714b57527f596fbe39b3422bc6bcf0a95d39bbde50c40c.

Ferudun, *Outer-Pedal Area Products in Elliptic Billiards*:
v1.0 https://zenodo.org/records/23087221 ; v1.1 https://zenodo.org/records/23088516 .
Original PDFs https://zenodo.org/api/records/23087221/files/main.pdf/content and https://zenodo.org/api/records/23088516/files/main.pdf/content .
Theorem1 p.1 is the product of OUTER-tangent-polygon area and its boundary-tangent pedal, for least N congruent2 modulo4 and arbitrary M. v1.1 Theorem2 p.2 adds its centered outer case. Neither is this original-side-pedal target. Relevant full pages1–2 in both original PDFs read in memory. v1 has90127bytes/SHA2563c6791ae0099a49b9215844c506970806148f0ab568a5be2bd798616b0f1d0c9; v1.1 has100311bytes/SHA2565ff816c279e39f478e96ae5454779cc3b5280bc9eed1084429578540b3d352b6.

## Existing theorems and methods, not exact-target proofs
- Chavez-Caliz, *More About Areas and Centers of Poncelet Polygons*: https://arxiv.org/abs/2004.05404 ; https://armj.math.stonybrook.edu/pdf-Springer-final/020-0154.pdf . Journal Theorem3 p.93 and repeated Theorem6/proof p.104 concern original area times OUTER tangent polygon area for even Poncelet families between concentric ellipses in general position. The second factor differs from the pedal. Page104 explicitly uses a meromorphic area product, complementary poles/zeros and constancy on the elliptic curve. Actual supplied relevant pages extracted; journal PDF816433bytes/SHA2569e575ffa9a67e3a4f5af90f0cb2824c190f06768afa30f1ad7c920921f9224bf.
- Stachel, *On the Motion of Billiards in Ellipses*: https://arxiv.org/abs/2105.03624 ; https://arxiv.org/pdf/2105.03624v2 ; https://doi.org/10.1007/s40879-021-00524-2 . Published Theorem4.3/(4.9), p.1614, supplies Jacobi canonical parameters with gcd(N,tau)=1; preprint numbering is Theorem2. Actual supplied journal p.1614 and context read. It is a parametrization/method input.726042bytes/SHA2569121028d7295435740cebb25ec60abe1a0dcc4e96686c226b1b6533bd49515d8.
- Bialy–Tabachnikov, https://arxiv.org/pdf/2001.08469v2 , pp.6–9 Theorems4.1/4.3: outer-foot centroid/squared-distance invariants and focal/center distance products. Different observables; actual primary statements read.
- Akopyan–Schwartz–Tabachnikov, https://arxiv.org/pdf/2001.02934 , pp.2–3 Theorems1–3, pp.5–7 complexification/Liouville argument: cosine invariants and an odd-period original/outer area ratio. Existing method family, not this exact product.
- Roitman–Garcia–Reznik, https://arxiv.org/pdf/2103.11260v3 , pp.2–5: bicentric limiting-point pedal PERIMETER/cosines; complex phase, cancellation of poles, Liouville. Different statement, related method.
- Reznik–Garcia–Stachel, https://arxiv.org/pdf/2009.02581 , pp.2–6 and8: continuous pedal-like curves and moving M on circles/ellipse, rather than finite billiard phase at fixed M. Actual relevant primary text read.
- Recent lead https://link.springer.com/article/10.1007/s00022-026-00818-4 : author text concerns pedal quadrilaterals for fixed arbitrary quadrilaterals; it does not state a billiard family product. Relevant article text inspected. No conclusion about all possible corollaries.
- https://arxiv.org/pdf/2011.06640 : self-intersected orbit lead opened; text search found no pedal occurrence. This is a limited lead check, not an independent full-paper exclusion proof.

## Reading limitations
No other PR was investigated. Generic searches surfaced irrelevant results; these were not processed. Search indexes and source bibliographies supplied leads, never sufficient evidence of theorem overlap. No full literature corpus, inaccessible/private material, unpublished work, non-English historical corpus, or potential unstated corollaries has been exhausted. No contact or outreach draft was made.
