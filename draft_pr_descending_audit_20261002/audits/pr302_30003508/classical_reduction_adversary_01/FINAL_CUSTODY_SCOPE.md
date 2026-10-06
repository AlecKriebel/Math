# Final physical seal and custody scope

The initial `NAMESPACE_CLOSURE.json` and `.sha256` remain unchanged at their original paths. Exact historical copies are made before any new closure manifest is generated. All 95 bodies pinned by that original manifest must retain their original hashes; the seal changes their permissions only.

Historical `run_capture.py` records bind actual child PID, argv, cwd, UTC start/end, complete captured stdout/stderr, return status, and recorder SHA. They do **not** bind full executable/runtime bytes at each historical launch. They did not preserve each historical child-program version either. No stronger retrospective launch custody is asserted. Those records remain unchanged.

`CURRENT_CLOSURE_CUSTODY.json` independently pins full bytes of specifically listed executables, the Python framework library, selected runtime module files, and current recorders/child programs at closure time. These are current-time observations, not historical byte claims. It does not claim exhaustive transitive runtime/dependency capture. Binary files are hashed in place, not copied into this folder.

The final closer is a real child process. Its actual PID, argv, cwd, UTC times, complete stdout/stderr and exit status are captured in `process_evidence/physical_seal`. The wrapper opens the final receipt/stream/manifest files before the child removes write permission; these already-open descriptors permit completion of the capture. Every such descriptor is closed before the wrapper reports success. This is an explicit completion procedure, not an assertion that chmod revokes existing descriptors.

The child verifies actual files `0444` and directories `0555`, including the namespace root. The wrapper independently verifies them after child completion and after closing every administrative write descriptor. `FINAL_SEALED_NAMESPACE.json` lists every body and directory with final modes. The two new administrative manifest files have explicit self-reference exclusions; both original manifests are fully hashed payloads in the new closure. The seal makes this a read-only filesystem snapshot under ordinary permissions; it does not claim immutable storage or prevent the owner from deliberately changing permissions later.

Audit completion remains 100% of the assigned validation. This checkpoint adds custody and physical sealing only; it changes no proof, source, verdict, historical process record, Git/index/global mapping, tracker, release, or external communication.
