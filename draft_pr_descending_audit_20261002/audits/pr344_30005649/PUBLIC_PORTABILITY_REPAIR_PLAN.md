# Planned public-output portability repair

The first fresh preprint reviewer identified a genuine release blocker in
the original public ZIP (SHA256
`e290f930354c82dc12c229455f25a31fb6ed3819be75c938ffdf31d4e96186b0`).
Root reproduced it independently in
`root_preprint_private/portability_original_001`: the default package
check succeeds under both available interpreters, but full mode succeeds
under the system interpreter and rejects the bundled interpreter's
intrinsic stdout. Both intrinsic controls themselves succeed, and their
complete mathematical JSON outputs are identical after deleting only
the `interpreter` field. These are actual native execution outcomes,
with separate complete stdout, stderr, interpreter and exit receipts.

The proposed repair will be applied after the reviewer completes its
review of the frozen original packet. Preserve the sealed intrinsic
family and every other sealed family without modification. Derive the
public intrinsic source by removing exactly the unique
`interpreter` member from its printed result dictionary. Preserve all
mathematical statements, calculations, assertions, mutant controls and
input specification bytes. Record the original source pin, the exact
transformation and the derived public source pin in SOURCE_IDENTITY.json.
Keep interpreter provenance in the actual package-build execution
receipts, outside deterministic public expected stdout. Retain strict
complete-stream comparison in the public wrapper.

Rebuild the ZIP with fresh deterministic expected streams; independently
extract and replay both integrity and full modes with both available
interpreters. Compare every complete mathematical stdout and require
empty stderr, exit0, unchanged package bodies/modes/inventory and an
unchanged manuscript/PDF/deposit metadata. Review the changed builder
and source derivation explicitly. Then dispatch a new independent
full-package adversary against the revised packet. No clearance,
merge, upload or tracker write follows merely from fixing this defect.

Checkpoint estimate: mathematics100%, bounded priority100%, publication
workflow50%; first fresh package review active and portability repair
not yet applied. Native reproduction completed
2026-10-04T06:30:44.005334+00:00.
