"""Independent read-only authentication and model checks. Never executes the closure operator."""
from pathlib import Path
import ast, datetime, hashlib, json, os, subprocess
D = Path(__file__).resolve().parent
A = D.parent
C = A.parents[2]
R = Path('/Users/alec/Documents/Math')
GH = '/opt/homebrew/Cellar/gh/2.85.0/bin/gh'
GIT = '/opt/homebrew/Cellar/git/2.38.2/bin/git'
events = []
def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b): return hashlib.sha256(b).hexdigest()
def need(ok, label):
    if not ok: raise ValueError(label)
def dump(p, x): p.write_text(json.dumps(x, indent=2, sort_keys=True)+'\n')
def load(p): return json.loads(p.read_text())
def pin(p):
    need(p.is_file() and not p.is_symlink(), 'Missing or redirected file: '+str(p))
    b=p.read_bytes()
    return {'path':str(p),'bytes':len(b),'sha256':sha(b),'mode':p.stat().st_mode&0o7777}
def read(argv, cwd=C):
    start=utc()
    p=subprocess.Popen(argv,cwd=cwd,env={**os.environ,'GIT_OPTIONAL_LOCKS':'0'},stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err=p.communicate()
    events.append({'argv':argv,'cwd':str(cwd),'actual_child_PID':p.pid,'UTC_start':start,'UTC_end':utc(),'exit_code':p.returncode,'stdout_bytes':len(out),'stdout_sha256':sha(out),'stderr_bytes':len(err),'stderr_sha256':sha(err)})
    need(p.returncode==0, 'Read-only command failed')
    return out
operator=A/'close_pr126_published_braid_20261006.py'
plan_path=A/'CLOSURE_ONLY_PLAN_20261006.json'
ready_path=A/'ROOT_PUBLISHED_BRAID_DISPOSITION_READY_20261006.json'
note_path=A/'PROPOSED_CLOSING_COMMENT_20261006.md'
plan=load(plan_path); ready=load(ready_path)
need(plan['operator_sha256']==sha(operator.read_bytes()),'Operator/plan mismatch')
need(plan['closing_comment_sha256']==sha(note_path.read_bytes()),'Comment/plan mismatch')
need(plan['ready_science_sha256']==sha(ready_path.read_bytes()),'Ready/plan mismatch')
inputs={p.name:pin(p) for p in [operator,plan_path,ready_path,note_path]}
snap=D/('reviewed_inputs_'+plan['operator_sha256'][:12]+'_'+str(os.getpid())); snap.mkdir(exist_ok=False)
for p in [operator,plan_path,ready_path,note_path]: (snap/p.name).write_bytes(p.read_bytes())
tree=ast.parse(operator.read_text()); compile(tree,str(operator),'exec')
# Parse and compile only. The operator is never imported or executed.
api_definition=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='api')
api_definition_text=ast.unparse(api_definition)
need("'--hostname', 'github.com'" in api_definition_text,'Explicit hostname binding absent')
api_calls=[]
for node in sorted(ast.walk(tree),key=lambda n:getattr(n,'lineno',0)):
    if isinstance(node,ast.Call) and isinstance(node.func,ast.Name) and node.func.id=='api':
        args=[x.value if isinstance(x,ast.Constant) else ast.unparse(x) for x in node.args]
        api_calls.append(args)
mutations=[x for x in api_calls if '--method' in x]
need(len(mutations)==2,'Unexpected static API mutation count')
need(mutations[0][0]=='repos/AlecKriebel/Math/issues/126/comments' and 'POST' in mutations[0], 'Wrong comment mutation')
need(mutations[1][0]=='repos/AlecKriebel/Math/pulls/126' and 'PATCH' in mutations[1], 'Wrong closure mutation')
manifest_path=A/ready['fresh_review_manifest']; manifest=load(manifest_path)
need(sha(manifest_path.read_bytes())==ready['fresh_review_manifest_sha256'],'Fresh seal mismatch')
fresh=[]
for name,expected in manifest['public_artifacts'].items():
    actual=pin(manifest_path.parent/name)
    need(actual['bytes']==expected['bytes'] and actual['sha256']==expected['sha256'],'Fresh member mismatch '+name)
    fresh.append(actual)
need(len(fresh)==44,'Unexpected scientific member count')
auth_path=A/'original_head_authentication_20261006/ORIGINAL_AUTHENTICATION.json'
need(sha(auth_path.read_bytes())==ready['original_authentication_sha256'],'Original authentication mismatch')
auth=load(auth_path); original=[]
for expected in auth['original_files']:
    actual=pin(auth_path.parent/'original_attempt'/expected['path'])
    need(actual['bytes']==expected['bytes'] and actual['sha256']==expected['sha256'],'Original member mismatch '+expected['path'])
    original.append(actual)
need(len(original)==16,'Unexpected original member count')
protected=[]
for expected in plan['protected_primary_full_index_and_eight_held_body_pins']+[plan['protected_isolated_full_index_pin']]:
    actual=pin(Path(expected['path'])); need(actual==expected,'Physical custody pin changed'); protected.append(actual)
need(len(protected)==10,'Full physical custody coverage changed')
local=read([GIT,'rev-parse','HEAD']).decode().strip()
primary=read([GIT,'rev-parse','HEAD'],R).decode().strip()
remote=read([GIT,'ls-remote','origin','refs/heads/main']).decode().split()[0]
need(local==plan['expected_local_main'] and remote==plan['expected_remote_main'] and primary==plan['primary_HEAD'],'Read-only main/primary pins changed')
pr=json.loads(read([GH,'api','--hostname','github.com','repos/AlecKriebel/Math/pulls/126']))
live={k:pr[k] for k in ['number','state','draft','merged','merged_at','closed_at','html_url']}|{'head_sha':pr['head']['sha'],'base_ref':pr['base']['ref']}
need(live['number']==126 and live['state']=='open' and live['draft'] and not live['merged'] and live['merged_at'] is None and live['head_sha']==plan['original_head'] and live['html_url']=='https://github.com/AlecKriebel/Math/pull/126','Live review input changed')
pages=json.loads(read([GH,'api','--hostname','github.com','repos/AlecKriebel/Math/issues/126/comments','--paginate','--slurp']))
matches=[x for page in pages for x in page if '<!-- pr126-old-published-braid-disposition-20261006 -->' in x['body']]
need(len(matches)<=1,'Duplicate marker')
need(all(x['body']==note_path.read_text() for x in matches),'Marker content changed')
# Independent finite guard models; these are not extracted/executed operator functions.
def is_open(p):
    return p['number']==126 and p['state']=='open' and p['draft'] and p['head_sha']==plan['original_head'] and p['base_ref']=='main' and p['url']=='https://github.com/AlecKriebel/Math/pull/126' and not p['merged']
base={'number':126,'state':'open','draft':True,'head_sha':plan['original_head'],'base_ref':'main','merged':False,'url':'https://github.com/AlecKriebel/Math/pull/126'}
head_guard_results=[]
for field,value in [('number',127),('state','closed'),('draft',False),('head_sha','0'*40),('base_ref','other'),('merged',True),('url','https://wrong-host.example/AlecKriebel/Math/pull/126')]:
    corrupt=base|{field:value}; rejected=not is_open(corrupt); need(rejected,'Guard accepts '+field); head_guard_results.append({'field':field,'rejected':rejected})
wrong_host_model_accepted=is_open(base|{'url':'https://wrong-host.example/AlecKriebel/Math/pull/126'})
need(not wrong_host_model_accepted,'Wrong-host guard model still accepted')
instant=datetime.datetime(2026,10,6,22,15,tzinfo=datetime.timezone.utc)
def interval_ok(start,end): return instant>=start and instant<end
timing=[]
for label,start,end,expected in [
 ('valid',instant-datetime.timedelta(seconds=1),instant+datetime.timedelta(seconds=1),True),
 ('not yet effective',instant+datetime.timedelta(seconds=1),instant+datetime.timedelta(seconds=2),False),
 ('exact expiration',instant-datetime.timedelta(seconds=1),instant,False),
 ('expired',instant-datetime.timedelta(seconds=2),instant-datetime.timedelta(seconds=1),False),
 ('empty interval',instant,instant,False)]:
    actual=interval_ok(start,end); need(actual==expected,'Interval model mismatch'); timing.append({'case':label,'accepted':actual})
for name,p in inputs.items(): need(pin(Path(p['path']))==p,'Input changed during review '+name)
need(not (A/'actual_closure_20261006').exists(),'Actual closure appeared during read-only review')
result={'schema':'pr126-independent-readonly-protocol-authentication/v1','UTC':utc(),'actual_recorder_PID':os.getpid(),'exact_reviewed_inputs':inputs,'input_snapshot':str(snap),'static_API_mutations':mutations,'explicit_host_API_definition':api_definition_text,'fresh_science_manifest_pin':pin(manifest_path),'original_authentication_pin':pin(auth_path),'all44_scientific_members':fresh,'all16_original_members':original,'all10_protected_physical_file_pins':protected,'local_main':local,'remote_main':remote,'primary_HEAD':primary,'live_PR':live,'existing_exact_marker_comment_count':len(matches),'independent_head_guard_negative_controls':head_guard_results,'independent_time_interval_controls':timing,'revised_open_guard_accepts_wrong_host_model':wrong_host_model_accepted,'operator_executed':False,'mutations_performed':False,'new_central_proof_search_turns':0,'original_effort':'1/5','completion_estimate_percent':90}
dump(D/'READONLY_AUTHENTICATION_AND_GUARD_MODELS.json',result)
dump(D/'PROCESS_JOURNAL.json',{'actual_recorder_PID':os.getpid(),'UTC':utc(),'read_only_child_events':events})
print(json.dumps({'PID':os.getpid(),'UTC':result['UTC'],'operator_sha256':plan['operator_sha256'],'plan_sha256':inputs[plan_path.name]['sha256'],'science_members':len(fresh),'original_members':len(original),'physical_pins':len(protected),'wrong_host_accepted_by_original_open_guard':wrong_host_model_accepted,'mutations':False},sort_keys=True))
