# Initial independent compactness/source family seal

UTC seal: 2026-10-02T23:17:00Z (written after source-first reading; actual filesystem time supplies precise write timestamp).
Progress estimate: 45% of this family audit; mathematical route established, published exact match and candidate comparison still unread.

## Exposure boundary
Read only applicable root AGENTS.md, immutable source_snapshot/source_record.json, authoritative EMS original report metadata and its group-work pages 411–413, plus search-result metadata naming a potentially relevant paper. No candidate README, SOURCE_STATUS, proof, helper, result, sibling-family work, historical ledger or PR diff has been read. Search-result metadata is not a paper proof. This seal precedes those exposures.

## Literal target and success criteria
The original report (DOI 10.4171/OWR/2020/6, workshop 2–8 February 2020; EMS publication 10 February 2021) defines unit-sphere projection laws of independent uniform[-1,1] variables. Its Lemma 1 asks for all weak/Prohorov limits of sequences nu_N in E_N. Its Conjecture 1 additionally asks for the speed-N random-measure LDP with the stated logarithmic rate. The immutable source labels this open as of 22 August 2026; that label is a hypothesis to verify. Compactness alone does not prove the LDP.

Set kappa_a = Law(sum_j a_j U_j + sqrt((1-||a||_2^2)/3) Z), for arbitrary real a in l2, ||a||_2 <= 1, independent U_j uniform[-1,1] and Z standard normal. The Gaussian coefficient is zero on the boundary. Series convergence and independence are required. Success for the intermediate target requires (i) every convergent E_N sequence has such a limit, and (ii) every such law is attained along all N, not just a subsequence. Full source resolution also requires the LDP or an exact matching published theorem.

## Independent mechanism
Canonical parameter space K consists of decreasing nonnegative sequences a with every finite sum of squares <= 1. Endow K with product topology, for example d(a,b)=sum_j 2^-j |a_j-b_j|. This is compact as a closed subset of [0,1]^N. It is not compact in l2 norm: N equal entries N^-1/2 converge coordinatewise to zero while retaining norm one. Every member has a_j <= j^-1/2.

The independent series sum a_j U_j converges in L2 because variance of a tail is sum_tail a_j^2/3. It also converges almost surely by the independent centered finite-total-variance convergence theorem; a self-contained maximal-inequality proof can be supplied if needed. Signs do not affect uniform summand laws. Any permutation preserves the L2 limit law by finite truncation and tail variance; sorting absolute values therefore loses no laws.

Characteristic function:
 phi_a(t) = exp(-(1-sum_j a_j^2)t^2/6) product_j sinc(a_j t).
For |x| <= 1/2 there is an absolute constant C with
 |log sinc(x)+x^2/6| <= C x^4.
After retaining m coordinates, the characteristic function differs multiplicatively from
 [product_{j<=m} sinc(a_j t)] exp(-(1-sum_{j<=m} a_j^2)t^2/6)
by an error whose logarithm has absolute value <= C t^4/(m+1). This bound is uniform over K, including boundary norm one, and follows from sum_tail a_j^4 <= a_{m+1}^2 sum_tail a_j^2 <= 1/(m+1). A zero in a retained factor causes no issue because the comparison is formed in the nonzero tail, then multiplied by the head. Hence coordinatewise convergence implies characteristic-function convergence and weak convergence, even when l2 mass escapes and becomes Gaussian. Compact image supplies necessity and weak/Prohorov completeness.

For attainability of arbitrary unsorted real a, retain r_N=floor(sqrt(N)) entries (with N=1 handled separately), append N-r_N equal nonnegative fillers of magnitude sqrt((1-sum_{j<=r_N} a_j^2)/(N-r_N)). The vector has norm exactly one; r_N tends to infinity and filler maximum tends to zero. Retained sums converge in L2 to sum a_j U_j. The independent filler sums converge to Gaussian variance (1-||a||_2^2)/3 by the characteristic-function expansion, including the zero-variance endpoint. This proves all laws are attained along all N. If a=0 it is the classical equal-coordinate CLT; if norm one, filler variance tends to zero; if finite nonzero coefficients, eventually the retained part is constant; if infinitely many coefficients, L2 controls retained convergence without requiring absolute summability.

Injectivity must be claimed only on K, not raw signed/permuted l2. For a!=0, the first positive real zero of phi_a is pi/a_1: no factor or Gaussian vanishes earlier; the tail product is nonzero there. Its multiplicity is the finite number of coordinates equal to a_1. Removing those sinc factors permits recursive recovery of all positive coordinates. Uniform convergence of the analytic product on compact complex sets follows from sum a_j^2<infinity; no extra tail zeros occur. Thus equality of laws determines the sorted coefficient multiset, hence the norm and rate. Zero is the unique zero-free canonical parameter. This yields a compact homeomorphism between K and its law image; it does not supply the probability LDP for the random parameter by itself.

## Current exact gap
Need write out analytic-product and almost-sure details, check constant with independent finite controls if useful, verify primary published theorem/version/date against the exact source, then read all original and amended candidate files without executing/importing any candidate helper. No claim of novelty or of a complete source solution has been made.
