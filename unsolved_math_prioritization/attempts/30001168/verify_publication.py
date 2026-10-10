#!/usr/bin/env python3
"""Fail-closed publication inventory, immutable archive binding, and replay.

Trust this verifier through its Git commit or an independent external hash.
Arithmetic replay does not replace the analytic proof or its two reviews.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import tempfile
import zipfile

MANIFEST_SHA = '83e462158ca72666cfd4f8b2812303404ad9c122447996e4c9c95d47ab619e5b'
FILES = ['ACCEPTANCE.json', 'PUBLICATION_MANIFEST.json', 'QUEUE_DELTA.json', 'README.md', 'RESEARCH_LOG.md', 'archives/WEIGHTED_YAMABE_30001168_AUTHOR_SAFE_FREEZE.zip', 'archives/WEIGHTED_YAMABE_30001168_INDEPENDENT_AUDIT_SAFE.zip', 'archives/WEIGHTED_YAMABE_30001168_SECOND_REVIEW_SAFE.zip', 'audit/AUDIT.md', 'audit/AUDIT_MANIFEST.json', 'audit/CONTROL_RESULTS.json', 'audit/INDEPENDENT_RESULTS.json', 'audit/README.md', 'audit/SOURCE_VERIFICATION.json', 'audit/author/APPROACH_LOG.md', 'audit/author/MANIFEST.json', 'audit/author/PROOF.md', 'audit/author/README.md', 'audit/author/RESULTS.json', 'audit/author/SOURCE_METADATA.json', 'audit/author/certificate.py', 'audit/author/verify_bundle.py', 'audit/independent_certificate.py', 'audit/run_audit_controls.py', 'audit/verify_audit.py', 'author/APPROACH_LOG.md', 'author/MANIFEST.json', 'author/PROOF.md', 'author/README.md', 'author/RESULTS.json', 'author/SOURCE_METADATA.json', 'author/certificate.py', 'author/verify_bundle.py', 'package_controls.py', 'second_review/INPUTS.json', 'second_review/MANIFEST.json', 'second_review/README.md', 'second_review/RESULTS.json', 'second_review/SECOND_REVIEW.md', 'second_review/four_region_certificate.py', 'second_review/verify_review.py', 'verify_publication.py']
ARCHIVES = {'author': {'path': 'archives/WEIGHTED_YAMABE_30001168_AUTHOR_SAFE_FREEZE.zip', 'bytes': 14945, 'sha256': '6c9ac2c22c5cb50da08c55e12a97a309e5f0b1108dbcb2ac32fa284f93da0987', 'members': 8}, 'audit': {'path': 'archives/WEIGHTED_YAMABE_30001168_INDEPENDENT_AUDIT_SAFE.zip', 'bytes': 33033, 'sha256': 'f278b5119caace5be52ed164c33373f7ebfdee5c7ede5e9f480562032c865bdb', 'members': 17}, 'second_review': {'path': 'archives/WEIGHTED_YAMABE_30001168_SECOND_REVIEW_SAFE.zip', 'bytes': 10915, 'sha256': '2b9b349b85226332cea8c3ff122fde7a29e124b64574ce3d53ff33e2892274ae', 'members': 7}}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def unique(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'duplicate JSON key')
        result[key] = value
    return result


def inventory(root):
    require(stat.S_ISDIR(root.lstat().st_mode), 'root must be a nonsymlink directory')
    directories = set()
    for name in FILES:
        directories.update(str(p) for p in Path(name).parents if str(p) != '.')
    actual = set()
    for p in root.rglob('*'):
        name = p.relative_to(root).as_posix()
        mode = p.lstat().st_mode
        require(not stat.S_ISLNK(mode), 'symlink: ' + name)
        if stat.S_ISDIR(mode):
            require(name in directories, 'unexpected directory: ' + name)
        else:
            require(stat.S_ISREG(mode), 'nonregular file: ' + name)
            actual.add(name)
    require(actual == set(FILES), 'strict publication inventory mismatch')
    raw = (root/'PUBLICATION_MANIFEST.json').read_bytes()
    require(hashlib.sha256(raw).hexdigest() == MANIFEST_SHA, 'pinned manifest mismatch')
    manifest = json.loads(raw, object_pairs_hook=unique)
    require(set(manifest) == {'schema', 'problem_id', 'files'}, 'manifest keys')
    require(manifest['schema'] == 'weighted-yamabe-publication-v1' and manifest['problem_id'] == 30001168, 'manifest schema')
    seen = set()
    for row in manifest['files']:
        require(set(row) == {'path', 'bytes', 'sha256'}, 'manifest row keys')
        name = row['path']
        require(name in FILES and name not in seen and name not in ('PUBLICATION_MANIFEST.json', 'verify_publication.py'), 'manifest path')
        seen.add(name)
        data = (root/name).read_bytes()
        require(type(row['bytes']) is int and len(data) == row['bytes'], 'byte count: ' + name)
        require(hashlib.sha256(data).hexdigest() == row['sha256'], 'hash mismatch: ' + name)
    require(seen == set(FILES)-{'PUBLICATION_MANIFEST.json', 'verify_publication.py'}, 'manifest coverage')
    for directory, info in ARCHIVES.items():
        data = (root/info['path']).read_bytes()
        require(len(data) == info['bytes'] and hashlib.sha256(data).hexdigest() == info['sha256'], 'immutable archive mismatch')
        expected = {p[len(directory)+1:] for p in FILES if p.startswith(directory+'/')}
        with zipfile.ZipFile(root/info['path']) as z:
            members = z.infolist()
            names = [i.filename for i in members]
            require(len(names) == len(set(names)) == info['members'] and set(names) == expected, 'archive inventory')
            require(not z.comment, 'archive comment')
            for item in members:
                require(not item.is_dir() and stat.S_ISREG(item.external_attr >> 16), 'archive nonregular member')
                require(not item.extra and not item.comment and not item.flag_bits & 1, 'archive metadata')
                require(z.read(item) == (root/directory/item.filename).read_bytes(), 'archive and extraction differ')
            require(z.testzip() is None, 'archive CRC mismatch')
    for p in (root/'author').iterdir():
        require(p.read_bytes() == (root/'audit/author'/p.name).read_bytes(), 'audit author copy mismatch')
    return {'verified': True, 'files': len(FILES), 'archives': ARCHIVES, 'manifest_sha256': MANIFEST_SHA}


def execute(root, script, cwd):
    command = [sys.executable, '-I', '-B'] + (['-O'] if sys.flags.optimize else []) + [str(root/script)]
    result = subprocess.run(command, cwd=cwd, capture_output=True, text=True, timeout=180)
    require(result.returncode == 0 and not result.stderr, 'replay failed: ' + script + '\n' + result.stderr)
    return json.loads(result.stdout, object_pairs_hook=unique)


def replays(root, cwd):
    scripts = ['author/verify_bundle.py', 'audit/verify_audit.py', 'second_review/verify_review.py']
    return {script: execute(root, script, cwd) for script in scripts}


def verify(root, integrity_only=False):
    result = inventory(root)
    result.update({'problem_id': 30001168, 'optimized': bool(sys.flags.optimize)})
    if integrity_only:
        return result
    result['ordinary'] = replays(root, root.parent)
    controls = execute(root, 'audit/run_audit_controls.py', root.parent)
    require(controls == json.loads((root/'audit/CONTROL_RESULTS.json').read_bytes()), 'control output mismatch')
    require(controls['passes'] == controls['total'] == 34 and controls['expected_rejections'] == 30, 'control count')
    result['audit_controls'] = {'total': 34, 'accepted_baselines': 4, 'expected_rejections': 30, 'both_optimization_modes': True}
    with tempfile.TemporaryDirectory(prefix='yamabe publication relocation ') as td:
        relocated = Path(td)/'proof with spaces'
        shutil.copytree(root, relocated)
        inventory(relocated)
        result['relocated'] = replays(relocated, Path(td))
        inventory(relocated)
    inventory(root)
    result['frozen_archives_unchanged'] = True
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).absolute().parent)
    parser.add_argument('--integrity-only', action='store_true')
    arguments = parser.parse_args()
    try:
        print(json.dumps(verify(arguments.root.absolute(), arguments.integrity_only), indent=2, sort_keys=True))
    except (ValueError, OSError, KeyError, TypeError, zipfile.BadZipFile) as exc:
        raise SystemExit('FAIL: ' + str(exc))
