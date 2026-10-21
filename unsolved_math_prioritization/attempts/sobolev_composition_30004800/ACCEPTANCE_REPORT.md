# Mathematical acceptance report: Fourier-envelope composition

Audit date: 2026-10-21 UTC.
Catalogue identifier: OWR-8415343-001; record 30004800.

## Disposition

**Existing attributed solution; accepted within the explicitly stated mathematical scope below.**

Alper Ferudun's October 9, 2026 manuscript supplies a valid proof of the intended smooth-composition inequality posed by P. T. Chrusciel. This is not a new solution by the reviewers. The manuscript identifies itself as an unrefereed preprint. This mathematical audit does not confer journal peer review, establish community consensus, or assert priority beyond the identified source.

## Exact accepted statement

Let s>1 and let G:R->R be smooth with G(0)=0. On the square torus of side 2pi, use the orthonormal Fourier basis (2pi)^(-1) exp(i l.x), indexed by l in Z^2. For a real-valued family phi(t), write phi_l(t) for its Fourier coefficients and define

N_s(phi) = sum_{l in Z^2} (1+|l|)^(2s) sup_t |phi_l(t)|^2.

There is a finite C_2 depending only on G and s such that

N_s(G composed with phi) <= C_2 N_s(phi)

whenever N_s(phi)<=1. The index set may be an arbitrary nonempty set, in particular the time interval in the original question. The result needs no continuity or measurability in the parameter. Fourier representatives are continuous in the spatial variable under the norm hypothesis. The extra original condition of a first-order zero is covered, although only G(0)=0 is needed.

The supremum is inside the sum and the homogeneous input factor is present. Neither replacing the left side by a supremum of Sobolev norms nor replacing the right side by an absolute constant would be an adequate substitute for this target.

## Source normalization qualification

The original printed exponential basis uses N^2 rather than Z^2 and displays coefficient squares without modulus signs. Full integer indices and absolute squares are the coherent full-Fourier interpretation. This acceptance explicitly adopts that interpretation; it does not describe it as an authenticated author erratum.

If the printed quadrant-only indexing is instead required literally, the resulting assertion is false. For nonzero A and B, phi=A cos(x1-2x2)+B cos(2x1-x2) has no Fourier coefficient in the nonnegative quadrant, whereas G(phi), with G(u)=u+u^2, has a nonzero (1,1) coefficient. This notation issue must not be concealed when describing the scope of the positive answer.

## Verified proof dependencies

The substantive audit covers the manuscript's Sections 2–6: the elementary envelope and lattice estimates, the exponential bound of Theorem 1.1, the measure-representation estimate of Theorem 1.2, and the smooth-composition conclusion of Corollary 1.3(b).

The key steps have been re-derived:

- The weighted envelope controls absolute Fourier convergence and admits a uniform small l^1 tail, since s>d/2.
- A uniform frequency split makes the high-frequency exponential controllable by a convolution majorant without assuming a small weighted l^2 tail.
- The low-frequency real input produces a unimodular exponential. Its Fourier derivative recurrence gives a polynomially decaying coefficient envelope beyond a controlled radius.
- Weighted convolution estimates combine the two parts to obtain a polynomial bound in the exponential parameter, uniform over all families in the norm ball.
- The difference of an exponential and 1 carries one explicit input factor. Scalar Fourier coefficient integration, followed by the coefficientwise supremum and weighted Minkowski inequality, preserves that factor and the correct order of supremum and summation.
- A smooth compactly supported extension of G on the bounded attained range has enough Fourier decay to integrate the polynomial bound. The finite-regularity criterion k>M+3/2 and its constants were also checked.
- The normalized-Haar coefficient convention in the proof differs from the original orthonormal convention by 2pi. The relation N_s=4pi^2 ||.||_X^2 yields the exact unit ball and the squared final constant.

The accompanying independent review details these checks and the relevant endpoint restrictions. No gap was found in this dependency chain.

## Limits and residual questions

The accepted conclusion is the functional inequality, not an independently verified Einstein–Maxwell existence theorem. Sharp minimal smoothness and optimal growth exponents in the lower-regularity range remain additional questions, not missing steps in the original smooth-G conclusion. The ancillary lower-bound results in Sections 7–9 and a comprehensive literature-priority determination are not certified by this acceptance. Real-valuedness is essential to the unimodularity step; complex inputs cannot be substituted without the separate real-coordinate argument.

## Public sources and exact inspected inputs

Original question: P. T. Chrusciel, Quo Vadis, Mathematical GR?, Oberwolfach Reports 18 (2021), section 3.3, pp. 2170–2171, equations (10)–(11). The report was published in 2022; 2021 is its volume/workshop year.

- Report DOI: https://doi.org/10.4171/OWR/2021/40
- Inspected publisher PDF: https://ems.press/content/serial-article-files/46918
- Size: 1295115 bytes.
- SHA-256: 6f260196006d0b22157e91804245d560b5f5e255a1ca1581556376e6682d4742.
- Author preprint: https://arxiv.org/abs/2112.02126
- Inspected PDF: https://arxiv.org/pdf/2112.02126
- Size: 138766 bytes.
- SHA-256: 70efa259dbb75a5a568d508101cfccb78cc91f78d91c3e0da9ef2d766083d4bd.

Existing solution: Alper Ferudun, A Composition Estimate for Fourier Series with the Supremum in Time Inside the Sum, and a Question of Chrusciel, version 1.0, October 9, 2026, 24 pages, unrefereed.

- Landing page: https://eulersolve.org/papers/owr-8415343-001/
- DOI: https://doi.org/10.5281/zenodo.23272241
- Inspected PDF: https://eulersolve.org/papers/owr-8415343-001/paper.pdf
- Size: 269262 bytes.
- SHA-256: 0dd8169c738142b17b1cf151f39d79b94ffa74522b74ebc487d47f831ee7c555.

All three PDFs were retrieved on 2026-10-21 UTC. Their sizes and hashes were recomputed during the audit and agree with the retrieval manifest. The acceptance rests on proof inspection, not on the claimant's verification report. This package contains authored mathematical analysis and public source metadata, not copies of the source documents or dataset contents.
