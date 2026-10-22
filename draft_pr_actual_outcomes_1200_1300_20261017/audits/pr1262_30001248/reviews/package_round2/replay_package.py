#!/usr/bin/env python3
"""Exact archive authentication and scratch-only three-mode verifier/workflow replay."""
from pathlib import Path
import datetime,hashlib,json,os,shutil,subprocess,sys,zipfile
R=Path(__file__).resolve().parent;A=R.parents[1];P=A/'publication';S=R/'_local';S.mkdir(exist_ok=True)
def require(x,m):
 if not x:raise RuntimeError(m)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
build=json.loads((P/'BUILD_RECEIPT.json').read_text());frozen=json.loads((R/'INPUT_FREEZE.json').read_text());fb={x['path']:x for x in frozen['files']}
# BUILD receipt is itself authenticated by the independent outside INPUT_FREEZE.
require(digest(P/'BUILD_RECEIPT.json')==fb['publication/BUILD_RECEIPT.json']['sha256'],'untrusted BUILD')
root=S/'portable';root.mkdir(exist_ok=True)
with zipfile.ZipFile(P/build['verification_zip']['path']) as z:
 names=z.namelist();require(len(names)==len(set(names))==192,'archive inventory');require(z.testzip() is None,'ZIP CRC')
 for n in names:
  require(not n.startswith('/') and '..' not in Path(n).parts and '\\' not in n,'unsafe ZIP member')
  b=z.read(n);require(b==(P/'verification'/n).read_bytes(),'ZIP/deployed member drift '+n)
  q=root/n;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(b)
 for n in ('ACCEPTANCE.json','ACCEPTANCE.md','AUDIT.md','MANIFEST.json','PROOF.md','README.md','SOURCES.json','VERIFICATION.json'):
  require(z.read('original_submitted/'+n)==(A/'submitted'/n).read_bytes(),'original '+n)
  require(z.read('current_edition/'+n)==(A/'current_edition'/n).read_bytes(),'current '+n)
anchors=build['verification_anchors'];args=[a for k,v in anchors.items() for a in ('--expected-'+k+'-sha256',v)]
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');env.pop('PYTHONOPTIMIZE',None)
results=[]
for mode in ([],['-O'],['-OO']):
 r=subprocess.run([sys.executable,'-B',*mode,str(root/'verify.py'),*args],cwd=root,env=env,capture_output=True,text=True,timeout=180)
 require(r.returncode==0,r.stderr);results.append({'mode':mode,'result':json.loads(r.stdout)})
(R/'PORTABLE_REPLAYS.json').write_text(json.dumps({'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_archive_members':len(names),'all_zip_members_equal_actual_deployed':True,'outside_build_receipt_sha256':digest(P/'BUILD_RECEIPT.json'),'anchors':anchors,'runs':results},indent=2)+'\n')
# Copy actual workflow to our own scratch layout; every potential write stays here.
program=S/'program';audit=program/'audits/pr1262_30001248';pub=audit/'publication';pub.mkdir(parents=True,exist_ok=True)
for name in ('prepare_package.py','build_package.py','compile_note.py','verification/verify.py','append_tracker.py','update_pr_publication.py','check_public_downloads.py','workflow_regression.py','zenodo-deposit.json'):
 q=pub/name;q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(P/name,q)
coord=program/'publication_coordinators/pr1262.py';coord.parent.mkdir(exist_ok=True);shutil.copyfile(A.parents[1]/'publication_coordinators/pr1262.py',coord)
runs=[]
for mode in ([],['-O'],['-OO']):
 r=subprocess.run([sys.executable,'-B',*mode,str(pub/'workflow_regression.py'),'--worker'],env=env,capture_output=True,text=True,timeout=180)
 require(r.returncode==0,r.stderr);runs.append({'mode':mode,'result':json.loads(r.stdout)})
require(all(x['result']==runs[0]['result'] for x in runs),'optimization dependent workflow')
(R/'WORKFLOW_REPLAYS.json').write_text(json.dumps({'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Hash-identical actual deployed helpers in own scratch layout. Compiler/services/Git mocked by worker. No real final gate generated.','all_modes_identical':True,'runs':runs},indent=2)+'\n')
print(json.dumps({'portable_modes':3,'workflow_modes':3,'status':'PASS'}))
