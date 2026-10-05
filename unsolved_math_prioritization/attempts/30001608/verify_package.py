"""Verify frozen mathematical and review evidence without modifying files."""
from pathlib import Path
import hashlib,json
p=Path(__file__).resolve().parent
checks=0
for rel in ['TURN_1_MANIFEST.json','TURN_2_MANIFEST.json','TURN_3_MANIFEST.json','TURN_4_MANIFEST.json','review/REVIEW_MANIFEST.json','ACCEPTED_MANIFEST.json']:
    source=p/rel
    m=json.loads(source.read_text())
    root=source.parent
    if m.get('previous_manifest'):
        b=(root/m['previous_manifest']).read_bytes()
        assert hashlib.sha256(b).hexdigest()==m['previous_manifest_sha256'],rel
        checks+=1
    for e in m['files']:
        b=(root/e['path']).read_bytes()
        assert len(b)==e['bytes'],(rel,e['path'],'size')
        assert hashlib.sha256(b).hexdigest()==e['sha256'],(rel,e['path'],'hash')
        checks+=1
original=(p/'review/independent_check.py').read_text()
old="Path('/workspace/scratch/c7d6ade09fc0/research_30001608/TURN_4.md')"
new="(Path(__file__).resolve().parents[1] / 'TURN_4.md')"
assert original.count(old)==1
assert original.replace(old,new)==(p/'checks/independent_review_portable.py').read_text()
checks+=1
state=json.loads((p/'CURRENT_STATE_ACCEPTED.json').read_text())
assert state['author_turns_consumed']==4 and state['budget']==5
assert state['status']=='claimed_solved'
checks+=1
print(json.dumps({'status':'PASS','evidence_checks':checks,'author_turns':4,'scope':'Frozen bytes, manifest chains, and exact one-path portability adaptation'},sort_keys=True))
