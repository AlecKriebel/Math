"""Independent read-only whole-review custody checker. Authenticate this file and manifest externally first."""
from pathlib import Path, PurePosixPath
import argparse,hashlib,json,os,stat,subprocess,sys,zipfile
SOURCE='b20f39f39a33b18822cff51850f8b5b220e139af4d7badec23a7f5a7e17805aa'
SOURCE_CHECKER='700eaab42e6d98589fb2f1c6fa4a3077b4dd74cad4f336a00cb53bd6dfe47489'
HEAD='aa44dec3baf8c1cd179cf8b55f32be95c74ee81a'
OUTPUTS={'main.tex':(11910,'f61324008c7b2fa99c4cc1b0d7f88921aa4dfc324a550e0b99662f6ff64367fd'),'output/pdf/paper.pdf':(60079,'c91648374d0467758de9773c95ef37b32c275993a20d2e0d9067c20702f18994'),'source-and-verification.zip':(338683,'9dfb13a945de2fe4d088eef8cd86ca1f9ecdb75b87162285a8fa4b7c1aab94b6'),'zenodo-deposit.json':(4814,'ccdb89bee9fabd3a544da90a783f9602e7c34f8122ee09d063bff1094d2893c4'),'zenodo-metadata.json':(4618,'2ae5c8869aac14300263e72b83d125e994b4caf814de77949c8359f7663df2e3'),'zenodo-upload-kit.zip':(368340,'2a6656e86604c57debd66ef2245a54fea402406fc0a1cca6266ebc100f0c13a9')}
def need(b,m):
 if not b:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def pairs(ps):
 d={}
 for k,v in ps:need(k not in d,'duplicate JSON key');d[k]=v
 return d
def js(b):return json.loads(b,object_pairs_hook=pairs,parse_constant=lambda s:(_ for _ in ()).throw(ValueError('nonfinite JSON')))
def safe(n):
 need(type(n)is str and n and '\\' not in n,'unsafe relative path')
 p=PurePosixPath(n);need(not p.is_absolute()and str(p)==n and all(x not in ('','.','..')for x in n.split('/')),'unsafe relative path');return n
def directory(p):
 p=Path(os.path.abspath(p))
 for x in [p,*p.parents]:need(stat.S_ISDIR(x.lstat().st_mode),'unsafe directory ancestry')
 return p
def read(p):
 directory(p.parent);st=p.lstat();need(stat.S_ISREG(st.st_mode)and st.st_nlink==1,'not single-link regular file')
 fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK)
 with os.fdopen(fd,'rb')as f:
  fs=os.fstat(f.fileno());need((st.st_dev,st.st_ino)==(fs.st_dev,fs.st_ino),'input raced');b=f.read()
 need(len(b)==st.st_size,'short read');return b
def inventory(root):
 directory(root);files={};dirs=set()
 for cur,ds,fs in os.walk(root,followlinks=False):
  for n in ds+fs:
   p=Path(cur)/n;rel=p.relative_to(root).as_posix();mode=p.lstat().st_mode
   if stat.S_ISDIR(mode):dirs.add(rel)
   else:files[rel]=read(p)
 want={str(x)for n in files for x in PurePosixPath(n).parents if str(x)!='.'}
 need(dirs==want,'unexpected empty directory');return files
def closed(root,pin,schema):
 files=inventory(root);raw=files['MANIFEST.json'];need(sha(raw)==pin,'external manifest mismatch');m=js(raw)
 need(set(m)=={'schema','files'}and m['schema']==schema,'manifest schema');expected=set()
 for r in m['files']:
  need(set(r)=={'path','bytes','sha256'}and type(r['bytes'])is int and r['bytes']>=0,'manifest row');n=safe(r['path']);need(n not in expected and n!='MANIFEST.json','duplicate/self row');expected.add(n)
  need(n in files and (len(files[n]),sha(files[n]))==(r['bytes'],r['sha256']),'bound bytes mismatch')
 need(set(files)==expected|{'MANIFEST.json'},'closed inventory mismatch');return files
def run(a):
 root=directory(a.packet);inv=Path(os.path.abspath(__file__));need(inv==root/'verify_review.py','entrypoint/root mismatch');need(sha(read(inv))==a.expected_checker_sha256,'external checker mismatch')
 own=closed(root,a.expected_manifest_sha256,'pr789-whole-preprint-round04/v1')
 source=directory(a.source);files=closed(source,SOURCE,'pr789-closed-source/v1');need(len(files)==151 and sha(files['verify_source.py'])==SOURCE_CHECKER,'source pins')
 ident=js(files['audit/intake/ROOT_SOURCE_IDENTITY.json']);need(ident['reviewed_head']==HEAD and len(ident['original_files'])==58,'scientific head')
 original=set()
 for r in ident['original_files']:
  n='audit/intake/original/'+safe(r['path']);need(n not in original,'duplicate original');original.add(n);b=files[n]
  need((len(b),sha(b))==(r['bytes'],r['sha256'])and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==r['git_blob'],'original identity')
 need({n for n in files if n.startswith('audit/intake/original/')}==original,'original closure')
 selected=js(files['audit/intake/SELECTED_PUBLIC_RECORD.json']);need(sha(selected['problem']['statement'].encode())=='628ed4ce70b7b62857ead560403291f24b890137a8073ce34a17c50d857aa3a6','statement');need(sha(json.dumps([selected['problem'],selected['prior_research']],sort_keys=True).encode())=='cf0071b62b0e096c74205deac1c8f7cad50cbbf50b4f37d8400170a2d742848f','selected pair')
 package=directory(a.package)
 for n,pin in OUTPUTS.items():b=read(package/n);need((len(b),sha(b))==pin,'distribution identity: '+n)
 with zipfile.ZipFile(package/'source-and-verification.zip')as z:
  names=z.namelist();need(len(names)==len(set(names))==151 and set(names)==set(files),'archive closure')
  need(all(z.read(n)==b for n,b in files.items()),'archive/source mismatch')
 metadata=js(files['zenodo-metadata.json'])['metadata'];need(metadata['related_identifiers'][3]=={'identifier':'1842/22886','relation':'references','scheme':'handle'},'canonical handle')
 need(js(read(package/'zenodo-deposit.json'))['metadata']==metadata,'deposit metadata mismatch')
 with zipfile.ZipFile(package/'zenodo-upload-kit.zip')as z:
  need(set(z.namelist())=={'README.md','paper.pdf','source-and-verification.zip','zenodo-deposit.json','zenodo-metadata.json'},'kit inventory')
  need(z.read('paper.pdf')==read(package/'output/pdf/paper.pdf')and z.read('source-and-verification.zip')==read(package/'source-and-verification.zip'),'kit payloads')
  need(z.read('zenodo-metadata.json')==files['zenodo-metadata.json']and js(z.read('zenodo-deposit.json'))['metadata']==metadata,'kit metadata')
 verdict=js(own['VERDICT.json']);need(verdict['result']=='PASS_COMPLETE_WHOLE_PREPRINT_REVIEW' and verdict['severity_counts']=={'critical':0,'high':0,'medium':0,'low':0} and verdict['actionable_findings']==[] and verdict['completion_percent']==100 and verdict['priority']=='UNRESOLVED' and verdict['firstness_certified'] is False and verdict['exhaustive_absence_certified'] is False and verdict['reviewed_head']==HEAD and verdict['source_manifest_sha256']==SOURCE,'review scope')
 replay=False
 if a.replay:
  p=subprocess.run([sys.executable,'-I','-B']+(['-O']if sys.flags.optimize else[])+[str(root/'check_math.py')],cwd='/',capture_output=True,text=True,timeout=60)
  need(p.returncode==0 and not p.stderr and js(p.stdout)==js(own['MATH_RESULTS.json']),'own exact math replay');replay=True
 need(inventory(root)==own and inventory(source)==files,'input changed')
 return {'result':'PASS','own_files':len(own),'source_files':151,'original_files':58,'distribution_files':6,'own_math_replayed':replay,'priority':'UNRESOLVED','scope':'Pinned custody and optional reviewer diagnostics; no universal-proof or historical-firstness automation.'}
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--packet',required=True,type=Path);p.add_argument('--source',required=True,type=Path);p.add_argument('--package',required=True,type=Path);p.add_argument('--expected-manifest-sha256',required=True);p.add_argument('--expected-checker-sha256',required=True);p.add_argument('--replay',action='store_true');a=p.parse_args()
 try:r=run(a)
 except Exception as e:print(json.dumps({'result':'FAIL','error':str(e)}));return 1
 print(json.dumps(r,sort_keys=True));return 0
if __name__=='__main__':sys.exit(main())
