"""Read-only leaf closure verification, not current external package authority."""
from pathlib import Path
import hashlib,json,stat,sys
base=Path(__file__).absolute().parent
def require(ok,message):
    if not ok:raise ValueError(message)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
require(len(sys.argv)==3 and sys.argv[1]=='--manifest-sha256','literal actual closure digest required')
mf=base/'SELF_MANIFEST.json';require(digest(mf)==sys.argv[2],'actual manifest changed')
data=json.loads(mf.read_bytes());require(data['schema']=='pr50-second-adversary-self-only-closure/v1','schema')
listed=set()
for row in data['files']:
    p=base/row['path'];s=p.lstat();listed.add(row['path'])
    require(stat.S_ISREG(s.st_mode) and not p.is_symlink(),'leaf regular file')
    require(format(stat.S_IMODE(s.st_mode),'04o')==row['mode'] and s.st_size==row['bytes'] and digest(p)==row['sha256'],'whole leaf row')
require(len(listed)==len(data['files'])==data['files_count'],'unique declared count')
require({str(p.relative_to(base)) for p in base.rglob('*') if p.is_file()}==listed|{'SELF_MANIFEST.json'},'exact leaf files')
require(['.']+sorted(str(p.relative_to(base)) for p in base.rglob('*') if p.is_dir())==data['relative_directories'],'exact leaf directories')
require(stat.S_IMODE(mf.stat().st_mode)==0o444,'manifest mode')
print(json.dumps({'status':'PASS_COMPLETE_CLOSED_REVIEWER_LEAF','payload_files':len(listed),'manifest_sha256':sys.argv[2],'external_bindings_dated':True,'root_or_publication_approval':False},indent=2))
