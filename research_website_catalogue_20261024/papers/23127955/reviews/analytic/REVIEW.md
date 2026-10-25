# Independent analytic review — Zenodo 23127955

**Disposition: PASS for the stated mathematical theorem.** No substantive proof gap or counterexample was found after the complete manuscript/support reading, an independent reconstruction, primary-source interface checks, fresh exact controls, and published-package replay. This is an internal mathematical review, not external human peer review or an exhaustive novelty certification.

## Identity, coverage, independence

The reviewed work is Alec Kriebel, *The spatial locus of common tangents to three disjoint convex sets is null*, Zenodo 23127955, version 1.0, dated 3 October 2026, eight pages. The fresh public PDF SHA256 is `80b3fc3e8cb470a22a1226b960467de9e67dd8c3ccf054b42133d9ba0ce9d327`; the public ZIP SHA256 is `1fd934e9f8b011307137500039192c93c34f505c472a19fb47ba03af3ab5b9c5`. The actual TeX SHA256 is `2522ac0138de5e21067af8c16e6749b3a9d3cd01f12bdb929cca87cb6baeabb6`. Fresh metadata/public-asset receipt and exact per-file hashes are retained in `source_pins.json` and `reviewed_source_hashes.json`.

All eight actual PDF pages were read and visually inspected, together with the full TeX, all 263 lines of mathematical support `source/CANDIDATE.md`, and the complete verifier, capture controller, archive builder, and README. No mathematical supplement was omitted. The proof and fresh controls were completed before reading the submitted verification helpers; the preliminary conclusion is timestamped in `independent_preliminary_conclusion.json`. No sibling findings or dedicated historical review reports were read. Shared raw primary PDFs and acquisition receipts were used, without sharing mathematical conclusions.

Incidental opinion-bearing text encountered and not used as evidence: the initial queue-bound local PDF path contains `reproduction/false`; the candidate header refers to previous independent audits/repairs and pending gates; the README refers to previous review/status work. No adjacent historical material or dedicated opinion report was opened. The initial PDF hash matches the fresh Zenodo PDF exactly. Provenance/history prose was not needed for the mathematical audit.

## Exact claim and result

Theorem 1 (PDF p.1; TeX lines 28–40) applies to **any three pairwise disjoint convex subsets of Euclidean R³**. They may be empty, nonclosed, unbounded, lower dimensional, or nonsmooth. A tangent is a **complete affine line** that meets the set and lies in a supporting plane; support means containment of the set in a closed halfspace and actual contact with its boundary plane. Contacts/support planes need not be unique, and contact can be a segment. The conclusion is zero **Lebesgue outer measure** of the union of all common tangent lines, equivalently containment in a measurable null set.

The strongest verified claim is precisely this full theorem. It does not assert closedness of the locus, countable rectifiability, or containment in countably many two-dimensional manifolds. There is no empirical/model assumption in the argument: convexity, pairwise disjointness, dimension three, and supporting contact are mathematical hypotheses. The finite computations corroborate local identities and boundary behavior; the universal result rests on the analytic proof.

## Independent proof reconstruction

### 1. Compact reduction and coordinates (PDF pp.2–3)

Given a common tangent, choose actual contacts in the three sets. Pairwise disjointness makes them distinct. From a fixed countable family of original-coordinate rational closed balls choose three disjoint balls with the contacts strictly inside. The paper's actual formula is `C_i = closure(K_i) ∩ B_i` (TeX lines 53–57; the closure bar was verified in the PDF rendering). Each cap is compact, convex, nonempty and disjoint from the other caps even when the original closures intersect. A supporting closed halfspace contains the closure, and the original contact and line still witness tangency. Countably many ball triples suffice. This avoids assuming measurability or closedness of the original locus.

The three coordinate-axis graph charts cover unoriented line space: `L(u,v) = {(u+zv,z): z∈R}`, with `u,v∈R²`. In each chart the support gap is

`g_C(u,v) = max_|n|=1 [n·u − h_C(n,−n·v)]`.

It is Lipschitz for compact C. The difference-of-maxima inequality gives its individual support-summand increment between `min_C n·(δu+zδv)` and `max_C n·(δu+zδv)`, with the printed signs correct. When the projected set has interior, gap zero is exactly projected boundary membership, hence exactly supporting tangency with an actual contact. Full-dimensional C always has projection interior. Planar C has it for transverse lines; lines meeting but not transverse to its affine plane are contained in that plane and sweep a null set.

### 2. Countable two-parameter cover (Lemma 2, PDF pp.3–5)

For two disjoint compact sets of dimension at least two, fix a retained common tangent and distinct contact heights s<t. Each projected contact-normal cone lies in a strict hemisphere: an interior disk with center w and radius r gives `n·w+r≤0`, hence `n·e≥α>0` for `e=−w/|w|` and `α=r/|w|`.

Localize at the contacts by sufficiently small rational balls with the contacts strictly interior. Short convex segments toward any original point show that these caps have exactly the same projected contact normals, and short segments toward an affine basis preserve the affine hull. Their heights can be confined to bands of width `ε(t−s)` with `ε<min(1/4,α_A/16,α_B/16)`.

The line motions `V_A(z)=(t−z)e_A/(t−s)` and `V_B(z)=(z−s)e_B/(t−s)` are independent because their evaluations at s,t are respectively `(e_A,0)` and `(0,e_B)`, including equal/opposite normal vectors. Completing to coordinates `(a,b,r)` leaves two residual coordinates. Compactness keeps nearby maximizing normals in the prescribed hemispheres. The signed increment bound then gives own-coordinate monotonicity at least `m_i=α_i/4` and cross-coordinate Lipschitz constant at most ε. The residual constants K_i are finite and need not be uniform over lines.

On a sufficiently small closed a,b square, choose residual radius η with `K_iη<(m_i−ε)δ/2`. The strict endpoint signs give unique one-variable roots throughout the whole required domain. Their cross Lipschitz constants are ε/m_i. Thus the simultaneous-root map is a self-map of the square, is strictly inside the three-quarter square, and is a contraction with `κ=max ε/m_i<1/4`. Its fixed point depends Lipschitz-continuously on r with constant at most `max(K_i/m_i)/(1−κ)`. These conclusions do not require differentiability of support functions.

The final countability step correctly fixes the caps before using second countability (TeX lines 159–165). For each rational cap pair P, the set T_P of tangents where that pair admits the construction has open neighborhoods U_L satisfying `T_P∩U_L⊂Γ_L`. A countable subcover of T_P suffices. There are countably many P, and every original retained tangent belongs to some T_P. The proof does not make the invalid inference that every nearby original tangent must meet one previously chosen cap.

### 3. Density and contact ranks (Lemma 3, PDF pp.5–6)

Tangency to a compact convex set is closed in line space, by convergent contact points and unit supporting normals; the limiting support inequality and incidence persist. The exclusions for lines contained in planar hulls or identical to one-dimensional hulls are also closed. Therefore the tritangent selector E of a Lipschitz family F on open U⊂R² is Borel.

At almost every q₀∈E, E has density one and F is differentiable. Density one gives, for every h, a sequence `q_j=q₀+τ_j h+o(τ_j)` in E: a proportional-size hole would contradict density. This is a deterministic consequence at each good q₀, so no uncountable intersection of full-measure sets is used. A fixed affine shear verticalizes the base line and preserves convex support and nullness. Write `A=Du(q₀)`, `B=Dv(q₀)`.

For a contact at height z_i, `rank(A+z_i B)≤1` follows in all affine dimensions:

* Dimension three: if onto, choose h mapping to the transverse coordinate w of an interior-ball center. A point on the nearby tangent at height `z_i+τ_j(c_z−z_i)` differs by o(τ_j) from the center of the convex-interpolated interior ball of radius τ_j r. It therefore lies in the interior, contradicting supporting tangency.
* Dimension two: the retained line is transverse to the affine plane, with `N_z≠0`. Its intersection height is `(N_z z_i−N_x·u)/(N_z+N_x·v)`. Differentiation at the good point in the chosen direction gives the correct height displacement `c_z−z_i`, so the same argument lands inside a relative interior disk. A supporting plane through relative interior must equal the affine hull and cannot contain the transverse line.
* Dimension one: incidence with the fixed affine line gives `u+z_i v=(d_x−d_z v)λ`, where `d_x≠0`. Dotting with d_x bounds λ by O(|q−q₀|). Dotting with a vector normal to d_x makes the right side O(τ_j²), forcing the derivative image into span(d_x).
* Dimension zero: point incidence gives `u+z_i v=0` on E, hence zero derivative along every density direction.

The p.6 phrase “the smooth function z(q)” is interpreted precisely as a smooth rational function **of line coordinates**. Its composition with a Lipschitz F is differentiable at the good q₀; this is all that the displayed derivative argument uses. It is not necessary, nor generally true, that F or z is globally smooth in q. The supporting candidate explicitly describes smooth dependence on line coordinates. This is a nonblocking wording precision, not a proof gap.

### 4. Quadratic determinant, sweep, and dimension exhaustion (PDF pp.6–7)

Pairwise disjointness gives three distinct contact heights. The polynomial `P(z)=det(A+zB)` has degree at most two and vanishes at all three; it is identically zero. For the sweep `G(q,z)=(u(q)+zv(q),z)`, its derivative has determinant P(z). G is Lipschitz on bounded parameter balls whose closures lie in U and bounded height intervals, since v is bounded there. The bad two-dimensional parameter set times a bounded interval is three-dimensional null. Applying the equal-dimensional area formula to the Borel selector on each patch gives a null image. Multiplicity is allowed, no injectivity is needed, and E need not contain an open set. Countably many patches and integer height intervals cover complete lines.

The remaining compact cases are exhaustive. If at least two sets have dimension at least two, use Lemma 2. A point set gives smooth two-parameter direction charts `u=x₀−z₀v`. Otherwise at least two sets are nondegenerate segments. Their contact parameters determine the joining line, and disjoint compactness keeps the points apart. Local choice of a nonzero coordinate difference yields smooth intercept/slope coordinates on open extensions of the segment-parameter rectangles, including endpoints; smaller bounded rectangles are Lipschitz and countably cover the parameters. Extra lines are filtered by E. Previously discarded planes and affine lines sweep null sets. Compact reduction then proves the arbitrary-set theorem; outer regularity gives a measurable null superset.

## Primary theorem interfaces and scope

Primary-source URLs, hashes, retrieval times and reading scope are in `primary_source_pins.json`.

* [Simon, Introduction to Geometric Measure Theory](https://math.stanford.edu/~lms/ntu-gmt-text.pdf): Ch.1 Corollary 3.10 (printed p.18) supplies density for measurable E; Ch.2 Theorem 1.4 (p.45) supplies almost-everywhere differentiability, applied componentwise on open patches; Ch.2 Theorem 3.3 (pp.57–58) gives the area formula for locally Lipschitz maps on open domains and measurable subsets, with counting multiplicity. For n=m=3, its Jacobian is the absolute determinant and multiplicity is at least one on the image. These exact hypotheses match the proof. Federer and Evans–Gariepy are redundant alternative citations; they were not needed or independently re-proved.
* [Oberwolfach Report 44/2008](https://ems.press/content/serial-article-files/46191), section 13, printed p.2552: the supporting-tangency definition and Conjecture 4 match the theorem. Conjecture 3 asks for a stronger countable manifold cover and is not proved here. The historical discussion of closedness is not imported for arbitrary nonclosed inputs.
* The [archived author-host Demouth–Goaoc manuscript](https://web.archive.org/web/20110401122240id_/http://www.loria.fr/~goaoc/papers/TopVE.pdf), section 7, printed p.11, asks the compact-convex nullness question. Its archive capture does not establish a publication date or identity with a version cited in 2008.
* Context was checked against the [publisher abstract of Some New Results on Geometric Transversals](https://link.springer.com/article/10.1007/s00454-023-00573-2) and the authors' [related arXiv note, 2205.14681v2](https://arxiv.org/pdf/2205.14681v2), Theorem 1. The latter asserts acyclicity of components of the space of meeting transversals to at least two disjoint open convex sets. This is a different conclusion from spatial nullness of supporting tangent lines. The related note is not represented as the full 2024 published article. No exhaustive literature/priority claim is certified by this review.

## Checkable fresh controls and published replay

`fresh_geometric_controls.py` uses exact standard-library rational arithmetic, independently of the submitted code. Its retained result records **26,250 passing checks**: all 6,561 pairs of 2×2 matrices with entries −1,0,1; determinant-polynomial evaluations, including 513 three-root pencils and 464 genuinely nonzero two-root pencils; arbitrary rational contact heights and very small height separation; 756 support-increment checks for full- and lower-dimensional convex hulls; 49 parameter values of a separately constructed nonsmooth max-of-affine simultaneous-root model, all active-piece solutions and pairwise Lipschitz comparisons; and 900 small-aperture pairs for root bracketing/self-map/contraction constants. The two-rectangle example independently gives swept volume exactly **2/3**. These are corroborative tests, not a substitute for the density, countability, compactness, or area-formula proofs.

The boundary claims on p.7 also check directly. Two supporting contacts can sweep positive volume. Three identical singleton sets violate disjointness and have all of R³ as their union of tangent lines. Vertical unit-ball tangents are parameterized by a zero-density circle, demonstrating why differentiating on an arbitrary parameter subset would be invalid. Mere interior intersection is not supporting tangency. The three open parallel segments give a genuinely nonclosed locus: their common horizontal lines approach the origin, but no line through the origin can meet both the first open segment and the second.

The submitted package was replayed in a private cache, with actual child stdout/stderr and capture records retained. The positive run passes **2,826 checks**. Optimized execution and an intentionally false control each exit 1 as expected. Building from the unchanged original inputs **before** updating the timestamped verification receipt reproduces the published ZIP byte for byte, with SHA256 `1fd934e9f8b011307137500039192c93c34f505c472a19fb47ba03af3ab5b9c5`. This certifies archive reproduction, not a fresh LaTeX compilation of the PDF. The actual PDF and TeX were read and their source bindings checked. Details are in `published_replay_receipt.json`, `replayed_verification.json`, and the four capture/child-stream sets.

## Remaining gap and disposition

**No remaining load-bearing mathematical gap was identified for Theorem 1.** All eight pages and mathematical support were covered, all four affine dimensions were reconstructed, and the exact imported measure-theory hypotheses were checked. The small smooth-composition wording point above has no effect on the argument. Stronger manifold-cover claims, exhaustive priority, and independent external human review remain outside this verdict. No source, website, spreadsheet, Git, Zenodo, or outreach action was performed. Review completion: **100% of the assigned analytic review**, not a probability of theorem truth.
