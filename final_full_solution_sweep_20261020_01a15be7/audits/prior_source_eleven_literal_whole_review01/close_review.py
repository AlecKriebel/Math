"""Close only this review directory, preserving all prior inputs untouched."""
import datetime,hashlib,json,os,pathlib,stat
O=pathlib.Path(__file__).resolve().parent
assert O.name=='prior_source_eleven_literal_whole_review01'
def inventory():
 out={}
 for p in [O,*sorted(O.rglob('*'))]:
  n='.'if p==O else p.relative_to(O).as_posix()
  if n=='CLOSED_MANIFEST.json':continue
  s=p.lstat();assert stat.S_ISREG(s.st_mode)or stat.S_ISDIR(s.st_mode)
  v={'kind':'file'if p.is_file()else'directory','mode':stat.S_IMODE(s.st_mode),'mtime_ns':s.st_mtime_ns,'nlink':s.st_nlink}
  if p.is_file():v.update(bytes=s.st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest())
  out[n]=v
 return out
free=os.statvfs(O);free=free.f_bavail*free.f_frsize
used=sum(p.lstat().st_blocks*512 for p in[O,*O.rglob('*')]);assert used<7*1024*1024 and free>=151*1024*1024
(O/'RESOURCE_AT_CLOSURE.json').write_text(json.dumps({'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'own_physical_before_manifest':used,'free_bytes':free,'own_limit':8*1024*1024,'free_reserve':150*1024*1024,'large_duplicate_bodies_saved':0},indent=2)+'\n')
mp=O/'CLOSED_MANIFEST.json';f=mp.open('xb')
for p in O.rglob('*'):
 if p.is_file():p.chmod(0o444)
for p in sorted([O,*[p for p in O.rglob('*')if p.is_dir()]],key=lambda x:len(x.parts),reverse=True):p.chmod(0o555)
m={'schema':'prior-source-eleven-literal-whole-review-v1','closed_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'self_excluded_exact':'CLOSED_MANIFEST.json','reserved_before_inventory':True,'entries':inventory(),'execution_ready':False,'new_publications':0,'service_writes':0,'Git_index_writes':0}
raw=(json.dumps(m,ensure_ascii=False,indent=2)+'\n').encode();f.write(raw);f.flush();os.fsync(f.fileno());f.close()
print(json.dumps({'manifest_sha256':hashlib.sha256(raw).hexdigest(),'verifier_sha256':hashlib.sha256((O/'verify_readonly.py').read_bytes()).hexdigest(),'report_sha256':hashlib.sha256((O/'REPORT.md').read_bytes()).hexdigest(),'payload_files':sum(v['kind']=='file'for v in m['entries'].values()),'read_only_modes':True},sort_keys=True))
