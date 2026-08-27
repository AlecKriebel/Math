# Research log

## 2026-08-27 06:48 PDT — Audit initialized

- Created a dedicated v1.2.5 referee workspace.
- Recorded submitted archive SHA-256:
  `e8302556f356ac04add887a59ab370d4a496f011d59ccfd8a3e87cc19876551e`.
- Inspected all 45 ZIP entries before extraction: no absolute paths, parent
  traversal components, or symbolic-link entries were found.
- Observed unrelated pre-existing changes elsewhere in the repository; they
  will remain untouched and unstaged.
- Review policy: read the manuscript before consulting packet prompts or the
  prior report; treat the editor's repair summary as hypotheses to falsify.

**Best-guess completion:** 5%.

## 2026-08-27 06:50 PDT — Archive provenance verified

- Copied the submitted ZIP into the audit workspace and extracted its sole
  top-level packet directory.
- All 41 files listed by the packet manifest passed SHA-256 verification.
- The audit-local ZIP copy has the same SHA-256 as the submitted attachment.

**Best-guess completion:** 8%.
