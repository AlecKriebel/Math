# Prepared helper; no compression has been executed

Prepared 2026-10-03 by the SOURCE subagent for ROOT review. This is an administrative proposal, not a mathematical review or an actual-run receipt. Only this new directory was written. No historical evidence body, Git data, native problem record, live family, or remote was changed.

The helper permits exactly three completed historical paths under `/Users/alec/Documents/Math/draft_pr_publication_program_20260930`: the checkpoint `PRIVATE_CHECKPOINT_INDEX` pilot, its sibling `RECONCILED_REAL_INDEX`, and the optional completed PR47 command-67 `stdout.bin`. It accepts named targets rather than arbitrary paths. The latter two require a successful positive-saving pilot receipt from this helper and a matching current pilot file. No follow-up runs are proposed before ROOT reads the pilot result.

The pilot pins the originally reported SHA256 `d8906de0095a0ac86d1afd15e2f351814fb91b3c2db3e60e70d8aa35764091aa`, 21,767,721 logical bytes, 21,770,240 allocated bytes, full mode 0644, flags 0, one link, and the sole existing xattr name `com.apple.provenance`. Actual existing xattr values, owner/group, nanosecond mtime, ACL, and complete available stat fields are captured at runtime and checked; they are not invented here.

ROOT must ensure these exact files remain completed and quiescent for the entire operation. The helper takes advisory exclusive locks on its own operation lock and the source descriptor. These do not prevent an uncooperative writer; a POSIX stat-check followed by rename is not a conditional atomic rename. The immediate final body/metadata/descriptor/path checks require a stable original inode/device and full post-read stat. No concurrency guarantee beyond ROOT's quiescence requirement is claimed.

Each run creates a private directory only here. It preserves a full prelaunch helper body, operator PID/argv/executable/flags/UTC, literal ditto argv, genuine native child PIDs/start/end/exit, full ditto stdout and stderr, and full base64 ACL-command stdout/stderr. It strips `DITTO*` environment variables and explicitly enables resource forks, xattrs, ACLs, and quarantine metadata. `prelaunch.json` is flushed and synced before ditto. The stage has the original basename and is checked to be on the same device.

The native invocation is `/usr/bin/ditto --hfsCompression --noclone --nocache --rsrc --extattr --acl --qtn SOURCE STAGE`. Staging must preserve every logical byte by full SHA256 and size, the entire mode including special bits, uid/gid, nanosecond mtime, ACL entries, and every original xattr value. Added compression bookkeeping attrs are limited to `com.apple.decmpfs` and `com.apple.ResourceFork`; an existing resource fork must remain byte equal. Flags must change only by adding `UF_COMPRESSED`. The allocated-block saving must be strictly positive. All these checks precede `os.replace`.

The original filename remains unchanged. Replacement necessarily changes inode and ctime and may change birthtime. Native reads can change access time; access time preservation is not claimed. Before/stage/after stat records expose these changes. ACL equality compares every raw ACL-entry line from native `ls -lde`, excluding its filename/stat header. No full-metadata-unchanged claim is made. No source chmod/chown/xattr operation, gzip rename, cache deletion, evidence deletion, or rollback/backup deletion is performed.

Before replacement, copy/check/write failures leave the original pathname unreplaced and retain any own temporary files plus a failure record where storage permits. A successful atomic replace is the commit point. If later readback or receipt writing fails, the status is explicitly `POSTCOMMIT_RECORD_FAILURE` with `source_replaced: true`; it must never be described as an untouched-original failure or a completed positive pilot. The already synced `prepared.json` preserves the checked stage and anticipated transformation. ROOT should also retain the complete outer command streams, since neither disk-full errors nor interrupted processes can guarantee a final receipt.

## Future ROOT command-record plan — all commands below unexecuted

Before any run, ROOT should full-read this source, copy its exact bytes and mode into its own actual-capture record, record literal argv/cwd and current UTC, and launch the pilot with `Popen` or its existing genuine capture operator. Record the actual operator and child PIDs, UTC interval, full stdout/stderr, exit status, and the helper source SHA256. Do not substitute an intended PID, historical capture, bounded preview, or this plan for actual evidence.

Pilot argv:

```
/usr/bin/python3 -B /Users/alec/Documents/Math/draft_pr_publication_program_20260930/storage_compression_20261003/compress_completed.py pilot --confirm-completed-quiescent
```

Only after full-reading a genuine `COMPRESSED` pilot receipt, confirming a positive saving, and checking original bytes/required metadata, ROOT may consider either named follow-up. Supply the exact absolute pilot `receipt.json` path emitted by that run; the placeholders below are not receipts:

```
/usr/bin/python3 -B /Users/alec/Documents/Math/draft_pr_publication_program_20260930/storage_compression_20261003/compress_completed.py reconciled --confirm-completed-quiescent --positive-pilot-receipt EXACT_PILOT_RECEIPT_PATH
/usr/bin/python3 -B /Users/alec/Documents/Math/draft_pr_publication_program_20260930/storage_compression_20261003/compress_completed.py pr47-stdout --confirm-completed-quiescent --positive-pilot-receipt EXACT_PILOT_RECEIPT_PATH
```

Review basis: the locally installed native `ditto` manual was read, including compression, cloning/cache options, explicit metadata preservation, environment switches, and failure behavior. The source was parsed without executing/importing it. No compression behavior, runtime failure path, saved space, or ROOT approval has been tested or claimed by this SOURCE preparation.
