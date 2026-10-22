# Round04 complete whole-preprint review

Read REPORT.md, then the three detailed review reports. STRATEGY.md and INDEPENDENT_DERIVATIONS.md preserve the independent pre-candidate position. VERDICT.json records zero actionable findings and unresolved historical priority. All authored files are closed by MANIFEST.json; full primary bodies/renders/control copies are in the excluded sibling scratch directory.

Before execution, independently authenticate verify_review.py and MANIFEST.json against the SHA256 pins supplied by the reviewer/parent outside this packet. A self-supplied manifest is not a trust root. The standard-library checker is read-only and its optional --replay runs only this reviewer's exact diagnostics, never the expensive full candidate tree. Full four-mode core terminal receipts are already retained.

```sh
python3 -I -B /absolute/review/verify_review.py \
  --packet /absolute/review \
  --source /absolute/preprint/source --package /absolute/preprint \
  --expected-manifest-sha256 EXTERNAL_MANIFEST_PIN \
  --expected-checker-sha256 EXTERNAL_CHECKER_PIN --replay
```

For the independently authored disposable custody controls, choose a new ordinary absolute scratch directory and an output path outside every sealed input:

```sh
python3 -I -B /absolute/review/run_controls.py \
  --packet /absolute/review \
  --source /absolute/preprint/source --package /absolute/preprint \
  --expected-manifest-sha256 EXTERNAL_MANIFEST_PIN \
  --expected-checker-sha256 EXTERNAL_CHECKER_PIN \
  --scratch /absolute/new-controls --output /absolute/control-results.json
```

The two positive controls replay own mathematics in normal/optimized modes. Twenty-four rejection controls exercise pins, bytes, closure, regular files, single links, lexical ancestry, duplicate/nonfinite/unsafe JSON, rehashed verdict/severity/firstness/head promotion, source changes and bound PDF mutation. They do not repeat the full candidate inner process tree. Finite algebra computations and custody cannot certify universal mathematics or historical first priority; the written reports state exactly what was proved and read.
