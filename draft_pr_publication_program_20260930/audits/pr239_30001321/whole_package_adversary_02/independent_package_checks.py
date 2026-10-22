#!/usr/bin/env python3
"""Read-only package/provenance authentication for the second whole-package review.
The only write is its named JSON result beside this script. No network, Git,
provider/tracker operation, source execution, or frozen-package mutation.
"""
from pathlib import Path, PurePosixPath
from datetime import datetime, timezone
import hashlib
import json
import stat
import zipfile

OUT = Path(__file__).resolve().parent
BASE = OUT.parent
Q = BASE / 'publication_package_v1'
V = Q / 'verification'
checks = []

def need(value, name):
    if not value:
        raise AssertionError(name)
    checks.append(name)

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def pinned(path, entry, label):
    raw = path.read_bytes()
    need(len(raw) == entry['bytes'] and digest(raw) == entry['sha256'], label)
    return raw

def relative(name):
    p = PurePosixPath(name)
    need(not p.is_absolute() and '..' not in p.parts and p.as_posix() == name
         and '\\' not in name, 'canonical relative path: ' + name)
    return p

freeze_path = BASE / 'root_package_freeze_01/ROOT_PACKAGE_FREEZE.json'
freeze = json.loads(freeze_path.read_bytes())
for entry in freeze['files']:
    pinned(Q / relative(entry['path']), entry, 'external freeze pin: ' + entry['path'])
    need((Q / entry['path']).stat().st_mode & 0o777 == 0o444,
         'frozen file mode 0444: ' + entry['path'])
need(len(freeze['files']) == 7, 'seven frozen pins')
contents = json.loads((Q / 'PACKAGE_CONTENTS.json').read_bytes())
expected = {e['path']: e for e in contents['files']}
need(len(expected) == len(contents['files']) == contents['file_count'] == 96,
     'positive package selection is 96 unique files')
with zipfile.ZipFile(Q / 'coarse_endpoint_verification.zip') as archive:
    infos = archive.infolist()
    names = [i.filename for i in infos]
    need(len(names) == len(set(names)) == 97, 'ZIP has 97 unique members')
    need(set(names) == set(expected) | {'PACKAGE_CONTENTS.json'}, 'ZIP exact positive membership')
    need(sum(i.file_size for i in infos) == 416304, 'ZIP uncompressed bytes 416304')
    for i in infos:
        relative(i.filename)
        need(not i.is_dir() and stat.S_ISREG(i.external_attr >> 16),
             'ZIP regular file: ' + i.filename)
        raw = archive.read(i)
        need(raw == (Q / i.filename).read_bytes(), 'ZIP/frozen file byte identity: ' + i.filename)
        if i.filename in expected:
            e = expected[i.filename]
            need(len(raw) == e['bytes'] and digest(raw) == e['sha256'],
                 'positive inventory hash: ' + i.filename)

family_manifests = [
    V / 'audits/math_replica_family_01/PUBLIC_MANIFEST.json',
    V / 'audits/math_martingale_family_01/PUBLIC_MANIFEST.json',
    V / 'audits/math_coalescence_family_01/PUBLIC_MANIFEST.json',
    V / 'audits/reproduction_history_family_01/PUBLIC_MANIFEST.json',
    V / 'priority/PUBLIC_MANIFEST_02.json',
]
nested = []
for path in family_manifests:
    data = json.loads(path.read_bytes())
    refs = []
    for e in data['files']:
        name = e.get('relative_path', e.get('name', e['path']))
        if Path(name).is_absolute():
            name = Path(name).name
        relative(name)
        pinned(path.parent / name, e, 'nested family hash: ' + str(path.parent.relative_to(V) / name))
        refs.append(name)
    need(len(refs) == len(set(refs)), 'nested family unique payloads: ' + str(path.relative_to(V)))
    total = sum(e['bytes'] for e in data['files'])
    counts = [data[k] for k in ('file_count', 'payload_count') if k in data]
    totals = [data[k] for k in ('total_bytes', 'total_payload_bytes') if k in data]
    need(all(n == len(refs) for n in counts) and all(n == total for n in totals),
         'nested family counts: ' + str(path.relative_to(V)))
    nested.append({'manifest': str(path.relative_to(V)), 'payload_count': len(refs), 'bytes': total})

seals = [
    V / 'audits/math_replica_family_01/PREPARATION_SEAL.json',
    V / 'audits/math_martingale_family_01/PREPARATION_SEAL.json',
    V / 'audits/math_coalescence_family_01/PREPARATION_SEAL.json',
    V / 'audits/reproduction_history_family_01/SEAL.json',
    V / 'priority/PREPARATION_SEAL_02.json',
]
seal_refs = 0
for path in seals:
    data = json.loads(path.read_bytes())
    for value in data.values():
        if isinstance(value, dict) and {'path', 'bytes', 'sha256'} <= value.keys():
            candidate = path.parent / Path(value['path']).name
            if candidate.is_file():
                pinned(candidate, value, 'nested seal hash: ' + str(candidate.relative_to(V)))
                seal_refs += 1

submission = V / 'submission'
old_manifests = [
    submission / 'TURN_1_MANIFEST.json', submission / 'TURN_2_MANIFEST.json',
    submission / 'FROZEN_MANIFEST.json',
    submission / 'independent_review/REVIEW_MANIFEST.json',
]
old_counts = []
for path in old_manifests:
    data = json.loads(path.read_bytes())
    for e in data['files']:
        pinned(path.parent / relative(e['path']), e, 'historical internal manifest: ' + str(path.relative_to(V)) + ':' + e['path'])
    old_counts.append(len(data['files']))
reviewed = json.loads((submission / 'independent_review/reviewed_hashes.json').read_bytes())
need(reviewed['author_manifest_sha256'] == digest((submission / 'FROZEN_MANIFEST.json').read_bytes()),
     'historical reviewer author-manifest pointer')
need(reviewed['author_files'] == json.loads((submission / 'FROZEN_MANIFEST.json').read_bytes())['files'],
     'historical reviewer exact author file list')
need(json.loads((submission / 'TURN_2_MANIFEST.json').read_bytes())['earlier_manifest_sha256']
     == digest((submission / 'TURN_1_MANIFEST.json').read_bytes()), 'turn-2 earlier-manifest pointer')

materialization_path = BASE / 'authenticated_sources_01/SOURCE_MATERIALIZATION_MANIFEST.json'
materialization_raw = materialization_path.read_bytes()
need(len(materialization_raw) == 65348 and digest(materialization_raw)
     == '4ddb9e5c9dc2487b9fb5fd8f993e562517b5efe2b4af2c2ae87c1a5c61feefa4',
     'external materialization manifest anchor')
materialization = json.loads(materialization_raw)
need(len(materialization['files']) == 64, '64 original/current materialized attempt bodies')
external = {}
for e in materialization['files']:
    p = Path(e['path'])
    need(p.is_relative_to(BASE / 'authenticated_sources_01'), 'materialization path within source scope')
    raw = pinned(p, e, 'materialized attempt body: ' + e['snapshot'] + ':' + e['repository_path'])
    native = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
    need(native == e['native_blob'], 'materialized native Git-blob digest: ' + e['snapshot'] + ':' + e['repository_path'])
    suffix = e['repository_path'].split('attempts/30001321/', 1)[1]
    external[(e['snapshot'], suffix)] = e
    need(raw == (submission / relative(suffix)).read_bytes(), 'archived submission/materialized byte identity: ' + e['snapshot'] + ':' + suffix)
need(len(external) == 64, '64 distinct materialization keys')
portable_manifest = json.loads((V / 'MANIFEST.json').read_bytes())
native_entries = [e for e in portable_manifest['files'] if e['path'].startswith('submission/')]
need(len(native_entries) == 32, '32 portable historical native entries')
for e in native_entries:
    suffix = e['path'][len('submission/'):]
    for snapshot in ('original', 'current'):
        need(all(e[k] == external[snapshot, suffix][k] for k in ('bytes', 'sha256', 'native_blob')),
             'portable/external native pin identity: ' + snapshot + ':' + suffix)

for snapshot in materialization['snapshots']:
    need(snapshot['HEAD'] == '7f17eef77c52b2d9b2ec3ad0803c016267fa6496', 'original/current recorded head')
    e = snapshot['QUEUE']
    p = Path(e['path'])
    need(p.is_relative_to(BASE / 'authenticated_sources_01'), 'materialized queue path within source scope')
    raw = pinned(p, e, 'materialized historical QUEUE bytes: ' + snapshot['label'])
    need(hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest() == e['native_blob'],
         'materialized historical QUEUE native digest: ' + snapshot['label'])

result = {
    'schema': 'pr239-second-whole-package-independent-read-only-authentication-v1',
    'UTC': datetime.now(timezone.utc).isoformat(),
    'status': 'PASS', 'checks': len(checks),
    'seven_freeze_pins': True, 'archive_members': 97, 'archive_payload_bytes': 416304,
    'nested_family_manifests': nested, 'nested_seal_references_checked': seal_refs,
    'historical_manifest_bound_counts': old_counts,
    'original_and_current_attempt_bodies_checked': 64,
    'original_and_current_historical_queue_bodies_checked': 2,
    'all_32_archive_submission_bodies_match_both_recorded_snapshots': True,
    'boundary': 'Read-only comparison of exact local materialized bodies and internal historical bindings. No fresh native-network custody, physical-time, distinct-reviewer-identity, historical-source-access, or pre-freeze-independence claim follows. No frozen package, Git, provider, tracker, PR, global file or lock was changed.',
}
(OUT / 'INDEPENDENT_PROVENANCE_CHECK_RESULT.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
