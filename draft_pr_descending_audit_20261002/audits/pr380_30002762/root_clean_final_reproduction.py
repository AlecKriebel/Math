"""Reproduce the fresh review's full streams and direct object bindings."""
import datetime,hashlib,json,shutil,subprocess,sys
from pathlib import Path
A=Path(__file__).resolve().parent
F=A/'clean_final_adversary'
m=json.loads((A/'repaired_snapshot_manifest.json').read_text())
D=A/'repaired_snapshot/problems/30002762_conjugation_norms'
prefix='problems/30002762_conjugation_norms/'
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*args):return subprocess.check_output(['git',*args])
for e in m['files']:
 b=git('show',f"{m['head']}:{e['path']}")
 assert b==(A/'repaired_snapshot'/e['path']).read_bytes()
 assert len(b)==e['bytes'] and sha(b)==e['sha256']
 blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
 assert git('rev-parse',f"{m['head']}:{e['path']}").decode().strip()==blob
 if e['path'].startswith(prefix):assert b==git('show',f"9946a67cf8a1f7e3130d2a12de902db05875283a:{e['path']}")
G=json.loads((F/'git_provenance.json').read_text())
assert G['head']==m['head'] and G['base']==m['base']
assert set(git('diff','--name-only',m['base'],m['head']).decode().splitlines())=={e['path'] for e in m['files']}
q='unsolved_math_prioritization/QUEUE.md'
x=git('show',f"{m['base']}:{q}").splitlines(keepends=True)
y=git('show',f"{m['head']}:{q}").splitlines(keepends=True)
assert len(x)==len(y)
diff=[i for i,(a,b) in enumerate(zip(x,y)) if a!=b];assert diff==[416]
a=x[416].split(b'|');b=y[416].split(b'|')
assert [j for j,(u,v) in enumerate(zip(a,b)) if u!=v]==[8,9]
assert b[2].strip().startswith(b'30002762 / ') and b[8].strip()==b'unsolved' and b[9].strip()==b'5/5'
N=json.loads((F/'nested_manifest_receipts.json').read_text())
for e in N['nested_files']:
 j=json.loads((D/e['manifest']).read_text());files=j['files']
 if isinstance(files,dict):files=[dict(v,path=k) for k,v in files.items()]
 match=[v for v in files if v['path']==e['path']];assert len(match)==1
 z=(D/e['manifest']).parent.joinpath(e['path']).read_bytes();assert sha(z)==e['sha256']==match[0]['sha256']
 if 'bytes' in match[0]:assert len(z)==match[0]['bytes']
for e in N['previous_links']:
 t=int(e['manifest'].split('_')[1]);h=sha((D/f'TURN_{t-1}_MANIFEST.json').read_bytes())
 assert h==e['previous_hash_verified']==json.loads((D/e['manifest']).read_text())['previous_manifest_sha256']
for e in N['historical_remote_receipts']:
 z=git('show',f"{e['head']}:{e['path']}")
 assert git('rev-parse',f"{e['head']}:{e['path']}").decode().strip()==e['expected_blob']
 assert z==git('show',f"{m['head']}:{e['path']}")
 r=json.loads((D/e['receipt']).read_text());p=e['path'].removeprefix(prefix)
 match=[v for v in r['files'] if v['path']==p];assert len(match)==1
 assert r['head']==e['head'] and match[0]['sha']==e['expected_blob'] and len(z)==match[0]['size']
S=json.loads((F/'independent_seal.json').read_text())
for p,h in S['files'].items():assert sha((F/p).read_bytes())==h
anc=json.loads((F/'ancestry_receipts.json').read_text())
for h in anc['ancestry']:assert subprocess.run(['git','merge-base','--is-ancestor',h,m['head']]).returncode==0
for p in anc['author_wip_file_matches']:assert git('show',f"{anc['author_wip']}:{prefix}{p}")==(D/p).read_bytes()
private=A/'tmp/root_clean_final_replay'
assert not private.exists()
shutil.copytree(D,private)
runs=[]
def run(p,cwd,expected,tag):
 r=subprocess.run([sys.executable,'-B',str(p)],cwd=cwd,capture_output=True)
 (A/(tag+'.stdout')).write_bytes(r.stdout);(A/(tag+'.stderr')).write_bytes(r.stderr)
 assert r.returncode==0 and not r.stderr,(p,r.returncode,r.stderr.decode())
 assert r.stdout==expected,(p,'full-stream mismatch')
 runs.append({'program':str(p),'exit_code':r.returncode,'stdout_bytes':len(r.stdout),'stdout_sha256':sha(r.stdout),'stderr_empty':True,'full_stream_byte_exact':True})
for e in json.loads((F/'complete_replay_outputs.json').read_text()):
 assert e['exit_code']==0 and e['stderr']==''
 run(private/e['program'],private,e['stdout'].encode(),'root_clean_'+e['program'].replace('/','_').removesuffix('.py'))
for p,o in [('independent_controls.py','independent_controls_output.json'),('postseal_adversarial_controls.py','postseal_adversarial_controls_output.json')]:
 run(F/p,private,(F/o).read_bytes(),'root_clean_'+p.removesuffix('.py'))
receipt={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reviewed_head':m['head'],'actual_base':m['base'],'direct_Git_files':len(m['files']),'unchanged_math_files':43,'only_queue_line':417,'only_queue_cells':[8,9],'every_other_queue_byte_preserved':True,'nested_file_bindings':len(N['nested_files']),'previous_links':len(N['previous_links']),'historical_remote_blob_bindings':len(N['historical_remote_receipts']),'source_first_seal_bindings':len(S['files']),'ancestry_bindings':len(anc['ancestry']),'runs':runs,'optional_public_source_bindings':0,'fresh_PDF_bindings_recorded_separately':6,'unreproduced_legacy_PNGs':2,'workflow_percent':95,'original_problem_resolution_percent':0,'scope':'Full-stream/object reproduction; universal mathematical proofs and source passages read separately.'}
(A/'root_clean_final_reproduction_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
