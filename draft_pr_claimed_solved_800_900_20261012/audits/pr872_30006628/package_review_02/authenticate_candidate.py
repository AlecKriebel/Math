#!/usr/bin/env python3
"""Independent read-only authentication. No candidate code is imported or run."""
import hashlib, json, os, stat, subprocess, sys, zipfile
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
ROOT=BASE.parents[1]/'work/pr872_revision_r1'
OUT=Path(__file__).resolve().parent
PINS={'seal':'9eafa209f3bb74f1ba81fd8eef52087e0d16ea4b05ae8624a1c2a4e36ec5ef22','outer':'02d511d2c24414615006dd1e97e134061c65888955f534c25d1c12e4edc4d8be','startup':'57b78a4813329b5964f94879b3fbff796d2e0d1e1298f3889b804117ec06d8fe'}
def check(ok,why):
 if not ok: raise ValueError(why)
def h(b):return hashlib.sha256(b).hexdigest()
def regular(p):
 s=p.lstat(); check(stat.S_ISREG(s.st_mode),str(p));return p.read_bytes()
def pin(p,d):
 b=regular(p);check(h(b)==d,str(p)+' hash');return b
seal=json.loads(pin(BASE/'PACKAGE_SEAL_R1.json',PINS['seal']))
manifest=json.loads(pin(ROOT/'PUBLICATION_MANIFEST.json',PINS['outer']))
pin(ROOT/'verify_current_publication.py',PINS['startup'])
rows=manifest['files']; names={r['path'] for r in rows}|{'PUBLICATION_MANIFEST.json'}
seen=set()
for folder,dirs,files in os.walk(ROOT,followlinks=False):
 for name in dirs+files:
  p=Path(folder)/name;s=p.lstat();check(not stat.S_ISLNK(s.st_mode),'alias')
  check(stat.S_ISDIR(s.st_mode) or stat.S_ISREG(s.st_mode),'special')
  if stat.S_ISREG(s.st_mode):seen.add(p.relative_to(ROOT).as_posix())
check(seen==names,'closed outer files')
for r in rows:
 b=pin(ROOT/r['path'],r['sha256']);check(len(b)==r['bytes'],'outer size')
seal_receipts=[]
for r in seal['receipts']:
 b=pin(BASE/r['path'],r['sha256']);check(len(b)==r['bytes'],'external receipt size');seal_receipts.append(r)
core=[]
for r in seal['core_files']:
 b=pin(ROOT/'publication_20261015/preprint'/r['path'],r['sha256']);check(len(b)==r['bytes'],'core size')
 check(b==regular(BASE/'preprint'/r['path']),'canonical copy '+r['path']);core.append(r)
portable=ROOT/'publication_20261015/verification_package'
idx=json.loads(pin(portable/'package_index.json',seal['index_sha256']))
check(len(idx['files'])+1==143,'portable count')
with zipfile.ZipFile(ROOT/'publication_20261015/preprint/verification.zip') as z:
 check(set(z.namelist())=={r['path'] for r in idx['files']}|{'package_index.json'},'ZIP set')
 check(len(z.namelist())==143,'ZIP duplicates')
 for name in z.namelist():check(z.read(name)==regular(portable/name),'ZIP member')
source=json.loads(regular(portable/'root_evidence/SOURCE_MANIFEST.json'))
check(h(regular(portable/'root_evidence/SOURCE_MANIFEST.json'))=='4589f9b70e9a65ae67356544b5ad59644290902bb9b3df80406710a22559e3f8','source pin')
originals=[]
for r in source['files']:
 b=pin(portable/'source'/r['path'],r['sha256']);check(len(b)==r['bytes'],'original size')
 git=subprocess.run(['git','show',source['frozen_head']+':'+source['source_prefix']+r['path']],cwd=ROOT,capture_output=True)
 check(git.returncode==0 and git.stdout==b,'frozen Git head mismatch '+r['path'])
 check(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==r['git_blob'],'git blob')
 if r['path'] not in ('PUBLICATION_MANIFEST.json','README.md'):check(b==regular(ROOT/r['path']),'preserved root')
 originals.append(r)
meta=json.loads(regular(portable/'metadata.json'));deposit=json.loads(regular(ROOT/'publication_20261015/preprint/zenodo-deposit.json'));current=json.loads(regular(ROOT/'CURRENT_PUBLICATION.json'))
check(meta==deposit['metadata']==current['zenodo_metadata']==json.loads(regular(ROOT/'publication_20261015/preprint/metadata.json')),'metadata equality')
check(deposit['files']==[{'path':'output/pdf/note.pdf','name':'property-t-free-product-note.pdf'},{'path':'verification.zip','name':'property-t-free-product-verification.zip'}],'exact 2 deposit files')
check(meta['creators']==[{'name':'Kriebel, Alec','affiliation':'Independent researcher','orcid':'0009-0001-9320-500X'}],'author')
result={'status':'PASS','external_pins':PINS,'outer_files':len(seen),'portable_members':143,'sealed_external_receipts':seal_receipts,'core':core,'frozen_originals_from_git_head':originals,'preserved_root_copies':13,'metadata_and_exact_two_file_deposit':'PASS','candidate_code_executed':False,'candidate_files_changed':False}
(OUT/(sys.argv[1] if len(sys.argv)>1 else 'INITIAL_AUTHENTICATION.json')).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':'PASS','outer_files':len(seen),'core_files':len(core),'originals':len(originals),'portable_members':143}))
