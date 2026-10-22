# Post-freeze exact-target comparison — Ferudun AMR-050-0026

This comparison changes the priority disposition: there is now a verified existing manuscript that directly proves the submitted general target. It is [Alper Ferudun, *Stationary Focal Antipedal Centroids for Even Elliptic Billiard Periods*](https://eulersolve.org/papers/amr-050-0026/), DOI [10.5281/zenodo.23071366](https://doi.org/10.5281/zenodo.23071366). Its six-page PDF and full LaTeX source were read after the independent original-author search froze at 2026-10-12T12:34:36.309594+00:00. The initial report, freeze, source pins and original manifest remain byte-for-byte unchanged.

The candidate supplies a mathematical proof, not only a repeated numerical observation or a special-period example. I detected no gap in its core all-even theorem. Its exact construction, domain and period conventions coincide with the submitted target. Its current official archive records associate the complete checked files to a deposit with clocks preceding PR259 creation. These facts justify treating the general result as an **existing target theorem/reproof**, with attribution. They do not establish an absolute first proof, historical first visibility, causal dependence, or copying.

## Exact theorem match and proof pins

| Audited condition | Candidate evidence |
|---|---|
| Original ellipse a>b>0 and strict nondegenerate confocal elliptical caustic | Section 1, PDF pp1–2, 0<λ<b² |
| Primitive least even N≥4, all coprime stars | Section 1 explicitly defines least period; half-period pairing and coprime winding include genuine stars |
| Every real phase of the prescribed family | Theorem 1 p2; the proof operates on the infinite fixed Poncelet family rather than sample orbits |
| Intersections of consecutive **original** tangents | Definition on p1; outer-conic polar equation (3), p2 |
| Pole either original focus | Definition p1; D=b²I+FFᵀ in Section 2 uses the original eccentricity |
| Full perpendicular lines, arithmetic vertex mean | Equation (1) and definitions p1; no pedal feet, focal inverses or area weights |
| Finite unique real intersections | Support inequality and determinant after equation (7), p2 |
| Phase constancy and focal-axis location | Theorem 1, equation (13) p3, Lemma 2 pp4–5 |
| C(−F)=−C(F) | Consequence of central pairing/linearity in F in equation (10), rather than an extra independent theorem |
| N=4 value zero | Candidate references its separate rectangle paper [6]; also follows from its general displayed formula by the derivation below |
| Odd primitive orbit padded to an even list excluded | Explicit least-period convention and rejection of padded odd cycles pp1–2 |
| Traversal reversal and self-intersections | Theorem 1 and post-lemma argument pp2,5; signed-area centroid is outside the theorem |

The geometric proof first identifies a fixed **nonconfocal** outer ellipse. Opposite-edge antipedal intersections are added exactly, giving a weighted boundary-normal sum in equation (10). The outer ellipse is then affinely normalized to a circle, with the original ellipse becoming a strictly nested concentric ellipse. Equation (13) expresses the arithmetic centroid through the adjacent complex-product trace.

Lemma 2 constructs the smooth compact bidegree-(2,2) curve and the global nonbacktracking step. Closure of infinitely many real family pairs forces that step's N-th iterate to be the identity. At a coordinate pole, the two adjacent edge products are grouped through Vieta's relation; equation (18), p5, is regular there. Adjacent coordinates cannot both have poles, so simultaneous nonadjacent poles are counted without losing or duplicating edge labels. Constancy then follows from compactness, and conjugation makes the trace real. The η=0 case and infinity charts are explicitly covered. This is a full global argument rather than reliance on finite checker output.

I checked the load-bearing scope and analytic steps against the primary body and source. Root's already-completed numerical/algebra audit was context, not a premise of my proof classification. I did not rerun its three checkers as though that would replace the proof. The candidate's certificate supplies the analytic details; its complete source includes the longer compact-trace note. AST Theorem 5, PDF pp5–6, and Schwartz–Tabachnikov's compact-curve argument establish the method lineage; they do not literally state this outer-original-focus application. The candidate credits that distinction.

## Independent deduction of the two apparent refinements

Let D=diag(a²,b²), c²=a²−b², and fix F=(c,0). In the candidate's equation (10), the matrices and denominator depend on F only through FFᵀ or squared components; the numerator is linear in F. Replacing F by −F therefore changes the centroid's sign. The central pairing assures that this is the same prescribed real polygon, not a change to an unrelated focus or family.

For N=4, the affinely normalized circle vertices have the form z₀,z₁,−z₀,−z₁, so their adjacent-product trace is zero. This is a rectangle; consecutive chord normals are perpendicular. The squared distances of its two neighboring sides from the circle's center add to one. Since those sides are tangent to the concentric ellipse, their squared support values add to U+V. Thus U+V=1, which gives λ=a²b²/(a²+b²). With the candidate's α=(b²−λ)/b⁴ and κ=α+λ/(a²b²), we obtain κ/α=2. Since L_y²=1/α, its equation (13) gives both centroid coordinates zero. These elementary deductions show that the sign and four-period refinements do not rescue general-target novelty merely because they are not both restated in Theorem 1.

## Authenticated contribution and date association

I independently fetched the website reading copy, source ZIP, metadata, verification report and official DataCite API record. Website PDF: 82,690 bytes, SHA-256 `317178430532655300d12aff19391751a3dc32ab6913b5062a4df803d56355b6`; source ZIP: 47,229 bytes, SHA-256 `b43108ae779b1f403e7e0f4c7d632b0ef49c2eb61c6be50178e5da3ce86e0183`. The ZIP was safely extracted only inside this audit's comparison_private directory.

Own GET of the Zenodo record returned HTTP403. I therefore used the archive family's actual primary API/file captures, copied them into my private evidence directory, and **independently rehashed** each against the official record's MD5/size fields and my own website bytes. All three files agree: main.pdf, arxiv_source.zip and verification_report.md. The exact calculations, primary record URL, source-local provenance, hashes and truthful distinction from own provider GET are in COMPARISON_ARCHIVE_ASSOCIATION.json. The public DOI, full-file body and record association are not being inferred from a search snippet or an author date alone.

| Event/field | Verified clock | What it establishes |
|---|---|---|
| Candidate website and metadata date | 2026-09-30 | Author/publisher stated manuscript and online date |
| Candidate PDF p1 and main.tex date | 2026-10-01 | Printed document date; differs from website date |
| Zenodo record created | 2026-09-30T22:04:12.260164+00:00 | Official current record creation clock |
| Zenodo record modified | 2026-09-30T22:04:12.820855+00:00 | Official current record modification clock |
| DataCite created/registered/updated | 2026-09-30T22:04:13.000Z | DOI record clock; state findable and issued date Sep30 |
| Submitted PR259 head author/committer date | 2026-10-01T12:06:30Z | Commit identity's declared dates, not push/publication time |
| PR259 creation | 2026-10-01T12:07:07Z | GitHub PR creation event |

DataCite was fetched independently from [its official API](https://api.datacite.org/dois/10.5281/zenodo.23071366), 8,098 bytes, SHA-256 `f804f9714428f2b974df62d95e42da38b8a32844665c832dfd2b8b61c9c209f2`. PR259 and its current head commit `0524ed734ee8185681d030af98088259134a6af7` were independently fetched via read-only GitHub GET; head identity matched authenticated intake. The full receipts are in COMPARISON_PINS.json.

The official record clocks precede the PR creation clock by roughly fourteen hours. **That is the supported clock ordering.** Current record/file association does not reconstruct every possible prior upload, replacement or access event. Neither document's own date proves when its exact bytes first became visible. These observations do not establish absolute first visibility, when either author began work, when either proof was obtained privately, or causal influence. No copying allegation is supported or made. The candidate itself states no absolute-priority certification.

## Current disposition and remaining gaps

The original authors' 2020 experimental observation remains the correct attribution lineage. Ferudun's exact-target general proof is a currently verified contribution with a recorded deposit chronology preceding PR259's creation. Cite both contributions distinctly. The submitted proof may be an independent alternative Jacobi-torus proof, but a different derivation does not restore first-proof novelty for its target statement. Its general theorem, sign symmetry, and N=4 specialization overlap the checked candidate.

Recommended disposition: **retain mathematical correctness separately; classify the core k407 theorem as an existing-result reproof and reject first-proof/novel-general-theorem clearance.** Any publishable new contribution would need a specific additional theorem, stronger result, materially improved proof, explicit general value, or other independent benefit, with a fresh comparison demonstrating that benefit. Root's separately noted Jacobi/cyclic-identity closed-form route is not evaluated or certified here.

No remaining scope gap was detected for the candidate's core constancy/axis/finiteness proof. Absolute historical proof priority remains unresolved; earlier unindexed proofs or broader reusable identities could exist. The printed-date/website-date mismatch remains recorded and is not silently repaired. Peer review status is not the same as mathematical proof completeness: this is an unrefereed preprint, and this comparison makes no claim of formal proof-assistant verification or independent human review.

The independent lineage report and frozen artifact set remain intact. COMPARISON_MANIFEST.json inventories this separate addendum, scope matrix, date pins, archive association, research log and private evidence; comparison_private must be excluded from publication. No Git/provider writes, release, external contact or outreach occurred.
