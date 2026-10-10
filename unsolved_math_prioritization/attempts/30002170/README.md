# Fractional Lévy-area optimal-approximation lower bound

Problem 30002170 / OWR-12013-003. First substantive attempt: 1/5. Accepted for the full original lower-bound target after independent AI mathematical audit and acceptance review.

For every fixed H in (1/4,1), independent standard fractional Brownian components B1 and B2, every T>0 and every integer n>=1, let X_T be the canonical iterated integral of B1 against B2. Observing both components at jT/n, j=1,...,n, gives

\[
\left\|X_T-\mathbb E[X_T\mid\sigma(B^i_{jT/n}:i=1,2;\ j=1,\ldots,n)]\right\|_2
\ge c_H T^{2H}n^{1/2-2H},\qquad c_H>0.
\]

The proof also bounds every square-integrable estimator measurable with respect to those observations. Formula (15) supplies an explicit positive constant depending only on H. The constant is not asserted sharp.

## Complete proof and review

- [PROOF.md](PROOF.md): complete rough-range proof for 1/4<H<1/2. Localized covariance paths yield Gaussian product witnesses independent of the complete observation vector. A uniform upper Gram bound and an exact covariance identity imply the lower rate by Cauchy–Schwarz.
- [ALL_H_COROLLARY.md](ALL_H_COROLLARY.md): complete extension to every H in (1/4,1), including every n and T directly.
- [AREA_CONVENTION_CHECK.md](AREA_CONVENTION_CHECK.md): complete proof that Euler and polygonal constructions have the same L2 limit, fixing the exact canonical iterated-integral convention.
- [INDEPENDENT_AUDIT.md](INDEPENDENT_AUDIT.md): full mathematical audit, including Fourier normalization, endpoint regularity, periodization, signed covariance matrices, nonlinear-estimator orthogonality, stochastic-limit passage, auxiliary Gaussian realization, all-H scope, and exclusions.

The original question is credited to [Neuenkirch's OWR contribution](https://doi.org/10.4171/owr/2012/41), pp.2524–2525. The established L2 convergence input is [Neuenkirch–Tindel–Unterberger](https://doi.org/10.1016/j.spa.2009.10.007), using the explicitly identified [arXiv version](https://arxiv.org/abs/0902.0497). The known smooth-range optimal asymptotic rate is credited to [Neuenkirch–Shalaiko](https://doi.org/10.1016/j.jco.2015.09.008); the Brownian exact optimum is already known. Those cases are not claimed as new discoveries.

There is no claim at H=1/4 or H=1, of a sharp constant or exact normalized-error limit, or for adaptive/arbitrary-mesh sampling, unequal Hurst parameters, or correlated components. Historical novelty and priority are not certified.

[SOURCE_LEDGER.md](SOURCE_LEDGER.md) records public bibliographic identities and inspection history. [PROVENANCE.md](PROVENANCE.md), [STATUS.json](STATUS.json), and [MANIFEST.json](MANIFEST.json) identify this proof-only edition.

All mathematical material is AI-assisted and unrefereed. Scoped acceptance is not external human peer review or formal proof-assistant certification. Edition preparation makes no new source-inspection or exhaustive-literature-search claim. No queue or historical accounting is changed by this edition.
