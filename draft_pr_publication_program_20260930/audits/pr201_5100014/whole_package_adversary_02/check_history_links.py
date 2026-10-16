from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
P=Path(__file__).resolve().parent.parent/'publication_package_v2/materials'
def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def need(c,m):
    if not c:raise RuntimeError(m)
rows=[]
for rel in ['audit/ROOT_MATHEMATICAL_GATE_01.json','audit/ROOT_PRIORITY_AND_EDITORIAL_GATE_01.json']:
    j=json.loads((P/rel).read_text());safe=j['safe_files'];need(rel.removeprefix('audit/') not in safe,'gate excluded itself')
    for target,pn in safe.items():
        q=P/'audit'/target
        need(q.is_file() and pin(q.read_bytes())==pn,'gate safe pin '+target)
    rows.append({'gate':rel,'safe_files_revalidated':len(safe)})
pr=json.loads((P/'verification/PORTABILITY_PROVENANCE.json').read_text());prows=[]
for r in pr:
    a=(P/'audit'/r['source']).read_bytes();b=(P/r['portable']).read_bytes();e=(P/'audit'/r['expected_result_source']).read_bytes()
    need(pin(a)==r['source_pin'] and pin(b)==r['portable_pin'] and pin(e)==r['expected_result_pin'],'portable source/expected pins '+r['source'])
    # Remove each listed path insertion independently; no other edits permitted.
    reduced=a.decode()
    for line in r['removed_lines']:
        need(reduced.count(line)==1,'unique removed line');reduced=reduced.replace(line,'')
    need(reduced.encode()==b,'only disclosed portable edits '+r['source'])
    prows.append({'source':r['source'],'portable':r['portable'],'exact_disclosed_delta':True,'all_pins':True})
print(json.dumps({'UTC':datetime.now(timezone.utc).isoformat(),'status':'PASS','gates':rows,'portable_scripts':prows},indent=2))
