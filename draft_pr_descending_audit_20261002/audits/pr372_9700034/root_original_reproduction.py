"""Full original-byte, historical-checkpoint and private-output audit of PR372."""
from pathlib import Path
import concurrent.futures,datetime,hashlib,json,os,shutil,subprocess,sys
A=Path(__file__).resolve().parent;R=A.parents[2];PREFIX='problems/9700034_sirsn_maximal_routes';P=A/'snapshot'/PREFIX
W=A/'tmp/root_original';assert not W.exists();shutil.copytree(P,W)
O=A/'root_original_streams';O.mkdir(exist_ok=True);sha=lambda b:hashlib.sha256(b).hexdigest()
git=lambda *args:subprocess.check_output(['git',*args],cwd=R)
m=json.loads((A/'snapshot_manifest.json').read_bytes());assert len(m['files'])==49
for f in m['files']:
    b=(A/'snapshot'/f['path']).read_bytes();assert len(b)==f['bytes'] and sha(b)==f['sha256']
    assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==f['git_blob_sha']
    assert git('show',m['head']+':'+f['path'])==b
assert set(git('diff','--name-only',m['base'],m['head']).decode().splitlines())=={f['path'] for f in m['files']}
nested=[]
for name in [*[f'TURN_{i}_MANIFEST.json' for i in range(1,6)],'FINAL_AUTHOR_MANIFEST.json','PUBLICATION_MANIFEST.json','review/REVIEW_MANIFEST.json']:
    root=P/'review' if name.startswith('review/') else P
    entries=json.loads((P/name).read_bytes())['files'];assert len({f['path'] for f in entries})==len(entries)
    for f in entries:
        b=(root/f['path']).read_bytes();assert len(b)==f['bytes'] and sha(b)==f['sha256'],(name,f['path'])
    nested.append({'name':name,'sha256':sha((P/name).read_bytes()),'bindings':len(entries)})
history=['35cc2c374ea854e21e6beb50210bb087ceea0cdd','c4169ccae93d60469db1ddfa508946e8e427a6b3','9654de1e3f96dc6ee92b273afb4e2d56cd81f912','a50223882a24011ac53ea0283ebf34fcd578fd4d','6f29bc5129f519ef5d6cb8901f5abb35868c4d03']
for i,commit in enumerate(history,1):
    name=f'TURN_{i}_MANIFEST.json';mf=json.loads((P/name).read_bytes());assert mf['author_turns_used']==i
    assert git('show',commit+':'+PREFIX+'/'+name)==(P/name).read_bytes()
    for f in mf['files']:assert git('show',commit+':'+PREFIX+'/'+f['path'])==(P/f['path']).read_bytes()
    if i>1:assert mf['previous_manifest_sha256']==sha((P/f'TURN_{i-1}_MANIFEST.json').read_bytes())
    state=json.loads((P/('STATE.json' if i==1 else f'STATE_T{i}.json')).read_bytes());assert state['substantive_author_turns_used']==i and state['original_target_resolved'] is False
author={f['path'] for f in json.loads((P/'FINAL_AUTHOR_MANIFEST.json').read_bytes())['files']}|{'FINAL_AUTHOR_MANIFEST.json'};assert len(author)==38
wip=history[-1];actual={p[len(PREFIX)+1:] for p in git('ls-tree','-r','--name-only',wip,'--',PREFIX).decode().splitlines()};assert actual==author
H=A/'tmp/root_historical_author';H.mkdir();
for name in author:
    b=git('show',wip+':'+PREFIX+'/'+name);assert b==(P/name).read_bytes();p=H/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
source=json.loads((P/'SOURCE_MANIFEST.json').read_bytes())['files']
for f in source:
    b=(A/'raw_sources'/f['name']).read_bytes();assert len(b)==f['bytes'] and sha(b)==f['sha256']
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');runs=[]
def run(label,argv,expected=None,expect_json=True):
    r=subprocess.run(argv,cwd=W,env=env,capture_output=True)
    (O/(label+'.stdout')).write_bytes(r.stdout);(O/(label+'.stderr')).write_bytes(r.stderr)
    assert r.returncode==0 and r.stderr==b'',(label,r.returncode,r.stderr.decode())
    if expected is not None:
        assert r.stdout==expected,label
        if expect_json:assert json.loads(r.stdout)==json.loads(expected)
    result={'label':label,'returncode':0,'stdout_sha256':sha(r.stdout),'stdout_bytes':len(r.stdout),'stderr_sha256':sha(r.stderr),'entire_stdout_exact':expected is not None,'entire_json_exact':expected is not None and expect_json}
    print(label+': PASS',flush=True);return result
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:runs=list(pool.map(lambda i:run(f'turn{i}',[sys.executable,'-B',str(W/f'check_turn_{i}.py')],(P/f'TURN_{i}_CHECKS.json').read_bytes()),range(1,6)))
runs.append(run('historical_independent',[sys.executable,'-B',str(W/'review/independent_check.py')],(P/'review/INDEPENDENT_CHECKS.json').read_bytes()))
runs.append(run('historical_author_wrapper',[sys.executable,'-B',str(W/'review/replay_author.py'),str(H)],(P/'review/AUTHOR_REPLAY.json').read_bytes()))
for supplied in [False,True]:
    label='packet_sources' if supplied else 'packet_no_sources';argv=[sys.executable,'-B',str(W/'verify_packet.py')]
    if supplied:argv+=['--source-dir',str(A/'raw_sources')]
    expected={'status':'PASS','public_bindings_checked':64,'replays':[{'turn':i,'exact_assertions':json.loads((P/f'TURN_{i}_CHECKS.json').read_bytes())['exact_assertions'],'stdout_byte_exact':True} for i in range(1,6)],'total_exact_assertions':503419,'source_files_checked':4 if supplied else 0,'source_check':'verified' if supplied else 'not requested; raw sources are not distributed'}
    stdout=(json.dumps(expected,indent=2,sort_keys=True)+'\n').encode();runs.append(run(label,argv,stdout))
    label='publication_sources' if supplied else 'publication_no_sources';argv=[sys.executable,'-B',str(W/'verify_publication.py')]
    if supplied:argv+=['--source-dir',str(A/'raw_sources')]
    stdout+=b'PASS: all publication bytes, frozen author replays and 2507 independent controls; original unsolved 5/5\n'
    runs.append(run(label,argv,stdout,False))
for f in m['files']:
    if f['path'].startswith(PREFIX+'/'):assert sha((W/f['path'][len(PREFIX)+1:]).read_bytes())==f['sha256']
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_COMPLETE_ORIGINAL_REPRODUCTION','workflow_percent':70,'general_resolution_percent':0,'all_49_original_git_api_manifest_paths_exact':True,'all_48_target_files_exact_and_unchanged_by_replay':True,'all_38_immutable_WIP_author_files_exact':True,'five_historical_checkpoints_exact':history,'nested_manifest_bindings':sum(x['bindings'] for x in nested),'manifests':nested,'four_fresh_primary_matches':source,'all_nine_verification_programs_and_helpers_read_in_full_before_execution':True,'runs':runs,'author_assertions':503419,'historical_review_assertions':2507,'historical_author_wrapper_64_bindings_exact_on_actual_38_file_WIP':True,'source_fetch_by_submitted_programs':False,'original_problem':'Ordinary SIRSN expected sampled maximum unresolved,5/5.','fresh_family_and_whole_final_gates_pending':True}
(A/'root_original_reproduction_receipt.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'runs':len(runs),'nested_manifest_bindings':out['nested_manifest_bindings'],'author':503419,'historical_review':2507}))
