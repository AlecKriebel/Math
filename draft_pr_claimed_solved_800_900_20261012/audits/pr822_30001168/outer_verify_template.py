#!/usr/bin/env python3
"""Bind the current repository package; arithmetic replays do not prove the analytic lemmas."""
import argparse,hashlib,json,stat,subprocess,sys,zipfile
from pathlib import Path,PurePosixPath
def need(ok,label):
 if not ok:raise RuntimeError(label)
def unique(pairs):
 d={}
 for k,v in pairs:
  need(k not in d,'duplicate JSON key');d[k]=v
 return d
def load(p):return json.loads(p.read_bytes(),object_pairs_hook=unique)
def bind(root,pin):
 manifest=root/'PUBLICATION_MANIFEST.json'
 need(stat.S_ISREG(manifest.lstat().st_mode),'regular manifest')
 need(hashlib.sha256(manifest.read_bytes()).hexdigest()==pin,'external outer manifest pin')
 d=load(manifest);need(d['format']=='weighted-yamabe-30001168-preprint-v2','outer format')
 rows=d['files'];names=[r['path'] for r in rows]
 need(len(names)==len(set(names)),'unique entries')
 need(all(type(n) is str and n==str(PurePosixPath(n)) and n not in ('','.','PUBLICATION_MANIFEST.json') and not n.startswith('/') and '..' not in PurePosixPath(n).parts and chr(92) not in n for n in names),'safe paths')
 dirs={str(p) for n in names for p in PurePosixPath(n).parents if str(p)!='.'}
 actual_files=set();actual_dirs=set()
 for p in root.rglob('*'):
  mode=p.lstat().st_mode;n=p.relative_to(root).as_posix()
  if stat.S_ISREG(mode):actual_files.add(n)
  elif stat.S_ISDIR(mode):actual_dirs.add(n)
  else:raise RuntimeError('nonregular member: '+n)
 need(actual_files==set(names)|{'PUBLICATION_MANIFEST.json'} and actual_dirs==dirs,'closed repository inventory')
 for r in rows:
  b=(root/r['path']).read_bytes()
  need(type(r['bytes']) is int and len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256'],'member binding: '+r['path'])
 return len(actual_files)
def main():
 a=argparse.ArgumentParser();a.add_argument('trusted_manifest_sha256');a.add_argument('--full',action='store_true');args=a.parse_args()
 root=Path(__file__).absolute().parent;count=bind(root,args.trusted_manifest_sha256)
 pub=root/'publication_20261013';pre=pub/'preprint';package=pub/'verification_package'
 metadata=load(root/'PUBLICATION_METADATA.json');kit=load(pre/'zenodo-deposit.json')
 need(kit['metadata']==load(package/'metadata.json')==metadata['zenodo_metadata'],'current metadata identity')
 need((pre/'note.tex').read_bytes()==(package/'note.tex').read_bytes(),'current note source')
 need((pre/'output/pdf/note.pdf').read_bytes()==(package/'note.pdf').read_bytes(),'current PDF')
 with zipfile.ZipFile(pre/'verification.zip') as z:
  entries=z.infolist();names=[i.filename for i in entries]
  need(len(names)==len(set(names))==metadata['verification_members'],'archive inventory')
  for i in entries:
   n=PurePosixPath(i.filename)
   need(not i.is_dir() and not n.is_absolute() and '..' not in n.parts and str(n)==i.filename and stat.S_ISREG(i.external_attr>>16),'regular safe ZIP member')
   need(z.read(i)==(package/i.filename).read_bytes(),'ZIP/extracted identity')
 frozen=package/'source'
 changed_wrappers={'PUBLICATION_MANIFEST.json','PUBLICATION_METADATA.json','README.md','RESEARCH_LOG.md','verify_publication.py','package_controls.py'}
 for p in frozen.rglob('*'):
  if p.is_file() and p.relative_to(frozen).as_posix() not in changed_wrappers:
   need(p.read_bytes()==(root/p.relative_to(frozen)).read_bytes(),'preserved original payload')
 flags=['-I','-B']+(['-O'] if sys.flags.optimize else [])
 cmd=[sys.executable,*flags,str(package/'verify_package.py'),metadata['package_index_sha256']]+(['--full'] if args.full else [])
 r=subprocess.run(cmd,cwd='/',capture_output=True,text=True,timeout=900)
 need(r.returncode==0,'inner package verification: '+r.stderr)
 result={'status':'PASS','regular_files':count,'archive_members_verified':len(entries),'inner':json.loads(r.stdout),'analytic_proof_verified_by_program':False}
 bind(root,args.trusted_manifest_sha256);print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':main()
