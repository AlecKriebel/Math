"""Read-only original-source and frozen INITIAL finite namespace guard."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import stat
import sys

LANE = Path(__file__).resolve().parent
PAPER = LANE.parents[1]
TARGETS = {"sources": PAPER / "sources", "initial": PAPER / "reviews/scope-sol"}

def records(root):
    out=[]
    for p in [root,*sorted(root.rglob('*'))]:
        st=p.lstat()
        e={"path": str(p.relative_to(root)) if p!=root else ".", "mode":oct(stat.S_IMODE(st.st_mode))}
        if stat.S_ISDIR(st.st_mode): e.update(kind="directory",empty=not any(p.iterdir()))
        elif stat.S_ISREG(st.st_mode):
            data=p.read_bytes();e.update(kind="file",bytes=len(data),sha256=hashlib.sha256(data).hexdigest())
        else: raise ValueError(str(p))
        out.append(e)
    return out

initial=TARGETS['initial']
for name,expected in {
    'INITIAL_MANIFEST.json':'ccc2d42694ab76d834624bb9a60edeeb79a6060a330a3f141e98a109a6d8fc19',
    'INITIAL_SEAL.json':'658f4d17a204ab3ba16d960dbe00ac397d99cc5d555ce2ba4187f657f0bb9631',
}.items(): assert hashlib.sha256((initial/name).read_bytes()).hexdigest()==expected
actual={label:records(path) for label,path in TARGETS.items()}
baseline=LANE/'INPUT_GUARD_BEFORE.json'
mode=sys.argv[1]
if mode=='before':
    assert not baseline.exists()
else:
    expected=json.loads(baseline.read_text())['namespaces']
    assert actual==expected,'Original source or frozen INITIAL changed'
result={"utc":datetime.now(timezone.utc).isoformat(),"mode":mode,"all_exact":True,
        "namespaces":actual,"source_file_count":sum(e['kind']=='file' for e in actual['sources']),
        "initial_file_count":sum(e['kind']=='file' for e in actual['initial'])}
target=baseline if mode=='before' else LANE/f'INPUT_GUARD_{mode.upper()}.json'
assert not target.exists()
target.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='namespaces'}))
