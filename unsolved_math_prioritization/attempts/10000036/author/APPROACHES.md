# Three substantive approaches

Problem 10000036 / AMR-099-0036. Maximum allowed: five. Early stopping applies after a full candidate proof.

## 1. Fixed density insertion and deletion

The previously published insertion-tolerant construction suggests first adding an independent Bernoulli noise field and then deleting at a fixed positive rate. This repair cannot work when the intermediate graph Y already has quenched p_c(Y)=1: every positive-rate independent thinning of Y has no infinite component, directly by the definition of p_c. Conversely, fixed-density insertion over an everywhere-percolating core is covered by the Benjamini-Tassion robustness theorem. These facts rule out these particular two naive constructions, not all uniform finite-energy laws.

Outcome: no solution by this route. The next construction must coordinate the small noise rates with geometry.

## 2. Summable perturbations along a distinguished axis

There is an easy nonstationary model. On the axis edges {n e_1, (n+1)e_1}, n in Z, independently delete with probability 2^{-|n|-2}. Enumerate all off-axis edges as f_1, f_2, ... and independently open f_j with probability 2^{-j-1}. Every edge has a strictly intermediate Bernoulli parameter. The total number of missing axis edges and open off-axis edges is almost surely finite by the first Borel-Cantelli lemma. Hence the resulting graph contains infinite axis tails. For each p < 1, independent thinning makes every axis component finite; adding finitely many off-axis edges only joins finitely many finite components and cannot create an infinite component. Thus its quenched internal critical probability is one.

This law visibly depends on the chosen axis and enumeration and is not invariant. It therefore does not solve the problem. In particular, no uniform probability distribution on all lattice translates of a chosen origin is available. The role of the failed approach is to isolate the useful summability mechanism.

Outcome: a complete weaker construction, missing the required symmetry.

## 3. Equivariant perturbation of a one-ended spanning tree

Replace the distinguished ray by the coherent rays of an invariant one-ended spanning tree. Let s(t) be the size of the finite component behind tree edge t. Delete t with probability 2^{-s(t)}. For an edge e outside the tree, take the maximum M(e) of s(t) along its finite tree path and add e with probability 2^{-M(e)}. All these choices are independent conditional on the tree.

For any root ray and its finite-side cuts, the expected number of exceptional cuts is at most sum_{m>=1}(1+Delta m)2^{-m}. The full proof proves finite energy of the marginal output law, all-vertex simultaneous cut control, percolation, uniqueness, quenched critical probability one, full invariance, and translation mixing. A published factor-of-iid spanning-tree theorem supplies inputs in all dimensions d >= 2.

The deletion mechanism has a close antecedent in Haggstrom-Mester's one-ended-tree site construction. That paper's insertion flips are controlled by the complementary site cluster, and its cited proposition does not state the no-bypass estimate needed here. We have not treated the present critical-probability conclusion as an already stated result of that proposition. No novelty is claimed for this perturbation or its conclusion.

Outcome: complete candidate proof. Stop at three approaches; independent review remains necessary.
