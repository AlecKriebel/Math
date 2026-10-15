"""Verify own artifact hashes and 0444 modes; never emit external source contents."""
from pathlib import Path
import hashlib
import json
import stat
import sys

root = Path(__file__).resolve().parents[1]
def require(condition, explanation):
    if not condition:
        raise RuntimeError(explanation)
def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

manifest_path = root / 'public/FINAL_MANIFEST.json'
manifest = json.loads(manifest_path.read_text())
receipt = (root / 'public/FINAL_MANIFEST.sha256').read_text().split()[0]
require(receipt == digest(manifest_path), 'Detached final manifest checksum mismatch')
for entry in manifest['hashed_files']:
    path = root / entry['path']
    require(path.stat().st_size == entry['bytes'], 'Byte-size mismatch: ' + entry['path'])
    require(digest(path) == entry['sha256'], 'Hash mismatch: ' + entry['path'])

inventory_path = root / 'public/FINAL_INVENTORY.json'
if inventory_path.exists():
    inventory = json.loads(inventory_path.read_text())
    actual = sorted(str(path.relative_to(root)) for path in root.rglob('*') if path.is_file())
    require(actual == sorted(entry['path'] for entry in inventory['files']), 'Recursive inventory mismatch')
    for entry in inventory['files']:
        path = root / entry['path']
        require(path.stat().st_size == entry['bytes'], 'Inventory byte mismatch: ' + entry['path'])
        if entry['sha256'] is not None:
            require(digest(path) == entry['sha256'], 'Inventory hash mismatch: ' + entry['path'])

all_files = [path for path in root.rglob('*') if path.is_file()]
for path in all_files:
    require(stat.S_IMODE(path.stat().st_mode) == 0o444, 'File is not 0444: ' + str(path.relative_to(root)))
allowlist = json.loads((root / 'public/SAFE_PUBLIC_ALLOWLIST.json').read_text())
actual_public = {'public/' + path.name for path in (root / 'public').iterdir() if path.is_file()}
if not inventory_path.exists():
    # These three noncircular integrity artifacts are written after the main
    # manifest. The final verification requires their actual presence.
    actual_public.update({'public/FINAL_INVENTORY.json', 'public/VERIFICATION_NORMAL.json',
                          'public/VERIFICATION_OPTIMIZED.json'})
require(sorted(allowlist['safe_paths']) == sorted(actual_public), 'Exact safe public allowlist mismatch')
print(json.dumps({'result': 'PASS', 'optimized': bool(sys.flags.optimize),
                  'manifest_sha256': digest(manifest_path),
                  'manifest_hashed_file_count': len(manifest['hashed_files']),
                  'file_count_at_run': len(all_files), 'every_file_0444': True,
                  'inventory_present_and_verified': inventory_path.exists(),
                  'inventory_sha256': digest(inventory_path) if inventory_path.exists() else None,
                  'verifier_source_sha256': digest(Path(__file__)),
                  'raw_external_content_emitted': False}, indent=2))
