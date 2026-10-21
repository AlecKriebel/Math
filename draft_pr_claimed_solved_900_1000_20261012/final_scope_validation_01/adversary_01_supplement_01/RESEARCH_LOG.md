# Research log: supplementary raw-retention repair

| UTC checkpoint | Finding / decision | Best guess narrow repair completion |
| --- | --- | ---: |
| 2026-10-16T22:01:50+00:00 | Acknowledged parent's case-insensitive filename-overwrite finding. Reauthenticated the external original manifest and all 458 members, preserved them unchanged, and created a sibling supplementary namespace. | 20% |
| 2026-10-16T22:02:20.664484+00:00 | New numbered exclusive-create raw filenames and explicit test/invocation/raw bindings passed all 84 controls in actual modes 0/1/2. Each mode recorded 72 controller invocations and retained 72 raw files. Both lowercase and uppercase statuses survived independently. | 80% |
| VERIFICATION.json timestamp | Independent archive verification checked every new raw receipt and the unchanged original seal, confirming 216/216 retained raw controller receipts and 252 passing new executions. | 95% |
| RESULT.json timestamp | Exact harness delta, correction report, result, verification evidence, and supplementary explicit allowlist sealed. The old report's 71-invocation and complete-retention claims are explicitly superseded. | 100% |

This repair changes evidence bookkeeping only. The inherited 49 controls and sweeper source remain unchanged. No mathematical research or global completion assessment was performed.
