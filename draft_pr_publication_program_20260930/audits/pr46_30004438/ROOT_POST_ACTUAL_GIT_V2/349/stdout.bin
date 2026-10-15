#!/usr/bin/env python3
"""Second independently authored private schema/source audit; no production imports."""
from pathlib import Path, PurePosixPath
import copy, datetime as dt, hashlib, json, re, stat, subprocess
F=Path(__file__).absolute().parent; A=F.parent; R=A.parents[2]; V=A/'current_preparation_family_v2'
C=[]
def req(v):
    if not v: raise ValueError('Independent source-contract fixture rejected')
def ck(n,v):
    if not v: raise AssertionError(n)
    C.append(n)
def bad(n,fn,*args):
    try: fn(*args)
    except (ValueError,KeyError,TypeError): ck(n,True)
    else: raise AssertionError('Negative fixture accepted '+n)
def sha(b): return hashlib.sha256(b).hexdigest()
def dump(v): return (json.dumps(v,indent=2,sort_keys=True,allow_nan=False)+'\n').encode()
def read(p):
    req(not p.is_symlink() and not any(x.is_symlink() for x in p.parents) and stat.S_ISREG(p.stat().st_mode)); return p.read_bytes()
def obj(p): return json.loads(read(p))
def same(x,y): return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False)==json.dumps(y,sort_keys=True,separators=(',',':'),allow_nan=False)
def clock(v):
    req(type(v) is str); v=dt.datetime.fromisoformat(v[:-1]+'+00:00' if v.endswith('Z') else v); req(v.tzinfo is not None and v.utcoffset()==dt.timedelta(0)); return v
def aware(v): req(clock(obj(V/'PREPARATION_MANIFEST.json')['utc'])<=clock(v)<=dt.datetime.now(dt.timezone.utc))
def row(v):
    req(type(v) is dict and set(v)=={'path','bytes','sha256'} and type(v['path']) is str and v['path'])
    p=PurePosixPath(v['path']); req(not p.is_absolute() and str(p)==v['path'] and not set(p.parts).intersection({'.','..','.git','__pycache__'}) and '\\' not in v['path'] and '\0' not in v['path'])
    req(type(v['bytes']) is int and v['bytes']>=0 and type(v['sha256']) is str and re.fullmatch('[a-f0-9]{64}',v['sha256']))
FLAGS=list(obj(V/'DRAFT_ROOT_READ_LEDGER.json')['root_flags'])
PINS={k:'a'*64 for k in ['scope_certificate_sha256','preparation_manifest_sha256','source_qualification_sha256','evidence_bindings_sha256']}
FAMILY={'projective_algebra_family':'b'*64,'complex_dynamics_family':'c'*64}
def ledger(v,schema):
    req(v['operative_preparation_directory']=='current_preparation_family_v2' and v['schema']==schema and v['reading_completed'] is True and same(v['root_flags'],{k:True for k in FLAGS}))
    req(type(v['reading_notes']) is str and len(v['reading_notes'].strip())>=40); aware(v['created_utc'])
    req(all(v[k]==p for k,p in PINS.items()) and same(v['family_manifest_sha256'],FAMILY))
    for k,num in [('original_substantive_attempts',0),('original_source_verification_responses',1),('new_substantive_attempts',0),('audit_turns',0)]: req(type(v[k]) is int and v[k]==num)
def science(v):
    ledger(v,'PR46_ROOT_SCIENCE_CARD_v1')
    req(v['status']=='already_solved' and v['exact_known_target_verified'] is True and v['full_problem_solved'] is True and v['full_target_prior_result_verified'] is True and v['project_solved'] is False and v['novelty_claimed'] is False)
    req(type(v['turn_limit']) is int and v['turn_limit']==5 and v['existing_result_credit']==['Khazhgali Kozhasov','Mario Kummer'] and v['source_publication_kind']=='preprint')
    req(all(v[k] is False for k in ['paper_created','new_DOI_created','tracker_row_created']) and v['read_ledger_sha256']=='d'*64 and v['current_input_manifest_sha256']=='e'*64 and v['new_whole_current_gate']=='PENDING')
    req(all(v[k] is None for k in ['current_model','current_reasoning_effort','current_deadline_utc','current_verdict']))
def evidence(v):
    req(type(v) is dict and set(v)=={'schema','approved_by_root','created_utc','notes','manifest','proof_notes','summary','raw_audit','source_adversary','operative_preparation_directory'})
    req(v['schema']=='PR46_ROOT_EVIDENCE_BINDINGS_v1' and v['approved_by_root'] is True and v['operative_preparation_directory']=='current_preparation_family_v2')
    aware(v['created_utc']); req(type(v['notes']) is str and len(v['notes'].strip())>=40)
    for k in ['manifest','proof_notes','summary','raw_audit','source_adversary']: row(v[k])
    expected={'manifest':'root_original_actual_reproduction_v2/MANIFEST.json','proof_notes':'ROOT_MATHEMATICAL_REVIEW.md','summary':'root_original_actual_reproduction_v2/ROOT_CURRENT_REPRODUCTION_SUMMARY.json','raw_audit':'ROOT_COMPLETE_RAW_SQL_AUDIT.json'}
    req(all(v[k]['path']==n for k,n in expected.items()))
def outer(v,name,parent,bhash,ohash,argv):
    req(type(name) is str and re.fullmatch(r'tmp/root_pr46_current_v2_outer_[0-9]{8}T[0-9]{6}\.[0-9]{6}Z',name))
    req(v['schema']=='PR46_ROOT_BUILDER_PRELAUNCH_v2' and type(v['operator_pid']) is int and v['operator_pid']==parent and v['builder_sha256']==bhash and v['operator_sha256']==ohash and v['argv']==argv and v['cwd']==str(R)); req(clock(v['started_utc'])<=dt.datetime.now(dt.timezone.utc))
def new_adversary(v):
    req(v['schema']=='PR46_ROOT_NEW_SOURCE_ADVERSARY_RECORD_v1' and all(v[k] is True for k in ['approved_by_root','complete_report_personally_read','new_different_source_adversary','closed_clean']) and v['mandatory_corrections']==[])
    req(v['preparation_manifest_sha256']==PINS['preparation_manifest_sha256'] and v['builder_sha256']=='f'*64 and v['operator_sha256']=='0'*64); aware(v['created_utc'])
    row(v['manifest']); row(v['report']); req(type(v['members']) is list)
    for rr in v['members']: row(rr)
    req(v['report']['path'] in {x['path'] for x in v['members']})
def main():
    now=dt.datetime.now(dt.timezone.utc).isoformat()
    l=obj(V/'DRAFT_ROOT_READ_LEDGER.json'); l.update(created_utc=now,reading_completed=True,root_flags={k:True for k in FLAGS},reading_notes='Synthetic private controls only; never real reading or ROOT approval.',family_manifest_sha256=FAMILY,**PINS)
    ledger(l,'PR46_ROOT_PRIMARY_READ_LEDGER_v1'); ck('complete synthetic read ledger fixture',True)
    for k,v in [('reading_completed',1),('reading_completed',False),('root_flags',{FLAGS[0]:True}),('root_flags',{k:1 for k in FLAGS}),('reading_notes','short'),('created_utc',None),('operative_preparation_directory','current_preparation_family'),('original_substantive_attempts',False),('original_source_verification_responses',True),('new_substantive_attempts',True),('audit_turns',False),('scope_certificate_sha256','b'*64),('family_manifest_sha256',{})]:
        q=copy.deepcopy(l); q[k]=v; bad('read ledger malformed '+k,ledger,q,'PR46_ROOT_PRIMARY_READ_LEDGER_v1')
    q=copy.deepcopy(l); q['root_flags']['unrecognized_extra_reading']=True; bad('unknown reading flag',ledger,q,'PR46_ROOT_PRIMARY_READ_LEDGER_v1')
    s=obj(V/'DRAFT_ROOT_SCIENCE_CARD.json'); s.update({k:v for k,v in l.items() if k!='schema'}); s.update(exact_known_target_verified=True,full_problem_solved=True,full_target_prior_result_verified=True,read_ledger_sha256='d'*64,current_input_manifest_sha256='e'*64)
    science(s); ck('complete synthetic known-result science fixture',True)
    for k,v in [('project_solved',True),('novelty_claimed',True),('paper_created',True),('new_DOI_created',True),('tracker_row_created',True),('turn_limit',True),('turn_limit',1),('current_model','claimed-current'),('current_reasoning_effort','xhigh'),('current_deadline_utc',now),('current_verdict','PASS'),('new_whole_current_gate','PASS'),('source_publication_kind','journal'),('existing_result_credit',[]),('read_ledger_sha256','0'*64),('current_input_manifest_sha256','0'*64),('operative_preparation_directory','current_preparation_family')]:
        q=copy.deepcopy(s); q[k]=v; bad('science forbidden/incorrect '+k,science,q)
    e=obj(V/'DRAFT_ROOT_EVIDENCE_BINDINGS.json'); e.update(approved_by_root=True,created_utc=now,notes='Synthetic private evidence fixture; no ROOT approval is supplied.')
    for k,n in [('manifest','root_original_actual_reproduction_v2/MANIFEST.json'),('proof_notes','ROOT_MATHEMATICAL_REVIEW.md'),('summary','root_original_actual_reproduction_v2/ROOT_CURRENT_REPRODUCTION_SUMMARY.json'),('raw_audit','ROOT_COMPLETE_RAW_SQL_AUDIT.json'),('source_adversary','synthetic/ROOT_RECORD.json')]: e[k]={'path':n,'bytes':0,'sha256':'a'*64}
    evidence(e); ck('complete synthetic evidence fixture',True)
    for k,v in [('approved_by_root',1),('approved_by_root',False),('created_utc',None),('operative_preparation_directory','current_preparation_family'),('notes','short'),('manifest',dict(e['manifest'],path='other/MANIFEST.json')),('summary',dict(e['summary'],path='summary.json')),('proof_notes',dict(e['proof_notes'],path='DRAFT_ROOT_MATHEMATICAL_REVIEW.md')),('raw_audit',dict(e['raw_audit'],path='../ROOT_COMPLETE_RAW_SQL_AUDIT.json')),('source_adversary',dict(e['source_adversary'],bytes=True))]:
        q=copy.deepcopy(e); q[k]=v; bad('evidence malformed '+k,evidence,q)
    q=copy.deepcopy(e); q['future_acceptance_approved']=True; bad('evidence extra future approval field',evidence,q)
    for n,fn,args in [('DRAFT_ROOT_READ_LEDGER.json',ledger,('PR46_ROOT_PRIMARY_READ_LEDGER_v1',)),('DRAFT_ROOT_SCIENCE_CARD.json',science,()),('DRAFT_ROOT_EVIDENCE_BINDINGS.json',evidence,())]: bad('actual false/null draft '+n,fn,obj(V/n),*args)
    argv=['/usr/bin/python3','-B',str(V/'prepare_current_packet.py'),'--execute']; o={'schema':'PR46_ROOT_BUILDER_PRELAUNCH_v2','operator_pid':123,'builder_sha256':'a'*64,'operator_sha256':'b'*64,'argv':argv,'cwd':str(R),'started_utc':now}
    on='tmp/root_pr46_current_v2_outer_20261003T050000.000000Z'; outer(o,on,123,'a'*64,'b'*64,argv); ck('synthetic inherited V2 parent source/argv fixture',True)
    for k,v in [('schema','PR46_ROOT_BUILDER_PRELAUNCH_v1'),('operator_pid',True),('operator_pid',124),('builder_sha256','b'*64),('operator_sha256','c'*64),('argv',argv+['--extra']),('cwd','/tmp'),('started_utc','2999-01-01T00:00:00+00:00'),('started_utc','2026-10-03T00:00:00')]:
        q=copy.deepcopy(o); q[k]=v; bad('parent inherited mismatch '+k,outer,q,on,123,'a'*64,'b'*64,argv)
    for name in ['tmp/root_pr46_current_outer_20261003T050000.000000Z','../'+on,on+'/','/tmp/'+on,'']:
        bad('inherited V2 outer path mismatch '+name,outer,o,name,123,'a'*64,'b'*64,argv)
    a={'schema':'PR46_ROOT_NEW_SOURCE_ADVERSARY_RECORD_v1','approved_by_root':True,'complete_report_personally_read':True,'new_different_source_adversary':True,'closed_clean':True,'mandatory_corrections':[],'preparation_manifest_sha256':PINS['preparation_manifest_sha256'],'builder_sha256':'f'*64,'operator_sha256':'0'*64,'created_utc':now,'manifest':{'path':'synthetic/MANIFEST.json','bytes':0,'sha256':'a'*64},'report':{'path':'synthetic/AUDIT.md','bytes':0,'sha256':'a'*64},'members':[{'path':'synthetic/AUDIT.md','bytes':0,'sha256':'a'*64}]}
    new_adversary(a); ck('synthetic separate adversary record fixture',True)
    for k,v in [('approved_by_root',1),('complete_report_personally_read',False),('new_different_source_adversary',False),('closed_clean',False),('mandatory_corrections',['defect']),('preparation_manifest_sha256','b'*64),('builder_sha256','b'*64),('operator_sha256','b'*64),('members',[]),('created_utc',None)]:
        q=copy.deepcopy(a); q[k]=v; bad('separate adversary malformed '+k,new_adversary,q)
    # Inspect each actual typed SQL row binding without copying raw payload bodies.
    raw=obj(A/'ROOT_COMPLETE_RAW_SQL_AUDIT.json'); keys=set()
    for r in raw['complete_row_bindings']:
        ck('typed complete SQL row binding '+str(r['key']),type(r) is dict and set(r)=={'key','payload_sha256','report_sha256','complete_payload_recursive_type_equal','complete_report_recursive_type_equal','prior_key_present','ambiguous_code'} and type(r['key']) is str and r['key'] not in keys and re.fullmatch('[a-f0-9]{64}',r['payload_sha256']) is not None and re.fullmatch('[a-f0-9]{64}',r['report_sha256']) is not None and r['complete_payload_recursive_type_equal'] is True and r['complete_report_recursive_type_equal'] is True and type(r['prior_key_present']) is bool and type(r['ambiguous_code']) is bool)
        keys.add(r['key'])
    ck('raw typed SQL full coverage and absent selected prior',len(keys)==15458 and raw['future_acceptance_approved'] is False and raw['selected_prior_key_present'] is False and raw['raw_null_present'] is False and same(raw['selected_prior_fallback'],{}))
    pins=obj(V/'STATIC_INPUT_BINDINGS.json')
    for rr in pins['original_preparation_members']:
        ck('original318 actual full0444 '+rr['path'],stat.S_IMODE((A/rr['path']).stat().st_mode)==0o444)
    ck('original318 sole self actual full0444',stat.S_IMODE((A/'ORIGINAL_PREPARATION_MANIFEST.json').stat().st_mode)==0o444)
    # Closed V2 own captures distinguish both real failed runs and successful final controls.
    caprows=[]
    for name in ['AUTHORING_ACTUAL_CAPTURE','SOURCE_INPUT_INSPECTION_ACTUAL_CAPTURE','PRIVATE_CONTROLS_ACTUAL_CAPTURE','PRIVATE_CONTROLS_REPAIRED_ACTUAL_CAPTURE','PRIVATE_CONTROLS_FINAL_ACTUAL_CAPTURE']:
        d=V/name; cap=obj(d/'CAPTURE.json'); pre=obj(d/'PRELAUNCH.json')
        ck('V2 actual private capture flags '+name,cap['actual_execution'] is True and cap['completed'] is True and type(cap['pid']) is int and cap['pid']>0 and type(cap['exit_code']) is int and cap['stdin_supplied'] is False and cap['production_builder_or_ROOT_operator_executed'] is False and cap['source_unchanged'] is True and cap['operator_unchanged'] is True)
        ck('V2 prelaunch source/operator hashes '+name,sha(read(d/'PRELAUNCH_SOURCE.py'))==cap['source_sha256'] and sha(read(d/'PRELAUNCH_OPERATOR.py'))==cap['operator_sha256'])
        ck('V2 aware capture times '+name,clock(cap['started_utc'])<=clock(cap['finished_utc'])<=dt.datetime.now(dt.timezone.utc))
        for k in ['stdout','stderr']:
            r=cap[k]; b=read(d/r['path']); ck('V2 complete stream '+name+'/'+k,len(b)==r['bytes'] and sha(b)==r['sha256'])
        expected=1 if name in ['PRIVATE_CONTROLS_ACTUAL_CAPTURE','PRIVATE_CONTROLS_REPAIRED_ACTUAL_CAPTURE'] else 0
        ck('V2 preserved failed or complete capture '+name,cap['exit_code']==expected and (bool(read(d/'stderr.bin')) if expected else not read(d/'stderr.bin')))
        caprows.append({'directory':name,'pid':cap['pid'],'exit_code':cap['exit_code'],'capture_sha256':sha(read(d/'CAPTURE.json'))})
    # Read-only Git checks are actual separate children captured here and never mutate index/refs.
    gitdir=F/'read_only_git_actual'; gitdir.mkdir(exist_ok=False); commands=[]
    snapshot=obj(A/'snapshot_manifest.json'); metadata=obj(A/'original_pr_metadata.json')
    def git(*args):
        index=len(commands); argv=['git',*args]; rec={'argv':argv,'cwd':str(R),'started_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_execution':False,'pid':None,'completed':False,'exit_code':None,'stdin_supplied':False}
        with (gitdir/(str(index)+'.stdout')).open('xb') as out, (gitdir/(str(index)+'.stderr')).open('xb') as err:
            child=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=out,stderr=err,env=dict(__import__('os').environ,GIT_OPTIONAL_LOCKS='0')); rec.update(actual_execution=True,pid=child.pid); rec['exit_code']=child.wait(timeout=60); rec['completed']=True
        rec['finished_utc']=dt.datetime.now(dt.timezone.utc).isoformat()
        for k in ['stdout','stderr']:
            b=read(gitdir/(str(index)+'.'+k)); rec[k]={'path':str(index)+'.'+k,'bytes':len(b),'sha256':sha(b)}
        commands.append(rec); (gitdir/'GIT_COMMANDS.json').write_bytes(dump(commands)); req(rec['exit_code']==0 and not read(gitdir/(str(index)+'.stderr'))); return read(gitdir/(str(index)+'.stdout'))
    ck('actual current branch remains main',git('branch','--show-current').strip()==b'main')
    current_head=git('rev-parse','HEAD').decode().strip(); ck('actual currentHEAD typed',re.fullmatch('[a-f0-9]{40}',current_head) is not None)
    for rr in snapshot['files']:
        native=rr['path']; ck('actual original Git wholebody '+native,git('show',snapshot['head']+':'+native)==read(A/'source_snapshot'/rr['relative_path']))
        ck('actual original Git wholemode/blob '+native,git('ls-tree',snapshot['head'],'--',native).decode().strip()=='100644 blob '+rr['git_object']+'\t'+native)
    actualtree=git('ls-tree','-r','-z',snapshot['head'],'--','unsolved_math_prioritization/attempts/30004438/').decode().split('\0')
    ck('actual original Git exact13 tree',{r.split('\t',1)[1] for r in actualtree if r}=={rr['path'] for rr in snapshot['files']})
    ck('actual original whole14 pathdiff',git('diff','--no-ext-diff','--no-textconv','--binary',metadata['merge_base'],metadata['head'],'--')==read(A/metadata['full_diff']['path']))
    ck('actual original fourteen changed paths',git('diff','--name-only',metadata['merge_base'],metadata['head']).decode().splitlines()==[rr['path'] for rr in metadata['all_changed_paths']])
    ck('actual HEAD stable during original readback',git('rev-parse','HEAD').decode().strip()==current_head)
    result={'schema':'PR46_INDEPENDENT_V2_EXTENDED_SOURCE_CONTROLS_v1','created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'assertions_passed':len(C),'failed':0,'assertion_labels':C,'synthetic_fixtures_only_no_ROOT_approvals':True,'actual_V2_capture_inspection':caprows,'actual_read_only_git_commands':len(commands),'actual_current_head_at_private_source_audit':current_head,'production_import_compile_execute':False,'native_body_copy':False,'future_acceptance_approved':False,'scope_limit':'SQL row hashes checked as complete typed first-party evidence; raw foreign payloads not staged or newly independently SQL-reproduced.'}
    (F/'EXTENDED_CONTROL_RESULTS.json').write_bytes(dump(result)); print(json.dumps({k:result[k] for k in ['assertions_passed','failed','actual_read_only_git_commands','actual_current_head_at_private_source_audit','production_import_compile_execute','future_acceptance_approved']},sort_keys=True))
if __name__=='__main__': main()
