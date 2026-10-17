# Acceptance: universal additive-kernel minimax obstruction

Shared PASS2 independent audit of `../pass2_devil/ADDITIVE_KERNEL_MINIMAX_OBSTRUCTION.md`, SHA-256 `71d45a1aa17e3a94e0e4981766aabf81125c2f0b37dfa8c06de611e37badf063`.

## Verdict

Accepted under its stated universal weighted-field hypotheses. This is an obstruction to a particular proof template, not a Devil winning strategy and not a claim that every additive-kernel policy loses.

## 1. Finite minimax step and infinite row set

Let D_i(delta)=K_(h−1)(z−delta)−K_h(z) for row i=(z,h). For a finite row set J, suppose no probability vector on the nine moves has every expected row value nonpositive. The convex hull of the nine column vectors is then disjoint from the closed negative orthant. A compact set and a disjoint closed set have positive distance here, so strict separation applies.

The separating functional must have nonnegative coordinates: a negative coordinate would make its supremum on the negative orthant infinite. That supremum is zero for a nonnegative functional. Consequently there are nonnegative weights lambda_i with

min_delta sum_i lambda_i D_i(delta)>0.

This is exactly a finite weighted field on which every Angel move increases the potential, contradicting the assumed universal nonincrease property.

Thus every finite collection of row constraints has a solution in the compact probability simplex. Each individual constraint is closed because every kernel value is finite. The finite-intersection property gives one probability vector pi satisfying every row simultaneously. Conversely, such a pi immediately proves universal nonincrease by averaging.

The use of one common pi across all remaining times is justified by the assumption that a single field may contain atoms with mixed timestamps. The proof does not silently replace that assumption by separate one-time inequalities.

Strict separation has a positive margin across only nine moves, so the finite real nonnegative weights can be approximated by nonnegative rational weights while preserving strictness. Scaling then produces integer weights. This verifies the finite-multiset dual-witness claim. It does not turn the witness into a forceable legal history, and it does not establish the property for indicator-only fields that ignore duplicates.

## 2. Independent-step majorization

The row inequality is K_h≥pi*K_(h−1). Nonnegativity permits iteration. Since K_0(0)≥1 and all other values are nonnegative, K_0≥delta_0, hence

K_h≥pi raised to convolution power h * delta_0.

The right side is the endpoint law of h independent king increments. No normalization of K_h itself is required. Unbounded global suprema cause no gap: they merely make a global worst-increment certificate unusable even sooner.

The accepted variance argument gives endpoint mass at least 1/(50h): each coordinate variance is at most h; at least half the mass lies in a square of at most 25h lattice points. Therefore sup_z K_h(z)≥1/(50h).

## 3. What the divergent sum actually proves

A method that charges every new bomb its global worst increment c_h=sup_z K_h(z), credits Angel moves only with nonincrease, and seeks safety from sum_(h=1)^(T−1)c_h<1 cannot establish all-terminal-time survival. Its charge sum is bounded below by a divergent harmonic sum.

The derivation does not show that Devil can attain all those worst increments along one play while suppressing all favorable Angel decreases. It therefore does not prove failure of the underlying minimizing policy. The distinction is explicit in the audited input and is essential.

## 4. Absolute-time-dependent extension

At each absolute time n, applying the same finite-row argument gives a common move distribution pi_n for that time's mixed-age inequalities. Iterating from (n,h) dominates the endpoint law of independent increments with laws pi_n,…,pi_(n+h−1). Coordinate variances still sum to at most h, so the same bound holds for each K_(n,h).

For a fixed terminal time T, announcements made at n=1,…,T−1 have remaining lengths h=T−n. Summing their respective worst increments again dominates (1/50) times the harmonic sum through T−1. Thus the stated extension is correct.

## Exact limits

The theorem assumes universal nonincrease for every finite nonnegative weighted field. A proof restricted to a maintained family of reachable states, nonlinear/configuration-dependent hazards, absolute spatial dependence, internal region/scale information, or quantified favorable decreases need not satisfy it. In particular, the nested-square and concentration-profile constructions use retained region/scale choices and are not contradicted by this result. The supplied document preserves these limits throughout.
