# Independent Linux CI evidence review

Final checkpoint: 2026-10-24T15:44Z. Completion estimate: **100% for both Linux CI evidence reviews**. The final combined source-build and endpoint-replay run passed. This report is frozen after the final review below.

## Initial source-build run

[GitHub Actions run 40105321824](https://github.com/AlecKriebel/Math/actions/runs/40105321824) succeeded on commit `03aecadaf76a43b8c5307a3f3c15f6978d37e251`. The Lean job ran on Ubuntu 24.04. Its preserved run is `20261024T150601Z-da92833f`. I independently recomputed and checked the evidence rather than relying on the parent's validation summary:

- All 104 protected-input hashes match the current workspace; all 122 command-log hashes match their receipt. Exactly two protected inputs differ from the September extraction: `scripts/run_lean.py` and `scripts/test_preflight.py`. Mathematical Lean sources remain unchanged.
- Individual build logs contain `Built` results for every one of the 68 production modules and the aggregate `Bell` module. Subsequent Lake `Replayed` messages only redisplay already completed build results; the earlier per-module logs establish the fresh compilation.
- All seven contract files, containing 78 anonymous examples, passed. Independently parsed raw axiom output contains exactly 826 distinct public declarations, equal to the public declaration inventory, with only `propext`, `Classical.choice`, and `Quot.sound` reported.
- The pinned Lean 4.19.0 compiler commit matches. All nine dependency checkout revisions match the manifest before and after the checks; their tracked-file cleanliness commands passed. The deliberately invalid smoke proof is the sole expected nonzero command.
- The bootstrap repair built `Cache.Main` before invoking the cache loader. The cache log explicitly records 6,641 downloaded dependency artifacts. This is a **fresh project source build using compiled dependencies**, not a complete Mathlib source rebuild.

The repository-root workflow at the verified commit invokes the complete runner with `--bootstrap --serial`, then the expanded physical endpoint contract. GitHub's job-step record reports success for that additional contract. Its standalone stdout is not part of the downloaded run-specific kernel receipt; this additional claim rests on the successful step record and workflow source. The ordinary seven contract checks are directly covered by the hashed command logs.

The receipt's explanatory note correctly limits `all_project_source_kernel_checked` to this project and explicitly disambiguates the legacy `all_imported_source_kernel_checked` flag. The existing verifier review correctly distinguishes proof-object replay from a dependency source rebuild. Earlier timestamped notes saying Linux CI was pending are superseded by this review. Run 40105321824 did **not** include the later endpoint-closure replay; that mechanism has separate successful local evidence and awaits the subsequent CI result.

No blocker was found. Remaining assumptions include the pinned Lean kernel/runtime, canonical compiler Init, dependency artifact/source correspondence, and authenticity of the supplied GitHub evidence. An independent kernel implementation or full dependency source rebuild is not established by these receipts.

Machine-readable recomputation results: `ci_evidence/40105321824/independent_review.json`.

## Final combined source-build and replay run

[GitHub Actions run 40106363370](https://github.com/AlecKriebel/Math/actions/runs/40106363370) succeeded at commit `8aae12015e4fb470ce5a0970f5b792dc3ca7ad8f`. I repeated the checks above against its fresh source receipt `20261024T151943Z-8d837c61`: all 104 current source hashes, 122 command-log hashes, 69 actual module builds, 78 examples in seven contracts, 826 unique public standard-axiom queries, and all nine dependency revision checks passed.

The replay receipt binds that exact successful source run and identical 104-input snapshot. I recomputed the hashes of its five command logs and both checker sources, confirmed successful exits with no panic/error diagnostics, and checked the actual positive and three negative kernel-control messages. The before/replayed inventories agree exactly: **33,644 declarations across 1,271 compiled modules**. The compiled-hash manifest covers exactly those 1,271 module paths. All three required equality/simulation endpoints appear in the inventory and successful replay log. The declaration-name set also equals the independent successful local replay over the September extraction.

The retained complete `lean_job.log` exposes the expanded physical contract's invocation/output and the successful wrapper unit-test method, whose source contains nine adversarial subtest scenarios. GitHub's corresponding step records all report success. This closes the additional-contract visibility limitation noted for the initial downloaded run.

The wrapper reports compiled-input hash stability before and after replay. **I checked the retained manifest coverage and receipt/log consistency; I did not rehash the remote Linux compiled files after the job**, because those files are not part of the selected downloaded evidence. The locally recomputed source/checker hashes and log hashes are separate, stronger direct comparisons of files actually available here.

The final run establishes a fresh project build followed by a complete transitive proof-object replay for the three selected endpoints using the same pinned Lean kernel. It does not establish a complete Mathlib source rebuild, an independent kernel implementation, or dependency source-to-cache correspondence. The current `ASSESSMENT.md` states these limits accurately. No unresolved blocker was found in the retained final evidence; the earlier pending-CI wording in timestamped historical notes is superseded.

Final machine-readable results: `ci_evidence/40106363370/independent_review.json`.
