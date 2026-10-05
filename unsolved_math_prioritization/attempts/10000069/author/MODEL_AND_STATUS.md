# 10000069: exact model and credited-result status

Reviewed 2026-10-05. Rank 711; AMR-099-0069. No new solution or historical priority is claimed. This is a source-verification and mathematical-reconstruction packet, not five new attempts.

## Exact question

Benjamini's *Euclidean vs. Graph Metric*, Question 9.6, concerns the function delta(p) on [1/2,1], with a specific question whether delta(1/2)=0. The primary author-PDF search index displays the question on page 18 of erd100.pdf. The original PDF URL now returned 404 and was not downloaded or visually checked. The live catalogue URL https://www.unsolvedmath.com/problems/10000069 returned HTTP 403. Its full current wording was not inspected. The available public descriptor identifies this title, ID and source link; lost raw AI-generated corpus records were not inspected and their statement hashes are not being represented as verified.

Start with a single undirected edge between distinguished terminals a,z. In each generation independently replace every edge by either two edges in series (probability p) or two parallel edges (probability 1-p). Multiple edges are retained and replaced separately. This is a two-terminal hierarchical multigraph, not a uniform labeled or unlabeled series-parallel graph. At generation n the edge count is exactly 2^n. D_n is the shortest-path edge distance between the original terminals, D_0=1. Thus

D_(n+1) =d= D_n'+D_n'' with probability p, and min(D_n',D_n'') otherwise,

with independent copies and independent gate choice. The question is the annealed generation exponent

delta(p)=lim (1/n) log E D_n.

It is not the exponent of diameter, effective resistance, random-vertex distance, E log D_n, or an asserted almost-sure exponent. With deterministic edge size N=2^n, its equivalent exponent is delta(p)/log 2.

## Verified prior results and interpretation

1. Chen, Derrida, Duquesne and Shi, *The distance on the slightly supercritical random series-parallel graph*, Advances in Applied Probability 58 (2026), 80-121, online 9 September 2025, DOI https://doi.org/10.1017/apr.2025.10023. Their Theorem 1 proves delta(1/2+epsilon)/sqrt(epsilon) -> pi/sqrt(6). Combined with monotonicity and nonnegativity, this implies delta(1/2)=0. The endpoint implication is reconstructed here; no first-priority attribution for that endpoint is asserted. The source's theorem and square-root scope were visually checked on journal p.82. Its 42-page proof was not independently reconstructed in full.

2. DannyExperiments, *A spectral characterization of the random series-parallel distance exponent*, public repository https://github.com/DannyExperiments/random-series-parallel-distance-exponent. At inspected main commit a875da08e8bfbdb70fd8165c097ab036731b5f6f, its canonical proof and four-page manuscript supply an attained maximal nonlinear eigenvalue and matching lower/upper variational formulas for every p in (1/2,1). The public metadata dates release 1.0.0 to 2026-08-10. This packet directly reconstructs the mathematical argument, rather than relying on the repository's self-reported audits. No human peer review or formal verification is claimed for that source or for this review. Its DOI metadata is not independently certified here.

3. At p=1, D_n=2^n, so delta(1)=log 2.

Recommended disposition: credited exact spectral characterization, with the literal 'shape' scope qualified. The closed parameter interval has an exact implicit operator characterization plus the known endpoints. This is not a verified elementary scalar formula, uniqueness theorem, convergence-of-normalized-laws theorem, or global convexity theorem. Whether the informal word 'shape' is considered fully answered by such a characterization is an interpretation, not a mathematical inference. Do not mark an unqualified closed-form resolution on this evidence.

Campaign accounting records one substantive source-verification/proof-reconstruction route, 1/5. No five-turn exhaustion is claimed. This count does not imply that the credited external theorem is a new result. A fresh independent source/proof audit and parent acceptance are still required before any remote update. No remote changes were made.
