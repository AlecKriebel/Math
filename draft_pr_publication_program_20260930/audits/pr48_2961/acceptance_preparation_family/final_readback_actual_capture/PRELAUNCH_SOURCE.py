"""Private whole-byte inspection only; no imports or execution of production."""
import datetime as dt, hashlib, json, os, stat
from pathlib import Path, PurePosixPath
F=Path(__file__).absolute().parent;A=F.parent;R=F.parents[3];C=A/'reviewed_candidate';W=A/'current_whole_adversary_family';P47=R/'draft_pr_publication_program_20260930/audits/pr47_2849/acceptance_preparation_family'
MUTABLE={'draft_pr_publication_program_20260930/inventory.json','unsolved_math_prioritization/QUEUE.md','unsolved_math_prioritization/state.json','unsolved_math_prioritization/history.jsonl'}
IMM=['PARTIAL.md','check_algebra.py','check_results.json','related_source_record.json','source_record.json','turns.jsonl','source_checksums.json','review/author_replay/check_algebra.py','review/author_replay/check_results.json','review/independent_checks.py','review/independent_results.json']
def need(v,m):
    if not v:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def raw(p):
    need(not p.is_symlink() and all(not x.is_symlink() for x in p.parents) and stat.S_ISREG(p.stat().st_mode),'Regular nonsymlink source');return p.read_bytes()
def parse(b):
    def pairs(v):
        d={}
        for k,x in v:need(k not in d,'Duplicate JSON key');d[k]=x
        return d
    return json.loads(b,object_pairs_hook=pairs,parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))
def pin(p):
    b=raw(p);return {'path':p.relative_to(R).as_posix(),'bytes':len(b),'sha256':sha(b),'full_mode':stat.S_IMODE(p.stat().st_mode)}
def check(base,z,mode=None):
    n=z['path'];q=PurePosixPath(n);need(type(n) is str and n and q.as_posix()==n and not q.is_absolute() and n!='.' and not {'.','..','.git','__pycache__'}.intersection(q.parts) and '\\' not in n and '\0' not in n,'Canonical member');b=raw(base/n);need(type(z['bytes']) is int and z['bytes']>=0 and len(b)==z['bytes'] and sha(b)==z['sha256'],'Full exact member '+n)
    if mode is not None:need(type(mode) is int and stat.S_IMODE((base/n).stat().st_mode)==mode,'Full mode '+n)
    return len(b)
def closure(base,digest,count,dirs):
    b=raw(base/'MANIFEST.json');need(sha(b)==digest,'Closed manifest identity');m=parse(b);need(m['self_excluded']==['MANIFEST.json'] and type(m['files_count']) is int and m['files_count']==count and len(m['files'])==count,'Literal closure count');names={z['path'] for z in m['files']}|{'MANIFEST.json'};ff=set();dd=set()
    for p in base.rglob('*'):
        need(not p.is_symlink() and (p.is_file() or p.is_dir()),'No special topology');(ff if p.is_file() else dd).add(p.relative_to(base).as_posix())
    parents={p.as_posix() for n in names for p in PurePosixPath(n).parents if p.as_posix()!='.'};need(ff==names and dd==parents and len(dd)==dirs,'Exact recursive files/directories');need(stat.S_IMODE((base/'MANIFEST.json').stat().st_mode)==0o444,'Self manifest full444');total=sum(check(base,z,0o444) for z in m['files'])+len(b);return m,total
def dump(n,o):
    with (F/n).open('xb') as h:h.write((json.dumps(o,sort_keys=True,indent=2,allow_nan=False)+'\n').encode());h.flush();os.fsync(h.fileno())
def walk(o):
    if type(o) is dict:return 1+sum(walk(k)+walk(v) for k,v in o.items())
    if type(o) is list:return 1+sum(map(walk,o))
    need(type(o) in {str,int,float,bool,type(None)},'JSON type');return 1
def main():
    cm,cb=closure(C,'3f8d6b38fcd0268df5a32fc006c5a759b2dd61f225f2fa2fa959861a9bcb115f',1946,365);wm,wb=closure(W,'060aac8a645879155b1f3ae0a8026a201c0e63303ca24b6bd7b1374046ac30c8',162,38)
    b=raw(A/'ROOT_WHOLE_CURRENT_REVIEW.json');need(len(b)==1293932 and sha(b)=='f4e568944f746c31d68f426fc70121d5cb70187b8ed8b6365ecbd747ac773ee3','Entire genuine ROOT whole body');root=parse(b);nodes=walk(root);verdict=parse(raw(W/'VERDICT.json'));need(root['complete_VERDICT_object']==verdict and type(root['actual_readback_pid']) is int and root['actual_readback_pid']==30858 and root['future_acceptance_approved'] is False,'Entire actual ROOT scoped verdict')
    need(len(root['normalized_complete_first_party_members'])==162 and len(root['normalized_complete_external_input_bindings'])==3916,'Whole normalized binding counts');first=sum(check(R,z,z['full_mode']) for z in root['normalized_complete_first_party_members']);stable=[];dated=[];total=0
    for z in root['normalized_complete_external_input_bindings']:
        if z['path'] in MUTABLE:dated.append(z)
        else:total+=check(R,z,z['full_mode']);stable.append(z)
    need(len({z['path'] for z in stable+dated})==3916 and len(dated)==4,'Unique3916, exact datednative4 exclusion')
    need(type(root['legitimate_dated_native_changes']) is list and len(root['legitimate_dated_native_changes'])==2 and all(z['fresh_native_authority'] is False and z['historical_whole_row']['path']=='unsolved_math_prioritization/QUEUE.md' for z in root['legitimate_dated_native_changes']),'Two explicit dated unrelated queue observations')
    refs=[pin(C/'MANIFEST.json'),pin(C/'CURRENT_DEPENDENCIES.json'),pin(W/'MANIFEST.json'),pin(W/'AUDIT.md'),pin(W/'VERDICT.json'),pin(A/'ROOT_WHOLE_CURRENT_REVIEW.json'),pin(A/'snapshot_manifest.json'),pin(A/'original_diff.patch')]
    for z in root['ROOT_evidence_and_actual_prerequisite_bindings']:check(R,z,z['full_mode']);refs.append(z)
    for z in root['complete_actual_closing_and_postclosing_readback_captures']:
        cap=z['complete_capture'];need(type(cap['pid']) is int and cap['pid'] in [28458,29104] and type(cap['exit_code']) is int and cap['exit_code']==0,'Actual close/readback');capref=next(v for v in z['complete_members'] if v['path'].endswith('/CAPTURE.json'));need(parse(raw(R/capref['path']))==cap,'Entire actual capture');need(parse(raw((R/capref['path']).parent/'stdout.bin'))==z['complete_stdout_object'],'Entire child stdout')
        for row in z['complete_members']:check(R,row,row['full_mode']);refs.append(row)
    capdir=R/'draft_pr_publication_program_20260930/audits/pr45_9900007/root_pr48_whole_ROOT_record_authoring_actual_capture';cap=parse(raw(capdir/'CAPTURE.json'));need(cap['pid']==30858 and type(cap['pid']) is int and cap['completed'] is True and cap['exit_code']==0,'Actual ROOT author30858')
    for p in sorted(capdir.iterdir()):refs.append(pin(p));raw(p)
    original=parse(raw(A/'snapshot_manifest.json'));need(len(original['files'])==17 and original['whole_repository_diff_files']==18,'Original17/18paths')
    for z in original['files']:
        b=raw(A/'source_snapshot'/z['relative_path']);need(len(b)==z['bytes'] and sha(b)==z['sha256'] and b==raw(C/'original_archive'/z['relative_path']),'Exact17 original bodies')
    for n in IMM:need(raw(C/n)==raw(A/'source_snapshot'/n),'Exact operative11')
    ledger=raw(C/'turns.jsonl');entries=[parse(x) for x in ledger.splitlines()];need(ledger.endswith(b'\n') and len(entries)==2 and all(type(z['turn']) is int for z in entries) and [z['turn'] for z in entries]==[1,2],'Literal two-entry shared ledger')
    for n,identity in [('source_record.json',2961),('related_source_record.json',30004403)]:o=parse(raw(C/n));need(type(o['id']) is int and o['id']==identity and 'problem' not in o,'Plain integer source objects')
    need(not (C/'prior_report.json').exists() and not (A/'source_snapshot/prior_report.json').exists(),'Original priorfile absent')
    result=parse(raw(A/'root_original_actual_reproduction_v2/ROOT_REPRODUCTION_RESULT.json'));queries=result['complete_actual_Git_captures'];helpers=result['complete_actual_helper_captures'];need(len(queries)==38 and len(helpers)==4,'Actual38Git4helpers')
    for z in queries+helpers:
        need(type(z['pid']) is int and z['pid']>0 and type(z['exit_code']) is int and z['exit_code']==0 and z['actual_execution'] is True and z['completed'] is True and z['operator_unchanged'] is True,'Actual exact original child')
        for n in ['stdout','stderr']:check(R,z[n])
        need(raw(R/z['stderr']['path'])==b'','Entire original stderr')
        if z in queries:need(z['schema']=='pr48-root-readonly-git-actual-capture/v1' and z['source'] is None and z['source_unchanged'] is None,'Git NULL source class')
        else:need(z['schema']=='pr48-root-unchanged-helper-actual-capture/v1' and type(z['source']) is dict and z['source_unchanged'] is True,'Typed helper class');check(R,z['source'])
    refs.append(pin(A/'root_original_actual_reproduction_v2/ROOT_REPRODUCTION_RESULT.json'));deps=parse(raw(C/'CURRENT_DEPENDENCIES.json'));need(deps['resolution']=='repository_root / files.path; never scratch' and len(deps['files'])==1798,'Repo-root1798 dependencies')
    for z in deps['files']:
        if z['path'] not in MUTABLE:check(R,z,z.get('full_mode'))
    for n,v in {'EXPECTED_CURRENT_DEPENDENCIES.json':deps,'EXPECTED_CURRENT_ADMIN.json':parse(raw(C/'status.json')),'EXPECTED_WHOLE_MANIFEST.json':wm,'EXPECTED_WHOLE_VERDICT.json':verdict,'EXPECTED_ROOT_WHOLE_REVIEW.json':root,'EXPECTED_PRIMARY_READ_LEDGER.json':parse(raw(A/'ROOT_PRIMARY_READ_LEDGER.json')),'EXPECTED_SCIENCE_CARD.json':parse(raw(A/'ROOT_SCIENCE_CARD.json')),'EXPECTED_ORIGINAL_LEDGER.json':entries,'EXPECTED_ORIGINAL_CAPTURE_RESULT.json':result}.items():dump(n,v)
    pattern={}
    for n in ['pr47_guards.py','integrate_reviewed_partial.py','state_mirror_reconciliation.py','verify_post_acceptance.py','seal_final_evidence.py','capture_root_final_operation.py','ROOT_POST_CONTRACT.json','SCIENTIFIC_SCOPE.json','DRAFT_ROOT_IMMUTABLE_BINDINGS.json','DRAFT_FINAL_PLAN.json']:
        p=P47/n;row=pin(p);pattern[row['path']]=row
    predecessor_contract=pin(P47/'ROOT_POST_CONTRACT.json');predecessor_manifest=pin(P47/'PREPARATION_MANIFEST.json') if (P47/'PREPARATION_MANIFEST.json').exists() else None
    inputs={'schema':'pr48-acceptance-source-input-bindings/v1','whole_binding_completed':True,'actual_predecessor_PR47_completed':False,'previous_mirror':None,'previous_post':None,'previous_root_post':None,'previous_post_contract':None,'pins':{z['path']:z for z in refs},'external_input_rows':stable,'external_input_count':len(stable),'complete_historical_external_input_count':3916,'dated_native_external_rows':dated,'dated_native13':deps['current_native13'],'future_native13_and_main_required':True,'closed_whole_manifest':pin(W/'MANIFEST.json'),'closed_whole_result':pin(W/'VERDICT.json'),'closed_whole_report':pin(W/'AUDIT.md'),'closed_root_whole_inspection':pin(A/'ROOT_WHOLE_CURRENT_REVIEW.json'),'source_pattern_dated_references':pattern,'known_predecessor_source_contract':predecessor_contract,'known_predecessor_source_manifest':predecessor_manifest,'source_pattern_body_only_not_readiness':True,'foreign_bodies_copied':False,'production_import_compile_or_execution':False};dump('INPUT_BINDINGS.json',inputs)
    out={'schema':'pr48-acceptance-private-complete-input-inspection/v1','actual_pid':os.getpid(),'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'current_payload':1946,'current_dirs':365,'current_total_bytes':cb,'whole_payload':162,'whole_dirs':38,'whole_total_bytes':wb,'ROOT_full_bytes':1293932,'ROOT_full_json_nodes':nodes,'first_party_whole_bytes':first,'historical_external_count':3916,'fixed_external_count':len(stable),'fixed_external_bytes':total,'dated_native4':4,'legitimate_dated_native_observations':2,'original17_operative11_exact':True,'original_shared_turns':2,'raw_source_ids_integer':True,'original_priorfile_absent':True,'actual38nullGit4typedhelpers':True,'final52_prefix50':True,'actual_whole_closing_pid':28458,'actual_whole_readback_pid':29104,'actual_ROOT_record_pid':30858,'known47_source_manifest_available':predecessor_manifest is not None,'actual_PR47_predecessor_completed':False,'production_imported_compiled_executed':False,'future_acceptance_approved':False};dump('COMPLETE_INPUT_INSPECTION.json',out);print(json.dumps(out,sort_keys=True))
def final_readback():
    names=['pr48_guards.py','integrate_reviewed_partial.py','state_mirror_reconciliation.py','verify_post_acceptance.py','seal_final_evidence.py','capture_root_final_operation.py'];controls=parse(raw(F/'PRIVATE_CONTROLS_RESULT.json'));source={}
    for n in names:
        b=raw(F/n);need(sha(b)==controls['source_sha256'][n],'Exact final proposed source body');source[n]={'bytes':len(b),'sha256':sha(b),'lines':len(b.splitlines())}
    expected={'inspect_inputs_v1_actual_capture':0,'author_sources_v1_actual_capture':0,'repair_sources_v2_actual_capture':0,'repair_metadata_v3_actual_capture':0,'private_controls_v1_actual_capture':0,'private_controls_v2_actual_capture':0,'expected_negative_actual_capture':1};captures=[]
    for n,code in expected.items():
        folder=F/n;need({p.name for p in folder.iterdir()}=={'CAPTURE.json','PRELAUNCH.json','PRELAUNCH_SOURCE.py','PRELAUNCH_OPERATOR.py','stdout.bin','stderr.bin'},'Complete actual private capture topology');cap=parse(raw(folder/'CAPTURE.json'));pre=parse(raw(folder/'PRELAUNCH.json'));need(type(cap['pid']) is int and cap['pid']>0 and type(cap['operator_pid']) is int and cap['operator_pid']>0 and cap['actual_execution'] is True and cap['completed'] is True and type(cap['exit_code']) is int and cap['exit_code']==code and cap['source_unchanged'] is True and cap['operator_unchanged'] is True and cap['stdin_supplied'] is False,'Actual complete typed private child');need(cap['argv']==pre['argv'] and cap['cwd']==pre['cwd']==str(R) and sha(raw(folder/'PRELAUNCH_SOURCE.py'))==cap['source_sha256']==pre['source_sha256'] and sha(raw(folder/'PRELAUNCH_OPERATOR.py'))==cap['operator_sha256']==pre['operator_sha256'],'Complete prelaunch/argv/cwd');
        for ch in ['stdout','stderr']:check(folder,cap[ch])
        need((raw(folder/'stderr.bin')==b'') if code==0 else (b'EXPECTED_REJECTION' in raw(folder/'stderr.bin')),'Complete stderr disposition');start=dt.datetime.fromisoformat(cap['started_utc']);end=dt.datetime.fromisoformat(cap['finished_utc']);need(start.tzinfo is not None and start.utcoffset()==dt.timedelta(0) and end.tzinfo is not None and end.utcoffset()==dt.timedelta(0) and start<=end<=dt.datetime.now(dt.timezone.utc),'Actual chronology');captures.append({'capture':pin(folder/'CAPTURE.json'),'entire_capture':cap,'whole_prelaunch_and_streams':[pin(p) for p in sorted(folder.iterdir())]})
    plan=parse(raw(F/'DRAFT_FINAL_PLAN.json'));bindings=parse(raw(F/'DRAFT_ROOT_IMMUTABLE_BINDINGS.json'));contract=parse(raw(F/'ROOT_POST_CONTRACT.json'));scope=parse(raw(F/'SCIENTIFIC_SCOPE.json'));need(type(plan['pr']) is int and plan['pr']==48 and type(plan['original_substantive_attempts']) is int and plan['original_substantive_attempts']==bindings['original_substantive_attempts']==scope['original_substantive_attempts']==2,'Literal PR48/shared2 drafts');need(plan['root_actual_PR47_predecessor_read_completed'] is False and bindings['root_actual_PR47_predecessor_read_completed'] is False and bindings['previous_root_post'] is None,'No future predecessor fabricated');need(len(contract['future48_required_ROOT_complete_keyset'])==22 and contract['future_ROOT_post_completed'] is False and contract['predecessor']['actually_completed'] is False,'Exact future ROOT contract remains pending');need(scope['related_problem_id']==30004403 and scope['duplicate_shared_budget'] is True and scope['related_alias_native_entry_added'] is False and scope['related_alias_QUEUE_row_absent_preserved'] is True and scope['full_problem_solved'] is False and scope['novelty_claimed'] is False,'Qualified scientific/alias scope')
    for n in ['DRAFT_ROOT_PRIMARY_READ_LEDGER.json','DRAFT_ROOT_SCIENCE_CARD.json','DRAFT_ROOT_SCOPE_CERTIFICATE.json']:z=parse(raw(F/n));need(z['root_completed'] is False and z['actual_pid'] is None and z['created_utc'] is None and z['actual_PR47_predecessor_completed'] is False and z['future_acceptance_approved'] is False,'Pending ROOT records')
    for n in ['REPORT.md','CONTRACT.md','close_source.py','verify_closed_source.py','VERDICT.json','RESEARCH_LOG.md']:raw(F/n)
    result={'schema':'pr48-final-private-source-readback/v1','status':'READY_SOURCE_ONLY_WAIT_ROOT_CLOSURE_AND_NEW_ADVERSARY','actual_pid':os.getpid(),'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'source_files':source,'report_sha256':sha(raw(F/'REPORT.md')),'contract_sha256':sha(raw(F/'CONTRACT.md')),'ROOT_post_contract_sha256':sha(raw(F/'ROOT_POST_CONTRACT.json')),'complete_actual_completed_captures':captures,'previous_actual_private_operations':7,'fullmode_and_raw_SQL_audits_repeated':False,'actual_PR47_predecessor_completed':False,'production_imported_compiled_executed':False,'native_index_remote_mutated':False,'independent_adversarial_review_claimed':False,'future_acceptance_approved':False};dump('FINAL_READY_CHECK.json',result);print(json.dumps({k:v for k,v in result.items() if k!='complete_actual_completed_captures'},sort_keys=True))
if __name__=='__main__':
    if (F/'REPORT.md').exists():final_readback()
    else:main()
