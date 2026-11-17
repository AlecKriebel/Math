# Specialized conceptual-model response

Problem 9700002 / AMR-096-0002. Current disposition: **claimed_solved, 2/5 author turns**, in the explicitly bounded sense of a **specialized conceptual-model response**.

The independent audit accepts the turn-2 theorem and its adequacy as a specialized existence response to Aldous's toy-model request. This is a rigorous example of the joint marginal-demand and spare-connectivity phenomenon. Historical novelty, a universal theorem, and a canonical resolution of an open-ended modeling program are not claimed.

## Result and scope

A sparse bounded-degree binary tree supports dense left-to-right OD traffic: k sources, k destinations, k^2 streams. Each stream has the same independent Exp(1) growth-rate law at every graph size. Cheapest fixed-topology enlargement to carry twice initial demand determines all capacities. Terminal capacities grow as 2k and top-edge capacities as 2k^2; each finite network is then held fixed while demand grows.

Demand is affine, d_ij(t)=1+(t-1)X_ij, so its variance is (t-1)^2. It is not the primary page's illustrative linear-variance demand process. The exact marginal r_k=F'_(k,+)/S_k uses the actual offered-demand slope S_k=sum X_ij. With the initial denominator k^2 instead, the finite lower-phase value would be S_k/k^2; the same macroscopic near-one limit holds.

With explicit probability tending to one, below 2-delta_k every optimizer admits all demand and has the entire physical tree spare; above 2+delta_k every optimizer saturates every physical edge and the spare graph is edgeless. Here delta_k=8 sqrt(log(k)/k). This provides only an **upper bound** on a transition window, not its exact scaling, a matching lower bound, or an assertion that finite instances switch at exactly two. The all-optimizer claims apply to these outer phases. No critical r_k(2), finite-size expected curve, or optimizer-independent critical spare graph is claimed.

The mechanism is concentration of a growing number of fixed-noise OD streams together with optimized capacities. Total admitted throughput saturates; it does not fall. The model addresses the HOT/design alternative, not SOC, adaptive capacity growth, arbitrary demand matrices, or generic cyclic networks.

## Preserved record

The files under `turns/` are unchanged frozen research records. Their historical pending-review language is superseded by this disposition and the independent review, not silently edited. Turn 1 remains an illustrative partial with its fixed-noise obstruction; turn 2 supplies the accepted specialized response. The public review has only the explicitly documented administrative/path omissions. Public proof and test provenance is recorded in `PUBLIC_PROJECTION.json`.

## Required prior credit

- R. Hassin and E. Zemel, *Probabilistic Analysis of the Capacitated Transportation Problem*, Mathematics of Operations Research 13(1):80-89 (1988), [publisher](https://pubsonline.informs.org/doi/10.1287/moor.13.1.80).
- R. M. Karp, R. Motwani, and N. Nisan, *Probabilistic Analysis of Network Flow Algorithms*, Mathematics of Operations Research 18(1):71-97 (1993), [publisher](https://pubsonline.informs.org/doi/10.1287/moor.18.1.71).

These are longstanding random-transport antecedents. Neither their ingredients nor the combined construction here is claimed historically novel. The Hassin-Zemel attribution is an additive improvement; the frozen candidate proof has not been rewritten.
