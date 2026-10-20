# Attempt 4: can the random-time criterion use a single comparison process?

2026-10-20. This attempt tests two natural strengthenings of Attempt 3 and proves exactly where they fail. Neither strengthening solves the target.

## 1. A fixed target is impossible even for an already stationary process

Take S={0,1}^{N₀}, and let μ=ν be fair iid Bernoulli path measure. Suppose the random-time criterion of Attempt 3 could take Y_j=Y for one common ν-law path Y. Let K_j have finite deterministic support, K_j≥j, and let the entire sequence (K_j) be independent of X. Put V_j=θ^{n_{K_j}}X. Assume P(V_j and Y disagree on their zeroth coordinate)→0; this is weaker than eventual full-path equality on high-probability success events.

Fix j. When l exceeds the maximum of the finite support of K_j, K_l≥l implies K_j≠K_l surely. For each possible pair of sampled indices, the selected coordinates of X are distinct iid fair bits. Summing over the finitely many possible pairs gives the same disagreement probability without invoking any regular conditional distribution. Independence of the entire index sequence from X is essential here. Hence

    P((V_j)_0≠(V_l)_0)=1/2.

If both (V_j)_0 and (V_l)_0 approached Y_0 in probability, the union bound would make this probability arbitrarily small for all sufficiently large j,l, a contradiction. Thus a common unshifted stationary-law target is impossible under these independent random times, despite exact stationarity of μ itself.

This strengthens the fixed-target obstruction in COUPLING_CRITERIA.md: arbitrary finitely supported independent random-time sampling cannot repair it.

## 2. One aligned pair chosen before all subsequences is exactly the rejected SC condition

Fix any coupling π of μ and stationary ν, represented by (X,X′). For A∈Σ write

    e_n(A)=Pπ(1_A(θ^nX)≠1_A(θ^nX′))≥0.

Consider the property: for EVERY deterministic subsequence n_k there are finitely supported probability weights a_{j,k}, supported on k≥j, such that for EVERY fixed A∈Σ,

    Σ_k a_{j,k} e_{n_k}(A)→0.

The weights can depend on the subsequence and π but must work for all fixed events. This property is equivalent to SC, namely e_n(A)→0 for every A.

SC implies the property simply by choosing a point mass at k=j. Conversely, if SC fails, some fixed A has e_{n_k}(A)≥ε>0 along an infinite subsequence. Every convex average over that subsequence is at least ε, contradicting the property. This proof needs no separability, topology, or measurable diagonal.

Equivalently, randomize a common sampled index K_j with weights a_{j,k}, independently of the entire pair (X,X′), and compare θ^{n_{K_j}}X with θ^{n_{K_j}}X′. Then its mismatch probability for A is exactly Σ_k a_{j,k}e_{n_k}(A). Independence from X alone would not justify this identity; this pair-independence convention is stronger than the independence used in Attempt 3. Thus independent randomization, even with freely chosen weights separately for every subsequence, gives no relaxation of SC when the ONE pair must be selected first. By the separately audited rank-one obstruction in Attempt 2, it is not necessary for setwise convergence.

## 3. The quantifier ordering left open

The statement

    for each subsequence there exists a possibly different coupling (X,X′)

is not disproved by Section 2; it reverses the crucial quantifier order. Attempt 3 does not prove that statement either, because its comparison variables Y_j need not be shifts of a common X′. It would be a genuine additional theorem to construct that original two-process coupling. Neither finite-partition maximal coupling nor the L1 separation argument supplies it automatically.

## Outcome

Two clean attempted upgrades fail: fixed unshifted targets fail for iid stationary paths; one aligned pair uniformly handling all subsequences is exactly SC and inherits its obstruction. The mathematically valid result at this stage remains the broader random-time coupling criterion of Attempt 3, with varying stationary-law copies and carefully stated quantifiers.
