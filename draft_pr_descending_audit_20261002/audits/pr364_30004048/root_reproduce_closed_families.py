"""Fresh ROOT literal Git and whole closed family reproduction, outside closures."""
from pathlib import Path
import datetime,gzip,hashlib,json,os,subprocess
A=Path(__file__).resolve().parent;R=A.parents[2];G=A/'graph_boundary_review/public';L=A/'polytope_duality_review'
D=A/'root_replay_private/closed_families_001';D.mkdir(exist_ok=False)
PY=R/'draft_pr_descending_audit_20261002/audits/pr378_30004322/sources_effective_review/private_runtime/bin/python'
env={'PYTHONDONTWRITEBYTECODE':'1','GIT_OPTIONAL_LOCKS':'0','GIT_NO_LAZY_FETCH':'1'}
sha=lambda b:hashlib.sha256(b).hexdigest();utc=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat();captures=[]
def run(name,argv,cwd=R):
 start=utc();p=subprocess.run([str(x) for x in argv],cwd=cwd,env=dict(os.environ,**env),capture_output=True);end=utc();c={'name':name,'argv':[str(x) for x in argv],'cwd':str(cwd),'environment_changes':env,'started_utc':start,'finished_utc':end,'exit_code':p.returncode,'streams':{}}
 for st,b in [('stdout',p.stdout),('stderr',p.stderr)]:
  q=D/(name+'.'+st+'.gz');z=gzip.compress(b,mtime=0);q.write_bytes(z);c['streams'][st]={'path':str(q.relative_to(A)),'stored_bytes':len(z),'stored_sha256':sha(z),'logical_bytes':len(b),'logical_sha256':sha(b)}
 captures.append(c);(D/(name+'.json')).write_text(json.dumps(c,indent=2)+'\n');assert p.returncode==0 and not p.stderr,c;return p.stdout
gp='f7f87c47b7604cfabc10110af936d29ccd41b6afe755bfd8a6502828d3889052';lp='5c0032d82c71a8632668ad6ce56ce0414a2aa16f777421f038265e768a24c6e8'
assert sha((G/'PUBLIC_MANIFEST.json').read_bytes())==gp and sha((L/'PUBLIC_MANIFEST.json').read_bytes())==lp
before={str(p):sha(p.read_bytes()) for d in [G,L] for p in d.rglob('*') if p.is_file()}
main=run('begin_main',['git','rev-parse','HEAD']);ix=Path(run('index_path',['git','rev-parse','--git-path','index']).decode().strip());ix=ix if ix.is_absolute() else R/ix;index=ix.read_bytes()
cs=json.loads((G/'COMMAND_RECEIPTS.json').read_bytes())['git'];assert len(cs)==136
for i,c in enumerate(cs):
 assert c['argv'][0]=='git';b=run('graph_literal_git_'+str(i),c['argv'],Path(c['cwd']));e=captures[-1]['streams'];assert len(b)==c['stdout_bytes'] and sha(b)==c['stdout_sha256'];assert e['stderr']['logical_bytes']==c['stderr_bytes']==0 and e['stderr']['logical_sha256']==c['stderr_sha256'];assert sha(b'STDOUT\0'+b+b'STDERR\0')==c['logical_stream_sha256']
graph=json.loads(run('graph_closed',[PY,'-B',G/'check_public_namespace.py','--require-private'],A));assert graph['status']=='PASS_CLOSED_PUBLIC_NAMESPACE' and graph['public_files']==15 and graph['private_components']==202 and graph['snapshot_status']=='ALL42_FROZEN_BYTES_MATCH' and graph['collective_private_captures']=='ALL_LISTED_HASHES_MATCH'
b=run('graph_controls',[PY,'-B',G/'check_graph_boundaries.py'],G);assert b==(G/'GRAPH_CONTROLS.json').read_bytes()
b=run('polytope_closed',[PY,'-B',L/'verify_review.py','--snapshot',A/'snapshot','--repo',R,'--fresh-api'],L);poly=json.loads(b);assert poly['status']=='PASS' and poly['complete_program_replays']==4 and poly['independent_controls']==357 and poly['fresh_api_checked'] and poly['captured_api_checked'] and poly['source_PDFs_checked']==3 and poly['nested_entries']==135
assert run('end_main',['git','rev-parse','HEAD'])==main and ix.read_bytes()==index
assert {str(p):sha(p.read_bytes()) for d in [G,L] for p in d.rglob('*') if p.is_file()}==before
out={'utc':utc(),'status':'PASS_ROOT_FULL_CLOSED_FAMILY_REPRODUCTION','graph_public_manifest_sha256':gp,'polytope_public_manifest_sha256':lp,'graph_readonly_literal_git_reexecutions':136,'graph_exact_controls':122568,'polytope_exact_controls':357,'graph_closed_verifier':graph,'polytope_closed_verifier':poly,'complete_namespace_and_index_unchanged':True,'current_main':main.decode().strip(),'captures':captures,'mathematical_verified_percent':100,'workflow_percent':60,'priority_and_preprint_pending':True,'scope':'Proof independently read and sealed earlier; literal Git/full streams/source identities/finite controls freshly reproduced. Counts do not replace universal proof or certify priority.','program_sha256':sha(Path(__file__).read_bytes())}
(A/'root_closed_families_receipt.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='captures'},indent=2))
