import hashlib,json,os,stat,subprocess
from pathlib import Path
from datetime import datetime,timezone
A=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
HEAD='7d3adb0e500b0414a49a449e7981d34ade329427'
PREFIX='unsolved_math_prioritization/attempts/6000001/'
snapshot=json.loads((A/'ORIGINAL_SNAPSHOT.json').read_text())['files']
def require(ok,msg):
 if not ok: raise RuntimeError(msg)
def sha(b): return hashlib.sha256(b).hexdigest()
def git(*args): return subprocess.check_output(['git',*args])
rows=git('ls-tree','-rz',HEAD,PREFIX).split(b'\0')
entries={}
for row in rows:
 if not row: continue
 meta,path=row.split(b'\t'); mode,typ,oid=meta.decode().split(); entries[path.decode()]=(mode,typ,oid)
require(set(entries)==set(snapshot),'Git/snapshot inventory mismatch')
original=A/'original'
actual={str(p.relative_to(original)) for p in original.rglob('*') if not p.is_dir()}
require(actual==set(snapshot),'Disk/snapshot inventory mismatch')
receipts=[]
for path,expected in snapshot.items():
 mode,typ,oid=entries[path]; disk=original/path; st=disk.lstat()
 require(mode=='100644' and typ=='blob' and stat.S_ISREG(st.st_mode) and not disk.is_symlink(), 'Unsafe mode '+path)
 raw=git('cat-file','blob',oid); d=disk.read_bytes()
 require(raw==d and sha(raw)==expected,'Git/disk/hash mismatch '+path)
 receipts.append(dict(path=path,bytes=len(raw),sha256=sha(raw),git_mode=mode,disk_mode=oct(stat.S_IMODE(st.st_mode)),git_oid=oid))
root=original/PREFIX
manifests=[]
for mf in sorted(root.rglob('*MANIFEST.json')):
 m=json.loads(mf.read_text()); rows=m['files']; rows=rows if isinstance(rows,list) else [dict(path=n,**r) for n,r in rows.items()]
 expected={r['path'] for r in rows}|{mf.name}; localactual={str(p.relative_to(mf.parent)) for p in mf.parent.rglob('*') if p.is_file()}
 require(expected==localactual,'Nested closed inventory mismatch '+str(mf))
 for row in rows:
  raw=(mf.parent/row['path']).read_bytes()
  require(len(raw)==row['bytes'] and sha(raw)==row['sha256'],'Nested byte/hash mismatch')
 manifests.append(dict(path=str(mf.relative_to(root)),files=len(rows),sha256=sha(mf.read_bytes()),closed_inventory=True))
state=json.loads(git('show',HEAD+':unsolved_math_prioritization/state.json'))
# Native target selection only; do not publish unrelated records.
entry=state.get('problems',state).get('6000001') if isinstance(state,dict) else None
if entry is None:
 entry={k:v for k,v in state.items() if k=='6000001'}
history=[]
for line in git('show',HEAD+':unsolved_math_prioritization/history.jsonl').splitlines():
 r=json.loads(line)
 if str(r.get('id',r.get('problem_id','')))=='6000001':history.append(r)
queue=[l for l in git('show',HEAD+':unsolved_math_prioritization/QUEUE.md').decode().splitlines() if '| 6000001 /' in l]
directories=[]
for directory in sorted(original.rglob('*')):
 if directory.is_dir():
  require(not directory.is_symlink() and stat.S_ISDIR(directory.lstat().st_mode),'Linked directory')
  directories.append(dict(path=str(directory.relative_to(original)),disk_mode=oct(stat.S_IMODE(directory.lstat().st_mode))))
result=dict(native_state_present='6000001' in state,native_history_target_count=len(history),directories=directories,utc=datetime.now(timezone.utc).isoformat(),status='PASS',head=HEAD,files=len(receipts),python_files=sum(r['path'].endswith('.py') for r in receipts),file_receipts=receipts,nested_manifests=manifests,native_state=entry,native_history=history,immutable_queue_row=queue,proof_budget_increment=0,limitation='Authentication and target-only native provenance; no proof of history beyond checked native records.')
(OUT/'evidence/AUTHENTICATION.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['file_receipts','native_state','native_history']},indent=2))
print(json.dumps(dict(native_state=entry,native_history=history),indent=2))
