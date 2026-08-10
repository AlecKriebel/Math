# Second adversarial review prompt

Act as an independent adversarial mathematical/software reviewer. Work
read-only. Do not edit any file. Audit only
`reviews/zero_sum_descriptor_cleanroom/` and the primary/quarantine input files
it explicitly reads. Do not import project modules.

Try to falsify both conclusions:

1. quartet zero-sum complement normalization plus exact-rooted-graph caching is
   mathematically exact and release-safe;
2. the bounded atlas's unnormalized rooted selected-side convention remains
   exact for graph-specific zero/nonzero/strict-sign classification through the
   positive product submersion, though it is not a canonical semi-directed
   descriptor.

In particular inspect for: confusing equality of group sums with JC's
zero/nonzero indicator; incomplete standard mixed reduction; a false claim
when a root arc enters a reticulation; invalid product-map surjectivity or sign
logic; reticulation inheritance-coordinate mistakes; accidental merging of
noncomplement splits; trusting stored graph IDs/hashes; AST checks that accept
dead code; mutation tests that pass vacuously; boundary use; and
nondeterministic or self-inconsistent manifests. Run the stdlib verifier and
construct small independent checks when useful.

Return a concise report with: blocking findings first (file and line), then
nonblocking limitations, then one of `ACCEPT`, `ACCEPT_WITH_CORRECTIONS`, or
`REJECT`. Distinguish this gate from the full landmark theorem.
