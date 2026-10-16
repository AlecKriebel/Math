"""Verify this audit's public artifacts and retained successful/failing receipts."""
from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent
M=json.loads((P/'MANIFEST.json').read_text())
n=0
for item in M['files']:
    b=(P/item['path']).read_bytes()
    assert len(b)==item['bytes'],item['path']
    assert hashlib.sha256(b).hexdigest()==item['sha256'],item['path']
    n+=1
x=json.loads((P/'independent_symbolic_stdout.json').read_text())
assert (x['assertions'],x['hessian_positive'],x['hessian_nullity'])==(8662,65,63)
assert hashlib.sha256((P/'independent_full_hessian.txt').read_bytes()).hexdigest()==x['full_hessian_sha256']
a=json.loads((P/'author_replay_with_sources_stdout.json').read_text())
assert(a['author_assertions'],a['manifest_entries_verified'],a['primary_source_files_verified'])==(102005,157,3)
for name in ['first','second','third']:
    code=(P/f'independent_symbolic_{name}_failure.py').read_bytes()
    want=(P/f'independent_symbolic_{name}_failure_script.sha256').read_text().split()[0]
    assert hashlib.sha256(code).hexdigest()==want
    assert 'AssertionError:' in (P/f'independent_symbolic_{name}_failure.txt').read_text()
for item in M['successful_stderr_files']:assert (P/item).read_bytes()==b''
print(json.dumps({'status':'PASS','public_files_bound':n,'independent_assertions':8662,'author_assertions':102005,'sources_verified':3,'failures_preserved':3,'scope':'Scoped holonomy/Hessian family audit only; unrestricted optimal flux remains unresolved.'},indent=2,sort_keys=True))
