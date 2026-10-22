# Attempt 2: Exact pair-scheduling invariant and involution route

Timestamp: 2026-10-03 13:53 UTC. Budget: 2/5. Exact-target completion estimate: 5%.

## Pair-scheduling identity

The additive pair-scheduling identity is established in [Ahn, Hendrey, Kim, and Oum, v2, Lemma 4.3](https://arxiv.org/abs/2110.03957v2). The formula below restates that prior mechanism using explicit mixed-rectangle indicators; it is not a new identity.
Fix disjoint vertex pairs P_i={a_i,b_i}, i=1,...,m, leaving at most one singleton. Define D_i={v in V(G) minus P_i : v is adjacent to exactly one of a_i,b_i}; in particular, neither endpoint belongs to D_i. Set h_i=|D_i|, d_ij=|D_i intersect P_j|, and q_ij=1 when the bipartite 2-by-2 adjacency rectangle P_i x P_j is nonconstant (otherwise 0). Put w_ij=q_ij-d_ij.

After exactly the index set S of pairs has been contracted, an existing pair-part P_i (i in S) has red degree

r_i(S)=h_i+sum_{j in S minus {i}} w_ij.

Proof: each uncontracted vertex contributes its original disagreement indicator. Replacing the two singleton vertices of P_j by their union replaces d_ij such contributions with the single red-indicator q_ij. This proves the formula directly from quotient partitions, without an assumption on the contraction history.

Unmerged singleton vertices have red degree at most |S|. Once all pairs are merged, there are ceil(n/2) parts, so arbitrary further contractions have red degree at most floor((n-1)/2). Thus for the conjectured bound D=floor((n-1)/2), it suffices to find pairs and an order whose every prefix S obeys r_i(S)<=D for every i in S. The singleton bound is automatic while there are unmerged pairs (for even n, |S|<=n/2-1; for odd n, |S|<=floor(n/2)).

This is a sufficient restricted-search formulation, not an equivalence to arbitrary twin-width sequences.

## A tractable symmetry class
Suppose an involutory automorphism has m two-element orbits and f<=1 fixed vertices. Use those orbits as pairs. Every cross-orbit rectangle has form [[a,b],[b,a]]. Consequently d_ij is either 0 or 2, and w_ij is respectively 0 or -1. Every fixed vertex is uniform to each pair. No existing pair's red degree can increase as other pairs are merged. Therefore

tww(G) <= max(max_i |D_i|, m+f-1).

Here the maximum over an empty set of pair-orbits is defined to be 0. For n=1, m=0 and f=1, the displayed bound is therefore 0, as required.

For graphs where max_i |D_i|<=floor((n-1)/2), this proves the conjectured bound by an explicit contraction sequence. It explains why inversion-type symmetry works for Paley and related graphs. This overlaps the existing symmetry proof in Ahn et al., Theorem 1.4, and Heinrich et al., Theorem 4.7; no novelty is claimed for the class result.

Gap: an arbitrary graph has no such automorphism, and pair rectangles with w_ij=+1 can increase an already saturated red degree. The next attempt tests whether low initial pair distances alone can replace symmetry.
