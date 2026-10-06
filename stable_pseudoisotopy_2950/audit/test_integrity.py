#!/usr/bin/env python3
"""Independent positive/negative packaging controls, never a math checker.

Usage: python test_integrity.py AUTHOR.zip AUTHOR_MANIFEST.json AUDIT.zip AUDIT_MANIFEST.json
The audit replay.py must be beside this file. All corruptions remain temporary.
"""
import copy
import hashlib
import json
import stat
import subprocess
import sys
import tempfile
import warnings
from pathlib import Path
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED

CASES = ('missing', 'extra', 'modified', 'duplicate', 'symlink',
         'solution_claim', 'manifest_duplicate_key', 'archive_hash')

def require(condition, message):
    if not condition:
        raise ValueError(message)

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def run(checker, archive, manifest, optimized):
    return subprocess.run([sys.executable] + (['-O'] if optimized else []) +
                          [str(checker), str(archive), str(manifest)],
                          capture_output=True, text=True, timeout=30)

def main():
    require(len(sys.argv) == 5, 'expected author archive/manifest and audit archive/manifest')
    az, am, uz, um = map(lambda value: Path(value).resolve(), sys.argv[1:])
    rows, positives = [], []
    with tempfile.TemporaryDirectory(prefix='stable-pseudoisotopy-controls-') as temp:
        root = Path(temp)
        with ZipFile(az) as archive:
            (root / 'verify_packet.py').write_bytes(archive.read('verify_packet.py'))
        for label, zpath, mpath, checker in (
                ('author', az, am, root / 'verify_packet.py'),
                ('audit', uz, um, Path(__file__).resolve().parent / 'replay.py')):
            require(checker.is_file(), 'checker missing')
            original_manifest = json.loads(mpath.read_text())
            with ZipFile(zpath) as archive:
                original = {name: archive.read(name) for name in archive.namelist()}
            for optimized in (False, True):
                mode = 'optimized' if optimized else 'normal'
                result = run(checker, zpath, mpath, optimized)
                require(result.returncode == 0, label + ' positive rejected: ' + result.stderr)
                positives.append({'packet': label, 'mode': mode, 'result': 'PASS'})
                for case in CASES:
                    folder = root / label / mode / case
                    folder.mkdir(parents=True)
                    files, manifest = dict(original), copy.deepcopy(original_manifest)
                    if case == 'missing':
                        del files['README.md']
                    elif case == 'extra':
                        files['EXTRA.txt'] = b'unauthorized extra member'
                    elif case == 'modified':
                        files['README.md'] += b'corrupted'
                    elif case == 'solution_claim':
                        target = 'STATUS.json' if label == 'author' else 'ACCEPTANCE.json'
                        content = json.loads(files[target])
                        content['status'] = 'solved'
                        files[target] = (json.dumps(content) + '\n').encode()
                        row = next(row for row in manifest['files'] if row['name'] == target)
                        row.update(bytes=len(files[target]), sha256=sha(files[target]))
                    archive_path, manifest_path = folder / zpath.name, folder / mpath.name
                    with warnings.catch_warnings():
                        warnings.simplefilter('ignore', UserWarning)
                        with ZipFile(archive_path, 'w', ZIP_DEFLATED) as archive:
                            for name, data in files.items():
                                info = ZipInfo(name, date_time=(2026, 10, 6, 0, 0, 0))
                                info.create_system = 3
                                info.compress_type = ZIP_DEFLATED
                                info.external_attr = (stat.S_IFREG | 0o644) << 16
                                if case == 'symlink' and name == 'README.md':
                                    info.external_attr = (stat.S_IFLNK | 0o777) << 16
                                archive.writestr(info, data)
                            if case == 'duplicate':
                                archive.writestr('README.md', files['README.md'])
                    raw = archive_path.read_bytes()
                    manifest['archive'].update(bytes=len(raw), sha256=sha(raw))
                    if case == 'archive_hash':
                        manifest['archive']['sha256'] = '0' * 64
                    encoded = json.dumps(manifest)
                    if case == 'manifest_duplicate_key':
                        encoded = encoded[:-1] + ', "problem_id": 2950}'
                    manifest_path.write_text(encoded)
                    result = run(checker, archive_path, manifest_path, optimized)
                    require(result.returncode != 0 and 'REJECT:' in result.stderr,
                            label + '/' + mode + '/' + case + ' did not reject')
                    rows.append({'packet': label, 'mode': mode, 'case': case, 'result': 'REJECT',
                                 'reason': result.stderr.strip()})
    return {'result': 'PASS', 'scope': 'artifact_integrity_only', 'mathematical_proof_check': False,
            'positive_replays': positives, 'negative_controls': rows,
            'negative_control_count': len(rows), 'per_packet_per_mode': len(CASES)}

if __name__ == '__main__':
    try:
        print(json.dumps(main(), indent=2, sort_keys=True))
    except Exception as error:
        print('REJECT: ' + str(error), file=sys.stderr)
        sys.exit(1)
