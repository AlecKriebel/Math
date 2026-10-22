#!/usr/bin/env python3
"""Mandatory recursive integrity and exact replay of the accepted 2809 packet."""
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

ROOT = Path(__file__).resolve().parent
ARCHIVES = {
    'KIRBY_MERIDIAN_2809_AUTHOR_SAFE_FREEZE.zip': ('kirby_meridian_2809', '14809993ffccbb97cc3510d7a17df91ad375bc85cf02bd6a9c430c31c12673c3'),
    'KIRBY_MERIDIAN_2809_INDEPENDENT_AUDIT.zip': ('kirby_meridian_2809_independent_audit', '79c4abdd006d1a1fcd5d917fec9984c82fc30ca4864f4c17f76ef461e927cb8f'),
    'KIRBY_MERIDIAN_2809_V2_SAFE_FREEZE.zip': ('kirby_meridian_2809_v2', 'e37dc6bdf5c5b0f5f1547e9d9db0225034fe403682770b59bc254c99140b01a0'),
    'KIRBY_MERIDIAN_2809_V2_DELTA_AUDIT.zip': ('kirby_meridian_2809_v2_delta_audit', '4f41bfb692e9fee556e7128f2d3c079c3412c0e49c2ead24304f2eeb5e1f1118'),
}

def need(condition, message):
    if not condition:
        raise RuntimeError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def inventory(root):
    result = {}
    for p in root.rglob('*'):
        need(not p.is_symlink(), 'Symlink rejected: ' + str(p))
        need(p.is_dir() or p.is_file(), 'Nonregular member rejected: ' + str(p))
        if p.is_file():
            result[p.relative_to(root).as_posix()] = p.read_bytes()
    return result

def manifest(root, filename):
    actual = inventory(root)
    need(filename in actual, 'Mandatory manifest missing: ' + filename)
    entries = json.loads(actual[filename])['files']
    expected = set()
    for item in entries:
        name = item['path']
        path = PurePosixPath(name)
        need(name == path.as_posix() and not path.is_absolute() and '..' not in path.parts and name != filename, 'Unsafe manifest path')
        need(name not in expected, 'Duplicate manifest path')
        expected.add(name)
    need(set(actual) == expected | {filename}, 'Complete recursive inventory mismatch: ' + str(root))
    for item in entries:
        data = actual[item['path']]
        need(len(data) == item['bytes'] and sha(data) == item['sha256'], 'Manifest hash mismatch: ' + item['path'])
    return actual

def run(script, optimized, *args):
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    env.pop('PYTHONOPTIMIZE', None)
    command = [sys.executable, '-B', *(['-O'] if optimized else []), str(script), *map(str, args)]
    with tempfile.TemporaryDirectory(prefix='meridian-unrelated-cwd-') as cwd:
        p = subprocess.run(command, cwd=cwd, env=env, capture_output=True, timeout=120)
    need(p.returncode == 0, str(script) + ' failed: ' + p.stderr.decode(errors='replace'))
    return p.stdout

def main():
    members = manifest(ROOT, 'PUBLICATION_MANIFEST.json')
    for filename, (directory, pinned) in ARCHIVES.items():
        archive = ROOT/'archives'/filename
        need(sha(archive.read_bytes()) == pinned, 'Archive pin mismatch: ' + filename)
        extracted = manifest(ROOT/directory/'safe', 'MANIFEST.json')
        with zipfile.ZipFile(archive) as z:
            entries = z.infolist()
            names = [e.filename for e in entries]
            need(len(names) == len(set(names)), 'Duplicate ZIP member')
            need(z.testzip() is None, 'ZIP CRC mismatch')
            need(set(names) == {directory + '/' + n for n in extracted}, 'Exact ZIP inventory mismatch')
            for e in entries:
                path = PurePosixPath(e.filename)
                need(len(path.parts) == 2 and path.parts[0] == directory and '..' not in path.parts and not path.is_absolute(), 'Unsafe ZIP path')
                kind = stat.S_IFMT(e.external_attr >> 16)
                need(not e.is_dir() and kind in (0, stat.S_IFREG), 'Nonregular ZIP member')
                need(z.read(e) == extracted[path.name], 'ZIP/extracted bytes mismatch')
    original = ROOT/'kirby_meridian_2809'/'safe'
    author = ROOT/'kirby_meridian_2809_v2'/'safe'
    audit = ROOT/'kirby_meridian_2809_independent_audit'/'safe'
    accepted = ROOT/'kirby_meridian_2809_v2_delta_audit'/'safe'
    decision = json.loads((accepted/'ACCEPTANCE.json').read_bytes())
    need(decision['decision'] == 'ACCEPT_EXACT_V2_AS_CORRECTED_SCOPED_UNRESOLVED_RECORD' and not decision['mandatory_corrections_remaining'], 'Acceptance decision mismatch')
    need(decision['v2_zip']['sha256'] == ARCHIVES['KIRBY_MERIDIAN_2809_V2_SAFE_FREEZE.zip'][1], 'Accepted archive differs')
    need((original/'RESULTS.json').read_bytes() == (author/'RESULTS.json').read_bytes(), 'Historical results changed')
    replays = []
    with tempfile.TemporaryDirectory(prefix='meridian-complete-inputs-') as tmp:
        inputs = Path(tmp)
        for p in (ROOT/'archives').iterdir():
            shutil.copyfile(p, inputs/p.name)
        for directory, _ in ARCHIVES.values():
            shutil.copytree(ROOT/directory, inputs/directory)
        for optimized in (False, True):
            for folder in (original, author):
                need(run(folder/'verify.py', optimized) == (folder/'RESULTS.json').read_bytes(), 'Author output mismatch')
            need(run(audit/'independent_controls.py', optimized) == (audit/'INDEPENDENT_RESULTS.json').read_bytes(), 'Independent output mismatch')
            run(audit/'verify_audit.py', optimized)
            run(accepted/'verify_package.py', optimized)
            packet = run(audit/'audit_packet.py', optimized, ROOT/'archives'/'KIRBY_MERIDIAN_2809_AUTHOR_SAFE_FREEZE.zip', '--author-directory', original)
            need(packet == (audit/'PACKET_RESULTS.json').read_bytes(), 'Original packet replay mismatch')
            delta = run(accepted/'verify_delta.py', optimized, inputs)
            need(delta == (accepted/'DELTA_RESULTS.json').read_bytes(), 'Exact delta replay mismatch')
            replays.append({'optimized': optimized, 'author_checks': 10768, 'independent_supplementary_checks': 3399, 'all_saved_outputs_byte_identical': True, 'integrity_mutations_rejected': 8, 'semantic_mutations_rejected': 12})
    need(members == inventory(ROOT), 'Publication files changed during replay')
    print(json.dumps({'ok': True, 'problem_id': 2809, 'status': 'unsolved', 'turns': '5/5', 'new_proof_attempts': 0, 'publication_files': len(members), 'immutable_zip_archives': len(ARCHIVES), 'recursive_inventory_and_manifests': 'PASS', 'exact_v2_patch_reconstruction': 'PASS', 'replays': replays}, indent=2, sort_keys=True))

if __name__ == '__main__':
    main()
