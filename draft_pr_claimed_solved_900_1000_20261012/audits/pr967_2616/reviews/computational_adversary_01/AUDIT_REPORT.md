# Independent computational, execution and packaging adversary

Target: PR967 / problem2616 / Kourovka21.107, exact head `b356dec5cb01e5f536b9cfeece56ad08844c03cb`. Candidate report SHA-256 `ddde58f03f320c881b78e59b60a40f315e1811c7c88aaa25ce620c427afbb6ca`.

**Assessment: no required mathematical or bounded-replay correction found. One optional error-format robustness issue was reproduced. Historical host/original-directory claims remain NOT_REPRODUCED, and fresh primary-source/corpus checks remain NOT_RUN.** This is this family's independently checkable audit, not final project acceptance, publication, peer review, novelty or current-open-status certification.

## Exact intake and preservation

The externally supplied original-file-record digest was checked before candidate execution. All26 original files,147731 bytes, matched exact Git blob bytes, Git modes100644 and disk modes0644 at the nominated head. The archive's14 headers and12 file bodies were safely read without extraction; every body matched the corresponding author file, and its modes were0555 for directories and0444 for files. Every text source, proof, receipt and metadata file was manually read in full before executing any candidate source. SOURCE_REVIEW.md records the complete26-file inspection.

The final read-only reauthentication at2026-10-16T20:35:24.100871+00:00 confirmed all26 original bytes, hashes and modes unchanged. receipts/original_before.json and receipts/original_after.json supply the individual records. No original was executed in place, chmodded or opened for writing. Candidate execution used owned scratch copies with TMPDIR,TMP,TEMP inside this effort's directory. No corpus, unrelated problem, private source record, source cache, Git/service state or remote state was mutated. No external communication occurred.

## Mathematical assessment independent of computation

MATHEMATICAL_RECONSTRUCTION.md gives the full independent argument, including the group and topology axioms, ZFC free-ultrafilter existence, dense support-size coloring and universal obstruction. The central finite-fiber lemma is proved abstractly rather than inferred from finite examples. Images of pairwise disjoint finite blocks under a finite-fiber map are point-finite, so a finite forbidden union excludes only finitely many indices and ordinary recursion gives an infinite pairwise disjoint image subsequence. The maximum-support map has exactly2^k elements in its k-th fiber. A parity split of the selected image unions and one ultrafilter complement yield a single open subgroup missing infinitely many entire original blocks.

This checks the relevant boundary cases: infinitely empty blocks, removal through the sole possible identity-containing block, repeated maxima in different blocks, non-covering blocks, growing/unbounded block sizes, finite images, nonuniform fiber bounds, strict increase of original indices, and one fixed neighborhood depending on the sequence. It uses neither countable completeness nor a selective/Ramsey/rapid/P-point property. Freeness, the ultrafilter decision property and ZFC existence are proved, not modeled numerically. The finite principal-filter boundary explicitly fails Hausdorff separation and sufficiently high color density, so it supplies no evidence for the infinite construction.

The strongest verified mathematical result is the specified complete ZFC construction and quantified obstruction, assessed by direct proof. No mathematical gap was found by this family. Formal mechanization and independently researched source scope/lineage/priority are outside the demonstrated result of this family. It does not use another current family's conclusions as evidence.

## Actual current-host reproduction

Actual host: macOS26.6.2 arm64, Python3.14.6, genuine UID501/EUID501. The original historical receipts describe Python3.12.14 and UID1000/EUID1000. That historical runtime/account was unavailable and was **NOT_REPRODUCED**. The current immutable snapshot's original-directory write-denial history was also **NOT_REPRODUCED**; original-directory write probes were **NOT_RUN** under the no-original-mutation rule. Real denial on newly created, owned read-only copies was observed and is reported as such.

receipts/actual_reproduction.json preserves exact commands, launch timestamps, return codes and raw stdout/stderr for six genuine runs. BOOTSTRAP normal,-O,-OO all returned zero with optimization0,1,2 and UID/EUID501. The authenticated mutation harness also returned zero in its three actual modes, each with53 negative controls plus relocation/read-only/hostile-import replay. The author and historical independent checkers were actually run by the wrapper, with their own normal/O/OO subprocesses. They were not replaced by stubs or simulated receipts. Their output was checked by the wrapper against historical records after the documented runtime/account substitutions.

The author case counts independently reconstruct as16^3+13+256*6*(1+2+3+4+5)+4^7=43533. The old independent finite counts sum to4096+65536+16+57344+65536=192528. These are counts of heterogeneous finite test cases, not numbers of proven infinite instances.

The wrapper genuinely denied five write attempts on read-only replay paths. Its mutation runner genuinely denied three more relocation/hostile-directory probes. The fresh independent controls additionally created and appended bytes while writable, read those bytes back, changed only their owned modes, and then observed PermissionError(errno13) on append/create attempts, with unchanged/absent readbacks. A deliberately active owned hostile module successfully wrote its sentinel without isolation; the corresponding isolated checker/bootstrap invocations left the sentinel absent. Thus the fresh hostile-module negative has an actual positive control.

The successful current replay does not retroactively convert historical host or immutable-original write claims into reproduced observations. No whole-machine write monitor or compromised-runtime/concurrent-filesystem security proof is claimed.

## New checks separated from checker reuse

sources/new_finite_checks.py never imports or executes an original checker. It passed actual normal,-O,-OO runs with identical mathematical results:

| New mechanism | Executed finite coverage |
| --- | --- |
| Fixed-coordinate characterization of a coset |4096 membership cases. |
| Compatible partial coordinate assignments |65536 mixed coset-pair intersection and exact sum cases. |
| Exact whole-coset size spectra |65536 eight-coordinate support/subgroup pairs; all miss color4, explicitly illustrating the finite-density boundary. |
| Modular least admissible color size |1290 size/color pairs, including zero extension. |
| Arbitrary finite-fiber maps, unrelated to maxima representation |81 maps,20736 map/block-assignment pairs. |
| Growing blocks and repeated maxima |400 blocks of sizes1 through400,80200 distinct nonidentity supports,17 selected indices. |
| Principal-filter boundary |Nonseparation and absent high colors detected; not a free-ultrafilter simulation. |

sources/execution_adversary.py launched409 real local child processes, retaining every raw output in receipts/new_execution_commands.jsonl. In each actual optimization mode it accepted the pinned fixture, accepted the valid65536-byte padded boundary, rejected133 malformed inputs including the65537-byte case, and successfully ran the separately authenticated author bootstrap. Cases include both boolean values for every integer, finite floats, negatives, changed values, strings/null/containers, every missing field, every duplicate field including Unicode-escaped equivalent keys, nonfinite constants, float overflow, a10000-digit integer, invalid UTF-8, trailing input, invalid roots and deep nesting. No malformed input was accepted.

sources/archive_and_binding_adversary.py exercised31 authenticated helper/integrity observations in each actual optimization mode. It attacked directory inventory, traversal, absolute/dot/double-separator/backslash paths, symlink/hardlink/FIFO/device members, duplicate directories/files, local/global PAX, changed bodies, nested duplicate JSON, nonfinite and overflow numbers, immutable evidence versus self-consistent manifest repinning, disk modes and regular hardlink aliases. All expected observations occurred; there was no extraction. sources/outer_boundary_processes.py independently launched22 actual CLI negatives, including self-repinned report and wrapper-document changes, changed bootstrap, oversized wrapper/public member, linked root and missing isolation/site flags. All returned nonzero with raw outputs retained.

receipts/receipt_validation.json and its launcher verify the before/after inventory, arithmetic counts, raw command counts, mode agreement, preserved failures and boundaries. This consistency check passed; it does not replace independent verification of the authored audit.

## Individual findings and limits

| ID | Classification | Checkable evidence and implication |
| --- | --- | --- |
| R0 | No required correction found | The independent written reconstruction closes the infinite argument; actual current-host authenticated replay passes all advertised modes and malformed inputs remain rejected. This family found no failed theorem step or accepted malformed fixture. |
| O1 | Optional robustness improvement | Input `[` repeated2000 times, then`0`, then`]` repeated2000 times is4001 bytes and produces a nonzero uncaught RecursionError/traceback in the author checker in normal,-O,-OO. Three raw stderr records are preserved under labels ending`:deep_array`. Catching RecursionError or bounding parser nesting could give the same structured JSON error format as ordinary invalid fixtures. The input is rejected, so this is not theorem evidence or an acceptance bypass. |
| B1 | Historical reproduction limit | Historical Python3.12.14/UID1000 and original frozen-directory denial are NOT_REPRODUCED. Current Python3.14.6/UID501 read-only scratch denial is actually observed. No surrogate is counted as the old environment. |
| B2 | Bounded archive/helper contract | The low-level archive reader accepts changed permission metadata and trailing bytes; inventory allows regular hardlink aliases and does not bind disk modes. Full integrity rejects changed archive bytes through fixed accepted-evidence hashes even after a manifest rehash. These are helper limits, not external-bootstrap-pin bypasses. A separately authenticated bootstrap remains necessary. |
| B3 | Author bootstrap read bound | The standalone author bootstrap reads a package file fully before comparing its length/hash. Its declared size limit is not an actual pre-read bound. The fresh1000001-byte member was rejected. The outer wrapper prebounds its own file reads and pins the accepted author snapshot; no memory-exhaustion or arbitrary-size safety claim is made for the standalone helper. |
| B4 | Source and publication boundary | Primary bodies/corpus were not retrieved or rehashed. Fresh source/corpus bindings remain NOT_RUN, and old source/status/lineage metadata is historical. No priority, firstness, current-open or publication certificate is issued. |
| B5 | Chronology correction preserved | One progress message inaccurately labeled itself20:31UTC without sampling a clock. The log corrects it at actual2026-10-16T20:28:34.059629+00:00 and records the parent's20:28:13UTC observation. Receipt/log timestamps were generated by actual clock calls and were not backdated. |

## Approach ledger and closure

| Approach | Mechanism | Status/evidence | Exact remaining gap |
| --- | --- | --- | --- |
| Infinite coordinate/fiber reconstruction | Coordinate signatures, unbounded size classes, finite-fiber thinning, ultrafilter decision | Complete direct deduction in MATHEMATICAL_RECONSTRUCTION.md | No mathematical gap found; not formally mechanized. |
| New finite falsification | Exact size spectra, arbitrary finite-fiber maps, repeated maxima/growing blocks | New independent source and three-mode raw receipts | Finite checks cannot validate existence/freeness or infinite quantifiers. |
| Existing checker replay | Externally pinned bootstrap/wrapper/manifest and actual local children | Six current-host runs, all returning0 | Historical runtime/account and original-directory denial NOT_REPRODUCED. |
| New software/packaging adversary | Active hostile-import/write controls,133 malformed inputs per mode,31 helper observations per mode,22 outer CLI negatives | Actual commands/raw receipts; optional O1 retained | No concurrent-race, compromised-host or resource-exhaustion security proof. |
| Source/corpus/priority audit | Historical metadata review only | NOT_RUN for fresh bodies/corpus; no novelty inference | Requires separate primary-scope and priority work. |

Final completion estimate:100% of this assigned computational-adversary review and checkable handoff, not100% of the parent research/publication program. The final manifest intentionally includes only authored audit reasoning/source and receipts. It excludes private/,fixtures/,tmp/, all copied candidate fixtures, caches, downloaded primary bodies/extracts/images (none fetched), private source records and corpus contents. The manifest itself is self-excluded and its SHA-256 is delivered externally for authentication before substantive intake.
