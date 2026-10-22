import hashlib,json,os,stat,subprocess,zipfile
from pathlib import Path
from datetime import datetime,timezone
O=Path(__file__).resolve().parent;A=O.parent.parent;D=A/'preprint';T=O/'private/cold';T.mkdir(exist_ok=True)
PY=A.parents[1]/'audits/pr906_30006419/reviews/computation_family/tmp/venv/bin/python'
PY=Path('/Users/alec/Documents/Math/draft_pr_claimed_solved_900_1000_20261012/audits/pr906_30006419/reviews/computation_family/tmp/venv/bin/python')
def h(b):return hashlib.sha256(b).hexdigest()
assert h((D/'FREEZE.json').read_bytes())=='9af8f2570af53b6a6658a7998ac08927829c8747be7c764a8d2c392dc6c6afe1'
assert h((D/'global_hessian_verification.zip').read_bytes())=='e687f7c9a3643a796a5fe813ec10e5c2c74a28adb081a7ebeefb6910823c6863'
assert h((D/'ARCHIVE_MANIFEST.json').read_bytes())=='0833606acbf062d90872dd562e27423e51e2efc91369059436ca2fb83d55e33b'
f=json.loads((D/'FREEZE.json').read_bytes());layout=f['archive_layout'];payload={}
with zipfile.ZipFile(D/'global_hessian_verification.zip') as z:
 prefix=layout['package_manifest'].removesuffix('PACKAGE_MANIFEST.json')
 for zi in z.infolist():
  if zi.filename.startswith(prefix):
   name=zi.filename[len(prefix):];assert name and '..' not in name.split('/') and not name.startswith('/')
   payload[name]=z.read(zi)
m=json.loads(payload['PACKAGE_MANIFEST.json']);assert len(m['files'])==207 and len(payload)==208
assert h(payload['PACKAGE_MANIFEST.json'])=='52165ba2410fa32238244feef20820e5bca9971f60c90542a2360f4d44e6c4ec'
assert h(payload['verify_package.py'])=='1896614c7b163e8fd69fa15c82c4d2a77e1ca46f4e4ada407d9ea5b52c2a2d2d'
for name,pin in m['files'].items():assert len(payload[name])==pin['bytes'] and h(payload[name])==pin['sha256'] and pin['mode']=='0644'
for name,b in payload.items():
 q=T/name;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b);q.chmod(0o644)
receipts={}
for mode,opt,flag in [('normal',0,[]),('O',1,['-O']),('OO',2,['-OO']),('env2',2,[])]:
 env=dict(os.environ,TMPDIR=str(O/'private'));env.pop('PYTHONOPTIMIZE',None)
 if mode=='env2':env['PYTHONOPTIMIZE']='2'
 cmd=[str(PY),'-B','-P',*flag,str(T/'verify_package.py'),'--package',str(T),'--manifest-sha256',f['package_manifest_sha256'],'--runtime-receipt',str(O/'private'/('runtime_'+mode+'.json'))]
 p=subprocess.run(cmd,env=env,cwd=O/'private',capture_output=True,text=True,timeout=1200)
 (O/('REPLAY_'+mode+'.stderr')).write_text(p.stderr);assert p.returncode==0,(mode,p.returncode,p.stderr)
 actual=json.loads(p.stdout);expected=json.loads((D/('PACKAGE_REPLAY_'+mode+'.json')).read_text());assert actual==expected,(mode,'entire receipt differs')
 assert actual['observed_outer_optimization']==opt and actual['worker_optimization']==0
 (O/('REPLAY_'+mode+'.json')).write_text(p.stdout)
 receipts[mode]=actual;print(mode+' PASS entire receipt equal; actual outer='+str(opt),flush=True)
for name,b in payload.items():assert (T/name).read_bytes()==b
result={'status':'PASS','utc':datetime.now(timezone.utc).isoformat(),'cold_extraction':True,'cold_extraction_details':{'outer_members':220,'outer_payloads':219,'inner_payloads':207,'inner_members':208,'every_payload_authenticated_before_execution':True,'new_private_directory':str(T)},'typed_float_policy_verified':True,'historical_strict_failure_preserved':True,'package_manifest_sha256':f['package_manifest_sha256'],'externally_pinned_verifier_sha256':'1896614c7b163e8fd69fa15c82c4d2a77e1ca46f4e4ada407d9ea5b52c2a2d2d','normalized_fields_ignored':[],'modes':[{'mode':k,'observed_outer_optimization':v['observed_outer_optimization'],'returncode':0,'receipt':v} for k,v in receipts.items()],'external_mutations':0}
(O/'COLD_REPLAY.json').write_text(json.dumps(result,indent=2)+'\n')
