#!/usr/bin/env python3
"""Build only the explicit PR952 public payload selection. No network or acceptance."""
import sys
if not(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):raise SystemExit('Use -I -S -B')
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,stat,zipfile
D=Path(__file__).absolute().parent;A=D.parent
FAMILIES={
'algebra_falsifier_01':'8bc684c6ed22cf0563e1533598141e2774cc093751b30a0737ad05f734b31810',
'quantum_bridge_01':'43af008160113d1b96c98ec2ce1f292d7344d6f71723f5e01caf57ced15b3e67',
'computation_01':'53378849c7b7cfa15948ca8ead4f09965c59da150e89e79b61b4048898b7f0ed',
'classical_priority_01':'b4c9078c6e94c614a957a663afa2ded74e5ab4898ec4163af22446c036510acc',
'recent_priority_01':'fc7478c5356a5ca5f1960f6c98137df3947cb7bc9c0845a4239d06ec1173d7ae'}
ENG='cda9dbdf2440b3f83074c80959d3678d2e421fbe1635a78abe76e516e7d8b712'
PDF='habiro-rank-interpolation-v1.0.pdf';ZIP='habiro-rank-interpolation-verification-v1.0.zip'
def need(x,s):
 if not x:raise RuntimeError(s)
def sha(b):return hashlib.sha256(b).hexdigest()
def data(p):
 need(not p.is_symlink() and not any(q.is_symlink() for q in p.parents),'link input')
 st=p.stat();need(stat.S_ISREG(st.st_mode) and st.st_nlink==1,'regular single-link input')
 b=p.read_bytes();need(len(b)==st.st_size and p.read_bytes()==b,'input drift');return b
def pin(b):return {'bytes':len(b),'sha256':sha(b),'mode':'100644'}
def family_records(m):
 if type(m.get('files')) is dict:return m['files']
 xs=m.get('payloads',m.get('public_payloads',m.get('files')))
 need(type(xs)is list,'known explicit route schema')
 return {x['path']:x for x in xs}
selected={}
def put(n,b):
 need(n not in selected,'duplicate selection');need('private' not in [x.lower() for x in Path(n).parts],'private selection')
 selected[n]=b
def copy(n,p):put(n,data(p))
for name,expected in FAMILIES.items():
 folder=A/'reviews'/name;raw=data(folder/'MANIFEST.json');need(sha(raw)==expected,'family external seal '+name);m=json.loads(raw);records=family_records(m)
 for n,p in records.items():
  b=data(folder/n);need(len(b)==p['bytes'] and sha(b)==p['sha256'],'family payload '+n);put('reviews/'+name+'/'+n,b)
 put('reviews/'+name+'/MANIFEST.json',raw)
folder=A/'package_engineering_01';raw=data(folder/'MANIFEST.json');need(sha(raw)==ENG,'engineering seal');m=json.loads(raw)
need(type(m['explicit_public_allowlist'])is list and set(m['files'])==set(m['explicit_public_allowlist']),'engineering explicit closure')
for n,p in m['files'].items():
 b=data(folder/n);need(len(b)==p['bytes'] and sha(b)==p['sha256'],'engineering payload');put('engineering/'+n,b)
put('engineering/MANIFEST.json',raw)
copy('verify_package.py',folder/'verify_package.py')
copy('checks/independent_math.py',folder/'independent_math.py')
originals=json.loads(data(A/'ORIGINAL_SNAPSHOT.json'))
need(originals['head']=='989a532ae1d50894190d010a0a02ba8c3d71ee05' and len(originals['files'])==33,'original identity')
for n,h in originals['files'].items():
 b=data(A/'original'/n);need(sha(b)==h,'original pin');put('original/'+n,b)
for n in ['README.md','AUDIT_LIMITS.md','AUTHORSHIP_PROVENANCE.md','SOURCE_MAP.md','SUPPLEMENT.md','VERIFICATION.md']:copy(n,D/n)
copy('INHERITED_FINDING_DISPOSITIONS.json',D/'FINDING_DISPOSITIONS.json')
copy('paper/main.tex',D/'note.tex');copy('paper/'+PDF,D/PDF)
root_names=[
'ELIGIBILITY_GATE.json','TARGET_IDENTITY_PREFLIGHT.json','ORIGINAL_SNAPSHOT.json','ORIGINAL_FILE_RECORDS.json','NATIVE_ACCOUNTING_BASELINE.json',
'RESEARCH_CHARTER.md','ROOT_INITIAL_FALSIFICATION.md','ROOT_PRIMARY_RETRIEVAL.json','ROOT_PRIMARY_SELECTED_READINGS.json',
'ROOT_ALGEBRA01_AUTHENTICATION.json','ROOT_QUANTUM_BRIDGE01_AUTH_ATTEMPT01_FAILURE.json','ROOT_QUANTUM_BRIDGE01_AUTHENTICATION.json',
'ROOT_COMPUTATION01_AUTHENTICATION.json','ROOT_ALGEBRA01_AND_QUANTUM01_INTAKE.json','ROOT_COMPUTATION01_INTAKE.json',
'ROOT_PORTABLE_REPLAY.json','ROOT_LINUX_AVAILABILITY_PROBE_INITIAL.json','ROOT_LINUX_AVAILABILITY_PROBE.json',
'ROOT_CLASSICAL_PRIORITY01_AUTHENTICATION.json','ROOT_CLASSICAL_PRIORITY01_AUTH_ATTEMPT01_FAILURE.json','ROOT_RECENT_PRIORITY01_AUTHENTICATION.json',
'ROOT_PRIORITY_INTAKE.json','ROOT_PACKAGE_ENGINEERING01_AUTHENTICATION.json','ROOT_PACKAGE_ENGINEERING01_INTAKE.json','ROOT_PAPER_CANDIDATE03_QA.json']
for n in root_names:copy('audit/root/'+n,A/n)
findings=json.loads(selected['INHERITED_FINDING_DISPOSITIONS.json'])
for f in findings['findings']:
 for n in f['evidence']:need(n in selected,'finding evidence locator missing: '+n)
package=D/'package';need(not package.exists(),'fresh build root required; preserve earlier candidate before rebuild')
package.mkdir()
for n,b in selected.items():
 p=package/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b);p.chmod(0o644)
manifest={'schema':'pr952-sourcefree-package-v1','version':1,'problem_id':10400145,'original_head':originals['head'],'files':{n:pin(b) for n,b in sorted(selected.items())},'archives':{}}
raw=(json.dumps(manifest,indent=2,sort_keys=True)+'\n').encode();(package/'PACKAGE_MANIFEST.json').write_bytes(raw);(package/'PACKAGE_MANIFEST.json').chmod(0o644)
with zipfile.ZipFile(D/ZIP,'w',compression=zipfile.ZIP_STORED) as z:
 for n,b in sorted({**selected,'PACKAGE_MANIFEST.json':raw}.items()):
  i=zipfile.ZipInfo(n,date_time=(2026,10,16,0,0,0));i.create_system=3;i.external_attr=0o100644<<16;i.compress_type=zipfile.ZIP_STORED;z.writestr(i,b)
(D/ZIP).chmod(0o644)
receipt={'utc':datetime.now(timezone.utc).isoformat(),'status':'BUILT_EXPLICIT_PUBLIC_PACKAGE_NOT_ACCEPTED','package_payload_files':len(selected),'package_manifest_sha256':sha(raw),'verifier_sha256':sha(selected['verify_package.py']),'pdf':pin(selected['paper/'+PDF]),'zip':pin(data(D/ZIP)),'family_manifests':FAMILIES,'engineering_manifest_sha256':ENG,'originals':33,'third_party_bodies_included':False,'private_raw_source_included':False,'full_package_acceptance':False,'files':manifest['files']}
(D/'BUILD_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({k:v for k,v in receipt.items() if k!='files'}))
