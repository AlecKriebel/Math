# Mathematical audit for problem 30003953

## Verdict

ACCEPT the frozen candidate as a correct, complete answer to the literal printed existence question, by established prior-literature examples. The answer is affirmative in dimension 4; its limit circle is not even C¹. No novelty claim is warranted.

The candidate audited has 5,984 bytes and SHA-256 d27f424511ad03ddbf70505b1e2422d1579805622f00db7cbb2a78008b0c16b9. Its bytes were checked before the audit and were not edited. PROOF.md supplies an expanded, independently checked argument. This audit is an authored mathematical assessment, not a formal proof-assistant certification.

This reconstruction and mathematical audit were prepared with AI assistance. Independent checking here means a separate mathematical checking pass; no independent human review, external peer review, or formal proof-assistant certification is claimed. The acceptance applies to the exact printed question and is subject to the source-inspection limits stated below.

## Target and quantifiers

The original item is Tengren Zhang's Problem 10 on printed p. 2527 of Oberwolfach Reports 40/2018, PDF p. 53. Both extracted text and the rendered page were inspected. It asks for a 1-Anosov representation of a closed orientable surface group of genus at least 2 into PGL(d, ℝ), with a rectifiable limit circle failing C^{1,α}. It does not fix d or require irreducibility, Zariski density in PGL, a second-root gap, or hyperconvexity. The candidate matches every printed hypothesis. The argument actually supplies an example for each allowed genus.

The neighboring Zhang–Zimmer talk description on printed p. 2498 does not insert additional assumptions into Problem 10. The regularity under discussion is embedded-submanifold regularity. Merely showing that a chosen boundary parametrization is not C¹ would be insufficient; the candidate proves the stronger statement about the image.

## Substantive checks

1. Existence and markings: PASS. Hyperbolic pants with prescribed positive boundary lengths can be glued using the same oriented marking. Length 1 versus length 2 for one cuff gives an explicit strict marked-length difference. The associated boundary conjugacy is orientation-preserving. No use of an unproved assertion that arbitrary distinct metrics have a preferred inequality is needed.

2. Projective lift signs: PASS. Changing a determinant-one representative of either PSL(2, ℝ) factor only changes its tensor by a scalar. The multiplication ambiguity is likewise scalar. This constructs the PGL homomorphism without a coherent linear lift or an overlooked parity hypothesis.

3. First singular-value gap: PASS. For factor singular logarithms ±a₁ and ±a₂, the tensor singular logarithms are a₁+a₂, |a₁−a₂|, −|a₁−a₂|, −a₁−a₂. Thus the first gap is exactly 2 min(a₁,a₂). Cocompactness supplies a uniform linear lower bound in ordinary word length for both displacements. The proof correctly uses displacement, not translation length, at this step. The explicit Anosov constants can be taken as exp(max(C₁,C₂)) and min(c₁,c₂) in the notation of PROOF.md.

4. Applicability of the Anosov criterion: PASS. Published PSW Definition 2.3, p. 3315, uses the same singular-value ratio and word norm. Its footnote identifies the dominated-representation formulation. There is no irreducibility assumption in that definition. The representation is consequently projective Anosov before any regularity or AdS terminology is used.

5. Boundary map and dual transversality: PASS. The top eigenline of the tensor is the tensor of the two attracting lines. These identify the continuous equivariant boundary map on a dense set. The bilinear form ω⊗ω is symmetric and nondegenerate of signature (2,2). Its pairing between distinct graph lines is nonzero. Orthogonal complements give the transverse dual boundary map. The attracting dual hyperplane at δ⁺ should not be confused with the repelling hyperplane for the original action, which is the dual boundary value at δ⁻.

6. Rectifiability and charts: PASS. A monotone graph has bounded total variation on compact affine charts. More globally, the angular lifts over a period each have variation π, giving a product-graph length at most 2π. The standard Segre map preserves the infinitesimal product metric in the selected round normalization, so the same bound holds in ℝP³. Smooth metrics on compact projective space are uniformly comparable. Rotated local coordinates also show that the graph is a Lipschitz submanifold even if h is not a Lipschitz function in the original coordinate.

7. Fixed-point secant estimate: PASS. The two-sided fundamental domain is compact and avoids ∞. With r = ℓ₂(γ)/ℓ₁(γ)>1, equivariance gives |h(x)| ≤ M|x|^r and |h(x)/x| ≤ M|x|^{r−1}. This establishes a unique horizontal secant direction at the chosen fixed point. The estimate is valid on both sides of 0 and does not assume differentiability elsewhere.

8. Density and the continuous tangent-line argument: PASS. Product projective transformations preserve the globally defined horizontal distribution, independently of affine coordinate poles. Boundary minimality makes the orbit of the chosen point dense. Under the hypothetical C¹-submanifold assumption, tangent lines vary continuously, so equality with the horizontal distribution on the dense orbit forces equality everywhere. The second projection then has zero differential and is constant on the connected curve, contradicting its surjectivity. No conclusion is drawn from a zero derivative at only a dense set without also invoking continuity of the tangent field.

9. Transfer back from the Segre surface: PASS. The Segre image is a smooth embedded surface. A hypothetical C¹ embedded curve in the ambient projective space lying in that surface is C¹ in its surface charts; composing with the smooth inverse of the Segre embedding gives a C¹ graph. Thus the contradiction is about the image as a projective submanifold, not about a parametrization that might have vanishing speed.

10. Full-PGL density and higher-root results: PASS as a scope exclusion. Preserving the quadratic form prevents full-PGL Zariski density. That restriction is absent from the question. No claim of a higher-root gap or a conflict with regularity theorems under stronger hypotheses is made.

## AdS identification and its harmless sign convention

The proof does not need a convex-cocompactness theorem to establish its conclusion. Nevertheless, it agrees with the established AdS examples. Take Q = −ω⊗ω when comparing with PSW's convention that the form on a triple of boundary lines has signature (2,1). In compatible increasing affine coordinates, distinct graph lifts have negative Q-pairing. For any three points the Gram matrix has zero diagonal, three negative off-diagonal entries, negative determinant, and trace zero. It therefore has two positive eigenvalues and one negative eigenvalue. The same conclusion for any triple follows by choosing compatible affine charts avoiding it. Published PSW Definition 8.1 then identifies the projective-Anosov representation with this convex-cocompact class. Changing Q to −Q does not change PO(2,2), its null quadric, or the orthogonal hyperplanes used in the candidate. Accordingly, the candidate's choice B = ω⊗ω creates no error.

For the selected γ, the four eigenvalue-modulus logarithms are ±(ℓ₁+ℓ₂)/2 and ±(ℓ₂−ℓ₁)/2. In particular none is zero. A Fuchsian AdS representation stabilizes a timelike line and has an eigenvalue of modulus 1 on that line. Our strict length difference therefore excludes the Fuchsian case. This also explains why the exception in the rigidity theorem is inapplicable.

## Negative controls and common false variants

- If j₁ = j₂, the diagonal graph is smooth. In the fixed-point estimate r = 1 and the decay needed for the contradiction vanishes. The construction deliberately excludes this case.
- If the lengths are ordered in the other direction, the horizontal estimate is unavailable. Swapping the two factors restores it; the example has already been chosen with the desired ordering.
- For the block direct sum j₁⊕j₂, the leading logarithmic gap would be |a₁−a₂|, which can vanish. Substituting a block direct sum invalidates the uniform-gap proof. The actual construction is the tensor product.
- A derivative equal to zero at a dense set alone would not prove global constancy for an arbitrary monotone homeomorphism. The contradiction assumes a C¹ embedded curve and uses continuity of its tangent-line field.
- Rectifiability does not require that the equivariant boundary parametrization h be Lipschitz. Local rotated coordinates or arclength parametrizations are different parametrizations of the same image.

## Literature and version checks

The published PSW article is Geometry & Topology 27(8) (2023), 3303–3360, DOI 10.2140/gt.2023.27.3303, published 9 November 2023. Its publisher PDF was retrieved, hashed, text-inspected, and visually checked at printed pp. 3304, 3315, and 3344. These pages respectively support the product-Fuchsian graph example with the conjugacy exception, the singular-value definition, and the AdS regularity discussion.

There is a small but useful version distinction: arXiv 1910.06627v3's introduction gives an unqualified non-C¹ formulation for the pair of hyperbolizations, whereas the published introduction expressly excepts conjugate factors. The candidate's strict length difference already rules out conjugacy, so this is a bibliographic improvement rather than a mathematical defect. The published paper describes the product action on S¹×S¹; the independent proof makes the additional Segre/tensor passage to ℝP³ explicit.

Glorieux–Monclair's inspected arXiv version is 1809.10639v2, revised 11 November 2023. Its Theorem 1.3, PDF p. 2, states C¹ rigidity for AdS quasi-Fuchsian groups; the following proposition and §2 provide context. Publication in Mathematical Research Letters 31(2) (2024), 429–439 was independently verified from the author's publication list and the publisher's DOI landing metadata. The landing metadata gives 24 October 2024 as the publication date and DOI 10.4310/MRL.241024233904.

The journal-PDF endpoint advertised by that landing page returned a short JSON response instead of a PDF. Therefore this audit does not claim to have checked the journal PDF or exact theorem numbering in the typeset GM version. This does not block acceptance: the current public arXiv theorem was inspected, the published PSW discussion is direct supporting evidence, and PROOF.md establishes the example without relying on the GM rigidity theorem.

## Deliverables and boundaries

PROOF.md is the complete authored reconstruction. SOURCE_PINS.json records public source identifiers, URLs, byte counts, hashes, inspection locations, and the GM journal-PDF retrieval limitation. AGGREGATE_CHECKS.json reports the limited integrity and finite exact-arithmetic outcomes. ACCEPTANCE.json binds the accepted statement to the proof, audit, and supporting public metadata. MANIFEST.json pins every other member of the closed public inventory.

The public inventory contains seven files: README.md, PROOF.md, AUDIT.md, SOURCE_PINS.json, AGGREGATE_CHECKS.json, ACCEPTANCE.json, and MANIFEST.json. The executable checker and its control outputs remain outside this inventory. No source PDFs, copied third-party source text, rendered source pages, dataset contents, raw tables, scripts, private correspondence, or coordination material are included. Byte-integrity and finite arithmetic checks are not a formal verification of the general mathematical argument.
