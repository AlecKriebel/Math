# Format review 01 research log

2026-10-16T04:02:59.323663+00:00 — 20% complete. Independent initial assessment frozen after full reads of portable.py, engineering_controls.py, parent diffs and INTEGRATION; both assigned hashes match. No other format verdict read; no archival execution. Attack families: strict typed/closed inventory; preexecution authentication and actual measured flags/schedule; complete-source pins before extraction with no archival access; current metadata/copy equality; closed raw ZIP/DEFLATE and same-runtime rebuild; CLI and path controls. Candidate not yet supplied.

2026-10-16T04:06:38.268460+00:00 — 45% complete. V1 helper suite completed 56 cases. Two actual path-containment failures reproduced through disclosed build helper sentinel (no archival code); root dotdot and symlink output parent placed output physically inside input. Typed rows, aliases, strict JSON, tree regularity, bounded reads, and raw DEFLATE suffix/concatenation controls behaved as expected.

2026-10-16T04:06:38.268460+00:00 — 50% complete. Source-only probe first failed its assigned startup SHA256 gate after tool changed; no source read or archival execution occurred. Parent supplied reviewed delta04 and V2 pin 09e4932f66c15916891245a1fb3d6a7052cb5619710d94e0e2305fb7a7612aa6. The canonical output-parent/root fix was independently read.

2026-10-16T04:06:38.268460+00:00 — 60% complete. V2 helper suite completed 56 cases; both original attacks rejected before replay sentinel and created no output. Real complete-corpus source-only dispatcher passed; all three streaming pins completed before first parse read, exact 5104-byte pair and 145-byte statement matched, zero archival file opens and zero subprocesses observed. Four-primary directory positive not run because BGT filename differs in available source directory; no bodies copied. Original verify_packet.py and all five checker bodies fully read before any future replay. Candidate current wrapper still not supplied; no whole-current default PASS claimed.

2026-10-16T04:08:13.304728+00:00 — 60% complete. Reviewer runner creation via apply_patch failed before execution; no candidate run attempted. Existing receipts remain available. Disk reports 101MiB but writes can still fail. No cleanup outside review directory.

2026-10-16T04:08:45.645881+00:00 — 65% complete. In-memory four-primary actual whole-body stream_pin checks all passed, including BGT under its existing BGT_2106.12266_root.pdf name (967612 bytes, 9d78c8dd86aaa62dbaa7bfcaf40195c901c3cc9dee025bffd4a6e29af64339ba). No body copied. Exact primary_only directory contract correctly rejects the missing required BGT filename, so that directory positive remains NOT_RUN. New 700-byte incident file also failed with explicit ENOSPC; tool transcript retains complete pin output.

2026-10-16T04:17:04.028172+00:00 — 65% complete; initial tooling handoff finalized.

## Initial tooling/metadata review handoff

The initial independent review is finished; estimated current publication-tooling validation completeness is 65%. The verdict for frozen portable V2 is REVISE, and actual current-wrapper integration is NOT RUN. This is neither of the two required new final whole-package reviews and gives no mathematical, novelty, human-review or publication approval. Original proof-search effort remains immutable 5/5.

The independently read initial code comprised all 668 portable.py lines, all 197 engineering_controls.py lines, four initial parent diffs and INTEGRATION. Both initial assigned hashes matched. The original verify_packet.py and all five archival checker bodies were fully read before any prospective replay. No archival code has been executed by this reviewer. The independent initial approach assessment was frozen before consulting historical artifact SOURCE_CONTRACT/FORMAT_CONTROLS. No other format reviewer verdict was read. No Git command, index/remote mutation, external contact, third-party body copy or foreign cleanup occurred.

Frozen V1 portable SHA256: a0ff2bc8e6cfb13b2b216be27ee06df7887427f98c1a1e1c7fd3aed5a2be5570.
Initial engineering_controls.py SHA256: 169405275b069a76c8c46f3dd818a7f62a0e462a1b9ac58093d7654f07d39f0f.
Assigned frozen V2 portable SHA256: 09e4932f66c15916891245a1fb3d6a7052cb5619710d94e0e2305fb7a7612aa6.
Delta04 and its engineering-control delta were independently read; no execution of the engineering-controls program is claimed here.

### Unresolved V2 defect: physical directory aliases evade build containment

The V2 build_output guard resolves the output parent and selected input root, then checks path-string ancestry. On the actual case-insensitive APFS filesystem, both the uppercase spelling FORMAT_REVIEW_01 and the /System/Volumes/Data-prefixed spelling of this review directory exist and have exactly the same device/inode as the input root, while Path.resolve() returns unequal paths. In two read-only helper tests, build_output accepted each as a purportedly outside output parent and reached verify_result. That function was replaced only for these narrow helper tests with a sentinel that raised immediately. No archival code executed and no output was created. This is a confirmed guard bypass; an end-to-end build against an actual package was not run.

The precise mechanism is that normalized path strings are not complete filesystem identities. Compare the input-root device/inode against every existing output-parent ancestor, or use Path.samefile on those ancestors. Retain the current final-output symlink/no-clobber checks and canonical output-parent handling. Add real CLI controls for filesystem case aliases and APFS firmlinks where available. Recheck both normal and optimized execution. Concurrent hostile filesystem replacement is a separate unsandboxed boundary and is not the mechanism demonstrated here.

Reproduction outline, read-only after loading the fully reviewed V2 helper with its exact SHA256 gate:

```python
p = Path('.../format_review_01').absolute()
aliases = [p.parent / 'FORMAT_REVIEW_01', Path('/System/Volumes/Data') / str(p).lstrip('/')]
def sentinel(*unused):
    raise RuntimeError('HELPER_SENTINEL_NO_ARCHIVAL_EXECUTION')
api['build_output'].__globals__['verify_result'] = sentinel
for alias in aliases:
    assert p.samefile(alias) and p.resolve() != alias.resolve()
    # Both actual tests reached the sentinel rather than rejecting containment.
    api['build_output']({}, '0'*64, SimpleNamespace(root=p, output=alias/'oriented-flow-verification.zip', verify_only=False))
```

The literal ellipsis is explanatory path notation, not a runnable final command or an invented actual candidate. Exact observations are retained in the tool transcript: case_alias and APFS_data_alias each had root_and_output_parent_same_inode=true, resolved_paths_equal=false, unexpected_replay_gate_reached=true, output_created=false, archival_execution=false.

### Preserved controls and findings

HELPER_RECEIPTS.json contains 56 V1 helper cases. Two disclosed helper-sentinel cases created a ZIP physically inside their synthetic helper input directory: a root spelling with dotdot, and a symlink output ancestor. These fixtures were format-boundary tests, had no paper, and replaced replay explicitly. No real current wrapper or mathematical verification was synthesized. Parent delta04 fixed these two specific mechanisms.

HELPER_V2_RECEIPTS.json contains the same 56 cases under assigned V2. The original dotdot/symlink attacks now reject before the replay sentinel and create no output. The additional two physical-alias bypasses above were discovered after that saved suite and are only in this log/transcript because new-file writes failed.

The bounded suites exercised strict duplicate/nonfinite/overflow JSON, typed integer byte counts, malformed SHA256, paths, case/directory aliases, file/directory collisions, total bounds, symlinks/FIFOs, extra empty directories, wrong sizes, raw ZIP prefix/suffix/truncation, local-metadata disagreement, and trailing/concatenated raw DEFLATE streams. The raw-DEFLATE controls adjust declared local/central compressed sizes and EOCD offsets, so they test actual unused compressed bytes rather than merely malformed outer ZIP extents. Same-runtime deterministic bytes matched. No cross-runtime compressed-byte promise was inferred.

SOURCE_ONLY_RECEIPT.json preserves a real full-corpus source-only dispatcher run with observational wrappers and an audit hook. All three complete corpus streaming pins completed before the first parse read. The exact canonical pair was 5104 bytes with SHA256 fef71ca1603c57d1335d95fdd80a4e3d8dad6e0ed454e92fd60b3945e229ca06. The statement was 145 bytes with SHA256 abd6df90fc1875d313d62fc5c4c3d26c55878cad686b63685885be06a1c979bb. Archival original_inputs/replay helpers were replaced with forbidding sentinels and were not reached. Zero archival-source file-open events and zero subprocess.Popen events were observed. No corpus body was copied.

Six additional real-process source-only CLI negatives were observed in the tool transcript: partial corpora returned1; unknown and abbreviated flags returned2; missing I, S, or B returned1. All six had zero subprocess.Popen events. These pending observations have no separately saved raw stdout/stderr file or raw-output hash receipt; no such capture is invented.

All four actual primary bodies independently passed complete stream_pin helpers with frozen sizes/hashes. Existing BGT_2106.12266_root.pdf was 967612 bytes and SHA256 9d78c8dd86aaa62dbaa7bfcaf40195c901c3cc9dee025bffd4a6e29af64339ba. No body was copied or renamed. The exact primary_only directory positive remains NOT RUN because the available BGT basename differs from required basdevant_gouere_theret_2106.12266.pdf. primary_only on that directory correctly rejected the absent required name. Hash agreement is only byte authentication, never theorem interpretation.

Actual authored preprint metadata was inspected read-only. metadata.json: 5392 bytes, SHA256 9cf4e1d1f3c9a9602999646f1f68bbed15da7283a005c6afdacd371fe02e879a. zenodo-deposit.json: 5707 bytes, SHA256 dec24c56cd7db7027221123d790f0c3a7837b4db04c5863adb7457ce9c9264b1. Nested metadata equality, exact two asset names/paths and creator/affiliation/ORCID match. The description explicitly separates finite/hash checks from proof/novelty, states the unrefereed and AI-agent-review status, and limits compressed reproducibility to the same runtime. This is authored-metadata inspection, not a current-wrapper pass.

Historical artifact-format boundaries were read after initial independent formulation: the original root permits several format cases excluded by the new wrapper, including extra empty directories/dangling symlinks/FIFOs, duplicated JSON keys/payload rows and unchecked metadata. The launcher preserves original bytes and accurately distinguishes the stricter current outer format. The reviewed code enforces measured I-S-B child isolation, historical requested []/O/I/IO labels, root and checker compile optimize=0, one root launch and 64 nested requests with 20 positive/20 assertion-negative/20 corrupt/4 patch schedule. These are code-review findings only here; actual replay of the current candidate is still not run.

### Environmental chronology and exact remaining work

The first source-only attempt stopped at its startup SHA256 gate when the tool changed from V1 before new V2 assignment. No corpus read or archival execution occurred in that failed attempt. After V2 assignment and delta review, saved helper/source-only runs succeeded. New-file creation later failed with explicit errno28 even for a small incident receipt; appending existing log succeeded. Parent cleanup of its own 77 completed renders was followed by one authorized new-file probe for SUPPLEMENTARY_RECEIPTS.json; this still failed errno28. candidate_review.py, ENVIRONMENT_INCIDENTS.json and SUPPLEMENTARY_RECEIPTS.json were not created. No later new-file probe or foreign cleanup was attempted. The final report and decision therefore live inside this existing research log and the handoff message; no nonexistent REPORT.md, DECISION.json or manifest file is claimed.

The parent reported actual current-root assembly blocked by ENOSPC and asked the user to free2GB. No independently pinned actual CURRENT_PUBLICATION_MANIFEST candidate was supplied. Consequently all actual-current authentication-only, default normal/O, exact ZIP builds, normal/O physical-alias CLI regressions, fresh current metadata/path mutations, every-safe-index-file authentication and current-tree before/after checks remain pending. The original30 current copies must be independently authenticated against all frozen byte/Git-blob pins; a fresh assigned-head Git tree/blob comparison also remains unperformed by this reviewer because Git was forbidden. No completed actual wrapper or end-to-end publication pass can be inferred from helper fixtures, source-only pins, metadata inspection or another agent's receipts.

Required next steps: fix physical-alias containment, freeze/review the delta, restore sustained writes, assemble the actual safe-file-allowlisted candidate, provide its independently computed external manifest pin, and perform the pending actual normal/O authentication/replay/build controls. Then perform the separately required two new sequential final whole-package reviews. The present report is an initial tooling handoff only.

## Initial decision object

```json
{
  "actual_current_wrapper": "NOT_RUN",
  "actual_exact_zip_builds": "NOT_RUN",
  "archival_code_executed_by_this_reviewer": false,
  "completion_estimate_percent": 65,
  "decision": "REVISE_TOOLING_AND_DEFER_CURRENT_WRAPPER",
  "default_normal_and_optimized_current": "NOT_RUN",
  "final_whole_package_clear": false,
  "initial_review_handoff_complete": true,
  "new_report_decision_manifest_files_created": false,
  "novelty_or_math_acceptance": false,
  "v1_dotdot_symlink_defect_fixed_in_v2": true,
  "v2_physical_alias_containment_defect_open": true
}
```

2026-10-16T04:30:34.638662+00:00 — 70% complete. After explicit restored-capacity authorization, actual written V4 was pinned (41629 bytes, SHA8832a44a53f0df4867cb8196d725209dd7ac5944c82b4f296b7514155fe72e6c). Fresh minimal exact30-source fixture and independent index 798dab320e333bbb09ff2e7664676335a5aecf0f1937551656fc3c7702f6207f authenticated in normal/O CLI processes. Twenty real CLI cases passed; every process completed package authentication exactly once and had zero Popen, all containment builds rejected with no ZIP and zero stderr. Originals and fixture unchanged. V3 narrower residual and V4 indexed-directory mechanism reviewed/tested in memory; wider Data-root case helper-only. New safe V4 report/decision/receipts and pending supplementary summaries saved. Actual full current candidate, default replay and outside exact build remain pending; no final whole-package CLEAR. No Git, archival execution or outside writes.
