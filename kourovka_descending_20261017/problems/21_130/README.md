# Kourovka21.130 research record

The full conjecture remains **unsolved**. STATUS.md and CLAIM_LEDGER.json distinguish checked partial results from the exact remaining gaps. No preprint or Zenodo upload is authorized by these partial results under the project publication rule.

The universal finite-cardinality proof is in combinatorial/universal_small_proof.md. Explicit contradiction DAGs for n3–7 are checked by combinatorial/verify_certificate_minors.py using exact rational ranks and Bareiss determinants; this verifier does not import the lattice search/HNF implementation. Independent adversary reports are in review_partial1/.

The p-group finite-cardinality proof is algebraic/FORMAL_GROUP_TRANSFER.md, with exact coefficient witnesses in algebraic/polynomial/SLACK_RESULTS.md and algebraic/COEFFICIENT_EXTENSION.md. The primary Lubin–Tate input is cited in algebraic/SOURCE_PROVENANCE.md. Fresh formal and arithmetic audits are in formal_fresh_review/; individual witness gcds suffice for the theorem, and full support at larger n is not assumed.

The finite_search/REPORT.md gives commands for the finite search and its standalone verifier. Run verification/root_large_certificate_audit.py from ordinary Python3 to independently verify all530233positive stored cycles and exact stated exhaustive domains with tuple arithmetic. The530155distinct group-subset pairs include overlaps between samples and exhaustive domains. Seventeen failed heuristic searches are UNKNOWN, not negative certificates. Data are positive witnesses, not an unrestricted proof.

Root relation_cover/REDUCTION.md proves the exact collision-cover reformulation; its exploratory search uses SymPy1.14.0 (requirements.txt). Root n7search is historically incomplete; the independent later completed symbolic n7certificates supersede it for that cardinality. The general all-n reformulation remains an unsupported central difficulty. The seven-point mixed-prime modeling obstruction has its own explicit successful cycle and fresh adversarial review.

Raw third-party sources, local environments, and duplicated frozen audit snapshots are intentionally local caches; versioned source manifests retain URLs/hashes. All partial-result novelty remains unassessed. No independent human peer review or formal proof-assistant verification is claimed.
