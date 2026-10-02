"""Read-only validation of all frozen author, review, and publication evidence."""
from pathlib import Path
import hashlib,json
p=Path(__file__).resolve().parent
names=['SOURCE_CHECKPOINT_MANIFEST.json']+[f'TURN_{k}_MANIFEST.json' for k in range(1,5)]+['FINAL_FROZEN_MANIFEST.json','review/REVIEW_MANIFEST.json','REVIEWED_MANIFEST.json']
count=0
for rel in names:
    source=p/rel;m=json.loads(source.read_text())
    for e in m['files']:
        b=(source.parent/e['path']).read_bytes()
        assert len(b)==e['bytes'],(rel,e['path'],'size')
        assert hashlib.sha256(b).hexdigest()==e['sha256'],(rel,e['path'],'hash')
        count+=1
assert hashlib.sha256((p/'FINAL_FROZEN_MANIFEST.json').read_bytes()).hexdigest()=='641216d1928d9c1066a382f6cd07efcc84151eaf1e0a1940a1c8e7535e5b6866'
state=json.loads((p/'CURRENT_STATE_REVIEWED.json').read_text())
assert state['status']=='unsolved' and state['author_turns']==5
print(json.dumps({'status':'PASS','manifest_file_checks':count,'author_turns':5,'original_status':'unsolved'},sort_keys=True))
