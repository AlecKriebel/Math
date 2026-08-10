# Status of the long nonroot Gate-2 replay

Status: **INTERRUPTED / UNRESOLVED**

The raw files `NONROOT_GATE2_REPLAY.md` and
`../independent/nonroot_gate2_replay.json` were emitted when the independent
Gate-2 calculation was stopped after approximately eighty minutes of
single-core exact Bernstein arithmetic.  The process exited with code 130 and
records `KeyboardInterrupt` as its failure.

The raw Markdown is a partially populated report template.  In particular,
its prose under “Local theorem” is not a completed conclusion: the finite
theta-atlas section is empty and the JSON contains no completed certificate
for that claim.  Nothing from this interrupted replay is used by the active
sharpness manuscript.  The independently completed atlas audit remains
`ATLAS_GATE_REVIEW.md`, whose verdict is that the positive classification is
unresolved because the end-to-end topology-to-polynomial binding and
arbitrary-subdivision theorem are absent.
