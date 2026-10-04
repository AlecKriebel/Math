"""Preserve unexpectedly generated UNTRACKED CLI documentation in this effort."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,stat,subprocess
A=Path(__file__).resolve().parent;R=A.parents[2];D=A/'gws_generated_private_03';D.mkdir(exist_ok=False)
sha=lambda b:hashlib.sha256(b).hexdigest()
def git(*args):return subprocess.check_output(['/usr/bin/git',*args],cwd=R)
assert not git('ls-files','--','skills','docs/skills.md')
assert not git('diff','--name-only','--','skills','docs')
sources=[p for p in (R/'skills').rglob('*') if p.is_file()]+[R/'docs/skills.md']
assert len(sources)==96
inventory=[]
for p in sources:
 st=p.stat();b=p.read_bytes();assert not p.is_symlink() and 1791135409 <= st.st_mtime <1791135412
 inventory.append(dict(path=str(p.relative_to(R)),bytes=len(b),sha256=sha(b),mode=oct(stat.S_IMODE(st.st_mode)),mtime_ns=st.st_mtime_ns))
(D/'docs').mkdir();(R/'skills').rename(D/'skills');(R/'docs/skills.md').rename(D/'docs/skills.md')
for row in inventory:
 p=D/row['path'];assert p.stat().st_size==row['bytes'] and sha(p.read_bytes())==row['sha256']
 assert oct(stat.S_IMODE(p.stat().st_mode))==row['mode']
assert not git('diff','--name-only','--','skills','docs')
j=dict(actual_utc=datetime.now(timezone.utc).isoformat(),status='PASS_GENERATED_UNTRACKED_DOCUMENTATION_ISOLATED_WITHOUT_TRACKED_CHANGES',
 observation='gws generate-skills --help unexpectedly generated95skills anddocs/skills.md in repo root; its help flag did not prevent generation.',
 original_command_timing='Tool transcript and measured file mtimes retained; no reconstructed exact command timestamp.',
 moved_files=len(inventory),all_bodies_and_modes_preserved=True,tracked_docs_and_index_untouched=True,
 shared_git_hold_retained=True,inventory=inventory)
(D/'ISOLATION_RECEIPT.json').write_text(json.dumps(j,indent=2)+'\n')
print(json.dumps({k:v for k,v in j.items() if k!='inventory'},indent=2))
