"""Current original Git/API, manifests, raw dataset and native replay bindings."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,subprocess
A=Path(__file__).resolve().parent;P=A.parents[1];R=P.parent
D=A/'root_authentication_private';D.mkdir(exist_ok=False)
utc=lambda:datetime.now(timezone.utc).isoformat()
sha=lambda b:hashlib.sha256(b).hexdigest()
def run(label,args):
    t=utc();q=subprocess.run(args,cwd=R,capture_output=True)
    for n,b in [('stdout',q.stdout),('stderr',q.stderr)]:(D/(label+'.'+n)).write_bytes(b)
    j=dict(argv=args,cwd=str(R),started_utc=t,ended_utc=utc(),exit_code=q.returncode,
           stdout_bytes=len(q.stdout),stdout_sha256=sha(q.stdout),stderr_bytes=len(q.stderr),stderr_sha256=sha(q.stderr))
    (D/(label+'.json')).write_text(json.dumps(j,indent=2)+'\n');assert q.returncode==0,(label,q.stderr.decode(errors='replace'))
    return q.stdout
m=json.loads((A/'snapshot_manifest.json').read_bytes());assert m['pr']==316 and len(m['files'])==19
api=json.loads(run('live_pr',['gh','api','repos/AlecKriebel/Math/pulls/316']))
assert api['state']=='open' and api['draft'] and api['head']['sha']==m['head']
pages=json.loads(run('live_files',['gh','api','--paginate','--slurp','repos/AlecKriebel/Math/pulls/316/files']))
live={e['filename']:e for page in pages for e in page};assert set(live)=={e['path'] for e in m['files']}
for i,e in enumerate(m['files']):
    b=(A/'snapshot'/e['path']).read_bytes();assert len(b)==e['bytes'] and sha(b)==e['sha256']
    assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==e['git_blob_sha']==live[e['path']]['sha']
    assert run('object_'+str(i),['git','show',m['head']+':'+e['path']])==b
    tree=run('mode_'+str(i),['git','ls-tree',m['head'],'--',e['path']]).split(b'\t',1)[0].split()
    assert tree==[b'100644',b'blob',e['git_blob_sha'].encode()]
target=A/'snapshot'/m['target_prefix']
counts={}
for manifest,style in [('TURN_1_MANIFEST.json','dict'),('PUBLICATION_MANIFEST.json','dict'),('review/REVIEW_MANIFEST.json','list')]:
    obj=json.loads((target/manifest).read_bytes());entries=obj['files'];rows=entries.items() if style=='dict' else ((e['path'],e) for e in entries)
    count=0
    for name,e in rows:
        q=(target/'review'/name) if manifest.startswith('review/') else target/name;b=q.read_bytes()
        assert len(b)==e['bytes'] and sha(b)==e['sha256']
        if 'git_blob_sha1' in e:assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==e['git_blob_sha1']
        count+=1
    counts[manifest]=count
rawmanifest=json.loads((R/'unsolved_math_prioritization/manifest.json').read_bytes());rawpins={};data={}
assert rawmanifest['revision']=='37e53eabe540fb458758e198be61634bd02ee008'
for n,e in rawmanifest['files'].items():
    q=R/'unsolved_math_prioritization/cache'/n;b=q.read_bytes()
    assert len(b)==e['bytes'] and sha(b)==e['sha256'];rawpins[n]=e;data[n]=json.loads(b)
problems=data['problems.json'];reports=data['research_results.json']
hits=[x for x in problems if str(x['id'])=='9900002'];assert len(hits)==1;problem=hits[0]
assert sum(x['problem_number']==problem['problem_number'] for x in problems)==1
prior=reports[problem['problem_number']];imported=json.loads((A/'source_inputs/imported_record.json').read_bytes())
assert imported['problem']==problem and imported['prior_research']==prior
assert sha(json.dumps([problem,prior],sort_keys=True).encode())==imported['review_hash']
adjacent=[x for x in problems if str(x['id']) in ['9900001','9900003']]
(D/'adjacent_source_records.json').write_text(json.dumps(adjacent,indent=2,ensure_ascii=False)+'\n')
replays={}
for label,expected in [('pr316_original_author_actual001',target/'TURN_1_CHECKS.json'),('pr316_original_reviewer_actual001',target/'review/independent_output.json')]:
    d=A/'root_runs_private'/label;j=json.loads((d/'execution.json').read_bytes());b=(d/'stdout.bin').read_bytes()
    assert j['exit_code']==0 and not (d/'stderr.bin').read_bytes() and b==expected.read_bytes()
    for e in j['programs']:
        q=Path(e['path']);assert len(q.read_bytes())==e['bytes'] and sha(q.read_bytes())==e['sha256']
    replays[label]=j
result=dict(utc=utc(),status='PASS_CURRENT_PR316_ORIGINAL_GIT_API_MANIFEST_RAW_SOURCE_AND_TWO_REPLAY_BINDINGS',
    original_head=m['head'],original_target_files=18,original_changed_paths=19,
    all_original_API_Git_disk_bytes_modes_equal=True,manifest_bound_counts=counts,
    raw_dataset_revision=rawmanifest['revision'],raw_dataset_files=rawpins,
    exact_raw_dataset_imported_problem_and_report_equal=True,source_problem_id_unique=True,source_report_join_unique=True,
    review_hash=imported['review_hash'],full_native_replays=replays,
    capture_directory=str(D),mathematical_acceptance=False,priority_acceptance=False,
    primary_full_binary_pending=True,original_author_turn_count='1/5',workflow_percent=15)
(A/'ROOT_INITIAL_INPUT_BINDINGS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
