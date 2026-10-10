# Independent adversarial audit: 30000750 / OWR-1537-002

Audit date: 2026-10-04 UTC. Reviewer: independent audit worker, no helper agents. Review scope: frozen seven-file release, exact source match, theorem-to-target deduction, boundary cases, finite controls, and explicit external-proof dependency. No remote writes were made.

## Verdict

**PASS for the exact deduction from the published theorem; recommend `already_solved`, 1/5, with no novelty claim.** Correct the malformed mathematics in the release's `PROOF.md` before publishing. The correction is editorial and does not change the claim or proof. A separate corrected copy and patch are supplied; the original release is preserved.

This is **theorem-dependency acceptance**, not a claim to have independently re-proved every line of Dobrowolski's theorem. Full-text inspection found a concrete printed linear-algebra defect in the external proof. Its local algebraic repair and regularity can be checked, but this audit does not silently promote that repair to a certified complete erratum. The precise boundary is below.

## Frozen input and integrity

Release manifest SHA-256:

`0ac9abb79cc743ff1a3ff162a757f4e59954460c874f45e05f6355efdad112fc`

All seven entries passed `sha256sum -c SHA256SUMS` before and after the audit. The manifest hash also remained unchanged. The source PDF hashes agree with the release provenance:

- Original report: `cbdfd81df599e91411f45db8f939b6f25ade11b87e9e7878844040b428d8cd0c`
- Dobrowolski paper: `98bdaf7f0670c8c0ba63b2e986a25bcb25ea80ab6b8a0f6e4798910603ec0d69`

The private PDFs and page images are read-only source evidence, excluded from the audit delivery manifest. Do not distribute them as part of the release.

## Exact original target

I read the pinned problem record in full, visually checked printed p. 1136 of the original report (PDF page 22), and independently opened its publisher URL. The actual question has:

- `t` real and in the closed interval `[-2,2]`;
- every real polynomial `P`, without monicity, integrality, degree, or irreducibility restrictions;
- reduced length defined using real monic polynomial multipliers `Q`;
- coefficient length, and multiplicative Mahler measure;
- the one inequality for `(x²+tx+1)P`.

The nearby cubic computation discussion is background, not an additional part of this problem. The report year is 2007, consistent with its DOI, despite the catalogue citation's parenthetical 2008.

Original source: https://ems.press/content/serial-article-files/46108 ; DOI https://doi.org/10.4171/owr/2007/21 .

## External theorem: verified scope and proof location

Theorem 2.1 on printed p. 454 of the publisher-hosted full paper has the needed complex-coefficient scope and a unit-circle zero hypothesis. It imposes no degree, monicity, integrality, irreducibility, or simple-zero restriction. The source was inspected beyond the statement: §3.1, pp. 455–458, contains its induction argument; §3.2, pp. 458–463, proves the central deformation lemma. The auxiliary height bound, invariance, continuity, compactness, perturbation, and real ODE are its proof ingredients. The special hypotheses of that lemma are reductions internal to the proof, not extra hypotheses on Theorem 2.1. This is therefore not reliance on an abstract or on the multivariate corollary.

Publisher full text: https://www.impan.pl/shop/en/publication/transaction/download/product/82795 ; DOI https://doi.org/10.4064/aa155-4-8 .

The 2024 article's historical discussion and reference 21 corroborate later recognition of this paper; they are not independent proof certification: https://aif.centre-mersenne.org/item/10.5802/aif.3611.pdf . Targeted searches did not locate an erratum or retraction. That negative search result does not establish that the printed proof is error-free.

## Deduction and adversarial checks

For `A_t=x²+tx+1`, its roots have modulus one throughout the closed interval. At `t=-2` and `t=2` the factors are `(x-1)²` and `(x+1)²`. Thus `M(A_t)=1`.

For every nonzero real `P` and every real monic `Q`, `F=A_tPQ` is nonzero and has a unit-circle zero. The published theorem gives

`L(A_tPQ) >= 2M(A_tPQ) = 2M(P)M(Q) >= 2M(P)`.

Every quantifier here is necessary: the theorem must be applied after adjoining an arbitrary multiplier. A bound merely on `L(A_tP)` would not prove the reduced-length claim. Monicity of `Q` ensures `M(Q)>=1`; its roots are allowed outside the disk. No normalization of `P` is needed, including when its leading coefficient is negative or has magnitude below one. Real polynomials are within the theorem's complex domain; no equality of real and complex reduced lengths is asserted.

Taking the infimum preserves the uniform lower bound. The admissible set is nonempty, and the proof uses neither attainment nor a degree bound on multipliers. The degree-zero monic polynomial is 1; even if a positive-degree-only convention were adopted, multiplication by `x` preserves both coefficient length and measure, so this convention would not change the result or sharpness examples.

`P=0` is explicitly handled under the stated extension `M(0)=0`. If Mahler measure is defined only for nonzero polynomials, the nonzero assertion is unchanged and the zero case is a conventional extension, not an application of the theorem. Constant nonzero `P`, zero roots of `P` or `Q`, repeated roots, and `t=±2` cause no gap. Products cannot cancel polynomial zeros.

The constant 2 is sharp for real nonzero `c`, `P=cx^m`, `t=0`: the matching upper bound follows from `Q=1`. This proves existence of equality cases only; it does not classify all of them.

### Supplementary endpoint nonattainment check

For `n>=2`, define

`Q_n(x) = (1/(n-1)) sum_{k=0}^{n-2} (k+1)x^k`.

This is monic and direct multiplication gives

`(x-1)²Q_n(x) = x^n - (n/(n-1))x^(n-1) + 1/(n-1)`.

Its coefficient length is `2n/(n-1)`, tending to 2. Combined with the published lower bound, this proves the reduced length equals 2 for `t=-2, P=1`. Yet no admissible multiplier attains 2: if monic degree-`n` `F` had `F(1)=F'(1)=0` and `L(F)=2`, equality in the coefficient triangle inequality would force every lower coefficient to be nonpositive real, with their absolute values summing to 1. Then `F'(1)>=n-(n-1)=1`, a contradiction. Replacing `x` by `-x` and adjusting the overall sign to preserve monicity proves the analogous statement at `t=2`.

This supplementary diagnostic is not needed for the main deduction. It demonstrates why the release's refusal to assert general attainment is important.

## External proof printing defect and dependency boundary

The source defines a complex matrix `M` of shape `d × (d-1)` and full column rank. Its printed expressions (3.12) and (3.13) use `(M^T M)^(-1)y` with `y=v(p(v_m)/P_0)` of dimension `d`. As printed, the multiplication is dimensionally undefined. In addition, complex full column rank does not imply invertibility of the ordinary-transpose Gram matrix. A concrete example is

`M = [[1,0],[i,0],[0,1]]`,

which has rank 2, but `M^T M=diag(0,1)`. Its Hermitian Gram matrix is `M* M=diag(2,1)`.

For a compatible right-hand side `y` in the image of `M`, the unique solution of `MX=y` is

`X = (M* M)^(-1) M* y`,

where `*` denotes conjugate transpose. The dimensions are `(d-1)×d` times `d×1`, and `M* M` is positive definite because `u*(M* M)u=||Mu||²>0` for nonzero `u`.

**Regularity check.** On the full-column-rank locus this corrected left inverse is rational in the real and imaginary parts of `M`, with nonzero denominator `det(M* M)>0`, and hence is smooth. The matrix entries in the source construction are polynomial in the real and imaginary parts of the factor coefficients. Coefficient phases `a_j/|a_j|` are smooth where the chosen coefficients remain nonzero. The fixed two-index phase system used to define `v_m` is invertible on a sufficiently small neighborhood of its initial point. These facts preserve the real continuous differentiability needed by a local real ODE. No holomorphic dependence is claimed or needed; conjugation would generally prevent it.

**Limit of this repair.** The identity `MX=y` follows from the repaired formula only when `y` belongs to the image of `M`. For arbitrary `y`, `M(M* M)^(-1)M*y` is the orthogonal projection of `y`, not necessarily `y`. The source obtains compatibility using its stationarity condition (3.10). Replacing the printed inverse alone does not independently establish all stationarity/continuation assertions along the ensuing trajectory. This audit certifies the local algebra and regularity repair, not a complete reconstruction of that deformation argument. It therefore does not assert that the source proof has been independently certified line by line. No counterexample to the published theorem or to the target deduction was found. The accepted external theorem remains the explicit dependency.

## Reproduction and finite evidence

The frozen check script was read and rerun. Its output matches the frozen JSON byte for byte: 21,420 product inequalities, 27 sharpness cases, one zero case, and two hypothesis-deletion negative controls. The root-based exact Mahler measures used in those controls are valid. The count is `17×126×10=21,420`.

A separate dictionary-convolution implementation adds 6,656 exact rational product checks using higher-degree root products, nonmonic and negative scalings of `P`, inside/outside roots of `Q`, conjugate quadratic factors, interval endpoints and parameters close to them. It also verifies the two endpoint approximant identities for every degree 2 through 64, totaling 126 checks. All pass. Neither suite is a universal proof, an exhaustive counterexample search, or a reduced-length solver.

## Corrections and release recommendation

1. Replace malformed display expressions such as `L$F$`, `M$F$`, `M$A_t$`, `M$Q$`, and `\\ell_{\\mathbb R}$F$` with ordinary function notation inside the existing math delimiters. The separately supplied corrected proof and unified diff perform only these replacements.
2. Retain the explicit external-theorem dependency and the no-novelty classification. Do not upgrade the wording to an independent proof certificate for the entire 2012 paper.
3. Preserve this audit, including its precise source-proof caveat, separately from the frozen historical payload. No source PDFs or page images should be published.
4. The proposed queue disposition `already_solved`, 1/5 is mathematically supported by the cited theorem and exact deduction. I did not re-audit live repository state or perform a remote publication action; those remain the parent's responsibility.

Audit completion estimate: 100% of the requested theorem-to-target and package audit, with the stated boundary on independently certifying the external paper.
