# Zenodo deposit tool log

2026-09-26 13:20 PDT — Started a dedicated folder. Defined the goal: reusable local paper deposits with private credentials, draft resume, file integrity checks, and an explicit publication gate. Checked Zenodo's current developer guide. Completion estimate: 15%.

2026-09-26 13:22 PDT — Implemented a standard-library client, manifest validation, sandbox separation, ignored local state and credentials, and separate `check`, `stage`, `inspect`, and `publish` commands. No real deposit attempted. Completion estimate: 75%; tests and review remain.

2026-09-26 13:23 PDT — Five offline tests pass, covering draft resume, publication ID gate, changed and extra files, duplicate names, private token file permissions, and API host restriction. Created the ignored 0600 credential file. Completion estimate: 95%; final source review and repository publication remain.

2026-09-26 13:24 PDT — Repeated the offline suite and checked that Git ignores the private key file. The reusable tool is complete; a live API test awaits a token. Completion estimate for tool construction: 100%.

2026-09-26T20:46:05.778314+00:00 — First live workflow found that requests without User-Agent received Zenodo HTML 403 traffic-filter responses. An otherwise identical authenticated GET with the truthful Math-Zenodo-Deposit-Tool/1.0 identity returned 200. Added that header and a regression assertion; all five offline tests pass. Brandes draft 22982894 staged and passed exact metadata/file inspection. Completion estimate for first production workflow: 70%; publish and tracker remain.

2026-09-26T20:50:33.155009+00:00 — First production upload/tracker workflow completed: Brandes record 22982894 (assigned DOI 10.5281/zenodo.22982894) was published, post-inspected against exact original metadata, and both public downloads matched local bytes. Google Workspace CLI appended and read back the requested tracker row. Completion estimate for requested actions: 100%. The DOI resolver initially returns 404 while the public Zenodo record returns 200; activation is tracked separately. Feedback and receipts: `../owr_17293_016_brandes_normalization/publication/README.md`.

2026-09-26T20:57:00.404168+00:00 — Requested follow-up hardening started. Completion estimate: 35%. The identifying header is retained. Implementing safe distinctions between traffic-filter HTML and API errors, strict response validation, read-back confirmation and saved publication receipts, safe recovery after an interrupted publish, and separately reported DOI resolution. An independent adversarial code reviewer is checking failure cases. Testing will use simulated mutations and a read-only inspection of the existing published record.

2026-09-26T21:02:34.821500+00:00 — Hardening checkpoint: 90% complete. All 22 offline regressions pass, including malformed successful responses, traffic/auth error distinctions, interrupted publish recovery, verified idempotent repeat, receipt-write failure, invalid DOI data and resolver failures. The independent reviewer found two DOI error-handling edge cases; both were fixed and regression-covered. Live read-only inspect confirmed exact original metadata/files and successful DOI resolution. Final independent recheck and commit/push remain.

2026-09-26T21:03:08.698766+00:00 — 100% implementation and validation complete. The independent reviewer rechecked both fixes with separate mocks and found no remaining actionable defects in the diff. All 22 regression tests pass with ResourceWarnings treated as errors; live read-only inspection confirmed metadata/file integrity and DOI resolution. Original source-manifest hashes remain valid. Preparing the scoped commit and push; unrelated working-tree files are excluded.
