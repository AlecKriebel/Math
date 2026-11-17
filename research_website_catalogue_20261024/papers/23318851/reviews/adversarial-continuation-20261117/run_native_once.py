"""Exactly one unmodified ordinary native driver in an isolated byte/mode-identical copy."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil
import stat
import subprocess
import sys
import time
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
A=P/'papers/23318851/reviews/adversarial-continuation-20261117'
S=P/'papers/23318851/sources/archives/02-gram_locus_support.zip.extracted'
D=A/'native-isolated'
def sha(b):return hashlib.sha256(b).hexdigest()
def snap(root):
    rows={}
    for p in [root,*sorted(root.rglob('*'))]:
        st=p.lstat();r={'mode':oct(stat.S_IMODE(st.st_mode))}
        if stat.S_ISDIR(st.st_mode):r.update(kind='directory',empty=not any(p.iterdir()))
        elif stat.S_ISREG(st.st_mode):
            b=p.read_bytes();r.update(kind='file',bytes=len(b),SHA256=sha(b))
        else:raise AssertionError('Nonregular route input '+str(p))
        rows['.' if p==root else str(p.relative_to(root))]=r
    return rows
assert not D.exists() and not (A/'NATIVE_RUN.json').exists()
source_before=snap(S)
shutil.copytree(S,D)
copy_before=snap(D)
assert source_before==copy_before
(A/'NATIVE_INPUT_BEFORE.json').write_text(json.dumps({'source':source_before,'isolated':copy_before},indent=2)+'\n')
argv=[sys.executable,'-E','-S','-B','-P',str(D/'verify_controls.py')]
start=datetime.now(timezone.utc).isoformat();timer=time.monotonic()
result=subprocess.run(argv,cwd=D,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=180)
elapsed=time.monotonic()-timer;end=datetime.now(timezone.utc).isoformat()
(A/'NATIVE.stdout.bin').write_bytes(result.stdout)
(A/'NATIVE.stderr.bin').write_bytes(result.stderr)
source_after=snap(S);copy_after=snap(D)
added=sorted(set(copy_after)-set(copy_before));removed=sorted(set(copy_before)-set(copy_after))
changed={n:{'before':v,'after':copy_after.get(n)} for n,v in copy_before.items() if v!=copy_after.get(n)}
(A/'NATIVE_INPUT_AFTER.json').write_text(json.dumps({'source':source_after,'isolated':copy_after,
    'source_exact':source_before==source_after,'added_paths':added,'removed_paths':removed,'changed_records':changed},indent=2)+'\n')
report={'start_UTC':start,'end_UTC':end,'argv':argv,'cwd':str(D),'elapsed_seconds':elapsed,
    'exit':result.returncode,'stdout_bytes':len(result.stdout),'stdout_SHA256':sha(result.stdout),
    'stderr_bytes':len(result.stderr),'stderr_SHA256':sha(result.stderr),'attempts':1,
    'repairs_retries_installs_interpreter_switches':0,'source_byte_mode_topology_exact':source_before==source_after,
    'isolated_added_paths':added,'isolated_removed_paths':removed,'isolated_changed_records':changed,
    'unmodified_driver_internal_schedule':'two baseline children then eight deliberately false variants, as fully read source',
    'internal_stream_time_limit':'Driver captures its child streams internally and exposes generated baseline JSON and rejection receipts, not literal separate child stderr/timing; no invented per-child stream/time claim',
    'scope':'Finite exact arithmetic and false-control rejection; arbitrary-polynomial theorem remains written proof'}
(A/'NATIVE_RUN.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
if result.returncode!=0 or source_before!=source_after or result.stderr:
    sys.exit(1)
assert not added and not removed
assert set(changed)<= {'verification.normal.json','verification.optimized.json','negative_controls.json'}
for n in ['verification.normal.json','verification.optimized.json']:
    assert (D/n).read_bytes()==(S/n).read_bytes(),n
old=json.loads((S/'negative_controls.json').read_text());new=json.loads((D/'negative_controls.json').read_text())
runtime={'Python_version','resolved_executable'}
assert {k:v for k,v in old.items() if k not in runtime}=={k:v for k,v in new.items() if k not in runtime}
