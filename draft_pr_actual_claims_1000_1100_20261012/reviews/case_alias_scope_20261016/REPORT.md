# Case-alias output-contract audit: stable unpublished packages

The confirmed affected packages are **PR #1064, #1071 and #1085**, each with a **P3 support-interface finding**. Their actual writers accept a fresh output below an uppercase alias of the kit directory while rejecting the equivalent canonical-spelling location. Mathematical acceptance is unchanged. No existing-input overwrite, hostile concurrent-filesystem flaw, or completed correction is asserted.

## Scope and evidence

Only stable unpublished #1033, #1034, #1037, #1041, #1047, #1052, #1064, #1071 and terminal-complete #1085 were inspected. Active #1080 administration, #1094 repair, #1097 review and #1098 preparation remain pending and were not inspected. The 83 excluded PRs, immutable published #1001/#1024/#1025/#1031, other shards and PR1032's priority question were outside this bounded task.

CANONICAL_INPUT_PINS.json hash-pins 2,244 files across these nine package trees, canonical ZIP/tar archives, paper PDFs, READMEs, operative code and existing root seals/integrity records. The external #1033 builder was also pinned. Its SHA-256 is ae229eeadf6537a88758d7ff974a18428c271a40caf77bfd8f52398e0bb041d7. No complete folder backup was made.

audit.py extracted one current support ZIP at a time into audit-owned scratch/clean, checked member safety, and invoked the actual archive writer through its canonical script pathname. Each of the four independent extractions (#1052/#1064/#1071/#1085) proved clean and CLEAN had the same device/inode and samefile=True, while Path.resolve() retained different spellings. TEST_RESULTS.json records those identities, exact paths and outcomes. All 16 actual command arguments, complete stdout/stderr and return codes are preserved at their original command_000.json through command_015.json names.

Each case-alias run used a genuinely absent leaf and existing uppercase-parent alias; a matched canonical-spelling control used another absent leaf at the same depth. Both ordinary Python and optimized -O were used. All six bypass ZIPs were byte-identical to the reviewed current canonical archives. All original extracted files remained unchanged. Created outputs were removed before the next case, and each extraction was removed after its package. CANONICAL_UNCHANGED.json proves all 2,244 canonical records were equal before and after at 2026-10-16T04:06:09.798077Z. The terminal seal supplies another final rehash.

No writer was invoked against any canonical-tree alias. No Git, publication service, compiler, external communication or other-worker action occurred. Mathematical checks, paper recompilation and visual review are not claimed by this support audit.

## Findings

### CASE-1064 — P3: physical case alias bypasses the internal output whitelist

preprint_v1_0/build_archive.py:17 permits physically internal outputs only at support.zip or under tmp/. It tests this using lexical out.is_relative_to(root). Lines 12–15 separately protect existing input leaves using resolved equality and samefile.

Both clean/direct_*.zip controls were rejected with “inside package output must be support.zip or under tmp/”. Both uppercase CLEAN/case_alias_*.zip paths succeeded, physically creating clean/case_alias_*.zip outside those permitted internal locations. This is **not an outside-only promise**: the kit intentionally supports support.zip and tmp/ internally. The failure is the narrower mismatch in its explicit code-enforced location policy. README.md:11–21 describes tmp outputs and protected-file guards. Existing-input samefile protection remains present; no existing-file overwrite was tested or observed.

Tested canonical support.zip: 612,938 bytes, SHA-256 aeb9344ff84b46412d4532dc463cad4b151edba363172620978129c2964b2dbc. Both produced ZIPs matched exactly. Since the verifier rejects unmanifested files outside tmp/, this is also a meaningful package-location boundary, but a post-contamination verifier was not separately run in this bounded audit.

### CASE-1071 — P3: outside-all-descendants rule misses the physical directory alias

NEWpreprint_v1_0/README.md:11 requires new outputs outside every descendant of the frozen extracted package, with an existing nonsymlink parent. scripts/package_paths.py:29–39 supplies the shared fresh_output policy. Line 38 uses only lexical containment before/after Path.resolve().

Both actual archive runs accepted uppercase CLEAN/case_alias_*.zip and created a fresh archive physically inside clean. Matched canonical paths were rejected with “Output must be outside all frozen package descendants.” The parent existed; no symlink or race was involved.

Tested canonical PR1071_preprint_v1_0_support.zip: 1,440,215 bytes, SHA-256 88578e338672ef426c8dd65e1b0020997fdd422487811d336d3953b8dff9e037. Both produced ZIPs matched exactly. Existing leaves are separately rejected at package_paths.py:32. The demonstrated defect concerns fresh output location. Archive, checker and PDF entry points call the same guard; only the archive writer was executed here. No checker/PDF output or compiler run is claimed.

### CASE-1085 — P3: outside-canonical-kit rule misses the physical directory alias

preprint_v1_0/README.md says the builder requires an output outside the canonical kit and guards run before writes, directory creation or compiler calls. kit_common.py:63–78 provides shared safe_output. Lines 71–73 compare target != ROOT and lexical parent membership after resolve(). Lines 76–77 separately test existing protected hardlinks using samefile.

Both actual archive runs accepted uppercase CLEAN/case_alias_*.zip and physically created a new ZIP inside clean. Matched canonical paths were rejected with “output must be outside canonical kit directory”. This breaks the documented outside-only static policy. All old input bytes remained exact.

Tested terminal canonical pr1085_support_v1_0.zip: 495,659 bytes, SHA-256 77a2b789e16c868e8c73b6c55a726957d63ab9f50441c9b4e20828ddabbe5533. Both produced ZIPs matched exactly. Archive/PDF/checker/verifier output callers share the guard; only archive-writing behavior was actually reproduced.

## Other packages: no finding for this bounded issue

| PR | Current interface and checkable source | Conclusion limited to this issue |
|---|---|---|
| 1033 | Audit-root build_package.py:7–8 fixes publication root/archive and generates in-kit manifest and wrapper. No caller-selected output argument or outside-only contract. | Intended fixed in-kit outputs; no case-alias contract violation established. |
| 1034 | publication/build_package.py:2–6 expressly keeps paths/outputs in its audit directory; generated targets are fixed. | No outside-only contract to bypass. |
| 1037 | preprint/build_supportkit.py:5–7 fixes root/archive; README instructs rebuilding from extracted root. | Intended in-kit regeneration. |
| 1041 | preprint_v1_0/build_archive.py:7–10 fixes archive/receipt targets; README directs disposable replay. | Intended in-kit regeneration, no selected outside-only contract. |
| 1047 | scripts/build_supportkit.py:9–10 fixes root/archive. The checker takes an existing chosen output directory; README demonstrates in-kit verification_output. | No outside-only contract. No universal input-alias protection is inferred. |
| 1052 | build_support.py:18–21 explicitly requires output below ROOT; README demonstrates _runs/. | Actual uppercase aliases rejected before output in both modes; intended canonical in-kit controls succeeded and matched the canonical ZIP. |

For #1033/#1034/#1037/#1041/#1047 the current code and README were inspected, but no writer test was needed or run: their intended in-kit writes do not contradict an outside-only rule. This is not certification of every writer, historical script or unrelated filesystem property.

## Follow-up and custody

Root should assess these newly confirmed support findings before immutable publication, apply bounded repairs where appropriate, and obtain the required new complete whole-package reviews. A physical directory-ancestry check must include the nearest existing ancestor of a new output path; merely lowercasing strings is not portable identity checking. Preserve #1064's documented permitted support.zip/tmp destinations or explicitly review a changed policy. Preserve existing direct/symlink/hardlink guards and genuinely external output behavior. Regression controls should cover actual samefile case aliases, fresh nested directories and normal/optimized execution.

This audit does not relabel old frozen zero-finding verdicts or change canonical readiness records. These are new support findings on the identified current bytes, not completed fixes. Mathematical truth, source priority and ordered publication remain separately gated.

Disk exhaustion temporarily prevented new-file creation. An attempted own-receipt inode workaround was fully reversed: all sixteen original receipt names and exact original bytes were restored and rehashed against the transparent raw ledger in RESEARCH_LOG.md before genuine final artifacts were written. No temporary misleadingly named receipt is treated as a final report, pins or seal. The research log preserves that custody sequence.

Completion: 100% for this bounded inventory/reproduction task. The overall parent goal remains incomplete.
