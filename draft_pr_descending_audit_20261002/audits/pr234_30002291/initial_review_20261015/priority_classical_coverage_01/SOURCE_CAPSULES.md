# Authored primary-source capsules

Each capsule is an original, short scope summary (under 200 words); no copied passages. Full texts and extraction products remain in ignored private storage. The report's constructions and implication arguments are this audit's deductions.

## OWR13 — original problem

[Official report](https://publications.mfo.de/handle/mfo/3340). The cached official PDF's printed pages 491–493 contain Podolskij's contribution. Printed page 492 gives the quadratic marked-jump stable limit for compound-Poisson noise and asks for sufficient hypotheses on a more general pure-jump semimartingale driver. The request does not specify a maximal class or require a functional topology. The contribution distinguishes Brownian and jump-driven smoothing regimes. This audit uses the fixed-time quadratic formula as the target, not the later spatial Gaussian discussion.

## SUR14 — early public announcement

[arXiv:1405.1531v1](https://arxiv.org/abs/1405.1531v1), submitted 2014-05-07 08:24:48 UTC. Podolskij's survey states the jump-phase power-variation limit in Theorem 4.8(i), with deterministic meshes tending to zero, a symmetric Lévy core, and power exceeding its activity index. It credits a 2014 working paper of Basse-O'Connor, Lachièze-Rey and Podolskij. It therefore establishes an earlier announcement than the 2015 arXiv paper. The survey is not used as an independently verified full proof. A separately retrieved December 2014 Thiele version renumbers this result Theorem 4.7 and changes some assumptions, so these documents must not be silently conflated. Its broader discussion of ambit fields and integration is not itself an asymptotic theorem for arbitrary predictable jump kernels.

## LMA15 — full Lévy proof

[arXiv:1506.06679v1](https://arxiv.org/abs/1506.06679v1), submitted 2015-06-22 17:02:04 UTC; later journal DOI [10.1214/16-AOP1170](https://doi.org/10.1214/16-AOP1170), 2017. Theorem 1.1(i) gives the jump-phase stable limit for scalar symmetric pure-jump Lévy moving averages when the power exceeds the activity index, the singularity is sufficiently mild, and the kernel/tail conditions hold. Theorem assumptions include activity strictly below 2. Remark 2.3 already identifies symmetry as largely a simplifying assumption. The full relevant proof treats finite jumps, suppresses separated tails, estimates small-jump contributions, and uses convergence together. Lemma 4.1 supplies full-original-sigma-field phase mixing under a smooth density assumption. The local file misleadingly named lma2017.pdf is this preprint, not an authenticated publisher copy. Publisher and author-institution PDF retrieval attempts were blocked.

## LSS16 — adapted scalar volatility

[arXiv:1604.02307v2](https://arxiv.org/abs/1604.02307v2), v1 submitted 2016-04-08 11:16:22 UTC and v2 submitted 2016-10-14 14:37:46 UTC; journal DOI [10.3150/17-BEJ956](https://doi.org/10.3150/17-BEJ956), 2018. Model (1.2) integrates a scalar adapted càdlàg volatility against a symmetric Lévy process relative to the given filtration; independence of volatility and noise is not imposed. Theorem 1.2(i) gives full-field functional stable M1 convergence under (A), (B1), activity below 2, and the power/singularity restrictions. Thus its fixed-time joint limit is stronger than the candidate's conclusion on their overlap. Lemma 4.7 and its proof are the relevant small-jump approximation. The v1 text asserted J1 convergence; v2 changes to M1 and explicitly rejects J1/J2. The finite-dimensional marked-jump result is present already in v1. The general spatial ambit model in the introduction is background, not the model of this theorem.

## FUN18 — formal nonsymmetric Lévy coverage

[arXiv:1806.10352v1](https://arxiv.org/abs/1806.10352v1), submitted 2018-06-27 09:08:09 UTC; journal DOI [10.1214/19-EJP336](https://doi.org/10.1214/19-EJP336), 2019. Model (1.1) permits a general two-sided Lévy process with no Gaussian component. Theorem 2.1(i) gives stable marked-jump limits for smooth functions vanishing sufficiently at zero; Proposition 2.3(i) gives finite-dimensional stability and M1 convergence under a sign condition. The assumptions retain activity strictly below 2 and a deterministic convolution kernel satisfying (A). The proof extends finite-jump analysis to infinite-activity Lévy noise by truncation. This removes nonsymmetry as an unqualified novelty claim for the quadratic Lévy specialization, but does not state a theorem for arbitrary predictable compensators.

## MULT18 — multiple kernel singularities

[arXiv:1803.01017](https://arxiv.org/abs/1803.01017) and [journal full text](https://www.vmsta.org/journal/VMSTA/article/122/read). Ljungdahl and Podolskij extend the singularity geometry in Lévy moving-average power variation. The scalar noise remains a symmetric pure-jump Lévy process, with activity below 2 and power exceeding it. The displayed prior theorem and the new theorem concern deterministic kernel singularities, not changing predictable mark distributions. This is important method context but supplies no direct arbitrary-kernel representation or compensator theorem.

## FIELD20 — marked Poisson random fields

[arXiv:2008.01412](https://arxiv.org/abs/2008.01412), v1 2020-08-04 08:42:42 UTC, v3 2022-02-21 17:07:35 UTC; [journal DOI](https://doi.org/10.1214/21-EJP617), 2021. The model integrates deterministic kernels against a symmetric independently scattered infinitely divisible random measure with deterministic homogeneous control characteristics. Its activity assumption is below 2, with additional small-jump regularity. Theorems 3.1(i) and 3.2(i) express limits using independently uniformly marked Poisson measures. This is an authentic marked-random-field extension, but neither its noise nor its integrand is the arbitrary predictable mark-dependent amplitude needed for a general Itô-driver embedding. The beta-equals-2 observation in Remark 3.3 concerns Gaussian noise in the ergodic regimes, not the candidate's pure-jump boundary.

## JAC06 — semimartingale criteria and embedding

[arXiv:math/0604450](https://arxiv.org/abs/math/0604450), submitted 2006-04-20 13:28:01 UTC; published 2008. Jacod studies functionals of increments of an observed semimartingale. Hypothesis (H) and representation (2.11) explicitly admit arbitrary predictable jump-size maps of a Poisson random measure on an enlarged space. Stronger envelopes and regularity appear in later hypotheses. Theorem 2.2 includes ordinary quadratic variation. Lemma 5.8 handles full-field stable limits around Poisson jump times and emphasizes arbitrary filtrations. These are established ingredients, but the observed singular moving average in the candidate is a different object; neither a representation nor an ordinary quadratic-variation theorem supplies the candidate's rescaled convolution statistic without additional analysis.

## ID14 — semimartingale recognition

[arXiv:1404.7598](https://arxiv.org/abs/1404.7598) and [publisher record](https://doi.org/10.1007/s00440-014-0609-1). Basse-O'Connor and Rosiński characterize semimartingales represented by infinitely divisible random measures, with decomposition and kernel criteria. The model uses deterministic representing kernels and infinitely divisible laws. Theorems 1.6/3.1 concern recognition and decomposition; they do not give the marked-jump asymptotic for a singular convolution of a general history-dependent Itô driver. This source guards against conflating a driver that is a semimartingale with a smoothed observed process that is one.

## FRONT24 — recent reference map

[arXiv:2410.00566v2](https://arxiv.org/abs/2410.00566v2), revised 2024-10-30. Benth and Veraart's survey maps univariate, multivariate, spatial and infinite-dimensional realized-variation literature. Section 2.3 points to the classical Lévy moving-average papers, Gaussian spatial work, and multivariate semistationary work. It was used for follow-up leads, not as negative evidence of novelty. It provides no controlling theorem establishing the submitted arbitrary-predictable-compensator limit.
