#!/usr/bin/env python3
"""Select only problem20000450 from independently retrieved primary dataset."""
import hashlib
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
D=R/'evidence/primary_provenance'
body=(D/'research_results.json').read_bytes()
assert len(body)==80334822
assert hashlib.sha256(body).hexdigest()=='8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b'
data=json.loads(body)
found=[]
def select(value):
    if isinstance(value,dict):
        if str(value.get('problem_id',value.get('id','')))=='20000450':
            found.append(value);return
        for key,item in value.items():
            if str(key)=='20000450':found.append(item)
            elif isinstance(item,(dict,list)):select(item)
    elif isinstance(value,list):
        for item in value:
            if isinstance(item,(dict,list)):select(item)
select(data)
assert len(found)==1,('Target selection count',len(found))
target=found[0]
text=json.dumps(target,indent=2,ensure_ascii=False)+'\n'
(D/'problem20000450_report.json').write_text(text)
ascii_body=(json.dumps(target,indent=2,ensure_ascii=True)+'\n').encode()
(D/'problem20000450_ascii_serialization.json').write_bytes(ascii_body)
print(json.dumps(dict(status='PASS_TARGET_SELECTED',source_bytes=len(body),source_sha256=hashlib.sha256(body).hexdigest(),selected_keys=list(target) if isinstance(target,dict) else None,selected_bytes=len(text.encode()),selected_ascii_bytes=len(ascii_body),selected_ascii_sha256=hashlib.sha256(ascii_body).hexdigest(),scope='Only selected target is read; remaining80MB corpus is not manually read. Computed serialization is not a historical native retrieval.'),indent=2))
