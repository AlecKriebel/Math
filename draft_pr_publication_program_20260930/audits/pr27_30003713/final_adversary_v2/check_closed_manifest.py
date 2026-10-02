"""Check the self-excluding v2 first-party manifest without changing files."""
from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parent;M=P/'FIRST_PARTY_SHA256_MANIFEST.json';d=json.loads(M.read_text());excluded={'ignoredtmp','__pycache__'}
actual={p.relative_to(P).as_posix() for p in P.rglob('*') if p.is_file() and p!=M and not (set(p.relative_to(P).parts)&excluded)}
assert actual=={x['path'] for x in d['files']}
for x in d['files']:
 b=(P/x['path']).read_bytes();assert len(b)==x['bytes'] and hashlib.sha256(b).hexdigest()==x['sha256']
v=json.loads((P/'VERDICT.json').read_text());assert v['verdict']=='PASS_KNOWN_UNSOLVED_PARTIAL' and not v['required_changes'];assert v['report_sha256']==hashlib.sha256((P/'REPORT.md').read_bytes()).hexdigest()
print('PASS closed v2 first-party manifest:',len(actual),'files; no foreign/replay bytes included')
