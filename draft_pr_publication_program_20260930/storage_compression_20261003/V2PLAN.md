# V2 source correction — unexecuted

2026-10-03 15:11 UTC. Preparation estimate 100% after syntax-only inspection; actual storage relief 0%. The frozen V1 helper, PLAN, and RESEARCH_LOG remain unchanged. V1 is superseded for any future execution. No helper or compression command has been executed during this correction.

The actual `/usr/bin/python3 -B` interpreter was checked read-only: both `os.listxattr` and `os.getxattr` are absent. The local `/usr/bin/xattr -h` output was read. Its names-only form is `xattr PATH`; `-p` prints a value, and `-x` represents that value as hex. V2 uses the literal native argv `["/usr/bin/xattr", "-px", NAME, PATH]` and parses the returned hex.

Names output is checked against a 16 KiB / 64-name bound with duplicate rejection. Hex lines are read with an 8 KiB bound. Original xattr values are bounded to 64 KiB each and preserved as complete base64 logical values, with the complete native hex stdout and stderr in command records. A larger original xattr aborts before replacement; its value is never silently omitted. Names and ACL command output, original attribute output, and full ditto streams remain actual runtime evidence with real argv/PID/UTC/exit records.

New names are accepted only for `com.apple.decmpfs` and `com.apple.ResourceFork`. Their values are streamed through the hex parser with a 64 MiB logical limit and recorded by name, decoded byte count, and full SHA256. Their raw hex stdout is intentionally not copied into JSON or a file; its hash is recorded and its retention field explicitly says `compression bookkeeping hash only`. Full stderr is retained. An existing resource fork is an original attribute and must remain fully byte equal. No raw compressed-encoding copy is made for added bookkeeping attributes.

Stable stat comparison now excludes **only** `st_atime_ns`. This applies to snapshot consistency, current-pilot identity, source descriptor identity, pre-replace source identity, and the immediate final pathname stat. Every other captured stat field remains compared. Snapshots retain the actual pre-read, post-body-read, and post-metadata-read stat values, including access time. Reading-induced access-time changes therefore remain visible without causing a false integrity rejection.

The exact three-path allowlist, source pilot SHA/size/full mode/flags/link/xattr-name/allocated-size pins, required uid/gid/mtime/ACL/original-xattr preservation, compressed flag rule, positive block saving, same-device staging, final inode/device/body/stable-stat checks, and atomic replacement are unchanged. The completed-file quiescence requirement and truthful `source_replaced` / postcommit-record-failure distinction remain as described in PLAN.md. V2 requires a positive pilot receipt bound to the V2 helper hash before either follow-up; a V1 receipt cannot qualify.

Future ROOT pilot argv, **unexecuted**:

```
/usr/bin/python3 -B /Users/alec/Documents/Math/draft_pr_publication_program_20260930/storage_compression_20261003/compress_completed_v2.py pilot --confirm-completed-quiescent
```

Use the existing outer genuine command-record plan in PLAN.md, substituting the V2 source pathname and its actual current hash. ROOT should full-read V2 before deciding to run it. For either later named target, use this V2 pathname and the exact real positive V2 pilot `receipt.json` path. No runtime preservation, actual saving, native acceptance, or ROOT approval is claimed by this source correction.
