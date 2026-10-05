#!/usr/bin/env python3
"""Audit the supplied freeze, run it, and reject safe-copy integrity mutations."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from zipfile import ZipFile

EXPECTED_ARCHIVE = '70191b3887e8863701651cdb54382958e1f8190fd889889a2ed81c46f16ee6a6'
EXPECTED_MANIFEST = 'bb24c27fef83fcc14106cbcc068a02f740c0b35385b79e6c7799371764ea9bdb'

def insist(condition, message):
    if not condition:
        raise ValueError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def safe_tree(root):
    manifest_bytes = (root / 'MANIFEST.json').read_bytes()
    insist(sha(manifest_bytes) == EXPECTED_MANIFEST, 'Unexpected original manifest')
    m = json.loads(manifest_bytes)
    expected = {x['path']: x for x in m['files']}
    insist(len(expected) == len(m['files']), 'Duplicate manifest entry')
    insist(set(p.name for p in root.iterdir()) == set(expected) | {'MANIFEST.json'}, 'Closed allowlist mismatch')
    for p in root.iterdir():
        insist(p.is_file() and not p.is_symlink(), 'Nonregular payload entry')
        if p.name == 'MANIFEST.json':
            continue
        record = expected[p.name]
        insist(Path(record['path']).name == record['path'], 'Nonlocal manifest entry')
        b = p.read_bytes()
        insist(len(b) == record['bytes'] and sha(b) == record['sha256'], 'Payload byte/hash mismatch')
    return expected

def main():
    if len(sys.argv) != 2:
        raise SystemExit('Usage: python3 verify_frozen.py ORIGINAL_DIRECTORY_WITH_SAFE_AND_ZIP')
    base = Path(sys.argv[1]).resolve()
    expected = safe_tree(base / 'safe')
    archive = (base / 'SIS_30003676_SAFE.zip').read_bytes()
    insist(len(archive) == 22001 and sha(archive) == EXPECTED_ARCHIVE, 'Frozen archive mismatch')
    with ZipFile(base / 'SIS_30003676_SAFE.zip') as z:
        names = z.namelist()
        want = {'safe/' + x for x in expected} | {'safe/MANIFEST.json'}
        insist(len(names) == len(want) and set(names) == want, 'Archive allowlist mismatch')
        for name in names:
            insist(z.read(name) == (base / name).read_bytes(), 'Archive member differs from safe tree')
    replay = subprocess.run([sys.executable, str(base/'safe'/'verify.py')], check=True,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout
    insist(replay == (base/'safe'/'verification_results.json').read_bytes(), 'Author replay differs')
    author_controls = json.loads(subprocess.run([sys.executable, str(base/'safe'/'verify_manifest.py')],
                                               check=True, stdout=subprocess.PIPE).stdout)
    mutations = ['content_tamper', 'unexpected_file', 'missing_file', 'symlink_entry']
    for mutation in mutations:
        with tempfile.TemporaryDirectory(prefix='sis-independent-integrity-') as temp:
            target = Path(temp)/'safe'
            shutil.copytree(base/'safe', target)
            if mutation == 'content_tamper':
                with (target/'REPORT.md').open('ab') as f:
                    f.write(b'\nSYNTHETIC TAMPER\n')
            elif mutation == 'unexpected_file':
                (target/'synthetic_unlisted.txt').write_text('synthetic negative control')
            elif mutation == 'missing_file':
                (target/'attempts.json').unlink()
            else:
                content = (target/'REPORT.md').read_bytes()
                outside = Path(temp)/'same_bytes.md'
                outside.write_bytes(content)
                (target/'REPORT.md').unlink()
                (target/'REPORT.md').symlink_to(outside)
            rejected = False
            try:
                safe_tree(target)
            except (ValueError, OSError):
                rejected = True
            insist(rejected, 'Escaped integrity control: '+mutation)
    safe_tree(base/'safe')
    print(json.dumps({'status':'PASS','archive_bytes':len(archive),'archive_sha256':sha(archive),
                      'manifest_sha256':EXPECTED_MANIFEST,'archive_members':10,'payload_files':9,
                      'archive_members_equal_safe_files':True,'author_replay_byte_identical':True,
                      'author_exact_checks':json.loads(replay)['total_checks'],
                      'author_integrity_controls':author_controls,
                      'independent_integrity_mutations_rejected':mutations,
                      'original_freeze_preserved':True,'remote_writes':False},indent=2,sort_keys=True))

if __name__ == '__main__':
    main()
