"""Own handwritten finite controls and syntax inspection; no proposed source execution."""
from pathlib import Path
import ast,copy,datetime as dt,hashlib,json,stat,os
H=Path(__file__).resolve().parent;A=H.parent;R=A.parents[2]
checks=[]
def demand(ok,label):
    if not ok:raise ValueError(label)
    checks.append(label)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def load(p):return json.loads(p.read_bytes())
def equal(a,b):
    if type(a) is not type(b):return False
    if type(a) is dict:return a.keys()==b.keys() and all(equal(a[k],b[k]) for k in a)
    if type(a) is list:return len(a)==len(b) and all(equal(x,y) for x,y in zip(a,b))
    return a==b
def rows_check(base,rows,frozen=False):
    names=[]
    for z in rows:
        p=base/z['path'];raw=p.read_bytes();names.append(z['path'])
        demand(p.is_file() and not p.is_symlink(),str(p)+': regular')
        demand(type(z['bytes']) is int and len(raw)==z['bytes'] and sha(raw)==z['sha256'],str(p)+': full bytes')
        if frozen:demand(stat.S_IMODE(p.stat().st_mode)==0o444,str(p)+': full literal0444')
    demand(len(names)==len(set(names)),'Unique complete rows '+str(base))
def closure(base,mf,pin,count):
    raw=(base/mf).read_bytes();demand(sha(raw)==pin,'Actual closed hash '+str(base));o=json.loads(raw)
    demand(o['self_excluded']==[mf] and o['files_count']==len(o['files'])==count,'Actual self-only count '+str(base))
    rows_check(base,o['files'],True)
    files={p.relative_to(base).as_posix() for p in base.rglob('*') if p.is_file()};demand(files=={z['path'] for z in o['files']}|{mf},'Exact actual file closure '+str(base))
    dirs={p.relative_to(base).as_posix() for p in base.rglob('*') if p.is_dir()};expected={q.as_posix() for n in files for q in Path(n).parents if q.as_posix()!='.'}
    demand(dirs==expected and stat.S_IMODE((base/mf).stat().st_mode)==0o444,'Exact directory/mode closure '+str(base))
    return o
inputs=load(H/'INPUT_BINDINGS.json');draft=load(H/'DRAFT_FINAL_PLAN.json');binding_draft=load(H/'DRAFT_ROOT_IMMUTABLE_BINDINGS.json')
for n,pin in inputs['pins'].items():rows_check(R,[pin])
C=A/'reviewed_candidate';W=A/'whole_current_source_first_family'
current=closure(C,'MANIFEST.json',inputs['current_manifest_sha256'],385)
deps=load(C/'CURRENT_DEPENDENCIES.json');demand(sha((C/'CURRENT_DEPENDENCIES.json').read_bytes())==inputs['current_dependencies_sha256'] and len(deps['files'])==517,'Exact complete517 portable dependencies');rows_check(A,deps['files'])
whole=closure(W,'OWN_CLOSED_MANIFEST.json',inputs['closed_whole_manifest']['sha256'],25)
foreign=whole['foreign_files_individually_pinned_and_excluded'];demand(len(foreign)==925,'Whole925 individually read foreign rows')
for z in foreign:
    p=Path(z['path']);demand(p.is_relative_to(R),'Absolute actual whole foreign origin');raw=p.read_bytes();demand(type(z['bytes']) is int and len(raw)==z['bytes'] and sha(raw)==z['sha256'],'Exact actual foreign full bytes '+str(p))
for n in ['closed_whole_result','closed_whole_report','closed_root_whole_inspection','root_capture_operator']:rows_check(R,[inputs[n]])
verdict=load(W/'RESULT.json');demand(verdict['mandatory_corrections']==verdict['mandatory_defects']==[] and verdict['scoped_mathematics_verified'] is True and verdict['full_problem_solved'] is False,'Actual new whole scoped disposition')
demand(load(A/'ROOT_WHOLE_CURRENT_REVIEW.json')['complete_RESULT_object']==verdict and load(A/'ROOT_WHOLE_CURRENT_REVIEW.json')['future_execution_approved'] is False,'Actual ROOT full RESULT; future approval false')
snapshot=load(A/'snapshot_manifest_v2.json');demand(len(snapshot['files'])==17 and len(snapshot['changed_paths'])==18,'Original17/diff18 actual schema')
for z in snapshot['files']:
    raw=(A/'source_snapshot_v2'/z['path']).read_bytes();demand(raw==(C/'original_archive'/z['path']).read_bytes(),'Byte-exact original archive '+z['path'])
turns_raw=(C/'turns.jsonl').read_bytes();turns=[json.loads(z) for z in turns_raw.splitlines()]
demand(turns_raw.endswith(b'\n') and [z['turn'] for z in turns]==[1,2] and all(type(z['turn']) is int for z in turns),'Exact original ordered typed JSONL2')
demand(load(A/'pinned_prior_report.json')=={} and (A/'pinned_prior_report.json').read_bytes()==(C/'root_evidence/pinned_prior_report.json').read_bytes(),'Absent raw prior exact{} SQL fallback')
cap=load(A/'root_current_freeze_actual_capture/CAPTURE.json');demand(cap['pid']==60795 and cap['completed'] is True and cap['exit_code']==0 and cap['native13_before']==cap['native13_after'] and cap['main_head_before']==cap['main_head_after'],'Actual freeze capture preserved')
for n in ['pr42_guards.py','integrate_reviewed_partial.py','seal_final_evidence.py','state_mirror_reconciliation.py','verify_post_acceptance.py']:
    raw=(H/n).read_text();tree=ast.parse(raw,filename=n);demand(isinstance(tree,ast.Module),'Syntax-only parsing, no compilation/execution '+n)
guard=(H/'pr42_guards.py').read_text();integration=(H/'integrate_reviewed_partial.py').read_text();mirror=(H/'state_mirror_reconciliation.py').read_text();post=(H/'verify_post_acceptance.py').read_text()
for fragment in ['stat.S_IMODE(regular(base,n).stat().st_mode)==0o444','Unknown critical closure schema','Complete prepared inputs','Exact current ROOT fresh input schema','Complete original-head preflight','Complete overlay schema','Complete prepush schema','Entire typed completed native intent','Unknown critical native mirror plan schema','derive_inventory','expected_acceptance','root_acceptance_source_review_completed=True','root_capture_operator','integration_state_before.json','integration_history_before.jsonl','Exactly one tracked native Git entry','Exact ignored cache must remain absent']:
    demand(fragment in guard,'Source explicit contract fragment '+fragment)
demand('[0-9a-f]{41}' not in guard and '[0-9a-f]{40}' in guard,'Actual full40-hex identity syntax')
demand('g.preflight_record(pins)' in integration and 'g.overlay_record(pins,frozen)' in integration and 'g.prepush_record(pins)' in integration,'All phase record checks invoked')
demand('g.mirror_proposal(proposal,pins)' in mirror and 'g.mirror_records(pins,pre,plan,intent,receipt,proposal)' in post,'Complete native critical schema checks invoked')
demand('frozen current packet of 2026-10-03T00:16:09.381522+00:00' in integration and 'root_approval' in integration,'Global dated pending/PASS interpretation')
demand(draft['partial_valid'] is None and all(draft[k] is False for k in ['root_full_current_read_completed','root_full_whole_read_completed','root_acceptance_source_review_completed','independent_whole_current_pass']),'All future plan flags false/null')
demand(binding_draft['created_utc'] is None and binding_draft['whole_manifest'] is None and binding_draft['root_whole_inspection'] is None and binding_draft['root_capture_operator'] is None,'Future bindings references are null')
for mode in [0o444,0o1444,0o2444,0o4444,0o644,0o0]:demand((stat.S_IMODE(stat.S_IFREG|mode)==0o444)==(mode==0o444),'Handwritten complete permission model '+oct(mode))
before=load(R/'draft_pr_publication_program_20260930/inventory.json');demand(len(before['items'])==180 and before['completed_count']==31,'Actual full180/31 before inventory')
# A private finite model in memory, never a future ROOT/remote receipt.
clock='2026-10-03T00:00:00+00:00';after=copy.deepcopy(before);item=next(z for z in after['items'] if z['number']==42)
item.update(stage='complete',outcome='unsolved_accepted_partial',queue_status='unsolved',audited_head=draft['original_head'],merge_commit='0'*40,merged_at=clock,workflow_completion_estimate_percent=100,original_attempts='2/5',new_substantive_attempts=0,cumulative_attempts='2/5',paper_or_new_doi_or_tracker=False)
after.update(updated_at_utc=clock,last_checkpoint_utc=clock,completed_count=32,program_completion_estimate_percent=32/180*100,completion_estimate_percent=32/180*100,current_pr=43)
demand(sum(z.get('stage')=='complete' for z in after['items'])==32,'Handwritten full inventory constructor private32 completions')
demand(type(item['workflow_completion_estimate_percent']) is int and type(after['completion_estimate_percent']) is float,'Private workflow integer/program float distinction')
demand(all(equal(a,b) for a,b in zip(before['items'],after['items']) if a['number']!=42),'Entire private unrelated179 inventory items preserved')
rejected=[]
for field,bad in [('completed_count',True),('completed_count',32.0),('program_completion_estimate_percent',None),('program_completion_estimate_percent',32),('completion_estimate_percent',False),('updated_at_utc',None),('last_checkpoint_utc','wrong'),('current_pr',42),('current_pr',True)]:
    obj=copy.deepcopy(after);obj[field]=bad;demand(not equal(obj,after),'Typed complete private inventory rejects '+field+'/'+repr(bad));rejected.append(field+'/'+repr(bad))
obj=copy.deepcopy(after);obj['items'][0]['phantom']=None;demand(not equal(obj,after),'Meaningful extra unrelated inventory field rejects');rejected.append('unrelated-extra')
for label in ['bool_turn','phantom_attempt','missing_turn','wrong_order','extra_field']:
    obj=copy.deepcopy(turns)
    if label=='bool_turn':obj[0]['turn']=True
    elif label=='phantom_attempt':obj.append({'turn':3})
    elif label=='missing_turn':obj.pop()
    elif label=='wrong_order':obj.reverse()
    else:obj[0]['extra']=None
    demand(not equal(obj,turns),'Exact handwritten original ledger mutant '+label);rejected.append(label)
for label in ['missing','unknown','bool','false-full-solution']:
    obj=copy.deepcopy(draft)
    if label=='missing':obj.pop('current_model')
    elif label=='unknown':obj['human_peer_review_asserted']=True
    elif label=='bool':obj['original_substantive_attempts']=True
    else:obj['full_problem_solved']=True
    demand(not equal(obj,draft),'Complete handwritten critical draft schema mutant '+label);rejected.append(label)
result={'schema':'pr42-own-source-control-results/v1','status':'PASS_OWN_HANDWRITTEN_CONTROLS_AND_SYNTAX_ONLY','actual_pid':os.getpid(),'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'demands':len(checks),'finite_mutants_rejected':rejected,'proposed_helpers_imported_compiled_executed':False,'private_model_is_future_evidence':False,'native_Git_remote_people_mutations':False,'limitations':'Handwritten finite models and explicit source/syntax inspection do not execute the proposed administrative helpers or certify future phase success; independent acceptance-source adversary and ROOT personal read remain necessary.','current_members':385,'dependencies':517,'whole_owned_members':25,'whole_foreign_rows':925,'original_files':17,'original_jsonl_entries':2}
(H/'OWN_CONTROL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
