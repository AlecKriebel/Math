"""ROOT independently reads the actual completed PR49 outer/final inner evidence."""
from pathlib import Path,PurePosixPath
import datetime as dt, hashlib,json,os,stat,sys
R=Path('/Users/alec/Documents/Math');A=Path(__file__).absolute().parent;F=A/'reviewed_candidate'
assert __debug__ and not sys.flags.optimize
def raw(p):
    assert not p.is_symlink() and all(not q.is_symlink() for q in p.parents) and stat.S_ISREG(p.stat().st_mode)
    return p.read_bytes()
def sha(b):return hashlib.sha256(b).hexdigest()
def loadbytes(b):
    def pairs(items):
        d={}
        for k,v in items:assert k not in d;d[k]=v
        return d
    def bad(v):raise ValueError(v)
    return json.loads(b,object_pairs_hook=pairs,parse_constant=bad)
def load(p):return loadbytes(raw(p))
def ref(p):
    b=raw(p);return dict(path=p.relative_to(R).as_posix(),bytes=len(b),sha256=sha(b),full_mode=stat.S_IMODE(p.stat().st_mode))
def safe(n):
    assert type(n) is str and n and PurePosixPath(n).as_posix()==n and not PurePosixPath(n).is_absolute() and not {'.','..','.git','__pycache__'}.intersection(PurePosixPath(n).parts)
    return n
mf=load(F/'MANIFEST.json')
assert sha(raw(F/'MANIFEST.json'))=='8ca8820e1e1493391224ea8f93dde859bd9b3f6316c41763e86433dc85a1fa47'
assert mf['schema']=='pr49-strict-current-packet/v1' and mf['self_excluded']==['MANIFEST.json'] and mf['files_count']==len(mf['files'])==1544 and mf['full_permission_mode']=='0444'
owned=[]
for r in mf['files']:
    assert set(r)=={'path','bytes','sha256'} and type(r['bytes']) is int
    p=F/safe(r['path']);b=raw(p);assert len(b)==r['bytes'] and sha(b)==r['sha256'] and stat.S_IMODE(p.stat().st_mode)==0o444
    if p.suffix=='.json':loadbytes(b)
    if p.suffix=='.jsonl':
        try:loadbytes(b)
        except json.JSONDecodeError:
            assert b.strip()
            for line in b.splitlines():assert line.strip();loadbytes(line)
    owned.append(ref(p))
files=set();dirs=set()
for p in F.rglob('*'):
    assert not p.is_symlink();n=safe(p.relative_to(F).as_posix())
    if stat.S_ISREG(p.stat().st_mode):files.add(n)
    else:assert stat.S_ISDIR(p.stat().st_mode);dirs.add(n)
assert len({r['path'] for r in mf['files']})==1544
assert files=={r['path'] for r in mf['files']}|{'MANIFEST.json'}
assert dirs=={q.as_posix() for n in files for q in PurePosixPath(n).parents if q.as_posix()!='.'}
assert stat.S_IMODE((F/'MANIFEST.json').stat().st_mode)==0o444
x=load(F/'CURRENT_EXECUTION_REFERENCE.json');O=A/safe(x['audit_relative_outer_capture']);I=A/safe(x['audit_relative_inner_attempt'])
cap=load(O/'CAPTURE.json');pre=load(O/'OPERATION_PRELAUNCH.json');inv=load(I/'INVOCATION.json')
assert cap['schema']=='pr49-root-actual-builder-operation/v1' and cap['actual_execution'] is True and cap['completed'] is True and type(cap['exit_code']) is int and cap['exit_code']==0 and cap['pid']==x['actual_builder_pid']==inv['pid']==47575 and cap['operator_pid']==x['outer_parent_pid']==inv['parent_pid']==47574
assert cap['cwd']==pre['cwd']==inv['cwd']==str(R) and cap['argv']==pre['argv']==['/usr/bin/python3','-B',*inv['argv']]
assert cap['builder_unchanged_after_child'] is True and cap['operator_unchanged_after_child'] is True and cap['current_whole_verdict'] is None and cap['new_whole_current_gate']=='PENDING'
assert sha(raw(O/'OPERATION_PRELAUNCH.json'))==x['outer_prelaunch_sha256']
assert raw(O/'PRELAUNCH_BUILDER_SOURCE.py')==raw(I/'PRELAUNCH_BUILDER_SOURCE.py')==raw(A/'current_preparation_family/prepare_current_packet.py')
assert raw(O/'PRELAUNCH_OPERATOR.py')==raw(A/'current_preparation_family/capture_root_builder_operation.py')
assert sha(raw(O/'PRELAUNCH_BUILDER_SOURCE.py'))==cap['builder_sha256']==pre['builder_sha256']==inv['source_sha256']
assert sha(raw(O/'PRELAUNCH_OPERATOR.py'))==cap['operator_sha256']==pre['operator_sha256']
for k in ['stdout','stderr']:
    b=raw(O/safe(cap[k]['path']));assert len(b)==cap[k]['bytes'] and sha(b)==cap[k]['sha256']
assert not raw(O/'stderr.bin');printed=load(O/'stdout.bin')
assert printed['manifest_sha256']==sha(raw(F/'MANIFEST.json')) and printed['current_whole_verdict'] is None and printed['full_problem_solved'] is True and printed['native_writes']==0
commands=load(I/'GIT_COMMANDS.json');prefix=load(F/'build/actual_attempt_prepublication_prefix/GIT_COMMANDS.json')
assert len(commands)==50 and len(prefix)==48 and commands[:48]==prefix
streams=[];pids=set()
for i,c in enumerate(commands):
    assert c['actual_execution'] is True and c['completed'] is True and type(c['pid']) is int and c['pid'] not in pids and type(c['exit_code']) is int and c['exit_code']==0 and c['stdin_supplied'] is False and c['cwd']==str(R)
    pids.add(c['pid']);argv=c['argv'];assert argv[0]=='git' and argv[1] in {'branch','rev-parse','show','ls-tree','diff','merge-base'}
    if argv[1]=='branch':assert argv==['git','branch','--show-current']
    assert dt.datetime.fromisoformat(cap['started_utc'])<=dt.datetime.fromisoformat(c['started_utc'])<=dt.datetime.fromisoformat(c['finished_utc'])<dt.datetime.fromisoformat(cap['finished_utc'])
    for k in ['stdout','stderr']:
        p=I/safe(c[k]['path']);b=raw(p);assert len(b)==c[k]['bytes'] and sha(b)==c[k]['sha256'];streams.append(ref(p))
    assert not raw(I/c['stderr']['path'])
assert commands[-2]['argv']==['git','branch','--show-current'] and commands[-1]['argv']==['git','rev-parse','HEAD']
dep=load(F/'CURRENT_DEPENDENCIES.json');assert len(dep['files'])==1407 and len(dep['current_native13'])==13
allowed={'unsolved_math_prioritization/QUEUE.md','unsolved_math_prioritization/state.json','unsolved_math_prioritization/history.jsonl','draft_pr_publication_program_20260930/inventory.json'}
external=[];dated=[]
for r in dep['files']:
    q=ref(R/safe(r['path']));old={k:r[k] for k in ['path','bytes','sha256','full_mode']}
    if q!=old:assert r['path'] in allowed;dated.append(dict(historical=old,present=q))
    external.append(old)
snap=load(F/'original_snapshot_manifest.json');assert len(snap['files'])==16
for r in snap['files']:
    b=raw(F/'original_archive'/safe(r['relative_path']));assert len(b)==r['bytes'] and sha(b)==r['sha256']
immutable=['verify.py','verification.json','prior_report.json','source_record.json','turns.json','source_checksums.json','review/submitted_verify.py','review/verification.json','review/independent_checks.py','review/independent_results.json','review/verdict.json']
for n in immutable:assert raw(F/n)==raw(F/'original_archive'/n)
assert sha(raw(F/'original_diff.patch'))=='9aafdb42b2983020e919d6ff66b03720e1d858eebd98b4e46fa6b3909923fb50'
patch=load(F/'CURRENT_QUEUE_PATCH.json');assert patch['phase']=='LOCAL_PROPOSAL_ONLY_NO_NATIVE_WRITE' and patch['allowed_named_changes']==['Status','Turns','Findings'] and len(patch['changes'])==1
for n in allowed:
    name=n.replace('/','__');before=raw(F/'native4_proposal/preimage'/name);after=raw(F/'native4_proposal/prospective'/name)
    if n.endswith('/QUEUE.md'):
        assert sha(before)==patch['whole_preimage_sha256'] and sha(after)==patch['whole_prospective_sha256']
        c=patch['changes'][0];assert c['id_code']=='30000703 / OWR-1460-009' and before.count(c['row_before'].encode())==1 and before.replace(c['row_before'].encode(),c['row_prospective'].encode(),1)==after
        b=c['row_before'].split('|');a=c['row_prospective'].split('|');assert len(a)==len(b)==14
        assert all(a[i]==b[i] for i in range(14) if i not in {8,9,11}) and a[8].strip()=='already_solved' and a[9].strip()=='0/5'
    else:assert before==after
status=load(F/'status.json');assert status['status']=='already_solved' and status['original_substantive_attempts']==0 and status['new_substantive_attempts']==status['audit_turns']==0 and status['full_problem_solved'] is True and status['project_solved'] is False and status['novelty_claimed'] is False and status['full_2007_journal_proof_independently_certified'] is False and status['current_verdict'] is None
record=dict(schema='pr49-root-actual-complete-current-freeze-inspection/v1',created_utc=dt.datetime.now(dt.timezone.utc).isoformat(),actual_inspection_pid=os.getpid(),status='PASS_ROOT_COMPLETE_ACTUAL_CURRENT_FREEZE_EVIDENCE_ONLY',candidate_manifest=ref(F/'MANIFEST.json'),complete_current_payload=owned,exact_relative_directories=sorted(dirs),complete_dependencies=external,legitimate_dated_native_changes=dated,entire_actual_outer_capture=cap,entire_outer_stdout_object=printed,complete_outer_members=[ref(p) for p in sorted(O.iterdir())],entire_final_original_inner_commands=commands,complete100_inner_streams=streams,original_inner_record=ref(I/'GIT_COMMANDS.json'),frozen48_honest_prefix_of_actual50=True,native4_local_proposal_preserves_all_other_rows_Chat_DOI=True,all16_archive_and11_operative_literal=True,new_SOURCE_record=ref(A/'ROOT_NEW_SOURCE_ADVERSARY_RECORD.json'),actual_ROOT_prerequisite_authoring_capture=ref(A.parent/'pr45_9900007/root_pr49_current_prerequisites_authoring_actual_capture/CAPTURE.json'),new_whole_current_gate='PENDING',whole_review_or_acceptance_approved=False,future_acceptance_approved=False,full_problem_solved=True,project_solved=False,novelty_claimed=False,paper=False,DOI=False,tracker=False)
out=A/'ROOT_ACTUAL_CURRENT_FREEZE_INSPECTION.json'
with out.open('xb') as h:h.write((json.dumps(record,indent=2,allow_nan=False)+'\n').encode());h.flush();os.fsync(h.fileno())
print(json.dumps(dict(status=record['status'],actual_pid=os.getpid(),record=ref(out),payload_files=len(owned),directories=len(dirs),dependencies=len(external),actual_final_inner50=len(commands),frozen_prefix48=len(prefix),future_acceptance_approved=False),indent=2))
