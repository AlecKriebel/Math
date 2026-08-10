# Preserved pre-correction core-retention failure

The manifest `16e15131c2a77cc51f75626286e01c0f815a0b8b4811299dba876a172ed6f333`
passed the primitive contract but had no selected-completion classifier.

If a downstream classifier inferred nonretention from the mere presence of a
dummy repair leaf, it misclassified theta restrictions that retain the
original strong core.
The minimal preserved case has:

```text
selected sink mask:        1
selected segment counts:   0,0,1,0,1
chosen completion repair:  2,3
dummy repair segment:      3
contained selected repair: 2,4
```

This is a core-retention statement only. It does not classify intrinsic
selected `S_TC` status after arbitrary reduction. The machine-readable copy
and all count deltas are in
`certificates/selected_core_retention_dummy_failure.json`.
