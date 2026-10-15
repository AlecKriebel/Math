# V3 proposal: completed private evidence copies only

Prepared 2026-10-03 15:28 UTC. V3 is unexecuted. V1/V2 sources, plans, logs, and actual ROOT receipts were not changed. The only executed new program was the read-only inventory, which hashed the exact eight candidates and read native metadata without copying their bodies. This is administrative preparation, not a scientific review or acceptance.

V3 permits exactly the three completed private PR39/PR38/PR33 `catalog.sqlite` copies requested by ROOT, the observed PR39/PR38 copies of `problems.json` and `research_results.json`, and PR41 `COMPLETE_TYPED_NODES.jsonl`. Exact paths appear in both the static helper allowlist and V3_INPUT_PINS.json. The optional JSON copies were found under those replicas' `unsolved_math_prioritization/cache/` directories; literal `data/` directories were absent. No canonical active raw corpus, `.git`, runtime, current primary, foreign family, or other path is permitted.

Read-only inventory operator PID 32016 launched child 32017 on 2026-10-03 at 15:22:47.577204 UTC; child exited 0 by 15:22:48.877576 UTC. Full inventory stdout, empty stderr, operator details, and the preserved inventory source are retained here. Source SHA256 is `b40463c0facf0c24c1882d298b6bb9bd262c1589b2bd4abb80ee7ccded4d0885`; full stdout SHA256 is `ab1cb1ebeb74fcb0ec2fa39ece1f42e2056bd975fdbeb0a5480ee28658cd92b4`. Actual native metadata child argv/PID/UTC/exit/full stdout/stderr are included in that stdout JSON.

All eight were present, singly linked regular files with flags 0 and uid/gid 501/20. PR33's catalog mode is 0644; the other seven modes are 0444. They remained stable across hashing and metadata reads, excluding only access time. Original allocated bytes total 876,691,456; logical bytes total 876,682,954. These totals are inventory sizes, not measured future savings. Each had only the same original `com.apple.provenance` value and no ACL entries. The compact 6,614-byte pin file binds each exact full SHA256, full stat, original xattrs, and ACL; its SHA256 is `4b9e86def253348a5b9e229ce6ec9162b080244afd0e44a258c994cc34061de8`.

The PR41 file was mode 0444 and unchanged during the inventory. Native `lsof -Fpcfatn` returned exit 1 with empty stdout/stderr, showing no matching open descriptor at that instant. This does not establish future absence of writers. ROOT must confirm the exact candidates remain completed and quiescent throughout each operation. No missing or already compressed candidate was found; if this changes, skip it rather than weakening the pin.

V3 requires the exact real V2 pilot receipt `pilot_h6k3r187/receipt.json`, SHA256 `8cef7006fe4fcb0dcf941930b909fa0f89bb343af690ec50a652c21367dbcd81`, whose source helper SHA is `10723bfc0432104fc281b1023d51235be7372f977fd95f3150744e182e05c8b1`. Its actual metadata were read here: status COMPRESSED, operator PID 25978, saving 18,149,376 allocated bytes. That was ROOT's V2 run; V3 has no pilot run. V3 checks the receipt identity, positive saving, V2 source version, and current pilot bytes/metadata excluding only access time. A fabricated or different-version pilot cannot qualify.

The runtime mechanisms are unchanged from V2: bounded native xattr reads, full original-value preservation, compact hashes for added compression bookkeeping, complete ditto streams, mode/owner/group/mtime/ACL/xattr checks, exact compressed flag transformation, strictly positive allocated-block saving, same-device private staging with original basename, source descriptor/path/body/stable-stat recheck, and atomic replacement. V3 additionally checks the immutable input-pin file and exact candidate identity before staging. It records inode/ctime/birthtime/flags changes honestly and retains the truthful postcommit failure distinction. Per-file allocated-block differences need not equal device-wide free-space changes when filesystem extents are shared.

Only the allowlist, original input pins, canonical V3 source pathname, and the explicitly reused V2 pilot gate differ from V2. No replacement, storage saving, ROOT approval, source closure, mathematical verdict, or acceptance has been performed by this preparation. Stage files are ordinary own temporary copies; no cleanup is authorized or implemented.

Future ROOT invocation, **unexecuted**, using one exact named target at a time:

```
/usr/bin/python3 -B /Users/alec/Documents/Math/draft_pr_publication_program_20260930/storage_compression_20261003/compress_completed_v3.py pr39-catalog --confirm-completed-quiescent --positive-pilot-receipt /Users/alec/Documents/Math/draft_pr_publication_program_20260930/storage_compression_20261003/pilot_h6k3r187/receipt.json
```

Other exact target names: `pr38-catalog`, `pr33-catalog`, `pr39-problems`, `pr39-results`, `pr38-problems`, `pr38-results`, and `pr41-typed`. ROOT should full-read V3 and the pins, capture the actual source/argv/operator and child PIDs/UTC/full streams, then read every resulting receipt. No bulk or unattended execution is proposed.

Checkpoint: preparation estimate 100% after syntax-only verification; compression of these eight files remains 0% in this agent's work. The observed earlier V2 compression remains credited to ROOT's genuine actual runs.
