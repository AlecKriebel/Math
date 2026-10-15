# PR411 merge administration continuation preparation (V5)

V4 integration and ready were genuinely confirmed. Its ordinary merge application ended at the clean/mergeable guard with only its exclusive local claim; no remote intent or acknowledgment was recorded. V5 permits exactly one separately approved merge successor while preserving that claim, journal, and terminal STOP.

The new pinned descriptor joins the prior canonical plan, original exclusive claim/run/head/phase, exactly one complete canonical journal event, terminal STOP, completed root CLI return code and exact guard message, and the caller-pinned root acceptance’s original byte hashes. The prior STOP’s GET observations may differ from its planned observations under the unchanged canonical approval policy. Any additional journal event, including an intent or acknowledgment, forbids continuation. Root-pinned authentic originals establish provenance; synthetic matching JSON does not establish service history.

The fresh plan binds the descriptor SHA256. Its original source/head/main/registration/confirmed-phase core stays exact; current helper and evidence refresh pass all existing scope, publication, Sheet, approved map, selected byte, deadline, and canonical approval checks. The same original journal root is mandatory. A new fsynced exclusive `continuations/merge-HEAD.json` guard names the one new run and plan before its journal is created. The prior claim remains in place. A concurrent or second successor, existing/torn/symlink guard, reused prior run, or different root stops. Creation failure consumes any allocated guard; it is never removed. Immediately before a remote intent, the helper rechecks the original zero-intent custody, new plan, and exact continuation guard bytes. It then requires the exact ordinary expected-head merge action and creates an exclusive fsynced `remote_intent_guard.json` in the successor run before appending the intent. That fence prevents direct reuse of the same open journal or concurrent same-object calls from claiming a second remote intent; append failure, response loss and later STOP leave it consumed.

Only this one merge continuation is supported. A later STOP, even before a remote intent, leaves this guard consumed; another attempt needs separately reviewed explicit work. Any attempted remote write retains the existing no-retry/GET-only recovery rules. The merge action still sends one ordinary expected-head PUT through the unchanged `execute()`/`mutate()` and preservation checks. GitHub ref/API CAS limits and the selected-preserving descendant-main predicate remain unchanged.

Root’s actual descriptor is `root_administration_inputs/ROOT_PREINTENT_MERGE_CONTINUATION_DESCRIPTOR.json`, SHA256 `7bc150a109e2ad48edafe5669e57d261944f5eeaad8de31526a4cfae2a417c48`. Root owns later native plans, fresh bindings and approvals. Add the same descriptor and original journal root to each separate plan/apply invocation:

```text
--continuation root_administration_inputs/ROOT_PREINTENT_MERGE_CONTINUATION_DESCRIPTOR.json:7bc150a109e2ad48edafe5669e57d261944f5eeaad8de31526a4cfae2a417c48
--journal-root /absolute/original/case/private_sources/root_merge_phase_journals_20261013
```

The current plan and its separate approval must be regenerated with this exact V5 helper and genuinely fresh native inputs. `plan` validates custody without allocating a continuation guard; `apply` consumes the durable guard only after the fresh canonical plan, approval, and deadline agree. The new run ID must differ from the stopped run. This prepared component grants no phase approval.

Offline controls require the privately held pinned ADMIN originals and a new nonexistent output directory:

```sh
python3 -B continuation_controls.py --case /absolute/case --private-dir /absolute/new-private-controls
python3 -B -O continuation_controls.py --case /absolute/case --private-dir /absolute/new-private-optimized
python3 -B cli_controls.py --case /absolute/case --private-dir /absolute/new-private-CLI
```

These execute copied path-adjusted synthetic ADMIN fixtures, fake API guards/responses and isolated CLI subprocesses. They read no scientific files or assets, contact no service, and never instantiate `Journal` on the actual operator root. Genuine prior custody receives only read-only validation. No production success or fresh native verification is claimed. Raw receipts, fixtures, runtime and private state are excluded from delivery.

Obtain the actual final seal digest independently, then verify the positive public inventory:

```sh
python3 -B verify_custody.py --expected-seal-sha256 ACTUAL_EXTERNAL_SHA256
```

The seal binds the actual whitelist, and both exclude themselves from payload entries. The external actual seal digest anchors custody without a self-hash cycle. V4, its seals and the original actual claim/journal/STOP remain unchanged.

The first independent V5 review at source942 found one direct-object retry counterexample despite its one-shot CLI passing. Its blocked verdict, source and two-PUT counterexample remain sealed as historical evidence. Intermediate source2c23 added the durable remote-intent fence. Intermediate sourceabd32 also snapshots live integer FDs before intent processing; a closed Journal stops before any file open or CWD fallback. A fresh reviewer then found that a terminal pre-intent STOP could be bypassed by reusing its same open object. Current source98fb additionally refuses any successor receipt entry before intent processing. `TERMINAL_RECEIPT_REPAIR_DIFF.patch` isolates this final correction; the fresh abd32 blocked review remains authentic. `CLOSED_OBJECT_REPAIR_DIFF.patch` isolates this final edge repair. After all corrections, a NEW fresh final independent adversary reviews the exact current98fb helper and compact package. `REMOTE_FENCE_REPAIR_DIFF.patch` isolates it, while `SOURCE_DIFF.patch` shows the complete V4-to-current change.

Supported contract: the root one-shot CLI and normal Journal lifecycle, including sequential reuse after a completed STOP/finish/close and concurrent remote-intent claims. Existing receipt entries of every file kind are terminal and are inspected without following links or opening FIFO data. The component does not promise safety under arbitrary private-member or standard-library tampering, deletion of durable guards/receipts, or malicious host behavior. Existing GitHub CAS/race limits remain unchanged.
