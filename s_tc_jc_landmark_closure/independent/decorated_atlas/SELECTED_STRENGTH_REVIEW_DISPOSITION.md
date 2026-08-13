# Selected-core review disposition

Status: **ACCEPTED AFTER CORRECTION WITH SCOPE LIMITATION**.

## Point-in-time stale-certificate finding

The nested reviewer returned `ACCEPT_WITH_LIMITATION` because the active
`certificates/` directory still contained the old manifest and did not bind
the selected audit or preserved dummy-repair failure. That high-severity
release finding is resolved in the active v2 release:

```text
manifest body hash:
fea4e1876d422234c7c25a7cc39a8e50a3e2a29eadac5b1d9fc4a4dc0f3c8f2a

manifest file SHA-256:
54e65cf0e031aec3ed73561bc82b03e468d6252081ac1005a42e4ba9ddfc06b2
```

The manifest now binds:

| artifact | SHA-256 |
|---|---|
| `selected_core_retention_audit.json` | `bb41ab36318857fd464f4e09c7ab95719eeb3c67c57502bb7f91c37dfbd0e33e` |
| `selected_core_retention_dummy_failure.json` | `e91171d8ee89befed68d85e0ec55b5e5748418ae56f2253e19454a50ca2219e7` |
| `selected_core_retention_semantic_limitation.json` | `0039526d7223ccf7fc0f995f3a9ba1e019a6439efe2f2be272db4bd3850b1609` |

The exact contract replay passed, and a clean regeneration reproduced all 24
active certificate files byte-for-byte.

## Later semantic correction

A separate clean-room review identified a more important limitation after the
nested review: all sinks selected plus minimum repair characterizes retention
of the original primitive core as a strong factor, not intrinsic selected
`S_TC` after arbitrary `red_*`. The code, JSON fields, manifest claim boundary,
and documents now use `selected_retains_strong_core`.

The withdrawn broader claim is preserved by the prior manifest body hash
`62da7d21262aba940b2e4576aa8937bd2be59e40b12a21dc05073396082fd20d`
and an exact sink-omission witness. In that witness, omitting the cycle sink
deletes the reticulation and reduces to the strong tree
`(L0,(L1,L2));`.

## Remaining low limitation

The selected-count table enumerates target completion-presentation rows under
the stated cycle-collapse convention. It is not a table of all repair-choice
rows and not a complete decorated source-target stochastic relation atlas.
This limitation remains explicit and does not affect the primitive or
ordinary-`T` relation counts.

## Mutation disposition

Both p4 and p7 fixtures rejected all 17 mutations. The added semantic mutation
attempts to change `intrinsic_selected_STC_membership_classified` from `false`
to `true`; regeneration rejects it.

