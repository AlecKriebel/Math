# Accepted strengthening: simple oriented graphs

**Status:** complete strengthening accepted separately by the accompanying independent mathematical audit, 10 October 2026. The main construction remains unchanged. This appendix uses the same banks, formula encoding, and chip counts from Sections 2–6 of [MATHEMATICAL_REPORT.md](MATHEMATICAL_REPORT.md). Acceptance has the AI-assisted, unrefereed meaning stated in that report.

The reduction can additionally forbid antiparallel arcs. Keep the distinguished vertex r and its Q counter vertices. Use P return vertices t_1,...,t_P, rather than P-1. Use exactly these arcs:

1. r -> v for each counter v;
2. v -> t_j for j=1,...,q_b, if v is in the modulus-q_b bank;
3. t_j -> r for every j=1,...,P.

Thus all arcs follow the three-part cyclic order

    root -> counters -> return vertices -> root.

There are no loops, no repeated ordered pairs, and no antiparallel arcs. The outdegrees remain Q at r, q_b at every counter in bank b, and 1 at every return vertex. Strong connectivity follows because a modulus-P counter reaches every return vertex; every counter reaches r through a return vertex; and r reaches every counter. Removing r leaves a depth-one acyclic counter-to-return graph.

The exact graph counts are

    N'=1+Q+P,
    E'=Q+sum_b q_b^2+P.

These are respectively one more vertex and one more arc than the original construction. Counter offsets and the root's initial count remain unchanged, and every return vertex starts with zero. The total chip count is still C=Q+B-1.

The checkpoint proof is unchanged. After one root firing, a ready modulus-q_b counter fires once and sends q_b chips to q_b distinct return vertices. Stabilizing the return vertices returns exactly q_b chips to r. Each counter therefore again holds (a+k) mod q_b after k root firings and non-root stabilization, all return vertices are zero, and r holds Q+B-1-S(k). The root is stable exactly when all bank predicates hold. Both implications of the 3-SAT equivalence and all polynomial bounds from the main proof survive verbatim.

For trivial preprocessing cases, use the directed three-cycle r->s->t->r. The configuration (0,0,0) halts and the configuration (1,0,0) has an infinite legal periodic game. These are loopless simple strongly connected oriented graphs, so the reduction's fixed YES/NO cases also obey the strengthened restriction.

Accordingly, the separately accepted hardness theorem holds even for strongly connected simple oriented graphs that become acyclic upon deletion of one vertex. Membership is inherited from the same prior NP-membership theorem. This strengthening is mathematical scope, not a first-in-literature claim.
