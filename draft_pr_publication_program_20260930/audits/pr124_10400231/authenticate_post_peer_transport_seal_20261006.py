"""Authenticate the narrow additive review; grant and actual execution remain separate."""
from pathlib import Path
import datetime,hashlib,json,os,subprocess
A=Path(__file__).resolve().parent;C=A.parents[2];F=A/'native_published_obstruction_protocol_adversary_20261006/post_peer_transport_addendum_20261006'
GIT='/opt/homebrew/Cellar/git/2.38.2/bin/git'
def req(v,s):
 if not v:raise RuntimeError(s)
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_text())
def dump(p,x):p.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
pins={'REPORT.md':'9f56c6e562d69c0a9049b51a73daf0c899a999464bdbe1d654fde21e43fd2753','RESULT.json':'71b562a78db1cea468af7c653c5a2977f828933a5e851b99c8462114cc39700a','ACTUAL_INPUT_HASHES.json':'5674b6b305a3da974ed0428db483df04e3c430ee95a5590c4030921a3dfbb800','PUBLIC_MANIFEST.json':'dbe4b0baaf38fa76691cc28156a54637584975360d56029cb9602eaffbde285b','SEAL.json':'e365b8f52cb73110d54e2ba8600a745e653b9cf014d3f68a9f321e535e045697'}
for n,h in pins.items():req(sha((F/n).read_bytes())==h,'Exact fresh additive seal '+n)
result=load(F/'RESULT.json');req(result['verdict']=='PASS' and not result['global_corrections_required'] and not result['operational_authorization'],'Validation only clean pass')
members=[]
for item in load(F/'PUBLIC_MANIFEST.json')['members']:
 p=F/item['path'];b=p.read_bytes();req(len(b)==item['bytes'] and sha(b)==item['sha256'],'Full sealed addendum body');members.append({'path':str(p.relative_to(A)),'bytes':len(b),'sha256':sha(b)})
for n in ['PUBLIC_MANIFEST.json','SEAL.json']:
 p=F/n;b=p.read_bytes();members.append({'path':str(p.relative_to(A)),'bytes':len(b),'sha256':sha(b)})
inputs=load(F/'ACTUAL_INPUT_HASHES.json');events=[]
for item in inputs['filesystem_inputs']:
 b=Path(item['path']).read_bytes();req(len(b)==item['bytes'] and sha(b)==item['sha256'],'Addendum filesystem input')
for item in inputs['full_Git_body_inputs']:
 ch=subprocess.Popen([GIT,'show',item['commit']+':'+item['path']],cwd=C,stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=ch.communicate();req(ch.returncode==0 and len(out)==item['bytes'] and sha(out)==item['sha256'],'Actual full immutable Git input');events.append({'PID':ch.pid,'commit':item['commit'],'path':item['path'],'bytes':len(out),'sha256':sha(out),'exit_code':ch.returncode})
req(len(members)==21 and len(inputs['filesystem_inputs'])==64 and len(events)==72,'Addendum cardinality')
record={'schema':'pr124-root-post-peer-addendum-full-body-authentication/v1','UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_operator_PID':os.getpid(),'sealed_members':members,'filesystem_full_inputs_verified':64,'immutable_Git_full_inputs_verified':events,'current_actor_sources_unchanged':True,'prior24_seal_preserved':True,'new_central_proof_search_turns':0,'main_index_worktree_service_mutations':False,'future_peer_release_and_concrete_grant_required':True}
out=A/'ROOT_POST_PEER_TRANSPORT_AUTHENTICATION_20261006.json';req(not out.exists(),'Authenticate once');dump(out,record)
ready={'schema':'pr124-root-post-peer-unchanged-transport-ready/v1','UTC':record['UTC'],'actual_operator_PID':os.getpid(),'PASS':True,'actual_peer_main':result['actual_peer_main'],'transport_authentication_sha256':result['transport_authentication_sha256'],'sealed_members':members,'report':str((F/'REPORT.md').relative_to(A)),'report_sha256':pins['REPORT.md'],'root_authentication_sha256':sha(out.read_bytes()),'operational_authorization':False,'actual_peer_release_and_fresh_specific_grant_still_required':True,'native_export_performed':False,'new_central_proof_search_turns':0}
dump(A/'ROOT_POST_PEER_TRANSPORT_PROTOCOL_READY_20261006.json',ready)
print(json.dumps({'UTC':record['UTC'],'actual_operator_PID':os.getpid(),'public_members':len(members),'filesystem_inputs':64,'Git_bodies':len(events),'PASS':True,'operational_authorization':False},sort_keys=True))
