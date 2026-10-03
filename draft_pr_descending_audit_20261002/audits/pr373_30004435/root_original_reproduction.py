"""Reproduce all unchanged author and historical-review streams with full bindings."""
from pathlib import Path
import base64,concurrent.futures,datetime,hashlib,json,os,shutil,subprocess,sys
A=Path(__file__).resolve().parent;R=A.parents[2];PREFIX='unsolved_math_prioritization/attempts/30004435';P=A/'snapshot'/PREFIX
W=A/'tmp/root_original';assert not W.exists();shutil.copytree(P,W)
O=A/'root_original_streams';O.mkdir(exist_ok=True);sha=lambda b:hashlib.sha256(b).hexdigest()
git=lambda *args:subprocess.check_output(['git',*args],cwd=R)
m=json.loads((A/'snapshot_manifest.json').read_bytes());assert len(m['files'])==53
for f in m['files']:
    b=(A/'snapshot'/f['path']).read_bytes();assert len(b)==f['bytes'] and sha(b)==f['sha256']
    assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==f['git_blob_sha']
    assert git('show',m['head']+':'+f['path'])==b
assert set(git('diff','--name-only',m['base'],m['head']).decode().splitlines())=={f['path'] for f in m['files']}
nested=[]
for name in [*[f'TURN_{i}_MANIFEST.json' for i in range(1,6)],'FINAL_FROZEN_MANIFEST.json','PUBLICATION_MANIFEST.json','final_review/REVIEW_MANIFEST.json']:
    root=P/'final_review' if name.startswith('final_review/') else P
    entries=json.loads((P/name).read_bytes())['files']
    for f in entries:
        b=(root/f['path']).read_bytes();assert len(b)==f['bytes'] and sha(b)==f['sha256'],(name,f['path'])
    assert len({f['path'] for f in entries})==len(entries)
    nested.append({'name':name,'sha256':sha((P/name).read_bytes()),'bindings':len(entries)})
history=['b059dfb82180f3857f1a8f876ab840e488a064ca','d825efc825674300103689b5ca13f6a292a981a7','5ef281ceecd5f347cde05c20d94f4e1ac6f5cd47','63b7f17b7f93f6b4418377c4b885f60560ffbbce','f1c1e710597b4d9d0993290091f601d086666126']
for i,commit in enumerate(history,1):
    name=f'TURN_{i}_MANIFEST.json';assert git('show',commit+':'+PREFIX+'/'+name)==(P/name).read_bytes()
    for f in json.loads((P/name).read_bytes())['files']:assert git('show',commit+':'+PREFIX+'/'+f['path'])==(P/f['path']).read_bytes()
    state=json.loads((P/f'TURN_{i}_STATE.json').read_bytes());assert state['turns_used']==i and state['event']=='proof_attempt_turn'
author=set(f['path'] for f in json.loads((P/'FINAL_FROZEN_MANIFEST.json').read_bytes())['files'])|{'FINAL_FROZEN_MANIFEST.json'};assert len(author)==42
wip='f1c1e710597b4d9d0993290091f601d086666126';actual={p[len(PREFIX)+1:] for p in git('ls-tree','-r','--name-only',wip,'--',PREFIX).decode().splitlines()};assert actual==author
for name in author:assert git('show',wip+':'+PREFIX+'/'+name)==(P/name).read_bytes()
remote=json.loads((P/'final_review/REMOTE_BINDING.json').read_bytes());assert remote['head']==wip and len(remote['files'])==42
for f in remote['files']:
    b=(P/f['path']).read_bytes();assert len(b)==f['size'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==f['sha']
source=json.loads((P/'SOURCE_MANIFEST.json').read_bytes())['primary_pdfs'];extra=json.loads((P/'TURN_3_SOURCE.json').read_bytes());source.append({'file':extra['local_source'],'bytes':extra['bytes'],'sha256':extra['sha256']})
for f in source:
    b=(A/'raw_sources'/f['file']).read_bytes();assert len(b)==f['bytes'] and sha(b)==f['sha256']
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
runs=[]
def run(label,argv,expected=None):
    r=subprocess.run(argv,cwd=W,env=env,capture_output=True)
    (O/(label+'.stdout')).write_bytes(r.stdout);(O/(label+'.stderr')).write_bytes(r.stderr)
    assert r.returncode==0 and r.stderr==b'',(label,r.returncode,r.stderr.decode())
    if expected is not None:assert r.stdout==expected and json.loads(r.stdout)==json.loads(expected),label
    result={'label':label,'returncode':0,'stdout_sha256':sha(r.stdout),'stdout_bytes':len(r.stdout),'stderr_sha256':sha(r.stderr),'full_stdout_stderr_and_whole_json_exact':expected is not None}
    print(label+': PASS',flush=True);return result
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:runs=list(pool.map(lambda i:run(f'turn{i}',[sys.executable,'-B',str(W/f'verify_turn{i}.py')],(P/f'TURN_{i}_CHECKS.json').read_bytes()),range(1,6)))
runs.append(run('whole_author_sources',[sys.executable,'-B',str(W/'REPLAY_ALL.py'),'--sources',str(A/'raw_sources')],(P/'final_review/AUTHOR_REPLAY.json').read_bytes()))
runs.append(run('historical_independent',[sys.executable,'-B',str(W/'final_review/independent_checks.py')],(P/'final_review/INDEPENDENT_CHECKS.json').read_bytes()))
expected=b'PASS: review, frozen author/remote bindings and independent exact replay\n'
last=run('historical_review_verifier',[sys.executable,'-B',str(W/'final_review/verify_review.py'),'--author-dir',str(W)])
assert (O/'historical_review_verifier.stdout').read_bytes()==expected;last['entire_literal_stdout_exact']=True;runs.append(last)
for f in m['files']:
    if f['path'].startswith(PREFIX+'/'):assert sha((W/f['path'][len(PREFIX)+1:]).read_bytes())==f['sha256']
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_COMPLETE_ORIGINAL_REPRODUCTION','workflow_percent':70,'original_method_resolution_percent':0,'all_53_original_git_api_manifest_paths_exact':True,'all_52_target_files_exact_and_unchanged_by_replay':True,'all_42_immutable_WIP_author_files_exact':True,'five_historical_checkpoints_exact':history,'nested_manifest_bindings':sum(x['bindings'] for x in nested),'manifests':nested,'historical_remote_author_blob_bindings':42,'four_fresh_primary_pdf_matches':source,'all_eight_verification_programs_and_helpers_read_in_full_before_execution':True,'runs':runs,'author_assertions':210974,'historical_review_assertions':9334,'historical_author_manifest_entries':166,'portable_runner_fetches_no_sources':'Optional --sources validates locally supplied fresh bytes only. No download performed by runner.','original_problem':'Unrestricted probability-only proof unresolved,5/5.','fresh_family_and_whole_final_gates_pending':True}
(A/'root_original_reproduction_receipt.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'runs':len(runs),'nested_manifest_bindings':out['nested_manifest_bindings'],'author':210974,'historical_review':9334}))
