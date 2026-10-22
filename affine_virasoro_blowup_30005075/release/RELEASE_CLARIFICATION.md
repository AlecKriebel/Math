# Release clarification: affine–Virasoro normalization

Problem 30005075 / OWR-9790367-005. Addendum dated 2026-10-03.

This addendum accompanies the unchanged author packet whose manifest SHA-256 is `6c1444e73c64c5b5a2e9eaebda234d3befb997fbf209c7522377c02b0c4bbf4a`. It makes the following points explicit following independent review. The original author files and their manifest are preserved byte-for-byte.

## Published affirmative prior work and this packet's scope

Bershtein–Feigin–Trufanov (BFT), *Highest-Weight Vectors and Three-Point Functions in GKO Coset Decomposition*, CMP 406, 142 (2025), explicitly presents its coset/AGT relation as a proof of the SU(2) surface-defect blowup relation. Its Theorem 4.5 and Eq. (4.59) are the substantive published input to this packet. The article's affirmative treatment must be credited; the intended route is not being claimed as a new solution here. [Published article](https://doi.org/10.1007/s00220-025-05318-1).

The independent audit accepts the repaired algebraic normalization, the all-integer three-point sign/norm correspondence, and the coefficient-free four-point sewing, conditional on the published Eq. (4.59) and compatible multiplicative regularization. The exact convention-specific identification of those full conformal blocks with the original gauge partition functions has **not been independently certified in this packet**. The missing local comparison concerns all four masses, the regular defect and its coordinate, and the abelian, classical and one-loop factors in all three charts.

This certification limit does not establish that the problem remains open in the literature. Nor do the corrected display mismatches disprove the underlying published theorem.

## Explicit third ordering correction: BFT (B.7)

Besides the affine-character correction in (B.4) and the aligned flux order in (B.6), the comparison requires correcting the weight assignment printed in (B.7). For periods `(e1,e2)=(1,−K)`, with `K=k+2`, the correct order for the formulas used here is

\[
(a_1,a_2,a_3)=(\lambda/2,\nu/2,\mu/2).
\]

The three slots are incoming weight `lambda`, inserted weight `nu`, and outgoing weight `mu`; their fluxes are `(l,n,m)`. The printed (B.7) assigns the second and third slots to `mu` and `nu`, respectively. Author Eq. (14) already uses the corrected order, so no change to its proof or executable checks is required. This addendum explicitly identifies that third source correction rather than leaving it implicit.

## Exact hypotheses and meaning

All algebraic coefficient identities are identities of rational functions, initially evaluated where every denominator is defined. The sewn block identity uses generic parameters with:

- nonzero **finite** highest-vector norms;
- invertible relevant Shapovalov/Gram matrices;
- `K` different from `0` and `−1`;
- in physical coordinates, `epsilon1 epsilon2 (epsilon1−epsilon2)` nonzero;
- all additional resonance/reducibility loci that obstruct the stated generic decomposition excluded.

Avoiding norm poles alone is insufficient: a zero norm also prevents the displayed inverse-norm sewing. For example, the cited norm formula gives

\[
N_1(\lambda)=\frac{K-\lambda-1}{K-\lambda-2},
\]

with a zero at `lambda=K−1` and a pole at `lambda=K−2`.

The result has **generic meromorphic-parameter, formal-conformal-block scope**. At each fixed conformal grade, only finitely many flux sectors contribute because their initial grade is `j²`. No analytic convergence theorem for the full bilateral sum, universal singular-level extension, or equality of arbitrarily chosen absolute regularizations is asserted. A degenerate specialization needs a specified common meromorphic limit and an independent justification that it exists. Infinite normalizers use the compatible multiplicative regularization assumed in the note; their finite ratios are given by the proved finite products.

## Bibliographic precision

The inspected local Nekrasov document is arXiv:2007.03646v2, dated 5 October 2021, for the work later published in AHP in 2024. It was not a separately checked 2024 publisher PDF. This does not change the target identity or the equation pointers used in the packet. [Inspected version](https://arxiv.org/abs/2007.03646v2).

## Queue interpretation

If this investigation is recorded as `unsolved` with `5/5` attempts, that label records **our incomplete exact-gauge-convention certification after this bounded investigation**. It must not be read as a claim of literature openness or absence of an affirmative published proof. The accompanying Findings entry should state:

> Published BFT 2025 affirmative coset/AGT route; independently audited normalization repair. Exact gauge-convention bridge not certified here; status records this investigation's certification only, not literature openness.

No full-resolution claim, remote publication, or queue mutation is authorized by this addendum itself.
