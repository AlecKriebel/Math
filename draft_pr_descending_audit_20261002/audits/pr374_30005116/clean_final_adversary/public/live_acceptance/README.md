# Additive acceptance evidence

The original PUBLIC_MANIFEST.json and its 68 bound files are immutable. Its
allowlist has exactly69 members including itself. This directory adds metadata
observations, every failed attempt, read-only diagnostic programs, a full gate
adaptation diff/build recipe, and the round2 prepared acceptance certificate.
No original mathematics, source, candidate, historical certificate or receipt was
rewritten. The unrestricted problem remains unsolved5/5.

The active metadata gate is final_gate_staged.py, generated deterministically from
the original gate by build_staged_gate.py. Its exact SHA256 is
1b64c7a4728c41ff2467241e5471338d4a1830e339befb0c5d6f11c36dbc2ab0.
ROUND2_STAGE_DESCRIPTOR.json SHA256 is
820cd232c67ca3510e104cba68f8f5afae1b086ac225651d02e4bdf95984dac9.
The descriptor is an explicitly frozen input; its expected hash is mandatory.
All original scope, source, queue, body, Git/API, current-main and full-tree checks
remain. Every prior stage is additionally checked independently.

Stage input roots must contain the following exact private bundles:

* initial: original snapshot/manifest, first repaired snapshot/manifest, first
  queue repair receipt, body662fbbe… and unchanged merge body.
* round1: live_acceptance_inputs, body0933d8a…, metadata binding4afe/8e047/9b4.
* round2: live_acceptance_inputs_round2, body9ad5abe…, metadata binding2bb/eb3/1464.

The descriptor lists all15 metadata hashes. Each root also supplies its complete
46 repaired files; the current root supplies the46 original frozen files. The
five fresh source PDFs are the same pinned private inputs as the original audit.
Raw source bytes, copied packets, API responses and Git streams remain private.
All complete top-level generated streams and public receipts are allowlisted.

From a private clone of the complete public tree, create OWN/public, then run:

```sh
python3 public/live_acceptance/final_gate_staged.py --inputs ROUND2_INPUT_ROOT --stage-input initial=INITIAL_INPUT_ROOT --stage-input round1=ROUND1_INPUT_ROOT --stage-input round2=ROUND2_INPUT_ROOT --stage-descriptor public/live_acceptance/ROUND2_STAGE_DESCRIPTOR.json --stage-descriptor-sha256 820cd232c67ca3510e104cba68f8f5afae1b086ac225651d02e4bdf95984dac9 --own OWN --source-dir SOURCE_DIR --git GIT_LOCATION
```

Compare every stdout/stderr byte and the entire generated receipt to
round2_prepared/. The receipt permits only observed_utc to differ while live
metadata stays unchanged. The original/current API blob union is47; independently
checking all historical stages adds one old queue blob, giving48. Both counts are
explicitly asserted and separately reported. No count is normalized silently.

After root reproduces this prepared gate and sends the exact prospective body,
run the identical command/code with --require-exact-api-body --require-ready into
a new OWN. Root then independently reruns that exact-live certificate before any
merge. Historical prepared/live body differences remain frozen observations.
The gate is read-only toward Git, remotes, source inputs and body artifacts.

Historical capture_live_gate.py, diagnose_live_refs.py, assess_refresh.py and
final_gate_refreshed.py preserve the actual earlier state and failures. They are
not the active round2 gate and do not claim that obsolete remote refs still pass.
All three original exact-live attempts rejected a stale API/test-merge base.
A first new gate attempt incorrectly assumed the old repaired manifest contained
git_blob_sha; its code and full streams are retained, and the corrected check uses
the independently read Git-tree blob SHA. A later attempt rejected transient
mergeable=null. Another rejected concurrent actual-main queue drift. A proposed
repair-map check rejected a live-head race; its corrected historical-only mode
does not certify a future object. These were metadata/harness observations, not
candidate mathematical failures. The initial certificate was never weakened.

Only the explicit manifests' union may be published. No raw input tree, recursive
own-folder staging, preprint, Zenodo upload, tracker entry or release is authorized
by this evidence. No outside individual was contacted.
