# Integrity validation scope and results

These checks concern local source and audit-artifact integrity only. They do not test or certify a universal mathematical statement.

| Check | Normal Python | Optimized Python (`-O`) | Check mechanism |
| --- | --- | --- | --- |
| Source receipts: three acquired source bodies and three permitted original inputs | Pass, 12 explicit checks, 2026-10-12 15:42:48.879 UTC | Pass, 12 explicit checks, 2026-10-12 15:42:48.951 UTC | Compare actual bytes and SHA256 against clean receipts; missing/unavailable bodies or mismatches raise errors. |
| True first inventory before feedback | Pass, 70 explicit checks, 2026-10-12 15:48:24.551 UTC | Pass, 70 explicit checks, 2026-10-12 15:48:24.557 UTC | Compare all 23 existing payload files' bytes, SHA256, and modes; separately require manifest mode0444. |

Neither utility uses Python assertions. Final inventory validation is run in both modes after creation and is emitted as an external receipt to ROOT, avoiding any post-validation addition that would invalidate the frozen file enumeration. It additionally checks that the actual complete file tree is exactly the inventory payload plus the manifest itself. All files are mode0444 at final freezing.

The first inventory records historical pre-feedback file modes and the log's pre-feedback bytes. Later log additions and freezing of other files are intentional changes recorded in the final inventory, not alterations to the immutable first assessment or first inventory.
