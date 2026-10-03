# Source and scope audit

## Original problem

The source is Sivaraman Balakrishnan, *Minimax hypothesis testing*, printed pp.2663–2664 of [Oberwolfach Report 46/2022](https://ems.press/content/serial-article-files/46984), DOI [10.4171/OWR/2022/46](https://doi.org/10.4171/OWR/2022/46). The workshop took place in October 2022; EMS published the report in July 2023.

The exact core question is: “does the rate for estimating ρ(P, P0) depend strongly on P0 or not?”

Its context also asks how increasing a tolerant-testing null radius connects testing and functional-estimation rates. The observation model is iid data from P, a fixed reference P0, and potentially different structured null and alternative classes. No loss, local neighborhood, or universal classification criterion is prescribed. The Yuxin Chen heading immediately afterward starts another contribution and is not this problem's attribution.

The catalogue's clean statement combines both research directions. This package retains both, distinguishes outer radius from separation gap, and does not turn a special example into a universal answer.

## Primary literature and exact applicability

1. [Jiao–Han–Weissman, *Minimax Estimation of the L1 Distance*](https://arxiv.org/abs/1705.00807), IEEE Transactions on Information Theory 64 (2018), 6672–6706, DOI [10.1109/TIT.2018.2846245](https://doi.org/10.1109/TIT.2018.2846245). The precise theorem and parameter restrictions used here are documented in Attempt 2. It supplies prior, sharp discrete results; it is not an all-functionals classification.

2. [Paninski, *A coincidence-based test for uniformity given very sparsely-sampled discrete data*](https://sites.stat.columbia.edu/liam/research/pubs/sparse-unif-test.pdf), IEEE Transactions on Information Theory 54 (2008), 4750–4755. Attempt 1 uses the classical paired-perturbation lower-bound mechanism rather than claiming that mechanism as new.

3. [Canonne–Jain–Kamath–Li, *The Price of Tolerance in Distribution Testing*](https://proceedings.mlr.press/v178/canonne22a.html), COLT 2022. This already studies the discrete tolerance tradeoff and reference-dependent complexity, up to logarithmic factors. One must consult the formal results: Theorem 5 assumes epsilon_1<=c epsilon_2; the instance-sensitive upper bound in Theorem 39 imposes epsilon_1<=c epsilon_2/log(S/epsilon_2). The introductory informal statement is not a license to extrapolate to arbitrarily small gaps.

4. [Kania–Manole–Wasserman–Balakrishnan, *Testing Imprecise Hypotheses*](https://arxiv.org/abs/2510.20717v2), revised 27 January 2026. For Gaussian sequence L1 testing, Theorem 3.1 gives, up to logarithmic factors, separation sigma d^(3/4), sigma sqrt(d lambda), and sigma d in the respective ranges lambda<=sqrt(d), sqrt(d)<=lambda<=d, and lambda comparable to d, where lambda=epsilon_0/sigma. These regimes interpolate to functional estimation. The paper also treats smooth white-noise and density models. It does not characterize larger L1 tolerances in that theorem; Appendix C.8 retains a constrained-moment-matching conjecture for nonsmooth norms. These are major existing partial answers, not grounds for a new complete-resolution claim.

## Remaining scope

The source is a research program rather than a single sharply quantified conjecture. These five approaches do not characterize arbitrary pairs of discrepancy and distribution class. They also do not obtain general reference-sensitive density rates or all-tolerance, all-norm transitions. A fixed-reference minimax criterion and a shrinking-neighborhood criterion are explicitly separated in Attempts 1 and 3.

Literature checked on 3 October 2026. No full resolution of the broad classification was established in this investigation; absence of a located result is not proof that none exists.
