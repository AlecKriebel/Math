# Restricted lower bounds and an exact-formula correction for C5 semisaturation

Problem 30001654 / OWR-4791-010. Approach 1 of 5.

**UNRESOLVED: this work does not establish or refute ssat(n,C5)=11n/8+O(1).** It contains two accepted restricted lower bounds, exact equality classifications in the stated scope, a structural lemma and an infinite construction refuting a separate optional eventual exact-equality suggestion in the inspected arXiv version of Füredi–Kim.

- Universal core: for n>=5, deleting the original leaves once gives H. If H has a universal vertex r and epsilon records whether r supports a leaf, then 8e(G)>=11n-11-3epsilon. Equality is exactly the hub over disjoint P4 blocks, with one leaf at each path vertex and optionally one at the hub.
- Rooted two-edge paths: if every other vertex is reached from r by a simple path of exactly two edges, then 8e(G)>=11(n-1)+w, where w counts nonleaf vertices outside N[r]. The proof includes the no-leaf strengthening and the one-root-leaf corollary. Equality is classified for the unstrengthened bounds, with K1/K2 exceptions explicitly qualified.
- Infinite correction: for every t>=1, the extra-hub-leaf family has n=8t+2 and e=11t+1, strictly below ceil(11(n-1)/8)=11t+2. This disproves only the optional eventual exact ceiling equality in arXiv:1103.0067v1, not its upper-bound inequality or asymptotic conjecture.

No reduction of arbitrary extremal graphs to either rooted class is proved. K3,3 shows that the structural hypotheses cannot simply be dropped for all semisaturated graphs.

## Reading order

1. [UNIVERSAL_CORE_THEOREM.md](UNIVERSAL_CORE_THEOREM.md): complete theorem, equality cases and all seven nonedge classes.
2. [ROOTED_TWO_PATH_BOUND.md](ROOTED_TWO_PATH_BOUND.md): complete stronger rooted inequality, equality, corollaries and auxiliary structural lemma.
3. [AUDIT_AND_ACCEPTANCE.md](AUDIT_AND_ACCEPTANCE.md): complete mathematical audit and exact acceptance boundary.
4. [SCOPE_CLARIFICATION.md](SCOPE_CLARIFICATION.md): explicit trivial-order qualifications.
5. [SOURCE_LEDGER.md](SOURCE_LEDGER.md): attribution, public-source identities and bounded search/retrieval/inspection history.
6. [PROVENANCE.md](PROVENANCE.md), [STATUS.json](STATUS.json) and [MANIFEST.json](MANIFEST.json): authorship, editorial boundary, status and exact inventory.

The proof and audit are AI-assisted and unrefereed. There is no claim of external human peer review or formal proof-assistant certification. The original construction and leaf lemmas are credited to Füredi–Kim. No first-discovery priority, global extremality, exact finite semisaturation value, defect in an uninspected journal version, or exhaustive literature-status certification is claimed.
