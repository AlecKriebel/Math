# Root actual-replay evidence binding update

2026-10-02T07:36:40.969754+00:00 — preparation completion **100%**. The revised builder has **not been executed or imported**. Previous active revision is preserved as `historical_revisions/prepare_current_packet_v3_before_root_retention.py`; the older report and static checkpoint remain historical observations.

Current builder SHA256: `ae8ae959a0de3c682d4d5e44005a4a01cea7b3261c27f01d539207c42b0c7bef`.

The builder now explicitly binds `ROOT_REPLAY_RETENTION.json`, `retain_root_replay.py`, and all **72** manifest-listed safe first-party streams/fresh receipts. It checks every retained byte size and SHA256, unique safe paths confined to `root_actual_replay/`, allowed first-party output extensions, the finalized PASS/count/new0 fields, and exact receipt linkage. No broad ROOT glob or scratch/foreign inclusion is used.

The three exact preserved comparison/setup receipts are:

- `ROOT_CLOSED_FAMILIES_STREAM_NAME_SETUP_FAILURE.json`
- `ROOT_CLOSED_FAMILIES_COMPARISON_SETUP_FAILURE.json`
- `ROOT_CLOSED_FAMILIES_DATED_CONTROL_MANIFEST_COMPARISON.json`

The three explicit preserved collector sources are:

- `root_replay_revisions/reproduce_root_closed_families_before_dated_control_manifest.py`
- `root_replay_revisions/reproduce_root_closed_families_before_executable_stream_names.py`
- `root_replay_revisions/reproduce_root_closed_families_before_full_stderr.py`

All six and the retention implementation have frozen size/SHA256 guards in the builder and are added as exact anchored dependencies. Their failures/corrections remain preserved observations and are not relabelled initial success. The exact retention manifest is copied into the current packet's root-verification evidence; its listed outputs remain reproducible at the repository audit anchor.

The finalized root receipt guards now also check original1/5, new0, **28** outer executions, **13** full structured comparisons, **170** full authored JSON/JSONL parses per before/after pass, and exact collector linkage. This records the actual already completed root evidence; the builder performs no new mathematical replay.

Actual read-only finalized pins:

| Input | SHA256 |
|---|---|
| Root reproduction receipt | `4281326133d4ae59a8da5fde61d82544dd2c8ce393219dbed7c33801b2be2b54` |
| Root priority decision | `ae1e9af799be1461eed24ec08aacc46a5585968d2bad0089f1b38c21a50a217d` |
| Root actual collector | `4f15d917bb8b6d59b4fb00f0ef604d0480bc2e74a910305bb9869ad042c4a24a` |
| Root retention manifest | `426186631fe35c19e535f1f289f15d6468735fbc5b76b45b279a80ac6d14539a` |

`STATIC_ROOT_RETENTION_REVIEW.json` records successful static parsing, all364 unchanged family-member hash/size checks, all72 retained root-member checks, all explicit extra pins, and every finalized root guard as true. No current candidate existed at that checkpoint. The NEW whole-current-packet source-first gate remains pending; original science/accounting preservation and queue-only prospective scope are unchanged. All preparation writes stayed inside this folder, no mathematical claim was changed, no outside individual contacted, original1/5/new0/audit0.
