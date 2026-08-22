# Blind-review protocol

Three preliminary tracks remain independent until each report is timestamped:

1. Analytic proof: manuscript PDF first, then exact TeX and bibliography; no
   code reports, audits, validation summaries, or other tracks' notes.
2. Software: manuscript PDF first, then the full implementation and tests;
   inspect before running anything and before opening committed expected
   outputs or reports; no other tracks' notes.
3. Adversarial: manuscript PDF first, then exact TeX and bibliography; search
   independently for counterexamples, boundary failures, hidden assumptions,
   and primary-source citation mismatches; no audits, golden reports, or other
   tracks' notes.

The three reports will be merged only after all are present. Canonical replay,
artifact comparison, and author-record comparison occur afterward.

