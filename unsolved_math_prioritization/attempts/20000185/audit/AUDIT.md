# Independent adversarial audit: fixed-camera epipole overlap

Target: 20000185 / AIM-ALGEBRAIC_GEOMETRY-0185, rank 639.
Date: 4 October 2026 UTC.

## Decision

**PASS for the explicitly scoped algebraic theorems; no blocking mathematical error found. Keep the broad target UNSOLVED.**

This is an independent AI-assisted mathematical and exact-computation review, not human peer review or formal proof-assistant certification. It confirms the manuscript's restricted claims under their stated hypotheses. It does not establish priority, a real/physical reconstruction criterion, or a full resolution of AIM 1.25. Five substantive approaches are recorded; this review has not created another source-problem proof attempt.

No frozen input was edited. No repository, branch, PR, or remote state was changed. No third-party full text, PDF, dataset content, credentials, or private coordination file is included in this audit deliverable.

## Exact object reviewed

The input directory contains eleven files and is named `submission`. The controlling external manifest is SHA-256:

`43286aeaa36c1e27b4ccfe7ef1a002f26e3dad3f56cce702c0b654a2eba05698`

The reviewed `PROOF.md` is 23,024 bytes and has SHA-256:

`488a29cd89d119140b23c7653933416d84935ab2a5201c90895f052316a89c36`

All eleven external-manifest byte counts and digests matched. The internal verifier separately checked its ten listed payload files; its eleventh file is the internal manifest itself. Thus the different counts are consistent, not a missing-file discrepancy.

## Mathematical challenge findings

### 1. Camera coordinates and the component dictionary

Distinct centers of rank-three projective cameras justify choosing two independent common linear forms and coordinates P=[a:s:t], Q=[b:s:t]. The joint map is an isomorphism from the complement of the baseline onto incident image pairs with both epipoles removed. That open-set inverse is essential: it establishes birational triangulation of a correspondence component rather than merely producing a parametrization of uncertain degree.

For an integral plane image, normalization correctly separates all branches over an epipole. The fixed pencil divisor has coefficient equal to the minimum of the two local section orders. A general line through the epipole has precisely those minimum orders on all branches, so its total fixed degree is the plane-curve multiplicity alpha. The moving degree is m-alpha. An integral curve with constant pencil coordinate is necessarily a line through the epipole. Thus all positive-degree claims exclude exactly the constant-pencil case that the manuscript treats separately.

The normalized factors are smooth projective curves; their finite maps to P1 are flat. Separability makes the generic tensor product reduced. Their fiber product is a nonzero Cartier divisor in a smooth surface, hence has no embedded associated points. Together these facts give reducedness, without an invalid claim that the fiber product is normal. Each one-dimensional component dominates both factors because those projections are finite. Removing finitely many singular-image points still leaves a dense open subset on each component. This suffices for the world-component dictionary even when either plane image is singular.

An additional world curve cannot hide on a camera ray: a curve contracted by one camera would have an epipolar-line image under the other. The hypotheses exclude that. The baseline itself has point images and is not an integral realization of the two prescribed image curves.

### 2. Degree, overlap, and center multiplicities

The four triangulation sections are sections of H(A+B), where H has degree N. At a normalization point with divisor coefficients U,V, their valuation list is

(x_order+V, y_order+U, U+V+S_order, U+V+T_order).

Here min(S_order,T_order)=0; U>0 forces x_order=0, and V>0 forces y_order=0. These constraints imply that the common minimum is min(U,V). The resulting world hyperplane bundle is therefore H(A+B-min(A,B))=H(max(A,B)). Birationality of triangulation, proved separately, is what permits its degree to be identified with the degree of the reduced embedded image.

The P-triple has residual fixed order (V-U)+ and the Q-triple has residual fixed order (U-V)+. The baseline pencil has fixed order max(U,V). These statements remain true at ramified pullbacks, where A and B already include their respective pullback ramification indices. Replacing these coefficientwise operations with a comparison of total degrees would be wrong; the manuscript does not make that replacement.

For an integral space curve, the sum over normalization branches of the minimum orders of coordinates through a point equals the multiplicity at that point. This is a general-hyperplane intersection computation and does not require a smooth embedded world curve. Consequently the center identities do not hide a smoothness assumption. The max/min degree formula and both center corrections survive this audit.

The gcd partition is a statement about N and moving degrees r,q. Degree multiplication gives r a_j=q b_j, and reducedness makes the sum of component projection degrees equal q. The arithmetic partition is correct; ordinary image degrees cannot be substituted for r,q in the epipole regime.

### 3. Saturation and baseline cycle

Irreducibility of f and g survives adjoining an unused variable. A common irreducible factor would force the two cones to coincide; then it depends only on s,t and is a binary homogeneous irreducible form, hence a linear form over the stated algebraically closed field. That is the excluded epipolar-line case. The two cone equations consequently form a proper complete intersection, with no embedded components.

Generic points of every non-baseline component dominate both images and avoid their finite singular and ramification loci. The incidence model is therefore generically reduced there. A primary ideal whose localization at its unique associated prime has length one equals that prime: its primary saturation property contracts the localization back unchanged. This validates the manuscript's primary-decomposition step. Saturating by the full baseline ideal removes precisely the baseline-supported primary piece and leaves a radical ideal with the claimed curve components.

Bezout gives total cycle degree mn. Subtracting the reduced proper-component degrees gives alpha beta plus the sum of the overlap-divisor degrees, exactly the stated baseline multiplicity. This is a cycle statement, not a claim that the raw intersection is reduced on the baseline. No hidden zero-dimensional embedded contribution has been discarded, because complete-intersection unmixedness was established first.

### 4. Hypotheses and excluded interpretations

The constant-pencil and coincident-center weak-existence claims are correct. A common-center pair differs by an image projectivity. For distinct centers, a single constant pencil cannot match a nonconstant one; two equal constant pencils admit a line in their common epipolar plane avoiding both centers.

The real quadratic-twist example has only the two listed real baseline-free intersection points, and its covers are not isomorphic over R. The disjoint-range example has no real incident pair, including at infinity. The characteristic-two example is a double conic, so omitting separability would invalidate reducedness and the unweighted component partition. These are genuine scope controls. They do not amount to a general real, visible, noisy-data, reducible, or nonreduced classification.

Normalizing a component does not certify its embedded image is smooth. The manuscript explicitly preserves this distinction. Its exact elimination criterion for embedded smoothness is appropriately scoped to the nonconstant-pencil regime.

## Computation replay and independent controls

The unmodified author verifier passed **8,625 assertions** and all **1,225** rational image pairs. The replay JSON is exactly equal to the frozen CONTROL_RESULTS.json, including the recorded Python and SymPy versions. The manifest verifier also passed.

The separate `independent_checks.py` passed **7,305 assertions** and does not import or execute the author verifier. Its exact tests include:

- 1,792 allowed local valuation patterns, checking the four-section common divisor, both camera fixed orders, and the baseline fixed order.
- A different local-length method: the order in s of Res_t(f,g) over Q(z). The script verifies that the projection is finite and that the only common point above s=0 is the origin. Thus the resultant valuation is the generic-baseline local intersection length, not a sum contaminated by other fiber points. This independently reproduces lengths 2, 1, 5, 7, and 14 without truncation or the author's Nakayama-stabilization method.
- Six pairs of irreducible toric image curves, with moving degrees from 2 through 6 and one, two, or three geometric correspondence components. These test ramified pullbacks and unequal center orders outside the author's r=q=1 rational family. The respective baseline lengths are 3, 15, 14, 15, 5, and 5.
- A multibranch monoid pair of degrees 4 and 5. One epipole divisor contains a double branch contribution; two distinct branches overlap. Exact cancellation gives world degree 6, and the independently computed baseline length is 14.
- A separate rational quartic with two distinct epipole branches and moving degree two, paired with itself. The diagonal and antidiagonal correspondence components have world degrees 4 and 6, although they have equal moving degrees. Exact saturation and ideal intersection agree; separate Hilbert-series computations give component degrees 4 and 6 and union degree 10. The generic-baseline resultant length is 6, yielding 10+6=16. This directly attacks component-dependent overlap, singular images, and extraneous-component concerns.

These computations are controls, not substitutes for the universal proof above. Their polynomials are review-generated mathematical test data, not copied source content.

## Source and attribution review

The canonical [AIM reconstruction page](http://aimpl.org/algvision/1/) was independently retrieved with HTTP 200. Its 38,731 bytes and SHA-256 match the declared source metadata. The selected item 1.25 exactly matches the selected dataset record; the canonicalized selected-record digest also matches. The primary status field is empty. Item 1.4 is related, not interchangeable with the target. A web-tool fetch initially failed; the ordinary canonical HTTP retrieval then succeeded without bypassing any TLS warning.

The four locally retained public PDFs all match their declared sizes and hashes. Relevant online primary-source passages were independently inspected:

- [Hidalgo, Reyes-Carocca and Vega, Proposition 2.6](https://arxiv.org/html/1611.07880v3): the gcd component bound and the lcm-divisibility mechanism are prior work. The manuscript's attribution and refusal of novelty are warranted.
- [Fryers, Kaminski and Teicher, Theorem 3](https://arxiv.org/pdf/math/0208099): the proof uses the epipolar fiber product and its monodromy to distinguish the generic true and ghost components. The manuscript correctly credits this foundation.
- [Agostini et al., Corollary 2.5 and Section 3](https://arxiv.org/html/2205.11287v2): the classical degree-three cover count is 40 and comes from 240 admissible transposition tuples modulo simultaneous conjugation. Its source credit is correct. The manuscript's use of a degree-three very ample line bundle explains why abstract genus-one covers yield plane-cubic projections.
- [Rydell and Sundelius](https://arxiv.org/html/2404.03063v1): back-projected cones and the two-view conic multiview variety are established context. A closure of image families must not be identified with every physical reconstruction notion.

The imported reports for the target and related ID 20000188 contain the clean correspondence and degree laws, as well as moving-degree and necessary center corrections. Their overlap is acknowledged in the manuscript. This audit does not certify novelty of the coefficientwise overlap formula. Nor does it independently rehash the complete upstream corpora; it verifies the selected record and source assets actually inspected.

## Nonblocking editorial clarifications

1. In Theorem 1's local proof, explicitly separate U=V=0 from the cases where exactly one coefficient vanishes. When both vanish, x and y can both vanish; one of S,T is a unit and supplies the required zero common order. Suggested sentence: "If U=V=0, one of S,T is a unit; if exactly one coefficient is positive, the corresponding epipole coordinate is a unit. In all cases the common order is min(U,V)." The existing argument already contains the needed basepoint-free premise; this is a clarity improvement, not a correction to the formula.
2. The finite-procedure statement should spell out the computational meaning of an effective coefficient field. Suggested qualification: "over characteristic-zero coefficient fields equipped with effective arithmetic and geometric factorization/primary-decomposition algorithms, for example algebraic-number input." Mere computability of field operations alone is not a promise of all geometric decomposition algorithms. The underlying algebraic criterion is unaffected.
3. The author examples saturate by t rather than computing saturation by the ideal (s,t) directly. This is valid in those examples because no proper component lies in t=0; a one-sentence explanation would prevent the code from appearing to implement arbitrary ideal saturation. The independent quartic test uses the full baseline ideal.

No change to the frozen packet is required to preserve the scoped mathematical conclusions. If these editorial clarifications are adopted, a new freeze and review binding should be generated; this report certifies only the hashes above.

## Reproduction

With Python 3 and SymPy 1.14 installed:

1. Run the packet's `verify_manifest.py` and `verify.py` without modifying its input directory.
2. Run `python independent_checks.py /path/to/submission` from this audit directory, with the exact external FREEZE_MANIFEST.json alongside that submission directory.
3. Compare generated JSON with `independent_results.json`. All test construction is local and deterministic; no network, source PDF, corpus, remote repository, or credential is required.
4. `AUDIT_MANIFEST.json` binds every audit artifact by byte count and SHA-256. It is a manifest rather than a self-hashing object.

The correct final disposition remains: **scoped partial result reviewed; broad AIM target unsolved; no novelty claim**.
