# Actual preparation failures

The source writer failed with `OSError: [Errno 28] No space left on device` while creating `build_scope.py` (tool result `bacfc9`, exit 1). The subsequent attempted launch returned exit 2 because that file was absent (tool result `667758`). No completed builder, process receipt, SCOPE, READY, stage, commit, or push resulted from those attempts. No PID or timestamp was recorded by those failed tool outputs, and none is reconstructed here.

After the failure, read-only storage observation returned 128,084 KiB available. This is a later observation, not a reservation or a claim about storage at the failure. The five already written source files remained present. No evidence was deleted by this preparer.

Actual collector PID49974 ran 15:49:31.284835–15:49:31.584857 UTC, exit1. It rejected the archived `captures/tree_unsolved_math_prioritization/` path because its initial exclusion used a substring rather than a native path prefix. Its complete stderr, empty stdout and exact prelaunch sources remain in `source_scope_collection_first_actual_capture`. The repaired collector PID50320 ran 15:49:58.519385–15:49:58.776778 UTC, exit0. Its capture remains separate. Neither collector called Git or any ROOT-only helper.
