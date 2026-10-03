"""ROOT's genuine closed whole-current inspection, after personal report reading."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import stat

A=Path(__file__).resolve().parent
R=A.parents[2]
F=A/'whole_current_source_first_family'
PIN='af80fc4d9ce1bb3b282b193f8dbe3dfdd873184f7ffb1143c6b027419f6a0c2d'
def sha(raw):return hashlib.sha256(raw).hexdigest()
def pairs(rows):
    o={}
    for k,v in rows:
        if k in o:raise ValueError('Duplicate JSON key')
        o[k]=v
    return o
def parse(raw):return json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda s:(_ for _ in ()).throw(ValueError(s)))
def read(p,digest=None,size=None):
    assert p.is_file() and not p.is_symlink() and all(not q.is_symlink() for q in p.parents)
    assert p.resolve(strict=True).is_relative_to(R.resolve())
    raw=p.read_bytes()
    if digest is not None:assert sha(raw)==digest
    if size is not None:assert type(size) is int and len(raw)==size
    return raw
def clock(value):
    t=dt.datetime.fromisoformat(value.replace('Z','+00:00'))
    assert t.utcoffset()==dt.timedelta(0)
    return t
assert __debug__ and os.environ.get('PYTHONOPTIMIZE','') in ('','0')
source=Path(__file__).read_bytes()
with (A/'ROOT_CLOSED_WHOLE_INSPECTION_PRELAUNCH_SOURCE.py').open('xb') as f:f.write(source)
mf=parse(read(F/'SELF_MANIFEST.json',PIN))
assert mf['schema']=='PR43_NEW_WHOLE_CURRENT_SOURCE_FIRST_SELF_ONLY_CLOSURE_v1'
assert mf['files_count']==len(mf['files'])==30 and mf['self_excluded']==['SELF_MANIFEST.json']
names={z['path'] for z in mf['files']}|{'SELF_MANIFEST.json'}
assert len(names)==31
assert {p.relative_to(F).as_posix() for p in F.rglob('*') if p.is_file()}==names
dirs={p.relative_to(F).as_posix() for p in F.rglob('*') if p.is_dir()}
assert dirs=={q.as_posix() for n in names for q in Path(n).parents if str(q)!='.'}==set(mf['directories'])
assert not any(p.is_symlink() for p in F.rglob('*'))
own_bytes=0
for z in mf['files']:
    raw=read(F/z['path'],z['sha256'],z['bytes']);own_bytes+=len(raw)
    assert z['mode']=='0444' and stat.S_IMODE((F/z['path']).stat().st_mode)==0o444
    if z['path'].endswith('.json'):parse(raw)
assert stat.S_IMODE((F/'SELF_MANIFEST.json').stat().st_mode)==0o444
foreign=mf['external_individually_excluded_inputs']
assert len(foreign)==len({z['path'] for z in foreign})==756
foreign_bytes=0
for z in foreign:
    p=Path(z['path']);assert p.is_absolute() and not p.resolve().is_relative_to(F.resolve())
    foreign_bytes+=len(read(p,z['sha256'],z['bytes']))
verdict=parse(read(F/'VERDICT.json','335da7b6ebb0d797e8b800b93f12b9acf6a96fc3f6a7ad966d784898a583a1c1'))
read(F/'FINAL_REPORT.md','5238f776e1228616b93e416ccc97ed3632296f8f319a7509217072e14733b706')
assert verdict['verdict']=='PASS_EXACT_FROZEN_CURRENT_PACKET_FOR_CREDITED_SOURCE_STATUS_ACCEPTANCE'
assert verdict['mandatory_defects']==[] and verdict['source_or_packet_repair_required'] is False and verdict['mathematical_gap'] is None
assert verdict['justified_status']=='already_solved' and verdict['full_target_resolved_in_prior_published_literature'] is True
assert verdict['prior_publication_doi']=='10.4064/sm210413-16-9'
assert verdict['full_problem_solved_by_project'] is verdict['novelty_claimed'] is verdict['priority_claimed'] is False
assert verdict['candidate_manifest_sha256']=='4849e6037a5db3dce546a656dcd57063ae83d782c19e24d4e3dff97ebbcdec14'
assert verdict['original_substantive_attempts']==verdict['new_substantive_attempts']==verdict['audit_turns']==0
assert verdict['ROOT_final_reconciliation_integration_merge_certified'] is False
captures=[]
for folder,pid,source_name in [('actual_whole_inspection_001',72547,'PRELAUNCH_READER.py'),('actual_acceptance_controls_001',78301,'PRELAUNCH_SOURCE.py'),('actual_supplement_001',82888,'PRELAUNCH_SOURCE.py')]:
    cap=parse(read(F/folder/'CAPTURE.json'))
    assert cap['actual_child_pid']==pid and cap['exit_code']==0 and cap['capture_complete_after_child_exit'] is True
    assert clock(cap['actual_start_utc'])<=clock(cap['actual_end_utc'])<=dt.datetime.now(dt.timezone.utc)
    read(F/folder/source_name,cap.get('prelaunch_reader_sha256',cap.get('prelaunch_source_sha256')))
    read(F/folder/'PRELAUNCH_OPERATOR.py',cap['prelaunch_operator_sha256'])
    for channel in ['stdout','stderr']:
        z=cap[channel];read(Path(z['path']),z['sha256'],z['bytes'])
    captures.append(cap)
obj={'schema':'pr43-root-complete-closed-whole-inspection/v1','status':'PASS_ROOT_COMPLETE_CLOSED_WHOLE_INSPECTION','created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'candidate_manifest_sha256':verdict['candidate_manifest_sha256'],'closed_whole_manifest_sha256':PIN,'first_party_members':30,'individually_bound_foreign_inputs':756,'complete_VERDICT_object':verdict,'personal_report_and_verdict_fully_read':True,'all_first_party_whole_bytes_and_modes_checked':True,'all_foreign_individual_whole_bytes_checked':True,'exact_self_only_recursive_closure_checked':True,'complete_actual_captures_checked':captures,'mandatory_defects':[],'mandatory_corrections':[],'original_substantive_attempts':0,'new_substantive_attempts':0,'audit_turns':0,'full_target_resolved_in_prior_published_literature':True,'full_problem_solved_by_project':False,'future_execution_approved':False}
with (A/'ROOT_WHOLE_CURRENT_REVIEW.json').open('x') as f:json.dump(obj,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
assert Path(__file__).read_bytes()==source
print(json.dumps({'status':obj['status'],'own_member_bytes':own_bytes,'foreign_input_bytes':foreign_bytes,'first_party_members':30,'foreign_inputs':756,'actual_pid':os.getpid(),'future_execution_approved':False}))
