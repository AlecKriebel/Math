"""Make private byte-identical copies of the two text-read historical helpers."""
from pathlib import Path
import hashlib
import json

F=Path(__file__).resolve().parent
pairs=[('verify.py','author/verify.py'),
       ('independent_review/independent_checks.py','historical_independent/independent_checks.py')]
rows=[]
for src,dst in pairs:
    a=F/'source_snapshot'/src;b=F/'private_replays'/dst
    b.parent.mkdir(parents=True,exist_ok=True)
    with b.open('xb') as t:t.write(a.read_bytes())
    b.chmod(0o644)
    assert a.read_bytes()==b.read_bytes()
    rows.append({'original':str(a),'private_copy':str(b),
                 'bytes':b.stat().st_size,'sha256':hashlib.sha256(b.read_bytes()).hexdigest(),
                 'text_read_before_execution':True,
                 'authority':'Historical finite diagnostic replay, not fresh independent mathematical acceptance'})
print(json.dumps({'schema':'pr51-private-literal-helper-copies/v1','copies':rows},indent=2))
