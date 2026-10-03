"""Optional ROOT-only leaf closure; never supplies acceptance/publication authority."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,stat,sys

base=Path(__file__).absolute().parent
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def require(ok,message):
    if not ok:raise ValueError(message)
require(len(sys.argv)==3 and sys.argv[1]=='--expected-report-sha256','literal expected report binding required')
require(digest(base/'REPORT.md')==sys.argv[2],'report changed before ROOT closure')
require(not (base/'SELF_MANIFEST.json').exists(),'already closed')
bindings=json.loads((base/'REVIEWED_PACKAGE_BINDINGS.json').read_bytes())
require(bindings['files_count']==19 and len(bindings['files'])==19,'whole package binding count')
for row in bindings['files']:
    p=Path(row['path']);s=p.lstat()
    require(stat.S_ISREG(s.st_mode) and not p.is_symlink(),'external regular file')
    require(format(stat.S_IMODE(s.st_mode),'04o')==row['mode'] and s.st_size==row['bytes'] and digest(p)==row['sha256'],'dated reviewed package changed before leaf closure')
verdict=json.loads((base/'VERDICT.json').read_bytes())
require(verdict['mandatory_issues']==[] and verdict['root_approval_supplied'] is False and verdict['publication_approval_supplied'] is False,'review scope/status')
for folder,source in [('independent_math_run',base/'independent_checks.py'),('author_checker_reproduction',base.parent/'preprint_v1/verify_even_calculus.py'),('fresh_crossref_source_access',base/'read_crossref_metadata.py')]:
    d=base/folder;cap=json.loads((d/'CAPTURE.json').read_bytes());pre=json.loads((d/'PRELAUNCH.json').read_bytes())
    require(cap['actual_execution'] is True and cap['completed'] is True and type(cap['exit_code']) is int and cap['exit_code']==0,'actual completed private child')
    require(cap['argv']==pre['argv'] and cap['operator_pid']==pre['operator_pid'] and type(cap['child_pid']) is int and cap['child_pid']>0,'whole actual private identity')
    start=datetime.fromisoformat(cap['started_utc']);finish=datetime.fromisoformat(cap['finished_utc'])
    require(start.utcoffset() is not None and finish.utcoffset() is not None and start<=finish,'aware enclosing interval')
    require(source.read_bytes()==(d/'prelaunch_source.py').read_bytes() and (base/'capture_private.py').read_bytes()==(d/'prelaunch_operator.py').read_bytes(),'whole prelaunch bodies')
    for name in ('stdout','stderr'):
        p=d/(name+'.bin');require(p.stat().st_size==cap[name]['bytes'] and digest(p)==cap[name]['sha256'],'complete private stream')
files=[]
for p in sorted(base.rglob('*')):
    require(not p.is_symlink(),'no leaf symlink')
    if p.is_file():
        require(stat.S_ISREG(p.lstat().st_mode),'leaf regular file');p.chmod(0o444)
        files.append({'path':str(p.relative_to(base)),'mode':'0444','bytes':p.stat().st_size,'sha256':digest(p)})
record={'schema':'pr50-second-adversary-self-only-closure/v1','closed_utc':datetime.now(timezone.utc).isoformat(),'self_excluded':'SELF_MANIFEST.json','files_count':len(files),'files':files,'relative_directories':['.']+sorted(str(p.relative_to(base)) for p in base.rglob('*') if p.is_dir()),'scope':'Self-only reviewer leaf, with dated external package bindings; no native/publication authority'}
(base/'SELF_MANIFEST.json').write_text(json.dumps(record,indent=2)+'\n');(base/'SELF_MANIFEST.json').chmod(0o444)
print(json.dumps({'status':'CLOSED_SELF_ONLY_REVIEWER_LEAF','payload_files':len(files),'manifest_sha256':digest(base/'SELF_MANIFEST.json'),'root_or_publication_approval':False},indent=2))
