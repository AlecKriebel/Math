#!/usr/bin/python3
"""Independent fixed SOURCE custody read, with no production import/compile/call."""
import datetime,hashlib,json,math,pathlib,re,stat
F=pathlib.Path(__file__).absolute().parent;A=F.parent;R=A.parents[2];H=A/'acceptance_preparation_family_v2'
MF='f44ccf65fa4397736305881de926eafcf211c33ef9e6fec5e5596c99d252ef40';reads=[];checks=0
def need(v,n):
    global checks
    if not v:raise ValueError(n)
    checks+=1
def sha(b):return hashlib.sha256(b).hexdigest()
def same(a,b):
    if type(a) is not type(b):return False
    if type(a) is dict:return a.keys()==b.keys() and all(same(a[k],b[k]) for k in a)
    if type(a) is list:return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
    return a==b
def parse(b):
    def pairs(items):
        out={}
        for k,v in items:
            if k in out:raise ValueError('Duplicate JSON key')
            out[k]=v
        return out
    def floating(s):
        v=float(s)
        if not math.isfinite(v):raise ValueError('Nonfinite JSON')
        return v
    def const(s):raise ValueError('Nonfinite JSON constant')
    return json.loads(b,object_pairs_hook=pairs,parse_float=floating,parse_constant=const)
def clock(s):
    t=datetime.datetime.fromisoformat(s)
    need(t.utcoffset()==datetime.timedelta(0),'Actual aware UTC');return t
def read(p,row=None,mode=None,role='fixed_first_party'):
    p=pathlib.Path(p)
    need(not p.is_symlink() and all(not q.is_symlink() for q in p.parents) and stat.S_ISREG(p.stat().st_mode),'Regular nonsymlink input')
    b=p.read_bytes();actual=stat.S_IMODE(p.stat().st_mode)
    if row is not None:need(type(row['bytes']) is int and len(b)==row['bytes'] and sha(b)==row['sha256'],'Complete pinned body '+str(p))
    if mode is not None:need(type(mode) is int and actual==mode,'Complete pinned full mode '+str(p))
    reads.append({'path':str(p),'canonical_path':str(p.resolve()),'bytes':len(b),'sha256':sha(b),'full_mode':actual,'role':role})
    return b
def relative(s):
    need(type(s) is str and s and '\\' not in s and '\0' not in s,'Relative text');p=pathlib.PurePosixPath(s);need(not p.is_absolute() and str(p)==s and not {'.','..','.git','__pycache__'}&set(p.parts),'Canonical member');return s
def closed(base,name,pin,count,dircount=None):
    b=read(base/name,mode=292,role='self_manifest');need(sha(b)==pin,'Actual manifest pin');d=parse(b);need(type(d['files_count']) is int and d['files_count']==count==len(d['files']) and same(d['self_excluded'],[name]),'Typed count/self-only closure')
    names=set();dirs=set();fold=set()
    for z in d['files']:
        relative(z['path']);need(z['path'] not in names and z['path']!=name,'Unique payload');names.add(z['path']);read(base/z['path'],z,292)
    found=set();founddirs=set()
    for p in base.rglob('*'):
        n=p.relative_to(base).as_posix();relative(n);need(n.casefold() not in fold and not p.is_symlink(),'No alias/symlink');fold.add(n.casefold())
        if p.is_dir():founddirs.add(n)
        else:need(stat.S_ISREG(p.stat().st_mode),'No special member');found.add(n)
    implied={str(p) for n in names for p in pathlib.PurePosixPath(n).parents if str(p)!='.'}
    need(found==names|{name} and founddirs==implied,'Entire closed topology')
    if dircount is not None:need(len(founddirs)==dircount,'Actual complete directory count')
    return d
def physical_absolute(s):
    need(type(s) is str and s.startswith(str(R)+'/'),'Exact literal absolute repository path');p=R
    for part in s[len(str(R))+1:].split('/'):
        need(part and part not in {'.git','__pycache__'} and not p.is_symlink() and p.is_dir(),'Real foreign traversal ancestors')
        if part=='.':continue
        if part=='..':need(p!=R,'No root escape');p=p.parent
        else:p=p/part
        need(p.exists() and not p.is_symlink() and (p==R or p.is_relative_to(R)),'No traversal escape or symlink')
    need(p!=R and p.resolve()==p,'Canonical resolved regular input');return p
def reference(z,role='reference'):
    relative(z['path']);return read(R/z['path'],z,z.get('full_mode'),role)
m=closed(H,'PREPARATION_MANIFEST.json',MF,109,23)
need(set(m)=={'files','files_count','future_acceptance_or_ROOT_approval_claimed','proposed_helpers_imported_compiled_executed','schema','self_excluded','source_only','status','utc'} and m['schema']=='pr46-acceptance-source-closure/v1' and m['source_only'] is True and m['proposed_helpers_imported_compiled_executed'] is False and m['future_acceptance_or_ROOT_approval_claimed'] is False,'Exact fixed source-only schema')
for z in m['files']:
    b=(H/z['path']).read_bytes()
    if z['path'].endswith('.json'):parse(b)
report=read(H/'FINAL_SOURCE_REPORT.md');need(len(report)==10317 and sha(report)=='990a322cd11062e5e9aa3efbd194d47cad04ffafbef0d80e87e7f691d2e247db','Exact final source report')
caps=[]
for suffix,pid in [('closure',36463),('closed_readback',36707)]:
    base=R/'draft_pr_publication_program_20260930/audits/pr45_9900007'/('root_pr46_acceptance_source_v2_'+suffix+'_actual_capture');c=parse(read(base/'CAPTURE.json'))
    need(c['schema']=='root-explicit-command-capture/v1' and c['actual_execution'] is True and c['completed'] is True and type(c['pid']) is int and c['pid']==pid and type(c['exit_code']) is int and c['exit_code']==0 and c['stdin_supplied'] is False and c['operator_unchanged'] is True and c['cwd']==str(R),'Actual ROOT closure/readback')
    need(sha(read(base/'prelaunch_operator.py'))==c['operator_sha256'],'Actual ROOT prelaunch operator')
    for stream in ['stdout','stderr']:read(base/c[stream]['path'],c[stream])
    need(c['stderr']['bytes']==0 and clock(c['started_utc'])<clock(c['finished_utc']),'Actual full successful split streams')
    obj=parse((base/'stdout.bin').read_bytes());need(obj['manifest_sha256']==MF and obj['payload_files']==109 and obj['relative_directories']==23 and obj['proposed_helpers_imported_compiled_executed'] is False and obj['future_acceptance_or_ROOT_approval_claimed'] is False,'Complete actual ROOT child stdout')
    caps.append(c)
need(clock(caps[0]['started_utc'])<=clock(m['utc'])<=clock(caps[0]['finished_utc'])<clock(caps[1]['started_utc'])<clock(caps[1]['finished_utc']),'Manifest inside closure interval, separate postexit readback')
need(sha(read(H/'close_source.py'))=='f6155f3ac542f9a17b774bd02e947fbe945a20591bce7f583cc75584f8c1db2e' and sha(read(H/'verify_closed_source.py'))=='072d3e446b7ec953d5619e7c151f212e9cf041d047fb1581b51af3ff4292428e','Actual final closer/verifier identity')
need(read(A/'ROOT_ACCEPTANCE_SOURCE_V2_CLOSURE_PRELAUNCH_SOURCE.py')==read(H/'close_source.py'),'Separately retained actual ROOT closer source')
inputs=parse(read(H/'INPUT_BINDINGS.json'));need(inputs['whole_binding_completed'] is True and inputs['external_input_count']==1877==len(inputs['external_input_rows']),'Entire actual whole evidence input contract')
candidate=closed(A/'reviewed_candidate','MANIFEST.json','66239699390b279235c4064208e63134049a5804884818de9176d377476a189d',946,142)
whole=closed(A/'current_whole_adversary_family','MANIFEST.json','be3fa099c6a080d5f9cddcf42f39ac51b51c8f89cd76d09fb5d360a99d1990e2',245,49)
need(same(whole,parse(read(H/'EXPECTED_WHOLE_MANIFEST.json'))),'Complete whole manifest typed equality')
for z in inputs['external_input_rows']:read(physical_absolute(z['path']),z,z['full_mode'],'unchanged_whole_external_current_body')
for z in inputs['pins'].values():reference(z)
for key in ['closed_root_whole_inspection','closed_whole_external_inventory','closed_whole_report','closed_whole_result','closed_whole_manifest','previous_mirror','previous_post','previous_root_post']:reference(inputs[key],key)
deps=parse(read(A/'reviewed_candidate/CURRENT_DEPENDENCIES.json'));need(same(deps,parse(read(H/'EXPECTED_CURRENT_DEPENDENCIES.json'))) and len(deps['files'])==826,'Complete dated current dependencies')
for z in deps['files']:read(A/z['path'],z,z.get('full_mode'),'dated_fixed_dependency')
root=parse(reference(inputs['closed_root_whole_inspection']));need(same(root,parse(read(H/'EXPECTED_ROOT_WHOLE_REVIEW.json'))) and root['mandatory_corrections']==[] and root['future_execution_approved'] is False and root['future_acceptance_approved'] is False,'Complete actual ROOT whole record, no future approval')
for z in root['normalized_complete_external_input_bindings']:reference(z,'entire_ROOT_whole_external')
repair=parse(read(H/'SOURCE_REPAIR_BINDINGS.json'));need(repair['closed_adverse_binding_completed'] is True and repair['future_acceptance_approved'] is False and repair['production_imported_compiled_executed'] is False and len(repair['complete_first_party_refs'])==297,'Completed negative history bindings')
for z in repair['complete_first_party_refs']:reference(z,'complete_rejected_source_binding')
closed(A/'acceptance_preparation_family','PREPARATION_MANIFEST.json','d97fb190b4b20a2566a1415130e4b7729cb1f8377f8b823e0fd0b263a3315dab',166,29)
adverse=closed(A/'acceptance_source_adversary_family','SELF_MANIFEST.json','eea93b507207955ba8aa00187e517d76f1f4e7e3826a333abedae924119fa845',94,13)
negative=parse(reference(repair['root_complete_adverse_inspection']));need(same(negative,parse(read(H/'EXPECTED_ROOT_REJECTED_V1_INSPECTION.json'))) and negative['acceptance_source_V1_rejected'] is True and negative['acceptance_source_V2_reviewed'] is False and negative['acceptance_source_V2_approved'] is False and negative['future_execution_approved'] is False and negative['future_acceptance_approved'] is False,'Actual full negative record is never repaired-source authority')
for z in negative['normalized_complete_external_input_bindings']:reference(z,'entire_ROOT_negative_unchanged_external')
for z in negative['additional_fixed_external_receipts']:reference(z,'negative_additional_actual_receipt')
for c in negative['complete_actual_closing_and_postclosing_readback_captures']:
    for z in c['complete_members']:reference(z,'negative_complete_actual_capture_member')
    cap=c['complete_capture'];need(cap['actual_execution'] is True and cap['completed'] is True and type(cap['pid']) is int and type(cap['exit_code']) is int and ((cap['exit_code']==0 and cap['status']=='PASS') or (cap['exit_code']!=0 and cap['status']=='FAIL')),'Honest completed negative success/failure classes')
need({c['complete_capture']['pid'] for c in negative['complete_actual_closing_and_postclosing_readback_captures'] if c['complete_capture']['exit_code']!=0}=={84831,2427,27909},'All three actual failures retained')
control=parse(read(H/'OWN_CONTROL_RESULTS.json'));need(control['actual_pid']==33881 and control['assertions']==80==len(control['checks']) and all(z['passed'] is True for z in control['checks']) and control['production_imported_compiled_executed'] is False and control['future_acceptance_approved'] is False and len(control['complete_input_reads'])==4560 and same(control['native13_before'],control['native13_after']),'Entire actual preparing control result, dated native observations')
for capfile in sorted(H.glob('*_ACTUAL_CAPTURE/CAPTURE.json')):
    d=capfile.parent;c=parse(read(capfile));pre=parse(read(d/'PRELAUNCH.json'));need(c['actual_execution'] is True and c['completed'] is True and type(c['pid']) is int and c['exit_code']==0 and c['source_unchanged'] is True,'All actual prepared nonproduction completions')
    need(sha(read(d/'PRELAUNCH_SOURCE.py'))==pre['source_sha256'] and sha(read(d/'PRELAUNCH_OPERATOR.py'))==pre['operator_sha256'] and same(c['prelaunch'],pre) and c['operator_unchanged'] is True,'Exact actual historical prelaunch source/operator')
    for stream in ['stdout','stderr']:read(d/c[stream]['path'],c[stream])
    need(clock(pre['created_utc'])<=clock(c['started_utc'])<=clock(c['finished_utc'])<clock(m['utc']),'Actual child/operator containment before ROOT closure')
actual=parse((H/'CONTROLS_ACTUAL_CAPTURE/CAPTURE.json').read_bytes());need(clock(actual['started_utc'])<=clock(control['utc'])<=clock(actual['finished_utc']),'Control result inside genuine child interval')
ledger=parse(read(A/'source_snapshot/turns.json'));need(same(ledger,parse(read(H/'EXPECTED_ORIGINAL_LEDGER.json'))) and type(ledger['substantive_turns_used']) is int and ledger['substantive_turns_used']==0 and type(ledger['source_verification_responses']) is int and ledger['source_verification_responses']==1,'Literal complete original0/5 and actual response1')
snap=parse(read(A/'snapshot_manifest.json'));need(len(snap['files'])==13,'All13 original science snapshot')
for z in snap['files']:need(read(A/'source_snapshot'/z['relative_path'],z,292)==read(A/'reviewed_candidate/original_archive'/z['relative_path']),'Literal original13 byte equality')
immutable={'SOURCE_STATUS.md','independent_review/independent_checks.py','independent_review/independent_results.json','provenance.json','source_record.json','turns.json','verification.json','verify.py'}
for n in immutable:need(read(A/'reviewed_candidate'/n)==read(A/'source_snapshot'/n),'Literal immutable8')
frozen={z['path'] for z in candidate['files']};admin={'status.json','readiness.json','independent_review/verdict.json','independent_review/review_summary.json'};overlay=frozen|{'reviewed_pending_administration/'+n for n in admin}|{'reviewed_pending_administration/MANIFEST.json','ACCEPTED_QUEUE_PATCH.json','CURRENT_ACCEPTANCE_SCOPE.md','CURRENT_CONTEXT_PRESENT.md','CURRENT_AUDIT_SCOPE_PRESENT.md'};need(len(overlay)==955 and len(overlay|{'acceptance.json','ACCEPTANCE.md'})==957,'Independent exact overlay/accepted set counts')
previous=parse(reference(inputs['previous_mirror']));post=parse(reference(inputs['previous_post']));rootpost=parse(reference(inputs['previous_root_post']));need(len(previous['entries'])==35 and same(post,rootpost['entire_post']) and rootpost['completed_primary_prs']==35 and same(post,parse(read(H/'EXPECTED_PREVIOUS_POST.json'))) and same(rootpost,parse(read(H/'EXPECTED_PREVIOUS_ROOT_POST.json'))),'Actual whole PR45 predecessor contract')
postcontract=parse(read(H/'ROOT_POST_CONTRACT.json'));need(len(postcontract['required_ROOT_complete_keyset'])==len(set(postcontract['required_ROOT_complete_keyset']))==22 and postcontract['future_ROOT_post_completed'] is False and postcontract['required_completed_values']['owned_operational_log_appends_exact'] is True,'22-key future ROOT post remains prospective')
for n in ['DRAFT_FINAL_PLAN.json','DRAFT_ROOT_IMMUTABLE_BINDINGS.json']:
    d=parse(read(H/n));need(d['independent_whole_current_pass'] is False and d['root_acceptance_source_review_completed'] is False and d['root_actual_PR45_predecessor_read_completed'] is False,'No draft future authority')
sources={}
for n in ['pr46_guards.py','integrate_reviewed_partial.py','state_mirror_reconciliation.py','verify_post_acceptance.py','seal_final_evidence.py','capture_root_final_operation.py']:
    b=read(H/n,mode=292,role='FULL_SOURCE_UTF8_TEXT_ONLY');b.decode('utf-8');sources[n]=sha(b)
result={'schema':'pr46-source-v2-independent-fixed-corpus-controls/v1','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_FIXED_CORPUS_CUSTODY_SOURCE_ONLY','assertions_passed':checks,'complete_read_bindings':reads,'complete_read_count':len(reads),'unique_canonical_read_count':len({z['canonical_path'] for z in reads}),'all_read_bytes_with_repeats':sum(z['bytes'] for z in reads),'preparation_manifest_sha256':MF,'entire_actual_ROOT_closure_and_postexit_capture':caps,'six_source_sha256':sources,'private_controls_not_production_runtime':True,'production_imported_compiled_executed':False,'foreign_bodies_copied':False,'future_acceptance_approved':False,'SOURCE_verdict':None,'new_substantive_attempts':0,'audit_turns':0,'dated_native4_and_preparer_mode_history_not_current_authority':True}
(F/'FIXED_CORPUS_RESULT_V2.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ['complete_read_bindings','entire_actual_ROOT_closure_and_postexit_capture','six_source_sha256']}))
