#!/usr/bin/env python3
"""Strict publication binding and portable replays. Trust this file via its Git commit."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import stat
import subprocess
import sys
import tempfile
import zipfile

MANIFEST_SHA256 = 'ffc3d842f5ea380ae40500f8879e4283808634f10ff2b2f0496bda6675cb2874'
MANIFEST_BYTES = 3330
PINNED = {
    'packet/MANIFEST.json': (1648, '1f64af140ad77607cfd4a0ea61ed418853f9af99740387632b6f30545050b1f6'),
    'independent-audit/AUDIT_MANIFEST.json': (1535, '17bd438880d29f36f4a1ae1007ca2c0463e461d8393654028d3258387bde2615'),
    'rank670-independent-audit.zip': (13241, '253082ed4706b701e2e45988bf6bb861cc0bf8b783130be1e2fbe469fbb06263'),
}
TRUST_ROOTS = {'PUBLICATION_MANIFEST.json', 'verify_release.py'}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def unique(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'Duplicate JSON key: ' + key)
        result[key] = value
    return result


def load_json(data):
    return json.loads(data, object_pairs_hook=unique)


def matches(data, size, digest):
    return len(data) == size and hashlib.sha256(data).hexdigest() == digest


def integrity(root):
    root = Path(root).absolute()
    require(not root.is_symlink() and root.is_dir(), 'Invalid or symlinked package root')
    actual_files, actual_dirs = set(), set()
    for path in root.rglob('*'):
        name = path.relative_to(root).as_posix()
        mode = path.lstat().st_mode
        require(not stat.S_ISLNK(mode), 'Symlink: ' + name)
        if stat.S_ISDIR(mode):
            actual_dirs.add(name)
        else:
            require(stat.S_ISREG(mode), 'Non-regular file: ' + name)
            actual_files.add(name)
    require(actual_dirs == {'packet', 'independent-audit'}, 'Directory-set mismatch')
    raw = (root / 'PUBLICATION_MANIFEST.json').read_bytes()
    require(matches(raw, MANIFEST_BYTES, MANIFEST_SHA256), 'Publication manifest binding mismatch')
    manifest = load_json(raw)
    require(manifest['target_id'] == 10300062 and manifest['rank'] == 670, 'Target mismatch')
    require(manifest['status'] == 'unsolved' and manifest['turns'] == '5/5', 'Disposition mismatch')
    require(set(manifest['trust_roots']) == TRUST_ROOTS, 'Trust-root mismatch')
    entries = manifest['files']
    expected = set()
    for entry in entries:
        name = entry['path']
        p = PurePosixPath(name)
        require(not p.is_absolute() and name == p.as_posix() and '..' not in p.parts and '\\' not in name, 'Unsafe path')
        require(name not in expected and name not in TRUST_ROOTS, 'Duplicate or excluded payload entry')
        expected.add(name)
    require(len(expected) == 19, 'Payload count mismatch')
    require(actual_files == expected | TRUST_ROOTS, 'File-set mismatch: ' + str(sorted(actual_files ^ (expected | TRUST_ROOTS))))
    for entry in entries:
        require(matches((root / entry['path']).read_bytes(), entry['bytes'], entry['sha256']), 'Payload mismatch: ' + entry['path'])
    for name, (size, digest) in PINNED.items():
        require(matches((root / name).read_bytes(), size, digest), 'Frozen binding mismatch: ' + name)
    audit_names = sorted(p for p in expected if p.startswith('independent-audit/'))
    with zipfile.ZipFile(root / 'rank670-independent-audit.zip') as archive:
        names = archive.namelist()
        require(len(names) == len(set(names)) and sorted(names) == audit_names, 'Archive inventory mismatch')
        for item in archive.infolist():
            require(stat.S_ISREG(item.external_attr >> 16), 'Archive contains non-regular entry')
            require(archive.read(item) == (root / item.filename).read_bytes(), 'Archive differs from expanded audit')
    return {'status': 'PASS', 'artifact_files': 21, 'payload_files': 19, 'publication_manifest_sha256': MANIFEST_SHA256,
            'author_manifest_sha256': PINNED['packet/MANIFEST.json'][1],
            'audit_manifest_sha256': PINNED['independent-audit/AUDIT_MANIFEST.json'][1]}


def run(script, *args):
    # -I ignores PYTHONOPTIMIZE and other interpreter environment variables.
    # -B prevents cache files; no -O is inherited by these new processes.
    result = subprocess.run([sys.executable, '-I', '-B', str(script), *map(str, args)], cwd=script.parent,
                            capture_output=True, timeout=120)
    require(result.returncode == 0, script.name + ' failed: ' + result.stderr.decode(errors='replace'))
    return result.stdout


def replay(root):
    with tempfile.TemporaryDirectory(prefix='leaf-approximation-replay-') as temporary:
        copied = Path(temporary) / 'relocated'
        shutil.copytree(root, copied)
        audit, packet = copied / 'independent-audit', copied / 'packet'
        run(audit / 'verify_binding.py', packet)
        run(audit / 'verify_audit_manifest.py')
        # replay_controls imports its sibling. Isolated -c explicitly adds only that audited directory.
        code = "import runpy,sys;sys.path.insert(0,sys.argv[1]);sys.argv=sys.argv[2:];runpy.run_path(sys.argv[0],run_name='__main__')"
        result = subprocess.run([sys.executable, '-I', '-B', '-c', code, str(audit), str(audit / 'replay_controls.py'), str(packet)],
                                cwd=Path(temporary), capture_output=True, timeout=120)
        require(result.returncode == 0, 'Independent replay failed: ' + result.stderr.decode(errors='replace'))
        require(result.stdout == (audit / 'replay_results.json').read_bytes(), 'Independent output differs byte-for-byte')
        # The audit runs the assertion-based author subprocesses. Strip optimization from that subprocess environment too.
        # The isolated audit's child sys.executable is invoked without -O, and PYTHONOPTIMIZE is removed below.
        integrity(copied)
    return {'status': 'PASS', 'author_results_byte_identical': True, 'independent_results_byte_identical': True,
            'independent_positive_power_pairs': 4096, 'Euler_degrees': 1000, 'torus_cover_degrees': '2 through 1000'}


def self_test(root):
    labels = ['changed_author_file', 'missing_author_file', 'extra_file', 'nested_manifest', 'extra_root_manifest',
              'changed_author_manifest', 'changed_audit_manifest', 'changed_publication_manifest',
              'changed_audit_archive', 'changed_audit_file', 'file_symlink', 'directory_symlink', 'empty_extra_directory', 'root_symlink']
    results = []
    with tempfile.TemporaryDirectory(prefix='leaf-approximation-negative-') as temporary:
        temporary = Path(temporary)
        for label in labels:
            copied = temporary / label
            shutil.copytree(root, copied)
            if label == 'missing_author_file':
                (copied / 'packet/README.md').unlink()
            elif label == 'extra_file':
                (copied / 'packet/EXTRA.txt').write_text('test\n')
            elif label == 'nested_manifest':
                (copied / 'packet/nested').mkdir()
                (copied / 'packet/nested/MANIFEST.json').write_text('{}\n')
            elif label == 'extra_root_manifest':
                (copied / 'MANIFEST.json').write_text('{}\n')
            elif label == 'file_symlink':
                p = copied / 'packet/README.md'; p.unlink(); p.symlink_to(root / 'packet/README.md')
            elif label == 'directory_symlink':
                p = copied / 'packet'; shutil.rmtree(p); p.symlink_to(root / 'packet', target_is_directory=True)
            elif label == 'empty_extra_directory':
                (copied / 'empty').mkdir()
            elif label == 'root_symlink':
                linked = temporary / 'root_link'; linked.symlink_to(copied, target_is_directory=True); copied = linked
            else:
                names = {'changed_author_file': 'packet/README.md', 'changed_author_manifest': 'packet/MANIFEST.json',
                         'changed_audit_manifest': 'independent-audit/AUDIT_MANIFEST.json',
                         'changed_publication_manifest': 'PUBLICATION_MANIFEST.json',
                         'changed_audit_archive': 'rank670-independent-audit.zip', 'changed_audit_file': 'independent-audit/AUDIT.md'}
                with (copied / names[label]).open('ab') as stream:
                    stream.write(b'\n')
            rejected = False
            try:
                integrity(copied)
            except (ValueError, OSError, zipfile.BadZipFile):
                rejected = True
            require(rejected, 'Corruption control accepted: ' + label)
            results.append({'mutation': label, 'rejected': True})
    return {'intact_accepted': True, 'rejected': len(results), 'controls': results}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--integrity-only', action='store_true')
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    root = Path(__file__).absolute().parent
    result = {'integrity': integrity(root)}
    # The historical audit invokes author scripts without -I; remove inherited optimization explicitly.
    os.environ.pop('PYTHONOPTIMIZE', None)
    os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
    if not args.integrity_only:
        result['replay'] = replay(root)
    if args.self_test:
        result['negative_controls'] = self_test(root)
    result['scope'] = 'Integrity and finite guardrails only; original question remains unresolved.'
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
