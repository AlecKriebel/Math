# Identified dependencies

The family construction and exact projection are elementary and self-contained. The exact-core argument uses the following accepted proofs and audits, each read in full and byte-checked before its independent acceptance:

1. [Boundary extension and mixed-constraint proof](../3251_boundary_core_20261012/BOUNDARY_EXTENSION_PROOFS.md): incidence-at-most-two mixed constraints fail exactly on a pure odd cycle of two-sets all demanding bichromaticity. Repeated residual occurrences are allowed. This is the completion lemma used after propagation.
2. [Boundary/core acceptance](../3251_boundary_core_20261012/BOUNDARY_CORE_AUDIT.md): verifies the mixed lemma and boundary extension, including singleton repair and repetitions.
3. [High-incidence-core addendum](../3251_boundary_core_20261012/HIGH_INCIDENCE_CORE_PROOFS.md): for indivisible k>=3 graphs, chi(G[X])>=2k-3 and omega(G[X])>=k-1, with incidence measured in the original graph.
4. [Sharp-order acceptance](../3251_boundary_core_20261012/SHARP_ORDER_AUDIT.md) and [proof](../3251_boundary_core_20261012/SHARP_ORDER_PROOFS.md): a C5-free graph of chromatic number q greater than clique number r has at least 2q-r+2 vertices.
5. [Initial maximum-clique audit](../3251_divisibility_partials_20261012/HYPERGRAPH_AUDIT.md): records the source check of the Chudnovsky–Robertson–Seymour–Thomas K4-free odd-hole-free four-color theorem. This external theorem is used for the k=4 core-clique consequence. Its full external proof is not re-audited here.

The fifth dependency's intended public filename is checked against the initial edition. These links identify the intended repository layout, not a claim that either predecessor is remotely published. The exact-core argument does not need the companion family as a premise; the family demonstrates why the signed constraints cannot be replaced by a division of G[X].
