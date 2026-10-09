# Edition notice for the independent audit

The mathematical audit below is preserved in full from 9 October 2026. Its verdict, complete mathematical checks, source findings and substantive limitations are unchanged. Only the original frozen-input inventory and administrative description of the bounded history review have been edited. Original input and package fingerprints are omitted; the retained hashes identify raw public scholarly PDFs. This edition's [MANIFEST.json](MANIFEST.json) identifies only its included files.

The original audit passed the partial structural reduction without requiring a mathematical correction. It did not resolve the square-root question, establish novelty or certify an exhaustive literature or history search. Its source inspections are historical: packaging did not retrieve or rehash the PDFs or repeat their reading. Independent AI-assisted mathematical auditing is not human peer review, journal acceptance or formal proof-assistant verification. See [PROVENANCE.md](PROVENANCE.md) for the exact editorial boundary.

---

# Independent audit: spherical lifts and extension complexity

Problem 30004900 / OWR-8415356-006, rank 1186. Audited 9 October 2026.

## Verdict

**PASS as a partial structural reduction. The original problem remains unresolved.**

The exact-vertex-count spherical lift, its full-dimensional sign choice, projection monotonicity, the all-fixed-dimension equivalence, and the concentrated-cap corollary are valid as stated. No mathematical correction to the frozen report is required. The simplex exception and dimension-dependent constants are handled correctly. The result supplies neither a new square-root upper bound nor a fixed-dimensional super-square-root lower bound. No novelty is established or claimed.

The accepted accounting is **one completed approach out of five**. This audit checks that approach; it does not constitute a second mathematical approach. Its history assessment is limited to the accessible evidence described below.

## 1. Original audit and edition boundary

The original audit read the complete authored report, status summary, approach accounting and public-source ledger. It independently checked the original input inventory against the available bytes, found every entry matched, and left the authored inputs unchanged. The original inventory and its fingerprints are excluded from this edition; that inventory included auxiliary research evidence not distributed here. This historical integrity result is not a claim that the omitted evidence can be reproduced from this edition.

The public report in [APPROACH1.md](APPROACH1.md) contains the complete original report after an edition notice. The included mathematical audit, accepted scope and source metadata are separately identified by the edition manifest. A later mathematical change requires renewed review before reusing this acceptance.

The relevant public-source PDFs were also rehashed:

| Public source | Bytes | SHA-256 |
|---|---:|---|
| Oberwolfach Report 53/2021, official EMS PDF | 613600 | 80b960c10c23bc89b6a74a2b7e1957a65c52fa5f16b15bf5c4aa82602ad16ef7 |
| Kwan–Sauermann–Zhao, arXiv:2006.08836v3 PDF | 1420209 | 39b078238f34a2ecf72f9df5c56af39941117d31862d1706a6ea9e71683fcccc |

## 2. Source formulation and attribution

The exact target is the universal square-root upper bound for n-vertex polytopes inscribed in a common Euclidean sphere, with dimension fixed first and the constant permitted to depend on that dimension. There is no source assumption that the vertices are uniformly distributed, that the sphere center belongs to the polytope, or that the polytope is simplicial.

The auditor freshly extracted printed pp. 2927–2929 and freshly rendered and visually inspected printed p. 2929, PDF p. 37 of 62. The question and adjacent cyclic-polygon theorem agree with the report's interpretation. The contribution is Lisa Sauermann's, joint with Matthew Kwan and Yufei Zhao. EMS identifies the volume as 18 (2021), issue 4, pp. 2893–2954, with actual publication on 26 November 2022. Thus the report correctly distinguishes the volume/report year from publication year. [Official article record](https://ems.press/journals/owr/articles/8415356); [official PDF](https://ems.press/content/serial-article-files/46931).

The report's definition of extension complexity is consistent with the source. Counting facets relative to the affine hull avoids an artificial dependence on ambient equations. Affine images and linear-image extensions give the same parameter: an affine map e ↦ Ae+b can be replaced by the linear map (e,s) ↦ Ae+sb on E×{1}, which is affinely isomorphic to E and has the same facets. If “projection” is interpreted specifically as coordinate projection, a general linear image is realized by projecting the graph {(Ae,e):e∈E}, again preserving the facet count. The report's scaled coordinate map in the cap corollary is therefore permissible.

No attribution of the elementary lift to Kwan–Sauermann–Zhao or Shitov is made. The report distinguishes those authors' established results from its self-contained observation, and its explicit lack of a novelty claim is appropriate.

## 3. Projection monotonicity

**Lemma 1: PASS.** If P=L(Q) and an extension E maps onto Q by T, then the same E maps onto P by L∘T. The number of facets of E does not change. Consequently xc(P)≤xc(Q), which is exactly the direction used later.

An optimum extension may be chosen because the possible facet counts form a nonempty set of nonnegative integers. Nonemptiness follows, for example, from a simplex extension. The argument needs no slack-matrix factorization, no genericity, and no assertion comparing the facet counts of P and Q themselves. A small extension complexity for P alone would not yield an upper bound for Q, and the report does not make that converse inference.

## 4. Spherical lifting theorem

**Theorem 2: PASS.** Let v₁,…,vₙ be the distinct vertices of a full-dimensional d-polytope, with n≥d+2.

### 4.1 Real and distinct available heights

Taking R strictly larger than every vertex norm makes hᵢ=(R²−‖vᵢ‖²)^(1/2) strictly positive. Both heights ±hᵢ are real and unequal. Strictness is important: allowing a vertex norm equal to R could remove the sign-choice argument at the extra vertex. The report uses the strict inequality correctly.

### 4.2 Affine dimension and the sign choice

Full dimensionality gives d+1 affinely independent input vertices. Their positive lifts remain affinely independent because any affine dependence of the lifts projects to one of the inputs. Their affine hull H consequently has dimension d.

More specifically, projection maps H affinely and bijectively onto Rᵈ, so H is the graph of the unique affine interpolant f with f(vᵢ)=hᵢ for i≤d+1. At v_(d+2), at most one of the distinct numbers h_(d+2) and −h_(d+2) can equal f(v_(d+2)). Choose a height unequal to that value. An explicit implementation is to use the positive height if it is unequal, and the negative height otherwise. This also clarifies that no choice ambiguity arises when both heights are unequal.

The additional lift lies outside H. Hence the first d+2 lifts already have affine dimension d+1, and adding the remaining lifts cannot decrease it. Since they lie in R^(d+1), this is exactly full dimensionality. No general-position perturbation, limiting argument, or extra vertex is hidden in the proof.

The centered-square warning in the report is valid: equal vertex norms produce equal positive heights and an all-positive lift of affine dimension two. Flipping one height produces a third dimension. The sign selection repairs precisely this possible degeneracy.

### 4.3 Sphere, distinctness, and exact vertex count

For every chosen sign, ‖(vᵢ,±hᵢ)‖²=R². Thus the lifts lie on the same Euclidean sphere. Distinct input vertices remain distinct because projection distinguishes them.

For i≠j, the identity

    wᵢ·wⱼ = R² − ‖wᵢ−wⱼ‖²/2 < R² = wᵢ·wᵢ

shows that the radial functional with coefficient vector wᵢ uniquely maximizes at wᵢ among the listed points, and hence on their convex hull. Every listed point is exposed and therefore a vertex. Conversely, a convex hull of these n points has no vertices outside the generating set. The vertex count is therefore exactly n, not merely at most n.

The exposure argument holds equally for positive and negative heights and does not require the sphere center to lie in the convex hull.

### 4.4 Exact projection

Coordinate projection commutes with finite convex hulls and sends each wᵢ to vᵢ. Its image is exactly P. There is no approximation error, projective distortion, loss of original vertices, or increase of vertex count. The resulting extension complexity inequality is xc(P)≤xc(Q).

### 4.5 Simplex exception

A full-dimensional d-polytope needs at least d+1 vertices. At n=d+1 it is a simplex, while n points always span dimension at most n−1. Thus a (d+1)-dimensional lift with only d+1 vertices is impossible. The report correctly excludes this case from Theorem 2 and uses xc(P)≤d+1 instead. It does not falsely extend the dimension-raising claim to simplices.

## 5. Extremal functions and quantifiers

**Corollary 3: PASS.** The extremal functions are well-defined for the stated ranges. An n-vertex polytope is a linear image of the standard simplex {λ∈Rⁿ:λ≥0, Σλᵢ=1}, under λ↦Σλᵢvᵢ, and this simplex has n facets. Hence xc(P)≤n and both suprema are finite.

Inscribed d-polytopes form a subclass of all d-polytopes, giving I_d(n)≤F_d(n). Theorem 2 applies separately to every d-dimensional n-vertex polytope for n≥d+2 and supplies an inscribed (d+1)-dimensional example with the same n and at least its extension complexity. Taking suprema gives F_d(n)≤I_(d+1)(n). No attainment of either supremum is needed. The full inequality chain in the report is valid on its explicit range.

For each fixed d, an assumed constant C_(d+1) for inscribed dimension d+1 therefore bounds unrestricted dimension d. The one omitted vertex count is absorbed by max{C_(d+1),√(d+1)}, because (d+1)/√(d+1)=√(d+1). If a big-O estimate begins only after a larger threshold, the finitely many earlier vertex counts are absorbed using xc(P)≤n. This is legitimate dimension-dependent asymptotic reasoning.

The conclusions have the correct strength:

- The two assertions quantified over **every fixed dimension** are equivalent.
- The proof does **not** identify I_d and F_d in the same dimension.
- It provides no constant uniform across dimensions.
- Inscribed dimension three would imply the unrestricted polygon bound; the established inscribed dimension-two bound does not already do so.
- A hypothetical fixed-dimension sequence with xc(Pₙ)/√n unbounded transfers to dimension d+1 with unchanged n. A sequence whose dimension grows remains growing-dimensional after the lift and cannot refute a fixed-dimension assertion merely by this operation.

These distinctions are present in the audited report, rather than being qualifications needed to repair its claims.

## 6. Concentrated-cap corollary and its limits

**Corollary 4: PASS.** Fix 0<θ<π/2 before varying n or the input polytope. The finite set of vertex norms permits ε>0 with ε maxᵢ‖vᵢ‖<sin θ. Applying the same construction to εP with radius one keeps all heights real and positive before the possible sign flip.

Every positive lift has last coordinate

    (1−ε²‖vᵢ‖²)^(1/2) > cos θ.

On the unit sphere, this is exactly the strict angular-cap condition around the north pole. Only the singled-out index d+2 can use a negative height, so at least n−1 vertices belong to the cap. Full dimension and exposedness follow from the same earlier proof. The map (x,t)↦x/ε is linear and sends the lift exactly to the original P.

Important limits are respected:

- The construction works for each positive cap radius, however small, with a positive ε. It does not set ε=0. A limit as ε→0 can collapse vertices and dimension, but no extension-complexity assertion at that limit is used.
- At least n−1 vertices are guaranteed; the report does not claim that all n must lie in the cap.
- The STATUS summary's reference to any prescribed positive-radius cap is justified by taking a smaller radius below π/2 and using cap inclusion when necessary.
- For the upper-bound implication, the cap radius can be fixed once. A constant depending on dimension and this fixed radius would still transfer to a dimension-dependent constant. A bound with uncontrolled dependence on the individual configuration would not suffice, and is not the universal bound contemplated in the report.
- Concentration demonstrates that inscription does not itself entail uniform distribution. It does not disprove the square-root conjecture or rule out an adaptive proof handling concentrated configurations.

## 7. Established results and 2026 publication check

The auditor read the Kwan–Sauermann–Zhao manuscript's definitions and Theorems 1.1, 1.3 and 1.4 on pp. 1–4. The report correctly separates the random-sphere theorem, the universal cyclic-polygon theorem with constant 24, and the near-linear lower bound with dimension allowed to grow. The surrounding discussion explicitly motivates well-distributed-point methods, so the report's narrow methodological caution is supported. Fresh arXiv metadata verifies version 3 dated 23 March 2022; the institutional record verifies *Transactions of the American Mathematical Society* 375(6) (2022), 4209–4250, DOI 10.1090/tran/8614. [Manuscript](https://arxiv.org/abs/2006.08836v3); [publication record](https://research-explorer.ista.ac.at/record/11443).

Shitov's comparison is used in the report and was therefore checked independently. The fresh official publisher abstract states the 147 n^(2/3) facet bound and identifies *Proceedings of the London Mathematical Society* 132(4) (2026), e70137, first published 8 April 2026. The arXiv v2 record, revised 29 February 2020, states the same bound. The report's 2026 publication statement is correct. This is bibliographic and theorem-statement verification, not a new audit of Shitov's full proof; the lifting result has no dependency on that proof. [Publisher](https://londmathsoc.onlinelibrary.wiley.com/doi/abs/10.1112/plms.70137); [arXiv v2](https://arxiv.org/abs/1412.0728v2).

A direct publisher DOI-page request failed, while its official abstract page succeeded. Likewise, the OWR DOI redirect failed while the official EMS record and official PDF were available. Neither failure prevented the stated primary-source checks. The report does not label the 147 n^(2/3) result the best possible or assert that a bounded literature search excludes all stronger work.

## 8. Status, approach accounting, and acceptance boundary

The audit reviewed the available source and history checks, target-specific branch and pull-request search results, and semantic comparison. They support the limited statement that this evidence did not identify an exact authored predecessor. The neighboring unrestricted-polygon linear-lower-bound question is mathematically distinct. The audit did not redo every remote branch or recover deleted or unindexed history, so it does not upgrade the report's bounded-history assessment into an exhaustive certificate. Those supporting history records are not part of this proof-only edition.

The single spherical-lifting construction, sign selection, projection implication, and immediate cap corollary form one coherent approach. Source checks and this independent audit do not add proof attempts. The 1/5 accounting is consistent with the inspected evidence.

The report repeatedly states the correct stopping point. In particular, “original problem unresolved” means that this work has not resolved it; the accompanying literature statement is expressly bounded. Fresh targeted searches in this audit did not establish a conflicting full resolution or a novelty claim, and no exhaustive status certification is implied.

**Required corrections: none.**

**Accepted content:** the exact lift and its proved structural consequences, with the source distinctions and limitations retained.

**Not established:** a new universal bound, a super-square-root fixed-dimensional example, a solution of the source question, or originality of the elementary lift.

The frozen authored files remain unchanged. No publication, repository mutation, or QUEUE edit was performed by this audit.
