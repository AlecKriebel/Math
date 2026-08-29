# K3P lost-bridge global transfer

This package closes the directed cut-transfer gap.  Its main proof is
`GLOBAL_TRANSFER_AUDIT.md`; its theorem object is
`GLOBAL_TRANSFER_CERTIFICATE.json`.

The first directed inclusion is now an active, self-contained K3P dependency:
`K3P_DIRECTED_CUT_INCLUSION_EVIDENCE.json` binds the displayed-tree boundary
lemma, the exact wrong-quartet `5 by 5` minor, the 808,642-word balanced
reduction, and the 379,742-presentation reduced-palette replay with zero
survivors. It uses neither the legacy global-logic report nor a JC cut theorem;
the direct verifier rejects 39/39 targeted mutations.

The decisive observation for the reverse inclusion is that the two-active
target alternative contains
a target bridge crossing the allegedly lost source bridge.  The already
proved inclusion `Cut(target) subset Cut(source)` would make both crossing
splits source bridge splits, contradicting tree compatibility.  The remaining
target witness is therefore one-active and belongs to the complete
204-direction pointwise K3P universe.

The proof uses no common bridge tree, fourteen-orbit classification, target
regularity, or target-open marginal.

The `adversarial/` subpackage is an independently written exact audit. It
replays the active K3P directed inclusion and the 204-direction handoff, tests
19,270 noncut tree colorings, derives the strict two-boundary side-blob mixture
closure, and rejects 35/35 targeted mutations. `verify_release.py` checks both
sealed layers without importing
either verifier, and `THEOREM_MANIFEST.json` binds their reports and manifests.

Replay commands are listed at the end of `GLOBAL_TRANSFER_AUDIT.md`.
