# Review artifact index scope

`REPORT_ARTIFACT_INDEX.sha256` binds the review-owned, delivery-sized files in
this review directory. It intentionally excludes itself; its own SHA-256 is
reported in the final handoff and can therefore bind the complete list.

The index deliberately excludes:

- the 214,823,405-byte submitted ZIP and its byte-identical isolated copy,
  which are separately bound in the report by ZIP SHA-256
  `ca08a3f50154610c7297ca83f92f0c9517fa5422ac7acf53b89582e1e14edbde`,
  outer/inner ledgers, and frozen/source Merkle roots;
- `isolated/`, `tmp/`, and `rendered_pdfs/`, which are disposable package,
  execution, and visual-QA material rather than review deliverables;
- generated PDF page images under `independent_checks/math/pdf_render/`, whose
  visual-QA command and source-PDF hashes are recorded in
  `EXECUTION_LEDGER.md`; the smaller mathematical scripts and text outputs are
  included in the index;
- reusable scripts from the immediately preceding independent review that
  were invoked in place and were not copied into this delivery.

The reused script authorities and hashes are:

- `k2p_same_neutral_referee_rereview_2026-08-25/independent_checks/math/primitive_core_enumeration.py`:
  `183d340ee52364abc15e0e48167de2e28f553dde8b54d2960b6465f8b80c712f`;
- `k2p_same_neutral_referee_rereview_2026-08-25/independent_checks/provenance/audit_git_binding.py`:
  `1ab61bbed9838b7177a422c6e4428262a9e47506b039bbe3edce341f8d539df8`;
- `k2p_same_neutral_referee_rereview_2026-08-25/independent_checks/provenance/audit_artifact_consistency.py`:
  `591a7fa52e05274e05de8be6b1a3eb1f6c07c897bf0b4db8458090f5ed65328c`;
- `k2p_same_neutral_referee_rereview_2026-08-25/independent_checks/provenance/make_manifest_mutations.py`:
  `ab2589625af538c5b578a5027e3d65b3d90b29135de47dfc4b3eb0687e723e81`.

This scope distinction prevents a review-delivery checksum list from being
misread as a new seal for the authoritative submission package.
