"""Independent read-only source/input audit; never loads candidate modules."""
from pathlib import Path, PurePosixPath
import ast, copy, datetime as dt, hashlib, json, os, stat, subprocess

H = Path(__file__).resolve().parent
A = H.parent
R = A.parents[2]
P = A / 'acceptance_preparation_family'
C = A / 'reviewed_candidate'
W = A / 'whole_current_source_first_family'
checks = []
read_rows = []
def demand(ok, label):
    if not ok: raise ValueError(label)
    checks.append(label)
def sha(raw): return hashlib.sha256(raw).hexdigest()
def decode(raw):
    def pairs(xs):
        out = {}
        for k, v in xs:
            if k in out: raise ValueError('duplicate JSON key ' + k)
            out[k] = v
        return out
    return json.loads(raw, object_pairs_hook=pairs)
def load(p): return decode(p.read_bytes())
def same(x,y):
    if type(x) is not type(y): return False
    if type(x) is dict: return x.keys() == y.keys() and all(same(x[k],y[k]) for k in x)
    if type(x) is list: return len(x) == len(y) and all(same(a,b) for a,b in zip(x,y))
    return x == y
def read_pin(p, row, frozen=False):
    demand(p.is_file() and not p.is_symlink(), 'regular ' + str(p))
    raw = p.read_bytes()
    n = row.get('bytes',row.get('size'))
    demand(type(n) is int and len(raw) == n and sha(raw) == row['sha256'], 'full hash ' + str(p))
    if frozen: demand(stat.S_IMODE(p.stat().st_mode) == 0o444, 'S_IMODE0444 ' + str(p))
    read_rows.append({'path':str(p),'bytes':len(raw),'sha256':sha(raw),'mode':stat.S_IMODE(p.stat().st_mode)})
    return raw
def closure(base, name, pin, count):
    raw = (base/name).read_bytes(); obj = decode(raw)
    demand(sha(raw)==pin,'literal manifest hash '+str(base))
    demand(obj['self_excluded']==[name] and type(obj['files_count']) is int and obj['files_count']==count==len(obj['files']), 'exact self/count '+str(base))
    names = set()
    for row in obj['files']:
        n = row['path']; demand(type(n) is str and str(PurePosixPath(n))==n and not PurePosixPath(n).is_absolute() and not {'..','.git','__pycache__'}.intersection(PurePosixPath(n).parts), 'safe member '+n)
        demand(n not in names,'unique member '+n);names.add(n)
        raw_member = read_pin(base/n,row,True)
        if n.endswith('.json'): decode(raw_member)
        if n.endswith('.jsonl'):
            demand(not raw_member or raw_member.endswith(b'\n'),'complete JSONL '+n)
            for line in raw_member.splitlines(): decode(line)
    names.add(name)
    files, dirs = set(), set()
    for p in base.rglob('*'):
        demand(not p.is_symlink() and (p.is_file() or p.is_dir()),'regular exact topology '+str(p))
        (files if p.is_file() else dirs).add(p.relative_to(base).as_posix())
    expected_dirs = {d.as_posix() for n in names for d in PurePosixPath(n).parents if d.as_posix()!='.'}
    demand(files==names and dirs==expected_dirs,'exact recursive topology '+str(base))
    demand(stat.S_IMODE((base/name).stat().st_mode)==0o444,'self literal0444 '+str(base))
    return obj

prep = closure(P,'PREPARATION_MANIFEST.json','48358afc32922caefd8cb0fad5a59c52352d86261c5da3429e33c627c8afbe31',27)
inputs = load(P/'INPUT_BINDINGS.json')
current = closure(C,'MANIFEST.json',inputs['current_manifest_sha256'],385)
deps = load(C/'CURRENT_DEPENDENCIES.json')
demand(sha((C/'CURRENT_DEPENDENCIES.json').read_bytes())==inputs['current_dependencies_sha256'] and len(deps['files'])==517,'exact dependency manifest517')
for z in deps['files']:read_pin(A/z['path'],z)
whole = closure(W,'OWN_CLOSED_MANIFEST.json',inputs['closed_whole_manifest']['sha256'],25)
foreign = whole['foreign_files_indiv idually_pinned_and_excluded'.replace(' ','')]
demand(len(foreign)==925 and len({z['path'] for z in foreign})==925,'whole925 individual unique rows')
for z in foreign:
    p = Path(z['path']);demand(p.is_absolute() and p.is_relative_to(R),'foreign actual repository origin')
    read_pin(p,z)
for z in inputs['pins'].values():read_pin(R/z['path'],z)
for k in ['closed_whole_result','closed_whole_report','closed_root_whole_inspection','root_capture_operator']:read_pin(R/inputs[k]['path'],inputs[k])

# Every production line is read and parsed as syntax; none is compiled or run.
for n in ['pr42_guards.py','seal_final_evidence.py','integrate_reviewed_partial.py','state_mirror_reconciliation.py','verify_post_acceptance.py']:
    raw = (P/n).read_bytes();tree=ast.parse(raw,filename=str(P/n))
    demand(type(tree) is ast.Module,'syntax only '+n)
mirror = R/'draft_pr_publication_program_20260930/infrastructure/accepted_state_sync/revision2/accepted_state_sync_v2.py'
demand(sha(mirror.read_bytes())=='ca7576ece5bc37a6e569a62764541de773243d38bffa811f4d1174f25635667f','actual reviewed native mirror source')
ast.parse(mirror.read_bytes(),filename=str(mirror))
for capture in ['AUTHORING_ACTUAL_CAPTURE','CONTROLS_ACTUAL_CAPTURE']:
    d=P/capture;o=load(d/'CAPTURE.json')
    demand(type(o['pid']) is int and o['pid']>0 and o['completed'] is True and o['exit_code']==0,'actual preparation capture '+capture)
    for k in ['stdout','stderr']:read_pin(d/o[k]['path'],o[k])
    demand(sha((d/'PRELAUNCH_SOURCE.py').read_bytes())==o['source_sha256'],'entire preparation prelaunch '+capture)
    demand(dt.datetime.fromisoformat(o['started_utc'])<=dt.datetime.fromisoformat(o['finished_utc']),'preparation clocks '+capture)

snap=load(A/'snapshot_manifest_v2.json')
demand(len(snap['files'])==17 and len(snap['changed_paths'])==18,'original17/diff18')
for z in snap['files']:
    raw=read_pin(A/'source_snapshot_v2'/z['path'],z)
    demand(raw==(C/'original_archive'/z['path']).read_bytes(),'original17 archived '+z['path'])
ledger_raw=(C/'turns.jsonl').read_bytes();ledger=[decode(z) for z in ledger_raw.splitlines()]
demand(sha(ledger_raw)=='60d0413980ac5f251913a26298692c5efc797d8f5084ca03e8d134472ab820e4' and ledger_raw.endswith(b'\n') and [z['turn'] for z in ledger]==[1,2] and all(type(z['turn']) is int for z in ledger),'original full ordered ledger2')
final=(C/'PARTIAL.md').read_bytes();review=(C/'review/PARTIAL.md').read_bytes()
final_header, final_body=final.split(b'## 1. Exact target and notation',1);review_header,review_body=review.split(b'## 1. Exact target and notation',1)
demand(final_body==review_body and final_header==review_header.replace(b'Separate adversarial review is pending.',b'Separate adversarial AI review passed; see [the report](review/REVIEW.md). This has not undergone human peer review.'),'actual PARTIAL difference restricted to exact review-status header')
demand(final==(A/'source_snapshot_v2/PARTIAL.md').read_bytes(),'original PARTIAL preserved')
demand(decode((A/'pinned_prior_report.json').read_bytes())=={} and (A/'pinned_prior_report.json').read_bytes()==(C/'root_evidence/pinned_prior_report.json').read_bytes(),'absent raw prior versus literal SQL fallback{}')
scope=load(P/'SCIENTIFIC_SCOPE.json');draft=load(P/'DRAFT_FINAL_PLAN.json');bd=load(P/'DRAFT_ROOT_IMMUTABLE_BINDINGS.json')
demand(same(draft['scientific_scope'],scope),'full exact science scope clone')
for o in [scope,draft,load(P/'SOURCE_STATUS.json')]:
    for k in ['full_problem_solved','novelty_claimed']:demand(o[k] is False,'explicit false '+k)
    for k in ['current_model','current_reasoning_effort','current_deadline_utc']:demand(k in o and o[k] is None,'explicit unknown current '+k)
    for k,v in [('original_substantive_attempts',2),('new_substantive_attempts',0),('audit_turns',0)]:demand(type(o[k]) is int and o[k]==v,'typed attempts '+k)
demand(scope['literal_target_status']=='UNSOLVED' and draft['partial_valid'] is None,'UNSOLVED with future partial_valid pending')
for k in ['root_full_current_read_completed','root_full_whole_read_completed','root_acceptance_source_review_completed','independent_whole_current_pass']:demand(draft[k] is False and bd[k] is False,'future authority remains false '+k)
for k in ['created_utc','whole_manifest','root_whole_inspection','root_capture_operator']:demand(bd[k] is None,'future binding null '+k)
keys=load(P/'CLOSED_WHOLE_RESULT_KEYS.json');result=load(W/'RESULT.json');root=load(A/'ROOT_WHOLE_CURRENT_REVIEW.json')
demand(len(keys)==43 and set(result)==set(keys),'entire actual whole43 field schema')
demand(same(root['complete_RESULT_object'],result) and root['future_execution_approved'] is False,'genuine ROOT whole full RESULT')
demand(result['mandatory_defects']==result['mandatory_corrections']==[] and result['full_problem_solved'] is False,'actual scoped whole disposition')
previous=load(R/inputs['pins']['previous/state_mirror_bindings.json']['path'])
demand(len(previous['entries'])==31 and 41 in previous['required_completed_prs'] and 42 not in previous['required_completed_prs'] and len(previous['duplicate_mirrors'])==1,'actual predecessor31 plus old duplicate')
for e in previous['entries']:
    b=e['budget'];demand(type(b['used']) is int and type(b['limit']) is int and 0<=b['used']<=b['limit'],'full predecessor typed budget '+e['id'])
    raw=(R/b['ledger']['path']).read_bytes();demand(sha(raw)==b['ledger']['sha256'],'individual prior ledger '+e['id'])
post=load(R/inputs['pins']['previous/post_acceptance_verification.json']['path']);rp=load(R/inputs['pins']['previous/ROOT_ACTUAL_POST_INSPECTION.json']['path'])
demand(same(rp['entire_post'],post) and post['targets']==32 and post['consumed_substantive_turns']==39 and post['primary_acceptances']==31 and post['fresh_native_mirror_noop'] is True,'actual predecessor full post/ROOT equality')

# Private finite controls use independent models, not extracted production code.
mutants=[]
for mode in [0o444,0o1444,0o2444,0o4444,0o644,0o0]:
    demand((stat.S_IMODE(stat.S_IFREG|mode)==0o444)==(mode==0o444),'full special-bit finite model '+oct(mode))
for label in ['bool','phantom','missing','reordered','extra']:
    bad=copy.deepcopy(ledger)
    if label=='bool':bad[0]['turn']=True
    elif label=='phantom':bad.append({'turn':3})
    elif label=='missing':bad.pop()
    elif label=='reordered':bad.reverse()
    else:bad[0]['extra']=None
    demand(not same(bad,ledger),'private exact ledger rejects '+label);mutants.append('ledger/'+label)
for label in ['unknown','missing','bool_integer','claim_full_solution','invent_model']:
    bad=copy.deepcopy(draft)
    if label=='unknown':bad['unknown']=None
    elif label=='missing':bad.pop('current_deadline_utc')
    elif label=='bool_integer':bad['original_substantive_attempts']=True
    elif label=='claim_full_solution':bad['full_problem_solved']=True
    else:bad['current_model']='invented'
    demand(not same(bad,draft),'private exact schema rejects '+label);mutants.append('schema/'+label)
inventory=load(R/'draft_pr_publication_program_20260930/inventory.json')
demand(len(inventory['items'])==180 and inventory['completed_count']==31,'actual before inventory180/31')
after=copy.deepcopy(inventory);clock=dt.datetime.now(dt.timezone.utc).isoformat();item=next(z for z in after['items'] if z['number']==42)
item.update(stage='complete',outcome='unsolved_accepted_partial',queue_status='unsolved',workflow_completion_estimate_percent=100,original_attempts='2/5',new_substantive_attempts=0,cumulative_attempts='2/5',paper_or_new_doi_or_tracker=False)
after.update(updated_at_utc=clock,last_checkpoint_utc=clock,completed_count=32,program_completion_estimate_percent=32/180*100,completion_estimate_percent=32/180*100,current_pr=43)
demand(sum(z.get('stage')=='complete' for z in after['items'])==32 and type(after['completion_estimate_percent']) is float and type(item['workflow_completion_estimate_percent']) is int,'private complete inventory derivation')
demand(all(same(x,y) for x,y in zip(inventory['items'],after['items']) if x['number']!=42),'private unrelated179 preservation')
for field,bad_value in [('completed_count',True),('completion_estimate_percent',32),('updated_at_utc',None),('last_checkpoint_utc','stale')]:
    bad=copy.deepcopy(after);bad[field]=bad_value;demand(not same(bad,after),'private inventory mutant '+field);mutants.append('inventory/'+field)
argv=['git','rev-parse','HEAD'];proc=subprocess.run(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'))
demand(proc.returncode==0,'read-only current HEAD query')
report={'schema':'pr42-acceptance-independent-source-static-controls/v1','status':'PASS_SOURCE_ONLY','actual_pid':os.getpid(),'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'checks':len(checks),'rejected_private_mutants':mutants,'preparation_members':27,'current_members':385,'dependencies':517,'whole_members':25,'whole_foreign_individual_rows':925,'whole_result_fields':43,'original_files':17,'original_ledger_entries':2,'observed_main_head':proc.stdout.decode().strip(),'read_only_git':{'argv':argv,'cwd':str(R),'exit_code':proc.returncode,'stdout':proc.stdout.decode(),'stderr':proc.stderr.decode()},'total_bound_reads':len(read_rows),'total_bound_bytes_read':sum(z['bytes'] for z in read_rows),'proposed_helpers_imported_compiled_executed':False,'native_helper_imported_compiled_executed':False,'private_controls_are_future_evidence':False,'native_Git_remote_people_mutations':False}
(H/'CONTROL_RESULT.json').write_text(json.dumps(report,indent=2)+'\n')
(H/'FOREIGN_READ_ROWS.json').write_text(json.dumps(read_rows,indent=2)+'\n')
print(json.dumps(report))
