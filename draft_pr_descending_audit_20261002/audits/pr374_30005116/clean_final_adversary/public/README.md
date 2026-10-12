# Fresh independent whole-package audit of PR374

The written five-turn mathematics passes within its exact scope. The unrestricted
induced-C4 profile remains **unsolved5/5**. No novelty, external human peer review,
or formal proof-assistant certification is claimed. No mandatory candidate
mathematical correction was found. The new whole-package audit is independent
of the old review: sources and original baseline were sealed first, and the
mathematical verdict and new programs were sealed before author code and old review.

The initial prepared acceptance gate passes. This does **not** say the prepared
body is live or the PR is ready or merged. Root reproduction and the final exact
live-body/current-main gate remain required. See FINAL_REPORT.md and the two seals.

## Public allowlist and private inputs

PUBLIC_MANIFEST.json is the explicit allowlist, binding every public original
program, proof reconstruction, full generated stdout/stderr, receipt, research log,
and failure artifact. Publish only those listed files and the manifest itself,
plus the own-directory .gitignore. All fetched source PDFs, extracts, rendered
pages, response headers, copied author packets, raw API responses and Git blob
streams are under ignored private/. Generated Python cache files are excluded.
No public file contains a source PDF/text/render or an input packet copy.

Private immutable input bundle for exact reproduction:

* Original input root: snapshot_manifest.json and snapshot/ (46 frozen paths).
* Refreshed input root: repaired_snapshot_manifest.json, repaired_snapshot/
  (same45 target bytes and refreshed queue), queue_repair_receipt.json.
* Prepared accepted_pr_body.txt SHA256
  662fbbeac83e2709a4374f540da4eebf137f5ef4240f1cb820b23814d1cb6b0f.
* Prepared merge_body.txt SHA256
  d05c7698cd384c8fc7f1431b420e9d871e2e6552277fd2a3066c5f497f7c0771.
* Fresh private/sources/{owr,lmr,pr,semi2026,cograph}.pdf, with exact hashes in
  source_first_seal.json and final_gate_prepared_receipt.json. Only these PDFs
  are active source-byte inputs to the gate. The15 historical source records
  include derivative text/render/HTML provenance; they are not claimed as15
  freshly regenerated raw derivatives.

The input root may be staged anywhere, and --own must be a separate private
output tree containing a cloned public directory. --git supplies the read-only
Git object database/check-out location; it is not mutated. The latest remote main
object must already be available there. No tool installs or symlink resolution
of the approved SymPy runtime are needed.

## Reproduction commands

From a cloned tree, the fresh mathematical controls are:

```sh
python3 public/controls/source_first_counts.py
python3 public/controls/fresh_adversarial.py
python3 public/controls/fresh_moments.py
/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr378_30004322/sources_effective_review/private_runtime/bin/python public/controls/fresh_symbolic.py
```

Their entire stdout and stderr must match the stored streams byte-for-byte.
The supplemental finite controls do not replace the universal proofs.

```sh
python3 public/controls/replay_package.py --snapshot INPUT_ROOT/snapshot --own OUTPUT_ROOT
python3 public/controls/final_gate.py --inputs INPUT_ROOT --own OUTPUT_ROOT --source-dir SOURCE_DIR --git GIT_LOCATION
```

The replay runner stages an exact45-file publication packet and a separate
explicit36-file author directory under OUTPUT_ROOT/private. All five author
receipts, historical author replay, historical independent JSON and portable
wrapper stdout/stderr are compared in full. The whole JSON objects also match.
No source retrieval occurs in the portable author wrapper. Only replay receipt
start/end UTC and measured elapsed seconds are volatile; its complete mathematical
outputs have no permitted differences. Failure1 replay code is preserved history,
not the corrected active command.

The initial gate's complete result JSON must match, including every queue byte
claim and the prepared/live body distinction, if live inputs have not changed.
The receipt's observed_utc may differ. Live API JSON raw streams remain private,
bound by receipt hashes. After a deliberate metadata mutation, the explicitly
declared live fields (body, draft, API base, remote main and corresponding merge
commit/tree) are freshly observed; old values are preserved as history. No other
count, file binding, program or mathematical result is normalized.

After root has sent the exact prepared body and marked the PR ready, run the
**same unchanged gate** with:

```sh
python3 public/controls/final_gate.py --inputs INPUT_ROOT --own OUTPUT_ROOT --source-dir SOURCE_DIR --git GIT_LOCATION --require-exact-api-body --require-ready
```

That mode requires the API body to equal the prepared bytes, draft=false, and the
GitHub API/test-merge base to equal the actual remote main. It checks the full
expected merge-tree SHA and a pure read-only legacy three-tree merge, preserving
every unrelated current-main path. A stale GitHub cache must settle before this
final mode passes. It performs no service write, Git fetch/mutation or merge.

fetch_sources.py records the fresh source acquisition and rendering; it is not a
mathematical assertion scan. Re-fetching permits new acquisition UTC and HTTP
runtime headers, while the five primary PDF bytes and hashes must remain exact.
The original source-first acquisition receipt remains private and immutable.

## Preserved failures and corrections

1. A first command used a directory that had not yet been created and failed
   before executing. The directory was then created only within the authorized
   own scope. This was not a source or candidate failure.
2. An additional render initially selected LMR page6 instead of Construction1.9
   on page5. Page5 was then rendered and inspected. Poppler marked-content
   warnings were retained; exit status was zero and critical formulas were legible.
3. replay_package.failure1.py passed the full45 packet to the historical
   glob-based replay, producing public_bindings104 instead of the stored60.
   The corrected runner isolates the exact36 author files. Every failed full
   stdout/stderr and code version is retained; no count was changed silently.
4. final_gate.failure1.py rejected GitHub's explicitly truncated recursive tree
   response. The corrected gate computes canonical Git Merkle-tree SHA values
   from complete local maps and compares the GitHub test-merge root SHA.
5. final_gate.failure2.py expected a result label for additions. Legacy merge-tree
   emits their for an absent path; the corrected parser permits that incoming
   blob only after verifying the path is absent from current main. Existing-path
   edits still require explicit result blobs. Failure streams and code are retained.

No outside individual was contacted. Root and sibling proof files were not read.
After the mathematical seal, read-only Git tree metadata for current main was
examined to preserve concurrent publication paths; this supplied no proof input.
