# Private actual replay

Keep this closed audit and all frozen input packets read-only. On this workspace, run:

```sh
/usr/bin/python3 /Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr34_7000004/v2_whole_adversary/replay_closed.py --output /Users/alec/Documents/Math/draft_pr_publication_program_20260930/audits/pr34_7000004/tmp/root-v2-whole-private-replay
```

Use a fresh nonexistent output directory. The helper accepts a private path under parent tmp or this audit's tmp, verifies every closed-audit member and all273 frozen currentv2 bindings, copies authored members into the new private output, and ACTUALLY runs the byte-exact historical nine-program runner, new v2 verifier and unchanged first-whole control replay. It preserves actual streams/return codes and compares all structured results against this closure. The only excluded comparison fields are fresh UTC clocks and stderr hashes that incorporate changed private traceback paths. It requires the old mandatory administrative failure to remain recorded as a failure and checks source/current bindings again after execution.

The output ROOT_REPLAY_RESULTS.json reports reproduction only. It cannot cure the disclosed source-first order failure or create a final acceptance gate. It does not run either packet builder, legacy queue generating entrypoints, publish, or communicate externally. Python3.9.6/SymPy1.14.0 were the verified runtime. Source file/cache/Git paths are intentionally pinned to this workspace; moving the repository requires a reviewed adaptation rather than assuming these absolute-path receipts apply.

Fresh PDF/HTML/notebook bytes are private ignored inputs bound by SHA256 in SOURCE_RETRIEVALS.json and ADDITIONAL_SOURCE_RETRIEVALS.json. The exact historical nine-run runner needs existing read-only source cache/SQL/Git inputs and preserves the full private corpus audit. HTTP retrieval helpers can separately be copied and executed privately when a new dated source receipt is wanted; those changing retrieval timestamps do not replace the frozen receipts or certify unchanged bytes without an explicit hash comparison.
