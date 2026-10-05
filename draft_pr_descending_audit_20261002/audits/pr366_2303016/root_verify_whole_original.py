"""Full new whole-review original evidence and independent complete replay."""
from pathlib import Path
from datetime import datetime,timezone
import gzip,hashlib,json,subprocess
A=Path(__file__).resolve().parent;R=A.parents[2];F=A/'clean_final_adversary';S=A/'root_whole_original_streams';S.mkdir(exist_ok=True);V=A/'root_replay_private/whole_math';V.mkdir(parents=True,exist_ok=True);PY=R/'draft_pr_descending_audit_20261002/audits/pr378_30004322/sources_effective_review/private_runtime/bin/python'
sha=lambda b:hashlib.sha256(b).hexdigest();checks=[];captures=[]
def ck(v,n):checks.append({'name':n,'passed':bool(v)});assert v,n
def bound(p,n,d):
 b=p.read_bytes();ck(len(b)==n and sha(b)==d,'every bound byte '+str(p));return b
for sealname in ['INDEPENDENT_BASELINE_SEAL.json','ORIGINAL_ASSESSMENT_SEAL.json']:
 se=json.loads((F/sealname).read_bytes())
 for name,e in se['files'].items():bound(F/name,e.get('bytes',e.get('size')),e['sha256'])
raw=(F/'FROZEN_PACKET_RECEIPT.json').read_bytes();ck(sha(raw)=='92d7fe638d55eda70aa4339acbbd223bedcde8ce250eb41afdf1cae727f84142','literal whole original receipt');o=json.loads(raw);ck(len(o['commands'])==43 and len(o['snapshot_file_bindings'])==22 and len(o['nested_bindings'])==48 and o['author_checkpoint_files']==14,'whole recorded scope')
for e in o['snapshot_file_bindings']:bound(A/'snapshot'/e['path'],e['bytes'],e['sha256'])
D=A/'snapshot/unsolved_math_prioritization/attempts/2303016'
for e in o['nested_bindings']:bound((D/e['manifest']).parent/e['path'],e['bytes'],e['sha256'])
for i,c in enumerate(o['commands']):
 label=c['label'];old=bound(F/'streams'/(label+'.stdout'),c['stdout_bytes'],c['stdout_sha256']);err=bound(F/'streams'/(label+'.stderr'),c['stderr_bytes'],c['stderr_sha256']);ck(c['exit']==0 and not err,'whole old exit '+label)
 z=subprocess.run(c['argv'],cwd=c['cwd'] or R,capture_output=True)
 ck(z.returncode==0 and z.stderr==err and z.stdout==old,'every fresh output byte '+label)
 streams={}
 for stream,b in [('stdout',z.stdout),('stderr',z.stderr)]:
  p=S/(str(i)+'_'+label+'.'+stream+'.gz');p.write_bytes(gzip.compress(b,mtime=0));ck(gzip.decompress(p.read_bytes())==b,'lossless whole stream '+label+'/'+stream);streams[stream]={'path':p.relative_to(A).as_posix(),'bytes':len(b),'sha256':sha(b),'gzip_bytes':p.stat().st_size,'gzip_sha256':sha(p.read_bytes())}
 captures.append({'label':label,'args':c['argv'],'exit':z.returncode,**streams})
for e in json.loads((F/'PRIMARY_SOURCE_RECEIPTS.json').read_bytes())['receipts']:
 bound(Path(e['original_pdf_path']),e['size'],e['sha256']);ck(sha((F/'private_sources'/(e['name']+'.txt')).read_bytes())==e['extracted_text_sha256'],'whole independent source extraction '+e['name'])
program=(F/'adversarial_controls.py').read_bytes();copy=V/'adversarial_controls.py';copy.write_bytes(program);ck(copy.read_bytes()==program,'private copy exact original executed source')
started=datetime.now(timezone.utc);z=subprocess.run([str(PY),str(copy)],cwd=V,capture_output=True);ended=datetime.now(timezone.utc)
ck(z.returncode==0 and not z.stderr,'new2590 controls fresh complete exit');fresh=json.loads(z.stdout);old=json.loads((F/'ADVERSARIAL_CONTROLS.json').read_bytes());ck(started<=datetime.fromisoformat(fresh['utc'])<=ended,'only fresh output timestamp validated');old['utc']=fresh['utc'];expected=(json.dumps(old,indent=2)+'\n').encode();ck(z.stdout==expected and fresh['assertions']==2590,'all2590 full output bytes except exactly regenerated UTC metadata');ck((copy.parent/'ADVERSARIAL_CONTROLS.json').read_bytes()==z.stdout,'entire fresh written control receipt')
for stream,b in [('stdout',z.stdout),('stderr',z.stderr)]:(S/('adversarial_controls.'+stream)).write_bytes(b)
out={'utc':datetime.now(timezone.utc).isoformat(),'status':'PASS_ENTIRE_NEW_WHOLE_ORIGINAL_EVIDENCE','check_count':len(checks),'checks':checks,'captures':captures,'readonly_original_commands_reexecuted':43,'new_adversarial_controls':2590,'fresh_control_stdout_sha256':sha(z.stdout),'only_control_output_normalization':'One exact utc field replaced with validated fresh execution timestamp; all other output bytes exact','program_sha256':sha(Path(__file__).read_bytes())}
(A/'root_whole_original_receipt.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:out[k] for k in ['status','check_count','readonly_original_commands_reexecuted','new_adversarial_controls']},indent=2))
