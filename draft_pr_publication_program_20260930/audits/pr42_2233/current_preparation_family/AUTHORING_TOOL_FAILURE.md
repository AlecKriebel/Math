# Retained authoring-tool limitation

During read-only preparation, a size-inventory command used `wc -c` with both
files and directories. The tool returned exit1 because three matched operands
were directories: PR41 `HISTORICAL_RECONSTRUCTION_ACTUAL_CAPTURE`, PR41
`STATIC_ACTUAL_CAPTURE`, and PR42 `source_snapshot_v2/review`. The complete tool
response remains in the task transcript (chunk5d241a). The command performed
no writes and executed no proposed candidate/helper. No scientific conclusion
depends on this size listing.

The tool did not expose a child PID or UTC clock; these are not invented here.
This note is an attributed transcript record, not a manufactured runtime
capture. Later authoring-only inspection has a separate genuine PID98633,
source/argv/cwd/UTC/full stdout/stderr/exit0 capture in AUTHORING_ACTUAL_CAPTURE.
Initial combined reads whose tool output was truncated were treated as such;
the proposed builder was subsequently read completely in one untruncated
source response and its later changed segment was read separately.
