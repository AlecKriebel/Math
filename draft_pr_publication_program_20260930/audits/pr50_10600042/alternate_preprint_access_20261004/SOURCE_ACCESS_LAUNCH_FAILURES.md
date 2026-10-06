# Local recording failures and recovery

The first two attempts to launch `record_access_limits.py` failed inside the
outer command recorder while creating its destination folder, with
`OSError: [Errno 28] No space left on device`. Neither attempt launched the
child helper; neither created a completed capture or changed publication state.
The tool conversation preserves both actual failure outputs.

ROOT then deduplicated two byte-identical, already committed outputs from the
fully completed PR18 audit. Both filenames, file contents and permissions remain
intact. `OWNED_DUPLICATE_STORAGE_RECEIPT.json` records the genuine process and
observed disk counters. The actual executed inline program was saved afterward
as `deduplicate_completed_pr18_outputs.py` with one additional final newline;
its receipt's source SHA256 binds the executed inline program rather than that
newline-normalized saved file. This is not a prelaunch source snapshot.

After recovery, the same source-record helper genuinely ran as child10836 with
exit0 at2026-10-04T02:07:00.002731Z–02:07:00.120379Z. That completed run is the
one bound by `root_pr50_public_source_access_record_20261004_actual_capture`.
No Chrome cache was cleared again and no unique source, proof, package or
foreign artifact was removed.

The first scoped Git helper then failed before staging or writing its plan: git diff attempted an index refresh and reported an index.lock write error from insufficient disk space. The complete actual child12344 capture and private Git command journal are preserved. Additional hardlink and native clone deduplication preserved every original path/body/mode, including two distinct committed PR18 snapshots verified against Git. The revised checkpoint helper uses a new command journal and includes the completed failed capture; it does not overwrite earlier evidence.
