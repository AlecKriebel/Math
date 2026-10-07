#!/usr/bin/env python3
"""Offline integrity, exact patch, deterministic controls, and corruption checks."""
import argparse, hashlib, json, re, shutil, subprocess, sys, tempfile
from pathlib import Path
PINS={
 'author/AUTHOR_MANIFEST.json':'c2dbe9efd1dcd44ee5621da4e1341ac0be078d5ccbfce614fa5f4532ab8ec048',
 'author/PROOF.md':'2b723d96cca5e1415f09dee97567c2711259e16c062cc6818d84b5a93bb9a4b8',
 'audit/AUDIT_MANIFEST.json':'b7d8ba56f95155120bc668a06199486960c217d0833d77a4368d1bfd6ead38cc',
 'audit/PROOF_CORRECTED_READING_COPY.md':'83f24e659b0527695c756f3e29600722f7b15409afe87e85007aaf3e8f2c7e4f',
 'audit/PRIME_END_WORDING.patch':'5d2cc5c89e40724424ec2ce00a83a612dc6d254b1c1f4899eb546cdb6cca2107',
}
def require(ok,msg):
 if not ok:raise ValueError(msg)
def digest(b):return hashlib.sha256(b).hexdigest()
def check_manifest(base,name):
 m=json.loads((base/name).read_text()); seen=set()
 for e in m['files']:
  path=e['path']; require(path not in seen and not Path(path).is_absolute() and '..' not in Path(path).parts,'unsafe/duplicate manifest path');seen.add(path)
  p=base/path;require(p.is_file() and not p.is_symlink(),'missing/nonregular '+path)
  b=p.read_bytes();require(len(b)==e['bytes'] and digest(b)==e['sha256'],'manifest mismatch '+path)
 return seen

def apply_patch(original,patch):
 src=original.decode().splitlines(keepends=True);pl=patch.decode().splitlines(keepends=True)
 require(pl[:2]==['--- a/PROOF.md\n','+++ b/PROOF.md\n'],'patch headers')
 out=[];pos=0;i=2;hunks=0
 while i<len(pl):
  m=re.fullmatch(r'@@ -(\d+),(\d+) \+(\d+),(\d+) @@\n',pl[i]);require(m is not None,'invalid hunk')
  a,n,c,k=map(int,m.groups());i+=1;hunks+=1;require(a-1>=pos,'overlapping patch')
  out+=src[pos:a-1];pos=a-1;require(len(out)==c-1,'new hunk position');old=new=0
  while i<len(pl) and not pl[i].startswith('@@ '):
   line=pl[i];i+=1;require(line and line[0] in ' +-','invalid patch line')
   if line[0] in ' -':require(pos<len(src) and src[pos]==line[1:],'patch context mismatch');pos+=1;old+=1
   if line[0] in ' +':out.append(line[1:]);new+=1
  require((old,new)==(n,k),'hunk counts')
 require(hunks==1,'unexpected hunk count');out+=src[pos:];return ''.join(out).encode()

def verify(base,run_controls=True):
 base=Path(base); inventory=check_manifest(base,'PUBLICATION_MANIFEST.json')|{'PUBLICATION_MANIFEST.json'}
 found={p.relative_to(base).as_posix() for p in base.rglob('*') if p.is_file() or p.is_symlink()}
 require(found==inventory,'packet inventory differs')
 require(not any(p.is_symlink() for p in base.rglob('*')),'symlink in packet')
 for path,h in PINS.items():require(digest((base/path).read_bytes())==h,'frozen input differs '+path)
 for sub,name in [('author','AUTHOR_MANIFEST.json'),('audit','AUDIT_MANIFEST.json')]:
  names=check_manifest(base/sub,name)|{name};require(names=={p.name for p in (base/sub).iterdir()},'frozen subpacket inventory')
 require(apply_patch((base/'author/PROOF.md').read_bytes(),(base/'audit/PRIME_END_WORDING.patch').read_bytes())==(base/'audit/PROOF_CORRECTED_READING_COPY.md').read_bytes(),'patch does not reproduce corrected proof')
 report={'problem_id':5300048,'status':'pass','files_checked':len(found),'originals_preserved':True,'patch_reproduces_corrected_proof':True,'author_assertions':5963,'independent_assertions':26958,'controls_rerun':run_controls,'scope':'Finite diagnostics and packet integrity; no formal or universal analytic proof certification.'}
 if run_controls:
  author=subprocess.run([sys.executable,str(base/'author/verify_controls.py'),'--check-result','--check-manifest'],capture_output=True,text=True,check=True)
  parsed=json.loads(author.stdout[author.stdout.index('{'):]);frozen=json.loads((base/'author/CONTROL_RESULTS.json').read_text());require(parsed==frozen and parsed['total_assertions']==5963 and parsed['status']=='pass','author controls')
  independent=subprocess.run([sys.executable,str(base/'audit/verify_independent_controls.py')],capture_output=True,text=True,check=True)
  parsed=json.loads(independent.stdout);frozen=json.loads((base/'audit/INDEPENDENT_CONTROL_RESULTS.json').read_text());require(parsed==frozen and parsed['total_assertions']==26958 and parsed['status']=='pass','independent controls')
 return report

def mutation_controls(base):
 cases=[('original proof corruption','author/PROOF.md','append'),('corrected proof corruption','audit/PROOF_CORRECTED_READING_COPY.md','append'),('patch corruption','audit/PRIME_END_WORDING.patch','append'),('author result corruption','author/CONTROL_RESULTS.json','append'),('audit result corruption','audit/INDEPENDENT_CONTROL_RESULTS.json','append'),('missing audit','audit/ACCEPTANCE_REPORT.md','delete'),('unexpected source file','unexpected_source.pdf','append'),('frozen manifest corruption','author/AUTHOR_MANIFEST.json','append'),('rehashed proof corruption','author/PROOF.md','rehash'),('manifest duplicate','PUBLICATION_MANIFEST.json','duplicate'),('unlisted file','README.md','unlist')]
 results=[]
 for label,rel,kind in cases:
  with tempfile.TemporaryDirectory(prefix='accessibility-packet-') as tmp:
   root=Path(tmp)/'packet';shutil.copytree(base,root);p=root/rel
   if kind=='delete':p.unlink()
   elif kind in ('append','rehash'):p.write_bytes((p.read_bytes() if p.exists() else b'')+b'corruption\n')
   mpath=root/'PUBLICATION_MANIFEST.json';m=json.loads(mpath.read_text())
   if kind=='rehash':
    for e in m['files']:
     if e['path']==rel:e.update(bytes=len(p.read_bytes()),sha256=digest(p.read_bytes()))
    mpath.write_text(json.dumps(m))
   if kind=='duplicate':m['files'].append(m['files'][0]);mpath.write_text(json.dumps(m))
   if kind=='unlist':m['files']=[e for e in m['files'] if e['path']!=rel];mpath.write_text(json.dumps(m))
   try:verify(root,False)
   except (ValueError,OSError,KeyError) as e:results.append({'case':label,'rejected':True})
   else:raise ValueError('mutation accepted: '+label)
 return results

def main():
 p=argparse.ArgumentParser();p.add_argument('--mutation-controls',action='store_true');args=p.parse_args();base=Path(__file__).resolve().parent
 result=verify(base)
 if args.mutation_controls:result['mutation_controls']=mutation_controls(base)
 print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':main()
