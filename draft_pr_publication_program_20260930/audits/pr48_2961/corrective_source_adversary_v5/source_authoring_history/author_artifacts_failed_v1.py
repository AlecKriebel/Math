"""Own lean review artifacts only. No proposed SOURCE/ROOT helper is executed."""
from pathlib import Path,PurePosixPath
import datetime as dt,hashlib,json,os,stat
R=Path('/Users/alec/Documents/Math');A=R/'draft_pr_publication_program_20260930/audits/pr48_2961';F=A/'corrective_source_adversary_v5';OLD=A/'corrective_source_adversary_v4';P=A/'post_push_foreign_epoch_preparation_v5';NOW=dt.datetime.now(dt.timezone.utc).isoformat();SHA='19c0ae5198d8dbe62074971ea26a2e2fc470ab7b0e9c76c6c6e27a145833060e';MF_SHA='7d6c549ddd7a3d65a0f329e4d1e550a2b91a9c51b09fb1a7291d8e25e0920fda'
def raw(q):
    assert q.is_file() and not q.is_symlink() and all(not p.is_symlink() for p in q.parents);return q.read_bytes()
def ref(q):
    b=raw(q);return dict(path=q.relative_to(R).as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),full_mode=stat.S_IMODE(q.stat().st_mode))
def put(n,v):
    b=(json.dumps(v,indent=2,allow_nan=False)+'\n').encode() if type(v) is not str else v.encode()
    with (F/n).open('xb') as q:q.write(b)
    assert stat.S_IMODE((F/n).stat().st_mode)==0o644
rows={}
def add(z):
    assert ref(R/z['path'])==z
    if z['path'] in rows:assert rows[z['path']]==z
    rows[z['path']]=z
old=json.loads(raw(OLD/'FIXED_INPUT_BINDINGS.json'));assert old['fixed_rows_count']==229
for z in old['fixed_rows']:add(z)
families=old['exact_preserved_families'][:]
def closed_family(base,expected_sha,expected_count,self_name):
    b=raw(base/self_name);assert hashlib.sha256(b).hexdigest()==expected_sha;m=json.loads(b);assert type(m['files_count']) is int and m['files_count']==expected_count==len(m['files'])
    names=sorted([z['path'] for z in m['files']]+[self_name]);dirs=sorted([z['path'] for z in m['directory_modes']]);assert len(set(names))==expected_count+1
    assert sorted(q.relative_to(base).as_posix() for q in base.rglob('*') if q.is_file())==names and sorted(['.']+[q.relative_to(base).as_posix() for q in base.rglob('*') if q.is_dir()])==dirs
    assert m['file_modes']==[dict(path=n,full_mode=0o444) for n in names]
    assert m['directory_modes']==[dict(path=d,full_mode=0o755) for d in dirs]
    for z in m['files']:
        q=base/z['path'];v=ref(q);assert {k:v[k] for k in z}==z and v['full_mode']==0o444;add(v)
    add(ref(base/self_name));assert stat.S_IMODE((base/self_name).stat().st_mode)==0o444 and all(stat.S_IMODE((base/d).stat().st_mode)==0o755 for d in dirs)
    families.append(dict(path=base.relative_to(R).as_posix(),payload_count=len(names),payload_names=names,directory_names=dirs,full_file_mode=0o444,full_directory_mode=0o755));return m
m=closed_family(P,MF_SHA,27,'SOURCE_MANIFEST.json');assert set(m)=={'schema','source_only','self_excluded','files_count','files','file_modes','directory_modes'} and m['schema']=='pr48-post-push-epoch-source-closure/v5' and m['source_only'] is True and m['self_excluded']==['SOURCE_MANIFEST.json']
oldself=closed_family(OLD,'86c38790af5d66aade5b5ebc09683b78eb31871d4e42b16687c5e2721e4f4911',21,'SELF_MANIFEST.json');assert oldself['verdict_status']=='REPAIR_REQUIRED_SOURCE'
history=json.loads(raw(P/'M4_AND_SUPERSEDED_V4_BINDINGS.json'));hcaps=history['independent_M4_binding']['actual_closed_adverse']['complete_actual_ROOT_captures'];assert [z['complete_capture']['pid'] for z in hcaps]==[19625,19768]
outerdirs=old['additional_genuine_outer_directories'][:];captured=[]
for z in hcaps:
    for t in z['members']:add(t)
    q=R/z['capture']['path'];v=json.loads(raw(q));assert v==z['complete_capture'] and v['status']=='PASS' and v['exit_code']==0 and stat.S_IMODE(q.parent.stat().st_mode)==0o700
    outerdirs.append(dict(path=q.parent.relative_to(R).as_posix(),full_mode=0o700));captured.append(dict(capture=ref(q),entire_capture=v))
for name,pid in [('root_pr48_v5_SOURCE_close_actual_capture',31203),('root_pr48_v5_SOURCE_readback_actual_capture',31334)]:
    d=A.parent/'pr45_9900007'/name;assert {q.name for q in d.iterdir()}=={'CAPTURE.json','prelaunch_operator.py','stdout.bin','stderr.bin'} and stat.S_IMODE(d.stat().st_mode)==0o700
    for q in d.iterdir():add(ref(q))
    v=json.loads(raw(d/'CAPTURE.json'));assert v['schema']=='root-explicit-command-capture/v1' and v['pid']==pid and v['actual_execution'] is True and v['completed'] is True and v['status']=='PASS' and v['exit_code']==0 and v['operator_unchanged'] is True and v['operator_sha256']=='c1ae969ccbbc48ed6fb486e96184da94329291a46b27d2b891ecb87185c909ec'
    for channel in ['stdout','stderr']:
        z=v[channel];b=raw(d/z['path']);assert len(b)==z['bytes'] and hashlib.sha256(b).hexdigest()==z['sha256']
    assert json.loads(raw(d/'stdout.bin'))['source_manifest_sha256']==MF_SHA
    outerdirs.append(dict(path=d.relative_to(R).as_posix(),full_mode=0o700));captured.append(dict(capture=ref(d/'CAPTURE.json'),entire_capture=v))
assert hashlib.sha256(raw(P/'SOURCE_READY.json')).hexdigest()==SHA
ready=json.loads(raw(P/'SOURCE_READY.json'));assert ready['closure_payload_count']==27 and ready['closure_directory_count']==6 and ready['source_only'] is True and ready['proposed_code_executed'] is False and ready['actual_epoch_or_acceptance_approved'] is False
for z in ready['source_files']:assert {k:rows[z['path']][k] for k in z}==z
mapping=json.loads(raw(F/'COMPLETE_SOURCE_CHANGE_MAP.json'));assert len(mapping['complete_sources'])==9
for z in mapping['complete_sources']:assert ref(P/z['new'])['sha256']==z['complete_new_sha256']
assert all(z['full_residual_diff']=='' for z in mapping['complete_sources'] if z['new']!='epoch_common.py')
common=raw(P/'epoch_common.py').decode();assert common.count('actual_outer_parent(directory);')==2 and 'directory.parent==A' in common and 'directory.resolve(strict=True)==directory' in common and 'A.resolve(strict=True)==A' in common
assert not (A/'capture_root_command.py').exists() and not (A/'capture_root_command.py').is_symlink()
cap=json.loads(raw(F/'private_actual_capture/CAPTURE.json'));result=json.loads(raw(F/'private_actual_capture/stdout.json'));assert cap['pid']==result['actual_private_pid']==32756 and cap['operator_pid']==32755 and cap['exit_code']==0 and cap['status']=='PASS' and result['status']=='PASS_PRIVATE_MODELS_ONLY' and result['checks']==21
put('FIXED_INPUT_BINDINGS.json',dict(schema='pr48-v5-independent-fixed-source-and-historical-bindings/v1',observed_utc=NOW,fixed_rows_count=len(rows),fixed_rows=[rows[k] for k in sorted(rows)],exact_preserved_families=families,additional_genuine_outer_directory=old['additional_genuine_outer_directory'],additional_genuine_outer_directories=outerdirs,actual_closed_candidate_SOURCE_manifest=ref(P/'SOURCE_MANIFEST.json'),actual_closed_M4_evidence_SELF=ref(OLD/'SELF_MANIFEST.json'),complete_current_ROOT_SOURCE_and_M4_captures=captured,actual_A48_runtime_operator_absent_at_dated_review=True,operator_absence_is_not_future_authority=True,qualification='V5 dated27-file644 observation is retained in COMPLETE_SOURCE_CHANGE_MAP. Current genuine SOURCE27+self28 is444; its custody closure is not production approval. Prior V4/V3/V2 candidates stay unclosed644, prior adversarial closures stay444. No native/currentHEAD authority.'))
put('VERDICT.json',dict(schema='pr48-post-push-epoch-independent-SOURCE-verdict/v1',status='PASS_SOURCE_ONLY',utc=NOW,source_ready_sha256=SHA,mandatory_findings=[],production_executed=False,future_acceptance_approved=False,review_continuity='Same independent M1/M2/M3/M4 corrective investigator; no blind new math family or authority transfer.',M1_M2_M3_M4_repair_in_current_SOURCE_verified=True,exact_actual_outer_parent_identity_required=True,checked_current_candidate_payloads=27,current_ROOT_SOURCE_manifest_sha256=MF_SHA,fixed_input_bindings=len(rows),actual_private_controls=dict(caller_pid=32755,pid=32756,checks=21,capture='private_actual_capture/CAPTURE.json',whole_stdout_sha256=cap['stdout']['sha256'],whole_stderr_sha256=cap['stderr']['sha256']),original_science17_original_first3_and22_ROOT_contract_unchanged=True,mathematical_credit=0,source_review_completion_percent=100,actual_recovery_completion_percent=0,remaining_gap='ROOT full reading/own review-evidence closure and separate readback, then unchanged actual A48 operator copy/source-mode inspection, fresh per-role epochs and genuine final3/complete22 post. PR49 needs a separate corrected mixed-phase/source-mode consumer. No world literature or mathematical novelty clearance is asserted.'))
put('REPORT.md',f'''# PR48 corrective V5 independent SOURCE review

PASS_SOURCE_ONLY for READY`{SHA}`. No mandatory SOURCE finding remains in this bounded complete corrective audit. The actual same-parent guard repairs the independently reproduced M4 counterexample and preserves the live-source/full07777/retained-snapshot conditions. This is source consistency clearance only; no production, native, Git, remote, operator copy or ROOT approval was performed by this reviewer.

This is the same independent investigator continuing M1/M2/M3/M4, with explicit historical continuity and no blind new mathematical-family claim. Independent scope was declared in actual tool inputs4d6182/eab55c before implementation reading. The shell first failed ENOSPC before Python; the direct retry started Python but mkdir failed before any folder/file creation or private child. Both true failures are preserved in AUTHORING_FAILURES.json. Scope file was honestly saved after subsequent read-only implementation inspection, at17:40:51.986844UTC, when space became available. No pre-read saved-file/PID/time was invented and no foreign/system cleanup occurred here.

## Complete continuity and repair mechanism

All nine operative/closure source bodies were read as text and compared completely with V4 using explicit literal filename/path/schema substitutions. COMPLETE_SOURCE_CHANGE_MAP retains every count and full residual. Only common adds the M4 history member and actual_outer_parent, invoked first in retained and live operator bindings. All other eight have zero residual change; derived finalizer/mirror are byte-identical. Original acceptance_preparation_family_v3/native revision2/old genuine author paths are left literal. Every changed contract key is recorded, limited to versions and exact-parent/M4 history. READY, prose, private source/results, preparation/finalization authorship sources and closure sources were read; none of the candidate code was imported, compiled or executed.

Shared actual_outer_parent requires an absolute existing directory, exact `directory.parent==A48`, no symlink or symlink ancestors, canonical strict resolved identity of outer and A48, and A48parent0755 via the existing typed directory binding. operator_binding and live_operator_binding invoke it before acquisition. The retained source stays644/c1ae and outer700. The named actual source is the literal A48/capture_root_command.py644, entire2593B c1ae hash and bytes equal the retained644 snapshot. Therefore c1ae's actual source parent—the parent beside which it creates its outer—must coincide with the checked literal live source parent. An A45 outer cannot substitute. Author/caller contexts and inspector live context all share the requirement; existing before/after comparisons and current epoch/phase/readonly/runtime evidence reacquire it.

All actual actor/prelaunch/dependency bodies and full07777 modes remain bound. Exact own/source/prelaunch directories755, closed prepared files/self444, actual source/operator644 and genuine outer700 remain separate roles. Same-parent mode600/2644/4644, parent/outer special bits, entire snapshot substitution, typed bool/float mode, lexical traversal and symlink outer are refused. No broad exemption, old capture rewrite, hidden predicate replacement or retroactive first-three mode assertion is introduced. Boundary checks assert those observations; they do not claim continuous observation between reads.

## Genuine independent controls and custody

Actual own caller32755/handwritten child32756 exited0 at2026-10-03T17:42:46.045844–17:42:46.084454UTC. Its21 directly relevant independent checks accept the exact same-parent combined context for author/caller/inspector and reject the old other-parent variants600/2644/4644 plus the direct fullmode/body/canonical cases above. Full prelaunch source/operator/argv/PIDs/UTC, stdout3635B SHA`{cap['stdout']['sha256']}` and empty stderr are retained. Neither candidate nor c1ae was run; only private fixture modes/bodies changed and were restored644/755, with the temporary symlink removed. The preparer's separate17 controls were read as their declared finite private-model evidence, not promoted as execution of production. No further unrelated test corpus was added.

The17:39:08.482152UTC complete source observation honestly records V5 as27 unclosed644 files/6relative755 dirs and no MF. ROOT then genuinely closed only that SOURCE in child31203 at17:40:38 and separately read it in31334 at17:40:50. Current MF`{MF_SHA}` binds27payload+self28, all444, sixrelative/root dirs755. Their complete CAP4 bodies/streams/modes are bound separately, without rewriting the old observation. Likewise genuine M4 evidence21+self22 MF86c38790…/children19625/19768 and previous M3 proof/controls remain closed444 adverse history; rejected24V4/V3/old45V2 remain unclosed644. No historical PASS or custody closure is future runtime authority. FIXED_INPUT_BINDINGS has{len(rows)} unique full-body/fullmode rows and strict family topology/modes, bound in place without duplicating bodies or foreign/native live hashes.

## Unchanged science and exact remaining gap

Original closed53/self9c525f7b, original17 scientific pins, genuine successful old3 phase receipts, actual merge209581a4627b01745974837fe7adab62ab8c0af7 and honest failed19622 history remain exact. Outcome is still ordinary UNSOLVED2961/related30004403/sharedoriginal2/5,new0/audit0: product-subgroup4/allpowers and qualified averaging obstruction only. This audit contributes no mathematics, novel resolution, alias-native event, paper, DOI, tracker or human-peer-review claim. Original22-key scientific ROOT contract26f89f5e remains unchanged.

Per-role descendantHEAD, whole clean index, complete current tracked foreign body/fullmode preservation, original other12 native bodies/all13 modes, whole QUEUE authentication with accepted target/absent alias/unrelated-row preservation, exact two logs and prescribed inventory/state/history effects remain unchanged. Absent-only finalization and honest failure recovery still forbid blind reruns; post-mirror/epoch drift refuses. The final3 must be genuine distinct V5 source/operator/argv/dependency/fullstream receipts in order with old3, followed by full22 ROOT post inspection; no count-only or documentary-helper substitution passes.

A48/capture_root_command.py was actually absent at this dated review. ROOT must copy unchanged c1ae2593B0644 there, independently inspect it and use only that parent for every actual outer role. Absence is a dated observation, not a future closure constraint. Actual epochs/final3/complete22 post and PR49's separately reviewed mixed-six/source-mode consumer remain unperformed here. Source audit100%; actual recovery0%; mathematical discovery0%. Own evidence closer/separate reader are unexecuted proposals, never ROOT approval or candidate production actions.
''')
put('RESEARCH_LOG.md',NOW+' — Complete V5 corrective SOURCE review PASS_SOURCE_ONLY. Nine sources fully compared with explicit normalization; sole substantive parent predicate repairs M4 without scientific/native/foreign relaxation. Actual independent32755/32756 exit0,21 bounded checks, source only. Both actual pre-read ENOSPC failures retained honestly. Dated644 observation retained separately from genuine ROOT27+self444 closure31203/read31334. Strongest verified result: clean bounded operational source consistency, no production authority. Source review100%; actual recovery0%; discovery0%.\n')
for original,new in [('closure_common.py','closure_common.py'),('close_adverse_family.py','close_review_family.py'),('verify_closed_adverse_family.py','verify_closed_review_family.py')]:
    s=raw(OLD/original).decode().replace('corrective_source_adversary_v4','corrective_source_adversary_v5').replace('pr48-corrective-v4-adverse','pr48-corrective-v5-review').replace('4a2ca334cfea92fb44dfebb874de8d4b0827292b0ab3fb7e82a57de3b8746771',SHA).replace('REPAIR_REQUIRED_SOURCE','PASS_SOURCE_ONLY').replace('ADVERSE_EVIDENCE','REVIEW_EVIDENCE').replace('adverse','review').replace('Adverse','Review')
    if original=='closure_common.py':s=s.replace('==len(rows)==229','==len(rows)=='+str(len(rows))).replace("==['M4']","==[]")
    put(new,s)
names=sorted(q.relative_to(F).as_posix() for q in F.rglob('*') if q.is_file());dirs=sorted(['.']+[q.relative_to(F).as_posix() for q in F.rglob('*') if q.is_dir()]);assert all(not q.is_symlink() and (q.is_file() or q.is_dir()) for q in F.rglob('*'));assert all(stat.S_IMODE((F/n).stat().st_mode)==0o644 for n in names) and all(stat.S_IMODE((F/d).stat().st_mode)==0o755 for d in dirs);assert set(dirs)=={'.'}|{d.as_posix() for n in names for d in PurePosixPath(n).parents}
def own(n):return {k:v for k,v in ref(F/n).items() if k!='full_mode'}|{'path':n}
put('READY.json',dict(schema='pr48-corrective-v5-review-readiness/v1',utc=NOW,status='READY_FOR_ROOT_SOURCE_REVIEW_EVIDENCE_READING_AND_CLOSURE_ONLY',source_only=True,production_executed=False,future_acceptance_approved=False,candidate_source_ready_sha256=SHA,candidate_SOURCE_manifest_sha256=MF_SHA,candidate_closure_genuinely_complete=True,closure_payload_files=sorted(names+['READY.json']),closure_directory_names=dirs,fixed_own_files=[own(n) for n in names],ROOT_closer_argv=['/usr/bin/python3','-B',str(F/'close_review_family.py'),'--execute','--personally-read-complete-source','--ready-sha256','ACTUAL_READY_SHA'],ROOT_reader_argv=['/usr/bin/python3','-B',str(F/'verify_closed_review_family.py'),'--self-manifest-sha256','ACTUAL_ROOT_CLOSED_SELF_SHA'],own_closer_and_reader_executed=False,no_self_manifest_authored=True,mandatory_findings=[],source_review_completion_percent=100,actual_recovery_percent=0,mathematical_credit=0,qualification='Independent same-reviewer corrective continuity; clean SOURCE only, no ROOT approval or production authority. Exact current295 custody rows; no mutable native/HEAD freshness transfer.'))
print(json.dumps(dict(status='READY_PASS_SOURCE_ONLY_V5',actual_author_pid=os.getpid(),utc=NOW,fixed_rows=len(rows),payload_count=len(names)+1,relative_dirs=len(dirs)-1,READY=ref(F/'READY.json'),REPORT=ref(F/'REPORT.md'),VERDICT=ref(F/'VERDICT.json'),common=ref(F/'closure_common.py'),closer=ref(F/'close_review_family.py'),reader=ref(F/'verify_closed_review_family.py')),indent=2))
