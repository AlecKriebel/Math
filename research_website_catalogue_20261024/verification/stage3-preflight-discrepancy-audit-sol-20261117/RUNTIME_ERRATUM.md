# Runtime erratum to prior static audit

2026-11-17T06:00:27.189401+00:00 — The prior audit FINAL dea0cef6122c2991de4fe7fc8f92b734a892452b10df32168434b41a425da5c8 remains immutable. Its STATIC_PASS/no-corrections conclusion is superseded for exact v1 helper70814930 after one later root-authorized preflight exposed a deterministic implementation defect at whole_snapshot238: inventory list order was treated as namespace identity.

The earlier reviewer read the actual code and data schemas but did not compare the ordering conventions. Frozen builder Path-component ordering differs from fresh helper string ordering at12 of772 file-list positions. This was a missed static defect, not merely unknown runtime behavior. Candidate bytes, modes, paths, root, directories and counts are exact.

The corrected current disposition is CORRECTIONS_REQUIRED_FOR_V1: normalize expected file/directory row ordering locally after existing strict validation, then obtain a fresh exact saved-code audit before any new execution. No frozen helper/stage/audit is repaired here; no runtime/copy/science success is inferred. This erratum records the error and remaining gap without rewriting historical evidence.
