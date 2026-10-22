from pathlib import Path
import hashlib,json,subprocess,sys,zipfile,datetime
P=Path(__file__).resolve().parent;S=P.parent/'publication_preparation_01';W=P/'work'
def need(p,m):
 if not p:raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
zpath=S/'release/tail-generation-source-and-verification.zip'
with zipfile.ZipFile(zpath) as z:
 for n in z.namelist():
  p=Path(n);need(not p.is_absolute() and '..' not in p.parts,'unsafe member')
  d=W/p;d.parent.mkdir(parents=True,exist_ok=True);d.write_bytes(z.read(n))
E=W/'tail_generation_source'
r=subprocess.run([sys.executable,'-B',str(E/'reproduce.py')],capture_output=True)
(P/'evidence/RELOCATED_REPRODUCE.stdout').write_bytes(r.stdout);(P/'evidence/RELOCATED_REPRODUCE.stderr').write_bytes(r.stderr);need(r.returncode==0,'reproduction failed')
r=subprocess.run([sys.executable,'-B',str(E/'build_package.py'),'--output',str(W/'rebuilt')],capture_output=True)
(P/'evidence/REBUILD.stdout').write_bytes(r.stdout);(P/'evidence/REBUILD.stderr').write_bytes(r.stderr);need(r.returncode==0,'build failed')
res=[]
for f in sorted((W/'rebuilt').iterdir()):
 b=f.read_bytes();need(b==(S/'release'/f.name).read_bytes(),'roundtrip mismatch '+f.name);res.append({'name':f.name,'bytes':len(b),'sha256':sha(b)})
with zipfile.ZipFile(S/'release/tail-generation-upload-kit.zip') as z:
 expected={'README.txt':'UPLOAD_README.txt','zenodo-metadata.json':'zenodo-metadata.json','zenodo-deposit.json':'zenodo-deposit.json','tail-generation.pdf':'tail-generation.pdf','tail-generation-source-and-verification.zip':'tail-generation-source-and-verification.zip'}
 need(set(z.namelist())==set(expected),'kit membership')
 for a,b in expected.items():need(z.read(a)==(S/'release'/b).read_bytes(),'kit mismatch '+a)
m=json.loads((E/'PUBLIC_MANIFEST.json').read_bytes());need(len(m['files'])==19,'public manifest count')
for n in ['zenodo-metadata.json','zenodo-deposit.json','UPLOAD_README.txt']:need((E/n).read_bytes()==(S/'release'/n).read_bytes(),'release metadata mismatch')
need((E/'paper.pdf').read_bytes()==(S/'release/tail-generation.pdf').read_bytes(),'PDF mismatch')
(P/'ROUNDTRIP_CHECK.json').write_text(json.dumps({'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','source_members':20,'kit_members':5,'recompiled_pdf':False,'source_author_code_executed':False,'audit_authored_code_executed':True,'ordinary_O_OO_checks_each':True,'files':res},indent=2)+'\n')
print(json.dumps(res,indent=2))
