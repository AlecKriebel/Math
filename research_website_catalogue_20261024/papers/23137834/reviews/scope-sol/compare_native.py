#!/usr/bin/env python3
"""One data-only exact comparison after the single native run; writes nothing."""
from pathlib import Path
import re
import hashlib
import json

root=Path(__file__).resolve().parent
expected=root/'../../sources/published-source/container-001/tree/expected/geometry.txt'
raw=(root/'native-run/stdout.txt').read_bytes()
text=raw.decode('utf-8')
stamp=r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?\+00:00'
lines=[]
for line in text.splitlines():
    if re.fullmatch(r'native_utc(?:_start|_end)? '+stamp,line):
        continue
    lines.append(re.sub(r' native_utc '+stamp+r'$','',line))
normalized=('\n'.join(lines)+'\n').encode()
assert normalized==expected.read_bytes(),'Complete mathematical text differs'
assert (root/'native-run/exit.txt').read_bytes()==b'0\n','Actual native exit'
assert (root/'native-run/stderr.txt').read_bytes()==b'','Actual native stderr'
assert (root/'native-run/SOURCES.before.sha256').read_bytes()==(root/'native-run/SOURCES.after.sha256').read_bytes(),'All source bytes'
assert (root/'native-run/SOURCES.before.topology').read_bytes()==(root/'native-run/SOURCES.after.topology').read_bytes(),'All source modes/topology'
print(json.dumps({'status':'PASS_SINGLE_NATIVE_EXACT_TEXT_AND_SOURCE_PRESERVATION','raw_stdout_bytes':len(raw),'normalized_bytes':len(normalized),'normalized_SHA256':hashlib.sha256(normalized).hexdigest(),'only_declared_UTC_metadata_removed':True,'native_routes':1,'writes_by_comparator':0},sort_keys=True))
