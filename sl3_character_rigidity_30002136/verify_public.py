"""Verify the sanitized public projection's exact file bindings."""
import hashlib,json,pathlib
p=pathlib.Path(__file__).resolve().parent
m=json.loads((p/'PUBLIC_MANIFEST.json').read_text())
for name,want in m['files'].items():
    q=p/name
    assert q.is_file() and hashlib.sha256(q.read_bytes()).hexdigest()==want,name
print(json.dumps({'status':'PASS','files':len(m['files']),'full_resolution':False},indent=2))
