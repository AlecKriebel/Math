"""Independent full-byte metadata inspection, never executes or imports a reviewed helper."""
from pathlib import Path, PurePosixPath
import datetime as dt, hashlib, json, math, os, re, stat
F=Path(__file__).absolute().parent; A=F.parent; R=F.parents[3]; S=A/'acceptance_preparation_family'; C=A/'reviewed_candidate'; W=A/'current_whole_adversary_family'
rows={}; reads=0; total=0
def need(v,m):
    if not v: raise ValueError(m)
def sha(b): return hashlib.sha256(b).hexdigest()
def equal(a,b):
    if type(a) is not type(b): return False
    if type(a) is dict: return a.keys()==b.keys() and all(equal(a[k],b[k]) for k in a)
    if type(a) is list: return len(a)==len(b) and all(equal(x,y) for x,y in zip(a,b))
    return a==b
def parse(b):
    def pairs(v):
        d={}
        for k,x in v: need(k not in d,'Duplicate JSON key'); d[k]=x
        return d
    def fl(s): x=float(s); need(math.isfinite(x),'Nonfinite JSON'); return x
    return json.loads(b,object_pairs_hook=pairs,parse_float=fl,parse_constant=lambda s:(_ for _ in ()).throw(ValueError(s)))
def rel(n):
    need(type(n) is str and n and n!='.' and '\\' not in n and '\0' not in n,'Literal relative path')
    p=PurePosixPath(n); need(not p.is_absolute() and p.as_posix()==n and not {'.','..','.git','__pycache__'}.intersection(p.parts),'Canonical path'); return n
def raw(p):
    global reads,total
    need(not p.is_symlink() and all(not q.is_symlink() for q in p.parents) and stat.S_ISREG(p.stat().st_mode),'Real regular nonsymlink input '+str(p))
    b=p.read_bytes(); reads+=1; total+=len(b); z={'path':rel(p.relative_to(R).as_posix()),'bytes':len(b),'sha256':sha(b),'full_mode':stat.S_IMODE(p.stat().st_mode)}
    if z['path'] in rows: need(equal(rows[z['path']],z),'Input changed during inspection '+z['path'])
    rows[z['path']]=z; return b
def load(p): return parse(raw(p))
def check(base,z,mode=None):
    need(type(z) is dict and type(z.get('bytes',z.get('size'))) is int and z.get('bytes',z.get('size'))>=0 and type(z.get('sha256')) is str and re.fullmatch('[0-9a-f]{64}',z['sha256']),'Typed full body reference')
    b=raw(base/rel(z['path'])); need(len(b)==z.get('bytes',z.get('size')) and sha(b)==z['sha256'],'Full body mismatch '+z['path'])
    if mode is not None: need(type(mode) is int and stat.S_IMODE((base/z['path']).stat().st_mode)==mode,'Full permission mismatch '+z['path'])
    return b
def closure(base,selfname,pin,count,dirs):
    b=raw(base/selfname); need(sha(b)==pin,'Exact fixed manifest SHA'); m=parse(b)
    need(m['self_excluded']==[selfname] and type(m['files_count']) is int and m['files_count']==count==len(m['files']),'Literal self-only full count')
    names=set()
    for z in m['files']:
        need(z['path'] not in names and z['path']!=selfname,'Unique payload'); check(base,z,0o444); names.add(z['path'])
    names.add(selfname); need(stat.S_IMODE((base/selfname).stat().st_mode)==0o444,'Full self0444')
    ff=set(); dd=set()
    for p in base.rglob('*'):
        need(not p.is_symlink() and (p.is_file() or p.is_dir()),'No special topology'); n=rel(p.relative_to(base).as_posix()); (ff if p.is_file() else dd).add(n)
    parent={str(p) for n in names for p in PurePosixPath(n).parents if str(p)!='.'}
    need(ff==names and dd==parent and (dirs is None or len(dd)==dirs),'Exact full files and directories'); return m
def clock(s):
    need(type(s) is str and s==s.strip(),'UTC scalar'); c=dt.datetime.fromisoformat(s.replace('Z','+00:00')); need(c.tzinfo is not None and c.utcoffset()==dt.timedelta(0),'UTC aware'); return c
def emit(n,o):
    with (F/n).open('xb') as h: h.write((json.dumps(o,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()); h.flush(); os.fsync(h.fileno())
def main():
    sm=closure(S,'PREPARATION_MANIFEST.json','2f5e572078066a5a895ac813e813106b140f4cc3beabd38f488b7633d07b9c86',121,23)
    need(set(sm)=={'schema','status','utc','self_excluded','files_count','files','source_only','proposed_helpers_imported_compiled_executed','future_acceptance_or_ROOT_approval_claimed'} and sm['schema']=='pr48-acceptance-source-closure/v1' and sm['source_only'] is True and sm['proposed_helpers_imported_compiled_executed'] is False and sm['future_acceptance_or_ROOT_approval_claimed'] is False,'Exact SOURCE schema')
    cm=closure(C,'MANIFEST.json','3f8d6b38fcd0268df5a32fc006c5a759b2dd61f225f2fa2fa959861a9bcb115f',1946,365)
    need(set(cm)=={'schema','self_excluded','files_count','files','current_gate','status','full_problem_solved','novelty_claimed','original_substantive_attempts','new_substantive_attempts','audit_turns','full_permission_mode','duplicate_shared_budget','turn_limit'},'Actual current schema parity')
    wm=closure(W,'MANIFEST.json','060aac8a645879155b1f3ae0a8026a201c0e63303ca24b6bd7b1374046ac30c8',162,38)
    inputs=load(S/'INPUT_BINDINGS.json'); need(inputs['actual_predecessor_PR47_completed'] is False and inputs['previous_mirror'] is None and inputs['previous_post'] is None and inputs['previous_root_post'] is None and inputs['future_native13_and_main_required'] is True,'No actual predecessor fabrication')
    refs=list(inputs['pins'].values())+inputs['external_input_rows']+list(inputs['source_pattern_dated_references'].values())+[inputs['known_predecessor_source_contract'],inputs['known_predecessor_source_manifest']]
    for z in refs: check(R,z,z['full_mode'])
    need(len(inputs['external_input_rows'])==3912==len({z['path'] for z in inputs['external_input_rows']}),'All distinct fixed3912')
    mutable={'draft_pr_publication_program_20260930/inventory.json','unsolved_math_prioritization/QUEUE.md','unsolved_math_prioritization/state.json','unsolved_math_prioritization/history.jsonl'}
    need({z['path'] for z in inputs['dated_native_external_rows']}==mutable and not mutable.intersection(z['path'] for z in inputs['external_input_rows']),'Exactly historicalnative4 excluded from stable external claims')
    root=load(A/'ROOT_WHOLE_CURRENT_REVIEW.json'); need(equal(root,load(S/'EXPECTED_ROOT_WHOLE_REVIEW.json')) and root['actual_readback_pid']==30858 and type(root['actual_readback_pid']) is int and root['future_acceptance_approved'] is False,'Complete genuine ROOT whole exact saved object')
    need(len(root['normalized_complete_external_input_bindings'])==3916 and len(root['legitimate_dated_native_changes'])==2,'Historical3916 and dated two queue changes')
    need(equal([z for z in root['normalized_complete_external_input_bindings'] if z['path'] not in mutable],inputs['external_input_rows']),'Exact3912 root exclusions')
    deps=load(C/'CURRENT_DEPENDENCIES.json'); need(equal(deps,load(S/'EXPECTED_CURRENT_DEPENDENCIES.json')) and len(deps['files'])==1798 and deps['resolution']=='repository_root / files.path; never scratch','Entire deps known schema')
    for z in deps['files']:
        if z['path'] not in mutable: check(R,z,z.get('full_mode'))
    need(equal(wm,load(S/'EXPECTED_WHOLE_MANIFEST.json')) and equal(load(W/'VERDICT.json'),load(S/'EXPECTED_WHOLE_VERDICT.json')),'Full WHOLE schema/object exact')
    snapshots=load(A/'snapshot_manifest.json'); need(len(snapshots['files'])==17 and snapshots['whole_repository_diff_files']==18,'Original17 vswhole18')
    for z in snapshots['files']:
        b=raw(A/'source_snapshot'/z['relative_path']); need(len(b)==z['bytes'] and sha(b)==z['sha256'] and b==raw(C/'original_archive'/z['relative_path']),'Literal original snapshot archive')
    imm=['PARTIAL.md','check_algebra.py','check_results.json','related_source_record.json','source_record.json','turns.jsonl','source_checksums.json','review/author_replay/check_algebra.py','review/author_replay/check_results.json','review/independent_checks.py','review/independent_results.json']
    for n in imm: need(raw(C/n)==raw(A/'source_snapshot'/n),'Entire operative immutable11')
    ledger=raw(C/'turns.jsonl'); events=[parse(z) for z in ledger.splitlines()]; need(ledger.endswith(b'\n') and len(events)==2 and [type(z['turn']) for z in events]==[int,int] and [z['turn'] for z in events]==[1,2] and equal(events,load(S/'EXPECTED_ORIGINAL_LEDGER.json')),'Entire shared literal original2/5 ledger')
    for n,i in [('source_record.json',2961),('related_source_record.json',30004403)]: z=load(C/n); need(type(z['id']) is int and z['id']==i and 'problem' not in z,'Plain integer source identity')
    need(not (C/'prior_report.json').exists() and not (A/'source_snapshot/prior_report.json').exists(),'Absent prior report file retained')
    science=load(S/'SCIENTIFIC_SCOPE.json'); need(science['literal_target_status']=='unsolved' and science['partial_valid'] is True and science['full_problem_solved'] is False and science['novelty_claimed'] is False and science['duplicate_shared_budget'] is True and type(science['original_substantive_attempts']) is int and science['original_substantive_attempts']==2 and science['new_substantive_attempts']==science['audit_turns']==0 and science['related_alias_QUEUE_row_absent_preserved'] is True and science['related_alias_native_entry_added'] is False,'Exact qualified science')
    drafts=[load(S/n) for n in ['DRAFT_ROOT_PRIMARY_READ_LEDGER.json','DRAFT_ROOT_SCIENCE_CARD.json','DRAFT_ROOT_SCOPE_CERTIFICATE.json']]
    need(all(equal(drafts[0],d) and d['root_completed'] is False and d['actual_pid'] is None and d['created_utc'] is None and d['actual_PR47_predecessor_completed'] is False and d['future_acceptance_approved'] is False for d in drafts),'Three entire false/null ROOT drafts')
    need(load(S/'DRAFT_ROOT_IMMUTABLE_BINDINGS.json')['previous_root_post'] is None and load(S/'DRAFT_FINAL_PLAN.json')['root_actual_PR47_predecessor_read_completed'] is False,'No final plan authority')
    pm=closure(R/Path(inputs['known_predecessor_source_manifest']['path']).parent,'PREPARATION_MANIFEST.json','1a10442d9962db99c608412f53fef754870bfadf24fd76e7e899112fc38ebef1',126,None)
    need(pm['source_only'] is True and pm['future_acceptance_or_ROOT_approval_claimed'] is False,'Closed47 source no actual authority')
    original=load(A/'root_original_actual_reproduction_v2/ROOT_REPRODUCTION_RESULT.json'); need(equal(original,load(S/'EXPECTED_ORIGINAL_CAPTURE_RESULT.json')),'Entire ROOT original capture result')
    for index,z in enumerate(original['complete_actual_Git_captures']+original['complete_actual_helper_captures']):
        helper=index>=38; need(type(z['pid']) is int and z['pid']>0 and type(z['exit_code']) is int and z['exit_code']==0 and z['actual_execution'] is True and z['completed'] is True,'Typed actual historical child')
        need((type(z['source']) is dict and z['source_unchanged'] is True) if helper else (z['source'] is None and z['source_unchanged'] is None),'Distinct NULL Git versus typed helper schema')
        for ch in ['stdout','stderr']: check(R,z[ch])
        need(raw(R/z['stderr']['path'])==b'','Complete original stderr'); need(clock(z['started_utc'])<=clock(z['finished_utc'])<=dt.datetime.now(dt.timezone.utc),'Actual dated UTC')
        if helper: check(R,z['source'])
    captures=[]
    for n,pid,status,arg in [('root_pr48_acceptance_source_closure_actual_capture',76301,'CLOSED_SOURCE_ONLY','close_source.py'),('root_pr48_acceptance_source_closed_readback_actual_capture',78175,'PASS_CLOSED_SOURCE_ONLY_READBACK','verify_closed_source.py')]:
        d=R/'draft_pr_publication_program_20260930/audits/pr45_9900007'/n; need({p.name for p in d.iterdir()}=={'CAPTURE.json','prelaunch_operator.py','stdout.bin','stderr.bin'},'Literal ROOT CAP4 topology, no invented prelaunch child')
        cap=load(d/'CAPTURE.json'); out=load(d/'stdout.bin'); op=raw(d/'prelaunch_operator.py')
        for ch in ['stdout','stderr']: check(d,cap[ch])
        need(sha(op)==cap['operator_sha256'] and cap['operator_unchanged'] is True and cap['schema']=='root-explicit-command-capture/v1' and type(cap['pid']) is int and cap['pid']==pid and type(cap['exit_code']) is int and cap['exit_code']==0 and cap['completed'] is True and cap['actual_execution'] is True and cap['stdin_supplied'] is False and cap['argv'][:3]==['/usr/bin/python3','-B',str(S/arg)] and cap['cwd']==str(R) and raw(d/'stderr.bin')==b'','Complete genuine ROOT close/read capture')
        need(out['status']==status and out['manifest_sha256']=='2f5e572078066a5a895ac813e813106b140f4cc3beabd38f488b7633d07b9c86','Entire ROOT child closure result')
        need(clock(cap['started_utc'])<=clock(cap['finished_utc'])<=dt.datetime.now(dt.timezone.utc),'Actual ROOT dated clock'); captures.append(cap)
    need(clock(captures[0]['finished_utc'])<clock(captures[1]['started_utc']),'Separate readonly child after closure exit')
    for n,code in {'inspect_inputs_v1_actual_capture':0,'author_sources_v1_actual_capture':0,'repair_sources_v2_actual_capture':0,'repair_metadata_v3_actual_capture':0,'private_controls_v1_actual_capture':0,'private_controls_v2_actual_capture':0,'expected_negative_actual_capture':1,'final_readback_actual_capture':0}.items():
        d=S/n; need({p.name for p in d.iterdir()}=={'CAPTURE.json','PRELAUNCH.json','PRELAUNCH_SOURCE.py','PRELAUNCH_OPERATOR.py','stdout.bin','stderr.bin'},'Private source CAP6 topology'); cap=load(d/'CAPTURE.json'); pre=load(d/'PRELAUNCH.json')
        need(type(cap['pid']) is int and cap['pid']>0 and type(cap['operator_pid']) is int and cap['operator_pid']>0 and type(cap['exit_code']) is int and cap['exit_code']==code and cap['completed'] is True and cap['actual_execution'] is True and cap['source_unchanged'] is True and cap['operator_unchanged'] is True and cap['production_import_compile_or_execution'] is False,'Actual source private capture')
        need(equal(cap['argv'],pre['argv']) and cap['cwd']==pre['cwd']==str(R) and sha(raw(d/'PRELAUNCH_SOURCE.py'))==cap['source_sha256']==pre['source_sha256'] and sha(raw(d/'PRELAUNCH_OPERATOR.py'))==cap['operator_sha256']==pre['operator_sha256'],'Entire private prelaunch binding')
        for ch in ['stdout','stderr']: check(d,cap[ch])
        need(raw(d/'stderr.bin')==b'' if code==0 else b'EXPECTED_REJECTION' in raw(d/'stderr.bin'),'Complete saved failure evidence'); need(clock(cap['started_utc'])<=clock(cap['finished_utc'])<=dt.datetime.now(dt.timezone.utc),'Capture UTC')
    result={'schema':'pr48-acceptance-source-adversary-fixed-inspection/v1','status':'PASS_READONLY_FIXED_BINDINGS','actual_pid':os.getpid(),'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'source_payload':121,'source_dirs':23,'current_payload':1946,'current_dirs':365,'WHOLE_payload':162,'WHOLE_dirs':38,'known47_source_payload':126,'fixed_external':3912,'historical_external':3916,'dated_native4_live_authority':False,'metadata_unique_inputs':len(rows),'full_input_reads':reads,'full_bytes_read_in_place':total,'foreign_bodies_copied':False,'SQL_queries_replayed':False,'full_mode_sweep_repeated':False,'complete_actual_ROOT_closure_captures':captures,'production_imported_compiled_executed':False,'future_acceptance_approved':False}
    emit('INPUT_READ_BINDINGS.json',{'schema':'pr48-acceptance-source-adversary-full-read-input-bindings/v1','rows':[rows[n] for n in sorted(rows)],'foreign_bodies_copied':False}); emit('FIXED_INPUT_INSPECTION.json',result); print(json.dumps(result,sort_keys=True))
if __name__=='__main__': main()
