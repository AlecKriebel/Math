"""ROOT checks both closed families and closes only its actual reproduction evidence."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import stat

A=Path(__file__).resolve().parent
R=A.parents[2]
D=A/'root_original_actual_reproduction'
def sha(raw):return hashlib.sha256(raw).hexdigest()
def load(p):return json.loads(p.read_bytes())
def pin(p,base=R):
    raw=p.read_bytes();return {'path':p.relative_to(base).as_posix(),'bytes':len(raw),'sha256':sha(raw)}
def check(base,z,frozen=False):
    p=base/z['path'];assert p.is_file() and not p.is_symlink() and all(not q.is_symlink() for q in p.parents)
    assert p.resolve().is_relative_to(R.resolve())
    raw=p.read_bytes();assert len(raw)==z['bytes'] and sha(raw)==z['sha256']
    if frozen:assert stat.S_IMODE(p.stat().st_mode)==0o444
    return raw
assert __debug__ and os.environ.get('PYTHONOPTIMIZE','') in ('','0')
source=Path(__file__).read_bytes()
(D/'ROOT_CLOSURE_PRELAUNCH_SOURCE.py').write_bytes(source)
family_rows=[]
for name,mname,pin_value,count in [('duality_algebra_family','AUTHORSHIP_MANIFEST.json','83dcad444a56274472224bbb58dec268ded92ac2042ddabe8fee7851626acb81',54),('literal_realization_family','SELF_ONLY_CLOSURE.json','6e656761b9c7938aa8901157706dcf9587e627903ee0dbac1b20eaa2be0dea40',13)]:
    F=A/name;assert sha((F/mname).read_bytes())==pin_value
    mf=load(F/mname);owned=mf['files'] if name=='duality_algebra_family' else mf['authored_members'];assert len(owned)==count
    own_names={z['path'] for z in owned}|{mname};assert len(own_names)==count+1
    for z in owned:check(F,z,True)
    assert stat.S_IMODE((F/mname).stat().st_mode)==0o444
    if name=='duality_algebra_family':
        foreign=mf['foreign_local_members_individually_excluded'];external=mf['external_parent_original_inputs'];assert len(foreign)==10 and len(external)==20
        for z in external:check(Path('/'),{**z,'path':z['path'].lstrip('/')})
    else:
        ref=mf['foreign_members_manifest'];assert sha((F/ref['path']).read_bytes())==ref['sha256'];foreign=load(F/ref['path'])['foreign_evidence'];assert len(foreign)==54
    for z in foreign:check(F,z)
    actual={p.relative_to(F).as_posix() for p in F.rglob('*') if p.is_file()}
    assert actual==own_names|{z['path'] for z in foreign}
    assert not any(p.is_symlink() for p in F.rglob('*'))
    dirs={p.relative_to(F).as_posix() for p in F.rglob('*') if p.is_dir()}
    assert dirs=={q.as_posix() for n in actual for q in Path(n).parents if str(q)!='.'}
    family_rows.append({'family':name,'manifest':pin(F/mname),'owned_members':count,'individually_checked_foreign_local_members':len(foreign),'exact_topology_checked':True})
diff=(A/'original_diff_v2.patch').read_bytes();assert len(diff)==75046 and sha(diff)=='e5f892ccda9e0202e97a98c045481c92b04d2291d5ae3c5a21d05e7e3c417f3b'
sections=diff.split(b'diff --git ')[1:];assert len(sections)==19
reconstructed=[]
for part in sections:
    header=part.splitlines()[0];path=header.split(b' b/',1)[1].decode()
    if path=='unsolved_math_prioritization/QUEUE.md':continue
    prefix='unsolved_math_prioritization/attempts/2912/';assert path.startswith(prefix)
    name=path[len(prefix):];lines=part.splitlines(keepends=True)
    added=b''.join(line[1:] for line in lines if line.startswith(b'+') and not line.startswith(b'+++'))
    assert b'new file mode 100644\n' in part and added==(A/'source_snapshot_v2'/name).read_bytes()
    reconstructed.append(name)
assert len(set(reconstructed))==18
outer_refs=[]
for old,label,pid,code in [('root_original_helper_reproduction_v2_actual_capture','actual_helper_outer_capture',9267,0),('root_full_raw_SQL_audit_actual_capture','actual_raw_SQL_outer_capture',11267,0),('root_original_helper_reproduction_actual_capture','failed_first_helper_wrapper_capture',7400,1)]:
    F=A/old;cap=load(F/'CAPTURE.json');assert cap['schema']=='root-explicit-command-capture/v1' and cap['pid']==pid and cap['exit_code']==code and cap['actual_execution'] is True and cap['completed'] is True
    for k in ['stdout','stderr']:check(F,cap[k])
    assert sha((F/'prelaunch_operator.py').read_bytes())==cap['operator_sha256']
    target=D/label;target.mkdir(exist_ok=False)
    for p in F.iterdir():assert p.is_file() and not p.is_symlink();(target/p.name).write_bytes(p.read_bytes())
    if code==0:outer_refs.append(pin(target/'CAPTURE.json',A))
repro=load(D/'ROOT_REPRODUCTION_RESULT.json');raw=load(D/'ROOT_RAW_SQL_AUDIT.json')
assert repro['all_three_entire_outputs_byte_exact'] is True and raw['all_entire_payload_and_prior_objects_type_sensitive_equal'] is True
ledger=(A/'source_snapshot_v2/turns.jsonl').read_bytes();whole_ledger=[json.loads(z) for z in ledger.splitlines()]
summary={'schema':'PR44_ROOT_CURRENT_REPRODUCTION_SUMMARY_v1','actual_reproductions_completed':True,'entire_author_result':repro['author_result'],'entire_independent_result':repro['independent_result'],'author_receipt_byte_exact':True,'independent_receipt_byte_exact':True,'full_original18_verified':True,'whole_original_ledger':whole_ledger,'finite_checks_do_not_prove_geometric_realization_or_full_problem':True,'whole_raw_bytes':raw['whole_raw_and_prior_bytes'],'whole_SQL_rows':raw['SQL_rows'],'prior_raw_key_present':raw['raw_prior_key_present'],'original_substantive_attempts':2,'new_substantive_attempts':0,'audit_turns':0,'actual_replay_captures':outer_refs,'actual_capture_scope_qualification':'Two genuine C1 outer captures: combined unchanged author/submitted/independent arithmetic runs and the full raw/SQL source comparison. All three inner actual captures and the full result objects remain separately retained. The copies here are byte-exact archives of actual earlier captures, not claims of earlier first-save time. The failed ROOT7400 wrapper launched no original helper.','entire_three_helper_result_record':pin(D/'ROOT_REPRODUCTION_RESULT.json',A),'entire_raw_SQL_record':pin(D/'ROOT_RAW_SQL_AUDIT.json',A),'full_original19_path_diff_and18_new_hunks_verified':True,'new_independent_families':family_rows,'historical_execution_or_human_review_certified':False}
(D/'ROOT_CURRENT_REPRODUCTION_SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
rows=[pin(p,D) for p in sorted(D.rglob('*')) if p.is_file()]
mf={'schema':'pr44-root-original-reproduction/v1','created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_closure_pid':os.getpid(),'original_head':'c772dc5b851ec91da9d46d534577609e5d3ca389','source_snapshot_manifest_sha256':'75f21617c7bdc192a0a64b76de4c1deec7ecc04d35bb93cf885ec11deb542b1d','original_substantive_attempts':2,'new_substantive_attempts':0,'audit_turns':0,'files_count':len(rows),'files':rows,'self_excluded':['MANIFEST.json'],'foreign_original_cache_inputs_individually_pinned_not_copied':raw['foreign_original_cache_inputs_individually_pinned_not_copied']}
(D/'MANIFEST.json').write_text(json.dumps(mf,indent=2)+'\n')
for p in D.rglob('*'):
    if p.is_file():p.chmod(0o444)
for z in rows:check(D,z,True)
assert stat.S_IMODE((D/'MANIFEST.json').stat().st_mode)==0o444 and Path(__file__).read_bytes()==source
print(json.dumps({'status':'PASS_ROOT_CLOSED_REPRODUCTION_AND_BOTH_FAMILY_INSPECTIONS','actual_pid':os.getpid(),'owned_reproduction_members':len(rows),'manifest':pin(D/'MANIFEST.json'),'summary':pin(D/'ROOT_CURRENT_REPRODUCTION_SUMMARY.json'),'families':family_rows,'all_original18_diff_hunks_reconstructed':True,'full_target_solved':False}))
