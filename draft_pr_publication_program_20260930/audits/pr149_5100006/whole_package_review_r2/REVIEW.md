# Independent whole-package adversarial review R2 — PR149 / 5100006

Review opened: 2026-10-11T22:40:27Z. Independent analytic/source conclusion formed before consulting any R1 artifact. Review completed: 2026-10-11T22:51:01.019556+00:00.

**Verdict: PASS for the frozen, expressly scoped, AI-assisted unrefereed publication package. No substantive mathematical, source-attribution, reproducibility, packaging or readiness defect was found. No repair is required.** This is an independent machine-assisted adversarial audit, not conventional human peer review, novelty certification, or a publication/merge receipt.

The verified contribution is the complete least-period classification of the ordinary original-vertex-to-fixed-focus product under the strict stated hypotheses. The review does not promote an unrestricted listed-return-length statement. It does not certify exclusive priority or claim a new general method.

## Candidate identity and scope

The reviewed folder is `publication_package_v1`, pinned by `PUBLICATION_CANDIDATE_INVENTORY.json` (SHA-256 `067d3fb55d36a9588fcdee6e971e18c215464b5ed0a80686142d051143467298`). All 16 file sizes and digests matched at opening and again after the review. The PDF digest is `280e7e703c50615def59d2c45d22386fde015d8bfce6705a7cc878d19aef0e1e`; the support ZIP digest is `23f032f0522b22f293e74eb4df9a97706f6414a385bd1d39b173c979df36ee3a`.

All 13 ZIP members match the current corresponding files byte for byte, in the inventory's declared order. The archive has no traversal or absolute-path member. All 13 entries of SHA256SUMS match, including the separately supplied PDF. The ZIP appropriately omits the PDF and outer deposit manifest, as README explains. The deposit manifest's metadata is structurally identical to metadata.json and lists exactly the present PDF and support ZIP.

No publication, original intake, native preparation, Git, remote, Zenodo or Sheets file was changed by this reviewer. All writes are under `whole_package_review_r2`. No external communication was prepared or initiated.

## Independent analytic mechanism and adversarial attacks

The proof audit below was conducted directly from the standalone manuscript and primary sources, before looking at the archived R1 package differences. Finite program success was not used to justify a universal theorem.

**Geometry and parameter coverage** — manuscript lines 35–48 and 75–135.

From B>0 and A²−B²=c², k=c/A is strictly between zero and one. The real function cn(v,k) decreases from one to zero on (0,K), so B/b in (0,1) determines a unique v. The advertised major-axis formula follows algebraically:
A² dn²(v)/cn²(v)=c²+B²/cn²(v)=c²+b²=a².
This also distinguishes modulus k from software's parameter m=k².

The tangent equation at Q(U) is correct. Substitution of P(U±v) using Jacobi addition cancels the mixed terms and gives numerator dn²(v)sn²(U)+cn²(U)=1−k²sn²(v)sn²(U), exactly the denominator. The two endpoints are distinct because 0<2v<2K. Q is strictly inside the outer ellipse, so it lies between the two boundary intersections of its tangent line; this is an actual segment tangent to the caustic.

The homogeneous direction quadratic dᵀMd=0 is the line/conic tangency discriminant. Its determinant is negative at every outer-boundary point. The displayed nuᵀMt identity is correct after imposing x²/a²+y²/b²=1 and confocality. In the orthogonal normal/tangent basis the mixed coefficient vanishes. The two real line directions, and their selected inward rays, are therefore exchanged by reflection across the normal. This is the physical billiard reflection law, including at the axes; the normal is never zero. There are exactly two caustic tangents from every boundary point, and the constructions exhaust them.

P(u)=(-a sn(u),b cn(u)) is one-to-one modulo its real period 4K because the real Jacobi amplitude is strictly increasing by 2π there. Thus the forward and reverse billiard maps are ±2v, and the primitive closure condition is exactly δ/(4K)=tau/n, gcd(tau,n)=1, 0<tau<n/2. No unsupported selection of only simple polygons is made: every allowed coprime star winding is included. Neither one- nor two-bounce primitive cycles occur in this strict elliptical-caustic setting.

**Actual ordinary distances** — manuscript lines 126–135.

Expansion gives |P(u)−F±|²=(a±c sn(u))². Since a>c and |sn(u)|≤1 on the real axis, each factor is at least a−c>0. No signed-distance interpretation or ambiguous complex square root is introduced. The meromorphic function used in the proof equals the actual positive Euclidean factor on every physical phase.

**Complete divisor on the correct torus** — manuscript lines 137–186.

The torus C/(4K Z+2iK' Z) is the full sn torus. It is not the cn period lattice, and the manuscript explicitly uses only the real 4K vertex period for closure. Directly checked DLMF Tables 22.4.1 and 22.4.3 give simple poles at p=iK' and p+2K, and
sn(p+K±v)=dn(v)/(k cn(v))=a/c, sn(u+2K)=−sn(u).
Hence g+=a+c sn has zeros p−K±v. They are distinct and nonpolar in the open parameter interval. Its coefficient c≠0 retains both simple poles. Equal total zero/pole degree then proves that the two located zeros are simple and exhaustive; the proof is not merely a check of some candidate zeros.

For H=<δ>, order n, the real offsets modulo 4K give H={j/n}. The two zero translates differ by δ, so the n-factor product has one zero coset, with multiplicity two at all its n points. Its representative is z=−1/4+tau/(2n), relative to p. The pole cosets are H and 1/2+H, with their full multiplicities retained.

When n is odd, the pole cosets are disjoint. Both nz=(−n+2tau)/4 and n(z−1/2)=(−3n+2tau)/4 have odd numerator and cannot be integral: no zero/pole intersection exists, and 2n simple poles remain. When n is even, tau is odd, 1/2∈H, and there are n double poles. Cancellation is complete exactly when nz is integral, namely n≡2 mod4. In the zero-mod-four class, the double-zero coset is disjoint from the double-pole coset. These conclusions apply to every allowed tau, not a finite sample.

**Constancy, converse, both foci and repeated traversals** — manuscript lines 184–208.

Complete cancellation gives a holomorphic function on a compact connected torus and therefore a constant. Positivity on the real line makes that constant nonzero. In all other primitive parity classes, retained poles exclude constancy on the real physical family by the identity theorem for meromorphic continuation. Thus the converse is rigorous; complex nonconstancy was not substituted for an unproved physical statement.

The equality g−(u)=g+(u+2K) transfers the classification to the other focus. For even n, 2K∈H makes the two products identical at each phase, even when they are nonconstant. Reversing orientation enumerates the same H orbit and leaves the product unchanged. The phase-zero antipodal evaluation is correct for every admissible odd tau when n=2m≡2 mod4.

An r-fold traversal produces exactly the positive primitive product's rth power. Injectivity of x↦x^r for positive x proves preservation of constancy in both directions. This covers noncoprime listed lengths without falsely making them primitive. A circle is separately handled by radius a, giving a^N for every listed length.

**Exact physical return-length counterexample** — manuscript lines 210–237.

The specified triangle has a²=15, b²=7, c²=8, A²=135/16, B²=7/16 and strict confocal separation 105/16. All three vertices satisfy the boundary equation. The vertical and two sloping side equations and their conic-support tangencies are exact. The off-axis inward unit rays have the stated unit lengths and sum along the inward normal; axial reflection and the other vertex follow by symmetry. Three distinct vertices and a three-event return give least period three. Central reflection is another physical phase of the same caustic family.

Its two primitive fixed-focus products simplify exactly to 15√15/2±3√8. Squaring them gives positive difference 180√30 for the six-event doubled traversals. This directly falsifies the unrestricted return-length version with N=6. The exact four-period control independently has products 4 and 64/25 in one strict confocal family. No contact, perpendicular or outer-polygon product is substituted in either argument.

**Boundary and limiting attacks.**

k=0/c=0 (circle), k=1/B=0 (degenerate caustic), v=0 (coalescing pair), and v=K (axis formulas singular for B>0) are outside the analytic proof's open hypotheses. The circle assertion has its own direct proof. Approaching those limits can make nonconstant variation arbitrarily small; no uniform numerical lower bound is asserted. Hyperbolic caustics, separatrices, degenerate two-bounce orbits and aperiodic families are not silently included. An irrational rotation has no n, and a noncoprime rational listed cycle is handled through its least period. I found no contradictory edge case inside the stated hypotheses.

## Primary-source and priority audit

The exact original claim was verified against both the 2020 v11 preprint and the 2021 version of record, including the actual Table 2 image. The latter's §3.1, p.344 defines d_j,i=|P_i−f_j|, and p.345 lists k114=∏d_1,i, N≡2 mod4, discovery 4/20 and proof “?”. The source introduction is a confocal ellipse pair. Its row does not explicitly settle the least-period/repetition convention. The original source/database statement in the immutable intake is the same target. The package appropriately proves the primitive interpretation and classifies, rather than affirms, the broader repeated-list interpretation.

The arXiv primary record independently confirms first submission 26 April 2020 and v11 revision 29 October 2020. The inspected published PDFs confirm the cited journal facts and online dates.

| Inspected primary statement | Actual content and effect on this target |
| --- | --- |
| Stachel, published Theorem 4.3 and (4.9), p.1614 | Supplies exactly the caustic-modulus canonical parameter, axes and step used here. It is classical machinery requiring the additional focal divisor deduction. The adjacent printed dn half-period sign error is not used by this manuscript. |
| Stachel, Theorem 5.6, p.1621 | Products of vertex-to-caustic-contact lengths; full products for even periods and half-products for zero-mod-four periods. This is k117 and has different factors. |
| Bialy–Tabachnikov, Lemma 4.2/Theorem 4.3, pp.1349–1353 | Focus-to-side perpendicular and center-to-side products. The published center-foot/focus-factor notation mismatch is real and the package's interpretation is supported by the lemma and proof. It does not state original vertex-to-focus constancy. |
| Akopyan–Schwartz–Tabachnikov, version-of-record Theorems 4.1 and 5.1, pp.1319–1322 | Angular invariants proved through complexification, Liouville and pole cancellation; the proof explicitly credits Schwartz. |
| Schwartz, author manuscript dated 3 February 2014, pp.5,12–14 | Monodromy invariants as meromorphic functions on a complex Poncelet torus; removal of poles and compact-torus constancy. No target identification is supplied. |
| Chavez-Caliz, pp.97–98 and Theorem 6, pp.104–105 | Cyclic/dihedral meromorphic functions on the elliptic flag curve; area-product pole cancellation. A method precedent and a distinct invariant. |
| Roitman–Garcia–Reznik, Theorems 1–2 and Corollary 1 | Angular sum and pedal/focus-inversion perimeters via Jacobi functions and Liouville. Distinct quantities. |
| Ferudun, current canonical k115 source/body, Theorem 1 and scope | Original foci to intersections of consecutive boundary tangents, least period divisible by four. Outer vertices, not the target's billiard vertices. Parametrization/divisor tools overlap and are properly credited. |
| Stachel 2021 geometry/grid paper and 2022 diagonal manuscript; King 1994; Tabachnikov 2005; Levi–Tabachnikov 2005 preprint | Symmetry, grids, diagonals and canonical-coordinate/rotation background. King’s PDF text encoding required independent rendering/OCR; its actual conjugacy lemma was inspected. No explicit target theorem was found in these inspected statements and target-relevant full-text passages. |
| Supplementary Garcia–Reznik book/self-intersection/inversion/spatial-integral texts | Relevant leads concern inverted polygons, area products, angle products or averaging. They supplied no explicit ordinary focal-vertex classification. |

The package's exact distinction at caustic axes (2,1), outer axes (√6,√3) was independently checked: rectangle/diamond ordinary focal products are 16 and 18; both contact products are 4; both focal-perpendicular products are 1. Equal known distinct invariants alone cannot be mistaken for the target.

[DLMF §22.4](https://dlmf.nist.gov/22.4), [§22.6](https://dlmf.nist.gov/22.6) and [§22.8](https://dlmf.nist.gov/22.8) were directly inspected for the period, shift, square and addition inputs. They match the formulas used, with modulus k throughout.

The strongest inspected published result furnishing the proof inputs is Stachel's canonical parametrization, combined with classical elliptic-function theory. I found no inspected published theorem already stating exactly this original-vertex target and all-period iff criterion. Established general tools still require the target-specific factor, complete divisor and subgroup arithmetic. The manuscript's limited claim of a short target-specific application is supported. This does not prove that an uninspected theorem cannot specialize to it.

The DG2023 coverage gap is appropriately explicit at manuscript lines 253–259, priority-note lines 49–55 and metadata description. The institutional primary record actually says “No Fulltext”; its abstract concerns inertia/confocal pencils and relationships with billiards. Direct publisher/repository requests in this review did not yield a full text. §§3.1 and 5.2 therefore remain genuinely uninspected and may contain relevant facts or citations. Accessible scope is not clearance, and this gap is not converted into an absence finding. The original Jacobi text and all unindexed/later specializations were not exhaustively inspected. These are precise priority-coverage limits, not gaps in the manuscript's mathematical deduction.

After forming my independent analytic/source verdict, I inspected the separate fresh recent-release catalog evidence. I independently reparsed the saved primary Atom and sitemap (202 entries and 202 paper landing pages; sitemap also has 202 PDF URLs and its root), the 71 unique release-window DOI records/35 titles, and the 43 relevant DOI records/21 titles. Every release-window title is in the publisher feed. The positive control returns both actual k115 concept/version nodes, whose IsVersionOf/HasVersion chain is as reported. The only focal-distance-product title advertises the already inspected outer-vertex k115 result; its PDF digest matches fresh publisher metadata. This is bounded additional evidence. Direct Zenodo access errors and discarded zero-hit/default-field queries carry no absence inference. I did not inspect every theorem body in the catalog and do not certify global priority.

## Every support member and outer file checked

| File/member | Audit |
| --- | --- |
| LICENSE.md | CC BY 4.0 applies to the author's materials/effort scripts; external sources retain rights; AI assistance is not called human review. |
| README.md | Exact scope, circle/exclusions, archive/PDF split, standard-library instructions, output writes, optimization behavior and evidential limits are accurate. |
| REPRODUCTION_NOTES.md | Counts, residuals, controls and floating-point limits match actual outputs; manuscript supplies the universal proof. |
| SOURCES_AND_PRIORITY.md | Observation credit, exact sources, distinct invariants, bounded priority and DG2023 gaps are supported as above. |
| focal_product_period_criterion.tex | Standalone analytic proof and attribution audited line by line. |
| metadata.json | Title, author/ORCID, date, scope, target resolution, limits, AI/unrefereed disclosure and related identifiers consistent with paper. |
| verification/verify_exact.py | Entire source read; explicit exceptions keep 21,508 finite exact checks active under -O; no imports outside stdlib, writes or network. |
| verification/check_divisor.py | Entire source read; rational half-period controls and separately implemented theta diagnostics; explicit -O refusal prevents removed assertions. |
| verification/check_classification.py | Entire source read; full sn-torus inventories for all sampled parities and both foci; imports only the bundled diagnostic module; repeated products and below-resolution label correct. |
| verification/exact_results.json | Actual stdout matches the packaged file byte for byte under normal and optimized Python. |
| verification/independent_results.json | Entire structure/output inspected; fresh diagnostic output byte-matches. |
| verification/classification_results.json | Entire structure/output inspected; fresh diagnostic output byte-matches, including unresolved-at-float-resolution cases. |
| SHA256SUMS.txt | Every declared entry valid; PDF entry intentionally refers to separate PDF. |
| focal_product_period_criterion.pdf (outer) | Five pages rendered and individually visually inspected; no clipping, overlap, broken equations, unresolved references or unreadable glyphs. |
| focal_product_support.zip (outer) | Exactly the declared 13 safe members, all current-file bytes. |
| zenodo-deposit.json (outer) | Metadata identical to metadata.json; both listed deposit paths exist. No DOI/publication-success invention. |

## Reproduction and independent controls

Fresh extraction: `whole_package_review_r2/scratch/unpacked_support`. Python 3.14.6, no external numerical dependencies for package scripts. Normal execution of all three portable scripts succeeded. verify_exact.py also succeeds under -O with byte-identical JSON; the two diagnostic scripts fail before computations/output writes with the documented explicit RuntimeError under -O.

The core counts are exactly 1,053 odd, 255 two-mod-four and 263 zero-mod-four primitive pairs over n=3..101, both foci and r=2,3,4; 21,508 explicit arithmetic checks. The supplementary divisor script reports 1,053 positive odd-half-period cases, 1,003 star cases, 1,036 even-half-period controls and 30 theta cases. The classification script reports 33 numerical cases. Maximum normalized norm disagreement is 1.2212453271354237e−15 and zero residual 2.29150134808483e−13. These are observed errors, not certified bounds.

For k=0.1 the n=9,tau=4 and n=12,tau=5 examples for both foci have variations labeled below float resolution. That does not override their analytic nonconstancy. The scripts do not assert a general numerical variation lower bound.

A separate reviewer-written `independent_geometry_checks.py` imports no package verifier. With scratch-installed mpmath 1.3.0 and 100 decimal digits, it checks 150 primitive (n,tau,k) families for n=3..18 and k=0.01,0.7,0.999999: axes/confocality, contact inside actual chord, both tangent choices, normalized reflected rays, actual Euclidean versus positive Jacobi distances, closure, reversed orbit products, even-period focal equality and complex zero locations/nonzero derivatives. All checks passed. Maximum observed geometric/zero residual was below 2e−96. These diagnostics remain explicitly unvalidated and are not the basis of the universal proof.

Tectonic compiled the extracted standalone source successfully. Its PDF's extracted text matches the supplied PDF byte for byte, and all five independently rendered PNG pages also match the supplied PDF's rendered PNG pages byte for byte. The generated PDFs have different binary digests. All five supplied PDF pages were inspected directly.

## Repaired references and native consistency addendum

Only after my independent verdict was formed, I compared the archived R1 support ZIP's affected members to current files. I did not read R1 REVIEW.md or RESULT.json. The only script/output changes are the evidence/interpretation strings that now refer to the bundled manuscript and separate PDF instead of unbundled REVIEW.md/EXTENSION_REVIEW.md. The two output JSONs have identical computation data after removing those strings. REPRODUCTION_NOTES accurately records that redirection. The current scripts, outputs, ZIP and checksum/inventory members all carry the repair. There is no computation change or stale proof reference.

The later supplied native-preparation candidate contains 18 files and a valid 17-entry SHA256SUMS manifest. Active PROOF.md, README.md and SOURCE_RESOLUTION.md were inspected against the publication paper; their mathematical claims and scope are identical. Active verify.py is byte-identical to the package's exact checker; native verification.json equals package exact_results.json and actual native replay stdout byte for byte. PROOF.md digest is `5523c8a3831d1a9a91109da0c1beafbf642eb4435aedc649977f23f19b58fdef`; SHA256SUMS digest is `73e3289ddcb7409ebbbc48bcde489b62f6231e8de094a4ad1966a4ccef138376`.

Eleven retained historical files match their immutable original_submission counterparts byte for byte, checked without adopting their verdicts. The README explicitly distinguishes old 29,397/210 and 5,198 receipts from current 21,508 counts, maps their old proof hash to the unchanged original, and does not represent old reviews as acceptance of the strengthened theorem. The original proof hash is correctly `f70821b0d44e96f6be9427f906cecc5d1aff8bbd7ab09a71ddec9d75d31ef2d5`. No native file was modified.

## Readiness judgement and precise remaining limits

**No substantive issue and no required repair.** Exact claim, hypotheses, complete all-period proof, physical counterexample, source differentiation and current artifact provenance are consistent and checkable. The source-listed observation is rigorously resolved under the natural primitive interpretation within its strict confocal-elliptical setting; the broader repeated-return convention is precisely classified and partly refuted.

The package is ready for the authorized next publication/integration decision as an AI-assisted unrefereed research note with its existing bounded priority language. Remaining limits are DG2023 §§3.1/5.2, uninspected historical/unindexed specializations, uncertified novelty/exclusive priority, unvalidated numerical residuals, and lack of proof-assistant or conventional human referee verification. None is concealed or used as evidence of absence. There is no mathematical gap within the exact stated theorem.

Completion estimate: **100% of this assigned whole-package R2 audit**. No release, merge or external publication was performed by this review.

