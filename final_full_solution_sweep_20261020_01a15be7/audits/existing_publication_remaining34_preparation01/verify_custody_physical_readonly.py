"""Read stored custody without writes by default. Optional own temporary physical replay
is a diagnostic command, never source execution or original CASE restoration.
"""
from pathlib import Path
import json,gzip,hashlib,stat,os,shutil,argparse
O=Path(__file__).resolve().parent

def read_inventory(path):
 j=json.loads(gzip.decompress(path.read_bytes()));assert type(j['entries'])is dict
 for name,e in j['entries'].items():
  r=Path(name);assert not r.is_absolute()and'..'not in r.parts
  assert e['kind']in['file','directory']and type(e['mode'])is int and type(e['mtime_ns'])is int and type(e['nlink'])is int
  if e['kind']=='file':
   b=gzip.decompress((O/e['capture']).read_bytes());assert len(b)==e['bytes']and hashlib.sha256(b).hexdigest()==e['sha256']
 return j

def physical(path,j):
 root=O/'controls/physical_replay_temporary';assert not root.exists();root.mkdir();entries=j['entries'];peak=0;restored=0
 def metadata(p):
  s=p.lstat();return{'kind':'directory'if stat.S_ISDIR(s.st_mode)else'file'if stat.S_ISREG(s.st_mode)else'bad','mode':stat.S_IMODE(s.st_mode),'mtime_ns':s.st_mtime_ns,'nlink':s.st_nlink}
 try:
  for name,e in sorted(entries.items(),key=lambda x:len(Path(x[0]).parts)):
   p=root if name=='.'else root/name
   if name=='.':continue
   if e['kind']=='directory':p.mkdir()
   else:p.write_bytes(b'')
  for name,e in sorted(entries.items(),key=lambda x:-len(Path(x[0]).parts)):
   p=root if name=='.'else root/name;os.chmod(p,e['mode']);os.utime(p,ns=(p.stat().st_atime_ns,e['mtime_ns']))
  assert {'.'if p==root else str(p.relative_to(root))for p in[root,*root.rglob('*')]}==set(entries)
  for name,e in entries.items():
   p=root if name=='.'else root/name;assert metadata(p)=={k:e[k]for k in['kind','mode','mtime_ns','nlink']},(name,metadata(p),e)
  for name,e in entries.items():
   if e['kind']!='file':continue
   p=root/name;b=gzip.decompress((O/e['capture']).read_bytes());before=sum(q.lstat().st_blocks*512 for q in[O,*O.rglob('*')]);assert before+len(b)+4096<10*1024*1024;assert os.statvfs(O).f_bavail*os.statvfs(O).f_frsize-len(b)>150*1024*1024
   with p.open('wb')as f:f.write(b);f.flush();os.fsync(f.fileno())
   os.utime(p,ns=(p.stat().st_atime_ns,e['mtime_ns']));assert p.read_bytes()==b and metadata(p)=={k:e[k]for k in['kind','mode','mtime_ns','nlink']};peak=max(peak,sum(q.lstat().st_blocks*512 for q in[O,*O.rglob('*')]));restored+=1
   with p.open('wb')as f:f.truncate(0);f.flush();os.fsync(f.fileno())
   os.utime(p,ns=(p.stat().st_atime_ns,e['mtime_ns']))
  return{'inventory':str(path.relative_to(O)),'physical_incremental_files':restored,'full_zero_namespace_and_directory_metadata_exact':True,'peak_own_physical_bytes':peak,'original_inode_OR_simultaneous_all_byte_CASE_restore_NOT_claimed':True}
 finally:shutil.rmtree(root)

def verify(do_physical=False):
 inventories=sorted((O/'controls').glob('*_custody.json.gz'));assert len(inventories)>=90
 results=[]
 for p in inventories:
  j=read_inventory(p)
  if do_physical:results.append(physical(p,j))
 return{'status':'PASS','custody_inventories':len(inventories),'all_captured_bytes_hashes_sizes_and_typed_metadata_checked':True,'physical_replay_requested':do_physical,'physical_replay':results,'service_effects':0,'action_authority':False}
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--own-temporary-physical-replay',action='store_true');args=a.parse_args();r=verify(args.own_temporary_physical_replay)
 if args.own_temporary_physical_replay:(O/'PHYSICAL_CUSTODY_REPLAY_RESULTS.json').write_text(json.dumps(r,sort_keys=True,indent=2)+'\n')
 print(json.dumps({k:v for k,v in r.items()if k!='physical_replay'}))
