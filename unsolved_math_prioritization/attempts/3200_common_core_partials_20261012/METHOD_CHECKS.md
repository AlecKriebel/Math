# Six-unit method classification: coverage and reproduction boundary

This is a bounded computational classification of three sufficient coloring methods, accompanied by complete symbolic arguments. It is a different kind of evidence from the independent common-two-color theorem. The latter is symbolic and has no computational premise. The exact six-unit phase classification relies on completed exhaustive computation; the raw collections and implementations needed to rerun those computations are excluded from this prose edition.

## Mathematical domain and normalization

The graph is finite, simple and subcubic, not ordinarily three-edge-colorable, and three-edge-colorable after every edge deletion. A base palette A has exactly three colors. Exactly six exceptional edges replace one base color each by one exterior singleton color. The exterior colors may coincide arbitrarily. The main domain uses nonconstant omission patterns.

The methods use only support-edge incidences and color equalities. Their domain therefore consists of 47 support line-graph types, 203 exterior equality partitions and 121 nonconstant omission partitions, totaling 1,154,461 cases. This is exact finite normalization of arbitrary singleton exterior colors. It is not an arbitrary cutoff on exterior palette size.

The complete symbolic justifications for all three sufficient methods, including the strict-deficit permutation count and exact three-residual Hall criterion, are in METHODS.md and AUDIT_METHODS.md. The classification's negative cases mean that these sufficient methods do not establish a coloring, not that the original lists are uncolorable.

## Independent support coverage

The 47 types occur among all 156 unlabeled graphs on six vertices. All supplied representations were checked to be simple subcubic supports with exactly six edges and the intended line graph. Their permutation orbits are pairwise disjoint and together contain 9,463 labeled line graphs.

Two different endpoint-partition constructions each find 508,285 valid partitions of twelve labeled edge endpoints into vertex blocks of size at most three, after rejecting loops and repeated edges. The resulting labeled-line-graph set is exactly the union of the 47 type orbits. The auditor's block-based generation is distinct from the author's incremental endpoint-label generation. Original supports need not be uniquely determined by a line graph; the classification depends only on their common incidence relation.

## Three-program classification agreement

The author primary classifier, the author's separately written checker and the independent auditor's third classifier agree point for point on all 1,154,461 cases. The third classifier directly enumerates labeled ordinary words and all six permutations, rather than using the Hall shortcut. This is stronger than agreement of totals alone.

The ordered phases are disjoint:

- 1,095,050 cases satisfy strict deficit
- 56,674 additional cases satisfy universal three-residual completion
- 2,725 additional cases satisfy deletion-adaptive repair
- 12 cases remain unsettled by these three methods

The public aggregate file retains each program's per-support count strata, including the author's breakdown of unresolved cases by two or three omission colors. Numeric stratum indices identify the reported aggregate rows only. Graph masks, endpoint representations, pointwise classification streams and individual normalized case records are not distributed.

All 12 residual records use one common exterior color. They form nine support/color orbits. Four records form the K4 orbit, which cannot occur in an edge-critical ambient graph. The remaining eight are distinct patterns on seven support types. The full list of support shapes and both simple cyclic C6 omission words remain in the mathematical text; raw pattern, orbit and local-witness collections are excluded.

## Actual critical examples and exact failure quantifiers

All eight non-K4 patterns are realized in three critical fixtures with respectively 5, 7 and 7 vertices; 7, 10 and 10 edges; and matching numbers 2, 3 and 3. Thus ordinary non-three-colorability follows from the matching-capacity bound. A complete independent Cartesian enumeration confirms colorings after every edge deletion.

Across the eight selected examples, there are 72 ordinary deletion colorings and 432 coloring/permutation trials. Two examples have 12 successful trials each. Six examples have none: every ordinary coloring of the selected deletion graph blocks every deletion-derived repair. Two actual Kempe-component switches were verified to produce successful deletion-derived repairs. There are three underlying critical graphs, not six distinct graphs.

All eight examples nevertheless have independently checked proper full list colorings with the selected edge exterior. The public aggregate retains per-fixture deletion-coloring counts and per-example trial/success/extension results, without any raw coloring or conflict-pair collection.

The full explicit seven-edge example, its exact lists and edge order, symbolic six-permutation argument, successful full coloring (1,3,2,0,1,2,3), and failed extension across edge 34 remain in METHODS.md and SCOPE_CORRECTION.md. Its six ordinary deletion colorings produce 36 failed repair trials. A full list coloring can yield an ordinary coloring of G−F that does not extend to G−e. The false converse is explicitly retracted; no impossibility of giving the selected edge its exterior color is inferred.

## Uniform omissions and direct local checks

The symbolic uniform-omission proof first covers supports with an edge meeting at most two other exceptional edges. The remaining six-edge support types are exactly K2,3 and K4, with K4 excluded by criticality. The direct K2,3 boundary construction is preserved in full and does not use the stronger common-two-color theorem as a premise.

All 27 boundary words were checked. The independent audit also checked all 203 exterior equality patterns for every word, totaling 5,481 restoration checks. The exact three-residual Hall criterion was checked across all eight labeled incidence graphs on three vertices and all 27 omission words, totaling 216 graph/omission cases, with every proper ordinary word and all six permutations considered.

## Reproduction modes and deliberate failures

The audit regenerated eleven result files with exact agreement to the recorded originals. Its independent Python verifier gives identical results normally and under -O and -OO; its checks do not rely on removable assertions. Both independently authored C++ enumerators reproduce their outputs under undefined-behavior sanitization without findings.

All eleven deliberate negative controls were rejected:

1. Omit an ordinary coloring
2. Duplicate an ordinary coloring in place of another
3. Omit a palette permutation
4. Erase a genuine exterior conflict
5. Falsify positive list membership
6. Remove the selected edge's exterior color from a positive coloring
7. Falsify a repair-success count
8. Reinstate the false extension implication
9. Change a pointwise classification
10. Omit an exterior equality partition
11. Misreport a residual count

No timeout, heuristic cutoff or interrupted search was interpreted as a negative answer. This edition preparation verifies preservation and arithmetic but does not rerun the mathematical classification.

## Distribution limits

METHOD_AGGREGATES.json preserves mathematical count aggregates, all relevant scopes and modes. It excludes original input or output file identities, graph encodings, raw support/omission/orbit/witness/ordinary-coloring collections and raw pointwise streams. The complete symbolic method arguments, uniform-boundary proof and explicit authored nonextension example remain inspectable. Reproduction of the exact finite classification requires fresh implementations and regenerated raw records. Neither this edition nor its manifest claims that those excluded records are supplied.
