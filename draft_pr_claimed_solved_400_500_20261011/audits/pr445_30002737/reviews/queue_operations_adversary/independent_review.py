#!/usr/bin/env python3
"""Targeted independent controls; creates no real remote calls and no producer writes."""
import base64, copy, datetime, hashlib, importlib.util, json, os, subprocess, sys
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).absolute().parent
CASE=HERE.parents[1]
PRIVATE=CASE/'private_sources/queue_operations_adversary'
MIRROR=PRIVATE/'mirror/draft_pr_claimed_solved_400_500_20261011/audits/pr445_30002737'
COPIED=MIRROR/'status_operations/classify_pr445.py'
QUEUE='unsolved_math_prioritization/QUEUE.md'
HEAD='3242c84e06db7e99012c7fe581adde5c3f89fc89'

def require(value,message):
    if not value: raise RuntimeError(message)
def sha(data): return hashlib.sha256(data).hexdigest()
def blob(data): return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
def trees(leaves):
    folders={}
    for path,entry in leaves.items():
        node=folders; pieces=path.split('/')
        for part in pieces[:-1]: node=node.setdefault(part,{})
        node[pieces[-1]]=entry
    def visit(node):
        entries=[]
        for name,value in node.items():
            if set(value)=={'mode','type','sha'}: entries.append((name,value['mode'],value['type'],value['sha']))
            else: entries.append((name,'040000','tree',visit(value)))
        entries.sort(key=lambda e:e[0].encode()+(b'/' if e[2]=='tree' else b''))
        raw=b''.join(mode.lstrip('0').encode()+b' '+name.encode()+b'\0'+bytes.fromhex(digest) for name,mode,kind,digest in entries)
        return hashlib.sha1(b'tree '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
    return visit(folders)

def unit_checks():
    spec=importlib.util.spec_from_file_location('reviewed_helper',COPIED)
    module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    checks={}
    header=b'| Rank | DOI | Turns | Status | ID / code | Extra |\r\n'
    row=b'| 1 |  | 1/5 |  claimed_solved  | 30002737 / example | claimed_solved |\r\n'
    other=b'| 2 |  | 1/5 | claimed_solved | 222 / example | Z |'
    data=b'prefix\r\n'+header+b'|---|---|---|---|---|---|\r\n'+row+other
    expected=data.replace(row,row.replace(b'  claimed_solved  ',b'  already_solved  ',1),1)
    receipt={'queue_sha256':sha(data),'selected_queue_row':row.rstrip(b'\r\n').decode()}
    after,meta=module.queue_change(data,receipt)
    checks['reordered_header_crlf_no_final_newline_other_status_bytes']=after==expected and meta['status_column']==3
    for name,mutant in [('duplicate_selected_row',data+b'\r\n'+row),('duplicate_status_header',data.replace(b'Extra',b'Status'))]:
        r={'queue_sha256':sha(mutant),'selected_queue_row':receipt['selected_queue_row']}
        try: module.queue_change(mutant,r); checks[name]=False
        except module.Refusal: checks[name]=True
    for name,raw in [('duplicate_json',b'{"approved":true,"approved":true}'),('nonfinite_json',b'{"x":NaN}'),('root_list',b'[]')]:
        try: module.parse_json(raw); checks[name]=False
        except module.Refusal: checks[name]=True
    checks['all_pass']=all(checks.values())
    return checks

if '--unit-child' in sys.argv:
    print(json.dumps(unit_checks(),sort_keys=True)); raise SystemExit(0)

COPIED.parent.mkdir(parents=True,exist_ok=True)
original=(CASE/'status_operations/classify_pr445.py').read_bytes()
COPIED.write_bytes(original)
(MIRROR/'SOURCE_RECEIPT.json').write_bytes((CASE/'SOURCE_RECEIPT.json').read_bytes())
receipt=json.loads((MIRROR/'SOURCE_RECEIPT.json').read_text())
queue=(CASE/'private_sources/status_operations/frozen_QUEUE.md').read_bytes()
queuefile=PRIVATE/'opaque_frozen_QUEUE.md'; queuefile.write_bytes(queue)
source_paths={}
for entry in receipt['files']:
    data=(CASE/'source_snapshot'/entry['path']).read_bytes()
    target=MIRROR/'opaque_sources'/entry['path']; target.parent.mkdir(parents=True,exist_ok=True); target.write_bytes(data)
    require(len(data)==entry['bytes'] and sha(data)==entry['sha256'],'frozen source fixture does not match receipt')
    source_paths[entry['path']]=str(target)
leaves={path:{'mode':'100644','type':'blob','sha':blob(Path(file).read_bytes())} for path,file in source_paths.items()}
leaves[QUEUE]={'mode':'100644','type':'blob','sha':blob(queue)}
leaves['root_sibling.txt']={'mode':'100644','type':'blob','sha':'b'*40}
leaves['unsolved_math_prioritization/parent_sibling.txt']={'mode':'100644','type':'blob','sha':'c'*40}
base={'head':HEAD,'ref':HEAD,'old_tree':trees(leaves),'old_leaves':leaves,'queue_fixture':str(queuefile),'sources':source_paths,'calls':[]}
BINDIR=PRIVATE/'bin'; BINDIR.mkdir(exist_ok=True)
(BINDIR/'gh').write_bytes((HERE/'independent_gh.py').read_bytes()); (BINDIR/'gh').chmod(0o755)
bindings=[]
for role in ('root_disposition','priority','numeric_certificate_adversary'):
    f=MIRROR/'synthetic_bindings'/f'{role}.txt'; f.parent.mkdir(exist_ok=True); f.write_text('Independent offline fixture, not root approval.\n')
    bindings.append({'role':role,'path':str(f.relative_to(MIRROR)),'sha256':sha(f.read_bytes())})
gate={'schema':'pr445_queue_classification_gate_v1','repo':'AlecKriebel/Math','pr':445,'problem_id':'30002737','source_head':HEAD,'branch':'research/diffraction-dynamical-30002737','from_status':'claimed_solved','to_status':'already_solved','approved':True,'genuine_accepted_certificate':True,'source_receipt_sha256':sha((MIRROR/'SOURCE_RECEIPT.json').read_bytes()),'review_bindings':bindings}
# Tuple: scenario, expected exit, expected mutation count. Acceptance of race is an explicit API limit demonstration.
SCENARIOS=[('normal',0,4),('draft_integer',2,0),('head_repo_list',2,0),('source_bool_size',2,0),('source_wrong_git_sha',2,0),('old_tree_duplicate_name',2,0),('tree_truncated_integer_false',2,0),('blob_wrong_sha',2,1),('root_sibling_changed',2,2),('queue_parent_sibling_changed',2,2),('original_leaf_changed',2,2),('queue_mode_changed',2,2),('lost_tree_post',2,2),('lost_commit_post',2,3),('commit_wrong_parent',2,3),('commit_parent_nondict',2,3),('commit_two_parents',2,3),('compare_total_bool',2,3),('patch_lost_applied',3,4),('patch_lost_not_applied',2,4),('patch_reconcile_ref_lost',2,4),('patch_reconcile_queue_lost',2,4),('fresh_read_race_ancestor',0,4)]
raw=[]
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
for optimized in (False,True):
    for scenario,expected_exit,expected_mutations in SCENARIOS:
        label=('optimized_' if optimized else 'normal_')+scenario
        folder=PRIVATE/'runs'/label; folder.mkdir(parents=True,exist_ok=True)
        state=copy.deepcopy(base); state['scenario']=scenario
        statefile=folder/'state.json'; statefile.write_text(json.dumps(state,sort_keys=True))
        gatefile=MIRROR/'synthetic_gate.json'; gatefile.write_text(json.dumps(gate,sort_keys=True))
        argv=[sys.executable]+(['-O'] if optimized else [])+[str(COPIED),'apply','--gate',str(gatefile),'--expected-gate-sha256',sha(gatefile.read_bytes())]
        env=dict(os.environ,PATH=str(BINDIR)+os.pathsep+os.environ['PATH'],PR445_INDEPENDENT_STATE=str(statefile),PYTHONDONTWRITEBYTECODE='1')
        child_start=datetime.datetime.now(datetime.timezone.utc).isoformat()
        child=subprocess.run(argv,capture_output=True,text=True,env=env,timeout=45)
        state=json.loads(statefile.read_text()); calls=state['calls']
        parsed=json.loads(child.stdout)
        mutations=[c for c in calls if c['method']!='GET']; patches=[c for c in calls if c['method']=='PATCH']
        source_reads=[i for i,c in enumerate(calls) if c['endpoint'].startswith('contents/') and not c['endpoint'].startswith('contents/'+QUEUE+'?')]
        checks={'exit':child.returncode==expected_exit,'mutation_count':len(mutations)==expected_mutations,'one_patch_maximum':len(patches)<=1,'helper_sha_unchanged':sha(COPIED.read_bytes())==sha(original),'mutation_receipt_matches':len(parsed['mutation_attempts'])==len(mutations),'all_calls_fixed_repository':True}
        if expected_mutations:
            checks['all_12_BODY_checks_before_first_mutation']=len(source_reads)==12 and max(source_reads)<next(i for i,c in enumerate(calls) if c['method']!='GET') and len(parsed['originals_verified_before_change'])==12
        if patches:
            at=calls.index(patches[0]); post=calls[at+1:]
            checks['nonforce_patch']=patches[0]['body']['force'] is False
            checks['no_post_patch_source_BODY']=all(not c['endpoint'].startswith('contents/') or c['endpoint'].startswith('contents/'+QUEUE+'?') for c in post)
            checks['post_patch_admin_GETs_only']=all(c['method']=='GET' and c['endpoint'].startswith(('git/ref/','contents/'+QUEUE+'?','git/commits/','compare/')) for c in post)
            checks['one_ref_readback']=sum(c['endpoint'].startswith('git/ref/') for c in post)==1
            checks['at_most_one_queue_readback']=sum(c['endpoint'].startswith('contents/') for c in post)<=1
        if scenario in ('normal','fresh_read_race_ancestor','patch_lost_applied'):
            row=receipt['selected_queue_row'].encode(); expected=queue.replace(row,row.replace(b'claimed_solved',b'already_solved',1),1)
            checks['independent_exact_queue_bytes']=base64.b64decode(state['new_queue'])==expected
            checks['every_other_leaf_unchanged']=all(state['new_leaves'].get(path)==entry for path,entry in base['old_leaves'].items() if path!=QUEUE)
            checks['new_commit_has_one_frozen_parent']=next(c['body']['parents'] for c in calls if c['endpoint']=='git/commits' and c['method']=='POST')==[HEAD]
            checks['success_outcome']=parsed['outcome']==('applied_reconciled_uncertain_patch' if scenario=='patch_lost_applied' else 'applied_verified')
        if scenario=='fresh_read_race_ancestor': checks['race_limit_demonstrated']=bool(state.get('race_observed_at_patch')) and parsed['nonforce_patch_is_compare_and_swap'] is False
        record={'label':label,'started_at_utc':child_start,'ended_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'argv':argv,'returncode':child.returncode,'stdout':child.stdout,'stderr':child.stderr,'checks':checks,'actual_mutation_count':len(mutations),'actual_patch_count':len(patches),'actual_calls':[{'method':c['method'],'endpoint':c['endpoint'],'request_sha256':sha(json.dumps(c['body'],sort_keys=True).encode()) if c['body'] is not None else None} for c in calls]}
        raw.append(record)
    argv=[sys.executable]+(['-O'] if optimized else [])+[str(HERE/'independent_review.py'),'--unit-child']
    child=subprocess.run(argv,capture_output=True,text=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),timeout=30)
    checks=json.loads(child.stdout); checks['exit']=child.returncode==0
    raw.append({'label':('optimized_' if optimized else 'normal_')+'independent_unit_checks','argv':argv,'returncode':child.returncode,'stdout':child.stdout,'stderr':child.stderr,'checks':checks,'actual_mutation_count':0,'actual_patch_count':0,'actual_calls':[]})
(HERE/'RAW_INDEPENDENT_EXECUTIONS.json').write_text(json.dumps(raw,sort_keys=True,indent=2)+'\n')
failed=[r['label']+':'+k for r in raw for k,v in r['checks'].items() if not v]
summary={'schema':'pr445_independent_operational_controls_v1','started_at_utc':start,'completed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'helper_sha256':sha(original),'actual_child_executions':len(raw),'normal_child_executions':sum(r['label'].startswith('normal_') for r in raw),'optimized_child_executions':sum(r['label'].startswith('optimized_') for r in raw),'actual_offline_mutation_attempts':sum(r['actual_mutation_count'] for r in raw),'actual_offline_patch_attempts':sum(r['actual_patch_count'] for r in raw),'real_remote_mutations':0,'synthetic_gates_are_root_approval':False,'failed_checks':failed,'all_checks_passed':not failed,'raw_sha256':sha((HERE/'RAW_INDEPENDENT_EXECUTIONS.json').read_bytes())}
(HERE/'INDEPENDENT_CONTROL_RESULTS.json').write_text(json.dumps(summary,sort_keys=True,indent=2)+'\n')
print(json.dumps(summary,sort_keys=True,indent=2)); raise SystemExit(1 if failed else 0)
