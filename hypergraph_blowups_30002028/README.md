# Hypergraph clique blow-ups: frozen unsolved attempt

Problem ID **30002028**, row **1836**, source key **OWR11781-001**.
Disposition: **UNSOLVED**, **5/5**. Six substantive approaches audited on 2026-10-21 UTC. No solution, disproof, or new unconditional improvement is claimed.

## Target and claim ledger

For fixed integers ell > r > 2 and fixed c > 0, the question asks whether every sufficiently large n-vertex r-uniform hypergraph with at least c n^ell copies of K_ell^(r) contains a balanced non-induced blow-up with disjoint parts of size at least gamma(c,ell,r)(log n)^(1/(r-1)).

1. Auxiliary clique hypergraph: establishes the imported generic exponent 1/(ell-1), not the target 1/(r-1).
2. Random construction: verifies optimality of the requested exponent as an upper scale for universal guarantees; it supplies neither the conjectured lower bound nor an optimal constant.
3. Joint-link averaging: proves an elementary reduction and a density-only residual obstruction. Arbitrary sparse random residuals are not shown to arise as joint links of the required dense host, so they are not structured-link counterexamples. Balancing yields an obstruction benchmark, not a new lower bound.
4. Jensen counting: audits homomorphism counts and collision subtraction. Its sufficient injectivity test is not necessary; no improved general embedding theorem follows.
5. Regularity/counting/blow-up lemmas: identifies missing uniform parameter dependence for a growing target, not an impossibility theorem for those methods.
6. The 2026 energy method: identifies the failed Cartesian-box identity for hypergraph links; a multilevel extension remains unproved, not ruled out.

The May 2026 Fox–Wigderson–Zhou manuscript explicitly retains the hypergraph extension as open. This bounded source review does not prove that no later result exists. Known graph, single-edge, and specified special-hypergraph cases do not settle ell > r > 2.

## Contents and verification

- ANALYSIS.md: six-route authored mathematical report.
- ACCEPTANCE_AUDIT.md: independent authored acceptance audit, including final acceptance and public-copy provenance.
- AUDIT_RESULT.json: disposition and frozen-input/public-copy digests.
- SOURCE_GATE.md and SOURCE_METADATA.json: authored source match, citations, retrieval/inspection history and public source hashes. No source documents are included.
- verify_integrity.py: inventory, digest and cross-reference checks plus tamper tests.
- MANIFEST.json: byte counts and SHA-256 digests of every other package file.

From this directory run:

    python3 verify_integrity.py
    python3 -O verify_integrity.py
    python3 verify_integrity.py --self-test
    python3 -O verify_integrity.py --self-test

These are file-integrity and tamper-detection tests only, not numerical experiments or mathematical proof verification. They do not retrieve or independently authenticate cited sources. Self-tests use temporary copies and leave this package unchanged. The manifest does not hash itself: its separately recorded SHA-256 is the external trust anchor. Replacing both the manifest and files can create a different internally consistent package.

Public copies remove administrative coordination wording without changing mathematical reasoning. The frozen accepted input report hash remains recorded separately from the public report hash. Copied third-party documents, dataset contents, extracted reading text, private sources, private paths and coordination material are excluded.
