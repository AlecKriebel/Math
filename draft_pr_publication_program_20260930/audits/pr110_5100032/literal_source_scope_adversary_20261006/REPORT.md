# Independent literal-source and scope adversarial review of PR110

The submitted theorem addresses the entire literal k603 target in the two designated original primary sources, within their nondegenerate confocal ellipse-pair setting. I found no required or optional correction for this assigned source/scope gate. This is not a certificate of the full algebraic proof, novelty, current open status, or publication readiness.

## Independence and immutable target

I read the original `PROOF.md`, `source_record.json`, `source_manifest.json`, and `prior_imported_report.json`, plus the applicable policies and original blob-authentication metadata. Their bytes and SHA256 values were independently checked against `ORIGINAL_BLOB_MANIFEST.json`. Original PR head: `3d159f0a00d0bd7ff8d558d6fbc75af5094f7a35`; problem ID 5100032 / AMR-050-0032; original budget 2/5. No submitted `independent_review` content or current other-agent report was read. Additional central proof-search turns: 0.

Success criteria were fixed in `SCOPE.md` before primary-source inspection. I treated the imported statement, source scope, proof's branch choice, ordinary-distance interpretation, and degeneracy exclusions as hypotheses. No Git/index/branch/native-assessment/service/publication changes, external contacts, or further subagents occurred.

## Primary-source binding and reading

I inspected these exact primary PDFs read-only:

- Reznik, Garcia, and Koiller, *Eighty New Invariants in the Elliptic Billiard*, [arXiv:2004.12497v11](https://arxiv.org/abs/2004.12497v11), revised 29 October 2020. PDF 3,389,610 bytes, SHA256 `c56bb4ea29734ed04ee153206bb8619286df544714fd3f77fe97bdc945dfe1da`, exactly matching the submitted source-manifest pin.
- The same authors, *Fifty New Invariants of N-Periodics in the Elliptic Billiard*, Arnold Mathematical Journal 7 (2021), 341–355, [DOI 10.1007/s40598-021-00174-y](https://doi.org/10.1007/s40598-021-00174-y), [journal-hosted PDF](https://amj.math.stonybrook.edu/pdf-Springer-final/021-0174.pdf). PDF 1,836,579 bytes, SHA256 `c2a2e644521fd03a15833a23bd57c2498b5644036f6bc8fe682c40581f640d42`.

The arXiv live landing page independently identifies v11, its authors, revision date, and the related published DOI. I read the complete relevant introductions, preliminaries, table-column explanations, §§3.5 and 3.7, Table 7, appendices of symbols, and experimental-method discussion. I also inspected the rendered arXiv PDF pages 1, 6, 7, 8, 9, 15 and published PDF pages 7, 9, 13 (printed 347, 349, 353). The table superscripts, summation signs, distance bars, period column, and figure construction were visually confirmed; conclusions do not rely on a potentially flattened text formula. `SOURCE_READ_CUSTODY.json`, `RENDERED_PAGE_PINS.json`, and `PROCESS_JOURNAL.json` record coverage and actual processes. Full PDFs, extracted text, and figure renders remain private and are excluded from the public output seal.

The following source comparison is deliberately short. Both introductions define this billiard using two confocal ellipses. Their §3.5 gives perpendicular objects through original vertices; Fig. 3 displays their supporting-line intersections. §3.7 and the symbol appendices define the focal antipedal quantities as Euclidean norms. Table 7 k603 is the ratio of their unprimed sums, value 1, with every admissible period and an unknown-proof marker at the source date. Table-column notes distinguish unknown proof from unknown value. No parity, convex-polygon, simple-polygon, or primitive-period restriction appears for k603.

## Exact claim and possible omitted components

For an outer ellipse with semiaxes a>b>0, let c²=a²−b² and foci (±c,0). A smaller nondegenerate confocal ellipse necessarily has squared semiaxes a²−λ, b²−λ with 0<λ<b². For every closed Poncelet billiard orbit tangent to that fixed ellipse, form Q*_{j,i} by intersecting the perpendicular lines through P_i and P_{i+1} to P_i−f_j and P_{i+1}−f_j. The source quantity is

    [Σ_i |Q*_{1,i}−f_1|] / [Σ_i |Q*_{2,i}−f_2|] = 1.

This is exactly the submitted theorem's quantity. The extra inner/outer polygons, pedal areas, and antipedal areas introduced in the imported record are background notation; k603 imposes no assertion about those areas, their products, or their primed/inner analogues. The two editions number some neighboring invariants differently, but k603 and its own quantities agree. An area-ratio proof would not by itself discharge this distance assertion; the submitted result instead targets the indicated focal vertex-distance sums. Neither individual sum is required to remain constant separately.

Taken in isolation, the phrase “confocal caustic” in the imported record could be read more broadly. Its cited original source fixes the ellipse-pair meaning, so the proof's elliptical-caustic limitation is source faithful. A future paper should retain that explicit setting. It would be incorrect to describe this as resolving all focal antipedal questions for every orbit in an outer elliptical billiard, including hyperbolic caustics.

## Perpendicular supporting lines versus literal half-rays

The sources use the word “rays” in §3.5, without fixing a direction convention. Their Fig. 3 depicts successive antipedal vertices on the full perpendicular supporting lines through the original polygon vertices. In the left panel, a single such side through P_1 joins Q*_5 and Q*_1 on opposite sides of P_1. Thus one fixed forward half-ray from each P_i cannot represent the displayed polygon. The proof's explicit line-intersection construction is the consistent mathematical interpretation, not a replacement by pedal feet or a different distance.

I independently tested that interpretation on an exact, genuinely closed four-bounce confocal billiard orbit. Take a=5, b=3, focus f=(4,0), vertices (5,0), (0,3), (−5,0), (0,−3), and λ=225/34. All four chords are tangent to the same nested confocal ellipse: its squared axes are 625/34 and 81/34. Symmetry about the coordinate-axis normals verifies the billiard reflection at each vertex.

For A=(5,0), B=(0,3), the antipedal intersection is Q=(5,29/3). Writing J(x,y)=(−y,x), the parameters in Q=A+t_A J(A−f)=B+t_B J(B−f) are t_A=29/3 and t_B=−5/3. Consequently the two positive J-oriented half-rays do not intersect at Q; reversing J reverses both signs and still fails. This is a negative control for an overly literal half-ray interpretation, not a counterexample to k603. All original focal antipedal distances are positive ordinary lengths, and both focal squared norms agree on each of the four edges in this control. The independent exact control runs pass 83 explicit checks both normally and with Python optimization enabled. No submitted verification program was executed or imported.

This terminology ambiguity is resolved by the source figure and the defined antipedal polygon. The submitted proof already defines full lines clearly. There is no outstanding required repair or optional defect; a brief footnote explaining the source's informal terminology would be a permissible editorial clarification, not a new mathematical hypothesis.

## All periods, winding families, self-intersections, and multiple traversal

The same-side orientation in the proof is legitimate for every regular elliptical-caustic Poncelet orbit, not an extra convexity assumption. From a point on the outer ellipse there are exactly two distinct tangent lines to the strictly inner convex ellipse. Their inward-pointing tangent rays place that ellipse on opposite sides. An incoming directed edge reverses the direction of one ray; continuation on the other tangent therefore keeps the caustic on the same side. This is the nonretracing Poncelet billiard continuation. Choosing one initial orientation propagates it over the whole orbit; the opposite orientation is its reversal.

The origin lies strictly inside the caustic, so each directed edge with the caustic on its left has det(P_i,P_{i+1})>0. Under the outer ellipse parametrization (a cos t,b sin t), this gives an unwrapped local parameter increment in (0,π). Its half-increment lies in (0,π/2), exactly the chord coordinates used in the proof. This is a statement about each consecutive edge, not about the cyclic order of all vertices on the outer ellipse. A star polygon can wind several times while all those local increments remain positive and below π. Hence simple-polygon ordering is not being imposed silently.

Neither k603 nor the telescoping closure step depends on parity. Arbitrary crossing points of nonconsecutive edges are not new Poncelet vertices; they do not enter the source's Q* indexing. Self-intersections of the original or antipedal polygon do not alter the ordinary-distance sum. Signed-area conventions and possible zero antipedal signed areas are irrelevant to this norm identity. Reversing the orbit permutes the unoriented chord intersections and sums. Repeating a primitive closed orbit multiplies each sum by the same positive integer; the ratio remains 1. No primitive-period hypothesis is needed.

This source/scope review confirms that the proof's claimed per-edge identity, if validated by the separate algebraic review, telescopes over every admissible closed orbit above. I did not use low-N tests to infer its all-N coefficient or undertake a new central proof search.

## Nondegeneracy and limiting cases

Each focus is strictly inside the inner ellipse, since c²/(a²−λ)<1 is equivalent to λ<b². A tangent line to that ellipse therefore cannot pass through either focus or through the origin. Distinct endpoints of a chord then cannot be collinear with a focus; the two antipedal perpendicular lines intersect uniquely at a finite point. The intersection cannot equal the focus because its defining equation has a strictly positive squared endpoint distance on the right. Thus every summand and the denominator sum are positive and finite. This supplies geometric justification for the submitted nondegeneracy claims without treating a signed height as an ordinary distance.

λ=0 merges the two ellipses and gives no nonzero chord tangent to the inner curve. λ=b² produces a degenerate confocal conic and invalidates the strict-interior argument; focal-height denominators can vanish. Hyperbolic caustics and the axis two-bounce limiting orbits likewise are not members of the defined nondegenerate ellipse pair. Table 7's all-period column means periods for which the specified regular family exists, not arbitrary undefined one- or two-vertex antipedal polygons. No extension through these singular limits is needed to resolve the literal k603 entry. The submitted circle-limit observation is harmless (coincident foci make equality immediate), but a=b is outside the sources' a>b setup and is not needed for this target.

## Findings, custody, and remaining work

Required findings: none. Optional findings: none. Strongest verified conclusion: the submitted nested-confocal-ellipse theorem faithfully and completely targets the literal unprimed k603 assertion, with correct ordinary-distance interpretation and no omitted parity, winding, self-intersection, or multiple-traversal component among its admissible regular orbits.

The actual process journal records four PDF metadata/extraction processes, nine page renderers, and two independent exact-control processes: all fifteen exited zero. The exact controls used actual PIDs 935 and 936, each completed 83 checks. `VISUAL_QA.json` records full nine-page visual inspection. The public per-file output manifest excludes all full source bodies and derived source pages, while their private metadata pins remain available for authorised local audit.

Remaining gaps for the overall PR: the independent full mathematical proof/program audit, deep priority search, current-literature assessment, and any eventual paper/package review are separate gates and have not been cleared by this report. The source's 2020/2021 unknown-proof marker and the imported prior report are not evidence that this is novel or still open in 2026. This audit grants only literal-source/scope clearance for the exact original proof pin `8478d2a792944c5fb9e8a53324e0c6bce8eba317de29c31a6fcbd6ca0205709d`.
