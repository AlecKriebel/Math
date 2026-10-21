# Candidate adversary audit

Read `REPORT.md` together with `INDEPENDENCE_ADDENDUM.md`; the addendum precisely qualifies the timing of independence during final coordination. The mathematical verdict is PASS in the printed source scope. The historical editorial replay and novelty limits remain explicit.

`AUTHORED_MANIFEST.json` lists only authored review members using relative paths, byte counts and SHA-256. It excludes itself to avoid a hash cycle; its own hash is delivered outside the package. The whole `own_local/` directory is excluded. That directory contains raw downloaded source inputs, extracted text, renders and raw receipts; none is an authored member. Source-input identities and outside paths appear only in separate read-only receipts.

`verify_candidate.py` and the exact four recorded runs are auxiliary diagnostics for the universal proof in the report. Deliberate corruption runs are expected to fail. Extra root-run checks are detached and are not represented as executions by this auditor. This package makes no publication or merge-approval claim.
