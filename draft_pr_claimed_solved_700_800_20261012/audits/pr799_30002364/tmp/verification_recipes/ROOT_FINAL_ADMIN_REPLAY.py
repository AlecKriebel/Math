from pathlib import Path
import datetime,hashlib,json,shutil,subprocess,sys,tempfile
T=Path('/Users/alec/Documents/Math/draft_pr_claimed_solved_700_800_20261012/audits/pr799_30002364/tmp');M=T/'root-receipts';P=T/'disposition_scope'
MP='7f72f2f949a592f9bfee02caceb4f6fc7095bf21e4617f035818be7ad3f5dab9';CP='ba4d78d7c9316260fae8e1671f46594f4f207859159b9f410e95cb5b7ac19b1b'
def need(ok,msg):
 if not ok:raise RuntimeError(msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
need(sha(P/'MANIFEST.json')==MP and sha(P/'verify_packet.py')==CP,'external pre-execution pins')
rows=json.loads((P/'MANIFEST.json').read_text())['files'];need(set(p.name for p in P.iterdir())==set(rows)|{'MANIFEST.json','verify_packet.py'},'closed20file inventory')
for n,v in rows.items():need(sha(P/n)==v,'pre-execution member digest')
runs=[];controls=[]
def run(packet,mp=MP,cp=CP,py=sys.executable,opt=False,ok=True):
 need(sha(packet/'verify_packet.py')==CP,'unchanged checker before child execution')
 r=subprocess.run([py,'-I','-S','-B']+(['-O'] if opt else [])+[str(packet/'verify_packet.py'),str(packet),mp,cp],cwd='/',capture_output=True,text=True,timeout=30)
 need((r.returncode==0)==ok,'control unexpected acceptance: '+r.stdout+r.stderr)
 if ok:need(json.loads(r.stdout)['result']=='PASS','PASS payload')
 return {'optimized':opt,'python':py,'expected_acceptance':ok,'returncode':r.returncode,'stdout_sha256':hashlib.sha256(r.stdout.encode()).hexdigest()}
for py in [sys.executable,'/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3']:
 for opt in [False,True]:runs.append(run(P,py=py,opt=opt))
for label in ['wrong_manifest_pin','wrong_checker_pin','report_tamper','extra_member','member_symlink','missing_member','semantic_native_DOI_after_fixture_repin']:
 with tempfile.TemporaryDirectory(prefix='root admin fixture ',dir=T/'owned-runtime-tmp') as td:
  q=Path(td)/'packet with spaces';shutil.copytree(P,q);mp=MP;cp=CP
  if label=='wrong_manifest_pin':mp='0'*64
  elif label=='wrong_checker_pin':cp='0'*64
  elif label=='report_tamper':(q/'REPORT_FINAL.md').write_text('changed')
  elif label=='extra_member':(q/'unexpected').write_text('x')
  elif label=='member_symlink':(q/'REPORT_FINAL.md').unlink();(q/'REPORT_FINAL.md').symlink_to(P/'REPORT_FINAL.md')
  elif label=='missing_member':(q/'REPORT_FINAL.md').unlink()
  else:
   p=q/'NATIVE_SCOPE_READBACK.json';d=json.loads(p.read_text());d['own_DOI_blank']=False;p.write_text(json.dumps(d)+'\n')
   p=q/'MANIFEST.json';d=json.loads(p.read_text());d['files']['NATIVE_SCOPE_READBACK.json']=sha(q/'NATIVE_SCOPE_READBACK.json');p.write_text(json.dumps(d)+'\n');mp=sha(p)
  controls.append({'control':label,**run(q,mp=mp,cp=cp,ok=False)})
need(sha(P/'MANIFEST.json')==MP and all(sha(P/n)==v for n,v in rows.items()),'original packet unchanged')
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'result':'PASS','manifest_sha256':MP,'checker_sha256':CP,'closed_files':20,'baselines':runs,'negative_controls':controls,'remaining_actionable_administrative_issues':[],'scope':'offline byte and administrative consistency replay; no mathematical re-review, production mutation or network call'}
(M/'ROOT_FINAL_ADMIN_PACKET_REPLAY.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'result':'PASS','baselines':4,'negative_controls':7,'closed_files':20}))
