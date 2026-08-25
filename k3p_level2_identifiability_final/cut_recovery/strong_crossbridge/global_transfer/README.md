# K3P lost-bridge global transfer

This package closes the directed cut-transfer gap.  Its main proof is
`GLOBAL_TRANSFER_AUDIT.md`; its theorem object is
`GLOBAL_TRANSFER_CERTIFICATE.json`.

The decisive observation is that the two-active target alternative contains
a target bridge crossing the allegedly lost source bridge.  The already
proved inclusion `Cut(target) subset Cut(source)` would make both crossing
splits source bridge splits, contradicting tree compatibility.  The remaining
target witness is therefore one-active and belongs to the complete
204-direction pointwise K3P universe.

The proof uses no common bridge tree, fourteen-orbit classification, target
regularity, or target-open marginal.

The `adversarial/` subpackage is an independently written exact audit. It
replays the 204-direction handoff, tests 19,270 noncut tree colorings, derives
the strict two-boundary side-blob mixture closure, and rejects 32/32 targeted
mutations. `verify_release.py` checks both sealed layers without importing
either verifier, and `THEOREM_MANIFEST.json` binds their reports and manifests.

Replay commands are listed at the end of `GLOBAL_TRANSFER_AUDIT.md`.
