import hashlib,json,os,sys,zipfile
from pathlib import Path
sys.dont_write_bytecode=True
D=Path(__file__).resolve().parent;A=D.parents[1];P=A/'NEWpreprint_v1_0';Z='PR1071_preprint_v1_0_support.zip'
def pin(p,n):
 b=p.read_bytes();return {'path':str(n),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def write(p,o):p.write_text(json.dumps(o,indent=2)+'\n')
m=json.loads((P/'PACKAGE_MANIFEST.json').read_text());m['members']=[pin(P/r['path'],r['path']) for r in m['members']];write(P/'PACKAGE_MANIFEST.json',m)
t=P/(Z+'.history-order-tmp')
with zipfile.ZipFile(t,'w',compression=zipfile.ZIP_STORED,allowZip64=False) as z:
 for name in sorted([r['path'] for r in m['members']]+['PACKAGE_MANIFEST.json']):
  i=zipfile.ZipInfo(name,(2026,10,14,0,0,0));i.create_system=3;i.external_attr=0o100644<<16;z.writestr(i,(P/name).read_bytes())
os.replace(t,P/Z);r=pin(P/Z,Z);(P/(Z+'.sha256')).write_text(r['sha256']+'  '+Z+'\n');b=json.loads((P/'UPLOAD_BINDINGS.json').read_text());b['archive']['bytes']=r['bytes'];b['archive']['sha256']=r['sha256'];b['manifest_sha256']=pin(P/'PACKAGE_MANIFEST.json','')['sha256'];write(P/'UPLOAD_BINDINGS.json',b)
s=json.loads((D/'BUILD_SUMMARY.json').read_text());s['archive']=r;write(D/'BUILD_SUMMARY.json',s);print(json.dumps(r))
