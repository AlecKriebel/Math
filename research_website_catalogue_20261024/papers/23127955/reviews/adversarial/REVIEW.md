# Independent adversarial review: Zenodo 23127955

**Disposition: PASS at the stated supporting-tangency definition and hypotheses.** No substantive mathematical defect or unresolved load-bearing gap was identified. This is an AI mathematical review, not human peer review, a formal proof certificate, a novelty certificate or permission to publish.

## Exact edition and coverage

Reviewed *The spatial locus of common tangents to three disjoint convex sets is null*, Zenodo version 1.0, published 3 October 2026. All eight pages of the deposited PDF, the complete mathematical TeX source and `source/CANDIDATE.md` were read. Pages 2, 4 and 6 were additionally rendered and visually inspected to verify closure notation, the quantitative root bounds and the rank/sweep formulas against extraction. All mathematical code in `verify.py`, `run_capture.py` and `build_archive.py` was read before running it in an isolated working copy.

Bindings:

- Main PDF SHA-256: `80b3fc3e8cb470a22a1226b960467de9e67dd8c3ccf054b42133d9ba0ce9d327`.
- Deposited ZIP SHA-256: `1fd934e9f8b011307137500039192c93c34f505c472a19fb47ba03af3ab5b9c5`.
- TeX SHA-256: `2522ac0138de5e21067af8c16e6749b3a9d3cd01f12bdb929cca87cb6baeabb6`.
- Mathematical candidate SHA-256: `8ac19b70bd9081107e903ca47bb9dd6ad05274f604d03000a7fd18e3cfb3bf12`.

The exact receipt, all extracted-source hashes, primary-source receipts, fresh controls and replay streams are bound in the accompanying verdict/evidence. The PDF contained in the ZIP is the same eight-page deposited PDF. No additional reader manuscript is hidden in the package.

## Target hypothesis and falsification criteria

The claim is that for **any three pairwise disjoint convex subsets of R³**, the union of the **complete affine lines** tangent to all three has three-dimensional Lebesgue outer measure zero. Here tangency requires both actual intersection with the set and containment of the whole line in a supporting plane. The latter bounds a closed halfspace containing the set. A contact need not be a singleton.

Empty, nonclosed, unbounded, nonsmooth and affine-dimension 0–2 sets are included. The assertion concerns spatial points on lines, not just a null subset of four-dimensional line space. It is not a statement about lines merely meeting three sets, or about avoiding their ambient interiors. It asserts neither a countable union of two-manifolds nor a Hausdorff-dimension bound of two.

I sought a positive-volume counterexample in degenerate configurations, a failure of the two-parameter covering lemma, a loss of countability caused by moving contacts/caps, an illicit differentiation of the tangency subset, and a mismatch between the measure-theoretic inputs and the image being measured. The proof survived those tests at its exact definitions.

## Independent reconstruction and attacks

### 1. Compact reduction does not import false closedness

For any one common line, actual contacts are three distinct spatial points. Pairwise disjoint rational closed balls can be chosen with the contacts strictly inside. Intersecting each ball with the corresponding original closure gives disjoint compact convex sets. The supporting halfspace survives taking closure and the original contact remains present, so that line is still tangent to the compact caps.

The balls come from one countable collection in the original ambient coordinates. Hence their triples give a countable outer cover even when the original closures intersect, sets approach one another at infinity, or the original spatial locus is not closed. A uniform lower separation of the original sets is unnecessary. The proof needs inclusion in the compact-case union, not equality; extra closure tangents cause no problem. This directly answers the most plausible nonclosed/unbounded objection.

### 2. The support-gap and local-chart mechanism is quantitative

In a line chart, a line is `(u+zv,z)`. Its projection of a compact convex set has a boundary point at `u` precisely when the line has the required supporting plane and actual contact, provided that projection has interior. Full-dimensional sets always have projection interior; for a planar set the exception is a line contained in its affine plane, already a null spatial contribution.

The signed support increment has the correct **plus** sign in `delta_u + z delta_v`: this follows by subtracting the two support maxima, with the minus sign in `h(n,-n·v)` reversing their changes. No differentiability of the support function is used.

At a boundary point of a full-dimensional planar projection, an interior disk places all outward contact normals in a strict hemisphere. A small ball containing the contact strictly inside preserves the entire contact-normal cone: a newly supporting functional positive on an original point would already be positive on a short segment from the contact inside the ball. The same segment argument retains an affine basis. Thus capping does not secretly create a lower-dimensional projection or change the supporting-normal condition.

At two distinct heights `s,t`, the two motions take respectively the values `(e_A,0)` and `(0,e_B)`. They are independent even for equal or opposite `e_A,e_B`. On sufficiently thin caps their own monotonicity constants are `m_i=alpha_i/4`, whereas the cross Lipschitz constant is at most epsilon. The manuscript chooses epsilon strictly below `alpha_i/16`; therefore the cross-root contraction constant is strictly below 1/4. The root brackets follow from `K_i eta < (m_i-epsilon) delta/2`. Those inequalities justify roots on the **whole** closed square, its strict self-map property and the Lipschitz dependence of the fixed point. No global aperture, contact-gap or uniform chart constant is needed.

I specifically checked the common-kappa versus individual-margin issue: the printed bound is 3/4, which follows from a common first term below 1/4 and an individual residual term below 1/2. The stronger discarded 5/8 estimate is not used in the published proof.

### 3. Countability keeps the cap pair fixed

Simply taking a countable subcover of neighborhoods around arbitrary original tangents would be invalid: nearby tangents may miss the originally chosen cap. I constructed that failure independently. Let `A=[-1,0]×[-1,1]×[0,1]`, and let `L_delta=(delta(1-z),0,z)` for positive delta. The plane `x+delta*z=delta` supports A, but its contact is only at height 1. These lines approach the vertical face line while missing the cap of radius 1/10 about `(0,0,1/4)`.

The paper avoids this exact failure. It first fixes a rational cap pair P and covers only the set T_P of tangents for which the construction is available for that same pair. Every selected neighborhood is controlled by the zero equations for those fixed caps. Second countability supplies a countable subcover of this subspace; a further countable union over P covers all original tangents. Orthogonal coordinates can vary among the selected charts because the resulting countably many spatial null sets are transformed by fixed invertible affine maps.

### 4. The contact-rank lemma uses density, not an open tangency set

Tangency to a compact set is closed: contact points and unit supporting normals have convergent subsequences, and their limiting inequalities retain incidence and support. Removing contained planar lines and identical one-dimensional affine hulls leaves a Borel parameter subset E.

At a density-one, differentiability point, every fixed parameter direction h can be approached by E with `q_j=q_0+tau_j*h+o(tau_j)`. The distance-to-E argument is valid: a hole of radius comparable to tau would remove a fixed fraction of a ball about q_0. A separate sequence for each h is sufficient; neither a common sequence nor a measurable contact selection is required.

The four affine dimensions were checked separately:

- **Dimension 3:** if `A+z_i B` were onto, choose h pointing toward an interior-ball center. A point on the nearby line lies within `o(tau)` of the convexly scaled center, while the contained ball has radius proportional to tau. This forces interior intersection and contradicts support. The changing height contributes only a second-order slope term.
- **Dimension 2:** after excluding contained lines, the reference line is transverse to the affine plane. Its nearby intersection height has a nonzero denominator and the stated derivative. The same scaled relative-disk argument forces a relative interior contact. Its only supporting plane is the affine hull, which cannot contain the transverse line.
- **Dimension 1:** after excluding the identical affine line, its transverse direction `d_x` is nonzero. Incidence gives `u+z_i v=(d_x-d_z v)lambda`; dotting with `d_x` bounds lambda by `O(|q-q_0|)`. The component perpendicular to `d_x` is consequently second order, giving rank at most one.
- **Dimension 0:** incidence at the fixed point gives `u+z_i v=0` on E and therefore zero derivative along the density sequences.

These arguments work at every chosen contact of a good parameter, so no smooth boundary, curvature or unique supporting plane is assumed. The bad set is null only **within E**; nothing in the subsequent argument needs it to be null throughout U.

### 5. Three distinct contacts nullify the complete spatial sweep

Disjointness makes any three selected contact heights distinct. The two-by-two pencil determinant `det(A+zB)` is quadratic or lower. Its three distinct zeros therefore force it to vanish at every finite height, not just at the contacts. The swept map has Jacobian block determinant equal to this polynomial.

The map is Lipschitz on bounded parameter balls with closure in the domain and bounded height intervals. The exceptional parameters in E, multiplied by a bounded interval, remain three-dimensionally null. The measurable-set area formula with multiplicity then bounds the swept image by zero. This neither requires injectivity nor incorrectly applies Sard's theorem to a nonsmooth map. Countably many parameter/height patches recover complete unbounded lines.

For the remaining dimensional configurations, a point gives ordinary two-parameter direction charts; if there is no point and fewer than two sets have dimension at least two, two sets are nondegenerate segments. Their disjoint compactness keeps endpoints apart, and a locally nonzero component of their connecting vector supplies smooth charts on open rectangles, including extensions around endpoint parameters. All other discarded lines remain in finitely many affine planes/lines. Thus no dimensional case is left uncovered.

## Fresh controls and independent family

Before reading submitted `verify.py`, `evidence/fresh_controls.py` passed **17,524 exact assertions**. These include 2,400 rational support-increment controls on varying finite convex hulls, all 6,561 pairs of 2×2 matrices with entries in {-1,0,1}, and the explicit moving-cap countercontrol above. Five families of false extensions were rejected: ambient-interior avoidance as tangency, two contacts, repeated contacts, omitting density and replacing support by interior transversality.

A distinct analytic test class was three unit balls centered at `(0,0,0)`, `(0,0,3)`, `(0,0,6)`. For a line `p+R*d`, the tangent condition at center `z*e_3` is

`|(z*e_3-p) cross d|² - |d|² = 0`.

This is a quadratic in z with leading coefficient `d_x²+d_y²`. Three tangencies force it identically zero, hence d is vertical and the transverse distance is one. Conversely every such vertical line is tangent to all three disjoint balls. Their complete spatial locus is the unit circular cylinder, a null surface. This classification is an independently derived exact family, not a numerical search or a proof for arbitrary convex sets. The script checks the distance polynomial at 1,200 rational choices and 483 exact positive incidences.

The paper's own two-rectangle positive-volume example has the stated supporting planes, signed determinant and volume 2/3. Its repeated-singleton, zero-density circle and nonclosed-strip controls also have the claimed mathematical behavior. These support the necessity of the hypotheses rather than strengthening the theorem.

## Primary theorem interfaces

Fresh original bytes were fetched independently from [Leon Simon's Stanford notes](https://math.stanford.edu/~lms/ntu-gmt-text.pdf), SHA-256 `ba7fd4a53bf0f1d0ac54aec50bb72c4bba196b8e784d65cd0a7fd85131a3bf03`. Chapter 1 Corollary 3.10 supplies density for measurable sets. Chapter 2 Theorem 1.4 supplies almost-everywhere differentiability; local vector-valued use follows by coordinatewise Lipschitz extension on patches. Chapter 2 Theorem 3.3 and its multiplicity remarks cover locally Lipschitz maps on open domains and measurable subsets without injectivity. Equal-dimensional Jacobians give precisely the required inequality.

The [official Oberwolfach report](https://ems.press/content/serial-article-files/46191), SHA-256 `3fcc907de0d7003b3d2cdfe3e7151e18309e926a4b6471e818e70f1ab085af35`, printed page 2552, uses the same actual-contact/supporting-plane definition. Its Conjecture 4 asks for null-set containment, whereas Conjecture 3 asks for two-manifold containment. The manuscript correctly separates them. The historical closedness sentence is not imported for nonclosed inputs.

Federer and Evans–Gariepy are redundant references, not additional unverified dependencies. I did not independently read their complete books, the complete archived Demouth–Goaoc body or the complete 2024 transversal paper. Those historical/novelty comparisons are outside this mathematical gate; no global novelty or current-openness conclusion follows from this review.

## Reproduction and source integrity

The published verifier ran in a copied package and passed **2,826** finite controls. Its optimized execution and intentional false-control modes each returned nonzero as intended. Full prelaunch metadata and output/error streams are retained under `evidence/replay/`.

Before the timestamped verification receipt was regenerated, the supplied archive builder reproduced the **exact deposited ZIP twice**, including its SHA-256. This checks the package's deterministic-byte claim. Re-running verification legitimately changes an archive input timestamp and is not alleged to preserve the old ZIP. All 15 extracted original files remained unchanged. The new computations establish finite algebra/implementation checks, not a universal convexity or measure-theoretic theorem.

## Independence, limitations and strongest supported result

No sibling review or separate historical verdict was read. Required mathematical support contained an old status header and references to previous audits; README and source-binding metadata also contain historical disposition summaries. These unavoidable incidental statements were recorded but not used as mathematical evidence. Fresh controls preceded inspection of the submitted verifier. The team supplied only raw primary paths/hashes after my own primary fetch had begun; no other review findings entered this verdict.

**Strongest supported result:** the stated outer-measure-zero theorem for the union of complete supporting tangent lines to any three pairwise disjoint convex subsets of R³, including all explicitly listed degenerate and noncompact cases.

**Exact remaining mathematical gap:** none identified in the reviewed proof. This judgment remains subject to ordinary limits of independent AI mathematical checking. It does not establish two-dimensional rectifiability, historical first priority, human peer review or formal machine verification. No follow-up conjecture meeting the required high bar is proposed here.

No manuscript repair, site/promotion edit, Git action, spreadsheet change, UI action or external outreach was performed.
