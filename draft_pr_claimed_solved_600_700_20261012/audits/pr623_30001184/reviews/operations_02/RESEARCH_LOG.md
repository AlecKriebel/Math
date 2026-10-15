# PR623 operational round2 repairs

## 2026-10-14T03:35:49.663957+00:00 — F1/F2 repair checkpoint

Captured each compact publication receipt exactly once and used those bytes for parsing, validation and SHA attestation. publication_inputs now returns the same archive-validated source-notice bytes that main installs, without a second path read; tracker and all active fixtures consume the three-value snapshot contract. The package schema gate now requires an exact integer value of 1.

18 controls pass under normal and optimized Python, including changed publication receipt, changed inspection receipt, post-validation source-notice mutation in a full mocked preparation with actual wrapper replay, tracker contract handoff, true/false/1.0/0/-1/2 schema rejection and the earlier 14 head/race/queue/frozen/tracker guards. Old package_round2 evidence is read only; all native29 SHA values match the pre-repair checkpoint.

Best-guess implementation completion: 100%; live execution completion: 0%. No remote mutation or shared checkout/index change was performed. Exact remaining gap: parent rebuild and rebound PDF/ZIP identities, then NEW independent sequential whole-package round3; no predecessor publication hashes are final readiness evidence.
