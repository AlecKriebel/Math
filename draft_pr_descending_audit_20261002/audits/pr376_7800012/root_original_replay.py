"""Direct-object and complete mathematical replay of the frozen original packet."""
import datetime,hashlib,json,shutil,subprocess
from pathlib import Path
A=Path(__file__).resolve().parent;D=A/'snapshot/unsolved_math_prioritization/attempts/7800012'
M=json.loads((A/'snapshot_manifest.json').read_text());head=M['head']
prefix='unsolved_math_prioritization/attempts/7800012/'
py='/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr378_30004322/sources_effective_review/private_runtime/bin/python'
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*args):return subprocess.check_output(['git',*args])
assert set(git('diff','--name-only',M['base'],head).decode().splitlines())=={e['path'] for e in M['files']}
for e in M['files']:
 z=git('show',head+':'+e['path']);assert z==(A/'snapshot'/e['path']).read_bytes()
 assert len(z)==e['bytes'] and sha(z)==e['sha256'] and git('rev-parse',head+':'+e['path']).decode().strip()==e['git_blob_sha']
nested=0
for f in sorted(D.rglob('*MANIFEST.json')):
 j=json.loads(f.read_text())
 for e in j.get('files',[]):
  z=(f.parent/e['path']).read_bytes();assert len(z)==e['bytes'] and sha(z)==e['sha256'];nested+=1
 for key,name in [('author_manifest_sha256','FINAL_FROZEN_MANIFEST.json'),('review_manifest_sha256','final_review/REVIEW_MANIFEST.json')]:
  if key in j:assert j[key]==sha((D/name).read_bytes())
assert nested==210
author=json.loads((D/'FINAL_FROZEN_MANIFEST.json').read_text());review=json.loads((D/'final_review/REVIEW_MANIFEST.json').read_text());wip=review['author_wip']
assert subprocess.run(['git','merge-base','--is-ancestor',wip,head]).returncode==0
for p in [e['path'] for e in author['files']]+['FINAL_FROZEN_MANIFEST.json']:assert git('show',wip+':'+prefix+p)==(D/p).read_bytes()
ready=json.loads((D/'READINESS.json').read_text());ledger=[json.loads(l) for l in (D/'TURN_5_LEDGER.jsonl').read_text().splitlines()]
assert len(ledger)==6 and [e['turns_used'] for e in ledger]==list(range(6))
for t in range(1,6):
 state=json.loads((D/f'TURN_{t}_STATE.json').read_text());assert state['evidence']==ready and state==ledger[t]
 assert [json.loads(l) for l in (D/f'TURN_{t}_LEDGER.jsonl').read_text().splitlines()]==ledger[:t+1]
for e in ledger:assert e['evidence']==ready
private=A/'tmp/root_original_packet';assert not private.exists();shutil.copytree(D,private)
runs=[]
def run(name,args,expected,tag):
 r=subprocess.run([py,'-B',str(private/name),*args],cwd=private,capture_output=True)
 (A/(tag+'.stdout')).write_bytes(r.stdout);(A/(tag+'.stderr')).write_bytes(r.stderr)
 assert r.returncode==0 and not r.stderr,(tag,r.returncode,r.stderr.decode())
 assert r.stdout==expected,(tag,'full stream mismatch')
 runs.append({'program':name,'args':args,'exit_code':0,'stderr_empty':True,'stdout_bytes':len(r.stdout),'stdout_sha256':sha(r.stdout),'full_stream_byte_exact':True})
for t in range(1,6):run(f'verify_turn{t}.py',[],(D/f'TURN_{t}_CHECKS.json').read_bytes(),f'root_turn{t}')
run('hessian_certificate.py',[],(D/'TURN_4_CERTIFICATE.json').read_bytes(),'root_hessian_certificate')
j=json.loads((D/'final_review/AUTHOR_REPLAY.json').read_text());j['primary_source_files_verified']=0
run('REPLAY_ALL.py',[],(json.dumps(j,indent=2,sort_keys=True)+'\n').encode(),'root_public_author_replay')
run('REPLAY_ALL.py',['--sources',str(A/'raw_sources')],(D/'final_review/AUTHOR_REPLAY.json').read_bytes(),'root_source_bound_author_replay')
run('final_review/independent_check.py',[],(D/'final_review/INDEPENDENT_CHECKS.json').read_bytes(),'root_historical_independent')
run('verify_review.py',[],b'PASS: frozen author/review hashes and 984 independent SymPy controls\n','root_public_review_wrapper')
r={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'frozen_head':head,'direct_Git_bindings':len(M['files']),'all_target_files':len(M['files'])-1,'nested_file_binding_occurrences':nested,'author_WIP':wip,'unchanged_frozen_author_files':41,'all_five_ledgers_exact_prefixes_and_states_exact':True,'runs':runs,'author_assertions':102005,'historical_independent_assertions':984,'public_replay_source_bindings':0,'separate_fresh_source_bound_replay_bindings':3,'full64_exact_Hessian_certificate_regenerated_byte_exact':True,'workflow_percent':60,'original_problem_resolution_percent':0,'scope':'Original-head reproduction only; independent families and new final exact corrected-head adversary still required.'}
(A/'root_original_replay_receipt.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
