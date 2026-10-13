#!/usr/bin/env python3
"""Standalone read-only closure verifier; uses only Python's standard library."""
import argparse, datetime, gzip, hashlib, json, pathlib, subprocess, sys

ap = argparse.ArgumentParser()
ap.add_argument('--include-private', action='store_true', help='require and verify every recorded private source/fixture')
ap.add_argument('--preseal', action='store_true', help='check prepared manifest before FINAL_SEAL exists')
ap.add_argument('--replay', action='store_true', help='replay stable read-only positive/negative programs and compare whole captured streams')
args = ap.parse_args()
root = pathlib.Path(__file__).resolve().parent
sha = lambda b: hashlib.sha256(b).hexdigest()
manifest = json.loads((root/'PUBLIC_MANIFEST.json').read_text())
private = {r['path']:r for r in manifest['private_inventory']}

def checked_path(name):
    p = pathlib.PurePosixPath(name)
    assert not p.is_absolute() and '..' not in p.parts, name
    return root/name

for rec in manifest['files']:
    data = checked_path(rec['path']).read_bytes()
    assert len(data) == rec['bytes'] and sha(data) == rec['sha256'], rec['path']
for name, rec in private.items():
    p = checked_path(name)
    if args.include_private or p.exists():
        data = p.read_bytes()
        assert len(data) == rec['bytes'] and sha(data) == rec['sha256'], name
for seal_name in ['BASELINE_SEAL.json','MATH_ASSESSMENT_SEAL.json']:
    for rec in json.loads((root/seal_name).read_text())['artifacts']:
        p = checked_path(rec['path'])
        if not p.exists():
            assert rec['path'] in private and not args.include_private, rec['path']
            continue
        data = p.read_bytes()
        assert len(data) == rec['bytes'] and sha(data) == rec['sha256'], rec['path']

for path in sorted((root/'captures').glob('*.receipt.json')):
    rec = json.loads(path.read_text())
    for stream in ['stdout','stderr']:
        r = rec[stream]
        data = gzip.decompress(checked_path(r['path']).read_bytes())
        assert len(data) == r['bytes'] and sha(data) == r['sha256'], r['path']
    assert rec['exit_code'] in [0,1] and not rec.get('timed_out',False), path.name

baseline = datetime.datetime.fromisoformat(json.loads((root/'BASELINE_SEAL.json').read_text())['sealed_utc'])
math = datetime.datetime.fromisoformat(json.loads((root/'MATH_ASSESSMENT_SEAL.json').read_text())['sealed_utc'])
first = datetime.datetime.fromisoformat(json.loads((root/'captures/author_replay.receipt.json').read_text())['start_utc'])
assert baseline < math < first

if not args.preseal:
    final = json.loads((root/'FINAL_SEAL.json').read_text())
    assert final['public_manifest_sha256'] == sha((root/'PUBLIC_MANIFEST.json').read_bytes())
    assert final['snapshot_manifest_sha256'] == sha((root.parent/'snapshot_manifest.json').read_bytes())
    assert final['baseline_seal_sha256'] == sha((root/'BASELINE_SEAL.json').read_bytes())
    assert final['math_assessment_seal_sha256'] == sha((root/'MATH_ASSESSMENT_SEAL.json').read_bytes())

if args.replay:
    labels = ['author_replay','portable_math_only','historical_verbatim','integrity_full','integrity_corrected']
    if args.include_private:
        labels += ['portable_full_sources','mutation_radial_sign','mutation_compact_cutoff','mutation_proof_binding','mutation_source_binding']
    for label in labels:
        rec = json.loads((root/'captures'/(label+'.receipt.json')).read_text())
        argv = [sys.executable] + rec['argv'][1:]
        import os
        proc = subprocess.run(argv,cwd=rec['cwd'],env=dict(os.environ,**rec['environment_changes']),stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=120)
        assert proc.returncode == rec['exit_code'], label
        for name, data in [('stdout',proc.stdout),('stderr',proc.stderr)]:
            assert data == gzip.decompress(checked_path(rec[name]['path']).read_bytes()), (label,name)
# Success is intentionally silent; full validation has no mutable output artifacts.
