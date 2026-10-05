#!/usr/bin/env python3
"""Writing preservation of failed preseal source and complete outside records."""
import gzip,json,pathlib,shutil
from capture import ROOT,sha
A=ROOT.parent;D=ROOT/'forensic';D.mkdir()
files=['verify_public.py','outside_public_only.py','FINAL_REPORT.md','PUBLIC_MANIFEST.json']
pins={}
for name in files:
    b=(ROOT/name).read_bytes();(D/(name+'.failed01')).write_bytes(b);pins[name]=dict(bytes=len(b),sha256=sha(b))
external=json.loads((ROOT/'EXTERNAL_PRIVATE.json').read_bytes())
outside=A/'root_replay_private/post_merge_tests';retained=[]
for p in sorted(outside.iterdir()):
    if not p.is_file():continue
    b=p.read_bytes();row=dict(bytes=len(b),sha256=sha(b))
    if p.suffix=='.gz':
        d=gzip.decompress(b);row.update(logical_bytes=len(d),logical_sha256=sha(d))
    rel=p.relative_to(A).as_posix();external['files'][rel]=row;retained.append(rel)
(ROOT/'EXTERNAL_PRIVATE.json').write_text(json.dumps(external,indent=2)+'\n')
(D/'PRESERVATION.json').write_text(json.dumps(dict(sources=pins,complete_outside_records=retained,initial_fixture='root_replay_private/post_merge_public_only',
    local_failure="KeyError: readonly; historical field is read_only_command",public_only_failure='Missing original snapshot/QUEUE.md dependency',
    child_capture_limitation='First wrapper retained its whole failure but did not include child stderr. A separate complete read-only child rerun diagnosed missing QUEUE; no retroactive original child stderr claim.'),indent=2)+'\n')
print(json.dumps(dict(pins=pins,outside_files_retained=len(retained)),indent=2))
