# PR149 fresh independent whole-package review, round 1

Started: 2026-10-11 22:31:46 UTC. Completed: 2026-10-11T22:37:51.799040+00:00.

**Verdict: PASS. No substantive mathematical, scope, claim-positioning, or reproduction defect was found.** One non-substantive stale diagnostic-document reference is listed below with a concrete repair. This pass rests on an independent all-period proof audit, not finite numerical agreement. Estimated completion of the assigned whole-package audit: **100%**. Historical novelty remains uncertified.

The review did not read previous reviewers' verdicts. I developed the geometric and divisor audit directly from the candidate before reading its priority note. I then consulted actual primary sources and the specifically requested DG2023 access report. All writes were confined to `whole_package_review_r1`; no candidate edit, Git mutation, publication action, tracker write, or external outreach occurred.

## Candidate identity and package coverage

Package: `publication_package_v1` beside this folder. Pinned inventory: `PUBLICATION_CANDIDATE_INVENTORY.json`, SHA-256 `f00214e4e70edb15be9f8ab3c17972ecaa1b64bae4543911d0dcbdb53cf2ce5e`.

Every one of its 16 file entries matched the recorded byte count and SHA-256 on initial inspection and again at the final check. The aggregate digest is `da35c3329d3600d03ff895708106bbc9c1f6e832bba6fd038d44e7677d045c9a`, defined as SHA-256 of canonical JSON mapping each inventory file path to its digest (sorted keys, compact separators). The PDF digest is `280e7e703c50615def59d2c45d22386fde015d8bfce6705a7cc878d19aef0e1e`; the ZIP digest is `494de41875eaafd2e930805f9ec09b72efa4b6f48979afd7928992b2cb6cbe10`. See `digest_checks.json` for the full member inventory.

I reviewed the actual five-page PDF visually, all standalone TeX lines, all 13 support ZIP members, README, license, checksum manifest, sources/priority note, reproduction note, both metadata files, all three scripts, and all three recorded JSON outputs. The ZIP member list is exact and every member is byte-identical to its package counterpart. All 13 checksum-manifest entries match. The PDF is intentionally deposited separately, and the README correctly explains that its digest is included in the support manifest. The deposit's metadata object equals `metadata.json` exactly. Title, author, ORCID, scope, version/date, AI disclosure, unrefereed status, citation relations, and listed deposit files are consistent.

## Independent mathematical mechanism and adversarial checks

### Geometric coverage and ordinary-distance bridge

The assumptions at TeX lines 35–48 imply `0 < k = c/A < 1`. Real `cn` decreases from 1 to 0 on `(0,K)`, giving a unique `v` with `cn(v)=B/b`. The relation

`A^2 dn(v)^2/cn(v)^2 = c^2 + B^2/cn(v)^2 = c^2+b^2 = a^2`

proves the remaining axis relation without a new assumption. For the caustic tangent at `Q(U)=(-A sn U,B cn U)`, substitution of the Jacobi addition formulas cancels the terms odd in `v` and gives

`[dn(v)^2 sn(U)^2 + cn(U)^2]/[1-k^2 sn(U)^2 sn(v)^2]=1`.

The denominator is strictly positive on the real line. Both endpoints are on the outer ellipse, and the contact is strictly inside it, so this is the actual chord segment, not merely tangency of an extended line.

The null quadratic form in lines 101–114 comes from the tangent-line discriminant. Its determinant is negative because every boundary point is outside the strictly nested caustic. Direct expansion gives exactly the displayed `nu^T M t = xy c^2/(a^2 b^2) (1-x^2/a^2-y^2/b^2)`. Thus the orthogonal normal/tangent basis diagonalizes the indefinite form. Reflection across the normal swaps its two null direction lines, and preserves the inward half-plane, so the inward unit rays satisfy the physical elastic reflection law. This includes the axis vertices where `xy=0`; no division by `x` or `y` is used. Monotonic real amplitude gives a bijective traversal of the entire boundary modulo `4K`. The two caustic tangents at each point correspond to the steps `+2v` and `-2v`, covering both orientations. There is no missing star family.

The real vertex period, rather than any complex period of `cn`, gives `delta=4K tau/n` with `gcd(tau,n)=1` and `0<tau<n/2`. Reversing orientation negates the step and merely reorders the finite orbit. The case `tau>1` needs no separate analytic argument. The inequalities exclude least periods 1 and 2. The focal algebra gives the exact positive real distance `a +/- c sn(u)`, since `a>c` and `|sn(u)|<=1` on the real line. Squared-distance branch or sign ambiguities therefore do not contaminate the invariant.

### Complete complex divisor and iff classification

The torus `C/(4K Z+2iK' Z)` is the full `sn` torus, not a claimed common complex torus for the whole vertex map. The two simple poles of `g_+=a+c sn(u)` are `p=iK'` and `p+2K`; `c!=0` preserves their residues. DLMF shifts give `sn(p+K +/- v)=dn(v)/(k cn(v))=a/c`, hence the two zeros are `p-K +/- v`. Their separation is `2v` strictly between 0 and `2K`, and neither is polar. Since the total pole degree is two, these two distinct zeros exhaust the zero divisor and are simple. This rules out the potentially serious hidden-zero/multiplicity failure.

The subgroup `H=<delta>` has exactly `n` elements because a real multiple cannot acquire an imaginary lattice component and `gcd(tau,n)=1`. Orders of meromorphic factors add even at collisions. The two translated zero orbits coincide because their base points differ by one step, producing multiplicity two on one coset with normalized offset `z=-1/4+tau/(2n)`. The two pole cosets are `H` and `1/2+H`.

For odd `n` the pole cosets are disjoint. Both `nz=(-n+2tau)/4` and `n(z-1/2)=(-3n+2tau)/4` have odd numerators, so no zero/pole cancellation occurs. Exactly `2n` simple poles remain. For even `n`, coprimality makes `tau` odd and the pole cosets coincide, giving exactly `n` double poles. The zero coset matches precisely when `-n+2tau` is divisible by four, equivalent to `n=2 mod 4`. Cancellation is complete there; for `n=0 mod 4` the zero and pole cosets are disjoint. There is no partial or overlooked cancellation class.

A complete zero divisor makes the nonzero meromorphic product holomorphic on a compact connected torus and hence constant. Conversely, the product is holomorphic in a neighborhood of the real axis. Real constancy would make the analytic germ constant by the identity theorem, and then the global meromorphic function constant, contradicting its uncancelled poles. The argument therefore proves genuine phase nonconstancy, even when its amplitude is too small for floating-point diagnostics. It is not merely a test at complex points.

The minus-focus product is the same plus-focus product shifted by `2K`, so the classification is identical. When `n` is even, `2K` belongs to `H` and gives pointwise equality of the two focal products. Antipodal pairing validates the positive value in lines 198–203. Repetition produces the positive primitive product to power `r`; that power map is injective on positive reals and cannot turn a nonconstant product into a constant one. For a return length `N=2 mod 4`, its least period divides `N`, hence is odd or `2 mod 4`, and constancy is exactly the even case. Circular boundaries have focal distance `a` directly; no unjustified continuity passage from the noncircular divisor proof is used. Caustic collapse, coincidence with the boundary, and hyperbolic caustics are explicitly excluded, so the argument is never extended through a coalescing-zero or disappearing-residue boundary.

### Exact physical counterexamples

The triangle at TeX lines 211–235 is strictly nested and confocal: `15-7=135/16-7/16=8`. All three vertices lie on the outer ellipse. Its vertical side is at `x=-A`; the other sides are `x +/- ay=a` and satisfy the dual tangency equation `A^2+a^2 B^2=a^2`. The stated sloping ray has length one because `(15+1)/16=1`; its sum with the vertical unit ray is five times the inward normal. Reflection at the lower vertex follows by axial symmetry, and at the axis vertex the two unit rays sum horizontally inward. The three distinct vertices give least period three. Central reflection preserves the same confocal pair and hence gives another phase of the same family.

Expansion of `(a-c)(a+3c/4)^2` and `(a+c)(a-3c/4)^2` using `a^2=15,c^2=8` gives `15a/2 +/- 3c`. Squaring the products gives difference `90ac=180 sqrt(30)>0`. This is an exact physical six-event counterexample, rather than a numerical phase sample or a nonreflecting Poncelet polygon. The supplementary primitive-four control also checks an actual common ellipse/caustic family: diamond and rectangle products are 4 and `64/25`.

**Strongest verified theorem:** the entire stated iff classification for each focus under strict noncircular/nested/nondegenerate elliptical-caustic hypotheses, all admissible primitive windings and orientations, even-period equality, all repeated traversals, and the direct circular extension. **Mathematical remaining gap: none within this scope.**

## Primary-source and priority audit

The original journal source statements defining the factors and setting were checked, and the actual Table 2 page was viewed. Section 3.1, printed p.344, defines `d_{j,i}=|P_i-f_j|` and says every sum/product ranges over `i=1,...,N`. Table 2, printed p.345, records `k114` as that product, condition `N=2 mod 4`, experimental date `4/20`, and a question mark in the proof column. Its introduction, printed p.341, describes two confocal ellipses. The cached v11 preprint has the same target row. This is genuinely the recorded ordinary billiard-vertex/fixed-focus observation. The manuscript attributes the observation rather than claiming discovery, and treats the repetition ambiguity cautiously.

The actual Stachel 2022 PDF, printed p.1614, Theorem 4.3 and (4.9), was viewed. It supplies precisely the canonical vertex coordinates, the modulus equal to caustic eccentricity, the `2v` step, the coprime period/turning relation, and the axis formulas. The same paper's Theorem 5.6, printed p.1621, concerns the `l_i,r_i` vertex-to-caustic-contact products. It is a distinct invariant and does not state the target focal product or converse.

The actual Bialy–Tabachnikov version of record, Lemma 4.2 and Theorem 4.3, printed pp.1349–1353, was examined (p.1350 also visually). Lemma 4.2 is about the product of the two focal perpendicular distances to a side line. Theorem 4.3's printed center-foot notation is inconsistent with its proof for part (a), as the candidate priority note correctly explains. These are not ordinary distances to the billiard vertices. The explicit four-period distinction in SOURCES_AND_PRIORITY.md line 45 is correct: outer axes squared `(6,3)`, caustic axes squared `(4,1)` give focal products 18 and 16, but contact products 4 and focal-perpendicular products 1. Known products therefore do not automatically identify the target.

Schwartz's 3 February 2014 author manuscript has Theorem 1.2 about the monodromy invariants of related Poncelet polygons; its p.5 explains the complex-torus/pole-removal method. It does not establish arbitrary cyclic functions as invariant, and no identification of the focal product with a monodromy invariant was found. Akopyan–Schwartz–Tabachnikov's actual papers establish angular sums/products and area ratios, with complexification and pole cancellation (version-of-record Theorems 4.1 and 5.1; the preprint's Theorems 5–6). Chavez-Caliz's Theorem 6, printed pp.104–105, proves an area product by the same mechanism. Roitman–Garcia–Reznik's Theorems 1–2 and Corollary 1 establish angular sums, limiting-pedal perimeters and focus-inversion perimeter. These are valid method precedents, not an already stated focal-product period classification.

Ferudun's actual October 2026 source was inspected: Theorem 1 concerns products to the outer vertices formed by consecutive boundary tangent intersections, for least period divisible by four. Its factor and divisor calculation is related, but it does not prove `k114`. Its unrefereed status is correctly recorded.

NIST DLMF §§22.2, 22.4 and 22.8 were independently inspected online. Table 22.4.3 directly supplies the shifts used above and the full `sn` lattice, while 22.8.1–2 supply the addition formulas. I also inspected §22.9's listed cyclic identities as a nearby classical analytic lead; the listed identities are not the stated arbitrary-period focal factor classification. General classical norm/divisor theorems remain enough machinery to deduce the result, but making the focal choice, proving its physical identification, and computing the finite-orbit cosets is still the target-specific deduction. The existence of such machinery is not evidence of an already published exact target theorem.

Additional fresh bounded searches for `k114` and elliptic-billiard focal products yielded no explicit prior target proof. This is only a bounded search finding. I did not audit every historical Jacobi text, every specialization of general multiplication/norm theorems, or all later literature. The source question mark only establishes publication-time unproved status.

The requested DG2023 access report was inspected after the proof audit. It documents no legitimate public full text and specifically leaves §§3.1 and 5.2 uninspected. The accessible introduction advertises inertia/confocal-pencil constructions and billiard first-integral connections, which supplies no positive exact-target preemption. That limited inference does not clear its uninspected sections. The candidate consistently discloses this in TeX lines 253–259, SOURCES_AND_PRIORITY.md lines 49–55, metadata line 12, and deposit metadata line 13.

**Publication-positioning conclusion:** the candidate is sufficient to publish a valid, independently checkable resolution of the least-period interpretation of an originally unproved recorded problem, with the stated converse and repetition qualification. It is not sufficient to certify that the exact formulation is historically new or that no earlier proof exists. The candidate makes no such certification or new-method claim, so that epistemic gap is properly represented rather than a substantive defect. No positive primary-source evidence encountered establishes an exact earlier theorem with the same product and full classification.

## Fresh reproduction and artifact quality

The support ZIP was extracted into `scratch/unpacked_support`. Python **3.14.6**, standard library only, reproduced the normal exact output and its optimized run exactly as JSON. It completed **21,508** explicit checks: odd/2-mod-4/0-mod-4 primitive-pair counts **1,053/255/263**, both focal signs and repeat multiplicities 2,3,4. The theta diagnostics produced recorded `independent_results.json` and `classification_results.json` **byte for byte**. The first gives 30 theta samples, maximum norm disagreement `1.2212453271354237e-15`, maximum zero residual `2.29150134808483e-13`, and the four-period/doubled-three controls. The classification diagnostic gives 33 samples and explicitly reports below-resolution variation. Both diagnostic scripts reject optimized Python before removable assertions could vanish. See `replay_summary.json` and the scratch stdout/stderr files.

I inspected the algorithms, not just the pass strings. Exact cosets enumerate proof-input divisors, rather than independently discovering the Jacobi identities; this limit is stated. The theta implementation uses standard definitions via theta series and AGM for `K`, but uses ordinary complex/floating arithmetic and fixed truncation without rigorous error bounds. Its sample agreement is useful supplementary evidence only; the package does not claim more. The physical triangle and four-period controls are exact rational/quadratic-field computations. No all-period theorem is inferred from finite sampling in this review.

The standalone TeX compiled from the extracted archive using Tectonic without repairs or external source files. Its compiled PDF has five pages, the same size, and text extraction identical to the supplied PDF. All five supplied pages were rendered and visually inspected: equations, theorem, references, accents, links, page numbers, and line wraps are legible with no clipping, overlap, missing glyphs, or unresolved citations.

## Issue list and concrete repair

No substantive issue. One **P3 documentation/provenance nit**, nonblocking for mathematical validity:

- `publication_package_v1/verification/check_divisor.py:181` and generated `verification/independent_results.json:358` say that the proof is in `REVIEW.md`. `verification/check_classification.py:94` and generated `verification/classification_results.json:1002` point to `EXTENSION_REVIEW.md`. Neither review file is in the publication archive. Readers should be directed to the deposited manuscript, not internal review artifacts. Replace both source strings with a statement that the analytic all-period proof is in `focal_product_period_criterion.tex` and the separately deposited PDF, rerun diagnostics, and regenerate checksums, ZIP and inventory. README lines 54–59 already give the correct evidential relationship, so this does not create a missing proof or prevent reproduction.

Any repair changes the candidate identity and should receive the user's requested fresh independent whole-package review. The present verdict applies only to the pinned bytes identified above.
