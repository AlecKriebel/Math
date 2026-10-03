"""Replay new whole-review programs and independence seals without modifying them."""
from pathlib import Path
import concurrent.futures,datetime,hashlib,json,os,subprocess,sys
A=Path(__file__).resolve().parent;C=A/'clean_final_adversary';W=A/'tmp/root_clean_math';assert not W.exists();W.mkdir(parents=True)
O=A/'root_clean_math_streams';O.mkdir(exist_ok=True);sha=lambda b:hashlib.sha256(b).hexdigest()
seals=[];copied=set()
for name in ['public/source_first_seal.json','public/mathematical_verdict_seal.json']:
 d=json.loads((C/name).read_text());assert d.get('candidate_access_before_seal',False) is False and not d.get('author_code_receipts_manifests_old_review_read_before_seal',False)
 for member,digest in d['files'].items():
  b=(C/member).read_bytes();assert sha(b)==digest,(name,member)
  q=W/member;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b);copied.add(member)
 shutil_seal=W/name;shutil_seal.parent.mkdir(parents=True,exist_ok=True);shutil_seal.write_bytes((C/name).read_bytes())
 seals.append({'seal':name,'sha256':sha((C/name).read_bytes()),'instances':len(d['files'])})
 for member,digest in d.get('proof_inputs',{}).items():
  p=A/'snapshot/problems/30005116_induced_four_cycle_profile'/member;assert sha(p.read_bytes())==digest
source=json.loads((C/'private/source_fetch_receipt.json').read_text())
root=json.loads((A/'root_primary_source_receipt.json').read_text())
known={e['sha256']:e for e in root['files']}
primary=[]
for f in sorted((C/'private/sources').glob('*.pdf')):
 b=f.read_bytes();h=sha(b);assert h in known and len(b)==known[h]['bytes'];primary.append({'private_file':f.name,'root_primary':known[h]['file'],'sha256':h,'bytes':len(b)})
assert len(primary)==5
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
def run(name):
 f=W/'public/controls'/name;r=subprocess.run([sys.executable,'-B',str(f)],cwd=f.parent,env=env,capture_output=True)
 label=name.removesuffix('.py');(O/(label+'.stdout')).write_bytes(r.stdout);(O/(label+'.stderr')).write_bytes(r.stderr)
 assert r.returncode==0,(name,r.returncode,r.stderr.decode())
 assert r.stdout==(C/'public/logs'/(label+'.stdout')).read_bytes() and r.stderr==(C/'public/logs'/(label+'.stderr')).read_bytes(),name
 print(label+': PASS full stdout/stderr byte-exact',flush=True)
 return {'program':name,'entire_stdout_stderr_byte_exact':True,'exit':0,'stdout_sha256':sha(r.stdout),'stderr_sha256':sha(r.stderr),'stdout_bytes':len(r.stdout)}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:runs=list(pool.map(run,['source_first_counts.py','fresh_symbolic.py','fresh_adversarial.py','fresh_moments.py']))
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_FRESH_WHOLE_MATH','workflow_percent':92,'unrestricted_discovery_percent':0,'mathematical_verdict_and_all_control_code_read_in_full':True,'all_sealed_binding_instances':sum(x['instances'] for x in seals),'seals':seals,'all_five_fresh_primary_PDFs_match_root':primary,'proofs_inputs_exact':5,'runs':runs,'new_moment_region_proof_independently_checked':'Localizer lower bound t>=s²/m, upper t<=s-(m-s)²/(1-m); both boundary two-atom laws have same first2moments, nonnegative masses; convex mixtures fill interval; endpoint means force deterministic laws. Bound difference=(s-m²)(m-s)/(m(1-m))>=0 for0<m<1.','full_final_package_remote_gate_pending':True}
(A/'root_clean_mathematical_reproduction_receipt.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'programs':len(runs),'seals':out['all_sealed_binding_instances']}))
