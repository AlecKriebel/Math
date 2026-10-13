"""Authenticate a closed PR97 correction without rewriting historical custody."""
from pathlib import Path, PurePosixPath
import argparse, datetime, hashlib, json, os, zipfile

parser = argparse.ArgumentParser()
parser.add_argument('expected_manifest_sha256')
args = parser.parse_args()
A = Path(__file__).resolve().parent
D = A / 'contingent_credited_note_v2'
M = D / 'CLOSED_MANIFEST.json'

def require(value, message):
    if not value:
        raise RuntimeError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def checked(path, row):
    require(path.is_file() and not path.is_symlink(), 'Invalid regular file ' + str(path))
    data = path.read_bytes()
    require(len(data) == row['bytes'] and sha(data) == row['sha256'], 'Pin mismatch ' + str(path))
    return data

raw = M.read_bytes()
require(sha(raw) == args.expected_manifest_sha256, 'Closed manifest changed')
manifest = json.loads(raw)
own = manifest['files']
for row in own:
    relative = PurePosixPath(row['path'])
    require(not relative.is_absolute() and '..' not in relative.parts, 'Unsafe own path')
    path = D / row['path']
    require(path.resolve().is_relative_to(D.resolve()), 'Own path escape')
    checked(path, row)
actual = {p.relative_to(D).as_posix() for p in D.rglob('*') if p.is_file() or p.is_symlink()}
require(len(own) == len({row['path'] for row in own}), 'Duplicate own path')
require(manifest['excluded'] == ['CLOSED_MANIFEST.json'], 'Unexpected excluded body')
links = manifest.get('controlled_symlinks', [])
for row in links:
    relative = PurePosixPath(row['path'])
    require(not relative.is_absolute() and '..' not in relative.parts, 'Unsafe link path')
    path = D / row['path']
    require(path.is_symlink() and os.readlink(path) == row['target'], 'Controlled symlink differs')
    require(path.resolve().is_relative_to(D.resolve()), 'Controlled symlink escapes correction')
    require(row['target_within_snapshot'] is True and sha(path.resolve().read_bytes()) == row['target_sha256'],
            'Controlled symlink target body changed')
groups = manifest.get('hardlink_groups', [])
for group in groups:
    paths = [D / relative for relative in group]
    require(len(paths) > 1 and all(path.is_file() and not path.is_symlink() for path in paths),
            'Invalid controlled hardlink group')
    require(all(path.resolve().is_relative_to(D.resolve()) for path in paths), 'Hardlink path escape')
    require(len({(path.stat().st_dev, path.stat().st_ino) for path in paths}) == 1, 'Hardlink identity changed')
require(len(links) == len({row['path'] for row in links}), 'Duplicate controlled symlink')
require(not ({row['path'] for row in own} & {row['path'] for row in links}), 'Overlapping file/link records')
require(actual == {row['path'] for row in own} | {row['path'] for row in links} | set(manifest['excluded']),
        'Own closure differs')
borrowed_schema = manifest['borrowed_input_bindings']
require(borrowed_schema['schema'] == 'pr97-v2-borrowed-inputs/v1', 'Unexpected borrowed schema')
require(borrowed_schema == json.loads((D / 'BORROWED_INPUT_PINS.json').read_text()), 'Borrowed ledger differs')
borrowed = borrowed_schema['original_and_round1'] + borrowed_schema['inherited_math_and_priority']
for row in borrowed:
    path = A / row['reference']
    require(path.resolve().is_relative_to(A.resolve()), 'Borrowed path escape')
    checked(path, row)

public = D / 'publicfiles'
payload = json.loads((public / 'MANIFEST.json').read_text())
for row in payload['files']:
    relative = PurePosixPath(row['path'])
    require(not relative.is_absolute() and '..' not in relative.parts, 'Unsafe payload path')
    checked(public / row['path'], row)
with zipfile.ZipFile(D / 'pr97_support.zip') as archive:
    names = archive.namelist()
    require(len(names) == len(set(names)), 'Duplicate ZIP entry')
    require(set(names) == {row['path'] for row in payload['files']} | {'MANIFEST.json'}, 'ZIP closure differs')
    for name in names:
        relative = PurePosixPath(name)
        require(not relative.is_absolute() and '..' not in relative.parts, 'Unsafe ZIP path')
        require(archive.read(name) == (public / name).read_bytes(), 'ZIP/directory body differs')

proof_copies = [
    ('support/CANDIDATE.md', 'credited_verification_candidate_v2/CANDIDATE.md'),
    ('support/review/author_replay/CANDIDATE.md', 'credited_verification_candidate_v2/CANDIDATE.md'),
    ('support/verify.py', 'credited_verification_candidate_v2/verify.py'),
    ('support/review/independent_checks.py', 'credited_verification_candidate_v2/review/independent_checks.py'),
]
for destination, source in proof_copies:
    require((public / destination).read_bytes() == (A / source).read_bytes(), 'Adopted proof/code copy differs')
preserved = [
    'pr97_note.tex', 'pr97_note.pdf', 'zenodo_metadata.proposed.json',
    'support/CANDIDATE.md', 'support/review/author_replay/CANDIDATE.md',
    'support/verify.py', 'support/review/independent_checks.py', 'check_integrity.py',
    'PRIMARY_SOURCE_READ_SCOPE.json', 'LICENSE.txt',
]
for relative in preserved:
    require((public / relative).read_bytes() == (A / 'contingent_credited_note_v1/publicfiles' / relative).read_bytes(),
            'Intended immutable v1 body changed: ' + relative)
for row in borrowed_schema['byte_identical_static_files']:
    checked(public / row['path'], row)
    path = A / row['original_reference']
    require(path.resolve().is_relative_to(A.resolve()), 'Static borrowed path escape')
    checked(path, row)
provenance = borrowed_schema['metadata_derivation']
path = A / provenance['original_reference']
require(path.resolve().is_relative_to(A.resolve()) and path.is_file() and not path.is_symlink(),
        'Invalid metadata provenance path')
require(sha(path.read_bytes()) == provenance['sha256'], 'Metadata provenance changed')
custody = json.loads((D / 'CUSTODY.json').read_text())
for key, relative in [
    ('payload_manifest_sha256', 'publicfiles/MANIFEST.json'),
    ('zip_sha256', 'pr97_support.zip'),
    ('metadata_sha256', 'publicfiles/zenodo_metadata.proposed.json'),
]:
    require(sha((D / relative).read_bytes()) == custody[key], 'Custody mismatch: ' + key)
deposit = json.loads((D / 'zenodo-deposit.proposed.json').read_text())
require(deposit['metadata'] == json.loads((public / 'zenodo_metadata.proposed.json').read_text()),
        'Proposed metadata wrapper differs')
require(sha(M.read_bytes()) == args.expected_manifest_sha256, 'Manifest changed during authentication')
receipt = {
    'schema': 'pr97-root-prepared-correction-authentication/v1',
    'UTC': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'operator_PID': os.getpid(), 'package': str(D),
    'closed_manifest_sha256': args.expected_manifest_sha256,
    'own_files_authenticated': len(own), 'borrowed_inputs_authenticated': len(borrowed),
    'controlled_symlinks_authenticated': len(links), 'hardlink_groups_authenticated': len(groups),
    'static_borrowed_files_authenticated': len(borrowed_schema['byte_identical_static_files']),
    'metadata_provenance_authenticated': True,
    'payload_files': len(payload['files']), 'zip_members': len(names),
    'zip_directory_byte_identity': True,
    'adopted_proof_and_mathematical_code_byte_identity': True,
    'preserved_v1_public_bodies': preserved, 'custody_and_metadata_bindings_match': True,
    'ROOT_full_preparation_report_read': True,
    'all_file_contents_substantively_reviewed_by_ROOT': False,
    'whole_package_acceptance': False, 'priority_clearance': False,
    'publication_authorized': False, 'original_effort': '2/5',
    'new_central_proof_search_turns': 0,
    'own_pins': own, 'borrowed_pins': borrowed,
}
destination = A / 'ROOT_PREPARED_PACKAGE_V2_AUTHENTICATION_20261006.json'
require(not destination.exists(), 'Authentication receipt already exists')
with destination.open('x') as stream:
    stream.write(json.dumps(receipt, indent=2) + '\n')
print(json.dumps({key: value for key, value in receipt.items() if key not in ['own_pins', 'borrowed_pins']}))
