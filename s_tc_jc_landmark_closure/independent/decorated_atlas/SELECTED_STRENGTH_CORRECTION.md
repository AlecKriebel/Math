# Selected core-retention corrections

Status: **VERIFIED AFTER CORRECTION, WITH A SEMANTIC LIMITATION**.

The historical filename is retained so links to the first audit do not break.
The certified predicate is now named `selected_retains_strong_core`. It is not
an intrinsic selected-network `S_TC` classifier.

## Preserved dummy-repair failure

The pre-correction release is identified by manifest body hash

```text
16e15131c2a77cc51f75626286e01c0f815a0b8b4811299dba876a172ed6f333
```

It generated only fully selected primitive factors. Its relation records
marked every outgoing port as `selected_support` and contained no dummy
completion universe or core-retention predicate. Thus its primitive counts
were internally correct, but it could not justify a downstream rule that
declared failure merely because one chosen completion contained a dummy repair
leaf. The exact failure is preserved in
`certificates/selected_core_retention_dummy_failure.json`.

## Exact core-retention criterion

For a contracted directed core, let `X` be its path-sink reticulations and let
`R` be its computed family of minimum ordinary-segment repairs. A selected
restriction retains that original core as a strong factor exactly when

1. every sink in `X` has its selected child port; and
2. the ordinary segments occupied by selected ports contain at least one
   member of `R`.

Dummy leaves in one chosen full completion do not enter this criterion.

The independent compiler derives five cores from the primitive graph
enumerator—one cycle and four theta cores—and computes their minimum repairs
by rebuilding every segment-occupancy graph and applying the nonvacuous
admissible-rooting census. The minimum repair-size multiset is

```text
1, 1, 2, 2, 2.
```

For every bounded selected pattern, the criterion agrees with a fixed-core
graph test. That test deliberately does not apply arbitrary induced-network
reductions.

## Semantic limitation: not intrinsic selected `S_TC`

The manifest body hash

```text
62da7d21262aba940b2e4576aa8937bd2be59e40b12a21dc05073396082fd20d
```

incorrectly described this fixed-core result as intrinsic selected `S_TC`
membership. That claim is withdrawn and preserved in
`certificates/selected_core_retention_semantic_limitation.json`.

An exact counterexample is a directed cycle core with one and two selected
ordinary ports on its two entry-to-reticulation paths. Omit the reticulation's
sink leaf. The original cycle core is not retained, but pruning vertices with
no selected descendant deletes the reticulation; suppressing the resulting
unary vertices gives the strong rooted tree

```text
(L0,(L1,L2));
```

Therefore the predicate makes no claim about generic intrinsic `S_TC`
membership after arbitrary `red_*` operations.

## Minimal counterexample to the dummy heuristic

The first exact dummy-heuristic counterexample is a theta core with one
path-sink. The sink is selected, and selected ordinary ports occupy segments
`2` and `4`. The core's minimum repairs are `{2,3}` and `{2,4}`. A completion
chosen using `{2,3}` adds a dummy on segment `3`, but the selected ports already
contain repair `{2,4}`. Hence the original strong core is retained although
that completion contains one dummy.

## Count impact

These are target completion-presentation rows, not all repair-choice rows and
not complete decorated source-target relations.

| selected outgoing ports | total rows | dummy-rule positive | retains strong core | corrected false negatives | does not retain core |
|---:|---:|---:|---:|---:|---:|
| 3 | 831 | 9 | 15 | 6 | 816 |
| 4 | 1,983 | 40 | 78 | 38 | 1,905 |
| 5 | 4,155 | 131 | 257 | 126 | 3,898 |
| 6 | 7,909 | 342 | 652 | 310 | 7,257 |

There are no dummy-rule false positives for core retention.

The existing fully selected primitive ordinary-`T` relation counts remain
exactly `18, 192, 1,800, 17,280` for four through seven total ports. Those
records omit no selected port, so the corrections change their counts by zero.
