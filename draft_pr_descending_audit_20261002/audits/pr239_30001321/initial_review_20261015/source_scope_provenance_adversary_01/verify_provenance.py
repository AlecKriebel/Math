"""Recheck all frozen packet and manifest links. Optional PDF fetches are held in memory."""
from pathlib import Path
import hashlib,json,sys,urllib.request
ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent;PACKET=BASE/'submitted/unsolved_math_prioritization/attempts/30001321'
intake=json.loads((BASE/'INTAKE.json').read_text());checks=[]
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
for entry in intake['original_source_files']:
    rel=entry['native_path'].split('/30001321/',1)[1];data=(PACKET/rel).read_bytes()
    checks.append(len(data)==entry['bytes'] and hashlib.sha256(data).hexdigest()==entry['sha256'] and hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==entry['native_blob'])
assert len(checks)==32 and all(checks)
assert sum(f.is_file() for f in PACKET.rglob('*'))==32
nested=0
for rel in ['TURN_1_MANIFEST.json','TURN_2_MANIFEST.json','FROZEN_MANIFEST.json','independent_review/REVIEW_MANIFEST.json']:
    manifest=PACKET/rel;j=json.loads(manifest.read_text())
    for entry in j['files']:
        path=manifest.parent/entry['path'];assert len(path.read_bytes())==entry['bytes'] and digest(path)==entry['sha256'];nested+=1
reviewed=json.loads((PACKET/'independent_review/reviewed_hashes.json').read_text())
for entry in reviewed['author_files']:
    path=PACKET/entry['path'];assert len(path.read_bytes())==entry['bytes'] and digest(path)==entry['sha256']
turn1=digest(PACKET/'TURN_1_MANIFEST.json')
assert json.loads((PACKET/'TURN_2_MANIFEST.json').read_text())['earlier_manifest_sha256']==turn1
assert json.loads((PACKET/'BUDGET_TURN2.json').read_text())['prior_frozen_turn1_manifest_sha256']==turn1
review=json.loads((PACKET/'independent_review/REVIEW_MANIFEST.json').read_text())
assert review['reviewed_proof_sha256']==digest(PACKET/'PROOF.md')
assert review['reviewed_manifest_sha256']==reviewed['author_manifest_sha256']==digest(PACKET/'FROZEN_MANIFEST.json')
assert len(reviewed['author_files'])==24
sources=reviewed['primary_pdfs'];assert len(sources)==4
original_sources=json.loads((PACKET/'source_manifest.json').read_text())['sources']
assert all(x['url']==y['url'] and x['sha256']==y['sha256'] for x,y in zip(original_sources,sources[:3]))
assert sources[3]['sha256'] in (PACKET/'SOURCE_ADDENDUM_TURN3.md').read_text()
assert sources[3]['url'] in (PACKET/'SOURCE_ADDENDUM_TURN3.md').read_text()
if '--fetch-sources' in sys.argv:
    for entry in sources:
        with urllib.request.urlopen(entry['url'],timeout=60) as response:data=response.read()
        assert data.startswith(b'%PDF') and hashlib.sha256(data).hexdigest()==entry['sha256']
        print('authenticated',entry['file'],len(data),entry['sha256'])
print(json.dumps({'status':'PASS','native_files':32,'nested_manifest_entries':nested,'old_reviewed_author_files':24,'primary_source_pin_crosslinks':4,'fetched_source_objects':4 if '--fetch-sources' in sys.argv else 0},sort_keys=True))
