#!/usr/bin/env python3
"""Verify immutable research-packet bytes and replay exact algebra checks."""
import hashlib,json,os,pathlib,subprocess,sys
ROOT=pathlib.Path(__file__).resolve().parent
MANIFEST=ROOT/'AUTHOR_MANIFEST.json'
def fail(message):raise RuntimeError(message)
manifest_bytes=MANIFEST.read_bytes()
man=json.loads(manifest_bytes)
if man.get('schema')!='borderline-soliton-author-v1':fail('Wrong manifest schema')
expected=set(man['files'])|{'AUTHOR_MANIFEST.json'}
actual={p.name for p in ROOT.iterdir()}
if actual!=expected:fail(f'Inventory mismatch: missing={sorted(expected-actual)}, extra={sorted(actual-expected)}')
for name,meta in man['files'].items():
    if pathlib.PurePosixPath(name).name!=name:fail('Invalid manifest filename')
    path=ROOT/name
    if path.is_symlink() or not path.is_file():fail('Non-regular payload: '+name)
    raw=path.read_bytes()
    if len(raw)!=meta['bytes'] or hashlib.sha256(raw).hexdigest()!=meta['sha256']:fail('Hash or size mismatch: '+name)
env=dict(os.environ);env['PYTHONDONTWRITEBYTECODE']='1'
p=subprocess.run([sys.executable,'-B',str(ROOT/'check_algebra.py')],cwd=ROOT,env=env,capture_output=True,timeout=90)
if p.returncode:fail('Algebra replay failed: '+p.stderr.decode())
if p.stdout!=(ROOT/'CHECK_RESULTS.json').read_bytes():fail('Algebra replay differs from frozen result')
report=json.loads(p.stdout)
if report['status']!='PASS' or report['exact_checks']!=43 or len(report['mathematical_mutations_rejected'])!=3:fail('Incomplete algebra result')
print(json.dumps({'status':'PASS','payload_files':len(man['files']),'manifest_sha256':hashlib.sha256(manifest_bytes).hexdigest(),'exact_algebra_checks':43,'mathematical_mutations_rejected':3,'claim_scope':'Partial results only; original PDE target unsolved.'},indent=2,sort_keys=True))
