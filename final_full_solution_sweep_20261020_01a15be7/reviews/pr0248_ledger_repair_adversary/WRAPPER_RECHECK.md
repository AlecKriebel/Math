# Revised wrapper adversarial recheck

2026-10-21T02:15:29Z — focused recheck 100% complete.
Wrapper SHA-256: `ed7d6e3797cba392c228e84266a002de344e46312fb39c9c89d20819f308b09b`.
Eighteen synthetic cases use the actual imported `zenodo_dois` helper (bytecode
writes disabled), fake API/subprocess calls and disposable fixtures under this
review folder. No live record, credential, payload, or shared Git action occurred.
See `WRAPPER_RECHECK.json` and `test_repair_wrapper_revised.py`.

## Previous action-safety findings addressed

- Open-ended range detects duplicates beyond row1169.
- HTTP, uppercase dx.doi.org and direct Zenodo record URL duplicates reject.
- Wrong numeric ID and stale eligibility head reject before mutation.
- Formula notes reject; concurrent notes remain intact.
- A changed source/DOI detected immediately before CAS prevents the write.
- A late identity swap causes a conditional rollback of the exact appended
  notes, retaining the changed identity cells. If notes change concurrently
  before rollback, the rollback condition fails and preserves those notes.
- Recovery of a prior intended value performs no repeated write and retains
  the original before/proposal artifacts.
- Post-mutation response/after/receipt persistence failures still permit
  readback and print a verified receipt before the final local-save error.

## One remaining preservation finding

`prior_same_old_snapshot_retention` demonstrates that an existing **unexecuted**
proposal and before-snapshot are overwritten when the current notes still equal
the prior old notes. Both `retained_before_unchanged` and
`retained_proposal_unchanged` are false. The fixture includes a later unrelated
sheet edit, so the original snapshot is actually lost rather than merely
reformatted. The recheck's other cases pass.

The preservation fix currently applies only to the recovered already-applied
branch. Retain the original proposal/before files for the ordinary pending
branch too; write fresh execution observations under separate immutable attempt
names (or explicitly archive the original before replacing it). This is a
local-evidence issue, not evidence of an incorrect live mutation in these tests.
It is relevant now because PR254 already has an earlier dry-run proposal.

## Residual boundaries

The Sheets operation is still not a transaction on the identity cells and D.
The new guard/rollback mitigates and detects tested races; an API/network failure
or another concurrent change can require manual reconciliation. In particular,
a CLI error after an uncertain mutation can occur before immediate readback;
the preserved proposal permits a later recovery check. Do not claim universal
atomicity or silent success under such failures.

This is wrapper/identity/ledger safety review, not new mathematical, originality,
or priority clearance for PR254 or any other result.
