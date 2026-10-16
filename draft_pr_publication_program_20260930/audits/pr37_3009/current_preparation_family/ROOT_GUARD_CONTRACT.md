# Root-only current-packet builder contract

This is prepared administrative source, not an executed build or new verdict.
All preparation writes are contained in this folder. The preparer has not
executed or imported the builder, replayed any verifier, read the live third
manifest as final, mutated Git or written shared/canonical/remote state.

Root supplies these exact arguments only after actual reproduction and closure:

- `--execute`
- `--third-manifest-path` for external audit-root closure (default RECURRENCE_FAMILY_ROOT_CLOSURE.json)
- `--third-manifest-sha256` for that external root closure of all21 recurrence files
- `--third-member-count` for every closed first-party member in that manifest
- `--root-receipt-sha256` for ROOT_CLOSED_FAMILIES_ACTUAL_REPRODUCTION.json
- `--root-replay-script-sha256` for reproduce_root_closed_families.py
- `--root-scope-certificate-sha256` for finalized ROOT_PARTIAL_SCOPE_CERTIFICATE.md

The two already closed manifest pins are hardcoded exactly as root supplied:
planar_fixed_continuum_family 10 members,
8165a184bc02e3c6f940c45fbf8aeea4f4a034225c2788a35949849880cf5dd6;
primary_scope_family 17 members,
d53bc8be2de3767f25c5c1576628027750c787b319ff4935c6d1991164acc590.
Root subsequently declared the third family CLOSED21. Its member-count guard
is now exactly21, for48 total authored members. Its final digest is still
required explicitly and is not inferred from a live directory.

The actual final root receipt must contain:

```json
{
  "status": "PASS",
  "closed_family_count": 3,
  "authored_members_verified_before_and_after": "integer: 27 plus third-member-count",
  "original_substantive_turns": 1,
  "turn_limit": 5,
  "new_substantive_attempts": 0,
  "root_script_sha256": "exact actual root collector SHA256",
  "hamilton1954_complete_three_page_proof_read_by_root": true,
  "actual_outer_program_runs": [{"exit": 0}],
  "full_structured_receipt_comparisons": ["actual root comparison records"],
  "family_manifests": {
    "planar_fixed_continuum_family": {
      "manifest_path": "planar_fixed_continuum_family/authored_manifest.json",
      "sha256": "8165a184bc02e3c6f940c45fbf8aeea4f4a034225c2788a35949849880cf5dd6",
      "member_count": 10
    },
    "primary_scope_family": {
      "manifest_path": "primary_scope_family/FIRST_PARTY_MANIFEST.json",
      "sha256": "d53bc8be2de3767f25c5c1576628027750c787b319ff4935c6d1991164acc590",
      "member_count": 17
    },
    "recurrence_orientation_family": {
      "manifest_path": "RECURRENCE_FAMILY_ROOT_CLOSURE.json",
      "sha256": "root-supplied final digest",
      "member_count": "root-supplied final integer"
    }
  }
}
```

The displayed strings describing integers/records are schema documentation,
not values to put in an actual receipt. The run interface accepts `returncode`
instead of `exit`. Final successful runs must actually return zero; observed
failure attempts stay in preserved support evidence. Root must provide actual
complete comparison records, rather than reducing the evidence to labels.
The finalized scope certificate must preserve the earlier dated Hamilton await
note and add a dated current addendum containing the literal marker
`ROOT_FINAL_CURRENT_ADDENDUM`. Root confirmed its actual three-page reading is
now complete. The actual final receipt still carries the explicit reading flag.
Printed1998 disk passage access remains unverified; no later text is backdated.

The recurrence original authored_manifest.json is a21-file allowlist including
itself, not a self-excluding set of hashed rows. Its manifest_verification.json
pins20 files except its own hash. Root supplies a new external audit-root
RECURRENCE_FAMILY_ROOT_CLOSURE.json whose files list/map has relative-to-family
paths and exact bytes/SHA256 for ALL21 unchanged files, including both original
inventory files. The builder hashes this external manifest, reads member bytes
from recurrence_orientation_family/, and requires its actual non-scratch file
set to equal the21 entries. It never writes inside the closed family. Both
original inventory files and the external closure are copied and bound exactly.
The recurrence closure is not relabelled as an originally self-excluding manifest.

Optional root retention/failure/revision binding uses both
`--root-support-manifest PATH` and `--root-support-manifest-sha256 SHA`.
The audit-relative manifest must have `status: PASS`,
`root_reproduction_receipt_sha256` equal to the final root receipt, and a
`files` list/map of audit-relative `path`, `bytes` (or `size`) and `sha256`.
It may enumerate actual first-party stdout/stderr streams, fresh receipts,
root implementation code, preserved failure receipts and prior source
revisions. No tmp/ignoredtmp/cache/foreign-source path is admitted. This
explicit manifest is the mechanism to bind future retained actual outputs;
the preparer has not invented an existing stream inventory.

Root's build produces a new reviewed_candidate directory only when absent,
uses a unique retained stage, copies exact original13 into original_archive,
freezes every closed family member, preserves exact source/turns/diagnostics,
and writes a strict self-excluding MANIFEST. It proposes unsolved1/5 in an
exact twelve-column queue row but writes no queue. A NEW whole-current-package
source-first gate remains pending even after successful administrative freeze.

The administrative patch changes exactly three PARTIAL strings: original
dated runtime header scope, explicit2009v3-versus-printed1998 qualifier, and
the same disk qualifier at its later reference. It changes no proof equation,
hypothesis or deduction. The exact original, unified patch, replacement byte
offsets/text/sizes/hashes and current hash are emitted as checkable evidence.

The source has two exact stored serializations: original source_record uses
default indent-two ASCII escaping, while root pinned_problem uses ensure_ascii
False. The builder preserves both byte-exact versions, requires entire-object
JSON equality, and emits CURRENT_SOURCE_SERIALIZATION_RECEIPT.json with both
sizes/hashes and actual byte-equality result. It does not falsely equate those
different bytes or silently reserialize the original.

Preparation completion estimate: 100% as of 2026-10-02 08:15:11 UTC; actual final freeze and new current gate
remain root-owned. Complete KP-5.2 resolution estimate: 0%, unchanged. No new
substantive response or audit proof-search turn is claimed.
