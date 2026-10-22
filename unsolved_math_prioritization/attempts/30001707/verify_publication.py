#!/usr/bin/env python3
"""Externally pinned, isolated publication verifier; trusted runtime required."""
import sys
if not (sys.flags.isolated and sys.flags.no_site):
    sys.stderr.write('ISOLATED STARTUP REQUIRED: python -I -S -B verify_publication.py TRUSTED_MANIFEST_SHA256 [--full]\n')
    sys.exit(2)
import hashlib
import json
from pathlib import Path
import shutil
import stat
import subprocess
import tempfile
import zipfile

ROOT = Path(__file__).absolute().parent
BOOTSTRAP_SHA = '38a043f47a90d1a7dcb2e59adc5c187be0e5ac04cc65a5584ddc2152693810fd'
MANIFEST_SHA = 'fa1046d7262b9682a98007bc12ad2b33de095e692dc3ee8e94b0f77e39f1bb30'
COUNTS = {'original_control_runners': 4, 'original_shadow_exploits': 2,
          'corrected_positive_replays': 8, 'independent_hostile_controls': 58,
          'independent_archive_controls': 10}

def need(ok, message):
    if not ok:
        raise ValueError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def unique(pairs):
    out = {}
    for key, value in pairs:
        need(key not in out, 'duplicate JSON key')
        out[key] = value
    return out

def read_json(path):
    return json.loads(path.read_bytes(), object_pairs_hook=unique)

def inventory(root):
    need(stat.S_ISDIR(root.lstat().st_mode), 'root must be a nonsymlink directory')
    files, dirs = set(), set()
    def visit(path):
        for p in path.iterdir():
            mode = p.lstat().st_mode
            name = p.relative_to(root).as_posix()
            if stat.S_ISDIR(mode):
                dirs.add(name)
                visit(p)
            else:
                need(stat.S_ISREG(mode), 'nonregular publication node: ' + name)
                files.add(name)
    visit(root)
    return files, dirs

def validate(pin):
    need(stat.S_ISREG(Path(__file__).absolute().lstat().st_mode), 'entry point symlink')
    files, dirs = inventory(ROOT)
    manifest = ROOT / 'PUBLICATION_MANIFEST.json'
    need('PUBLICATION_MANIFEST.json' in files, 'missing publication manifest')
    raw = manifest.read_bytes()
    need(len(pin) == 64 and sha(raw) == pin, 'untrusted publication manifest')
    seal = json.loads(raw, object_pairs_hook=unique)
    need(type(seal) is dict and set(seal) == {'schema', 'problem_id', 'files'}, 'publication manifest schema')
    need(type(seal['schema']) is int and seal['schema'] == 1 and type(seal['problem_id']) is int and seal['problem_id'] == 30001707, 'publication identity')
    expected = seal['files']
    need(type(expected) is dict, 'manifest inventory type')
    need(files == set(expected) | {'PUBLICATION_MANIFEST.json'}, 'unexpected/missing publication file')
    expected_dirs = set()
    for name, entry in expected.items():
        path = Path(name)
        need(not path.is_absolute() and name == path.as_posix() and '..' not in path.parts and '\\' not in name, 'unsafe manifest path')
        expected_dirs.update(p.as_posix() for p in path.parents if str(p) != '.')
        need(type(entry) is dict and set(entry) == {'bytes', 'sha256'} and type(entry['bytes']) is int, 'member schema')
        raw = (ROOT / name).read_bytes()
        need(len(raw) == entry['bytes'] and sha(raw) == entry['sha256'], 'publication member mismatch: ' + name)
    need(dirs == expected_dirs, 'unexpected/missing directory')
    need(sha((ROOT / 'audit/ISOLATED_VERIFY.py').read_bytes()) == BOOTSTRAP_SHA, 'isolated entry-point pin')
    need(sha((ROOT / 'audit/CORRECTED_EXTERNAL_MANIFEST.json').read_bytes()) == MANIFEST_SHA, 'corrected manifest pin')
    return len(files)

def check_archives():
    results = []
    metadata = read_json(ROOT / 'PUBLICATION_METADATA.json')
    for a in metadata['archives']:
        archive = ROOT / 'archives' / a['filename']
        raw = archive.read_bytes()
        need(len(raw) == a['bytes'] and sha(raw) == a['sha256'], 'archive pin')
        m = a['manifest']
        manifest = ROOT / 'manifests' / m['filename']
        raw = manifest.read_bytes()
        need(len(raw) == m['bytes'] and sha(raw) == m['sha256'], 'external manifest pin')
        seal = read_json(manifest)['files']
        with zipfile.ZipFile(archive) as z:
            members = z.infolist()
            names = [i.filename for i in members]
            need(len(names) == len(set(names)) and set(names) == set(seal), 'ZIP inventory')
            for info in members:
                name = info.filename
                path = Path(name)
                need(not path.is_absolute() and '..' not in path.parts and name == path.as_posix() and '\\' not in name, 'ZIP path')
                need(stat.S_ISREG(info.external_attr >> 16) and not info.flag_bits & 1, 'ZIP type/encryption')
                b = z.read(info)
                need(len(b) == seal[name]['bytes'] and sha(b) == seal[name]['sha256'], 'ZIP member pin')
                need(b == (ROOT / a['role'] / name).read_bytes(), 'ZIP / extracted mismatch')
        results.append({'role': a['role'], 'members': len(seal), 'sha256': a['sha256'], 'exact': True})
    for p in (ROOT / 'corrected').iterdir():
        need(p.read_bytes() == (ROOT / 'audit/corrected' / p.name).read_bytes(), 'corrected copies differ')
    return results

def call(script, *args):
    flags = ['-I', '-S', '-B'] + (['-O'] if sys.flags.optimize else [])
    r = subprocess.run([sys.executable] + flags + [str(script)] + [str(a) for a in args],
                       cwd='/tmp', capture_output=True, text=True, timeout=600, check=False)
    need(r.returncode == 0 and not r.stderr, 'authenticated replay failed: ' + r.stderr)
    return json.loads(r.stdout, object_pairs_hook=unique)

def main():
    need(len(sys.argv) in (2, 3) and (len(sys.argv) == 2 or sys.argv[2] == '--full'), 'usage: TRUSTED_MANIFEST_SHA256 [--full]')
    pin = sys.argv[1]
    count = validate(pin)
    archives = check_archives()
    output = {'accepted': True, 'isolated_startup': True, 'all_members_authenticated_before_execution': True,
              'files': count, 'archives': archives, 'original_execution_boundary': 'historically vulnerable; not fail-closed',
              'scope': 'scoped partial / source correction; original conjecture unresolved; no novelty'}
    if len(sys.argv) == 3:
        cm = ROOT / 'manifests/MULTIPLICITY_FREE_30001707_CORRECTED_EXTERNAL_MANIFEST.json'
        output['corrected_bootstrap'] = call(ROOT / 'audit/ISOLATED_VERIFY.py', ROOT / 'corrected', cm)
        need(output['corrected_bootstrap']['accepted'] is True, 'bootstrap acceptance')
        with tempfile.TemporaryDirectory(prefix='multiplicity-publication-patch-') as tmp:
            work = Path(tmp) / 'applied'
            shutil.copytree(ROOT / 'original', work)
            result = subprocess.run(['patch', '--batch', '--fuzz=0', '-p1', '-i', str(ROOT / 'audit/AUTHOR_PATCH.diff')],
                                    cwd=work, capture_output=True, text=True, timeout=30, check=False)
            need(result.returncode == 0 and not result.stderr, 'actual patch application failed')
            need({p.name for p in work.iterdir()} == {p.name for p in (ROOT / 'corrected').iterdir()}, 'patched inventory')
            changed = []
            for p in work.iterdir():
                need(p.read_bytes() == (ROOT / 'corrected' / p.name).read_bytes(), 'patched derivative mismatch')
                if p.read_bytes() != (ROOT / 'original' / p.name).read_bytes():
                    changed.append(p.name)
            need(set(changed) == {'README.md', 'certificate.py', 'controls.py', 'verify.py'}, 'patch scope')
            replay = call(ROOT / 'audit/ISOLATED_VERIFY.py', work, cm)
            need(replay['accepted'] is True, 'patched bootstrap acceptance')
            output['actual_patch_application'] = {'applied': True, 'all_9_members_match': True, 'changed_files': sorted(changed), 'bootstrap': replay}
        acceptance = call(ROOT / 'audit/INDEPENDENT_TESTS.py', ROOT / 'archives/MULTIPLICITY_FREE_30001707_AUTHOR_SAFE_FREEZE.zip')
        need(acceptance['counts'] == COUNTS and acceptance['original_freeze_unchanged'] is True, 'independent acceptance counts')
        frozen = read_json(ROOT / ('audit/ACCEPTANCE_OPTIMIZED.json' if sys.flags.optimize else 'audit/ACCEPTANCE.json'))
        need(acceptance == frozen, 'independent acceptance differs from frozen record')
        output['independent_acceptance'] = {'matches_frozen_exactly': True, 'counts': acceptance['counts'],
                                           'math_checks': acceptance['independent_math_checks']}
    need(validate(pin) == count, 'post-replay identity')
    return output

if __name__ == '__main__':
    try:
        print(json.dumps(main(), sort_keys=True, indent=2))
    except (OSError, ValueError, KeyError, TypeError, subprocess.TimeoutExpired, zipfile.BadZipFile) as error:
        print('PUBLICATION REJECTED: ' + str(error), file=sys.stderr)
        sys.exit(1)
