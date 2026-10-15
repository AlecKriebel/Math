#!/usr/bin/env python3
"""Provider-free Root byte association and independent checker replay.

Only a fresh owned output directory is written. Full third-party bodies remain
private and are never copied into the public findings packet.
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument('--output-dir', required=True)
ap.add_argument('--library-dir', required=True)
args = ap.parse_args()
assert not sys.flags.optimize
B = Path(__file__).resolve().parent
D = Path(args.output_dir).resolve()
D.mkdir(exist_ok=False)
checks, inputs, replays = [], [], []
pin = lambda raw: {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}
def ck(value, label):
    assert value, label
    checks.append(label)
def read(p):
    ck(p.is_file() and not p.is_symlink(), 'regular:' + str(p))
    raw = p.read_bytes()
    inputs.append({'path': str(p), **pin(raw)})
    return raw
G = B / 'priority_general_theorem'
freeze = json.loads(read(G / 'INDEPENDENCE_FREEZE.json'))
for item in freeze['files']:
    path = Path(item['path'])
    ck(not path.is_absolute() and '..' not in path.parts, 'safe frozen path')
    raw = read(G / path)
    ck(pin(raw) == {k: item[k] for k in ('bytes', 'sha256')}, 'independent-freeze:' + str(path))
A = B / 'priority_repository_archive'
P = A / 'private_reading'
association = json.loads(read(A / 'public/DEPOSIT_ASSOCIATION.json'))
record = json.loads(read(P / 'zenodo_23071366_retry.json'))
doi = '10.5281/zenodo.23071366'
ck(record['doi'] == association['doi'] == doi, 'record DOI')
ck(record['id'] == association['record_id'] == 23071366, 'record identity')
ck(record['status'] == 'published' and record['metadata']['access_right'] == 'open', 'record published open')
ck(record['metadata']['title'] == 'Stationary Focal Antipedal Centroids for Even Elliptic Billiard Periods', 'record title')
for key in ('created', 'modified'):
    ck(record[key] == association[key], 'repository clock:' + key)
names = {
    'main.pdf': ('zenodo_23071366_main.pdf', 'eulersolve_0026.pdf'),
    'arxiv_source.zip': ('zenodo_23071366_source.zip', 'eulersolve_0026_source.zip'),
    'verification_report.md': ('zenodo_23071366_verification.md', 'eulersolve_0026_verification.md'),
}
for row in association['attachments']:
    files = [f for f in record['files'] if f['key'] == row['key']]
    ck(len(files) == 1, 'unique record attachment')
    f = files[0]
    raw = read(P / names[row['key']][0])
    website = read(P / names[row['key']][1])
    md5 = 'md5:' + hashlib.md5(raw).hexdigest()
    ck(raw == website, 'actual archived and website byte equality:' + row['key'])
    ck(len(raw) == f['size'] == row['record_size'] == row['actual_bytes'], 'record size:' + row['key'])
    ck(md5 == f['checksum'] == row['record_md5'] == row['actual_md5'], 'record MD5:' + row['key'])
    ck(pin(raw)['sha256'] == row['actual_sha256'], 'actual archive SHA256:' + row['key'])
    ck(f['links']['self'] == row['record_file_url'] == 'https://zenodo.org/api/records/23071366/files/' + row['key'] + '/content', 'record-owned URL:' + row['key'])
datacite = json.loads(read(P / 'datacite_23071366.json'))['data']
ck(datacite['id'] == doi and datacite['attributes']['doi'] == doi, 'DataCite DOI')
ck(datacite['attributes']['state'] == 'findable', 'DataCite state')
ck(datacite['attributes']['created'] == datacite['attributes']['registered'] == '2026-09-30T22:04:13.000Z', 'DataCite clocks')
root_datacite = read(B / 'root_priority_capture_01/reading_private/official_02/datacite.body')
ck(json.loads(root_datacite) == {'data': datacite}, 'independent Root DataCite content equality')
def inventory(base, manifest_name, keys):
    manifest = json.loads(read(base / manifest_name))
    for key, path_key in keys:
        for item in manifest[key]:
            rel = Path(item[path_key])
            ck(not rel.is_absolute() and '..' not in rel.parts, 'safe manifest path:' + str(rel))
            raw = read(base / rel)
            ck(pin(raw) == {k: item[k] for k in ('bytes', 'sha256')}, 'manifest:' + manifest_name + ':' + str(rel))
    return manifest
inventory(G, 'PUBLIC_MANIFEST.json', [('included', 'path')])
inventory(G, 'POST_FREEZE_PUBLIC_MANIFEST.json', [('files', 'path')])
inventory(A / 'public', 'MANIFEST.json', [('files', 'path')])
private_pin = json.loads(read(A / 'public/PRIVATE_INVENTORY_PIN.json'))
ck(pin(read(P / 'MANIFEST.json')) == {k: private_pin[k] for k in ('bytes', 'sha256')}, 'archive private inventory pin')
private_manifest = inventory(P, 'MANIFEST.json', [('files', 'path')])
ck(len(private_manifest['files']) == private_pin['file_count'] == 88, 'archive private inventory count')
L = B / 'priority_primary_lineage'
inventory(L, 'ARTIFACT_MANIFEST.json', [('public_derived_artifacts', 'relative_path'), ('private_evidence', 'relative_path')])
comparison_manifest = inventory(L, 'COMPARISON_MANIFEST.json', [('public_derived_artifacts', 'relative_path'), ('private_comparison_evidence', 'relative_path')])
ck(pin(read(L / 'ARTIFACT_MANIFEST.json'))['sha256'] == comparison_manifest['initial_manifest_sha256'], 'primary initial manifest preserved')
for row in json.loads(read(G / 'PRIVATE_SOURCE_MANIFEST.json')):
    ck(pin(read(G / 'private_sources' / (row['id'] + '.pdf'))) == {k: row[k] for k in ('bytes', 'sha256')}, 'general primary PDF:' + row['id'])
    ck(pin(read(G / 'private_sources' / (row['id'] + '.txt')))['sha256'] == row['text_sha256'], 'general primary extracted text:' + row['id'])
def replay(source, output, receipt_name, excluded):
    raw = read(source)
    scratch = D / output
    scratch.mkdir()
    target = scratch / source.name
    target.write_bytes(raw)
    ck(read(target) == raw, 'unchanged scratch checker')
    wrapper = 'import runpy,sys;sys.path.insert(0,sys.argv[1]);sys.path.insert(0,sys.argv[2]);runpy.run_path(sys.argv[3],run_name="__main__")'
    result = subprocess.run([sys.executable, '-I', '-B', '-c', wrapper, str(Path(args.library_dir).resolve()), str(scratch), str(target)], cwd=scratch, env={**os.environ, 'PYTHONHASHSEED':'0'}, capture_output=True, timeout=240)
    (scratch / 'stdout').write_bytes(result.stdout)
    (scratch / 'stderr').write_bytes(result.stderr)
    ck(result.returncode == 0, 'checker exit:' + source.name)
    ck(not result.stderr, 'checker stderr:' + source.name)
    fresh_raw = read(scratch / receipt_name)
    old_raw = read(source.parent / receipt_name)
    fresh, old = json.loads(fresh_raw), json.loads(old_raw)
    for key in excluded:
        fresh.pop(key, None)
        old.pop(key, None)
    ck(fresh == old, 'checker exact mathematical receipt equality:' + source.name)
    replays.append({'source': str(source), 'source_pin': pin(raw), 'returncode': result.returncode, 'receipt_pin': pin(fresh_raw), 'historical_receipt_pin': pin(old_raw), 'excluded_metadata': excluded, 'mathematical_content_identical': True})
replay(G / 'verify_reduction.py', 'general_reduction', 'REDUCTION_VERIFICATION.json', ['utc'])
replay(A / 'public/check_algebra.py', 'archive_algebra', 'ALGEBRA_RECEIPT.json', ['checked_utc'])
replay(G / 'verify_comparison.py', 'general_comparison', 'COMPARISON_VERIFICATION.json', ['utc'])
receipt = {'utc': datetime.now(timezone.utc).isoformat(), 'decision': 'PASS_COMPONENT_VERIFICATION_ONLY', 'completed': True, 'checks': len(checks), 'check_labels': checks, 'inputs': inputs, 'replays': replays, 'limits': 'Component byte association and reproduced identities only. No provider authority, final aggregate priority disposition, absolute first visibility or private intellectual-order claim.'}
(D / 'VERIFICATION.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps({'decision': receipt['decision'], 'checks': len(checks), 'replays': len(replays)}))
