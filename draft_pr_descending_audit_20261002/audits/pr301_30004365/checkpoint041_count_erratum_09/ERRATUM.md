# PR301 held-file custody count erratum

This additive correction supersedes the erroneous held-file quantities in review06 REPORT/DERIVATIONS, review08 REPORT/READ_SCOPE and the completion log's interpretation of “one owned control in the baseline.” Closed historical files and failures remain unchanged. The accepted mathematics, adverse priority outcome and actual checkpoint publication are unaffected.

The exact baseline contains **41,253 distinct paths totaling 1,273,600,002 bytes**. It contains neither the literal live program SHARED_GIT_WINDOW_STATUS.json nor any of the 97 checkpoint041 paths. The live control was verified separately and must not be subtracted from this baseline.

| Actual check | Files checked | Bytes checked | Baseline exclusions |
|---|---:|---:|---|
| Reviewer06 native binding check, PID29661/exit0 | 41,234 | 1,273,589,714 | 19 historical mock fixture files, 10,288 bytes |
| Reviewer08 native custody check, PID69774/exit0 | 41,253 | 1,273,600,002 | None |
| Actual041 ROOT readback, PID84900 | 41,253 | 1,273,600,002 | None |

Reviewer06 used a suffix test for every path ending in /SHARED_GIT_WINDOW_STATUS.json. That skipped 19 historical mock control fixtures, not the absent live control. Its actual result JSON and complete native stdout correctly record 41,234 and 1,273,589,714; the prose incorrectly said 41,252. No assertion is made that reviewer06 checked those omitted fixtures in that execution.

Reviewer08 used literal live-control and owned-path exclusions, both empty on this baseline. Its actual result and native stdout correctly record all 41,253, the full byte total and excluded_count=0. I incorrectly hardcoded inherited quantities of 41,252 and 1,273,589,714 into its REPORT and READ_SCOPE instead of using that actual result. Those documentation values are superseded here. The earlier ROOT completion-log qualifier likewise incorrectly imagined one live-control baseline entry.

The genuine ROOT metadata and checkpoint predicates compare the literal live-control path, not every matching suffix. Their authenticated actual acceptances therefore include all 19 fixtures. The complete actual041 acceptance (SHA2567e4c4cbf0544f533ad3781e832a5d5ff050a33e3b420f6fe60f9fecbe5f09c70) correctly reports 41,253, binds the executed validator source41d07aef... and authenticates the successful checkpoint PID82834/exit0, 844 native captures and commit6144d964777214c6963a915288c18fcf97b42026. Its coverage requires no corrective mutation or renewed full audit.

The new reader independently derived the baseline sets and authenticated the original source/result/full native output relationships. Its v02 native execution passed 60 predicates. The first reader failed on a legacy envelope schema assumption about start_UTC; that exit1, its source and full stderr are preserved. V02 checks the actual separate started-record PID/time interval. No prior failure is relabeled success. No held-body reread, Git/PR/service mutation, new scientific review or execution authority is part of this erratum.
