# Independent source-scope report: Di Persio summary

Prepared 2026-10-15 UTC. Independent conclusion was formed from the complete primary PDF and matching supplied text before reading parent source findings or other audit verdicts. This is a scope assessment, not a novelty certificate or a judgment about the complete contents of an unseen cited paper.

## Conclusion

The available statements do not establish the target, including for a nonconstant finite-state small-noise law. They concern weak topology, fixed smooth tests, or cumulants. Passing from those statements to every diverging mesoscopic width and every polynomial environmental tail order requires an unsupported bridge. This neither disproves the target nor settles what an unseen complete BMP1999 article establishes.

## Compact source-fact record

The document is a thesis summary by Luca Di Persio, supervised by Alessandro Pellegrinotti. Cover: February 2002; academic year 2000-2001. Model: finite-state space-time product environment, mean-zero perturbation P_0+epsilon c, valid probabilities, finite range, aperiodicity, nondegenerate covariance (printed pp.1-4; PDF pp.2-5). Conclusions require small epsilon.

Theorem 0.1 (p.6/PDF7): almost-sure quenched weak Gaussian CLT, nu>=1. Theorems 0.2/0.3 (p.6/PDF7): mean/covariance correction convergence in L^(2n), nu>=3/5; thresholds depend on n. Theorems 0.4/0.5/0.6 (pp.7-9/PDF8-10): smooth-test higher-order expansions, nu>=3/5/(2m+1). Theorem 0.7 and (4) (p.10/PDF11), attributed to [7], BP2001: one-dimensional annealed-centered fixed-regular-test fluctuation, scale T^(-1/4), Gaussian convergence in distribution. The printed dispersion formula (5) contains zeta; no interpretation is used here.

Equations (6)-(8) (p.11/PDF12): pointwise difference definition, then two-dimensional smooth-test distributional fluctuation at scale sqrt(log(T)/T). Theorems 0.8-0.11 (p.12/PDF13): Gaussian distributional limits for mean/covariance corrections, respective environmental L2 scales T^(1/4), sqrt(log T), T^(3/4), sqrt(T), dimensions 1,2,1,2.

Bibliography [8] (p.14/PDF15): Boldrighini-Minlos-Pellegrinotti, Central limit theorem for a random walk in dynamical environment: integral and local, Theory of Stochastic Processes 5(21), 3-4 (1999), 16-28. No local-limit residual/rate is stated in the summary.

## Provenance and checks

Supplied source URL: https://www.mat.uniroma3.it/scuola_orientamento/alumni/laureati/dipersio/sintesi.pdf . I did not refetch it or perform broad searches. Full PDF: 127,191 bytes, 15 PDF pages, SHA-256 `65791491207ab830741671141861f71afae5af8ff4d9e768a2faa08f806cc202`. Supplied matching text: 24,892 bytes, 673 lines, SHA-256 `324dd2b9f6b5468f6d5cdd39b062a310e2c79775096d6aa60fdf1e3ba8c6988b`.

Printed page j is PDF page j+1; the cover is PDF page 1. Complete text was read. The cover, model assumptions, every theorem page, and final bibliography page were also inspected visually. The PDF annotation scan found no annotations or embedded links; its catalog has only Type and Pages. No textual URL or direct original-source footnote was found, so there was no embedded original-source link to follow. The complete BMP1999 article was not read. Its title is a retrieval lead, not evidence for a particular residual estimate. The unclear printed dispersion notation is solely a reason to consult the cited original before using that formula; no allegation about BP2001 or BMP1999 follows.

## Exact target and independently derived model comparison

Let p_(t,x) be i.i.d. scalar right-jump probabilities with an arbitrary fixed law supported in (0,1), with mean q. Let P_N^omega be the quenched endpoint law and A_N the annealed binomial endpoint law of the +/-1 walk. For deterministic bins I_(N,j) of width M_N and deterministic alignment a_N, define

`D_N = sum_j |P_N^omega(I_(N,j)) - A_N(I_(N,j))|`.

The convention-dependent factor 1/2 does not affect the issue. The target requires, for every deterministic M_N tending to infinity and alignment, and every fixed eta,K>0,

`P_environment(D_N > eta) = O(N^(-K))`.

The law stays fixed as K varies, and no rate such as M_N>=N^delta may be imposed.

Parity does not exclude this walk from an aperiodic formulation. Set `Y_t=(X_t+t)/2`. Its increments are 0 or 1 and its environment is `eta_t(y)=p_(t,2y-t)`. This is an injective reindexing of independent space-time coordinates, hence eta remains i.i.d. The annealed characteristic function is `1-q+q exp(i lambda)`, with modulus strictly below one away from zero and variance q(1-q)>0. For a finite law `p_s=q+epsilon a_s`, choose `c(1,s)=a_s` and `c(0,s)=-a_s`, with mean-zero a. Centered X is twice centered Y; bins become intervals of half the width, with endpoint rounding. Diverging width and arbitrary deterministic alignment are preserved.

This comparison permits applying suitable finite-state weak-noise statements to a nonconstant law in the target setting. It does not convert them into the target estimates. Nor can a general scalar law be covered merely by finite-state approximation without uniform estimates; none is available here. Formally shrinking epsilon while enlarging c does not verify a smallness threshold that can depend on c. Likewise, a theorem permitting a different smallness threshold for each moment order does not by itself provide every tail order for one fixed law.

## Independently derived topology and probability gaps

Coarse L1 is the supremum of `sum_j sigma_j [P_N^omega(I_j)-A_N(I_j)]` over all signs sigma_j in {-1,1}. These tests are discontinuous, vary with N, oscillate on scale M_N/sqrt(N) in diffusive coordinates, and their optimizing signs may depend on the environment. Fixed-test conclusions supply no operator control over this class. Smoothing produces derivative norms growing as the transition scale shrinks; a usable bridge must track those norms and the number of bins. Even small weak errors allow substantial alternating excess and deficit on diverging blocks of size o(sqrt(N)).

A Gaussian distributional fluctuation limit does not give an every-K fixed-error tail, even with exact finite-N centering and the natural L2 fluctuation scale. For N>=2, set `B_N=1_{U<=N^(-2)}` and `R_N=N^(-1/4)G + S B_N`, where G is standard Gaussian, U is uniform on (0,1), S is a symmetric +/-1 sign, and G,U,S are independent. Then E[R_N]=0 and `Var(N^(1/4)R_N)=1+N^(-3/2)`, tending to one. Almost surely U>0, so B_N eventually vanishes: R_N tends to zero, and N^(1/4)R_N tends to G almost surely, hence in distribution. Moreover, `E[(N^(1/4)R_N-G)^2]=N^(-3/2)`, so normalized convergence also holds in L2. Conditional on B_N=1, the probability that `|R_N|>1/2` tends to one, with exponentially small Gaussian error in sqrt(N); off that event the Gaussian tail has the same exponential bound. Thus `P(|R_N|>1/2)` is asymptotic to N^(-2), which is not O(N^(-K)) for K>2. This is an abstract scalar implication counterexample, not a walk construction. It matches exact centering and the natural L2 scaling while leaving the higher-tail-order gap exposed.

There is a valid weaker binning corollary of an almost-sure weak CLT to a continuous Gaussian: binned L1 tends to zero for widths at least a positive multiple of sqrt(N), uniformly over deterministic alignments. Indeed, the two rescaled CDFs converge uniformly to the same continuous limit; a fixed central diffusive window meets only boundedly many such bins, and tightness handles its complement. This has no environmental rate and does not reach all diverging widths. A deterministic environment gives zero discrepancy exactly, but does not constitute a nonconstant law-special target result.

## Exact remaining gap and route status

The missing input is dimension-one coarse endpoint-law control for a fixed nonconstant law, uniform over all diverging deterministic widths and alignments, with fixed-error environmental probability O(N^(-K)) for every fixed K. Neither a pointwise-difference definition nor a fixed-test fluctuation limit supplies that input. Reading the actual BMP1999 original could potentially change the source assessment, but its contents are outside this review. The route from this summary alone to the target is blocked at the unsupported local/mesoscopic uniform estimate and environmental-tail upgrade. No claim of novelty, target falsity, or exhaustive literature resolution is made.
