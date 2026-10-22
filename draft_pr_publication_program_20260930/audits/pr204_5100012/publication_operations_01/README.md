# PR204 guarded operations preparation

Use revision_02/publish_exact.py and revision_02/update_tracker.py as the current drafts. Root-level scripts preserve the earlier tested revision. FINAL_REPORT.md and RECEIPT_CONTRACT.json describe authority and receipt compatibility.

Reproduce only the offline preparation checks with Python3.14:
`python3 -B revision_02/run_offline.py --prefix NEW_UNUSED_PREFIX`
The prefix must be new; existing evidence is never overwritten. This runs fake transports only, records both ordinary and optimized modes, and creates disposable fixtures within revision_02/offline_work. It does not run the repository Zenodo KIT, GWS, authentication or network.

Real operations are separate explicit invocations of publish_exact.py modes stage, inspect, publish, inspect-doi and finalize; update_tracker.py has append and recover modes. Every real invocation requires the authentic Root gate, actual ready90 acceptance and exact package. Publish requires --confirm-id. Unknown mutation outcomes require read-only inspection or recovery; never delete the inflight marker or original baseline to force a retry. --base locates PR204, and --kit can identify the byte-pinned repository KIT. No home-specific path is required.

Private service responses and full sheet baselines, if real operations are later separately authorized, stay in PR204/private_operations. Column B remains blank unless a future explicitly reviewed change supplies a verified user-provided share URL. These drafts never auto-share. Current test success is preparation only.
