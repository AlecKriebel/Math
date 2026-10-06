# Reproduction of this original-package audit

Use Python3 with SymPy1.14.0; in the current host /usr/bin/python3 provides it. All external input directories are read-only. Supply a writable private output and scratch location rather than changing this frozen family after its final manifest. Third-party PDF/text inputs are version/hash-bound in SOURCE_BINDINGS.json and privately present under sources/; they are not redistributed. Their official URLs and retrieval receipts are provided separately. A different PDF rendering or text extraction should be recorded as a new input, not silently substituted for the bound bytes.

From /Users/alec/Documents/Math, reproduce the exact main diagnostics with:

```sh
/usr/bin/python3 draft_pr_publication_program_20260930/audits/pr35_2744/algebraic_family/algebraic_controls.py \
  --repo /Users/alec/Documents/Math \
  --snapshot draft_pr_publication_program_20260930/audits/pr35_2744/source_snapshot \
  --metadata draft_pr_publication_program_20260930/audits/pr35_2744/snapshot_manifest.json \
  --sources draft_pr_publication_program_20260930/audits/pr35_2744/algebraic_family/sources \
  --source-bindings draft_pr_publication_program_20260930/audits/pr35_2744/algebraic_family/SOURCE_BINDINGS.json \
  --output /absolute/private/path/algebraic-results.json \
  --scratch /absolute/private/path/algebraic-scratch
```

Expected summary:108 passing diagnostics,3 original unchanged actual program replays,9 actual mathematical mutants rejected. The output JSON is deterministic, with private traceback locations normalized. It contains exact source/metadata hashes, replay output hashes and full failed mutant tracebacks; it is not a proof of an arc. Reproduce the16 additional toy boundary controls with:

```sh
/usr/bin/python3 draft_pr_publication_program_20260930/audits/pr35_2744/algebraic_family/component_boundary_controls.py \
  --output /absolute/private/path/component-boundary-results.json
```

The two exact output files should byte-match RESULTS.json and COMPONENT_BOUNDARY_RESULTS.json, respectively. The initial setup-failure revision intentionally does not pass and must not replace the final actual program.
