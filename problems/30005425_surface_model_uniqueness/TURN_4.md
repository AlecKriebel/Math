# Turn 4 — Connected fixed-algebra families with every allowable genus

AI-assisted mathematical proof candidate; independent review pending. Original unresolved 4/5. This is an underlying-surface result, not a claim about the OWR tile-rotation quotient.

## 1. Construction and statement

For each k≥1, take k ordered copies of the turn-1 four-vertex quiver. Copy j has vertices 0j,1j,2j,3j and arrows a_j:0j→1j, b_j:0j→2j, c_j:1j→2j, d_j:1j→3j, e_j:2j→3j. Add z_j:3j→0_(j+1), for 1≤j<k. Let A_k be the radical-square-zero algebra on this quiver: its ideal I_k contains every length-two path. It is connected, acyclic and string, with 4k vertices and 6k−1 arrows, so dim A_k=10k−1.

For a binary vector ε∈{0,1}^k define a quadratic cover B_ε by retaining a_j c_j at every copy, retaining b_j e_j if ε_j=0 or c_j e_j if ε_j=1, and retaining e_j z_j and z_j b_(j+1) at every join. These are all its quadratic relations.

Then B_ε is a finite-dimensional saturated gentle cover of A_k, all such chosen covers have dimension (9k²+13k)/2, and their underlying surfaces have

g=Σ_j ε_j,    b=2k+1−2Σ_j ε_j,    p=p*=0.

In particular a single fixed connected string algebra has at least k+1 pairwise nonhomeomorphic finite-cover surfaces. The selected 2^k labelled covers realize every genus permitted by their common cycle rank β=2k. Their genus multiplicities among this selected family are the binomial coefficients. This does not assert there are no additional covers of A_k or certify novelty.

## 2. Algebra and permitted threads

At each original degree-three interior vertex exactly one composable pair is retained as a relation and one is permitted. At a join, d_j z_j and z_j a_(j+1) are permitted, while e_j z_j and z_j b_(j+1) are forbidden. Thus both the permitted and forbidden successor/predecessor bounds hold. Every available local choice is maximal, so the cover is saturated. Acyclicity implies finite dimension, and J_ε⊆I_k gives the stated quotient.

All threads a_j d_j concatenate through the z_j to make one central permitted thread with 3k−1 arrows and vertex sequence

(01,11,31,02,12,32,...,0k,1k,3k).

Each copy contributes two other threads. For ε_j=0 their vertex sequences are (0j,2j) and (1j,2j,3j); for ε_j=1 they are (0j,2j,3j) and (1j,2j). Each quiver vertex occurs exactly twice in this list of thread vertices. No trivial-thread convention enters. There are 2k+1 threads, one with 3k−1 arrows and k each with one and two arrows. Nontrivial paths belong to a unique maximal thread, so

dim B_ε=4k+(3k−1)(3k)/2+k(1+3)=(9k²+13k)/2.

## 3. Ribbon boundary-sum proof

Use the credited permitted-thread ribbon construction, equivalent to the PPP surface model (see PPP Remark 4.13 and the OPS construction). Before connecting the copies, each copy has one distinguished ribbon vertex corresponding to a_j d_j. The new central thread replaces these k vertices by a single vertex whose cyclic order is the concatenation of their cyclic orders. Every ribbon edge and every other cyclic order is unchanged.

For two ribbon graphs on disjoint connected surfaces, concatenating the cyclic orders at a chosen vertex of each is the ribbon-graph operation obtained by attaching a bridge between the chosen vertex disks, thickening it as an untwisted band, and contracting the bridge. The band joins one boundary component of each of the two previously disjoint surfaces. The contraction does not change the thickened surface. Thus this is a boundary connected sum: g=g1+g2, b=b1+b2−1. This argument does not require choosing the same boundary component in different summands, nor an isotopy of their dissections.

Apply this k−1 times. A copy with ε_j=0 has (g,b)=(0,3); one with ε_j=1 has (1,1), proved by explicit ribbon permutations in turn 1. Therefore genus adds to h=Σε_j and boundary count is (3k−2h)−(k−1)=2k+1−2h. No punctures occur because the quiver is acyclic. The result also satisfies the independent PPP identity 2g+b=β+1=2k+1.

This supplies an arbitrarily large topology difference within finite covers of a single connected A_k. Nevertheless turn 2's local surgery switches any one ε_j, so these examples also emphasize how a sufficiently broad tile-regluing equivalence can erase all the genus differences. They do not resolve which moves the source intends.

## 4. Reproducibility and status

Run `python turn4/verify_family.py`; stdout must match turn4/verification.json. It independently constructs all 510 selected covers for k≤8, computes their full ribbon permutations, boundary cycles, genus and dimensions, and compares against the separate PPP lozenge gluing for every k≤5. All 2,674 exact assertions pass. The all-k proof is the thread list and boundary-sum argument, not extrapolation from these checks.

Credit: PPP https://arxiv.org/abs/1807.04730v2, Theorem 4.10 and Remarks 4.11–4.13; OPS https://arxiv.org/abs/1801.09659. No novelty certification. Original unresolved 4/5, informal completion estimate 50%. The remaining fifth turn will isolate an exact general simultaneous-surgery statement and the source interpretation gap; no full result can be inferred from these topology examples alone.
