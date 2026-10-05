#!/usr/bin/env python3
"""Independent checker anchored to both immutable digests in the audit assignment."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import tempfile
import zipfile

MANIFEST_SHA256 = '5f892f30acb55e30ccfcf88932e933c55b76942583bca032bbc8339d95548791'
ARCHIVE_SHA256 = 'd3c1884b33f378a1289dcbd6eea175dd0e721964f478a6ceb6186d7990d77b1b'
ARCHIVE_BYTES = 29837
ARCHIVE_NAME = 'DIRICHLET_ZERO_30002507_AUTHOR_FREEZE.zip'


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def verify(root):
    root = Path(root)
    require(root.is_dir() and not root.is_symlink(), 'root is not a regular directory')
    safe = root / 'safe'
    require(safe.is_dir() and not safe.is_symlink(), 'unsafe safe-payload directory')
    files = list(safe.iterdir())
    require(all(p.is_file() and not p.is_symlink() for p in files), 'nonregular payload entry')
    data = (safe / 'MANIFEST.json').read_bytes()
    require(digest(data) == MANIFEST_SHA256, 'frozen manifest digest mismatch')
    manifest = json.loads(data)
    require(manifest['schema'] == 'dirichlet-single-zero-manifest-v1', 'manifest schema mismatch')
    rows = manifest['files']
    require(len(rows) == 17, 'payload count mismatch')
    expected = {r['path'] for r in rows} | {'MANIFEST.json'}
    require(len(expected) == 18 and {p.name for p in files} == expected, 'inventory mismatch')
    for row in rows:
        require(Path(row['path']).name == row['path'], 'nonflat path')
        content = (safe / row['path']).read_bytes()
        require(len(content) == row['bytes'] and digest(content) == row['sha256'], 'payload mismatch')
    archive = root / ARCHIVE_NAME
    require(archive.is_file() and not archive.is_symlink(), 'nonregular archive')
    archive_data = archive.read_bytes()
    require(len(archive_data) == ARCHIVE_BYTES and digest(archive_data) == ARCHIVE_SHA256, 'frozen archive mismatch')
    with zipfile.ZipFile(archive) as z:
        members = z.infolist()
        require(len(members) == 18 and {i.filename for i in members} == expected, 'archive inventory mismatch')
        require(z.testzip() is None, 'archive CRC failure')
        for member in members:
            require(not member.is_dir(), 'archive directory entry')
            require(z.read(member) == (safe / member.filename).read_bytes(), 'archive payload mismatch')
    return {'result': 'PASS', 'payload_files': 17, 'safe_files': 18, 'archive_members': 18,
            'author_manifest_sha256': MANIFEST_SHA256, 'author_archive_sha256': ARCHIVE_SHA256}


def negative_controls(author):
    labels = ['alter_payload', 'truncate_payload', 'missing_payload', 'extra_payload',
              'extra_directory', 'payload_symlink', 'wrong_recorded_hash', 'wrong_recorded_size',
              'extra_manifest_key', 'duplicate_manifest_row', 'parent_path', 'rehash_changed_payload',
              'duplicate_json_key', 'manifest_whitespace', 'alter_archive', 'truncate_archive',
              'root_symlink', 'private_pdf_intrusion']
    results = {}
    with tempfile.TemporaryDirectory(prefix='dirichlet-independent-binding-') as temp:
        temp = Path(temp)
        for label in ['intact'] + labels:
            root = temp / label
            root.mkdir()
            shutil.copytree(author / 'safe', root / 'safe')
            shutil.copy2(author / ARCHIVE_NAME, root / ARCHIVE_NAME)
            target = root / 'safe/TURN_5_GENERALIZED_ROUNDING.md'
            mp = root / 'safe/MANIFEST.json'
            if label == 'alter_payload':
                target.write_bytes(b'!' + target.read_bytes()[1:])
            elif label == 'truncate_payload':
                target.write_bytes(target.read_bytes()[:-1])
            elif label == 'missing_payload':
                target.unlink()
            elif label == 'extra_payload':
                (root / 'safe/extra.txt').write_text('extra')
            elif label == 'extra_directory':
                (root / 'safe/extra').mkdir()
            elif label == 'payload_symlink':
                target.unlink()
                target.symlink_to(author / 'safe/TURN_5_GENERALIZED_ROUNDING.md')
            elif label == 'private_pdf_intrusion':
                (root / 'safe/private.pdf').write_bytes(b'%PDF-1.4\nsynthetic exclusion fixture\n')
            elif label in {'wrong_recorded_hash', 'wrong_recorded_size', 'extra_manifest_key',
                           'duplicate_manifest_row', 'parent_path', 'rehash_changed_payload'}:
                m = json.loads(mp.read_text())
                if label == 'wrong_recorded_hash':
                    m['files'][0]['sha256'] = '0' * 64
                elif label == 'wrong_recorded_size':
                    m['files'][0]['bytes'] = True
                elif label == 'extra_manifest_key':
                    m['extra'] = True
                elif label == 'duplicate_manifest_row':
                    m['files'].append(m['files'][0])
                elif label == 'parent_path':
                    m['files'][0]['path'] = '../outside'
                else:
                    target.write_bytes(b'!' + target.read_bytes()[1:])
                    row = next(r for r in m['files'] if r['path'] == target.name)
                    row['sha256'] = digest(target.read_bytes())
                mp.write_text(json.dumps(m, indent=2) + '\n')
            elif label == 'duplicate_json_key':
                mp.write_text(mp.read_text().replace('{', '{"schema":"dirichlet-single-zero-manifest-v1",', 1))
            elif label == 'manifest_whitespace':
                mp.write_text(mp.read_text() + '\n')
            elif label == 'alter_archive':
                p = root / ARCHIVE_NAME
                b = bytearray(p.read_bytes()); b[len(b)//2] ^= 1; p.write_bytes(b)
            elif label == 'truncate_archive':
                p = root / ARCHIVE_NAME; p.write_bytes(p.read_bytes()[:-1])
            elif label == 'root_symlink':
                link = temp / 'linked-root'; link.symlink_to(root, target_is_directory=True); root = link
            accepted = True
            try:
                verify(root)
            except (ValueError, OSError, KeyError, zipfile.BadZipFile):
                accepted = False
            require(accepted == (label == 'intact'), 'incorrect verdict for ' + label)
            results[label] = 'accepted' if accepted else 'rejected'
    return {'schema': 'dirichlet-independent-binding-negative-controls-v1', 'result': 'PASS',
            'negative_cases': len(labels), 'cases': results,
            'scope': 'Byte-frozen binding and inventory; not analytic theorem certification.'}


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--author', type=Path, default=Path(__file__).resolve().parent.parent / 'dirichlet_zero_30002507')
    ap.add_argument('--negative-controls', action='store_true')
    args = ap.parse_args()
    result = negative_controls(args.author.resolve()) if args.negative_controls else verify(args.author)
    print(json.dumps(result, indent=2, sort_keys=True))
