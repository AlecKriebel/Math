# Supplement: repair raw evidence retention

The parent found a real evidence-retention defect in my independent harness. On the case-insensitive filesystem, the raw filename for the uppercase `CLAIMED_SOLVED` testcase overwrote the lowercase `claimed_solved` testcase. This is a harness defect, not a sweeper defect. I missed it during the initial review.

This supplement explicitly supersedes the original report's **71-controller-invocation** and **complete raw-retention** claims. The independent suite executed **72 controller invocations plus 12 direct parser controls = 84 controls** per mode. Each old run retained only **71 raw files**, losing the lowercase claimed-solved raw receipt. This occurred in all six archived independent runs, including pilots. The old passing control outcomes are retained as reported execution results, but their raw controller evidence is incomplete. The original seal and all 458 members remain unchanged byte-for-byte; the original report is preserved as historical evidence with this correction alongside it.

The new harness uses a four-digit invocation index followed by the testcase label for each raw filename, verifies uniqueness under case folding, and creates each raw file exclusively. It binds each invocation to the exact active named testcase and records that index, testcase, filename, source pin, interpreter mode, byte count, and SHA-256. Before accepting a run, it checks a one-to-one mapping among all actual controller invocations, their named testcases, and retained raw receipts. The lowercase and uppercase status records receive separate explicit checks.

| Actual mode | Passing controls | Controller invocations | Direct parser controls | Retained raw receipts |
| --- | ---: | ---: | ---: | ---: |
| Normal, optimize 0 | 84 | 72 | 12 | 72 |
| `-O`, optimize 1 | 84 | 72 | 12 | 72 |
| `-OO`, optimize 2 | 84 | 72 | 12 | 72 |

All 252 new control executions passed. All 216 new controller invocations have distinct retained raw receipts, including lowercase `claimed_solved` classified as eligible and uppercase `CLAIMED_SOLVED` classified as skipped. The exact same 84 testcases ran in the same order. The copied subject remains pinned to `fc8ef5d6493c0088d94441e3a1876b9dc99bbaef84a98320647b84d15d5d048e` before compilation in each actual process. The exact harness delta is preserved in HARNESS_REPAIR.patch; the prior harness copy is authenticated through the externally pinned original manifest. No subject source or inherited 49-control harness was changed.

The separate verify_supplement.py checks every new raw receipt and its case-sensitive binding independently of the suite, verifies both distinct status/action records, and reauthenticates all 458 original sealed members and the unchanged original directory inventory. VERIFICATION.json contains the complete outcomes and exact lower/upper raw filename bindings.

All new files reside in this separate supplementary namespace. No shared alias, hard link, symbolic link, live service call, Git mutation, excluded material, mathematical artifact, PR body, comment, or external communication was used. All raw service responses are explicitly synthetic. Production status scans remain with the parent; these tests do not establish live scope clearance.

Narrow evidence-retention repair completion: **100%** at the RESULT.json timestamp. No global research completion claim is made.

For reproduction, run independent_controls.py with an unused --output directory under actual normal, -O, and -OO Python processes. The verifier names the sealed actual0/1/2 directories explicitly; it creates VERIFICATION.json exclusively. Authenticate the supplementary MANIFEST.json using its independently transmitted SHA-256 before intake.
