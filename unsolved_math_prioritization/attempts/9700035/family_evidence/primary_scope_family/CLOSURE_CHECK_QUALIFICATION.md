# Initial closure-check exclusion order

The initial independently authored preclosure check actually exited1 at
2026-10-02T13:32:31.767939+00:00. Its full source, arguments, empty stdout and
793-byte stderr are preserved in `closure_check_actual_capture`. It inspected
an intentional symlink countercontrol under the old PR40 family's explicitly
excluded root `ignored_tmp` before applying that family's exclusion.

The correction applies only the declared exact root exclusion before inspecting
its descendants. All included first-party paths still reject symlinks, the
self-manifest exclusion remains root-only, and every declared included old
member must match its pinned bytes and exact membership. No old file, source
snapshot, mathematical proof, or native state was modified. The corrected
actual check is captured separately in `closure_check_actual_capture_v2`.

This was a bookkeeping error in our own closure checker, not a defect in the
submitted result. It adds no substantive target or native audit-attempt record.
