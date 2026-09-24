# Supplied-paper priority review: Matsuzoe (1999)

**Finding:** this paper does not state a prior answer or counterexample to FMU (1998), Question 3(e). It does contain established curvature criteria and **the exact transformation used in the proposed non-self-dual extension**. Combined with the classical Riemannian Gauss lemma, these earlier tools readily imply the proposed negative answer. Closing this full-text gap therefore improves the bibliography; it does not certify a first resolution or make the construction itself new.

## Source and coverage

Hiroshi Matsuzoe, *Geometry of contrast functions and conformal geometry*, Hiroshima Mathematical Journal **29** (1999), 175–191. [DOI: 10.32917/hmj/1206125160](https://doi.org/10.32917/hmj/1206125160). The first page records receipt on October 27, 1997, and revision on March 18, 1998.

- Supplied file: `Download.pdf`.
- SHA-256 independently checked: `a10835acdc04536bfacb9a4c2698a5ce7d5546fd7f48cf8af4ff708baeda2bea`.
- Read the complete extracted text and visually inspected **all 18 PDF pages**: printed pp. 175–191, followed by one blank page. The visual inspection corrected missing formulas and OCR errors, including `≥` misread as `>`.
- Extraction: `tmp/priority_supplied_pdfs/download.txt`; rendered pages: `tmp/priority_supplied_pdfs/matsuzoe1999_agent/page-01.png` through `page-18.png`.
- 2026-09-24 04:13:41 UTC: started the supplied-source review; 10% complete.
- 2026-09-24 04:15:57 UTC: complete text and visual coverage achieved; theorem comparison complete; 90% of this bounded review complete.
- 2026-09-24 04:17:20 UTC: comparison and report completed; 100% of this supplied-source review complete, with the separate priority gaps stated below.

The percentages concern completion of this source review, not confidence in worldwide priority. No individual was contacted. The PDF was treated only as a mathematical source.

## Theorem-level comparison

| Location | Verified content relevant to the candidate | Consequence for the priority audit |
|---|---|---|
| §1, pp. 176–177; discussion before Corollary 5.2, p. 190 | A statistical structure has a torsion-free connection with symmetric covariant derivative of its metric. Duality is the same identity used in the candidate. The paper explicitly includes a Riemannian metric with its Levi–Civita connection and notes self-duality. | No hidden requirement excludes the candidate's Levi–Civita example. |
| §2.1, p. 178, equation (2.1) | Projective equivalence is `∇̃_X Y = ∇_X Y + τ(Y)X + τ(X)Y`. With `τ=dψ` and `h̃=e^ψ h`, this is statistical `(-1)`-conformal equivalence. The projective curvature tensor is invariant; for `n≥3` and symmetric Ricci, its vanishing characterizes projective flatness. | This includes dimension **three**, despite the OCR. The candidate's deformation is precisely the substitution `ψ=t`. |
| §2.2, pp. 178–179, equations (2.2)–(2.3) | The change `∇̃_X Y=∇_X Y−h(X,Y)α♯`, with `α=dφ` and `h̃=e^φh`, is statistical `1`-conformal equivalence. A dual-projective curvature obstruction is given; for `n≥3`, the paper identifies statistical 1-conformal flatness with dual-projective flatness. | This is the candidate's convention, and gives an earlier curvature route to its obstruction. |
| Proposition 3.1, pp. 182–183; Corollary 3.5, pp. 185–186 | Characterizations by centroaffine realizations, followed by construction of a contrast function on a conformally-projectively flat structure. | These are hypotheses about realizations and conformal-projective flatness; they are not conclusions from radial orthogonal integrability. |
| Theorem 4.1, pp. 186–187 | For `n≥3`, symmetric Ricci, and a simply connected statistical manifold, projective flatness is equivalent to existence of an inducing contrast function whose Bartlett tensor satisfies `B(X,Y)Z=−Ric(Y,Z)X/(n−1)`. Theorem 4.2, pp. 187–188, gives the dual-projective counterpart. | A very specific fourth-order tensor condition is essential. Existence of a contrast function, or integrability of level hypersurfaces, cannot replace it. The final paragraph on p. 191 gives the local formulation without simple connectivity. |
| §2.4, p. 180; Theorem 5.1, pp. 188–190; Corollary 5.2, pp. 190–191 | Conformal-projective equivalence permits two independent functions. Theorem 5.1 computes Bartlett tensors for the resulting geometric divergences. Corollary 5.2 characterizes ordinary Riemannian conformal flatness in dimensions `n≥4`. | Ordinary metric conformal flatness and statistical 1-conformal flatness are explicitly different notions. Corollary 5.2 neither applies directly to the three-dimensional example nor proves the implication in Question 3(e). |

There is no discussion of radial connection-geodesics, their orthogonal distributions, or the all-centers integrability condition. The occurrences of “radial” on pp. 181 and 183 refer to position vector fields in ambient affine spaces used in centroaffine immersion theory. They are not the distributions in the question. The complete paper contains no `S²×R` example, explicit resolution of Question 3(e), or citation of the FMU problem list. The acknowledgement of Urakawa on p. 176 is general and does not identify this question.

## Direct application of the earlier formulas

The following is this review's application of the paper's formulas, **not a counterexample stated by Matsuzoe**.

For the candidate product Levi–Civita structure, choose the usual orthonormal frame with sphere directions `e₁,e₂` and line direction `e₃`. Its Ricci operator is `diag(1,1,0)` and scalar trace is `γ=2`. Section 2.2 defines

\[
M=-\operatorname{Ric}^{\sharp}+\frac{\gamma}{n-1}I,
\qquad
W_{DP}(X,Y)Z=R(X,Y)Z-h(Y,Z)M(X)+h(X,Z)M(Y).
\]

Thus `M=diag(0,0,1)` and

\[
W_{DP}(e_1,e_2)e_2=e_1\ne0.
\]

Consequently this structure is not 1-conformally flat. The independent projective formula on p. 178 also gives `W_P(e₃,e₁)e₁=−e₃/2`. Self-duality makes these obstructions applicable to the conclusion sought in Question 3(e).

The radial-integrability half comes from the classical Gauss lemma/first variation of squared distance, not from a new theorem in this paper. Adding that classical fact supplies the whole Levi–Civita counterexample using prior machinery.

For the non-self-dual extension, set `ψ=t` in equation (2.1) and the accompanying metric change. This gives exactly

\[
h_1=e^t h_0,\qquad
\nabla^1_XY=\nabla^0_XY+dt(X)Y+dt(Y)X.
\]

Projective equivalence preserves unparametrized geodesics and conformal metric change preserves orthogonality, so their combination preserves the local radial distributions. The same projective curvature obstruction persists. Hence the non-self-dual construction is a standard `(-1)`-conformal deformation of the Riemannian example. It should not be described as a newly discovered deformation mechanism; this paper gives a directly checkable older citation, in addition to Kurose's already-reviewed foundational work.

## Priority conclusion and remaining scope

The previous statement that the Matsuzoe 1999 contrast-function paper was unread is superseded **for this supplied file**. The accurate source-specific conclusion is: **fully inspected; no explicit earlier answer found; substantial underlying theory and the exact deformation already present**.

Some assertions about automatic symmetry of Ricci in §2 are attributed to reference [9], which the bibliography identifies as **Kurose, “Private letter.”** It is not the published Kurose 1999 realization paper. The content of that correspondence beyond what is stated here remains unseen; no inference about an unpublished answer is justified.

The companion reviews now close the Matsuzoe 2010 and Kurose 2023/2024 full-text gaps; see the [combined update](priority_supplied_papers.md). Kurose 1999, Binder–Simon 2000, and the unseen Kurose 2016 talk remain uninspected. This paper's silence cannot certify the absence of a solution elsewhere. The warranted presentation remains a short, attributed counterexample to the printed implication, with historical priority left unconfirmed.
