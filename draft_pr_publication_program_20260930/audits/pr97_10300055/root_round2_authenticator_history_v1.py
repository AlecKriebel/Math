"""Authenticate the complete closed fresh review, including dangling/dir controls."""
from pathlib import Path, PurePosixPath
import datetime, hashlib, json, os

A = Path(__file__).resolve().parent
D = A / 'whole_package_round2_20261006'
M = D / 'CLOSED_EVIDENCE_MANIFEST.json'
expected = '4696051fa095f36d77a39063ea9b763148e23d8ffeab9dca48860c785f7cb265'

def require(value, message):
    if not value:
        raise RuntimeError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def own_path(relative):
    name = PurePosixPath(relative)
    require(not name.is_absolute() and '..' not in name.parts, 'Unsafe own path')
    return D / relative

data = M.read_bytes()
require(sha(data) == expected, 'Review manifest differs')
manifest = json.loads(data)
files = manifest['own_files']
for row in files:
    path = own_path(row['path'])
    require(path.is_file() and not path.is_symlink(), 'Invalid own regular file')
    require(path.resolve().is_relative_to(D.resolve()), 'Own regular path escape')
    body = path.read_bytes()
    require(len(body) == row['bytes'] and sha(body) == row['sha256'], 'Own body differs: ' + row['path'])
for row in manifest['controlled_symlinks']:
    path = own_path(row['path'])
    require(path.is_symlink() and os.readlink(path) == row['target'], 'Controlled symlink differs')
    target = path.resolve()
    require(target.is_relative_to(D.resolve()) and row['target_within_review'], 'Controlled symlink escape')
    require(target.exists() == row['target_exists'], 'Controlled target existence changed')
    kind = 'directory' if target.is_dir() else 'regular' if target.is_file() else 'absent'
    require(kind == row['target_kind'], 'Controlled target kind changed')
    if kind == 'regular':
        require(sha(target.read_bytes()) == row['target_sha256'], 'Controlled target body differs')
for group in manifest['hardlink_groups']:
    paths = [own_path(relative) for relative in group]
    require(len(paths) > 1 and all(path.is_file() and not path.is_symlink() for path in paths),
            'Controlled hardlink group invalid')
    require(all(path.resolve().is_relative_to(D.resolve()) for path in paths), 'Hardlink path escape')
    require(len({(path.stat().st_dev, path.stat().st_ino) for path in paths}) == 1,
            'Controlled hardlink identity differs')
    require(all(path.stat().st_nlink == len(group) for path in paths), 'Hardlink group incomplete')
for row in manifest['read_only_input_pins']:
    path = Path(row['path'])
    require(path.is_file() and not path.is_symlink(), 'Borrowed file invalid')
    body = path.read_bytes()
    require(len(body) == row['bytes'] and sha(body) == row['sha256'], 'Borrowed body differs: ' + str(path))
declared = {row['path'] for row in files} | {row['path'] for row in manifest['controlled_symlinks']} | set(manifest['excluded'])
actual = {path.relative_to(D).as_posix() for path in D.rglob('*') if path.is_file() or path.is_symlink()}
require(len(files) == len({row['path'] for row in files}), 'Duplicate regular body')
require(manifest['excluded'] == ['CLOSED_EVIDENCE_MANIFEST.json'] and actual == declared, 'Review closure differs')
require(sha(M.read_bytes()) == expected, 'Manifest changed during authentication')
verdict = json.loads((D / 'VERDICT.json').read_text())
receipt = {
    'schema': 'root-fresh-round2-review-authentication/v1',
    'UTC': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'operator_PID': os.getpid(),
    'review': D.name, 'manifest_sha256': expected,
    'own_regular_files': len(files), 'controlled_symlinks': len(manifest['controlled_symlinks']),
    'hardlink_groups': len(manifest['hardlink_groups']),
    'borrowed_inputs': len(manifest['read_only_input_pins']),
    'all_bytes_and_inventory_authenticated': True,
    'controlled_target_kind_existence_and_regular_bytes_authenticated': True,
    'hardlink_groups_complete': True,
    'ROOT_full_report_independent_assessment_and_reconstruction_read': True,
    'mathematical_verdict': verdict['mathematical_verdict'],
    'whole_package_verdict': verdict['whole_package_verdict'],
    'required_issue_ids': verdict['unresolved_substantive_issue_ids'],
    'priority_clearance': False, 'publication_authorized': False,
    'new_central_proof_search_turns': 0,
}
destination = A / 'root_whole_package_review_authentication_20261006' / (D.name + '.json')
with destination.open('x') as stream:
    stream.write(json.dumps(receipt, indent=2) + '\n')
print(json.dumps(receipt))
