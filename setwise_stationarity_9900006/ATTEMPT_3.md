# Attempt 3: subsequence convexification and arbitrary-space random-time coupling

2026-10-20. Target: Thorisson Problem 3.2. This is a proved, full-path coupling criterion with explicit scope. It does not require the recoupled comparison variables to be one stationary orbit; that distinction must accompany any claim based on it.

## The theorem

Let (S,Σ) be any measurable space, θ:S→S measurable, μ a probability, and ν a θ-invariant probability. Put μ_n=θ^n_*μ for n∈N₀. Throughout, ||α−β||_TV=sup_{A∈Σ}|α(A)−β(A)| for probability measures. The following are equivalent.

(A) μ_n(A)→ν(A) for every A∈Σ.

(B) For every strictly increasing sequence of nonnegative integers 0≤n_1<n_2<... and every positive sequence ε_j, there are finitely supported probability vectors (a_{j,k})_{k≥j} such that

    ||Σ_{k≥j} a_{j,k} μ_{n_k} − ν||_TV < ε_j.

(C) For every such subsequence there is ONE probability space carrying X with law μ, integer-valued K_j≥j, variables Y_j with law ν, and measurable success events H_j such that:

- each K_j has finite deterministic support and the entire sequence (K_j) is independent of X;
- θ^{n_{K_j}}X = Y_j at every point of H_j;
- P(H_j^c)≤2^{-j}; hence almost surely equality holds for all sufficiently large j.

Equality in the last bullet is guaranteed on explicit measurable events; no measurability of the diagonal of S×S is assumed. In particular, (C) retains the full law of ONE original X and samples its actual orbit, rather than independently rebuilding its shifts. In the path-space specialization, each comparison Y_j is a full-path stationary-law variable. They need not form the orbit of one stationary process, and K_j need not be independent of Y_j or H_j.

## (A) implies (B): a full functional-analytic argument

Define the finite dominating measure λ=ν+Σ_{n≥0}2^{-n-1}μ_n. Write f_n=dμ_n/dλ and g=dν/dλ. Setwise convergence implies ∫h(f_n−g)dλ→0 for every bounded measurable h: first prove it for simple h, then approximate a bounded h uniformly, using ∫|f_n−g|dλ≤2. Thus f_n converges weakly to g in L1(λ), whose continuous dual is L∞(λ).

For any subsequence tail {f_{n_k}:k≥j}, g belongs to its L1-norm closed convex hull. Otherwise real Hahn–Banach separation of a point from a closed convex set would supply h∈L∞(λ) and c>0 such that ∫h(f_{n_k}−g)dλ≥c for every k≥j, contrary to weak convergence. A point of the (unclosed) convex hull is a finite convex combination, so such combinations approximate g arbitrarily closely in L1. For probability densities the supremum-event TV distance is one half their L1 distance. This proves (B).

This argument uses all bounded measurable tests on the WHOLE space S. It does not pass from cylinder convergence to full-path convergence, and assumes neither countable generation nor separability of the measure algebra.

## (B) implies (C): explicit product-space realization

Apply (B) with ε_j=2^{-j}, obtaining q_j=Σ_k a_{j,k}μ_{n_k}. Let r_j=q_j∧ν denote the measure with density min(dq_j/d(q_j+ν),dν/d(q_j+ν)) relative to q_j+ν. Its mass is 1−δ_j, where δ_j=||q_j−ν||_TV<2^{-j}. Let b_j=dr_j/dq_j, chosen everywhere measurable with values in [0,1] by modifying a null set if necessary. If δ_j>0 let β_j=(ν−r_j)/δ_j; if δ_j=0 set β_j=ν.

Take the countable product probability space carrying mutually independent coordinates:

- X with law μ;
- K_j with the finitely supported probability vector (a_{j,k})_{k≥j};
- U_j with uniform law on [0,1];
- Z_j with law β_j.

Countable products of probability measures exist on arbitrary measurable factor spaces. The residual samples Z_j are coordinate projections with their own prescribed laws; no assertion is made that an arbitrary S-valued distribution is a measurable function of a uniform random variable.

Define pointwise

    V_j=θ^{n_{K_j}}X,
    H_j={U_j≤b_j(V_j)},
    Y_j=V_j on H_j, and Y_j=Z_j on H_j^c.

The map V_j is measurable because K_j has finite support and θ has measurable iterates. H_j is measurable. For each A∈Σ,

    {Y_j∈A}=(H_j∩{V_j∈A})∪(H_j^c∩{Z_j∈A}),

so Y_j is measurable. By definition Y_j=V_j at every point of H_j. This is a pointwise construction of equality on a measurable success event, not a claim that a canonical product measure is supported on a potentially nonmeasurable diagonal.

Independence gives Law(V_j)=q_j and

    P(H_j^c)=∫(1−b_j)dq_j=δ_j,
    P(Y_j∈A)=∫_A b_j dq_j+δ_jβ_j(A)=ν(A).

The entire sequence (K_j) is independent of X. The construction also makes its entries mutually independent, although the theorem does not need that extra property. Neither independence of K_j from Y_j nor mutual independence of the final Y_j is asserted.

Finally, E=⋃_{J≥1}⋂_{j≥J}H_j is measurable, and the union bound gives

    P(⋃_{j≥J}H_j^c)≤Σ_{j≥J}δ_j→0.

Thus P(E)=1, and at every point of E equality holds for all sufficiently large j. No independence of the success events, no regular conditional distribution, and no measurability of the entire equality event in S×S is required.

## (C) implies (A): the universal subsequence quantifier is decisive

Suppose (A) fails. There are A∈Σ, η>0, and a subsequence n_k such that either μ_{n_k}(A)≥ν(A)+η for every k, or μ_{n_k}(A)≤ν(A)−η for every k. Select this subsequence in (C). Independence of K_j and X yields

    P(θ^{n_{K_j}}X∈A)=Σ_k P(K_j=k)μ_{n_k}(A),

which remains on the same side of ν(A) by at least η. But equality on H_j and Law(Y_j)=ν imply the absolute difference is at most P(H_j^c)≤2^{-j}, a contradiction.

## Exact reach and unresolved interpretation

This is an arbitrary-measurable-space, full-path theorem, not just a finite-partition restatement. It gives explicit random-time couplings of a single original orbit, with exact agreement eventually against a varying sequence of stationary-law comparison variables. Its cost is universal quantification over deterministic subsequences and permission to reselect the coupling and random-time weights for each subsequence.

It does NOT establish a single joint law of (X,X′) and times under which the same stationary X′ supplies every comparison through its shifts. Nor does it assert a finite exact/distributional coupling time as defined in Thorisson's Section 3. It is a proved broad coupling characterization: it is necessary and sufficient for exactly the stated full-path setwise convergence on arbitrary measurable spaces. The source does not explicitly require a single-pair format. Whether this auxiliary-copy formulation is the intended or novel resolution of the named problem is nevertheless unverified. In particular, it does not provide one stationary orbit, and it must not be confused with the specific aligned-pair property SC obstructed in Attempt 2. Other two-process formulations are not ruled out by that obstruction.
