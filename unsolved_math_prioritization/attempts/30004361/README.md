# Majority three-coloring: accepted approach-1 partial results

**The original problem remains unresolved after approach 1 (1/5).** This edition publishes the full written report and full independent AI audit, with explicit evidence limits. It supplies no proof or counterexample for the full assertion, no claim of novelty, and no comprehensive current-literature assessment.

The question asks whether every finite 6-regular, 6-uniform hypergraph has a three-coloring in which each edge contains at most three vertices of any color. Each edge has six distinct vertices; indexed edges may repeat. The report proves the universal equivalence with the simple-regular and maximum-degree-six formulations, so this convention is explicit rather than silently changed.

## Reading order

- [APPROACH1_REPORT.md](APPROACH1_REPORT.md): full approach-1 report, preceded by an edition notice.
- [AUDIT_REPORT.md](AUDIT_REPORT.md): full independent written audit, preceded by an edition notice.
- [ACCEPTANCE.md](ACCEPTANCE.md) and [STATUS.json](STATUS.json): accepted scope and exact limitations.
- [PRECISION_NOTE.md](PRECISION_NOTE.md): the nonblocking distinction between two sufficient Local Lemma thresholds.
- [PROVENANCE.md](PROVENANCE.md): byte identities, editorial treatment and publication boundary.
- [SOURCE_MANIFEST.json](SOURCE_MANIFEST.json) and [SOURCE_CHECKS.json](SOURCE_CHECKS.json): original public-source metadata and recorded independent source checks.
- [MANIFEST.json](MANIFEST.json): exact edition membership and byte identities.

## What the included written arguments establish

The complete report and audit retain the 36-copy regularization construction, equivalence of multiplicity conventions, exact pairing reformulation, maximum-degree-three theorem, potential and one-vertex change identities, and the theorem for maximum degree six on at most eleven vertices, including repeated edges. The last theorem implies that any counterexample to the target must have at least twelve vertices. These conclusions come from written mathematical arguments, not extrapolation from finite tests.

The projective-plane argument proves that no subset of PG(2,5) meets every line in two or three points. This is an obstruction to a stronger preliminary extraction requirement. The elementary bad-edge probability and dependency calculation rule out the stated direct symmetric Local Lemma sufficient conditions for this distribution and bound. Neither argument proves the original assertion false or excludes other probabilistic methods.

## Displayed finite example and omitted auxiliary evidence

The report itself contains the 15-vertex edge list, starting coloring, 450-move potential histogram and explicit three-vertex repair. All are retained as authored. The audit records its exhaustive verification of these properties. The histogram has 52 neutral moves and no strictly improving move, so the example is a non-strict local minimum for recolorings of at most two vertices. Its displayed valid repair shows that it is not a counterexample to the target.

No checking programs, machine-readable fixtures, per-move result lists, computational output files or logs accompany this edition. The displayed example can be inspected from the report's text, but no executable reproduction of its 450-move calculation is supplied. The other local-search examples, the PG(2,5) positive coloring of class sizes (11,10,10), and supplementary finite consistency tests appear only as historical reports of the original checks. In particular, the PG(2,5) positive coloring vector is not included; the written nonexistence argument for the stronger two-or-three-points subset condition is included. This edition does not claim that every finite-check result in the preserved report and audit is independently reproducible from its included files.

The original reproduction commands and references to the original packet's MANIFEST.json remain in the historical text. They do not refer to runnable materials or to this edition's different MANIFEST.json. No omitted fixture or program was transcribed into a replacement prose artifact.

## Source and review limits

The target is Tibor Szabó's question in [Oberwolfach Report 1/2020, pp. 83–84](https://ems.press/content/serial-article-files/46836?nt=1), also appearing as Problem 1 on page 13 of [Anastos–Lamaison–Steiner–Szabó, Majority Colorings of Sparse Digraphs](https://page.mi.fu-berlin.de/szabo/PDF/MajorityColorings.pdf). The subcubic result invokes [Brooks' theorem](https://doi.org/10.1017/S030500410002168X). Source metadata records the scope and date of the original inspections; packaging is not a new source-reading pass.

The review is AI-assisted mathematical auditing, not human peer review or formal verification. This addition changes no queue file and adds no substantive proof-search approach. It contains authored mathematical prose and public-source metadata, with no copied third-party source documents, datasets, private sources or private coordination material.
