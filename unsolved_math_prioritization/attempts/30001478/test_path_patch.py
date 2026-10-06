#!/usr/bin/env python3
"""Apply the actual reviewed two-line delta in a disposable extraction only."""
import hashlib,json,os,shutil,subprocess,sys,tempfile,zipfile
from pathlib import Path
def need(ok,msg):
 if not ok:raise ValueError(msg)
def run(root,entry,optimized):
 return subprocess.run([sys.executable,'-I','-B']+(['-O'] if optimized else [])+[str(root/entry)],cwd=root.parent,text=True,capture_output=True,timeout=240)
def rehash(root):
 p=root/'manifest.json';m=json.loads(p.read_text())
 for n in m['files']:
  b=(root/n).read_bytes();m['files'][n]={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
 p.write_text(json.dumps(m,sort_keys=True,indent=2)+'\n')
def main():
 root=Path(__file__).absolute().parent;archive=root/'archives/PRIME_IDEALS_30001478_INDEPENDENT_AUDIT_SAFE.zip';before=archive.read_bytes();need(hashlib.sha256(before).hexdigest()=='075159f6da95ded37cbeb3aab31aa8cd26a441b3e2e1f53e18fcd1a41f0d8ae6','audit archive pin')
 patch=root/'second_review/verifier_path_hardening.patch';expected=(root/'second_review/manifest.json').read_text();m=json.loads(expected)['files'][patch.name];b=patch.read_bytes();need(len(b)==m['bytes'] and hashlib.sha256(b).hexdigest()==m['sha256'],'patch identity')
 results=[]
 with tempfile.TemporaryDirectory(prefix='prime actual patch ') as d:
  work=Path(d)/'patched audit with spaces';work.mkdir()
  with zipfile.ZipFile(archive) as z:z.extractall(work)
  prior={p.relative_to(work).as_posix():p.read_bytes() for p in work.rglob('*') if p.is_file()}
  applied=subprocess.run(['patch','--batch','--forward','-p1','-i',str(patch)],cwd=work,text=True,capture_output=True,timeout=20);need(applied.returncode==0,'actual patch failed: '+applied.stderr)
  changed={p.relative_to(work).as_posix() for p in work.rglob('*') if p.is_file() and prior.get(p.relative_to(work).as_posix())!=p.read_bytes()};need(changed=={'author/verify.py','verify_audit.py'},'unexpected patch delta')
  for name in changed:need((work/name).read_bytes()==prior[name].replace(b'Path(__file__).resolve().parent',b'Path(__file__).absolute().parent'),'not exact two-line delta')
  rehash(work/'author');rehash(work)
  for folder,entry in [('author','verify.py'),('audit','verify_audit.py')]:
   original=work/'author' if folder=='author' else work
   for opt in (False,True):
    p=run(original,entry,opt);need(p.returncode==0 and json.loads(p.stdout)['status']=='PASS','patched baseline: '+p.stderr)
    copy=Path(d)/(folder+str(opt));shutil.copytree(original,copy);(copy/entry).unlink();(copy/entry).symlink_to(original/entry);(copy/'extra.txt').write_text('unexpected')
    p=run(copy,entry,opt);need(p.returncode!=0,'patched self symlink accepted');results.append({'target':folder,'optimized':opt,'baseline':'PASS','self_symlink':'REJECT'})
 need(archive.read_bytes()==before,'immutable archive changed')
 print(json.dumps({'status':'PASS','actual_patch_command_applied':True,'changed_code_files':['author/verify.py','verify_audit.py'],'inner_then_outer_manifests_rebuilt':True,'checks':results,'patched_derivative_published':False,'immutable_archive_unchanged':True},sort_keys=True,indent=2))
if __name__=='__main__':
 try:main()
 except Exception as e:print('FAIL: '+str(e),file=sys.stderr);sys.exit(1)
