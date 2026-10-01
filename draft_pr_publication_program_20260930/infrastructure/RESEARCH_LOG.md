# Publication infrastructure research log

## 2026-10-01T03:37:37.001948+00:00 — Read-only audit checkpoint

Infrastructure audit completion estimate: **100%**. Overall publication-program and mathematical-review completion are outside this estimate.

Read the repository Zenodo README/client, the recent Brandes publication receipts, the installed GWS Sheets skill, and the relocated generated shared prerequisite. Inspected the installed get/values.get/values.append schemas. Verified GWS authenticated metadata and explicit target-tab reads without writes. Resolved sheet ID 1254632077 to **Math Puzzles**, with exact A:D headers Original Problem, Solution Chat URL, DOI, Notes. Observed nine body records, blank Solution Chat URL cells, no exact normalized duplicate problem/DOI keys, ordinary string values, and existing header/body formatting. Saved reproducible subprocess argv commands and sanitized local credential-availability booleans.

Production Zenodo token availability is true; sandbox availability is false. Authentication/scopes and Google write permission remain untested. No Zenodo API call, stage/publish action, Google Sheet write, researcher contact, or Git branch/commit/push action occurred. The 27-test offline Zenodo suite passed. The exact remaining operational gap is live authentication/scopes and eventual write verification for a fully validated candidate, handled by the authorized publisher's normal stage/inspect/publish/receipt/explicit-tab-append/readback sequence.

Documented failure recovery for ambiguous creation/publication/append outcomes, stable manifest path and ignored draft-state retention, DOI-registration independence, duplicate detection, exact-tab targeting, serialization, and bounded metadata-description normalizations. The installed `+append` shortcut lacks a range selector, so the direct values.append method is required.
