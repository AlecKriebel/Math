"""Own bounded audit authorship only; no proposed production imports or executions."""
from pathlib import Path
import datetime as dt, hashlib, json, os, stat
R=Path('/Users/alec/Documents/Math')
A=R/'draft_pr_publication_program_20260930/audits/pr48_2961'
F=A/'corrective_source_adversary_v3'
P=A/'post_push_foreign_epoch_preparation_v3'
NOW=dt.datetime.now(dt.timezone.utc).isoformat()
SHA='3e53126a491880c8aefc614f1c40a5fb965dfcb4c11678cd085e1394369650f8'
def raw(p):
    assert p.is_file() and not p.is_symlink() and all(not q.is_symlink() for q in p.parents)
    return p.read_bytes()
def ref(p):
    b=raw(p);return dict(path=p.relative_to(R).as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),full_mode=stat.S_IMODE(p.stat().st_mode))
def put(n,v):
    b=(json.dumps(v,indent=2,allow_nan=False)+'\n').encode() if type(v) is not str else v.encode()
    with (F/n).open('xb') as f:f.write(b)
    assert stat.S_IMODE((F/n).stat().st_mode)==0o644
rows={}
def add(z):
    q=R/z['path'];v=ref(q)
    assert v==z
    if z['path'] in rows:assert rows[z['path']]==z
    rows[z['path']]=z
old=json.loads(raw(A/'corrective_source_adversary_v2/FIXED_INPUT_BINDINGS.json'))
assert len(old['fixed_rows'])==117
for z in old['fixed_rows']:add(z)
families=[]
for name,expected in [('post_push_foreign_epoch_preparation_v3',24),('corrective_source_adversary_v2',20),('corrective_source_adversary_v2_m2_addendum',6)]:
    base=A/name;files=sorted(q for q in base.rglob('*') if q.is_file());dirs=sorted(q for q in base.rglob('*') if q.is_dir())
    assert len(files)==expected and all(not q.is_symlink() and (q.is_dir() or q.is_file()) for q in base.rglob('*'))
    assert all(stat.S_IMODE(q.stat().st_mode)==0o644 for q in files)
    assert all(stat.S_IMODE(q.stat().st_mode)==0o755 for q in [base]+dirs)
    for q in files:add(ref(q))
    families.append(dict(path=base.relative_to(R).as_posix(),payload_count=len(files),payload_names=[q.relative_to(base).as_posix() for q in files],directory_names=['.']+[q.relative_to(base).as_posix() for q in dirs],full_file_mode=0o644,full_directory_mode=0o755))
m2=json.loads(raw(A/'corrective_source_adversary_v2_m2_addendum/OBSERVATIONS.json'))
for z in [m2['operator']]+m2['genuine_actual_CAP4_members']:add(z)
outer=m2['genuine_outer_directory'];assert stat.S_IMODE((R/outer['path']).stat().st_mode)==outer['full_mode']==0o700
assert hashlib.sha256(raw(P/'SOURCE_READY.json')).hexdigest()==SHA
assert not (P/'SOURCE_MANIFEST.json').exists()
assert not (A/'post_push_foreign_epoch_preparation_v2/SOURCE_MANIFEST.json').exists()
assert not (A/'corrective_source_adversary_v2/SELF_MANIFEST.json').exists()
ready=json.loads(raw(P/'SOURCE_READY.json'))
assert ready['closure_payload_count']==24 and ready['closure_directory_count']==4
for z in ready['source_files']:
    actual=rows[z['path']];assert {k:actual[k] for k in z}==z
cap=json.loads(raw(F/'private_actual_capture_v2/CAPTURE.json'))
result=json.loads(raw(F/'private_actual_capture_v2/stdout.json'))
assert cap['pid']==result['actual_private_pid']==92858 and cap['operator_pid']==92857
assert cap['status']=='PASS' and cap['exit_code']==0 and result['checks']==49
assert result['status']=='PASS_CONTROLS_WITH_M3_COUNTEREXAMPLES'
assert len(result['M3_actual_private_chmod_counterexamples'])==3
for c in result['M3_actual_private_chmod_counterexamples']:
    assert c['V3_mode_context_unchanged'] is True and c['required_live0644_predicate_accepts'] is False and c['c1ae_body_only_unchanged_predicate_accepts'] is True
    assert c['snapshot_full_mode']==0o644 and c['outer_full_mode']==0o700
    assert c['live_complete_body_sha256']==c['snapshot_complete_body_sha256']=='c1ae969ccbbc48ed6fb486e96184da94329291a46b27d2b891ecb87185c909ec'
assert [c['live_full_mode'] for c in result['M3_actual_private_chmod_counterexamples']]==[0o600,0o2644,0o4644]
put('FIXED_INPUT_BINDINGS.json',dict(schema='pr48-v3-independent-fixed-source-and-historical-bindings/v1',observed_utc=NOW,fixed_rows_count=len(rows),fixed_rows=[rows[k] for k in sorted(rows)],exact_preserved_families=families,additional_genuine_outer_directory=outer,candidate_SOURCE_manifest_absent_at_observation=True,superseded_V2_SOURCE_manifest_absent_at_observation=True,old_twenty_payload_review_SELF_absent_at_observation=True,candidate_closure_required=False,qualification='Rejected unclosed V3 SOURCE stays body/full0644 fixed. Old V2 and its twenty-payload incomplete PASS stay unclosed and unmodified. No future live native/HEAD approval; no production import/compile/execution. Whole-body hashing is custody verification, not an independent mathematical proof.'))
finding=dict(id='M3',title='Actual live ROOT capture operator full07777 mode is absent from source custody contexts',locations=['epoch_common.py:92-93','epoch_common.py:100-102','inspect_complete_actual_post_epoch_v3.py:37','inspect_complete_actual_post_epoch_v3.py:52','capture_root_command.py:47'],mechanism='Only retained prelaunch_operator.py is described. Chmod-only changes to the actual live c1ae ROOT operator leave all described context bodies and full modes equal; c1ae operator_unchanged compares bytes only.',actual_private_child_pid=92858,live_private_modes=[0o600,0o2644,0o4644],retained_snapshot_mode=0o644,actual_outer_role_mode=0o700,body_sha256='c1ae969ccbbc48ed6fb486e96184da94329291a46b27d2b891ecb87185c909ec',repair='Add typed actual-live ROOT operator path/body/full0644 descriptors in author, caller, and complete-inspector before/after boundary contexts. Require its actual parent0755 and entire body equal the retained genuine c1ae snapshot. Preserve genuine outer0700, all source/prelaunch0755 roles, and c1ae original source unchanged.',reasonably_repairable=True,mathematical_defect=False)
put('VERDICT.json',dict(schema='pr48-post-push-epoch-independent-SOURCE-verdict/v1',status='REPAIR_REQUIRED_SOURCE',utc=NOW,source_ready_sha256=SHA,mandatory_findings=[finding],production_executed=False,future_acceptance_approved=False,review_continuity='Same independent investigator as original M1 rejection and incomplete V2 PASS; explicit corrective continuity, no blind/new-math-family claim.',M2_four_typed0700_outer_roles_repaired=True,M1_full07777_source_custody_complete=False,prior_incomplete_PASS_preserved_unchanged=True,prior_M2_addendum_preserved=True,checked_current_candidate_payloads=24,fixed_input_bindings=len(rows),actual_private_controls=dict(pid=92858,caller_pid=92857,checks=49,capture='private_actual_capture_v2/CAPTURE.json',whole_stdout_sha256=cap['stdout']['sha256'],whole_stderr_sha256=cap['stderr']['sha256'],candidate_or_ROOT_operator_executed=False),unchanged_original_merge='209581a',original_first_three_captures_unchanged=True,original22_scientific_ROOT_contract_unchanged=True,mathematical_adversary_credit=0,actual_recovery_completion_percent=0,source_audit_completion_percent=100,remaining_gap='Exact bounded actual-live operator repair and corrective SOURCE review, then genuine ROOT closure/readback, actual per-role final three operations, complete22 ROOT post, and separately corrected PR49 mixed-phase consumer.'))
report=f'''# PR48 corrective V3 SOURCE audit

REPAIR_REQUIRED_SOURCE. V3 READY `{SHA}` fixes the four outer-directory mode mismatches (M2), but the actual running ROOT capture operator is still omitted from the promised full07777 source custody (M3). This is a repairable operational defect. It changes no mathematical conclusion or prior genuine merge/push receipt.

Scope was saved before implementation reading at 2026-10-03T16:29:30.645077+00:00. This is the same investigator continuing the original M1 rejection and the subsequently incomplete V2 PASS. The twenty original V2 review files, old READY9435a9…/VERDICT9177f9…/REPORT404190…, both rejected unclosed source versions, and the separate M2 addendum remain byte/mode unchanged. No earlier PASS is authority for V3. The M2 addendum records both original failed allocations honestly.

## Verified repair and unchanged scope

V3 common83–85 requires typed exact0700 or0755. Operator-binding93, author101, caller102 and inspector37 now use0700 solely for genuine ROOT outer captures. Own/source/runtime/retained-prelaunch directories still require0755. The actual immutable c1ae operator line25 creates0700, and the genuine PR57 closure outer directory was read as0700 without mutation. Handwritten private controls accepted that genuine read-only observation and rejected755 and special-bit outer modes; own directories755 remain strict. The candidate's own28 directory controls were read as evidence of their declared narrow model, not full execution of the proposal.

All seven complete current operative sources were compared to the preceding V2 sources with explicit version/path substitutions; COMPLETE_SOURCE_CHANGE_MAP.json retains the residual changes. The two derived finalizer/mirror bodies are byte-identical to V2. Four actor changes after those explicit substitutions are limited to the intended M2/history changes. Candidate READY, contract, source closers/readers, authorship sources and control artifacts were read as text. FIXED_INPUT_BINDINGS.json independently rechecks all24 candidate payloads, the previous117 selected custody rows, the prior20 review payloads, the six M2 addendum payloads and selected genuine c1ae/PR57 CAP4 members, without duplicating their bodies. No proposed production code was imported, compiled or executed.

The original science17 pins, accepted2961 unsolved shared2/5 budget with30004403 alias absent, product-subgroup4/all-powers partial claim, signed-averaging obstruction, new0/audit0 accounting, original closed53 source, original first three CAPs and original22-key scientific ROOT contract remain unchanged. There is no proof of the full group, paper, DOI or discovery credit from this operational review. Per-role fresh HEAD/index/foreign epochs, whole-current QUEUE authentication with exact selected-row/unrelated-row preservation, other12 native constraints, exact two owned logs and mixed genuine old3/new3 phase receipts remain required. Their actual future execution is absent.

## Mandatory M3: live operator omitted

`epoch_common.py:92–93` binds only `outer/prelaunch_operator.py` (retained source644/c1ae) and outer700. `author_source_modes:100–101` and `caller_source_modes:102` carry that retained snapshot and runtime dependencies, without an actual-live `capture_root_command.py` path or full mode. `inspect_complete_actual_post_epoch_v3.py:37` does the same; its line52 body-only snapshot comparison adds no actual-live mode. The unchanged c1ae operator line47 tests its own bytes, not permissions.

Actual private caller92857 launched handwritten child92858 successfully at 2026-10-03T16:47:54.060409–16:47:54.096208UTC, exit0. Its49 checks include actual chmod of only the private live c1ae byte copy644→600/2644/4644 while the snapshot stays644, outer700 and actual parent755. Entire live/snapshot body SHA is c1ae969c… for all three. Each declared V3 snapshot mode context stays identical and body-only operator_unchanged stays true, while the required actual-live644 predicate rejects. This is a filesystem counterexample to completeness of the declared custody mechanism, not a simulated candidate production run. Actual ROOT source/capture modes were never changed. Fixtures were restored644/755. Full stdout9262B SHA`{cap['stdout']['sha256']}` and empty stderr are retained with complete prelaunch source/operator, exact argv/PIDs/UTC in private_actual_capture_v2.

Narrow repair: include a typed actual-live operator descriptor in all author/caller/inspector boundary contexts, require its whole c1ae body and full0644, require actual parent0755, and require bytes identical to the retained snapshot. Keep c1ae unchanged and outer700 intact. No exemption, monkeypatch or broad role relaxation is warranted.

ROOT has stated the concrete future runtime copy step: copy the entire reviewed c1ae2593B source unchanged0644 to absent A48/capture_root_command.py, independently reread body/mode/hash, then use the A48-adjacent operator and the exact inspector capture basename. This resolves the source's adjacency integration plan when genuinely performed. It is a future requirement, not an executed copy or approval; it does not repair M3 by itself.

## Failures and remaining gap

The first independent private capture attempt (tool517c37) failed ENOSPC while creating prelaunch source, before capture setup or private child launch. PRIVATE_PREPARATION_FAILURE.json preserves the returned traceback locator; no child PID/time/full stream is invented. The original attempted operator source remains. A distinct v2 private operator and distinct actual directory then succeeded as above. A later read-only summary-print command (tool496a0c) printed complete capture and result before TypeError on an integer `checks` field; it changed no artifacts and is not the child control result. The mistaken candidate-closer filename read (d5096e) returned file-not-found and was followed by reading the exact declared source names; it changed no artifacts.

This SOURCE audit is100% complete for the bound V3 rejection; actual recovery0%, new mathematical discovery0%. Remaining work is exact repaired SOURCE review and genuine ROOT-only evidence closure/readback, then real authorized operations and complete22 post; PR49 needs its own corrected mixed-phase/full-mode consumer. No future approval, self-closure or native/Git/index/ref/remote change occurred here. ROOT-only own closer/reader are unexecuted proposals for freezing this adverse evidence alone, not the rejected candidate.
'''
put('REPORT.md',report)
put('RESEARCH_LOG.md',f'{NOW} — Corrective V3 SOURCE scope complete. Four typed0700 M2 roles independently verified; full actual-live operator custody still omitted (M3). Handwritten actual private caller92857/child92858 exit0 passed49 selected checks with three real chmod-only counterexamples. Original517c37 prelaunch ENOSPC failure retained; no candidate/ROOT execution. Prior incomplete20-file PASS and six-file M2 addendum untouched. Strongest result: repairable SOURCE rejection with exact mechanism and finite permission counterexamples. SOURCE review100%; actual recovery0%; mathematical discovery0%.\n')
print(json.dumps(dict(status='SAVED_REPAIR_REQUIRED_SOURCE_M3',actual_author_pid=os.getpid(),utc=NOW,fixed_rows=len(rows),report=ref(F/'REPORT.md'),verdict=ref(F/'VERDICT.json'),M2_report=ref(A/'corrective_source_adversary_v2_m2_addendum/REPORT.md'),M2_verdict=ref(A/'corrective_source_adversary_v2_m2_addendum/VERDICT.json')),indent=2))
