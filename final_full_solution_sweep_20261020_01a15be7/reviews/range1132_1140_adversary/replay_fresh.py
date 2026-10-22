#!/usr/bin/env python3
"""Seal authored review and run new copies with adverse custody controls."""
from pathlib import Path
import hashlib,json,datetime as dt,shutil,subprocess,sys,tempfile
H=Path(__file__).resolve().parent;EX={'MANIFEST.json','MANIFEST.sha256','REPLAY_RESULTS.json','FINAL_SEAL.json'}
def sha(b):return hashlib.sha256(b).hexdigest()
def need(v,m):
 if not v:raise RuntimeError(m)
def write(p,v):p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
files={str(p.relative_to(H)):{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in H.rglob('*') if p.is_file() and not p.is_relative_to(H/'runtime') and str(p.relative_to(H)) not in EX}
write(H/'MANIFEST.json',{'schema':'bounded-adversarial-closed-payload-v1','checkpoint':'39e8a7e1f675baa98d4907e7831edcbf2bf53767','created_at':dt.datetime.now(dt.timezone.utc).isoformat(),'payloads':dict(sorted(files.items())),'excluded_control_files':sorted(EX),'excluded_disposable_runtime':'runtime/','privacy':'Raw captures and third-party payloads are private; public manifest publishes hashes only.'})
mb=(H/'MANIFEST.json').read_bytes();mh=sha(mb);(H/'MANIFEST.sha256').write_text(mh+'  MANIFEST.json\n');verifier=sha((H/'verify_artifact.py').read_bytes());results=[];(H/'runtime').mkdir(exist_ok=True)
for flags in [[],['-O'],['-OO']]:
 with tempfile.TemporaryDirectory(prefix='fresh_',dir=H/'runtime') as tmp:
  c=Path(tmp)/'review';shutil.copytree(H,c,ignore=lambda path,names:['runtime'] if Path(path)==H else [])
  need(sha((c/'verify_artifact.py').read_bytes())==verifier,'copied verifier external seal')
  def run(expected):
   r=subprocess.run([sys.executable,*flags,str(c/'verify_artifact.py'),mh],cwd=c,capture_output=True,text=True)
   need((r.returncode==0)==expected,'unexpected copied verification result:'+r.stderr[-500:]);return r
  good=run(True);pin=json.loads(good.stdout);adverse=[]
  target=c/'private/pr1139/CAPTURE.json';orig=target.read_bytes();target.write_bytes(orig+b' ');bad=run(False);need('payload:' in bad.stderr,'corruption rejection reason');adverse.append('changed captured payload rejected');target.write_bytes(orig)
  alien=c/'UNDECLARED.txt';alien.write_text('adverse own-copy custody control');bad=run(False);need('closed payload membership' in bad.stderr,'extra file reason');adverse.append('undeclared payload rejected');alien.unlink()
  mp=c/'MANIFEST.json';orig=mp.read_bytes();mp.write_bytes(orig+b' ');bad=run(False);need('external manifest seal' in bad.stderr,'manifest rejection reason');adverse.append('altered manifest rejected');mp.write_bytes(orig)
  again=run(True);need(again.stdout==good.stdout,'restored-copy deterministic result')
  results.append({'flags':flags,'fresh_copy':True,'copied_verifier_sha256':verifier,'normal_exit':good.returncode,'stdout_sha256':sha(good.stdout.encode()),'result':pin,'negative_controls':adverse,'restored_recheck':True})
need(len({x['stdout_sha256'] for x in results})==1,'optimization modes disagree')
write(H/'REPLAY_RESULTS.json',{'at':dt.datetime.now(dt.timezone.utc).isoformat(),'status':'PASS','manifest_sha256':mh,'modes':results,'all_three_fresh_copies_and_nine_negative_controls_pass':True})
write(H/'FINAL_SEAL.json',{'at':dt.datetime.now(dt.timezone.utc).isoformat(),'status':'PASS_SCOPED_REVIEW','checkpoint':'39e8a7e1f675baa98d4907e7831edcbf2bf53767','files':{name:{'bytes':(H/name).stat().st_size,'sha256':sha((H/name).read_bytes())} for name in ['MANIFEST.json','MANIFEST.sha256','REPLAY_RESULTS.json','REPORT.md','CHECKS.json','FINAL_RECHECK.json','verify_artifact.py']},'self_hash_policy':'FINAL_SEAL excludes itself; parent receives its SHA256 independently.','scope':'PR1132–1140 only; no whole-sweep, global priority or human certification.'})
print(json.dumps({'status':'PASS','payloads':len(files),'payload_bytes':sum(x['bytes'] for x in files.values()),'manifest_sha256':mh,'final_seal_sha256':sha((H/'FINAL_SEAL.json').read_bytes()),'three_fresh_modes':True,'negative_controls':9}))
