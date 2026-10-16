#!/usr/bin/env python3
"""Terminal bounded-repair evidence seal; no service or candidate mutation."""
import difflib, hashlib, importlib.util, json, sys
sys.dont_write_bytecode=True
from datetime import datetime, timezone
from pathlib import Path
D=Path(__file__).resolve().parent
A=D.parents[1]
P=A/'NEWpreprint_v1_0'
ARCHIVE='PR1071_preprint_v1_0_support.zip'
def need(ok,msg):
    if not ok:raise RuntimeError(msg)
def read(p):return json.loads(p.read_text())
def write(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
def pin(p,n):
    b=p.read_bytes();return {'path':str(n),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def check(p,r):need(pin(p,r['path'])==r,'Identity drift '+str(p))
def main():
    need(not (D/'SEAL.json').exists(),'Already sealed: inspect rather than overwrite')
    result=read(D/'FINAL_VERIFICATION.json');need(result['status']=='PASS','Controls not passed')
    s=importlib.util.spec_from_file_location('bounded_custody',D/'verify_case_alias.py');v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
    need(v.custody()==result['custody'],'Terminal custody differs')
    commands=[json.loads(line) for line in (D/'COMMAND_STREAM.jsonl').read_text().splitlines()]
    need(len(commands)==result['controls']['actual_commands']==201,'Incomplete actual-command stream')
    need([r['index'] for r in commands]==list(range(len(commands))),'Actual-command index gap')
    need(all((r['returncode']==0)==r['expected_success'] for r in commands),'Unexpected command result')
    need(sum(r['expected_success'] for r in commands)==19,'Success accounting drift')
    write(D/'COMMAND_RECEIPT_INDEX.json',{'status':'PASS','complete_exact_command_records':'COMMAND_STREAM.jsonl','actual_commands':len(commands),'expected_successes':19,'expected_rejections':182,'all_outcomes_match':True,'stream':pin(D/'COMMAND_STREAM.jsonl','COMMAND_STREAM.jsonl'),'meaning':'Each JSONL record contains actual UTC, exact argv/cwd, mode, return code, expected outcome, full stdout and stderr. This is a retained execution record, not planned tests.'})
    changes=read(D/'AUTHORIZED_EXISTING_CHANGES.json')['records']
    patch=[]
    for row in changes:
        name=row['path']
        if name.endswith('.zip'):continue
        before=A/row['before_bytes_path_relative_to_audit'];after=A/name
        patch.extend(difflib.unified_diff(before.read_text().splitlines(keepends=True),after.read_text().splitlines(keepends=True),fromfile='before/'+name,tofile='after/'+name))
    for name in ['CASE_ALIAS_REPAIR_STATUS.json','CASE_ALIAS_REPAIR_NOTES.md','CASE_ALIAS_SOURCE_EVIDENCE.json','CASE_ALIAS_COPY_EXCLUSIONS.json']:
        patch.extend(difflib.unified_diff([], (P/name).read_text().splitlines(keepends=True),fromfile='/dev/null',tofile='after/NEWpreprint_v1_0/'+name))
    (D/'COMPLETE_CODE_AND_PROSE_CHANGES.patch').write_text(''.join(patch))
    current=[pin(f,f.relative_to(P)) for f in sorted(P.rglob('*')) if f.is_file() and not f.is_symlink()]
    audit=[pin(f,f.relative_to(A)) for f in sorted(A.rglob('*')) if f.is_file() and not f.is_symlink() and not f.is_relative_to(D)]
    write(D/'CURRENT_CANDIDATE_PINS.json',{'scope':'Every current regular candidate file, including unchanged excluded historical preparation derivatives. Manifest alone defines the distribution.', 'records':current})
    write(D/'CURRENT_AUDIT_PINS.json',{'scope':'Every current regular audit file outside this bounded effort; no copied source tree. Effort is separately sealed.', 'records':audit})
    before=read(D/'BASELINE_INPUT_PINS.json')['records']
    need(len(audit)==len(before)+len(read(D/'CHANGE_INVENTORY.json')['all_new_paths_outside_effort']),'Current audit path count drift')
    pdf=pin(P/'paper.pdf','paper.pdf');tex=pin(P/'paper.tex','paper.tex');archive=pin(P/ARCHIVE,ARCHIVE)
    need(pdf['bytes']==93113 and pdf['sha256']=='33b90a4d846db58ea93efd453c13455fbeb3a29dcaa3e4cc49a68c0a8ebdff5b','Paper PDF changed')
    need(tex['sha256']=='4ffbe0d65609213fd91aecf675661ff278e4e1bd5037db8836f1291f5bdc1d78','Paper source changed')
    stamp=datetime.now(timezone.utc).isoformat()
    with (D/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+stamp+': Terminal rehash, complete code/prose/manifest/map diff, exact before bytes, all actual receipts and current inventories complete. Bounded repair completion estimate 100%. This is not NEW whole03 or root adoption; publication_ready/issues_resolved/published remain false; service cursor held after PR1032; full priority UNKNOWN. No Git, service mutation, external contact, new agent, compile/render or PDF marker occurred.\n')
    report=f'''# PR1071 bounded physical case-alias support repair

Completed {stamp}. Candidate: literal `NEWpreprint_v1_0`; submitted head `fc37aa5169a0fe6adae0a254c9ee6c1531a2911f`, problem 30002170 / OWR-12013-003. This is the bounded repair of the new **CASE-1071 P3** support-interface defect, followed by actual adverse filesystem/replay/custody controls. Extensive AI assistance; unrefereed. It is not a new whole mathematical review, human review, formal certificate, priority clearance or publication approval.

**The assigned case-alias defect is repaired and all 201 actual controls pass.** Two prior NEW complete whole reviews remain completed (minimum two); their latest whole02 verdict was zero actionable. A later program/root support audit found CASE-1071. Current `CASE_ALIAS_REPAIR_STATUS.json` requires a **NEW complete whole03** and root repair/terminal adoption. `publication_ready=false`, `issues_resolved=false`, `published=false`; ordered services remain held after PR1032. Earlier `STATUS.json`, `CURRENT_STATUS.json`, `TERMINAL_STATUS.json`, `FINAL_ACCEPTANCE.md`, `FINAL_SEAL.json` and `FINAL_INTEGRITY.json` remain exact dated history. The later program support hold supersedes their former readiness; this worker does not rewrite or reissue those seals.

The seven-page paper PDF is unchanged: {pdf['bytes']:,} bytes, SHA256 `{pdf['sha256']}`. The source is unchanged, SHA256 `{tex['sha256']}`. Current support ZIP: **{archive['bytes']:,} bytes**, 166 regular members, SHA256 `{archive['sha256']}`. The previous 1,440,215-byte ZIP, SHA256 `88578e338672ef426c8dd65e1b0020997fdd422487811d336d3953b8dff9e037`, and its sidecar are retained exactly only in local before custody.

## Exact defect and repaired mechanism

The outside-every-frozen-descendant contract previously compared lexical paths before/after `Path.resolve()`. On this case-insensitive Mac filesystem, `kit` and `KIT` identify the same physical directory while `resolve()` retains different spelling. Root's actual normal/-O archive commands accepted the alias path despite rejecting the canonical-spelling control. This concerned creation of a fresh file physically inside the kit; existing leaves remained guarded, and no existing-input overwrite or mathematical defect was established.

`scripts/package_paths.py:fresh_output` now compares every existing output ancestor's physical identity (`Path.samefile`, hence device/inode identity) with the existing frozen root. It examines the entire ancestor chain even above absent intermediate directories. It therefore handles the output alias in either script-root spelling direction without generic lowercasing. The existing lexical/resolved containment test is retained. A genuinely absent leaf, a real existing parent, no symlink ancestors and a new empty external checker/compiler directory remain mandatory. Existing files/directories, dangling links and existing hardlink aliases remain rejected. Parent traversal (`..`) is rejected before normalization so lexical collapse cannot hide a symlink ancestor. No output directory or file is created by preflight. This is the same static local/trusted-program boundary, with no concurrent filesystem race or arbitrary-executable guarantee.

All three actual entry points call this shared guard before ZIP creation, checker mkdir/copy/subprocess, or PDF mkdir/copy/compiler. Their source bytes are unchanged. The copied original finite checker, all result/source mathematical guards and citation parser are unchanged. The fresh-empty-output-directory boundary continues to exclude existing aliases at every checker/compiler child file, log and receipt path.

The second operative code change is explicit current support-hold accounting in `scripts/verify_package.py`. It still validates the dated historical preparation/current/terminal records and prior whole02/root evidence, then requires the new repair state, two prior reviews/minimum two, new whole03 incomplete/required, new P3 bounded-repaired, root adoptions required, all false readiness/publication flags and the PR1032 hold. Coherent-manifest mutations demonstrate that these are semantic checks, beyond hashes. This bounded repair does not reinterpret historical whole02 as having found the later issue or count itself as whole03.

## Read scope, permitted edits and preserved claims

Before mutation I read the full program `ROOT_CASE_ALIAS_SCOPE_REVIEW.json` and full scope REPORT, current README/supplement/status/repair notes, all five operative support modules, full prior whole02 REPORT, root whole02 adoption, old root final seal/integrity, full terminal administrative REPORT, full prior bounded-repair REPORT, and current native/custody/manifest/binding interfaces. No unrelated candidate package was inspected. Source identities are in `PROGRAM_SOURCE_PINS.json`. The distributed `CASE_ALIAS_SOURCE_EVIDENCE.json` is expressly a scoped authored excerpt: the exact CASE-1071 report section, relevant root fields and root's actual PR1071 command records, accompanied by full source pins. It is not mislabeled as a complete program-scope copy or a replay of those old commands.

The hash-only baseline captured **668 prior regular audit files** before any mutation. Every one of the **nine** permitted existing edits was saved first as exact before bytes: README, SUPPLEMENT, shared path policy, operative verifier, copy map, manifest, ZIP, sidecar and upload bindings. The **659 other baseline files remain byte-exact**. All source/PDF/TeX, native bibliographic metadata, citation, original finite checker/baseline, submitted proof and review/source/priority artifacts, historical statuses/pins/seals, native uploader manifest and entry scripts remain unchanged. `CHANGE_INVENTORY.json` inventories all before/after identities and new candidate paths; `PROTECTED_UNCHANGED.json` names every unchanged baseline file.

The accepted all-H claim remains for independent standard equal-H fBm, canonical iterated area, each fixed H in (1/4,1), every T>0, n>=1, both complete uniform grids and every L2 observation estimator. Brownian optimum and smooth rate are prior; Fourier bump/Gaussian projection antecedents remain credited. The specific old NTU v1 lag-coefficient defect is not asserted to be a journal error. No endpoint, sharp constant, exact limit, H-uniform, adaptive/nonuniform, unequal-H or correlated-component claim is added. Full novelty, historical/method priority and worldwide current-open status remain UNKNOWN. No firstness, human review or formal certification is claimed.

`COMPLETE_CODE_AND_PROSE_CHANGES.patch` includes every changed existing text file (including the complete map/manifest/binding/sidecar diffs) and every new current authored prose/status/evidence/exclusion artifact. The changed binary ZIP is fully before/after pinned and independently reconstructed. New exact historical custody copies are individually byte-compared and inventoried, rather than treated as newly authored semantic changes.

## Complete custody and individual omissions

All **116 original source-copy rows retain their exact values and order**. Twelve exact authored copies were appended: seven changed pre-repair interface snapshots, the old ROOT final seal/integrity, and terminal administrative report/output pins/seal. All **128** source/copy pairs are byte-equal. Explicit `source_snapshot` locators resolve changed old originals to their exact before bytes. The old root seals remain complete and retain their dated meanings inside the distribution as well as unchanged at their original locations.

`HISTORICAL_STAGE_RESOLUTION.json` preserves and actually rechecks every **2,788** original terminal stage row, in order, to exact current or before bytes. It also rechecks **1,558** later terminal output/current-candidate/current-audit/protected captures. The baseline's 668 immediate inputs and AGENTS bytes are separately verified. No captured stage, old report, pin or seal is silently rewritten, omitted or made to point at different current bytes.

`CASE_ALIAS_COPY_EXCLUSIONS.json` individually pins all **29** unselected terminal files, previous ZIP/sidecar and full program/scope source records; existing whole01/whole02 omission ledgers remain exact and are independently rehashed. Full scope sources are represented only by clearly scoped authored excerpts plus full-source hashes. No third-party full source, extract, pixel, runtime, raw service/compiler stream or old archive payload is added to the distribution. No omitted historical program/environment is claimed newly replayed. `CURRENT_CANDIDATE_PINS.json` and `CURRENT_AUDIT_PINS.json` hash all current regular files; the explicit manifest controls the narrower archive membership.

The external `publication/zenodo-deposit.json` is unchanged byte-for-byte and has exactly `metadata`/`files`. Its native metadata object equals all three unchanged reviewed package bibliographic objects exactly. It still selects the unchanged `paper.pdf` and same-named current support ZIP. Included `deposit.json` remains a historical metadata wrapper, not a native uploader input. Only three required external binding scalars changed: archive byte count, archive SHA256 and manifest SHA256; the PDF binding and all descriptive fields remain exact. The current workflow qualifications are given explicitly by the new repair record and README.

## Actual controls and retained execution evidence

One disposable extraction was used, with small disposable copies for protected external record types. `ACTUAL_CASE_IDENTITY.json` records actual samefile/device/inode identity for `kit`/`KIT`, distinct resolved spellings and nested `custody`/`CUSTODY` identity. No writer or alias control targeted a canonical audit inode. The extraction was removed by its context after all controls; no pre-existing derivative or historical file was removed.

The **201 actual commands** comprise **19 expected successes** and **182 expected rejections**, all with correct outcomes. `COMMAND_STREAM.jsonl` retains actual timestamps, exact argv/cwd, normal/-O mode, return codes and complete stdout/stderr for every command, indexed 0 through 200 without a gap. `COMMAND_RECEIPT_INDEX.json` binds and rechecks that stream. Planned tests are not evidence.

There are **72 actual writer-location rejections**: archive/check/PDF, ordinary and optimized Python, canonical and uppercase script-root paths, canonical/uppercase target spellings, existing nested parents and absent multi-level parents. Every rejection occurs before output creation; PDF tests name a nonexistent compiler and reject in preflight before attempting it. Missing intermediate directories are never created. The frozen extracted bytes are checked before/after each such case. Safe physically external case aliases are accepted, including actual archive and checker commands through the uppercase script path; no generic case-folding false rejection occurs.

Both modes pass documented default read-only verification, explicit/default temporary original checker replay, deterministic archive rebuilding, strict present bindings and repeat verification. Required missing bindings, malformed bindings, corrupt PDF/ZIP/manifest hashes and missing archives reject. The original checker is byte-exact, with all mathematical outputs compared ignoring utc only; its original assertions are disabled under -O, so the unchanged explicit result wrapper supplies that validation. No omitted historical supplementary program is replayed.

All three writers also reject existing files, reused directories containing aliases at thirteen checker/compiler child filenames, hardlink/symlink/dangling destinations, linked parents, symlink ancestors above missing directories, outside missing parents, nondirectory ancestors and direct/symlink-hidden parent traversal in both modes. Disposable canaries and all extracted inputs remain unchanged. The shared API separately rejects direct/hardlink/symlink output forms for **192** protected targets per mode, **576 rejections per mode / 1,152 total**, and accepts four physically external case-spelling combinations per mode. Canonical inodes are never linked for these controls.

Twenty-four coherent-outer-manifest current-status mutations reject: state, completed-review/minimum count, required/new-complete whole03 accounting, bounded-repair identity, root repair/terminal adoption requirements, readiness/issues/published flags and service hold. Identical/malformed bootstrap-manifest symlinks reject before JSON parsing or archive writes in both modes. All scratch mutations are restored exactly, and all **166** extracted files are byte-identical at the final check.

Every ZIP header, payload, CRC, lexicographic name order, fixed 2026-10-14 timestamp, ZIP_STORED compression, Unix create-system and 0644 regular-file mode was checked. A separately implemented reconstruction was compared **after its ZipFile closed** and is byte-identical; the documented normal/-O and safe-case-external rebuilds match too. The actual repository uploader's entirely **LOCAL** `check` passes on the unchanged native manifest, selecting exact current assets. No remote staging, deposit, publish, DOI or service mutation occurred.

No new actual PDF compile, render or PDF marker occurred. The paper/PDF are unchanged, and the root-adopted complete whole02 had already actually compiled both modes and viewed all seven current pages. This task does not claim to repeat that whole-review evidence.

## Disk interruption and remaining gate

After the one-shot mutation and before controls, ENOSPC blocked a read-only shell here-document, then creation of the intended failure-context file. The research log successfully recorded the interruption; a short read then succeeded and the genuine `FAILED_ATTEMPT_01.json` was written. Zero new control commands had run at failure. No incomplete test prefix is promoted to a completed suite, no canonical restoration was necessary, and no old artifact was deleted or masqueraded as another record. The earlier package01 ENOSPC failure record remains exact; `PRIOR_ENOSPC_CONTEXT.json` preserves its distinction from this new interruption. The final 201-command stream is the actual successful suite, followed by full terminal custody rehashes.

Bounded repair execution completion estimate: **100%**. NEW complete whole03 and root repair/terminal adoption remain required. Mathematical acceptance and UNKNOWN priority boundaries are unchanged; support readiness remains held. No Git/index/branch, remote service, DOI, spreadsheet, PR, external communication, other-worker action or new subagent occurred. This seal does not authorize bypassing the ordered PR1032 hold.
'''
    (D/'REPORT.md').write_text(report)
    outputs=[pin(f,f.relative_to(D)) for f in sorted(D.rglob('*')) if f.is_file() and not f.is_symlink() and not f.is_relative_to(D/'_scratch') and f not in {D/'OUTPUT_PINS.json',D/'SEAL.json'}]
    write(D/'OUTPUT_PINS.json',{'utc':stamp,'scope':'Every current regular non-scratch effort file, including complete drivers/report/diff, exact before bytes, failed-attempt context and actual receipts; excludes only this self-manifest and its separate terminal seal. No subsequent command-output writes are pending.', 'records':outputs})
    write(D/'SEAL.json',{'utc':stamp,'status':'BOUNDED_CASE_1071_REPAIR_PASS_PENDING_NEW_COMPLETE_WHOLE03_AND_ROOT_ADOPTION','pr':1071,'head':'fc37aa5169a0fe6adae0a254c9ee6c1531a2911f','output_pins':pin(D/'OUTPUT_PINS.json','OUTPUT_PINS.json'),'output_records':len(outputs),'current_candidate_records':len(current),'current_audit_records_outside_effort':len(audit),'baseline_records':668,'permitted_existing_changes':9,'protected_unchanged':659,'original_terminal_stage_rows':2788,'additional_terminal_stage_rows':1558,'copy_pairs':128,'original_116_rows_unchanged_ordered':True,'archive':archive,'paper':pdf,'tex':tex,'actual_commands':201,'prior_whole_reviews_completed':2,'minimum_whole_reviews':2,'prior_whole02_actionable_findings':0,'new_support_P3_repaired':['CASE-1071'],'new_complete_whole_review_required':3,'new_complete_whole_review_completed':False,'root_repair_adoption_required':True,'root_terminal_adoption_required':True,'old_ROOT_seals_and_all_prior_statuses_preserved_exact':True,'publication_ready':False,'issues_resolved':False,'published':False,'services_held_after_pr':1032,'bounded_completion_percent':100,'no_new_compile_render_or_PDF_marker':True,'no_Git_service_mutation_external_contact_or_new_agent':True})
    for r in outputs:check(D/r['path'],r)
    for r in current:check(P/r['path'],r)
    for r in audit:check(A/r['path'],r)
    check(D/'OUTPUT_PINS.json',read(D/'SEAL.json')['output_pins'])
    print(json.dumps(read(D/'SEAL.json'),indent=2))
if __name__=='__main__':main()
