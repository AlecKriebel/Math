# Read the complete review

Start with REPORT.md and VERDICT.json. The mathematical, source/priority, and
package/PDF derivations are in three separate readable reports. STRATEGY.md
preserves the independent target-only initial plan and RESEARCH_LOG.md records
checkpoints and completion estimates.

Authenticate MANIFEST.json and verify_review.py against the final SHA-256
digests supplied outside this packet before running code. Then use an ordinary
absolute nonsymlinked path:

```sh
python3 -I -B /absolute/round03/verify_review.py \
  --packet-root /absolute/round03 \
  --expected-manifest-sha256 EXTERNAL_MANIFEST_PIN \
  --expected-checker-sha256 EXTERNAL_CHECKER_PIN \
  --source-root /absolute/preprint/source \
  --release-root /absolute/preprint --replay
```

Optional `--primary-root /absolute/whole_preprint_round03_scratch/primary`
rehashes the 23 recorded fresh primary-bank files. It does not claim full
reading. Omit it when those excluded bodies are unavailable. The read-only
checker never fetches sources, rewrites files, typesets, builds distributions,
or launches candidate programs. Its optional replay runs only the sealed
reviewer-owned exact math diagnostic. It cannot certify a formal proof or
exhaustive priority search.

run_checks.py, retrieve_primary.py, and package_controls.py are preserved
review-procedure sources, not checker prerequisites. They write receipts or
owned scratch when intentionally run and should not be confused with the
read-only checker. All mutations during the review used copied packets/PDFs
and stayed outside the frozen source. The review packet itself contains no
full third-party body, render, private configuration, or unrelated problem.

To rerun the own-checker 4-positive/20-negative suite, use control_checker.py
with the same --packet-root, external manifest/checker pins, --source-root,
and --release-root, plus --primary-root, a new owned --scratch directory, and
an --output JSON path outside the packet. This harness writes disposable
copies; it never modifies the sealed packet or source. Its preserved receipt
is from the preterminal seal; the terminal seal is rechecked separately into
excluded scratch to avoid a circular receipt/manifest hash.
