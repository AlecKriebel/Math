# Zenodo deposit tool log

2026-09-26 13:20 PDT — Started a dedicated folder. Defined the goal: reusable local paper deposits with private credentials, draft resume, file integrity checks, and an explicit publication gate. Checked Zenodo's current developer guide. Completion estimate: 15%.

2026-09-26 13:22 PDT — Implemented a standard-library client, manifest validation, sandbox separation, ignored local state and credentials, and separate `check`, `stage`, `inspect`, and `publish` commands. No real deposit attempted. Completion estimate: 75%; tests and review remain.

2026-09-26 13:23 PDT — Five offline tests pass, covering draft resume, publication ID gate, changed and extra files, duplicate names, private token file permissions, and API host restriction. Created the ignored 0600 credential file. Completion estimate: 95%; final source review and repository publication remain.

2026-09-26 13:24 PDT — Repeated the offline suite and checked that Git ignores the private key file. The reusable tool is complete; a live API test awaits a token. Completion estimate for tool construction: 100%.

2026-09-26T20:46:05.778314+00:00 — First live workflow found that requests without User-Agent received Zenodo HTML 403 traffic-filter responses. An otherwise identical authenticated GET with the truthful Math-Zenodo-Deposit-Tool/1.0 identity returned 200. Added that header and a regression assertion; all five offline tests pass. Brandes draft 22982894 staged and passed exact metadata/file inspection. Completion estimate for first production workflow: 70%; publish and tracker remain.
