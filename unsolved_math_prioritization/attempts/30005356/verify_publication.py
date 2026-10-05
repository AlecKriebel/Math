#!/usr/bin/env python3
"""Strict offline publication inventory and replay; finite checks are not proof."""
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import stat
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parent
PINS = [
    ('author', 'GENERIC_ENDOMORPHISMS_30005356_AUTHOR_SAFE_FREEZE.zip', 16791,
     'b5d4c852204b60d7a91cfa0d1c6125bd9deac64d460fc1a0f49a196df01a9d96',
     '6766c7778f334090cb84e86246331fced277d8a62e6469263c8adbfc8cd76cdb', 9),
    ('independent_audit', 'GENERIC_ENDOMORPHISMS_30005356_INDEPENDENT_AUDIT_PASS.zip', 19761,
     'bc7212bad569fe9ee00330ae9fbdc0c17dad7dd645e0da8ebf91dbb1a93fb681',
     '16c07b61037df2833520d9c5dd2c6cfdf6f178ee193a2bdafeb1d4e19453e6ea', 10),
]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def regular_files(root):
    result = set()
    for path in root.rglob('*'):
        require(not path.is_symlink(), 'Symlink: ' + str(path))
        if path.is_file():
            result.add(path.relative_to(root).as_posix())
        else:
            require(path.is_dir(), 'Nonregular filesystem entry')
    return result


def safe_path(name):
    p = PurePosixPath(name)
    require(bool(name) and not p.is_absolute() and '..' not in p.parts
            and '.' not in p.parts and str(p) == name and '\\' not in name,
            'Unsafe path: ' + name)


def check_manifest(root, manifest_name):
    manifest = json.loads((root / manifest_name).read_text())
    entries = manifest['files']
    names = [entry['path'] for entry in entries]
    require(len(names) == len(set(names)), 'Repeated manifest path')
    require(manifest_name not in names, 'Self-referential manifest')
    for entry in entries:
        safe_path(entry['path'])
        data = (root / entry['path']).read_bytes()
        require(len(data) == entry['bytes'] and sha(data) == entry['sha256'],
                'Manifest mismatch: ' + entry['path'])
    require(regular_files(root) == set(names) | {manifest_name}, 'Unexpected or missing file')
    expected_dirs = {str(parent) for name in names for parent in PurePosixPath(name).parents
                     if str(parent) != '.'}
    actual_dirs = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_dir()}
    require(actual_dirs == expected_dirs, 'Unexpected or missing directory')
    return len(names)


def replay(folder):
    commands = [('verify_manifest.py',)]
    if folder.name == 'author':
        commands.append(('verify_math.py', '--check', 'CHECK_RESULTS.json'))
    else:
        commands.append(('independent_controls.py', '--check', 'INDEPENDENT_RESULTS.json'))
    env = os.environ.copy()
    env.pop('PYTHONOPTIMIZE', None)
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    probe = subprocess.run([sys.executable, '-B', '-c', 'print(__debug__)'],
                           env=env, text=True, capture_output=True, check=True)
    require(probe.stdout.strip() == 'True', 'Child assertions disabled')
    outputs = []
    for command in commands:
        result = subprocess.run([sys.executable, '-B', *command], cwd=folder, env=env,
                                text=True, capture_output=True, check=True)
        outputs.append({'command': 'python3 ' + ' '.join(command), 'exit_code': result.returncode,
                        'stdout': result.stdout.strip(), 'assertions_active': True})
    return outputs


def main():
    require(__debug__, 'Run without -O: mathematical assertion checks must remain active')
    count = check_manifest(ROOT, 'PUBLICATION_MANIFEST.json')
    status = json.loads((ROOT / 'PUBLICATION_STATUS.json').read_text())
    require(status['problem_id'] == 30005356 and status['rank'] == 778, 'Wrong target')
    require(status['status'] == 'claimed_solved' and status['turns'] == '1/5', 'Wrong disposition')
    require(status['independent_AI_audit'] == 'PASS', 'Wrong audit disposition')
    require(status['characteristic_zero_classification'] == 'OPEN'
            and status['localized_Z_1_over_p_theta_classification'] == 'OPEN', 'Scope widened')
    require(not status['human_peer_review'] and not status['editorial_acceptance_claim']
            and not status['formal_proof_assistant_verification'], 'Review status overstated')
    require(status['review_hash'] == '00c719d497159151748580b116c2a138f20956fbd106b60808c144bf4ca63de8',
            'Catalogue review hash mismatch')
    results = []
    with tempfile.TemporaryDirectory(prefix='generic-field-replay-') as temporary:
        for folder, archive, size, ah, mh, files in PINS:
            archive_path = ROOT / archive
            data = archive_path.read_bytes()
            require(len(data) == size and sha(data) == ah, 'Frozen archive changed')
            directory = ROOT / folder
            require(sha((directory / 'MANIFEST.json').read_bytes()) == mh, 'Frozen manifest changed')
            require(check_manifest(directory, 'MANIFEST.json') + 1 == files, 'Frozen file count changed')
            extracted = Path(temporary) / folder
            extracted.mkdir()
            with zipfile.ZipFile(archive_path) as z:
                entries = z.infolist()
                names = [entry.filename for entry in entries]
                require(len(names) == len(set(names)) == files, 'ZIP member count mismatch')
                require(set(names) == regular_files(directory), 'ZIP member inventory mismatch')
                for entry in entries:
                    safe_path(entry.filename)
                    require('/' not in entry.filename and not entry.is_dir()
                            and not stat.S_ISLNK(entry.external_attr >> 16), 'Unsafe ZIP member')
                    content = z.read(entry)
                    require(content == (directory / entry.filename).read_bytes(), 'ZIP bytes differ')
                    (extracted / entry.filename).write_bytes(content)
            normal = replay(directory)
            clean_zip = replay(extracted)
            results.append({'directory': folder, 'archive_sha256': ah,
                            'manifest_sha256': mh, 'files': files,
                            'normal_replay': normal, 'clean_zip_replay': clean_zip})
    require(check_manifest(ROOT, 'PUBLICATION_MANIFEST.json') == count, 'Replay modified package')
    print(json.dumps({'status': 'PASS', 'problem_id': 30005356, 'files_including_manifest': count + 1,
                      'assertions_active': True, 'closed_recursive_inventory': True,
                      'source_inputs_required_for_offline_replay': False, 'results': results,
                      'limitation': 'Integrity and finite controls; written proofs require mathematical review.'},
                     indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
