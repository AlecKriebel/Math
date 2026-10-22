# Packaging acceptance, 2026-10-20 UTC

The packaged mathematical documents retain the independent audit’s restricted acceptance boundary. Status remains unsolved, 5/5; no originality or novelty claim is made. The exact target requires either a proof for all sufficiently large primes or counterexamples for unbounded primes, neither of which is provided.

Post-packaging replay checks:

- Count/Walsh identities: 256 colorings at p=5 and 4096 at p=7; exact pair law at p=10007.
- Independent audit: 80 seeded colorings with exact identities and all 24 telescoping permutations; 52 exact pair laws; quartic coefficients 513 and 252 and threshold arithmetic; all 256 patterns at p=263729, primitive root 3, minimum count 934.
- Four seam formulas: 400 tests, m=1 through 100. The written proof, not this sample, proves all m≥1.
- Local AP support checks: p=17,19,23,29,31,43. Pair-link example: components of sizes 11 and 1 at p=23. Global cardinality support is proved in text, not tested by this script.
- Independent Python exhaustive absence: p=5,7,11,13,17, node counts 13,47,1137,6959,160394.
- C++ exhaustive absence: p=5,7,11,13,17,19,23,29, node counts 11,21,309,1113,9947,25051,180787,3086007.
- The recorded relaxed SAT witnesses are validated against every ordered modular progression and their stated relaxed sizes. Historical relaxed UNSAT and timeout searches are retained as historical exploratory records, not newly replayed here; none is a balanced counterexample.
- The fresh bounded p=31 result is recorded in replay/prime31.json and summarized in replay/summary.json. UNKNOWN does not imply absence.

Replay comparisons ignore timings and, for p=31, timeout-dependent node counts. All expected deterministic outputs match. These remain implementation-dependent computations, not formal proof certificates. The missing uniform pair-link large-component lemma remains unproved.

The package contains only text artifacts. There are no source PDFs/images, executable binaries, caches, private datasets, private coordination documents, or queue content. The package inventory covers payload bytes, not a claim of formal mathematical verification. No publication or queue modification is performed by the replay driver.
