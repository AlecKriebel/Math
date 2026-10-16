# Fresh adversarial review of the fixed PR18 preprint package

**Result: no unresolved substantive issue in the fixed mathematical proof, PDF, portable archive, or intended production manifest.** One independently detected error in an external source's proof is recorded below with a corrected argument; it does not invalidate the source's theorem or require a manuscript change. This review is an internal AI examination, not external human peer review or authorization to publish.

Original submitted PR head: `99e403e85d38d92b021198c4a57bbad3cd8775ba`; problem `30001075 / OWR-2090-028`; submitted accounting `claimed_solved`, `1/5`. No additional central research attempt or novelty credit is assigned.

## Independence, exact inputs, and custody

I began from `preprint_v1/paper.tex`, reconstructed the complete argument, and attempted falsifications before consulting the current coordinating priority assessment, submitted provenance, historical candidate, or prior family verdicts. The sealed record is `ORIGINAL_RECONSTRUCTION.md`. I used a bibliographic source ledger only to locate existing private primary PDFs. I did not accept earlier reviewers' mathematical conclusions as evidence. After that reconstruction, I personally checked the primary analytical statements, read the supplied complete 2024 article, inspected the historical question, and reviewed the package and provenance records.

All my writes were confined to `preprint_round2_adversary_family`. Execution and fault injection occurred only in my extracted copies. I did not overwrite shared `verification.json`, alter the fixed package, change Git/index/refs, modify a PR, upload to Zenodo, change a tracker, or communicate externally with any individual. Third-party PDFs, extracted text, and renders are under `tmp/private`, ignored by the tracked root `tmp/` rule. Reused source bodies are explicitly recorded as reuse, not fresh downloads.

The following exact pins were independently checked, both against the supplied values and against archive contents where applicable:

| Artifact | Bytes | SHA256 |
|---|---:|---|
| `paper.tex` | 24,824 | `2522ac0138de5e21067af8c16e6749b3a9d3cd01f12bdb929cca87cb6baeabb6` |
| `common_tangent_nullness.pdf` | 92,307 | `80b3fc3e8cb470a22a1226b960467de9e67dd8c3ccf054b42133d9ba0ce9d327` |
| `common_tangents_null_locus_v1.zip` | 182,613 | `1fd934e9f8b011307137500039192c93c34f505c472a19fb47ba03af3ab5b9c5` |
| `ARCHIVE_MANIFEST.json` | checked in audit | `595bf1903377f68b6836f345bdfa252d6e65342c4d5cce0c67f02fc9f2b333b2` |
| `ZENODO_UPLOAD_MANIFEST.json` | checked in audit | `5d45d5b3ba4137ddfa19efd2b2a8c63055cb308942b8cc9a6c01019d4f0ed119` |
| historical `source/CANDIDATE.md` | 20,728 | `8ac19b70bd9081107e903ca47bb9dd6ad05274f604d03000a7fd18e3cfb3bf12` |
| intended `root_final_package_20261003/zenodo-deposit.json` | checked in audit | `fc0d603caee348ebf8442119b28733349779f53d155681a9f1342f67b9ea291a` |

`ARCHIVE_AUDIT.json` records actual sizes, modes, timestamps, hashes, and the exact member domain. `PROCESS_AUDIT.json` and its per-run captures retain actual controller/child PIDs, argv, runtime, inputs, complete stdout/stderr, and nonoptimized controller execution. `SOURCE_OPERATION_AUDIT.json` similarly records twelve genuine read-only PDF decoding/rendering operations. No process receipt was fabricated retrospectively.

## Literal target and strongest verified result

I personally read and visually inspected the official [EMS report](https://ems.press/content/serial-article-files/46191), section 13, printed p. 2552 / PDF p. 76. Its convention requires actual intersection with the convex set and containment in a plane bounding a closed halfspace containing that set. Its spatial locus is a union of complete lines. Conjecture 4 asks that this locus be contained in a measure-zero set for three pairwise disjoint convex sets. Conjecture 3 separately asks countable containment in 2-manifolds. The manuscript addresses the literal Conjecture 4 and does not assert Conjecture 3.

The strongest result supported by this review is: for every three pairwise disjoint arbitrary convex subsets of R3, the union of complete affine lines actually meeting each and lying in a supporting plane of each has Lebesgue outer measure zero. Empty, nonclosed, unbounded, lower-dimensional, nonsmooth, and nonunique-contact cases are included. No unresolved mathematical gap in that statement was found. Neither a first-proof certificate nor the stronger countable-manifold theorem follows.

The source's background sentence asserting closedness for all convex sets is not imported into the proof. The manuscript's nonclosed example correctly shows why that background cannot be exported beyond the compact setting. Nonclosed arbitrary convex sets may also require outer measure, rather than an unsupported measurability assertion; the compact-cap domination resolves this.

## Mathematical reconstruction and falsification results

The full derivation and attempted counterexamples appear in `ORIGINAL_RECONSTRUCTION.md`. The main review conclusions are as follows.

### Compact reduction and projected support gap

At `paper.tex:50`, distinct actual contacts admit mutually disjoint closed rational balls in one globally fixed ambient coordinate system. Each contact lies strictly inside its ball. Intersecting the original convex closure with that ball yields a nonempty compact convex cap. Supporting inequalities extend to the closure, while the original actual contact remains on the line. Thus each original common tangent is dominated by one of countably many compact triples even when the original closures intersect. I attempted intersecting-closure and unbounded-set objections; neither defeats this reduction.

The support gap is the maximum of normalized support inequalities of the compact projected convex set. With projection interior, its signs are negative inside, zero on the boundary, and positive outside. A projected support line lifts to a support plane containing the entire line, and membership in the projection supplies an actual contact. The signed increment uses a difference of maxima; it does not differentiate a support function. Its plus sign in `du + z dv` is correct. Planar projection interior is preserved exactly for directions transverse to the affine hull. A line meeting a plane and parallel to it lies in the plane, so discarded lines have a null spatial union.

### Two-tangency charts, root domains, and countability

At `paper.tex:89`, an interior projected disk forces every contact normal into one open hemisphere with aperture alpha > 0. A cap with its contact strictly inside the ball retains that entire supporting-normal set: any original point violating a cap support inequality would violate it already on a short segment inside the ball. Short segments toward an affine basis also preserve affine dimension and thus projection interior. This handles nonsmooth corners without a unique normal or contact.

The two line-coordinate motions are independent by their evaluations at distinct contact heights. This remains true when their transverse directions are equal or opposite. Tiny height separation and arbitrarily small apertures affect only local constants. Maximizing-normal continuity follows from compactness of the unit circle and continuity of the gap, not a differentiability assumption. Own increments have lower slope m_i = alpha_i/4; cross increments have absolute slope at most epsilon. The bounds hold throughout one suitably chosen local coordinate box.

At `paper.tex:131`, the common closed square and residual ball are justified explicitly. Endpoint brackets have opposite signs uniformly over the other root coordinate. Unique scalar roots exist on the entire stated domain. Root comparison gives the declared cross and residual Lipschitz constants. The coupled root map is a self-map and a contraction on the complete square; comparison of fixed points proves Lipschitz dependence on the open residual ball. The safe common bound is 3delta/4. The manuscript does not use the invalid mixed-constant 5delta/8 bound; the package contains a rational countercontrol against it.

At `paper.tex:159`, the cap quantifiers are correctly ordered. Nearby tangents of the original body need not hit a cap chosen at the base line. The proof first fixes a rational cap pair P and then covers T_P, so every selected neighborhood is applied to tangents of the same caps. Second countability gives a countable subcover of that subspace, and the outer union over rational cap pairs is countable. Every original retained tangent belongs to some T_P by localization. This is an actual covering argument and does not transfer the central difficulty to an unsupported local-contact-continuity claim.

### Density, first variation, determinant, and swept images

At `paper.tex:166`, tangency to a compact convex set is closed: compact contacts and unit supporting normals admit subsequential limits, and line incidence and supporting inequalities persist. The retained parameter subset is Borel, including the plane/hull-line exclusions. Density and differentiability are used almost everywhere in that selected subset; no open tritangent domain or injectivity is assumed.

Density one gives selected sequences in every prescribed first-order direction. A hole of radius proportional to the displacement would remove a fixed fraction of a comparable ball centered at the density point. This defeats the objection that the selected set may have no ordinary tangent curve. Conversely, the unit-circle family of ball tangents is a valid countercontrol showing why density cannot be omitted.

At `paper.tex:179`, the rank lemma is valid for all dimensions. In dimension three, surjective transverse first variation directs a nearby selected line into an interpolated interior ball whose radius scales linearly with the displacement; the error is smaller order. In dimension two, the nonzero planar denominator comes from the retained line's transversality. The intersection-height derivative gives the same convex interpolation center. A supporting plane at relative interior must be the affine hull, which cannot contain that transverse line. In dimension one, excluding the identical hull line makes the transverse direction nonzero. The incidence denominator stays away from zero; its interval parameter is first order, and the perpendicular error is second order. In dimension zero, fixed incidence gives zero transverse derivative directly. Contacts need not be unique: any actual selected contact from each disjoint set suffices.

The three heights are distinct by disjointness. A determinant of a 2-by-2 affine matrix pencil has degree at most two, so three distinct roots annihilate it identically. The swept map has this same determinant as its three-dimensional Jacobian at every finite height of every good parameter. On bounded parameter and height patches it is Lipschitz. At `paper.tex:224`, the bad parameter set times a bounded height interval is three-dimensionally null; those exceptional fibers therefore cause no missing swept volume. Applying the measurable-subset area formula to each Borel patch and exhausting by countably many patches yields outer nullness. Noninjective or collapsing charts are harmless because multiplicity is allowed.

### Dimensional coverage and controls

At `paper.tex:229`, the case split is exhaustive. Two dimensions-at-least-two sets use the cap chart lemma. A point supplies direction charts. Otherwise two nondegenerate compact intervals supply two contact parameters. Disjoint compactness makes their difference nonzero; one ambient coordinate remains nonzero on a sufficiently small open extension of the parameter rectangle, including endpoint pairs. The resulting line map is smooth and Lipschitz on a smaller bounded rectangle. The actual compact tritangent subset is selected afterward, so extra lines do not create a hidden hypothesis.

Discarded lines contained in planar hulls, and lines identical to interval hulls, contribute only finitely many null planes or lines. Countably many compact-cap reductions preserve nullness in the arbitrary-set case.

The positive-volume two-contact rectangles, repeated singleton contacts, zero-density circle, intersection-versus-support distinction, moving-cap misses, cap-boundary normals, and nonclosed strip controls are mathematically appropriate boundary tests. Finite checks of them do not certify the universal proof. The universal proof survives independently of the verifier.

## Personally checked analytical inputs and external erratum

The [Stanford-host Simon notes](https://math.stanford.edu/~lms/ntu-gmt-text.pdf) used here are the NTU 2018 body, 1,234,390 bytes, SHA256 `ba7fd4a53bf0f1d0ac54aec50bb72c4bba196b8e784d65cd0a7fd85131a3bf03`, with PDF creation/modification metadata 7 March 2018. I personally checked the complete selected statements, plus the relevant proofs:

- Ch. 1, Cor. 3.10, printed p. 18 / PDF p. 13: density one almost everywhere in a Lebesgue-measurable subset.
- Ch. 2, Thm. 1.4, printed pp. 44–46 / PDF pp. 26–27: almost-everywhere differentiability for a Lipschitz scalar function. Local open-domain and vector versions follow by local extension/patching and finitely many coordinates; the notes' extension theorem is on printed p. 44.
- Ch. 2, Thm. 3.3 and Remark 3.4, printed pp. 57–58 / PDF pp. 32–33: locally Lipschitz maps on open domains, arbitrary measurable selected subsets, and multiplicity without injectivity. For equal dimensions the Gram Jacobian is the absolute determinant and multiplicity is at least one on the image, giving the manuscript's outer-image inequality.

**Informational source issue E1, resolved analytically here; no manuscript repair required.** In the proof of Thm. 3.3, Case (ii), printed p. 60 / PDF p. 34, the unnumbered display immediately after (10) claims an augmented-Jacobian error bounded by C epsilon squared. It is at line 2033 of my `pdftotext -layout` extraction, whose bytes are bound in `SOURCE_OPERATION_AUDIT.json`. This stronger estimate is false: for n = 1 and f constant, the augmented map F_epsilon(x) = (f(x), epsilon x) has J_F = epsilon, so J_F / epsilon squared = 1/epsilon is unbounded.

Here is a checkable corrected version of the actual proof mechanism. Work on a patch where f is L-Lipschitz and the selected measurable set A has finite n-dimensional Lebesgue measure. At a differentiability point in A with J_f = 0, let lambda_1,...,lambda_n be the eigenvalues of Df^T Df. They satisfy 0 <= lambda_j <= L squared, and one is zero. Therefore, for 0 < epsilon <= 1,

    J_Fepsilon = sqrt(product_j(lambda_j + epsilon squared))
               <= epsilon (L squared + epsilon squared)^((n-1)/2)
               <= epsilon (L squared + 1)^((n-1)/2).

F_epsilon is injective and has full-rank derivative at each such point, so the already proved full-rank Case (i) gives

    H^n(F_epsilon(A)) = integral_A J_Fepsilon dL^n.

The projection from R^m times R^n to the first R^m coordinates is 1-Lipschitz and sends F_epsilon(A) to f(A). Consequently

    H^{n,*}(f(A)) <= epsilon (L squared + 1)^((n-1)/2) L^n(A) -> 0.

For the present n = m = 3 application the bound is simply epsilon (L squared + 1). Countable locally Lipschitz bounded patches supply finite measure and finite L. The nondifferentiability set has null image by the Lipschitz null-set estimate, as in Case (iii). This repair uses no conclusion of zero-Jacobian Case (ii) circularly.

Nearby formula (9) in that same external proof prints an integration-domain label R^(m+n) instead of A, and the subsequent projection description swaps the coordinate dimensions. The dimensionally consistent statement above integrates over A subset R^n and projects R^m times R^n to R^m. These source notation slips and the rate estimate do not change the correct Thm. 3.3 statement. The manuscript invokes that theorem correctly and never asserts the false rate. No retraction of its analytical dependency or global manuscript change follows.

I did not personally read the complete original Federer or revised Evans–Gariepy books. They are supplemental references, and the necessary hypotheses have been checked in the cited Simon statements and the corrected zero-Jacobian mechanism above.

## Bounded priority examination

The complete user-supplied published [Cheong–Goaoc–Holmsen article](https://doi.org/10.1007/s00454-023-00573-2), DCG 72 (2024), 674–703, is 596,169 bytes, SHA256 `478c879b6fea91b1aa17b0ea90172c10e01432b90e11c0873881f864151fdafc`. I personally read all thirty text pages, all presented proofs and remarks, and the bibliography. I additionally inspected the rendered topology proof and compact-set remarks on printed pp. 691–693. I do not claim all thirty rendered pages were visually inspected or all fifty-nine cited works were read.

| Presented result or mechanism | Exact scope and adapter assessment |
|---|---|
| Thm. 1.1; Sect. 2, pp. 681–684 | Finite weak-net counterexamples for meeting lines and convex sets, including the k-flat lifting. No supporting tangency or entire spatial null locus is proved. Hyperbolic-paraboloid examples do not supply the missing arbitrary-family differential restriction. |
| Prop. 1.2; Sect. 3, pp. 684–689 | Finite blue/red-line convex selectors and stable incidence obstructions. The conclusion is finite intersection, not measure of a union of supporting tangent lines. |
| Thm. 1.3; Sect. 4, pp. 689–693 | Acyclic connected components of meeting-transversal spaces for pairwise disjoint open convex sets. The proof uses an open line-space domain, contractible fixed-direction fibers, and the Vietoris–Begle mechanism. Acyclicity or contractibility does not bound dimension or swept volume. Open sets cannot meet a supporting plane at all. |
| Compact-set remarks, p. 693 | Four compact convex sets can encode arbitrary compact parameter subsets; inflating sets or taking interiors drastically changes the meeting-transversal family. Thus a direct openness-to-compactness limit preserving the needed family is not available. No spatial measure statement or three-contact density argument is hidden in this construction. |
| Higher k-flat universality, p. 693 | The stated range is 3 <= k <= d-3 and concerns homotopy realization, not lines in R3 or supporting-tangent spatial measure. |
| Thms. 1.4, 1.5, 6.2; Sects. 5–6, pp. 694–701 | Finite colorful/matroid intersection and order-type conditions imply existence of particular flat/hyperplane transversals. They do not control the spatial union of all tangent lines; colorful intersection assumptions also do not supply the present disjoint-set hypothesis. |

I found no direct resolution or sufficient implication of the present universal nullness statement in that complete body. This is a proof-mechanism comparison, not inference merely from differing titles or abstracts.

I personally read and visually inspected the complete printed p. 11 of the [author-host manuscript preserved in the 1 April 2011 archive capture](https://web.archive.org/web/20110401122240id_/http://www.loria.fr/~goaoc/papers/TopVE.pdf), using the existing private body, 464,566 bytes, SHA256 `4e380b3007469c0173500144cb560220c01d542ba1f0c6a5b7921acdb47a1c89`. It explicitly asks compact three-set nullness and explains that nowhere density is insufficient. I do not certify its date of publication or byte identity with the manuscript cited in September 2008. The final preprint makes exactly those qualifications.

After my own reconstruction and body comparisons, I checked the current coordinating bounded-priority record and its named source/process evidence for consistency. All fourteen listed comparison/evidence records were present at their stated sizes and hashes; the two separately tasked read records name the correct thirty-page input and explicitly distinguish text reading from limited visual inspection. `PROVENANCE_RECORD_CHECK.json` records this check. Such records corroborate the reported process; they do not prove a person's reading state or replace my own examination.

The preserved historical candidate is dated 30 September 2026 and retains its old priority/access header. README, PROVENANCE, and SOURCE_BINDING explicitly supersede that historical hold with the dated current bounded assessment without changing the historical source bytes. This is not a contradiction in the operative final status. The manuscript, README, and metadata avoid first-proof, exhaustive worldwide coverage, and historical-evidence-based current-openness assertions. My bounded primary review does not refute those qualified statements. I did not independently repeat every broader prior search or certify global literature completeness.

## Verifier, archive, and production manifest

I inspected the complete standard-library verifier and builder. Polynomial identities use integer coefficient dictionaries, not integer samples. Rational controls use exact Fraction arithmetic. Checks are explicit runtime branches and optimized execution is rejected. The source binding is checked against the exact historical candidate. The verifier does not claim that its finite computations establish arbitrary convex geometry or measure theory.

The independent reproduced verifier passed 2,826 controls under Python 3.14.6, optimization 0. Thirteen actual outer runs were captured. In addition to successful untouched-input builds and positive verification:

| Injection/control | Actual result |
|---|---|
| Optimized verifier | Nonzero rejection before controls |
| Intentional false control | Nonzero rejection with complete failure stream |
| Reversed formal determinant sign | Nonzero failure of formal coefficient identity |
| Modified manuscript with stale receipt | Builder rejects stale `paper.tex` hash |
| Modified candidate | Verifier rejects reviewed-source binding |
| Modified verifier with stale receipt | Builder rejects stale `verify.py` hash |
| Modified PDF | Builder rejects PDF binding |
| Modified PDF source binding | Builder rejects manuscript/PDF binding |
| Copied portable capture controller, positive mode | Actual child passes; PIDs, argv, streams and input hashes retained |
| Copied portable capture controller, negative mode | Controller succeeds because the actual verifier child rejects as intended; the child failure stream is retained |

Failures were retained as observed, without rewriting them into passes. The portable-controller negative case correctly distinguishes the wrapper's zero exit from the child's nonzero exit.

Both independent same-input builds produced the exact 182,613-byte pinned archive, SHA256 `1fd934e9f8b011307137500039192c93c34f505c472a19fb47ba03af3ab5b9c5`. I preserved the original timestamped verification receipt for these builds; I did not claim byte identity after rerunning verification and changing an input. The archive has fourteen payload members plus its self-excluded manifest, exactly the expected lexicographic unique domain. Every member's bytes, hash, size, UNIX regular-file mode 0100644, 3 October 2026 midnight timestamp, and ZIP_STORED mode were checked. No extra member, traversal path, historical draft, private capture, third-party PDF, or foreign extracted body is present. Its standalone source, README instructions, licenses, mathematical input, metadata, and bindings are portable as described.

The actual intended production manifest's metadata equals `zenodo_metadata.json['metadata']` exactly, and its files are exactly `../preprint_v1/common_tangent_nullness.pdf` and `../preprint_v1/common_tangents_null_locus_v1.zip`. Both resolve to the fixed pinned files. The planned upload manifest agrees on names, hashes, sizes, author, and status. The metadata does not assert a completed deposit, assigned DOI, external peer review, journal acceptance, or merge. Its CC BY 4.0 prose/manuscript grant and MIT code exception agree with LICENSE.md; third-party works are not relicensed or redistributed.

The local PDF export receipt exists at the size/hash named by PDF_BINDING. Source and PDF pins agree. I observed its reported native compilation/export provenance but did not independently run a compiler or install one. My source/PDF agreement and actual render checks are separate from that historical compiler report.

## Every submitted PDF page personally inspected

I personally inspected all eight pages rendered from the exact pinned PDF at 100 dpi. A second genuine captured render reproduced those same PNG bytes. Each page was inspected individually, not inferred from a hash or a subset of pages.

| Page | Personally checked content and layout |
|---:|---|
| 1 | Title, sole author/ORCID, date/unrefereed label, abstract, exact theorem and tangency convention; readable and within margins. |
| 2 | Qualified priority continuation, analytical inequality/citations, rational-cap reduction and support coordinates; equations legible. |
| 3 | Projection/tangency equivalence, chart lemma, hemisphere and cap arguments, two motions; no clipped text. |
| 4 | Own/cross bounds, full root brackets, contraction constants and correct 3/4 bound; displays fit and continuation is coherent. |
| 5 | Fixed-cap-first countability, compact closedness, Borel selection, density sequence, full/planar rank arguments; no overlap. |
| 6 | Planar height formula, interval/point cases, three-root polynomial, swept derivative, exceptional fibers and proposition; matrix and determinants readable. |
| 7 | Exhaustive dimensional cases and endpoint rectangles, completion, boundary controls and nonclosed example; no overflow. |
| 8 | Reproducibility caveat, extensive AI/unrefereed disclosure, complete references and hyperlinks; no broken glyphs or clipped references. |

The PDF is eight Letter pages, unencrypted, with no JavaScript or forms. Its displayed source equations and conclusions agree with `paper.tex`. I found no unresolved visual/readability defect or scientific/PDF discrepancy.

## Final disposition and limits

No repaired-by-me package issue, pending package issue, or new issue requiring global changes was found. The critical potential defects—hidden closure assumptions, cap-boundary normals, root-domain quantifiers, common constants, fixed-cap countability, density at selected parameters, all affine dimensions, exceptional fibers, and source/PDF or metadata drift—were tested and resolved by the fixed package's own correct arguments and evidence. External source issue E1 is resolved for this application by the explicit corrected singular-value proof above.

The exact remaining limitations are ordinary, explicit ones: this is an unrefereed internally AI-examined result; the bounded priority review does not establish earliest proof or exhaustive current literature status; Conjecture 3 is not established; and no publication or native acceptance action is authorized by this report. These are not named unresolved mathematical/source-access gaps. Completion estimate for this assigned fresh review: 100%; additional research-attempt/novelty credit: 0.
