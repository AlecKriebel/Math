# Independent review of 2800904: clustering stability and LP integrality

**Verdict: PASS for the two explicitly limited partial results.** Retain **unsolved, 2/5 attempts** for the original problem. No mandatory mathematical correction was identified. This is a separate adversarial AI review, not human peer review, and establishes no novelty.

The frozen `PARTIAL_RESULT.md` has SHA-256 `576934a5f48389781b7d51b73db575f74de82b45d14b64bd71de3d642f0e3d9f`. The reviewed snapshot and submitted verifier are included under `author_replay/`.

## Source scope

[Bandeira's complete lecture notes](https://people.math.ethz.ch/~abandeira/TenLecturesFortyTwoProblems.pdf), printed pp.128–129, specify the facility-assignment k-median LP with assignment columns summing to one, assignment entries bounded by facility variables, facility variables summing to k, and all variables in [0,1]. This is exactly the LP used in the artifact. The source also presents a separate k-means SDP. Open Problem 9.4 asks for stability-based integrality conditions for either relaxation. Its immediate motivation compares the objectives at k−1, k and k+1; it does not fix a multiplicative perturbation parameter. The preceding stochastic-ball results and random-model Problem 9.3 are separate.

The source section concerns Euclidean clustering and more broadly expresses the objectives using distances. The submitted eight-point example is only a **finite metric**. No Euclidean realization is asserted or established. Its valid negative conclusion is that uniqueness or merely some multiplicative resilience greater than one cannot, by themselves, force this finite-metric LP to be integral. It is not a counterexample to a specified Euclidean objective-gap conjecture or to a sufficiently strong universal resilience threshold. The artifact preserves this distinction.

[Chekuri–Gupta (2018)](https://arxiv.org/abs/1806.04202), Question 3, asks whether some fixed resilience parameter forces integrality for k-median and k-means LPs. The paper's preceding integrality results concern k-center variants. [Makarychev–Makarychev (2016)](https://arxiv.org/abs/1607.06442), Theorem 1.2, gives an exact algorithm for 2-metric-perturbation-resilient center-based clustering; its construction uses a minimum spanning tree and dynamic programming. An exact algorithm is not automatically an integrality theorem for the LP or SDP under discussion. I checked the full primary PDFs at the cited statements and definitions. This limited comparison is not an exhaustive current-literature audit or an assertion that all related threshold questions remain open today.

## Exact finite metric and universal perturbation claim

The distance matrix is symmetric, has zero diagonal and positive off-diagonal entries. Its off-diagonal range is [1006,1998]. A triangle with three distinct vertices satisfies the strict inequality because 1998 < 2·1006; cases with repeated vertices give the remaining metric inequalities.

For each of the 28 unordered center pairs, I independently formed the cost-generating polynomial

\[
\prod_{j=0}^{7}(z^{d_{aj}}+z^{d_{bj}}).
\]

Adding these polynomials counts all 7,168 center/assignment solutions, including assignments that are not nearest-center assignments. The lowest coefficient occurs at exponent 7099 with multiplicity one, at centers {2,4} and assignment (4,2,2,4,4,4,2,4). The next occupied exponent is 7110. Counting the larger feasible family, which even permits a selected center to be assigned elsewhere, causes no problem: the unique minimizer assigns each center to itself.

For every coordinatewise perturbation satisfying d ≤ d′ ≤ (1001/1000)d, the displayed optimum has new cost at most 7106.099. Every competing integral solution has new cost at least its old cost, hence at least 7110. The uniform strict margin is exactly 3901/1000. This quantifies **every** permitted perturbation, rather than a random sample, and covers alternative assignments with unchanged centers. It implies unchanged unique clustering even if the perturbed array need not be symmetric or metric, and therefore also under metric-only perturbations. Scaling a shrinking perturbation d/α ≤ d″ ≤ d by α reduces it to the same argument; uniform scaling does not change minimizers.

The proposed fractional point uses weight 1/4 on each diagonal and on the three cyclic-distance-1-or-4 neighbors of each client. Thus each column sums to one, all entries lie between zero and y_i = 1/4, and Σy_i = 2. Its objective is 12607/2 = 6303.5, strictly below 7099 by 1591/2. No claim about the exact fractional optimum is needed. The relaxation is feasible and compact, so its optimum is attained and cannot be attained at an integral point.

The exact integral objectives at k = 1,2,3 are 10887, 7099 and 5171. These values supply no specified large-drop/plateau theorem or counterexample. In particular the example does not answer the source's qualitative request, determine a strongest threshold, or prove anything about its k-means SDP.

## Strict-margin certificate and robustness

The dual-style inequalities in Section 3 are valid for the precise primal LP. With α_j = d_{c(j),j} + t/|C_{c(j)}| and β_ij = max(α_j−d_ij,0), every selected center has β-row sum exactly t: its own-cluster contribution totals t, and the strict off-cluster inequalities remove the others. The off-center row sums are strictly less than t. Pointwise α_j−β_ij ≤ d_ij and nonnegativity yield the stated objective lower bound Σα_j−kt, attained by the specified integral point.

Uniqueness follows at the level of the full LP, not just the center choice. Equality forces every unselected facility variable to zero. The upper bound y_i ≤ 1 and the sum Σy_i = k then force each of the k selected variables to one. For a wrong selected center the pointwise objective inequality has positive slack, excluding any positive wrong assignment. Column normalization gives the unique remaining assignment. The argument needs the displayed upper bound on y_i; it is present in the source and in the candidate.

For a cost perturbation bounded entrywise by ε, rebuilding α changes each difference α_j−d_ij by at most 2ε. The positive-part function is 1-Lipschitz, so an unselected row sum changes by at most 2nε. Thus 2ε < γ and 2nε < η preserve all strict inequalities. Selected row sums remain exactly t under the rebuilt formula. Empty index sets simply impose no restriction. This also covers k=1 or k=n when the corresponding margin family is absent. No metric or randomness hypothesis is used in this certificate.

This is a standard sufficient dual-certificate mechanism. It is not a derivation of the off-center margins from perturbation resilience or from the source's k−1/k/k+1 objective gaps. The candidate explicitly states that residual gap.

## Independent checks and reproduction

The copied submitted verifier reproduced its receipt byte for byte: **8,267 exact assertions** passed. The separate `independent_checks.py` imports no author code and uses exact integers and rational numbers. Its **6,509 assertions** cover the assignment-generating-polynomial certificate, all metric inequalities, the universal perturbation margin, the fractional point, the three integral objective values, and the dual certificate on a separate six-point line metric. The positive-control margins are γ = 97 and η = 1. Single-entry perturbations in every positive and negative cost direction obey the predicted margins; these are finite controls supporting, not replacing, the general Lipschitz proof.

From this review directory:

```sh
python independent_checks.py > independent_results.replayed.json
cmp independent_results.replayed.json independent_results.json
```

For the author replay:

```sh
cd author_replay
python verify.py
```

Publish only the files listed in `review_summary.json`; omit downloaded source PDFs and caches. Source hashes and precise inspection scopes appear in `source_verification.json`.

The exact publication status remains **unresolved partial progress**. The finite-metric weak-resilience diagnostic and the robust strict-margin sufficient condition are valid; a meaningful source-style stability implication and the k-means SDP component remain outside the established results.
