# Source resolution: ball-shaped large-mass minimizers

**Proposed disposition: already_solved, 0/5. Independent review pending.**

The question in Rupert L. Frank's contribution to OWR 43/2016, pp. 2505–2506, is answered affirmatively by Rupert L. Frank and Elliott H. Lieb, *Proof of spherical flocking based on quantitative rearrangement inequalities*, Ann. Sc. Norm. Super. Pisa Cl. Sci. (5) **22** (2021), 1241–1263, **Theorem 1.1**. [Published article](https://journals.sns.it/index.php/annaliscienze/article/view/852), [DOI](https://doi.org/10.2422/2036-2145.201909_007), [preprint](https://arxiv.org/abs/1909.04595v1).

## Exact specialization

The original report fixes \(\alpha>0\), minimizes over all measurable densities \(0\le\rho\le1\) on \(\mathbb R^3\) of mass \(m\), and uses
\[
\frac12\iint \rho(x)(|x-y|^{-1}+|x-y|^\alpha)\rho(y)\,dx\,dy.
\]
The catalog omits the parameter range from its isolated question; the original contribution supplies it. No radial, smoothness, connectedness, compact-support or center-of-mass restriction is imposed on the admissible class.

Frank–Lieb's published functional (1.1) has the same factor \(1/2\), coefficient 1 on each kernel term, and the same density cap and mass constraint, in dimension \(N\) with repulsive power \(\lambda\). Their Theorem 1.1 applies for every \(\alpha>0\) and \(0<\lambda<N-1\). Set \(N=3\), \(\lambda=1\). Then \(0<1<2\), so the original functional is literally the same one; no parameter-changing dilation is needed for this main application.

There is a finite threshold \(m_{3,\alpha,1}\) above which **every** minimizer is the indicator of a ball, almost everywhere. Thus one may take \(m'_{c_2}(\alpha)=\max\{1,m_{3,\alpha,1}\}\). The ball has volume \(m\), hence radius \((3m/(4\pi))^{1/3}\). Its center is arbitrary by translation invariance. Null-set changes are immaterial for densities, so literal pointwise uniqueness is neither asserted nor needed.

The theorem is a rigidity result, not just convergence toward a ball. It does not give an optimal threshold, a threshold uniform as \(\alpha\) varies, ball optimality at every mass, or a claim about the intermediate liquid/solid regime. The published introduction explicitly leaves a general quantitative energy-gap inequality as a further question; it is not included here.

## Proof and dependency audit

`DEPENDENCY_AUDIT.md` records the checked main proof from the quantitative attraction estimate, through the density-valued shell modification, to the final exact rigidity argument. It also records the supplementary density extension, the precise dimension/exponent condition, the earlier diameter theorem, and the existence input.

This is a **credited prior-theorem application with a proof-chain audit**, not a new proof or a fresh foundational recertification of every external symmetrization, spectral, rearrangement and compactness result. The complete main proof and supplement were read; the scope of each other dependency check is explicitly recorded. No original proof-attempt turn was needed.

The catalog's cited 2021 paper by Pegon concerns perimeter plus an integrable repulsive kernel. That model differs from the pure attractive–repulsive power-law functional here and is not evidence that this question remained open.
