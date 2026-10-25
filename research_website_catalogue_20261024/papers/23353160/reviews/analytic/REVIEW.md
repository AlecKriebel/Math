# Analytic review — Zenodo 23353160, v1.0

**PASS for the exact stated theorem, using the expressly imported, published Fawzi theorem.** No substantive mathematical defect was found. The two-hyperplane section is real-linearly isomorphic to normalized complex Sep(3,3); consequently the oriented real mass ball C(4,12) has no finite projected semidefinite lift. The supporting affine-SOS and calibration-completion consequences follow with the stated existential limitations.

Completion: 100% of the assigned analytic review, 2026-10-25 UTC. No source repairs, outreach, site, spreadsheet, Git, or publication actions were taken.

## Version, coverage, and independence

| Published input | SHA-256 |
|---|---|
| Six-page PDF | `2228c5e4379d43302b5ca2d0f97e99d428e3755fc14abb91accef168d2b533d5` |
| Source/verification ZIP | `d7519c53310f6a1425fcc8b521f8b6f7e2c94a372bca9bf0173ee8f047706c5d` |

Read all six actual published pages, the complete current TeX source, the full mathematical PROOF.md preserved in the package, and the entire SUPPLEMENT.md. Read the principal exact coordinate checker, portable reproduction runner, and preserved finite-check runner whose pure mutation function is used by the portable runner. Checked the exact certificate against independently reconstructed coefficients. The other historical review narratives, search records, and previous reviewer programs are not theorem premises and were not used to validate the result.

The package's research_note.pdf is byte-identical to the separately published PDF. A fresh Tectonic build gave exactly the same extracted text on all six pages. The map and normalization on printed page 2 were inspected in a rendering. All 253 extracted files were compared byte-for-byte with their ZIP entries at completion, and both published files still match the acquisition receipt.

**Independence is qualified.** The full current-paper argument and my fresh 126-check exact program were reconstructed before opening supplied arithmetic implementations. Opening the additional mathematical PROOF.md then exposed its first-line status stating acceptance after an AI-assisted audit. The later full supplement also contains favorable historical audit summaries. This incidental exposure was immediately reported to root. No historical review-report bodies or current sibling opinions were opened; initial conclusions and fresh controls preceded the favorable status. The completed review is therefore not described as wholly blind. Historical approval statements are not evidence for this verdict.

## Exact claim and parameter domain

The objects are real exterior vectors in Λ⁴R¹², with both orientations of every unit simple four-vector included. Their convex hull is the mass ball. The separability body used in the section is the trace-one **complex** 3-by-3 bipartite body; it is neither an unnormalized cone nor the real separable-state analogue. The auxiliary projector space is Herm(Λ²C⁶), real dimension 225, and its mixed block has complex dimension nine.

“No finite semidefinite lift” excludes any finite projected LMI with additional affine equations and auxiliary variables. It is stronger than failure of an unprojected spectrahedron or failure of a particular relaxation hierarchy. The SOS assertion concerns affine polynomials of degree at most one, modulo the full real vanishing ideal. Constants are allowed.

The result asserts existence of a nonzero rational-coefficient **unnormalized** supporting functional whose support defect is not affine SOS. Its maximum and its normalized calibration need not be rational, and no explicit coefficient list is supplied. No least-dimension, lower-dimensional classification, priority, or community-acceptance claim is inferred.

## Primary-source interfaces

1. **Fawzi's published Theorem 1:** read the normalized-state definition on printed p.1319, the projected Hermitian-LMI definition on p.1320, and Theorem 1 and its explicit Sep(3,3) specialization on p.1321. These are exactly the body and representation class required here. Real-symmetric lifts are a subclass of the Hermitian lifts excluded there. An affine equality may be appended to a lift as two scalar semidefinite inequalities or eliminated in its affine parameter space. No restriction to a hierarchy or finite list of positive maps is being substituted. Source: [published paper, Cambridge repository](https://www.repository.cam.ac.uk/bitstreams/e6e52df9-b317-4616-9462-c79a3cb4844b/download), SHA-256 `42a425544b2318b75aa1b9cad3374eb8681eaaea4b427208eb526ace56f697b6`. The [2019 v1 preprint](https://arxiv.org/abs/1905.02575) was also read at the same interface. The theorem itself is accepted as an established external result, not purportedly reproved by finite checks.

2. **Original SOS question:** read Sanyal's complete Grassmann-orbitope discussion on printed pp.707–709 of [OWR 13/2015](https://ems.press/content/serial-article-files/46561), including the degree-one conjecture and credit to Rostalski. The manuscript's affine interpretation matches the polynomial-degree formulation. Even if one used the ideal generated by the displayed equations rather than the full vanishing ideal, failure modulo the larger full ideal would still imply failure modulo that smaller ideal.

3. **Original calibration question:** read Harvey–Lawson's comass and geometry definitions (printed pp.56–57), calibration Definition 4.1, and [Question 6.5 on printed p.68](https://archive.ymsc.tsinghua.edu.cn/pacm_download/117/6313-11511_2006_Article_BF02392726.pdf). The scanned question was also visually inspected to confirm its norm-square identity and quantification over all simple vectors. A constant closed comass-one form satisfies the original calibration definition. The argument only needs local completion to imply completion at a point; it makes no unjustified smooth-selection inference in the opposite direction.

4. **Tensor-to-wedge and fermionic-body lineage:** read Vrana–Lévay's [§3.1, equation (25), lemma and theorem](https://arxiv.org/abs/0902.2269v2), and Grabowski–Kuś–Marmo's [Definition 4.2 and Theorem 5.1](https://arxiv.org/abs/1111.4812v2). They support the claimed prior constructions. Normalized rank-one projectors are invariant under the harmless exterior-product norm convention: the latter source uses a factorial in writing its orthonormal wedge generators, whereas this manuscript declares the standard induced exterior norm. The proof uses its declared convention consistently.

Primary URLs, timestamps, byte sizes, and hashes are retained in `primary_sources.json`. The Kähler equality case, finite-lift transfer, moment implication, and pointwise SOS/completion relation were independently reconstructed below. No generic theta-body theorem with hidden closure hypotheses is needed. The broad historical priority search and counts of queries/PDFs were not independently repeated or used as proof evidence.

## Reconstruction of the mathematical argument

### Kähler equality and the linear embedding (printed p.2)

Let J be the standard orthogonal complex structure and Φ=ω²/2. Compressing J to an oriented real four-plane gives a skew operator with two singular values of magnitude at most one. Its signed Pfaffian is Φ evaluated on the unit volume vector. Equality at +1 forces both singular values to have magnitude one. Equality of projected and full norms then makes the plane J-invariant; the Pfaffian sign selects its complex orientation. The reverse implication follows from an orthonormal complex frame. Thus the exposed face Φ=1 consists exactly of convex combinations of positive complex two-planes. Compactness and finite convex combinations suffice; no closure of an infinite mixture is inserted.

In the complexified exterior space, the u_i and their conjugates are independent bases of the +i and -i eigenspaces of J. Consequently the 225 products u_I∧conjugate(u_J) are a complex basis of type (2,2). The formula A(H)=ΣH_IJ u_I∧conjugate(u_J) is fixed by conjugation for Hermitian H: transposing the coefficients is canceled by swapping the two degree-two exterior factors, which has positive sign. It is real-linear and injective on all 225 Hermitian coordinates.

With w_i=e_i-if_i, each two-vector contributes a factor 1/2, giving the required 1/4 factor in A. For arbitrary complex a,b, the identity a∧Ja=-i â∧conjugate(â), followed by moving conjugate(â) past b̂, yields

\[
A((a\wedge b)(a\wedge b)^*)=a\wedge Ja\wedge b\wedge Jb.
\]

Both sign changes are needed and cancel. A decomposable unit complex bivector has a complex-orthonormal factorization after a phase adjustment. Conversely every generating positive complex plane has such a factorization. Hence F=A(K), not merely a nonlinear identification of extreme points. Direct coefficients give Φ(A(H))=tr(H) for every Hermitian H.

### Exact mixed-block section and transfer (printed p.3)

Write C⁶=U⊕Z with both factors C³ and split Λ²C⁶ into pure blocks D and mixed block B=U∧Z. If H=Σλ_t z_tz_t* belongs to K and tr(P_DH)=0, then Σλ_t‖P_Dz_t‖²=0. Every positive-weight generator lies in B. This proves the needed generator-level statement; mere matrix support alone would not identify the convex hull.

If a∧b is nonzero and lies in B, the U components of a,b are dependent and the Z components are dependent. Neither component span can be zero. Choosing their respective spanning vectors x,y gives a∧b equal to a nonzero scalar times x∧y. This is exactly the rank-one tensor condition under the unitary map U⊗Z→B. Orthogonality supplies the norm product, so a unit mixed bivector corresponds to unit product factors and trace-one complex separable projectors. Thus K₀ is exactly Sep(3,3).

The ambient functional Q=(ω_U²+ω_Z²)/2 equals the pure-block trace on A(H). Therefore the section of the mass ball cut simultaneously by Φ=1 and Q=0 is A(K₀). Q need only be nonnegative on F. It is indeed negative at some points of the mass ball, and no global nonnegativity claim is used. The two equations without mass-ball membership do not specify the separable set: a normalized rank-one entangled mixed projector meets both equations but cannot belong to K.

Affine sections preserve a lift by imposing the section equations on its projected point. Linear images preserve lifts, and A's inverse on its image extends to an ambient real-linear map. A hypothetical lift of C(4,12) would therefore give the exact forbidden lift of Sep(3,3). This completes the nonrepresentation deduction using precisely the established Fawzi theorem.

### Compact first moments and a rational separator (printed p.4)

For compact nonempty X in the unit sphere of Rᴺ, the degree-at-most-two part J₂ of its full vanishing ideal is finite-dimensional. The matrix constraints M≥0, M₀₀=1 and L_M(J₂)=0 are finitely many affine constraints. The sphere relation fixes the remaining diagonal sum to one, so tr(M)=2. Positive semidefiniteness bounds all entries, making the feasible spectrahedron and its projection compact. This removes the potential nonclosed-shadow issue.

Every point of X has its rank-one moment matrix, so conv(X) lies in the projection T_X. If a supporting defect δ-ℓ is a sum of squares of affine forms modulo I(X), its discrepancy has degree at most two and is in J₂. Applying L_M gives δ-ℓ(x)=Σa_jᵀMa_j≥0 for every projected point. If every support had such a representation, all supporting halfspaces would contain T_X, giving T_X=conv(X) and a finite lift.

Here N=binomial(12,4)=495, so the putative lift has size 496. The no-lift conclusion makes T_X strictly larger than C(4,12). A point outside the compact mass ball admits a strict separating linear functional. Its positive gap persists under perturbation: the change is bounded by ‖c-c′‖(‖x‖+1). A sufficiently close rational vector therefore gives a rational unnormalized failing functional. Signed coordinate wedges span the exterior space, so its maximum δ is positive. No exact δ or explicit separating point is supplied or needed for this existence argument.

### Calibration completion and the converse boundary (printed p.4)

Normalize φ=ℓ/δ. Both orientations ensure that its positive maximum equals its absolute comass, and as a constant differential form it is closed. A finite pointwise norm completion would give on unit simple vectors

\[
1-\varphi=\tfrac12(1-\varphi)^2+\tfrac12\sum_j\psi_j^2.
\]

This is an affine SOS; multiplying by δ produces the forbidden SOS for δ-ℓ. Therefore no pointwise completion exists, and a local differential-form completion is impossible at every point.

The optional converse is also sound. From 1-φ(p)=‖a+Bp‖² on the centrally symmetric spanning set X, comparison at ±p yields Bᵀa=-φ/2 and ‖a‖²+‖Bp‖²=1. A maximizing p₀ gives Bp₀=-a; its negative gives ‖a‖²=1/2. Subtracting the component parallel to a yields 2‖P_(a-perp)Bp‖²=1-φ(p)². Scaling extends the identity to all simple vectors. This is a pointwise algebraic equivalence, not a smooth-selection theorem.

## Checkable computational evidence

`fresh_controls.py` was independently written before supplied arithmetic source was opened. It uses Gaussian rationals, exterior products, a separate determinant expansion of real frames, and an exact modular rank certificate over F101. Its **126 named checks passed**:

- Reality and both exposing functionals on all 225 Hermitian basis elements; full rank 225 for the rational linear map.
- Full 495-coordinate projector identities for twelve generic rational complex frames, including nonorthogonal frames, together with phase invariance and squared-bivector-norm checks.
- All nine mixed-minor identities in eight independently generated complex matrices.
- Orientation and normalization controls, a mixed entangled projector satisfying both equations, and rational-circle controls for the affine-SOS and moment normalization identities.

These finite frames corroborate the universally reconstructed algebraic identity; they are not alone a proof of its universal quantifier. Every one of the independently constructed 225 exact columns agrees with the published certificate (`coefficient_comparison.json`).

The portable published suite also passed **48 executions**: three unchanged symbolic baselines and fifteen actual certificate faults under each of three Python optimization modes. The baselines check all 495 polynomial coordinates in 24 real variables with 11,760 nonzero coefficients after cancellation, all 25,425 upper-triangle Gram entries, both exposing functionals, and all nine mixed-minor relations. The 45 faulty runs reject their intended certificate faults. Repeated optimization modes are not counted as new mathematical examples. These are certificate mutations, not 45 distinct defects in the verifier implementation. The old UID1000 environment harness was neither executed nor simulated.

See `published_replay.json`, `published_replay.log`, `fresh_controls.results.json`, `source_pdf_comparison.json`, and `input_integrity.json`. These calculations do not reprove Fawzi, certify priority, or construct the existential failing form.

## Strongest verified claim and remaining gap

The strongest verified claim is the complete published Theorem 1: no finite projected semidefinite lift of the oriented real C(4,12), an existential rational unnormalized failing support functional for affine SOS, and a constant closed comass-one four-form on R¹² with no finite pointwise or local norm completion.

**Remaining substantive mathematical gap identified: none.** The result properly remains an application of an external established theorem. Explicit coefficients, an exact comass, lowest possible dimension, historical priority, current expert acceptance, and formal proof-assistant verification are outside what was established. The late historical-status exposure is an independence limitation, explicitly recorded rather than used as validation.
