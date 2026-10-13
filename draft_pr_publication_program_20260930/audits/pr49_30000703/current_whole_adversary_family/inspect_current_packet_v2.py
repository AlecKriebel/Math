"""Bounded read-only current packet audit. Reads bodies in place; writes only own ledger."""
from pathlib import Path
import json, os, stat, hashlib
from datetime import datetime, timezone
F=Path(__file__).resolve().parent; R=F.parents[3]; A=F.parent; C=A/'reviewed_candidate'; A45=A.parent/'pr45_9900007'
EXPECTED='8ca8820e1e1493391224ea8f93dde859bd9b3f6316c41763e86433dc85a1fa47'
rows={}; parse_count=0
def check(p, expected=None):
    p=Path(p)
    assert p.is_absolute() and p.is_relative_to(R)
    for v in [p,*p.parents]:
        if v == R.parent: break
        assert not v.is_symlink(), str(v)
    s=p.lstat(); assert stat.S_ISREG(s.st_mode),str(p)
    key=str(p.relative_to(R))
    if key not in rows:
        b=p.read_bytes(); rows[key]={'path':key,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'full_mode':stat.S_IMODE(s.st_mode)}
        assert p.lstat().st_mode==s.st_mode and p.lstat().st_size==len(b)
    row=rows[key]
    if expected:
        for k in ['bytes','sha256','full_mode']:
            if k in expected: assert type(expected[k]) is type(row[k]) and row[k]==expected[k],(key,k,row[k],expected[k])
    return row
def obj(p):
    global parse_count
    check(p); b=p.read_bytes(); parse_count+=1
    return json.loads(b)
def normalized(v): return {k:v[k] for k in ['path','bytes','sha256','full_mode']}
def tree(p):
    files=[]; dirs=[]
    for root, ds, fs in os.walk(p,followlinks=False):
        for n in ds:
            q=Path(root)/n; assert stat.S_ISDIR(q.lstat().st_mode) and not q.is_symlink(); dirs.append(str(q.relative_to(p)))
        for n in fs:
            q=Path(root)/n; assert stat.S_ISREG(q.lstat().st_mode) and not q.is_symlink(); files.append(str(q.relative_to(p)))
    return sorted(files),sorted(dirs)
check(C/'MANIFEST.json',{'sha256':EXPECTED,'full_mode':0o444})
m=obj(C/'MANIFEST.json'); assert m['files_count']==1544 and len(m['files'])==1544
assert len({v['path'] for v in m['files']})==1544
payload=[]
for v in m['files']:
    assert type(v['path']) is str and not Path(v['path']).is_absolute() and '..' not in Path(v['path']).parts
    assert v['full_mode']==0o444
    q=C/v['path']; payload.append(check(q,v))
    if q.suffix in ['.json','.jsonl']:
        b=q.read_bytes()
        if q.suffix=='.json': json.loads(b); parse_count+=1
        elif b.strip():
            try: json.loads(b); parse_count+=1
            except json.JSONDecodeError:
                for line in b.splitlines():
                    if line.strip(): json.loads(line); parse_count+=1
files, dirs=tree(C)
assert files==sorted([v['path'] for v in m['files']]+['MANIFEST.json'])
d=obj(C/'CURRENT_DEPENDENCIES.json'); assert len(d['files'])==1407
assert len({v['path'] for v in d['files']})==1407
dependencies=[check(R/v['path'],v) for v in d['files']]
root=obj(A/'ROOT_ACTUAL_CURRENT_FREEZE_INSPECTION.json')
assert root['schema']=='pr49-root-actual-complete-current-freeze-inspection/v1'
assert root['actual_inspection_pid']==50553 and root['status']=='PASS_ROOT_COMPLETE_ACTUAL_CURRENT_FREEZE_EVIDENCE_ONLY'
assert root['candidate_manifest']==check(C/'MANIFEST.json')
assert root['complete_current_payload']==payload
assert root['exact_relative_directories']==dirs and len(dirs)==273
assert root['complete_dependencies']==dependencies
assert root['new_whole_current_gate']=='PENDING'
assert all(root[k] is False for k in ['whole_review_or_acceptance_approved','future_acceptance_approved','project_solved','novelty_claimed','paper','DOI','tracker'])
for k in ['complete_outer_members','complete100_inner_streams']:
    for v in root[k]: check(R/v['path'],v)
inner_path=R/root['original_inner_record']['path']; check(inner_path,root['original_inner_record']); inner=obj(inner_path)
frozen=obj(C/'build/actual_attempt_prepublication_prefix/GIT_COMMANDS.json')
assert len(inner)==50 and len(frozen)==48 and inner[:48]==frozen and root['entire_final_original_inner_commands']==inner
def dt(v): return datetime.fromisoformat(v)
outer_path=A/'tmp/root_pr49_current_outer_20261003T081806.986644Z'; outer=obj(outer_path/'CAPTURE.json')
assert outer==root['entire_actual_outer_capture']
assert outer['operator_pid']==47574 and outer['pid']==47575 and outer['exit_code']==0 and outer['completed'] is True
assert json.loads((outer_path/'stdout.bin').read_bytes())==root['entire_outer_stdout_object']
for v in inner:
    assert v['completed'] is True and v['actual_execution'] is True and type(v['pid']) is int and v['exit_code']==0
    assert dt(outer['started_utc'])<=dt(v['started_utc'])<=dt(v['finished_utc'])<=dt(outer['finished_utc'])
    for k in ['stdout','stderr']: check(inner_path.parent/v[k]['path'],v[k])
assert hashlib.sha256((outer_path/'PRELAUNCH_BUILDER_SOURCE.py').read_bytes()).hexdigest()==outer['builder_sha256']
assert hashlib.sha256((outer_path/'PRELAUNCH_OPERATOR.py').read_bytes()).hexdigest()==outer['operator_sha256']
captures=[]
def cap4(p,expected_pid=None,expected_exit=0):
    q=obj(p/'CAPTURE.json')
    assert q['actual_execution'] is True and q['completed'] is True and q['exit_code']==expected_exit
    assert type(q['pid']) is int and (expected_pid is None or q['pid']==expected_pid)
    assert dt(q['started_utc'])<dt(q['finished_utc'])
    own=[]
    for n in ['CAPTURE.json','prelaunch_operator.py','stdout.bin','stderr.bin']: own.append(check(p/n))
    assert check(p/'prelaunch_operator.py')['sha256']==q['operator_sha256']
    for k in ['stdout','stderr']: check(p/q[k]['path'],q[k])
    captures.append({'capture':str((p/'CAPTURE.json').relative_to(R)),'pid':q['pid'],'exit_code':q['exit_code'],'members':own})
    return q
root_outer=cap4(A45/'root_pr49_current_freeze_actual_capture',47574)
assert dt(root_outer['started_utc'])<=dt(outer['started_utc'])<=dt(outer['finished_utc'])<=dt(root_outer['finished_utc'])
inspect=cap4(A45/'root_pr49_actual_current_freeze_inspection_v3_capture',50553)
assert dt(outer['finished_utc'])<dt(inspect['started_utc']) and dt(root['created_utc'])<=dt(inspect['finished_utc'])
for n,pid in [('root_pr49_actual_current_freeze_inspection_capture',49453),('root_pr49_actual_current_freeze_inspection_v2_capture',49723)]: cap4(A45/n,pid,1)
new_path=R/root['new_SOURCE_record']['path']; check(new_path,root['new_SOURCE_record']); new=obj(new_path)
assert check(new_path)['sha256']=='9b669194d6e083b0a55d062bb08718fde55869d866182e38476b9afeeebf07fd'
assert new['closed_clean'] is True and new['mandatory_corrections']==[] and new['future_acceptance_approved'] is False
assert new['new_whole_current_gate']=='PENDING' and len(new['normalized_complete_owned_body_mode_rows'])==74
for k in ['normalized_complete_owned_body_mode_rows','individual_complete_external_bindings','normalized_postclosure_final_own_rows']:
    for v in new[k]: check(R/v['path'],v)
check(R/new['manifest']['path'],new['manifest']); sm=obj(R/new['manifest']['path'])
assert sm==new['complete_source_adversary_manifest_object'] and sm['files_count']==74
sf=R/new['manifest']['path']; sf_files,sf_dirs=tree(sf.parent)
assert sf_files==sorted([v['path'] for v in sm['files']]+[sf.name]) and sf_dirs==sm['directories']
assert all(v['full_mode']==0o444 for v in new['normalized_complete_owned_body_mode_rows']) and check(sf)['full_mode']==0o444
for v in new['complete_actual_SOURCE_and_adversary_closure_readback_captures']:
    for w in v['complete_members']: check(R/w['path'],w)
    cq=v['complete_capture']; assert cq['actual_execution'] is True and cq['completed'] is True and cq['exit_code']==0
    cp=R/v['complete_members'][0]['path']; assert obj(cp)==cq
    assert json.loads((cp.parent/'stdout.bin').read_bytes())==v['complete_stdout_object']
check(R/root['actual_ROOT_prerequisite_authoring_capture']['path'],root['actual_ROOT_prerequisite_authoring_capture'])
author=cap4(A45/'root_pr49_current_prerequisites_authoring_actual_capture',47212)
assert dt(author['finished_utc'])<dt(root_outer['started_utc'])
original=obj(C/'original_snapshot_manifest.json'); assert original['original_files']==16
literal=[]
for v in original['files']:
    q=C/'original_archive'/v['relative_path']; check(q,v)
    original_source=A/'source_snapshot'/v['relative_path']; check(original_source,{'bytes':v['bytes'],'sha256':v['sha256'],'full_mode':0o444})
    assert q.read_bytes()==original_source.read_bytes(); literal.append(v['relative_path'])
operative=['SOURCE_STATUS.md','verify.py','review/submitted_verify.py','review/independent_checks.py','review/verification.json','review/independent_results.json','source_record.json','prior_report.json','turns.json','source_checksums.json','verification.json']
operative=list(dict.fromkeys(operative))
for n in operative: assert (C/n).read_bytes()==(C/'original_archive'/n).read_bytes(),n
assert (C/'prior_report.json').read_bytes()==b'null\n'
turns=obj(C/'turns.json'); assert type(turns['count']) is int and turns['count']==0 and turns['substantive_attempts']==[]
assert 'source_verification_response' not in turns
assert type(obj(C/'source_record.json')['id']) is int and obj(C/'source_record.json')['id']==30000703
patch=obj(C/'CURRENT_QUEUE_PATCH.json'); assert patch['target_ids']==[30000703] and patch['allowed_named_changes']==['Status','Turns','Findings']
native4=['draft_pr_publication_program_20260930/inventory.json','unsolved_math_prioritization/QUEUE.md','unsolved_math_prioritization/history.jsonl','unsolved_math_prioritization/state.json']
input_by_path={v['path']:v for v in d['current_native13']}
for n in native4:
    pre=C/'native4_proposal/preimage'/n.replace('/','__'); post=C/'native4_proposal/prospective'/n.replace('/','__')
    check(pre,input_by_path[n]); check(post)
    if n.endswith('QUEUE.md'):
        pre_b=pre.read_bytes(); post_b=post.read_bytes(); ch=patch['changes']; assert len(ch)==1
        before=ch[0]['row_before'].encode(); after=ch[0]['row_prospective'].encode()
        assert pre_b.count(before)==1 and post_b==pre_b.replace(before,after,1)
        assert hashlib.sha256(post_b).hexdigest()==patch['whole_prospective_sha256']
        h=next(v for v in pre.read_text().splitlines() if '| Status |' in v and '| Turns |' in v).split('|')
        b=before.decode().rstrip('\n').split('|'); a=after.decode().rstrip('\n').split('|'); assert len(h)==len(a)==len(b)
        assert {h[i].strip() for i in range(len(h)) if a[i]!=b[i]}<={'Status','Turns','Findings'}
    else: assert pre.read_bytes()==post.read_bytes(),n
stable=[]
for v in d['current_native13']:
    if v['path'] not in native4: stable.append(check(R/v['path'],v))
assert len(stable)==9
status=obj(C/'status.json'); assert status['status']=='already_solved'
result={'schema':'pr49-current-whole-in-place-read-ledger/v1','status':'PASS_BOUNDED_CURRENT_PACKET_FULL_BODY_AND_MODE_READ','actual_pid':os.getpid(),'created_utc':datetime.now(timezone.utc).isoformat(), 'candidate_manifest':check(C/'MANIFEST.json'),'payload_count':1544,'relative_directories':dirs,'dependency_count':1407,'full_body_mode_rows':sorted(rows.values(),key=lambda v:v['path']),'JSON_objects_parsed':parse_count,'actual_final_inner_commands':50,'honest_frozen_inner_prefix':48,'complete_actual_caps':captures,'original_archive_literals':literal,'operative_literals':operative,'stable9':stable,'native4_status':'Frozen dated proposals checked; no live acceptance authority or native writes','original_attempts':0,'new_attempts':0,'audit_turns':0,'imported_journal_proof_independently_certified':False,'unrelated_SQL_or_mode_probe_rerun':False,'production_imported_compiled_executed':False,'future_acceptance_approved':False}
(F/'CURRENT_READ_LEDGER.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['status','actual_pid','payload_count','dependency_count','JSON_objects_parsed','actual_final_inner_commands','honest_frozen_inner_prefix']}))
