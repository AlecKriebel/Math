# Source scope and attribution

## Exact original target

The pinned record is 30006576, OWR-14299907-001, rank201. Its full source is [Oberwolfach Report5/2026, DOI10.4171/OWR/2026/5](https://ems.press/content/serial-article-files/53599), Praetorius's contribution *Odd behavior of even geometries*, joint with Hardering and Zavalani, printed312–313. The report concerns smooth two-dimensional surfaces in R³, piecewise degree-k geometric parametrizations on refined reference triangulations, and weighted consistency estimates. Its displayed even-k curvature term has order h^k despite a pointwise h^{k-1} bound. The requested internal mesh characterization is broader than the sufficient mirrored-pair argument already outlined in the source.

The source's distance notation is abbreviated. The later full paper defines signed distance; the present result uses only Gaussian curvature and does not infer a signed cancellation statement for unsigned distance. Likewise the original smooth test-field assumptions and displayed weaker norms are not silently treated as a full Sobolev-extension theorem for every geometry. Our graph-patch estimate is proved directly for its stated W^{1,1} weights.

The pinned prior report is null. Current queue, prior state/history, all-ref attempt paths, related-target groups and176 all-state PRs were checked at the initial gate. No prior Alec/campaign attempt or exact duplicate was found. No shared queue or historical review was edited.

## Precise later sufficient theorem

[Hardering–Praetorius–Zavalani, arXiv2607.29466v1](https://arxiv.org/abs/2607.29466v1), submitted31July2026, is a full primary preprint absent from the imported triage. The author research page lists the work as submitted. No final journal publication or comprehensive priority search is claimed.

The following portions were checked in the complete paper:

- Section2: a fixed smooth macro parametrization, standard barycentric Lagrange interpolation, full-rank geometry, and the distinction between the parametrization lift and closest-point lift
- Definition2.7, printed p.7: symmetric triangles meet only at a vertex and are centrally reflected about it
- Lemma2.8 and Definitions2.7–2.10: red-refinement pair decomposition with an unpaired boundary strip; this is not a theorem for arbitrary shape-regular meshes
- Theorem3.2 and Corollary3.3, pp.10–12: leading Taylor-moment cancellation and weighted derivative estimates
- Lemma4.3 and Corollary4.4, pp.25–26: the Weingarten and Gaussian-curvature estimates, with the quadratic curvature remainder controlled by h^{2k-2}<=h^k for k>=2
- AppendixB, pp.38–40: projected refinement is not directly a fixed smooth macro parametrization; a compatible smooth interpolation parametrization is not constructed. Newest-vertex-bisection experiments have less transparent pairs and unmatched-region boundaries, without the main theorem's established decomposition

Consequently the later paper answers substantial sufficient-analysis questions but does not itself provide the requested complete necessary mesh characterization. Our tensor-moment formulation and finite rotation averaging use the same established Taylor-cancellation mechanism, with a restricted graph geometry and a different local symmetry. No novelty is asserted.

## Surface Stokes connection

The complete author preprint [Hardering–Praetorius, arXiv2309.00931](https://arxiv.org/abs/2309.00931) was checked at its geometric definitions, equation(9) and Remark2.4. It defines elementwise Gaussian curvature and formulates the appropriate curvature-consistency bound; its Remark2.4 describes the improved even-degree exponent as numerical evidence. The work subsequently appeared in *IMA Journal of Numerical Analysis*45(5)(2025),2948–2987, [DOI10.1093/imanum/drae080](https://doi.org/10.1093/imanum/drae080). We do not claim a line-by-line comparison with the final typeset version. The July2026 paper explicitly supplies its later proof under symmetric-mesh assumptions.

The original source credits Chien, *Numerical evaluation of surface integrals in three dimensions*, *Math. Comp.*64(210)(1995),727–743, for earlier interpolation/surface-integration cancellation. The 2026 paper also cites Zavalani–Shehu–Hecht's 2024 integration analysis, [arXiv2301.02996](https://arxiv.org/abs/2301.02996). The complete v2 integration preprint was recovered and checked at Definition3.1 and Theorem3.3, pp.5–7: it explicitly assumes symmetric triangle pairs with O(h^{-1}) unmatched triangles. Its integral uses an interpolated smooth integrand together with an interpolated surface; that is not automatically the discrete intrinsic Gaussian curvature in our local criterion. These are antecedents of the parity mechanism, not newly discovered results. Chien's entire proof was not independently audited here.

## Precisely bounded contribution

Theorem1 of `PARTIAL.md` characterizes cancellation only for all smooth graph jets on a fixed shrinking patch. Theorem2 gives a regular odd fan with no source-defined mirrored pair. The degree3 radial-quartic calculation distinguishes the even-degree cancellation from a universal consequence of rotation symmetry. The conditional fixed-domain estimate explicitly assumes a uniform patch decomposition; no global family made from odd regular fans is constructed.

The original global necessity question, projected-refinement and newest-vertex-bisection explanations, closest-point transfer, other geometry terms, and a full closed-surface Stokes theorem are not settled by this package. Recommended original status is **unsolved, 1/5**. The finite exact checks certify polynomial identities and rotation-character cancellations, not these remaining global assertions.
