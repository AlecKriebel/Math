import hashlib
import importlib.util
import json
from pathlib import Path
import sys
sys.dont_write_bytecode = True
case = Path(__file__).resolve().parents[3]
own = case / 'private_sources/publication_admin_helper_v3/publication_v3_software_adversary2'
p = case / 'package_update_preparation/update_package.py'
raw = p.read_bytes()
assert hashlib.sha256(raw).hexdigest() == 'e32d5a12d08f6c7331070e2a5e7368aec5c1a44f6e1e8d2bef2623df9afb8ebf'
sp = importlib.util.spec_from_file_location('review_gate', p)
g = importlib.util.module_from_spec(sp)
exec(compile(raw, str(p), 'exec'), g.__dict__)
engine = g.Engine(g.Native(), own / 'native_gate')
r = engine.gate(head='ff7a7521458c1d2d9ae6f762eac04a3c3d9b9568')
pr = json.loads((engine.evidence_dir / '0000_response.json').read_bytes())
assert pr['merged'] is False and pr['merged_at'] is None and pr['closed_at'] is None
assert len(engine.records) == 6 and all(x['method'] == 'GET' for x in engine.records)
r.update(pr=411, open=True, draft=True, merged=False, status='claimed_solved', turns='2/5', native_gets=len(engine.records))
g.durable(own / 'GATE_RESULT.json', r, exclusive=True, private=True)
print(json.dumps(r, sort_keys=True))
