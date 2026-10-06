"""Check all preserved v1/R1 bodies without updating their frozen receipts."""
from pathlib import Path
import datetime, hashlib, json, os

A = Path(__file__).resolve().parent

def require(value, message):
    if not value:
        raise RuntimeError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def checked(path, row):
    require(path.is_file() and not path.is_symlink(), 'Invalid regular body: ' + str(path))
    data = path.read_bytes()
    require(len(data) == row['bytes'] and sha(data) == row['sha256'], 'Body changed: ' + str(path))

summaries = []
for folder, manifest_name, digest, file_key, borrowed_key in [
    ('contingent_credited_note_v1', 'CLOSED_MANIFEST.json',
     'ca4ce63be4957fc836b9e0a5d30dc7049eb22e33cc50d15994444d8e4638adc3',
     'files', 'borrowed_input_bindings'),
    ('whole_package_round1_20261006', 'CLOSED_EVIDENCE_MANIFEST.json',
     'a92201a04ffa95ea2a64ccf6788923221ba5ed198a29f31c95effc428c0a8e42',
     'own_files', 'read_only_input_pins'),
]:
    root = A / folder
    manifest_path = root / manifest_name
    data = manifest_path.read_bytes()
    require(sha(data) == digest, 'Original manifest changed: ' + folder)
    manifest = json.loads(data)
    files = manifest[file_key]
    for row in files:
        path = root / row['path']
        require(path.resolve().is_relative_to(root.resolve()), 'Historical body escape')
        checked(path, row)
    links = manifest.get('controlled_symlinks', [])
    for row in links:
        path = root / row['path']
        require(path.is_symlink() and os.readlink(path) == row['target'], 'Historical symlink changed')
        require(path.resolve().is_relative_to(root.resolve()), 'Historical symlink escape')
    groups = manifest.get('hardlink_groups', [])
    for group in groups:
        paths = [root / relative for relative in group]
        require(len(paths) > 1 and all(path.is_file() and not path.is_symlink() for path in paths),
                'Historical hardlink members invalid')
        require(all(path.resolve().is_relative_to(root.resolve()) for path in paths), 'Historical hardlink escape')
        require(len({(path.stat().st_dev, path.stat().st_ino) for path in paths}) == 1,
                'Historical hardlink group changed')
    declared = {row['path'] for row in files} | {row['path'] for row in links} | set(manifest['excluded'])
    actual = {path.relative_to(root).as_posix() for path in root.rglob('*') if path.is_file() or path.is_symlink()}
    require(actual == declared and manifest['excluded'] == [manifest_name], 'Historical inventory changed')
    for row in manifest[borrowed_key]:
        path = A / row['reference'] if 'reference' in row else Path(row['path'])
        checked(path, row)
    summaries.append({'folder': folder, 'manifest_sha256': digest, 'regular_files': len(files),
                      'controlled_symlinks': len(links), 'hardlink_groups': len(groups),
                      'borrowed_inputs': len(manifest[borrowed_key]), 'all_bytes_and_inventory_unchanged': True})
receipt = {'schema': 'pr97-root-baseline-preservation-after-v2/v1',
           'UTC': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'operator_PID': os.getpid(),
           'historical_packages': summaries, 'frozen_historical_receipts_updated': False,
           'new_central_proof_search_turns': 0, 'publication_authorized': False,
           'priority_clearance': False, 'whole_package_acceptance': False}
destination = A / 'ROOT_V2_BASELINE_PRESERVATION_20261006.json'
with destination.open('x') as stream:
    stream.write(json.dumps(receipt, indent=2) + '\n')
print(json.dumps(receipt))
