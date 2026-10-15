"""Verify closed review bindings and literal complete streams; not a proof replay."""
from pathlib import Path
import gzip,hashlib,json,sys
D=Path(__file__).resolve().parent
P=Path(sys.argv[1]) if len(sys.argv)>1 else D.parent/'preprint'
excluded={'IMMUTABLE_MANIFEST.json','FINAL_SEAL.json'}
ignored={'isolation','temporary','private','__pycache__'}
manifest=json.loads((D/'IMMUTABLE_MANIFEST.json').read_bytes())
seal=json.loads((D/'FINAL_SEAL.json').read_bytes())
assert hashlib.sha256((D/'IMMUTABLE_MANIFEST.json').read_bytes()).hexdigest()==seal['manifest_sha256']
expected={r['path'] for r in manifest['files']}
actual={p.relative_to(D).as_posix() for p in D.rglob('*') if p.is_file()
        and p.relative_to(D).as_posix() not in excluded
        and not any(x in ignored for x in p.relative_to(D).parts)}
assert expected==actual and len(expected)==len(manifest['files'])
for row in manifest['files']:
    p=D/row['path'];assert not p.is_symlink() and p.resolve().is_relative_to(D)
    b=p.read_bytes();assert len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256']
for row in manifest['candidate_bindings']:
    b=(P/row['path']).read_bytes()
    assert len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256']
for name in ('SOURCE_ONLY_SCOPE','MATH_ONLY_ASSESSMENT','CERTIFICATE_CONCLUSION'):
    s=json.loads((D/(name+'.seal.json')).read_bytes())
    assert hashlib.sha256((D/s['file']).read_bytes()).hexdigest()==s['sha256']
for rank in range(1,7):
    original=P/'verification/certificates'/('30_action_records.txt.gz' if rank==6 else f'rank{rank}_action_records.txt.gz')
    with gzip.open(original,'rb') as a,gzip.open(D/f'terminal_rank{rank}_records.txt.gz','rb') as b:
        while True:
            left=a.read(65536);right=b.read(65536)
            assert left==right
            if not left:break
assert seal['assigned_review_completion_percent']==100
assert seal['verdict']=='PASS_EXACT_REPAIRED_BYTES_CLEARED_FOR_PUBLICATION'
print('PASS: closed review artifacts, three independence seals, exact repaired submission bindings, and all complete independent record streams')
