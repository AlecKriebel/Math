"""Close only this owned preparation packet; never overwrite an existing seal."""
from pathlib import Path
import datetime,hashlib,json,os,stat
ROOT=Path(__file__).resolve().parent
def need(v,m):
    if not v:raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def inventory():
    entries={};inodes={};allocated=0
    for p in [ROOT,*sorted(ROOT.rglob('*'))]:
        if p==ROOT/'MANIFEST.json':continue
        st=p.lstat();need(not p.is_symlink(),'Unexpected symlink')
        name='.' if p==ROOT else p.relative_to(ROOT).as_posix()
        record={'kind':'directory' if p.is_dir()else 'file','mode':stat.S_IMODE(st.st_mode),'mtime_ns':st.st_mtime_ns}
        if record['kind']=='file':
            need(stat.S_ISREG(st.st_mode),'Nonregular evidence');b=p.read_bytes();record.update(bytes=len(b),sha256=sha(b))
            inodes.setdefault((st.st_dev,st.st_ino),[]).append(name)
        key=(st.st_dev,st.st_ino)
        if key not in seen:allocated+=st.st_blocks*512;seen.add(key)
        entries[name]=record
    return entries,[v for v in inodes.values()if len(v)>1],allocated
need(not(ROOT/'MANIFEST.json').exists(),'Existing seal: no retry/overwrite')
need(not(ROOT/'runtime').exists(),'Production runtime must not exist')
seen=set();entries,links,allocated=inventory()
need(allocated<10*1024*1024,'Incremental footprint cap')
free=os.statvfs(ROOT).f_bavail*os.statvfs(ROOT).f_frsize;need(free>=150*1024*1024,'Actual free reserve')
out={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_manifest_sha256':sha((ROOT/'source/SOURCE_MANIFEST.json').read_bytes()),'bootstrap_sha256':sha((ROOT/'source/bootstrap17.py').read_bytes()),'files':sum(v['kind']=='file'for v in entries.values()),'directories':sum(v['kind']=='directory'for v in entries.values()),'entries':entries,'hardlink_groups':links,'allocated_before_seal_bytes':allocated,'actual_free_before_seal_bytes':free,'publication_ready':False,'root_action_accepted':False,'complete_recursive_byte_mode_nsmtime_closure':True,'actual_service_or_Git_mutations':0,'exclusions':['MANIFEST.json']}
body=(json.dumps(out,sort_keys=True,indent=2)+'\n').encode()
need(allocated+len(body)+16384<10*1024*1024,'Preflight final seal cap')
need(free>=150*1024*1024+len(body)+16384,'Preflight final seal reserve')
with (ROOT/'MANIFEST.json').open('xb')as h:h.write(body);h.flush();os.fsync(h.fileno())
rootpin=entries['.'];os.chmod(ROOT,rootpin['mode']);os.utime(ROOT,ns=(rootpin['mtime_ns'],rootpin['mtime_ns']))
fd=os.open(ROOT,os.O_RDONLY)
try:os.fsync(fd)
finally:os.close(fd)
need((ROOT/'MANIFEST.json').read_bytes()==body,'Outer seal readback')
seen=set();again,againlinks,after=inventory()
need(again==entries and againlinks==links,'Complete recursive byte/mode/nsmtime/closure readback changed')
need(after+(ROOT/'MANIFEST.json').stat().st_blocks*512<10*1024*1024,'Final allocated cap')
print(json.dumps({'seal_sha256':sha(body),'files':out['files'],'directories':out['directories'],'allocated_bytes_including_seal':after+(ROOT/'MANIFEST.json').stat().st_blocks*512,'actual_free_after_seal_bytes':os.statvfs(ROOT).f_bavail*os.statvfs(ROOT).f_frsize,'complete_recursive_readback':'PASS','publication_ready':False},indent=2))
