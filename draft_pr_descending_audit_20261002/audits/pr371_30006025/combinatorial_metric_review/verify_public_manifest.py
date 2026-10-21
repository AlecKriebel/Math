#!/usr/bin/env python3
"""Verify this audit's explicit public allowlist and preserved receipts; no writes."""
from pathlib import Path, PurePosixPath
import argparse
import hashlib
import json

parser = argparse.ArgumentParser()
parser.add_argument('--check-private-sources', action='store_true')
args = parser.parse_args()
root = Path(__file__).resolve().parent
def sha(data):
    return hashlib.sha256(data).hexdigest()
def blob(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
def read_json(name):
    return json.loads((root / name).read_bytes())

manifest_bytes = (root / 'PUBLIC_MANIFEST.json').read_bytes()
manifest = json.loads(manifest_bytes)
assert manifest['snapshot_head'] == '51fddd150e8da33f4cf17b1a642a0ffd3466bf5d'
listed = set()
for row in manifest['files']:
    rel = PurePosixPath(row['path'])
    assert not rel.is_absolute() and '..' not in rel.parts and '.' not in rel.parts
    assert rel.as_posix() == row['path'] and row['path'] != 'PUBLIC_MANIFEST.json'
    assert 'private' not in rel.parts and '__pycache__' not in rel.parts
    assert row['path'] not in listed
    listed.add(row['path'])
    path = root.joinpath(*rel.parts)
    assert not path.is_symlink() and path.resolve().is_relative_to(root)
    data = path.read_bytes()
    assert len(data) == row['bytes'] and sha(data) == row['sha256'], row['path']
actual = {p.relative_to(root).as_posix() for p in root.rglob('*')
          if p.is_file() and not {'private', '__pycache__'}.intersection(p.relative_to(root).parts)
          and p.relative_to(root).as_posix() != 'PUBLIC_MANIFEST.json'}
assert actual == listed, {'unlisted': sorted(actual-listed), 'missing': sorted(listed-actual)}

source_seal = read_json('SOURCE_FIRST_BASELINE.seal.json')
assert sha((root/'SOURCE_FIRST_BASELINE.md').read_bytes()) == source_seal['baseline_sha256'] == 'c68f2d0ea64f08a8a6b67862499ccc36ce597f687caa1302274ac75266b15c41'
assert sha((root/'SOURCE_RECEIPTS.json').read_bytes()) == source_seal['receipts_sha256']
math_seal = read_json('MATHEMATICAL_VERDICT.seal.json')
assert sha((root/'MATHEMATICAL_VERDICT.md').read_bytes()) == math_seal['verdict_sha256'] == '689bc8b2003f89b61ab20f2baa7d82a9a396c2d49603f73a7e9b41a10fde0914'
assert sha((root/'SOURCE_FIRST_BASELINE.seal.json').read_bytes()) == math_seal['source_first_seal_sha256'] == '3a10d413c65b5c6c7b08368941b7df2eb482c4262da8ae3b9cd83626196b0bda'
assert sha((root/'SOURCE_ADDENDUM_RECEIPTS.json').read_bytes()) == math_seal['additional_receipts_sha256']
assert source_seal['utc'] < math_seal['utc']

replay = read_json('outputs/AUTHOR_REPLAY_RECEIPT.json')
assert replay['status'] == 'PASS' and len(replay['runs']) == 7
for run in replay['runs']:
    assert run['exit_code'] == 0 and run['stderr_bytes'] == 0
    for stream in ['stdout', 'stderr']:
        data = (root/'outputs'/f"{run['name']}.{stream}").read_bytes()
        assert len(data) == run[f'{stream}_bytes'] and sha(data) == run[f'{stream}_sha256']
    if 'whole_json_retained' in run:
        assert (root/'outputs'/f"{run['name']}.json").read_bytes() == (root/'outputs'/f"{run['name']}.stdout").read_bytes()
        assert run['matches_frozen_receipt_byte_for_byte']
assert sum(r['assertions'] for r in replay['runs'] if r['name'].startswith('turn')) == replay['total_author_assertions'] == 15618
assert math_seal['utc'] < replay['runs'][0]['started_utc']
controls = read_json('outputs/INDEPENDENT_CONTROL_RECEIPT.json')
assert controls['exit_code'] == 0
assert sha((root/'independent_controls.py').read_bytes()) == controls['code_sha256']
for stream in ['stdout','stderr']:
    data = (root/'outputs'/f'independent_controls.{stream}').read_bytes()
    assert len(data) == controls[f'{stream}_bytes'] and sha(data) == controls[f'{stream}_sha256']
assert (root/'outputs/independent_controls.json').read_bytes() == (root/'outputs/independent_controls.stdout').read_bytes()
control_data = read_json('outputs/independent_controls.json')
assert control_data['status'] == 'PASS' and control_data['assertions'] == controls['assertions']

inputs = read_json('outputs/INPUT_READ_RECEIPT.json')
assert inputs['target_files'] == len(inputs['files']) == 46
snapshot = root.parent/'snapshot/problems/30006025_geometric_chapuy'
for row in inputs['files']:
    data = (snapshot/row['path']).read_bytes()
    assert len(data) == row['bytes'] and sha(data) == row['sha256'] and blob(data) == row['git_blob_sha1']
checked = read_json('outputs/MANIFEST_CHECKS.json')
assert all(g['verified'] for g in checked['groups']) and sum(g['entries'] for g in checked['groups']) == checked['total_entries'] == 150

source_count = None
if args.check_private_sources:
    sources = read_json('SOURCE_RECEIPTS.json') + read_json('SOURCE_ADDENDUM_RECEIPTS.json')
    for row in sources:
        data = (root/'private/sources'/f"{row['name']}.pdf").read_bytes()
        assert len(data) == row['bytes'] and sha(data) == row['sha256']
        assert sha((root/'private/sources'/f"{row['name']}.txt").read_bytes()) == row['text_sha256']
    source_count = len(sources)
print(json.dumps({'status':'PASS','public_files':len(listed),'public_manifest_sha256':sha(manifest_bytes),
                  'seals_unchanged':True,'frozen_target_files':46,'historical_manifest_entries':150,
                  'author_assertions':15618,'independent_assertions':controls['assertions'],
                  'private_sources_checked':source_count,
                  'scope':'Receipt and artifact consistency only; mathematical status comes from the sealed independent proof review.'}, indent=2))
