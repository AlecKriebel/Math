# Independent audit: Ricci-flow dimension threshold

Problem 30000789 / OWR-1588-003, rank 815. Audit date: 2026-10-06.

## Verdict

**Accept the scoped partial mathematics, with the separate source clarification below. The threshold problem remains unsolved here after five substantive approaches.** No defect was found in the exact cone criterion, even-dimensional necessity, obstruction for dimensions 4–11, diagonal local maximum, or the four specified mixed-pencil certificates. This is an independent mathematical and executable audit, not formal proof-assistant certification or human peer review.

The audit does not upgrade the missing global bound to a theorem. In dimension 12 the remaining condition is beta_12^2 <= 55/36. In every larger even dimension the corresponding non-strict sharp inequality is needed; in every odd dimension at least 13 the strict inequality is needed. Solving only dimension 12 would not establish the proposed all-dimensions threshold.

## 1. Transport, identity, and full-record review

The original 26,608-byte, 16-member author ZIP matches SHA-256 `899b09e6754a8d8473be07c3b12a20817f90c2ecf777be48e9e2d1f32bbef491`. Its 2,314-byte manifest matches the externally supplied anchor `76c2f50b88d9270c9a0c76e3e7774d3f863b29dd9fa6e1eeeeb4a73632f2cbda`.

All three complete supplied corpus files were hashed, parsed, and matched to the recorded counts and byte sizes. The target's complete record and absent-report value were reselected from the full files. Default sorted JSON serialization of [record, {}] reproduces exactly 3,982 bytes and SHA-256 `a666de9756585166e72a1d850a28d02cd7b1a195a7f17583cbf19d546f991d24`. The catalog identity, rank, and review hash agree. These datasets are not distributed in this audit.

The frozen author archive is preserved byte for byte as `AUTHOR_FREEZE.zip`. Editorial corrections are additive and separate; neither the original archive nor its extracted files was rewritten.

## 2. Necessity, sufficiency, and the scalar-zero locus

I independently derived the boundary condition with operator Hilbert–Schmidt norm, I of squared norm N=n(n-1)/2, Ric(R)=(n-1)a id+S, and Q=R^2+R#. The scalar equation is a'=(n-1)a^2+|S|^2/[n(n-1)]. Orthogonal Weyl projection gives the S-dependent Weyl term P_W(S wedge S)/(n-2). Trilinear symmetry eliminates the mixed terms paired with W.

On the positive-scalar boundary, setting S=0 forces the Weyl-cubic upper endpoint; scaling arbitrary S forces the Ricci lower endpoint. Independence of S and W is valid because this cone imposes no restriction on traceless Ricci curvature. Conversely, the two endpoint inequalities separately control the cubic and quadratic groups. There is no assumption that a common pair maximizes both.

At a=W=0, S is still arbitrary. The tangent cone requires ||dot W|| <= sqrt(cN) dot a, rather than merely a nonpositive derivative of a squared defining function. Substitution of the exact apex velocity yields the same lower endpoint. The included independent code checks this velocity directly on three non-diagonal algebraic examples and symbolically checks endpoint agreement.

The cone is a closed convex second-order cone times a vector space; the locally Lipschitz polynomial ODE satisfies the tangent-cone criterion throughout its maximal existence interval. Thus the stated equivalence L_n <= c <= U_n is accepted, including the non-smooth locus. The algebraic argument does not require compactness of the cone. Compactness is used correctly only for the finite-dimensional unit spheres defining the extrema.

## 3. Ricci estimate and low-dimensional obstruction

The fourth-moment formula follows from orthogonal scalar/Ricci/Weyl decomposition and is consistent with the independently implemented projection. Equality in the Cauchy–Schwarz lower bound on the fourth moment requires equal absolute eigenvalues. Trace zero permits this in even dimensions and excludes it in odd dimensions. Compactness makes the odd inequality strict; the argument does not claim an unevaluated odd extremum is sharp.

The balanced two-block Weyl model has Q(V)=(n-1)V and the claimed norm. In even dimensions it supplies the upper restriction complementary to the exact lower endpoint, forcing c=n/(n-2). The embedded self-dual H has eigenvalues 4,-2,-2 on its self-dual block, vanishes on the opposite block, has squared norm 24, and satisfies Q(H)=6H. Its squared cubic ratio is 3/2 in every embedding dimension. No n-dependent tensor/operator norm factor has been lost.

The exact necessary intervals are incompatible for all dimensions 4–11. At n=11 the endpoints are 2662/2187 and 40/33, with positive gap 122/24057. At n=12 the same witness has ratio 54/36, one thirty-sixth below the target. It is not a counterexample there.

## 4. Local maximum and pencil scope

The four stated diagonal eigenspace families have the claimed dimensions and eigenvalues. Their sum is n(n-3)/2, with the radial direction removed on the norm sphere. At n=12 this is a 54-dimensional linear subspace and a 53-dimensional tangent space. The one-third constrained Hessian eigenvalues are -11 (18), -77/5 (25), and -11/5 (10).

In addition to replaying the author's characteristic-polynomial test, I derived the diagonal cubic as a sum of edge cubes and triangle products, restricted its Hessian to the kernel of the row-sum and radial constraints, and obtained an exact LDL factorization with all 53 diagonal pivots negative. This independently verifies strict diagonal local maximality. It does not cover the full 1,638-dimensional Weyl space or distant maxima.

For each of the four ordered coordinate embeddings, I directly computed Q(V+H)-Q(V)-Q(H) through Lie brackets. This verifies both mixed cubic coefficients, not just a polynomial formed by assuming them. The three distinct overlaps and the residual-quadratic discriminants match the frozen results. Positive leading coefficients and negative discriminants give all-real-parameter quartic positivity. Homogeneity covers the full two-dimensional spans, including pure H. Nothing here covers arbitrary four-plane rotations or multiple simultaneous perturbations.

## 5. Sources and required clarification

The [2007 report](https://publications.mfo.de/handle/mfo/3018), pp. 1878–1879, was reread and page 1878 visually inspected from the hash-matched local PDF. Its repeated even parity and scalar-to-interval equality are genuinely printed. Interpreting part (b) as odd with interval membership remains an inferred repair, not an official erratum.

**Source clarification:** the [2008 report](https://ems.press/content/serial-article-files/46179), p. 1942, defines strict C_d but states its preservation theorem for the closure, overline(C_d). The frozen note mentions the strict definition without recording the overbar in the theorem. A fresh local rendering confirms it. The closed cone corresponds exactly to c=2n(n-1)/d^2. What prevents substitution for the 2007 assertion is the distinction between PDE sufficiency and ODE equivalence; necessity for PDE preservation is separately conjectural. `CORRECTIONS.md` and `corrections.patch` provide the replacement paragraph.

The [Beitz thesis](https://noah.nrw/ulbmshsnoah/content/titleinfo/4277665), Remark 6.3.15 and Lemma 6.3.16, was checked in the hash-matched text. The [Xu preprint](https://arxiv.org/html/2412.13633v1) and [published metadata](https://doi.org/10.1007/s12220-025-02158-2) confirm the cited near-round result. At n=12 its parameter range starts at 35/12 and does not reach the central-cone endpoint zero. The live arXiv history showed only v1; the published full text was not audited. The live aggregator could not be read. A bounded fresh search located no source establishing the requested threshold; this is not exhaustive literature clearance.

## 6. Executable audit

The author harness reran successfully from the frozen extraction: four positive normal/optimized and original/relocated package replays; 24 package-integrity rejections; byte-for-byte reproduction of its saved integrity report. Each mathematical replay reports 85,363 exact checks and five mathematical negative controls. Most of that large count consists of componentwise identities, not independent global cases.

The auditor's checker imports no author code and uses the so(n) structure constants with 2-by-2 minors to compute Q#, rather than the author's four-index Q formula. It performs 69 named aggregate checks and four mathematical negative controls. Independent normal, optimized, and relocated checks and deliberate code mutations are documented in `audit_replays.json`. Both programs use explicit exceptions, not Python assert.

Reproduce the new checker with Python 3 and SymPy: run `python -B independent_check.py` and compare stdout with `independent_results.json`; run `python -B audit_harness.py` for the four-location/mode checks and ten mutation rejections. The observed environment is Python 3.12.14, SymPy 1.14.0.

Transport controls do not defeat an attacker controlling the verifier or interpreter. The external archive and manifest anchors remain necessary. Finite diagnostics do not prove the remaining universal optimization statement.

## 7. Acceptance boundary

Accepted: the complete tangency reduction, sharp even Ricci endpoint, strict odd Ricci margin, all-dimensional explicit model formulas, dimensions 4–11 obstruction, diagonal local maximality, and exactly the four stated pencils. Accepted status: `unsolved_here`, five of five approaches used. Source correction: explicit 2008 closure.

Not accepted as established: n_0=12; a global extremizer classification; the full Weyl-space inequality at n=12 or higher; novelty; exhaustive absence of prior work; any converse PDE statement; or any noncompact Ricci-flow theorem. No remote mutation, publication, or outreach was performed.
