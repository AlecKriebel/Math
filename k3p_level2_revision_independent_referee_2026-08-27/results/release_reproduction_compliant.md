# Compliant release-engineering reproduction

**Date:** 2026-08-27
**Source commit:** `76a097fbc4ddadf23ba0119a371c5ac29f4802b1`
**Dynamic evidence root:**
`package_copy/review_runs/20260827T142318Z/release/`

## Isolation and source identity

The successful run used `logs/offline_release_git_read.sb`, a default-deny
macOS sandbox with no network, denied credential/keychain reads, and writes
confined to `package_copy`. It allowed read-only access only to the monorepo
Git object store and the two explicitly named delivered sibling archives. The
runner created a sparse detached checkout at exactly the source commit above,
required a clean scoped status before execution, and required it again after
all builds.

Two preliminary attempts are preserved and excluded from the successful
result. The first could not normalize the read-only alternate object-store
path; no Python release code ran. The second reached the mutation driver but
showed that the sandbox could kill a direct timeout child but not its
descendant process group. The policy was repaired to allow signals to targets
inside the same sandbox; a live parent/descendant kill test passed while the
network, credentials, and sibling source tree remained denied. The final
profile SHA-256 is
`9f5461644839fa437a539bee3e710f5fae316651382781341b74c5b938c67b49`.

## Results

1. The release-engineering mutation driver passed with all 32 mutations
   rejected, zero survivors, and ten controls passing. The generated report
   is byte-identical to the sealed report, SHA-256
   `de21482645a437066a405839eb9df2953327eeb1a08a62daadfdab05ab60363f`.
   Runtime: 11.14 seconds.
2. Two compact archives were built independently. Each structurally verified,
   each extracted artifact-only gate passed with transcript hash
   `749d2b85d617eaa2138899636e13c0b7bcbfde0a1ccd200a8ecab174005957fc`,
   and both are byte-identical to each other and to the delivered sibling:
   `95e909f433b2a7cb1975f34324dc84cbe94e1ac0e76d43352cfccd69db18b955`.
   Runtimes: 27.35 and 26.69 seconds.
3. Two full archives were built independently. Each structurally verified,
   each extracted artifact-only gate passed with the same transcript hash,
   and both are byte-identical to each other and to the delivered sibling:
   `ab0c2b068a6a0e7c80767000c29b1375591ac14a77b8fcb359818a73e167b9d8`.
   Runtimes: 33.42 and 32.92 seconds.
4. The exact checkout remained clean after all outputs, which were written to
   ignored release-work paths.

The complete console transcript is 24,714 bytes, SHA-256
`433cfd13dffc062dc0a617b30cacd1ce2eef655b0fa8c79c8d84de6451917884`.
`SHA256SUMS_AUDIT` binds that transcript, every per-step log and timing, the
mutation report, all four rebuilt archives, both delivered archives, the
sandbox profile, and the reviewer runner.

## Qualification and surviving packaging findings

This reproduction verifies the current executable release claims; it cannot
retroactively authenticate the historical 7,686-second/54-command run or PDF
double-build narrative whose cited final ledger is absent from the sealed
handoff (`proof_package/README.md:64-78`). The archive builder invokes
`verify_k3p_same_classification.py --artifact-only --no-write-report`
(`proof_package/release/build_release.py:594-609,627-637,687-705`), so the
extracted gate is an artifact-integrity/promotion check and deliberately
performs no fresh mathematical producer replays. It should not be described
without that qualifier as a fresh theorem recomputation.
