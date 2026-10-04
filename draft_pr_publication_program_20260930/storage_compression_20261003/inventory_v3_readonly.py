#!/usr/bin/python3
"""Read only the eight named completed private copies; write no input files."""
import base64, datetime, hashlib, json, os, stat, subprocess, sys
from pathlib import Path
P = Path('/Users/alec/Documents/Math/draft_pr_publication_program_20260930')
R39 = 'audits/pr39_9500008/tmp/root_pr39_actual_x_hc1nyr/unsolved_math_prioritization/cache/'
R38 = 'audits/pr38_2765/tmp/root_pr38_actual_f4mchuie/unsolved_math_prioritization/cache/'
CANDIDATES = {'pr39-catalog': R39+'catalog.sqlite', 'pr38-catalog': R38+'catalog.sqlite',
 'pr33-catalog': 'audits/pr33_10000046/tmp/root_new_whole/replica/unsolved_math_prioritization/cache/catalog.sqlite',
 'pr39-problems': R39+'problems.json', 'pr39-results': R39+'research_results.json',
 'pr38-problems': R38+'problems.json', 'pr38-results': R38+'research_results.json',
 'pr41-typed': 'audits/pr41_9700035/acceptance_static_adversary_family/COMPLETE_TYPED_NODES.jsonl'}
FIELDS = ('st_dev','st_ino','st_mode','st_nlink','st_uid','st_gid','st_size','st_rdev',
 'st_atime_ns','st_mtime_ns','st_ctime_ns','st_flags','st_blocks','st_blksize','st_birthtime')
def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def stats(path): return {k:getattr(os.lstat(path),k) for k in FIELDS}
def stable(s): return {k:v for k,v in s.items() if k != 'st_atime_ns'}
record = {'role':'READONLY_INVENTORY_NOT_COMPRESSION', 'pid':os.getpid(), 'argv':sys.argv,
 'executable':sys.executable,'flags':repr(sys.flags),'cwd':os.getcwd(),'start_utc':utc(),'candidates':{},'commands':[]}
def command(argv, accepted=(0,)):
    start=utc(); child=subprocess.Popen(argv,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err=child.communicate()
    record['commands'].append({'argv':argv,'pid':child.pid,'start_utc':start,'end_utc':utc(),
      'exit':child.returncode,'stdout_base64':base64.b64encode(out).decode(),'stderr_base64':base64.b64encode(err).decode()})
    if child.returncode not in accepted: raise RuntimeError('native readonly metadata command failed')
    return out
for key, rel in CANDIDATES.items():
    path=P/rel; item={'path':str(path)}; record['candidates'][key]=item
    if not path.exists(): item['status']='MISSING'; continue
    if any(q.is_symlink() for q in (path,)+tuple(path.parents)): item['status']='SYMLINK_SKIP'; continue
    before=stats(path); item['pre_read_stat']=before
    if not stat.S_ISREG(before['st_mode']) or before['st_nlink']!=1: item['status']='TYPE_OR_LINK_SKIP'; continue
    if before['st_flags'] & stat.UF_COMPRESSED: item['status']='ALREADY_COMPRESSED_SKIP'; continue
    h=hashlib.sha256()
    with os.fdopen(os.open(path,os.O_RDONLY|os.O_NOFOLLOW),'rb') as stream:
        for chunk in iter(lambda:stream.read(1048576),b''): h.update(chunk)
    names_raw=command(['/usr/bin/xattr',str(path)])
    if len(names_raw)>16384: raise RuntimeError('xattr names exceed bound')
    names=names_raw.decode('utf-8').splitlines(); attrs={}
    if len(names)>64 or len(names)!=len(set(names)): raise RuntimeError('invalid xattr inventory')
    for name in names:
        out=command(['/usr/bin/xattr','-px',name,str(path)])
        if len(out)>262144: raise RuntimeError('original xattr output exceeds bound')
        value=bytes.fromhex(out.decode('ascii'))
        if len(value)>65536: raise RuntimeError('original xattr value exceeds bound')
        attrs[name]=base64.b64encode(value).decode()
    acl=command(['/bin/ls','-lde',str(path)]).splitlines()[1:]
    after=stats(path)
    item.update(status='ELIGIBLE_STABLE' if stable(before)==stable(after) else 'CHANGED_SKIP',stat=after,
      sha256=h.hexdigest(),mode_07777=oct(stat.S_IMODE(after['st_mode'])),allocated_bytes=after['st_blocks']*512,
      xattrs=attrs,acl_base64=[base64.b64encode(line).decode() for line in acl])
record['pr41_lsof_stdout']=base64.b64encode(command(['/usr/sbin/lsof','-Fpcfatn',str(P/CANDIDATES['pr41-typed'])],(0,1))).decode()
record['end_utc']=utc()
print(json.dumps(record,indent=2,sort_keys=True))
