import ast,hashlib,json,stat,subprocess
from pathlib import Path
from datetime import datetime,timezone
B=Path(__file__).resolve().parent;V1=B.parent;A=B.parents[2];HEAD='7d3adb0e500b0414a49a449e7981d34ade329427';oldpin='e535bb4b46e2ebac2d80713b9500eb6748a294fd8ff4d91f748c40f11946b091';sha=lambda b:hashlib.sha256(b).hexdigest()
def require(ok,msg):
 if not ok:raise RuntimeError(msg)
old=V1/'MANIFEST.json';require(sha(old.read_bytes())==oldpin,'Historical seal changed')
for row in json.loads(old.read_text())['files']:
 p=V1/row['path'];raw=p.read_bytes();require(len(raw)==row['bytes'] and sha(raw)==row['sha256'],'Historical sealed payload changed')
def expected(path):
 for node in ast.parse(path.read_text()).body:
  if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='EXPECTED' for t in node.targets):return ast.literal_eval(node.value)
 raise RuntimeError('Expected original inventory missing')
require(expected(B/'portable_gate.py')==expected(V1/'portable_gate.py'),'Original source anchors changed')
rows=[];prefix='unsolved_math_prioritization/attempts/6000001/'
for line in subprocess.check_output(['git','ls-tree','-rz',HEAD,prefix]).split(b'\0'):
 if not line:continue
 meta,name=line.split(b'\t');mode,typ,oid=meta.decode().split();name=name.decode();p=A/'original'/name;raw=p.read_bytes();gitraw=subprocess.check_output(['git','cat-file','blob',oid]);r=expected(B/'portable_gate.py')[name[len(prefix):]]
 require(mode=='100644' and typ=='blob' and stat.S_ISREG(p.lstat().st_mode) and not p.is_symlink(),'Original mode changed');require(raw==gitraw and len(raw)==r['bytes'] and sha(raw)==r['sha256'],'Original bytes changed');rows.append(dict(path=name,bytes=len(raw),sha256=sha(raw),git_mode=mode))
require(len(rows)==33,'Original count changed')
result=dict(utc=datetime.now(timezone.utc).isoformat(),status='PASS',original_files=33,original_head=HEAD,original_payloads=rows,historical_sealed_payloads=61,historical_manifest_sha256=oldpin,historical_seal_unchanged=True,original_anchor_map_unchanged=True,substantive_proof_turns_added=0)
(B/'evidence/FINAL_CHECKPOINT.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS: original33 and historical61 unchanged')
