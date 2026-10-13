# Weakened Wills inequality: accepted restricted progress

Problem 30000114, rank 1217, source alias OWR-741-008. Approach 1 of 5.

**The unrestricted problem remains unresolved.** The independent audit accepts the bounded-lattice-width theorem, hollow-body corollary, lower-dimensional lattice-hull reduction, necessary large-width condition, and the limited coefficientwise Ehrhart obstruction.

The original question asks whether, for each fixed n, some finite c(n) gives

    G(K) <= V_n(K) + V_(n-1)(K) + c(n) sum_(i=0)^(n-2) V_i(K)

for every compact convex K in R^n. Both leading coefficients are exactly 1. The accepted restricted estimate is, for every primitive integer normal a,

    G(K) <= V_n(K) + V_(n-1)(K)/||a||
            + A_n (floor(w_a(K))+1) sum_(i=0)^(n-2) V_i(K),

where A_n depends only on n. It preserves arbitrary translations and degenerate-body cases. The dependence on width is not removed.

Every divergent normalized target-residual sequence must have lattice width tending to infinity. Large lattice width does not force large Euclidean inradius, as the exact unimodular-shear example shows. The height-one-pyramid example refutes an auxiliary coefficientwise estimate, not the original target; the Euclidean-minus-lattice surface deficit must be retained.

## Reading order

- [APPROACH1.md](APPROACH1.md): the complete restricted proof, exact formulas, prior results and remaining gap.
- [AUDIT.md](AUDIT.md): the independent mathematical audit, including precision repairs and boundary cases.
- [SOURCE_LEDGER.md](SOURCE_LEDGER.md): public source identities, applicability and retrieval/inspection history.
- [PROVENANCE.md](PROVENANCE.md): attribution, exact report identities and editorial boundary.
- [STATUS.json](STATUS.json) and [MANIFEST.json](MANIFEST.json): scoped disposition and publication inventory.

Established results of Henk--Wills, Blichfeldt, Betke--Böröczky and classical flatness theory are credited. Historical novelty has not been established. The proof and audit are AI-assisted and unrefereed; this is not external human peer review or proof-assistant certification. This edition changes no queue entry or historical approach count.
