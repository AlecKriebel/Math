#!/usr/bin/env python3
"""Independent, offline replay of the exact reviewed percolation reader archive.

Usage: python3 -I -B replay_package_review.py PATH_TO_PUBLIC_ARCHIVE
Prints verification metadata; writes only to temporary directories.
This packaging review is not an additional mathematical research pass.
"""
import argparse
import ast
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
from fractions import Fraction
from pathlib import Path, PurePosixPath

ARCHIVE_SHA256 = 'b56864bab1cb4877015e51c47c2c88e59969fae12f17f284df413f586500fa12'
ARCHIVE_BYTES = 63024
MANIFEST_SHA256 = '251ddc64465a0e7f7378fb99a955c967e9294f5194f4ccddfca5408fa5ccfab3'
MANIFEST_BYTES = 6852
ANCHORS = {
    'pass1_construction/CONSTRUCTION_PROOF.md': '731c8569a73f275c857991a4f97b47ee6debc2d3d46bb2399134021f65804f60',
    'pass1_audit/INDEPENDENT_ACCEPTANCE.md': '81844f28b60e4976fcdbfa2f47e4518c3baa94df37a4d1a435099f5821893f40',
    'pass1_validation/validate_construction.py': 'b43bbff8c330525f385b202711acc528a44ef405e217625682fa6c9415acb9b5',
    'pass1_validation/validation_report.json': '699ccdc94cddbd0d7d7b5de549c6c2da6a926cb9b0264fd8e451603f7959a633',
}
MODES = [('normal', []), ('optimized', ['-O']), ('double_optimized', ['-OO'])]

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def canonical(data):
    return (json.dumps(data, indent=2, sort_keys=True) + '\n').encode()

def run(root, script, flags=(), args=()):
    result = subprocess.run([sys.executable, '-I', '-B', *flags, str(root / script), *args],
                            cwd=root, capture_output=True, timeout=240)
    return result

def snapshot(root):
    return {p.relative_to(root).as_posix(): digest(p.read_bytes())
            for p in root.rglob('*') if p.is_file()}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('archive', type=Path)
    args = parser.parse_args()
    archive = args.archive.read_bytes()
    require(len(archive) == ARCHIVE_BYTES and digest(archive) == ARCHIVE_SHA256,
            'Archive differs from the independently reviewed identity')
    require(archive[:2] == b'\x1f\x8b' and archive[4:8] == b'\0' * 4,
            'Unexpected gzip format or timestamp')
    with tempfile.TemporaryDirectory(prefix='percolation-independent-review-') as temp:
        base = Path(temp)
        root = base / 'baseline' / 'public'
        with tarfile.open(fileobj=io.BytesIO(archive), mode='r:gz') as tar:
            members = tar.getmembers()
            names = [m.name for m in members]
            require(names == sorted(set(names)), 'Duplicate or unsorted archive members')
            require(len(names) == 35, 'Wrong archive member count')
            for member in members:
                path = PurePosixPath(member.name)
                require(member.isfile() and len(path.parts) > 1 and path.parts[0] == 'public'
                        and not path.is_absolute() and '..' not in path.parts
                        and str(path) == member.name and '\\' not in member.name,
                        'Unsafe archive member')
                require(member.uid == member.gid == member.mtime == 0 and member.mode == 0o444,
                        'Unexpected archive ownership, timestamp, or mode')
                require(not member.uname and not member.gname, 'Unexpected archive owner names')
                data = tar.extractfile(member).read()
                require(len(data) == member.size, 'Archive member byte count mismatch')
                target = root.parent / member.name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)
        manifest_raw = (root / 'MANIFEST.json').read_bytes()
        require(len(manifest_raw) == MANIFEST_BYTES and digest(manifest_raw) == MANIFEST_SHA256,
                'Manifest differs from the independently reviewed identity')
        manifest = json.loads(manifest_raw)
        require(canonical(manifest) == manifest_raw, 'Manifest encoding is not canonical')
        rows = manifest['files']
        paths = [row['path'] for row in rows]
        require(paths == sorted(set(paths)), 'Duplicate or unsorted manifest paths')
        require(set(snapshot(root)) == set(paths) | {'MANIFEST.json'}, 'Manifest/file-set mismatch')
        for row in rows:
            data = (root / row['path']).read_bytes()
            require(len(data) == row['bytes'] and digest(data) == row['sha256'],
                    'Manifest mismatch for ' + row['path'])
        for path, sha in ANCHORS.items():
            require(digest((root / path).read_bytes()) == sha, 'Accepted anchor changed: ' + path)
        identities = json.loads((root / 'ORIGINAL_IDENTITIES.json').read_bytes())['files']
        require(len(identities) == 22, 'Wrong original/public identity count')
        adapted = []
        for row in identities:
            data = (root / row['path']).read_bytes()
            require(len(data) == row['public_bytes'] and digest(data) == row['public_sha256'],
                    'Public identity mismatch: ' + row['path'])
            if row['original_sha256'] != row['public_sha256']:
                adapted.append(row['path'])
        require(sorted(adapted) == ['CONSTRUCTION_CONTRACT.md',
                'pass1_geometry/GEOMETRY_AND_ENDPOINT_AUDIT.md'], 'Unexpected adapted input')
        internal_links = 0
        external_urls = set()
        for p in root.rglob('*'):
            if not p.is_file():
                continue
            require(p.suffix in {'.md', '.json', '.py'}, 'Unexpected payload file type')
            text = p.read_text()
            external_urls.update(u.rstrip('.,;') for u in
                re.findall(r'https?://[^\s\)\]>"`]+', text))
            if p.suffix == '.md':
                for dest in re.findall(r'\[[^\]]*\]\(([^)]+)\)', text):
                    if dest.startswith(('https://', 'http://', '#')):
                        continue
                    local = (p.parent / dest.split('#')[0]).resolve()
                    require(local.is_relative_to(root.resolve()) and local.is_file(),
                            'Broken or escaping internal link: ' + dest)
                    internal_links += 1
        before = snapshot(root)
        for mode, flags in MODES:
            result = run(root, 'verify_package.py', flags, ['--manifest-sha256', MANIFEST_SHA256])
            require(result.returncode == 0 and not result.stderr, 'Pinned verifier failed: ' + mode)
        replay = run(root, 'run_checks.py')
        require(replay.returncode == 0 and not replay.stderr, 'Finite replay runner failed')
        replay_data = json.loads(replay.stdout)
        require(replay_data['execution_count'] == 6 and replay_data['status'] == 'PASS',
                'Unexpected finite replay result')
        require(replay.stdout == (root / 'CHECK_REPLAY.json').read_bytes(),
                'Finite replay metadata differs from retained result')
        tamper = run(root, 'check_tamper_controls.py')
        require(tamper.returncode == 0 and not tamper.stderr, 'Packaged tamper controls failed')
        tamper_data = json.loads(tamper.stdout)
        require(tamper_data['case_count'] == 15 and tamper_data['original_package_intact'],
                'Unexpected tamper result')
        require(tamper.stdout == (root / 'TAMPER_CONTROLS.json').read_bytes(),
                'Tamper metadata differs from retained result')
        extra_cases = ['negative_bytes', 'boolean_bytes', 'unsorted_paths', 'absolute_path',
                       'backslash_path', 'dot_component_path', 'symlink_directory',
                       'hidden_extra_file', 'coordinated_manifest_and_payload_change']
        extra = []
        for case in extra_cases:
            work = base / case
            shutil.copytree(root, work)
            path = work / 'MANIFEST.json'
            m = json.loads(path.read_bytes())
            if case == 'negative_bytes':
                m['files'][0]['bytes'] = -1
            elif case == 'boolean_bytes':
                m['files'][0]['bytes'] = True
            elif case == 'unsorted_paths':
                m['files'].reverse()
            elif case == 'absolute_path':
                m['files'][0]['path'] = '/outside'
            elif case == 'backslash_path':
                m['files'][0]['path'] = 'folder\\file'
            elif case == 'dot_component_path':
                m['files'][0]['path'] = './' + m['files'][0]['path']
            elif case == 'symlink_directory':
                (work / 'extra').symlink_to('pass1_audit', target_is_directory=True)
            elif case == 'hidden_extra_file':
                (work / '.hidden').write_bytes(b'{}')
            elif case == 'coordinated_manifest_and_payload_change':
                target = work / 'README.md'
                target.write_bytes(target.read_bytes() + b'\nChanged.\n')
                row = next(x for x in m['files'] if x['path'] == 'README.md')
                row['bytes'] = target.stat().st_size
                row['sha256'] = digest(target.read_bytes())
            path.write_bytes(canonical(m))
            pinned = case == 'coordinated_manifest_and_payload_change'
            if pinned:
                require(run(work, 'verify_package.py').returncode == 0,
                        'Coordinated control must demonstrate internal hashing limitation')
            for mode, flags in MODES:
                arguments = ['--manifest-sha256', MANIFEST_SHA256] if pinned else []
                result = run(work, 'verify_package.py', flags, arguments)
                require(result.returncode != 0, 'Independent tamper accepted: ' + case + ' ' + mode)
            extra.append({'case': case, 'rejected_in_all_three_modes': True,
                          'external_pin_required_for_this_control': pinned})
        require(before == snapshot(root), 'Isolated baseline was modified')
        bridge = Fraction(8, 3) * Fraction(3, 32) ** 4 / (1 - Fraction(3, 32)) ** 2
        survival = 1 - Fraction(4, 3) * (Fraction(3, 10) / (1 - Fraction(3, 10)) ** 2
                                       - Fraction(3, 10))
        lower = survival ** 2 * (1 - bridge)
        require(bridge == Fraction(27, 107648) and survival == Fraction(143, 245)
                and lower == Fraction(2200741829, 6461571200) and lower > Fraction(1, 3),
                'Independent rational recomputation failed')
        print(json.dumps({'status': 'PASS', 'mathematical_passes_added': 0,
            'archive_bytes': ARCHIVE_BYTES, 'archive_sha256': ARCHIVE_SHA256,
            'manifest_bytes': MANIFEST_BYTES, 'manifest_sha256': MANIFEST_SHA256,
            'payload_files': len(names), 'original_public_identity_pairs': len(identities),
            'adapted_inputs': sorted(adapted), 'internal_links_checked': internal_links,
            'unique_external_urls': len(external_urls), 'pinned_verifier_modes': 3,
            'finite_checker_executions': 6, 'packaged_tamper_cases': 15,
            'packaged_tamper_verifier_runs': 45, 'independent_tamper_cases': extra,
            'independent_tamper_verifier_runs': 27,
            'baseline_tree_unchanged': True, 'independent_rational_constants_match': True,
            'finite_replay_metadata_sha256': digest(replay.stdout),
            'tamper_replay_metadata_sha256': digest(tamper.stdout)}, indent=2, sort_keys=True))

if __name__ == '__main__':
    main()
