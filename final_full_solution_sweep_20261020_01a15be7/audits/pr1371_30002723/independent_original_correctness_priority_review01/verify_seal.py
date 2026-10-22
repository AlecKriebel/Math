"""Read-only closed-tree and pinned-input verifier; never executes author code."""
import hashlib,json,os,stat,subprocess,sys
from pathlib import Path

def demand(ok,msg):
 if not ok:raise RuntimeError(msg)
def check_tree(root,m):
 demand(m['schema']=='independent-closed-audit-v1','schema')
 files=m['files'];dirs=m['directories'];names=[x['path'] for x in files]
 demand(len(set(names))==len(names),'duplicate files')
 for name in names+[x['path'] for x in dirs]:
  demand(not Path(name).is_absolute() and '..' not in Path(name).parts,'unsafe path')
 actual_files=[];actual_dirs=['.']
 for p in root.rglob('*'):
  demand(not p.is_symlink(),'symlink')
  demand(p.is_file() or p.is_dir(),'nonregular tree member')
  if p.is_file() and p.relative_to(root).as_posix()!='MANIFEST.json':actual_files.append(p.relative_to(root).as_posix())
  elif p.is_dir():actual_dirs.append(p.relative_to(root).as_posix())
 demand(set(names)==set(actual_files),'closed file membership')
 demand({x['path'] for x in dirs}==set(actual_dirs),'closed directory membership')
 for x in files:
  p=root/x['path'];s=p.stat();data=p.read_bytes()
  demand(len(data)==x['bytes'] and hashlib.sha256(data).hexdigest()==x['sha256'],'file bytes: '+x['path'])
  demand(stat.S_IMODE(s.st_mode)==x['mode'] and s.st_mtime_ns==x['mtime_ns'],'file metadata: '+x['path'])
 for x in dirs:
  s=(root/x['path']).stat()
  demand(stat.S_IMODE(s.st_mode)==x['mode'] and s.st_mtime_ns==x['mtime_ns'],'directory metadata: '+x['path'])
 return True

def mutations(root,m):
 altered=[]
 def copy():return json.loads(json.dumps(m))
 x=copy();x['schema']='bad';altered.append(x)
 x=copy();x['files'][0]['sha256']='0'*64;altered.append(x)
 x=copy();x['files'][0]['bytes']+=1;altered.append(x)
 x=copy();x['files'][0]['mode']^=0o100;altered.append(x)
 x=copy();x['files'][0]['mtime_ns']+=1;altered.append(x)
 x=copy();x['directories'][0]['mtime_ns']+=1;altered.append(x)
 x=copy();x['files'].append(x['files'][0]);altered.append(x)
 x=copy();x['files'][0]['path']='../outside';altered.append(x)
 x=copy();x['files'].pop();altered.append(x)
 for i,x in enumerate(altered):
  try:check_tree(root,x)
  except RuntimeError:continue
  raise RuntimeError('mutation escaped: '+str(i))
 return len(altered)

def main():
 root=Path(__file__).resolve().parent;m=json.loads((root/'MANIFEST.json').read_text());check_tree(root,m)
 st=(root/'MANIFEST.json').stat();demand(stat.S_IMODE(st.st_mode)==m['manifest_self']['mode'] and st.st_mtime_ns==m['manifest_self']['mtime_ns'],'manifest metadata')
 receipt=json.loads((root/'INPUT_RECEIPT.json').read_text())
 for x in receipt['blobs']:
  d=subprocess.check_output(['git','show',receipt['head']+':'+x['path']],cwd='/Users/alec/Documents/Math')
  demand(len(d)==x['bytes'] and hashlib.sha256(d).hexdigest()==x['sha256'],'pinned git blob')
 n=mutations(root,m)
 print(json.dumps({'status':'PASS','payload_members':len(m['files']),'directories':len(m['directories']),'payload_bytes':sum(x['bytes'] for x in m['files']),'pinned_blobs':len(receipt['blobs']),'in_memory_manifest_mutants_rejected':n,'manifest_sha256':hashlib.sha256((root/'MANIFEST.json').read_bytes()).hexdigest(),'manifest_mode':stat.S_IMODE(st.st_mode),'manifest_mtime_ns':st.st_mtime_ns,'read_only':True},sort_keys=True))
if __name__=='__main__':main()
