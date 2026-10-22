from pathlib import Path
import argparse,datetime,hashlib,json,os,stat
R=Path(__file__).resolve().parent;SEAL=R/'MANIFEST.json';CAP=75*1024*1024
def need(v,m):
 if not v:raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def metadata(s):return {'mode':stat.S_IMODE(s.st_mode),'uid':s.st_uid,'gid':s.st_gid,'mtime_ns':s.st_mtime_ns}
def inventory():
 files={};dirs={};cache={};inodes={};allocated=0;rs=R.stat();seen={(rs.st_dev,rs.st_ino)};allocated=rs.st_blocks*512
 for parent,ds,ns in os.walk(R,followlinks=False):
  for name in ds+ns:
   p=Path(parent)/name;s=p.lstat();need(not stat.S_ISLNK(s.st_mode),'Own custody symlink');rel=p.relative_to(R).as_posix();key=s.st_dev,s.st_ino
   if key not in seen:seen.add(key);allocated+=s.st_blocks*512
   if stat.S_ISDIR(s.st_mode):dirs[rel]=metadata(s);continue
   need(stat.S_ISREG(s.st_mode),'Own custody nonregular file');inodes.setdefault(key,[]).append(p)
   if p==SEAL:continue
   fingerprint=key+(s.st_size,s.st_mtime_ns)
   if fingerprint not in cache:cache[fingerprint]=sha(p.read_bytes())
   after=p.stat();need((after.st_dev,after.st_ino,after.st_size,after.st_mtime_ns)==fingerprint,'Own custody changed during hash')
   files[rel]={**metadata(s),'bytes':s.st_size,'sha256':cache[fingerprint],'hardlink_count':s.st_nlink}
 for paths in inodes.values():need(paths[0].stat().st_nlink==len(paths),'A regular owned inode has links outside this review')
 need(allocated<=CAP,'Own review exceeds75MiB')
 return {'files':dict(sorted(files.items())),'directories':dict(sorted(dirs.items())),'root_metadata':metadata(R.stat()),'allocated_bytes':allocated}
def verify(expected=None):
 b=SEAL.read_bytes();out=json.loads(b)
 if expected is not None:need(sha(b)==expected,'External own-manifest pin differs')
 need(out['excluded_files']==['MANIFEST.json'] and out['excluded_directories']==[],'Unexpected exclusion')
 now=inventory();need(all(out[k]==v for k,v in now.items()),'Own full recursive bytes/metadata/closure changed')
 need(out['file_count']==len(now['files']) and out['directory_count']==len(now['directories']),'Own counts changed')
 return {'status':'PASS','manifest_sha256':sha(b),'manifest_bytes':len(b),'files':len(now['files']),'directories':len(now['directories']),'allocated_bytes':now['allocated_bytes'],'allocated_cap_bytes':CAP,'all_private_inputs_results_sources_and_metadata_included':True,'all_regular_hardlinks_confined_to_this_review':True,'decision':'HOLD','overall_percent':80}
def main():
 p=argparse.ArgumentParser();p.add_argument('--verify-only',action='store_true');p.add_argument('--expected-sha256');a=p.parse_args()
 if not a.verify_only:
  need(not SEAL.exists(),'Do not overwrite own final seal');now=inventory()
  out={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'schema':'independent_operations06_full_recursive_custody_v1','excluded_files':['MANIFEST.json'],'excluded_directories':[],'file_count':len(now['files']),'directory_count':len(now['directories']),'allocated_cap_bytes':CAP,'decision':'HOLD','overall_percent':80,**now}
  with SEAL.open('xb') as f:f.write((json.dumps(out,sort_keys=True,indent=2)+'\n').encode());f.flush();os.fsync(f.fileno())
  for _ in range(6):
   current=inventory()
   if all(out[k]==v for k,v in current.items()):break
   out.update(current)
   with SEAL.open('wb') as f:f.write((json.dumps(out,sort_keys=True,indent=2)+'\n').encode());f.flush();os.fsync(f.fileno())
  else:raise RuntimeError('Own seal fixed point failed')
  fd=os.open(R,os.O_RDONLY)
  try:os.fsync(fd)
  finally:os.close(fd)
 print(json.dumps(verify(a.expected_sha256),indent=2))
if __name__=='__main__':main()
