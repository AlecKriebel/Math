# Minimax obstruction to universal additive, translation-invariant hazard certificates

## Status and purpose

This is a structural obstruction to a specified proof method, not a Devil strategy and not a disproof of the Time-Bomb conjecture. It explains why merely replacing an independent-step kernel by an arbitrarily shaped spatial kernel does not repair a universal additive nonincrease certificate. The conclusion follows from the certificate's hypotheses; an actual policy may win using decreases or information the certificate discards.

The game remains the exact two-dimensional king-move Time-Bomb game, with one announcement after each Angel move. Put M={−1,0,1}².

## 1. The proposed class of certificates

For each integer h≥0 let K_h:Z²→[0,∞) be finite-valued. A future hazard atom is specified by relative position z and remaining time h≥1. For a finite list of such atoms with nonnegative weights w_(z,h), define the potential before an Angel move as

    Φ = sum_(z,h) w_(z,h) K_h(z).

If the Angel chooses increment δ∈M and there is no new announcement yet, the new potential is

    Φ_δ = sum_(z,h) w_(z,h) K_(h−1)(z−δ).

The kernels are translation-invariant: only the displacement from the current Angel position enters. They have no additional configuration-dependent or multiscale internal state. Assume the following **universal nonincrease property**:

    For every finite nonnegative weighted hazard field,
    some δ∈M satisfies Φ_δ≤Φ.                                  (U)

Also assume K_0(0)≥1, so landing on a lethal atom of unit weight forces potential at least one. All other kernel values are nonnegative.

The universal weighted-field hypothesis is essential. It is satisfied if the proposed argument asserts the same inequality for arbitrary nonnegative hazard functions, as weighted smoothing/composition arguments often do. It is also enough to require (U) for every finite multiset of unit atoms; rational approximation and scaling recover the weighted version. A method that proves its inequality only on a smaller invariant family is not covered without an additional argument.

## 2. Exact minimax representation

**Theorem 1.** Property (U) holds if and only if there is a probability distribution π on the nine king increments such that, simultaneously for every h≥1 and z∈Z²,

    K_h(z) ≥ sum_(δ∈M) π(δ) K_(h−1)(z−δ).                    (1)

The same π must work for every remaining time. This shared distribution is imposed by simultaneous protection of mixed timestamps.

**Proof.** If (1) holds, the π-average of Φ_δ is at most Φ, so at least one move has Φ_δ≤Φ.

For the converse, index the pairs (z,h) by i and put

    D_i(δ)=K_(h−1)(z−δ)−K_h(z).

Fix any finite index set J. If there were no probability vector π with sum_δ π(δ)D_i(δ)≤0 for every i∈J, then the convex hull of the nine vectors (D_i(δ))_(i∈J) would be disjoint from the closed negative orthant in R^J. The hull is compact. Strict separation therefore gives nonnegative coefficients λ_i, not all zero, such that

    min_(δ∈M) sum_(i∈J) λ_i D_i(δ) > 0.

The coefficients are nonnegative because otherwise the separating functional would be unbounded above on the negative orthant. The displayed strict inequality contradicts (U) for the field with weights λ_i. Thus such a π exists for every finite J.

Each row inequality defines a closed subset of the compact probability simplex on M. Their finite intersections are nonempty, so their full intersection is nonempty. Any π in that intersection satisfies (1). ∎

**Finite dual certificate.** If a proposed kernel family has no common π satisfying (1), the same proof yields a finite list of positions/times and nonnegative weights for which every one of the nine Angel moves strictly increases the potential. Thus failure is witnessed by a finite linear-program dual certificate; one need not search infinite bomb schedules to refute the universal nonincrease claim.

Strictness also permits replacing the λ_i by sufficiently close nonnegative rational numbers and scaling to integers. Consequently a failure witness can be a finite multiset of unit hazard atoms, rather than requiring fractional bombs. Such a multiset may count redundant announcements separately; this observation does not assert that an indicator-only certificate ignoring duplicate pairs has property (U).

## 3. Forced independent-step majorization

Let P_h(z) be the law of the sum of h independent increments, each with distribution π from Theorem 1. Iterating (1), and using K_0≥1_{0}, gives

    K_h(z) ≥ P_h(z)    for every h≥0 and z∈Z².               (2)

In particular the freedom to choose arbitrary kernel shapes has not removed the independent-step lower bound: it was forced by universal linear nonincrease itself.

**Theorem 2.** Every kernel family satisfying the preceding assumptions obeys

    sup_z K_h(z) ≥ 1/(50h)    for every integer h≥1.         (3)

**Proof.** Write S_h for the independent-increment sum and μ_h for its mean. Every coordinate of one increment lies in [−1,1], so each coordinate of S_h has variance at most h. Chebyshev's inequality and the union bound show that, with probability at least 1/2, both coordinates of S_h−μ_h have absolute value at most 2sqrt(h). This square contains at most

    (4sqrt(h)+1)² ≤ 25h

integer points. Therefore some point has probability at least 1/(50h). Equation (2) gives the same lower bound for K_h. ∎

## 4. Consequence for the usual worst-increment argument

For a single terminal time T, one common sufficient argument would charge an announcement made with h moves left by

    c_h = sup_z K_h(z),

use only that Angel moves do not increase the potential, and conclude safety from

    sum_(h=1)^(T−1) c_h < 1.

Theorem 2 makes this sum at least (1/50)sum_(h=1)^(T−1)1/h. It therefore cannot stay below one for every T.

This conclusion already holds in the single-terminal-time subproblem. The actual unrestricted game introduces further coupling across timestamps, so it cannot repair this particular certificate merely by adding more deadlines.

This is not a claim that the Devil can realize all worst increments while preventing favorable Angel decreases. It is specifically a failure of a proof that discards all such decreases and charges every announcement its global worst increment.

## 5. Absolute-time-dependent kernels do not remove this obstruction

The same conclusion holds if the kernels are K_(n,h)(z), where n is the current absolute time, provided they remain translation-invariant and obey the universal transition condition

    min_δ sum w_(z,h) K_(n+1,h−1)(z−δ)
        ≤ sum w_(z,h) K_(n,h)(z)

for every finite nonnegative mixed-age field and every n. Assume K_(n,0)(0)≥1 at every n.

The minimax argument gives a probability distribution π_n for each n, common to all h,z at that n. Iterating yields domination by the law of independent, not necessarily identically distributed, increments with laws π_n,…,π_(n+h−1). Coordinate variances still add to at most h, so (3) holds for every K_(n,h). Charging a fixed terminal time T along n=1,…,T−1 again produces the divergent harmonic lower bound.

## 6. Exact limitations and the direction not excluded

The result does not cover:

- configuration-dependent or nonlinear hazards;
- a transition inequality restricted to a properly maintained subset of states;
- proofs that quantify and use strict decreases on Angel moves;
- kernels with genuine location dependence beyond relative displacement;
- internal state such as nested regions, remembered choices of scale, or correlated continuation choices.

In particular, the nested-square terminal strategy and the peak-aware three-deadline repair carry internal region/scale information and are not refuted here. The obstruction says that an arbitrary spatial kernel alone cannot replace that information while keeping the universal additive nonincrease/worst-increment proof unchanged.

No preloaded configuration is claimed to be forceable from the empty initial state. The finite dual witness refutes a universal inequality; it does not establish an unrestricted losing game state reachable under every Angel response.
