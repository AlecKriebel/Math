# PR12 artifact-integrity and document-consistency audit log

All work in this audit is read-only outside this directory. No candidate,
canonical, Git, or remote mutation was performed. This is an artifact and
claims audit, not an independent proof or literature-priority determination.

- 2026-10-01T13:46:13Z — First recorded checkpoint. Defined acceptance anchors:
  requested current proof `782a92710ba0e1932bdf02e89f741df2fdf74651d09af260d1e0b1a391da8fa4`,
  frozen PR head `19dfaccb52a7640eec79af28a778b4f22f93479a`, and exactly 21
  original files. Enumerated every manifest/provenance hash schema and assigned
  an independent document-claims/history check. Completion estimate: 35%.
- 2026-10-01T13:49:30.856130+00:00 — Byte audit verified all 268 declared
  manifest/provenance/root-packaging hash checks and all 21 originals against
  the Git blobs at the frozen PR head. The sole failed check was the initial
  requested proof pin, because the concurrently corrected current proof had
  become `2d2e394d83ab96a6aee9b022d375fb1520499ed4aa360de51f7d1ed04f5b75ea`.
  Preserved this run as `superseded_requested_pin_results.json` and its delta;
  did not misclassify the authorized pin transition as file corruption.
  Completion estimate: 60%.
- 2026-10-01T13:52:20.395757+00:00 — Parent confirmed the corrected proof pin.
  Rechecked 273 file/canonical hash claims, all 21 original Git blobs, exact
  original/current inventories, all literal SHA256 coverage, and 11 current
  document link destinations. All pass. Pinned the correction addendum and
  confirmed the historical source/review files remain preserved. Independent
  document audit is rechecking the corrected bytes. Completion estimate: 90%.
- 2026-10-01T13:53:31.640860+00:00 — Independent document-claims agent completed
  its second pass on the corrected final proof. It found no mandatory issue,
  unintended novelty claim, or claim that the older spectral theorem is
  disproved. All 12 history-preservation checks pass and all three precision
  correction links target the pinned local addendum. Completion estimate: 98%.
- 2026-10-01T13:55:14Z — Final scoped report, verdict, and output manifest
  prepared. Strongest verified result: complete declared-hash integrity, exact
  original21-file Git preservation, and consistent credited-method/history
  framing at the final candidate pin. No mandatory issue in this scope. Exact
  remaining gap: mathematical/source acceptance belongs to other fresh audit
  families; remote publication of links was not tested. Completion estimate:
  100% of this artifact-integrity/document-consistency audit.
