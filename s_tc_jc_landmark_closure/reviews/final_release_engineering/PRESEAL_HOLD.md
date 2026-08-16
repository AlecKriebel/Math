# Pre-seal adversarial release review

Status: **HOLD — RELEASE-BLOCKING DEFECT**

An independently dispatched release-engineering referee found that the first
deposit archive was built from source commit
`fa5dd3c4f31e15f499e7a2861a794d878c46bf05`, whose bundled active metadata
still contained the placeholder `TO_BE_SEALED`.  Although the outer checksum,
submission files, clean-clone transcripts, mathematical scope, and Outcome-A
claims all agreed, the verifier extracted from that archive correctly failed
with `release source commit is not sealed`.  The then-current outer release
envelope was also not committed.

This report is intentionally preserved as a failed release gate.  The repair
replaces the self-referential design with two layers:

1. a commit-independent core manifest that is included in and verifies inside
   the archive; and
2. an external envelope that binds the immutable source commit, appended
   clean-clone transcripts, final archive hash, and checksum sidecar.

No mathematical theorem failed this review.  A final adversarial release
review is required after the two-layer seal is complete.
