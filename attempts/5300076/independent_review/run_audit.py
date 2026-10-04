#!/usr/bin/env python3
"""Portable, read-only replay against a hash-bound author packet."""
import argparse, hashlib, json, pathlib, subprocess, sys, zipfile
ROOT=pathlib.Path(__file__).resolve().parent
ap=argparse.ArgumentParser()
ap.add_argument('--input',required=True,type=pathlib.Path)
ap.add_argument('--zip',type=pathlib.Path)
args=ap.parse_args()
source=args.input.resolve()
binding=json.loads((ROOT/'AUDITED_INPUTS.json').read_text())
def digest(data):return hashlib.sha256(data).hexdigest()
def run(script,cwd):
    result=subprocess.run([sys.executable,str(script)],cwd=cwd,capture_output=True,check=True)
    if result.stderr:raise AssertionError(result.stderr.decode())
    return result.stdout
expected={e['path'] for e in binding['files']}
actual={str(p.relative_to(source)) for p in source.rglob('*') if p.is_file()}
assert actual==expected, ('Input inventory mismatch',sorted(actual^expected))
for entry in binding['files']:
    p=pathlib.Path(entry['path'])
    assert not p.is_absolute() and '..' not in p.parts
    data=(source/p).read_bytes()
    assert len(data)==entry['bytes'] and digest(data)==entry['sha256'],str(p)
manifest_output=run(source/'verify_manifest.py',source)
assert manifest_output==b'PASS: 11 frozen files\n'
author=run(source/'verify.py',source)
assert author==(source/'CONTROL_RESULTS.json').read_bytes()
assert author==(ROOT/'AUTHOR_REPLAY_RESULTS.json').read_bytes()
independent=run(ROOT/'independent_checks.py',ROOT)
assert independent==(ROOT/'INDEPENDENT_CHECK_RESULTS.json').read_bytes()
zip_status='NOT_REQUESTED'
if args.zip:
    data=args.zip.read_bytes()
    assert len(data)==binding['zip']['bytes'] and digest(data)==binding['zip']['sha256']
    with zipfile.ZipFile(args.zip) as z:
        names=z.namelist()
        assert len(names)==len(set(names))
        assert set(names)==expected
        for name in names:assert z.read(name)==(source/name).read_bytes()
    zip_status='PASS'
print(json.dumps({'status':'PASS','problem_id':5300076,'bound_author_files':len(expected),
                  'author_assertions':json.loads(author)['assertions'],
                  'independent_assertions':json.loads(independent)['assertions'],
                  'author_manifest':'PASS','author_output_byte_match':True,
                  'independent_output_byte_match':True,'zip':zip_status},indent=2,sort_keys=True))
