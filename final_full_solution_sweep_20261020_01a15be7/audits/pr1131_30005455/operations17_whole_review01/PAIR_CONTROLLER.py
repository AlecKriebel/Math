"""Own preparation controller; never accepts shell or provider commands."""
from pathlib import Path
import sys,traceback,json,datetime,lzma,base64,os,hashlib
ROOT=Path(__file__).resolve().parent
if sys.flags.optimize or not(sys.flags.isolated and sys.flags.no_site and sys.flags.dont_write_bytecode):raise RuntimeError('Use -I -S -B optimize0')
if len(sys.argv)!=2 or sys.argv[1]not in {'PAIR_FIDELITY17.py'}:raise RuntimeError('Fixed own suite only')
target=ROOT/sys.argv[1];ns={'__file__':str(target),'__name__':'inert_suite'}
try:exec(compile(target.read_bytes(),str(target),'exec',dont_inherit=True,optimize=0),ns)
except BaseException:
 error=traceback.format_exc();idx=1
 while(ROOT/'private'/('DEV_ABORT_'+str(idx)+'.json')).exists():idx+=1
 evidence={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'suite':target.name,'traceback':error,'actual_effects':0}
 dest=ns.get('DEST')
 if dest is not None and dest.exists():
  for q in dest.iterdir():
   if q.is_dir()and not(dest/(q.name+'.json')).exists():(dest/(q.name+'.json')).write_text(json.dumps({'case':q.name,'status':'UNEXPECTED_ABORT','traceback':error},indent=2)+'\n')
  try:
   if ns.get('archive_completed'):ns['archive_completed']()
  except BaseException:
   evidence['archive_failure']=traceback.format_exc()
   raw=json.dumps({'paths':ns.get('MEMORY_PATHS',{}),'bodies_base64':{k:base64.b64encode(v).decode()for k,v in ns.get('MEMORY_BODIES',{}).items()},'directories':list(ns.get('VIRTUAL_DIRECTORIES',set()))},sort_keys=True).encode();packed=lzma.compress(raw)
   if ns.get('allocated',lambda:0)()+len(packed)+65536<8*1024*1024 and os.statvfs(ROOT).f_bavail*os.statvfs(ROOT).f_frsize>=150*1024*1024+len(packed)+65536:
    p=ROOT/'private'/('DEV_ABORT_'+str(idx)+'_VFS.xz')
    with p.open('xb')as h:h.write(packed);h.flush();os.fsync(h.fileno())
    evidence['emergency_VFS']={'path':str(p),'bytes':len(packed),'sha256':hashlib.sha256(packed).hexdigest()}
   else:evidence['emergency_VFS_not_saved_due_bound']=True
 (ROOT/'private'/('DEV_ABORT_'+str(idx)+'.json')).write_text(json.dumps(evidence,indent=2)+'\n')
 raise
