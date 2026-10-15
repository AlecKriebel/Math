# Independent static review of PR880 package code

Authored by the independent Codex static reviewer, 15 October 2026 UTC. This is a new full-body source review, not an adoption of packaged audit verdicts. The initially supplied source map was used only for inventory. No candidate Python module or inherited tool was imported or executed during this review. All review writes were confined to the assigned private static-review directory; the candidate was unchanged.

## Exact claim and result

The claim checked was: **in the exact pinned portable package, determine every executable Python body, its direct and inherited effects, its reachable execution policy, and whether unexpected network/outreach, source mutation, private-content redistribution, or overclaimed verification is present.** Static success means complete code-body coverage with checkable byte identities and an explicit effect/scope account. It does not mean the analytic theorem, novelty, historical provenance, or historical test receipts have been independently certified by execution.

**Result:** all 19 unique Python bodies were read in full, covering 23 physical Python paths, 4,015 unique source lines and 5,060 physical source lines. All 192 lines of `note.tex` were also inspected. No network/outreach operation, opaque payload execution, hidden external process, or unannounced source/corpus write was found in the current verification chain. No static code blocker to that chain was identified. The ancillary scripts have consequential direct-run/import behaviors and portability limits listed below; their inclusion is not evidence that the current full replay executes them.

The package location is `draft_pr_claimed_solved_800_900_20261012/audits/pr880_9700026/replay/portable_r1_polished`, relative to the research workspace. The external trust anchor supplied to this review is:

```
package_index.json
bytes: 28008
SHA-256: 7af74074708d9ee7b462be7d74546ef1f090a3262223d538082e872288e3df3d
```

A separate reviewer-authored byte-inventory check confirmed that digest, all 160 indexed payload rows, and the exact 161-file tree including the index: no missing/extra file, byte-count/hash mismatch, or nonregular entry was found. There are no executable-mode files or additional non-Python shebang files. The two extensionless files are ordinary `.gitignore` text. The archive inspection recursively identified six Python occurrences, including the nested author ZIP, and every one was byte-identical to a fully read flat Python body. There was no additional unique archive-only code. This is static identity checking, not execution of the candidate verifiers.

## What the current entry points actually execute

- `local_tools/pr880_assemble.py:163–225` reads an externally pinned explicit source/destination allowlist, validates it before materialization, copies authenticated data into a fresh/empty output, and emits an inventory. It neither imports supplied files nor executes them. Its result is correctly named `ASSEMBLED_REQUIRES_INDEPENDENT_VERIFICATION` at line 226. The `subprocess` import is used for the exception type only.
- `local_tools/pr880_verify_current_publication.py:177–318` authenticates the externally pinned outer tree, nested portable inventory, copy relations, original source identity, and ZIP boundaries/metadata/data. Lines 321–348 materialize only authenticated in-memory bytes in a temporary directory and invoke that copy of `verify_package.py` using `-I -S -B` (plus `-O` when applicable). Lines 372–378 explicitly limit the result and report that the historical wrapper was not executed.
- `verify_package.py:161–182` authenticates the external inventory pin and closed tree; line 200 checks the startup copy equality. Its `--full` branch at 204–225 copies authenticated bytes and invokes only `check_originals.py` in a temporary working directory. Without `--full`, it performs inventory authentication and reports `full_replay=NOT_RUN` at 201–203.
- `check_originals.py:205–267` authenticates all forty original source files, nested archives, manifests and duplicates. Its replay at 340–381 creates temporary byte copies and runs the original author and audit checkers in normal and optimized modes, with and without self-tests. With separately supplied complete pinned inputs, it additionally runs `audit_a/verify_sources.py`. The eight source-free subprocess receipts, or ten with source replay, are finite arithmetic/provenance receipts. It does not execute `source/verify_publication.py` or any ancillary audit/diagnostic harness.
- `build_verification.py:168–195` authenticates the external index, external verifier digest and startup builder copy. Lines 205–218 execute the authenticated temporary verifier before writing the ZIP at 223–232. Its output parent directories can be created at line 203 before replay; its output archive is created only after successful validation. The builder creates a local ZIP and prints metadata; it contains no upload, Git, GitHub, Zenodo, or release action.

This graph is consistent with the code's explicit limitations: artifact authentication plus finite diagnostics, not an analytic proof or priority certificate. The names `--full` and `PASS` must retain that stated scope. The independent diagnostic and historical harness files are authenticated package contents, but the current replay does not claim or provide fresh execution of all of them.

## Findings and operational limits

### SC-01 — Ancillary direct invocation writes into and changes a sealed package

This is a direct-run caution, not an unexpected side effect in the current graph. These files overwrite a result or receipt next to themselves:

| File | Exact lines | Direct effect |
| --- | --- | --- |
| `geometric_barrier_audit_01/exact_geometric_stress.py` | 189–191 | Writes `EXACT_STRESS_RESULTS.json` and prints it. |
| `ode_wellposedness_audit_01/check_auxiliary.py` | 98–126 | Reads pinned source inputs, writes `AUXILIARY_RESULTS.json`, prints selected results. |
| `priority_direct_audit_01/check_priority.py` | 98–113 | Reads chronology, writes timestamped `CHECK_RESULTS.json`, prints counts and exits. |
| `artifact_integrity_audit_01/audit_harness.py` | 529–560 | Creates a temporary directory under its own directory and writes `RESULTS_SOURCE_FREE.json` or `RESULTS_WITH_PROVENANCE.json`. |
| `package_engineering_01/guard_probes.py` | 37–151, 158–159 | Builds/deletes synthetic fixtures, then writes `GUARD_RESULTS_*.json`. |
| `tooling_review_01/guard_review.py` | 90–92, 419–422 | Creates a fixed private run tree, writes `RECEIPTS_*.json`, removes its run tree. |
| `tooling_review_01/docstring_bridge.py` | 20–25, 60–69 | Creates a fixed private fixture, writes `DOCSTRING_BRIDGE.json`, removes fixture. |
| `tooling_review_01/reproduce_fixed_defects.py` | 18–22, 66–75 | Creates a fixed private fixture, writes `REGRESSION_REPRODUCTION.json`, removes fixture. |

Fresh timestamps and elapsed-time fields can change otherwise similar outputs. Running these directly in the sealed tree can therefore invalidate its exact inventory/hash seal. They should be reproduced in an authenticated disposable copy with resulting receipts kept separate from the immutable candidate. This reviewer did not run any of them.

### SC-02 — Four ancillary modules run work when imported

`ode_wellposedness_audit_01/check_auxiliary.py:34–126` and `priority_direct_audit_01/check_priority.py:25–113` perform their checks and result writes unconditionally at module scope. The latter also executes `SystemExit` at line 113. `tooling_review_01/docstring_bridge.py:15–69` and `tooling_review_01/reproduce_fixed_defects.py:13–75` are also unguarded: they load the shared guard and run synthetic assembly/replay workflows when imported. Treat these as executable scripts, not harmless libraries. No current verifier imports them.

The shared guard itself has a main guard (`guard_review.py:441–445`), so loading that file with a non-main name defines its helpers; its `freeze` method subsequently executes the top-level code of copied candidate tools using `runpy.run_path` at 124–130. Those five tool bodies were all inspected: their non-main top levels contain imports, definitions and constants, not hidden workflow calls.

### SC-03 — Historical harnesses are not standalone portable provenance entry points

`tooling_review_01/guard_review.py:28` fixes `WORKSPACE = BASE.parents[2]`, and its `provenance` method at 392–408 constructs original repository corpus/PDF locations. The sealed package is deeper in a replay hierarchy, so the ancestor calculation does not identify the original workspace there. The package also excludes the required primary PDF directory. `package_engineering_01/guard_probes.py:141–146` and `artifact_integrity_audit_01/audit_harness.py:411–417` likewise construct historical `private_sources` locations. `priority_direct_audit_01/check_priority.py:25–44` expects ledger-listed private primary files/metadata/text that are not included in this portable tree.

This limits direct reruns of these archived workflows. The current portable `check_originals.py` is the supported provenance route and instead accepts all required explicit locations (`392–405`) with fixed-byte verification (`270–305`). No public package result should represent the historical optional provenance branches as newly replayed merely because their code/old receipts are present.

### SC-04 — Ancillary success booleans do not always propagate as exit failures

In `tooling_review_01/guard_review.py:412–423`, a changed candidate can make the receipt's `success` false and return false. `run` ignores that return in its `finally` block at 425–438. If the probes complete and only the final unchanged check is false, the script can exit zero while printing `success:false`. The docstring bridge at 61–69 similarly prints a false success without explicitly choosing a nonzero exit status. This is a low-impact historical harness interface limitation: consumers must inspect the success JSON, not just the exit code. Neither harness is a child of the current replay.

### SC-05 — Intentional inherited execution in older audits is visible, not a new trust anchor

`artifact_integrity_audit_01/audit_harness.py:245–251` reads and executes a known original source body after comparing its file pin, in order to probe its helper behavior. Its main authentication precedes those calls at 528–535. Its positive runs at 390–408 deliberately invoke the historical wrapper, which in turn starts author/audit children. `package_engineering_01/guard_probes.py:27–29` directly uses `runpy.run_path` on candidate tools, and `guard_review.py:124–130` loads copied candidate tools. These harnesses do not implement a new independent pre-execution authentication root for themselves. They must themselves be externally authenticated and inspected before direct use.

The historical `source/verify_publication.py` is weaker than the current wrapper: it uses ordinary `json.loads` (`38`, `55`, `77`), inventory tests based on `rglob/is_file` (`45–48`), and child flags without `-S` (`72–75`). The author checker also lacks an explicit list type check for weights (`source/author/verify.py:48`), and the original audit's own manifest is optional (`source/audit_a/verify_audit.py:115–124`). These are preserved standalone limitations, not fixed-pin bypasses in the current graph: current strict parsing, closed-tree authentication, exact frozen-byte pins, and isolated temporary execution precede the original child checks.

### SC-06 — Static review is not a general-purpose sandbox or proof

Current code deliberately requires an externally supplied inventory/startup digest. A running program's self-hash/copy equality is not pre-execution trust, which the module docstrings explicitly acknowledge. Child commands use a trusted interpreter/standard library; `-I -S -B` controls import/startup policy but is not an operating-system security sandbox. `check_originals.py:362–366` uses hardlinks to authenticated source inputs, not file-system-enforced read-only copies; the inspected original source checker only reads them. Historical malformed-input probes explicitly detach hardlinks before writing new files (`artifact_integrity_audit_01/audit_harness.py:457–466`).

The current closed-tree/type/size/hash checks reject the static malformed cases visible in source. This review does not establish safety against malicious standard libraries, hostile concurrent filesystem replacement, abrupt process termination, or all possible future user-supplied specs/inputs. Cleanup is normal control-flow cleanup, not a guarantee after an uncatchable kill.

## Network, source mutation, and privacy account

All Python imports are from the standard library. No HTTP client, browser/API connector, mail/chat service, Git/GitHub command, upload, publication command, or network request was found. The one socket use is `tooling_review_01/guard_review.py:171–183`: an `AF_UNIX` socket bound to a disposable local pathname to test nonregular-file rejection. It never connects, listens, accepts, sends, or receives. TeX URLs/hyperlinks are rendered links, not source-fetch commands. The TeX body contains ordinary article/package/macro/document material and no shell escape, Lua, external file-content inclusion, or embedded executable payload. The installed TeX packages themselves are outside this source review.

The current assembler copies only explicitly pinned allowlist entries and rejects source/output collisions (`pr880_assemble.py:180–218`); it does not scan a workspace or automatically include private material. Current replay children are authenticated byte copies. No corpus/PDF source is written, chmodded or truncated by those children. Optional provenance reads the complete pinned inputs locally and returns sanitized names, sizes, hashes, exact-ID counts and canonical-pair identity. `source/audit_a/verify_sources.py:45–49` explicitly separates source interpretation from hash verification. `source_scope_audit_01/check_source_scope.py:97–105` marks the analytic theorem, semantic reading, and novelty as uncertified.

Historical harnesses may serialize local fixture paths, exceptions, or tool receipts. This is visible logging behavior and can expose local path metadata if their newly generated receipts are later redistributed; there is no code that transmits them. No raw corpus records or primary PDF contents are printed by the inspected provenance routines. This report and its coverage JSON contain only code identities, finite scope/effect descriptions, and package-relative paths; no private corpus/source content was copied into them. Distribution rights and content privacy of non-code packaged documents remain a separate whole-package review question.

## Coverage pins

Each body below was manually read through its final line. Duplicate flat paths and recursive archive occurrences are listed in `STATIC_CODE_COVERAGE.json`; every duplicate was independently hashed. `note.tex` has its own full-body review record there. No conclusion here depends on a packaged old verdict or receipt.

| Canonical file | Lines | Bytes | SHA-256 | Flat paths |
| --- | ---: | ---: | --- | ---: |
| `artifact_integrity_audit_01/audit_harness.py` | 564 | 33210 | `8ca300b214af02f9b34b615398c7ffc2c18847a104a25e22580860022bad0f9e` | 1 |
| `build_verification.py` | 242 | 10648 | `a1d76f65b2438236f2251c0f4dc850140fd1495a6e7ed418bfbf10fc86e23cca` | 2 |
| `check_originals.py` | 410 | 22093 | `e78f97d36210f29e466636861767124a338c9ad0fe48e050eeec2a5355c3771f` | 2 |
| `counterexample_scope_audit_01/independent_exact_check.py` | 168 | 8068 | `211a721cd64ba1e6b91b7e6dbbd14214c0eafb2bfd39997db4e4612812676d61` | 1 |
| `geometric_barrier_audit_01/exact_geometric_stress.py` | 195 | 8534 | `609ca8fd204e99ead5873e62053eb294b5c18fa409e9add07203dc9d1bfbde51` | 1 |
| `local_tools/pr880_assemble.py` | 230 | 10086 | `939fea38779e6df5e81f7930a6a39153a082bcea046ad2879dabc4e0b8115055` | 1 |
| `local_tools/pr880_verify_current_publication.py` | 383 | 19010 | `b8279f4945b2f05b3755bfec20ae6c78dbbb00d053abdb04f87d8068f2ff62a7` | 1 |
| `ode_wellposedness_audit_01/check_auxiliary.py` | 126 | 5372 | `a5e1a35caad1d75be7407696197ce9637213d96f235cfad4a17662cdc62ace9f` | 1 |
| `package_engineering_01/guard_probes.py` | 160 | 17632 | `a014d4c098877545869cd864ad0778c3a4fd752d86e945b5d654496711bf4bbc` | 1 |
| `priority_direct_audit_01/check_priority.py` | 113 | 5189 | `34c45572e5061675f885edffdb58d959341f2871b92746dcbf61d8abae048cf2` | 1 |
| `source/audit_a/verify_audit.py` | 150 | 8554 | `47d9f4597b60427bafeafa289309b10f609dbc1ddde4160a4d74bffe13f9863e` | 1 |
| `source/audit_a/verify_sources.py` | 53 | 3035 | `91d0840661da53dce61f7270f90eeb3e49242dfb0c5630e14700ed55c99ea536` | 1 |
| `source/author/verify.py` | 163 | 7542 | `ea32cb10ec774debeffd8ccfe2541fc833bb958f93650a56d8c16448b15cdf07` | 2 |
| `source/verify_publication.py` | 127 | 6640 | `9ae285d9a0f63b3d6556277599f66173246149e0ce296bc45004b612baea5d24` | 1 |
| `source_scope_audit_01/check_source_scope.py` | 112 | 5488 | `06247d7c318ce577a08029cfc8a8bf32a22a2bd7f131447c1cbec894f9c3bce1` | 1 |
| `tooling_review_01/docstring_bridge.py` | 69 | 4088 | `16660c30d3b9c9507e5711bf1c6594c9273c1ada072dfbe1411d90fbbe35b2a7` | 1 |
| `tooling_review_01/guard_review.py` | 445 | 30951 | `2e6f922d97d02f118dfab0b0019d08611f46de7e1aabc40b467813b55f20ac43` | 1 |
| `tooling_review_01/reproduce_fixed_defects.py` | 75 | 4892 | `fb0150d07e6a4865123e3249d55e242afe3292303295e7803f90b7db2e41df0e` | 1 |
| `verify_package.py` | 230 | 9852 | `73faad1cfa4ab2e9c7e6cfa214e58fadb361ccf4de3199ed87e96883ae6a351a` | 2 |

The associated JSON also records per-file startup behavior, exact reviewed line range `[1, final_line]`, imports, effects and analytic/verification scope. It records the recursive ZIP duplicates, exact index/member pin check, and explicit non-execution status.

## Remaining gap and completion

The assigned static-code review is complete: **100% of its finite inspection target**, with all unique bodies and all code duplicates accounted for. The strongest verified result is complete static effect/scope coverage of this exact externally pinned package, with no unexpected external-communication or source-mutation mechanism identified in the current execution chain. The exact remaining gap is dynamic behavior/reproducibility and semantic mathematical/source/priority validity; this review does not supply those forms of evidence. The ancillary cautions above must remain distinct from claims about the current isolated replay path.
