# Colorings without disjoint color-isomorphic triangles

Problem **30006563 / OWR-14299905-038**, five attempts completed. **Unsolved, 5/5.** The exact asymptotic target remains unresolved; this packet contains independently checked partial results. It is AI-assisted and unrefereed, with no novelty claim.

## Verified results and remaining question

- An explicit three-color K9 proves **g(n) <= n-6 for every n >= 9** by a fresh-color vertex extension. This is a hand-proved constant improvement on the upper bound displayed in the source, not an asymptotic resolution.
- **g(6)=g(7)=2** has an elementary proof. **g(8)=g(9)=3** additionally uses a complete, replayable Boolean impossibility certificate for two colors on K8.
- The other attempts prove scoped deletion, intersecting-family, common-neighborhood and monochromatic-cut statements, and identify their missing general steps.
- Neither g(n)=Theta(n) nor g(n)=n-O(1) has been established or refuted.

The original report concerns **arbitrary edge-colorings**, not just proper colorings. Triangle colors are actual labels with multiplicities. The source credits Conlon, Fox and Pham with g(n) >= c*n^(1/2+epsilon), for unspecified positive constants; no explicit exponent or proof is supplied there. The packet preserves this attribution and its limits. See [primary source](https://publications.mfo.de/handle/mfo/4435), Question 14 on printed page 74, and the [full source discussion](author/README.md#source-and-exact-scope). The exact catalog page could not be read directly.

## Proofs and independent validation

- [Authored mathematical summary](author/README.md)
- [Five complete proof attempts](author/attempts/turn_01.md), continuing through [Attempt 5](author/attempts/turn_05.md)
- [Full independent adversarial audit](audit/AUDIT_REPORT.md): PASS for the scoped partial results; no mandatory mathematical repairs
- [Independent checker](audit/independent_audit.py), [results](audit/independent_results.json), and [24 explicit failed-construction witnesses](audit/ansatz_failure_witnesses.json)
- [K8 proof certificate](author/checks/k8_two_color_unsat_certificate.json) and [standalone author verifier](author/checks/verify_results.py)

The independent checker imports no author module and executes no author script. It reconstructs the colorings, verifies all 729 three-color triangle-isomorphism comparisons, rebuilds all 5,600 K8 clauses, checks 17,920 local truth assignments and complement symmetry, and validates all 571 proof-tree nodes, 3,847 unit assignments and 286 contradiction leaves. Its negative controls pass. The full audit distinguishes hand proofs, finite computations, restricted hypotheses and unresolved claims.

## Reproducibility and historical freeze

Use Python 3.10+ and its standard library. No network or source PDF is required. Copy this entire problem directory to a disposable location before running any script. From that copy, run:

    python3 audit/independent_audit.py
    python3 author/checks/verify_results.py

Run optional search reproductions on a separate disposable copy:

    python3 author/checks/small_two_color.py
    python3 author/checks/extend_k7.py
    python3 author/checks/test_pair_amplification.py

Search reruns overwrite output JSON, including timing values, and can change the frozen manifest. This is expected; do not run the original-freeze audit afterward on that modified copy. The exact finite upper construction has a complete written proof independent of the search output.

The `author/` directory is the byte-preserved pre-audit freeze; its earlier references to pending review and local publication state are historical. The complete mathematical audit is preserved, with only its absolute execution path sanitized. [CLARIFICATIONS.md](CLARIFICATIONS.md) records the two optional editorial improvements without rewriting the frozen attempts. [RESEARCH_LOG.md](RESEARCH_LOG.md) records the five substantive checkpoints. No sixth proof search, external researcher contact, merge, release, paper or DOI is part of this submission.
