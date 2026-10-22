"""Externally authenticate this file before execution. Standard library only."""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.flags.dont_write_bytecode):
    raise SystemExit('REFUSED: Python -I -S -B required')
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import tempfile
import zipfile

PINS = {
    'STRINGY_30002042_AUTHOR_SAFE_FREEZE.zip': (13660, '3e77fa2a11514444ea34bbee9ebd9096cbf313749d22dd4c7afc21060ef4218b'),
    'STRINGY_30002042_AUTHOR_EXTERNAL_MANIFEST.json': (1123, '7ed84eb3615eba0c2a413e3a7653e7a826312171aff1f61666c67d614b06503f'),
    'STRINGY_30002042_AUTHOR_BOOTSTRAP.py': (4427, '303c8a3f91db4cafd7a73504357ac1c90170bdee17635f8222498462fb3f2d7c'),
    'STRINGY_30002042_INDEPENDENT_AUDIT_SAFE.zip': (22832, '8de29301c48759449c5c91e3d75729c0f06b5b4955a6f1706b0573ec904102d0'),
    'STRINGY_30002042_INDEPENDENT_AUDIT_EXTERNAL_MANIFEST.json': (1774, '78ad637f5d2ea1f458c9187e588ccc40aed694a921cddb0f5ff72ffd095a5e64'),
}

def need(ok, why):
    if not ok: raise ValueError(why)

def sha(b): return hashlib.sha256(b).hexdigest()

def unique(pairs):
    d = {}
    for k, v in pairs:
        need(k not in d, 'duplicate JSON key')
        d[k] = v
    return d

def parse(b): return json.loads(b, object_pairs_hook=unique)

def safe_path(p):
    p = Path(os.path.abspath(p))
    for ancestor in [p] + list(p.parents):
        need(not ancestor.is_symlink(), 'symlink path or ancestor')
    return p

def regular(p):
    safe_path(p)
    need(stat.S_ISREG(p.lstat().st_mode), 'nonregular file')
    need(p.stat().st_size < 2000000, 'file size ceiling')
    return p.read_bytes()

def verify(root, manifest_pin):
    root = safe_path(root)
    own = safe_path(__file__)
    need(own == root / 'publication_bootstrap.py', 'wrong operative entrypoint')
    need(stat.S_ISDIR(root.lstat().st_mode), 'non-directory root')
    mb = regular(root / 'PUBLICATION_MANIFEST.json')
    need(re.fullmatch('[0-9a-f]{64}', manifest_pin) is not None and sha(mb) == manifest_pin, 'external manifest pin mismatch')
    manifest = parse(mb)
    need(type(manifest) is dict and set(manifest) == {'schema', 'problem_id', 'files'}, 'manifest schema')
    need(type(manifest['schema']) is int and manifest['schema'] == 1, 'manifest version')
    need(type(manifest['problem_id']) is int and manifest['problem_id'] == 30002042, 'problem identity')
    entries = manifest['files']
    need(type(entries) is dict and entries, 'manifest entries')
    expected_dirs = set()
    for name, item in entries.items():
        path = PurePosixPath(name)
        need(type(name) is str and str(path) == name and not path.is_absolute() and '..' not in path.parts and '\\' not in name, 'unsafe manifest path')
        need(type(item) is dict and set(item) == {'bytes', 'sha256'}, 'entry schema')
        need(type(item['bytes']) is int and 0 <= item['bytes'] < 2000000, 'entry size')
        need(type(item['sha256']) is str and re.fullmatch('[0-9a-f]{64}', item['sha256']) is not None, 'entry digest')
        expected_dirs.update(str(p) for p in path.parents if str(p) != '.')
    files, dirs = set(), set()
    for base, names, fs in os.walk(root, followlinks=False):
        for name in names:
            p = Path(base) / name
            need(not p.is_symlink() and stat.S_ISDIR(p.lstat().st_mode), 'nonregular directory')
            dirs.add(str(p.relative_to(root)))
        for name in fs:
            p = Path(base) / name
            need(not p.is_symlink() and stat.S_ISREG(p.lstat().st_mode), 'nonregular inventory entry')
            files.add(str(p.relative_to(root)))
    need(files == set(entries) | {'PUBLICATION_MANIFEST.json'} and dirs == expected_dirs, 'strict package inventory')
    payload = {}
    for name, item in entries.items():
        b = regular(root / name)
        need(item == {'bytes': len(b), 'sha256': sha(b)}, 'package byte mismatch: ' + name)
        payload[name] = b
    for name, pin in PINS.items():
        b = payload[name]
        need((len(b), sha(b)) == pin, 'immutable input pin: ' + name)
    member_count = 0
    for folder, prefix in [('author', 'STRINGY_30002042_AUTHOR'), ('audit', 'STRINGY_30002042_INDEPENDENT_AUDIT')]:
        zname = prefix + ('_SAFE_FREEZE.zip' if folder == 'author' else '_SAFE.zip')
        m = parse(payload[prefix + '_EXTERNAL_MANIFEST.json'])['files']
        with zipfile.ZipFile(io.BytesIO(payload[zname])) as z:
            infos = z.infolist()
            need(len(infos) == len(m) and {i.filename for i in infos} == set(m), 'archive inventory')
            for i in infos:
                need(i.create_system == 3 and stat.S_ISREG(i.external_attr >> 16) and not i.is_dir() and not i.flag_bits & 1, 'archive member type')
                need('/' not in i.filename and '\\' not in i.filename and i.filename not in ('.', '..'), 'archive path')
                b = z.read(i)
                need(m[i.filename] == {'bytes': len(b), 'sha256': sha(b)} and i.file_size == len(b), 'archive member binding')
                need(payload[folder + '/' + i.filename] == b, 'extracted member mismatch')
                member_count += 1
    acceptance = parse(payload['audit/ACCEPTANCE.json'])
    need(acceptance['overall'] == 'unsolved_by_this_attempt' and acceptance['approaches_used'] == 5 and acceptance['full_solution'] is False, 'acceptance scope')
    need(acceptance['correction_required'] is False and acceptance['general_finiteness_proved'] is False, 'correction scope')
    a = parse(payload['author/SOURCES.json'])['sources']
    b = parse(payload['audit/SOURCE_BYTE_CHECKS.json'])['records']
    need(len(a) == len(b) == 7, 'source count')
    for x, y in zip(a, b):
        need((x['id'], x['bytes'], x['sha256'], x['public_url']) == (y['id'], y['bytes'], y['sha256'], y['url']), 'source metadata binding')
    return root, payload, {'verified': True, 'problem_id': 30002042, 'package_files': len(files), 'archive_members': member_count, 'source_metadata_matches': 7, 'overall': 'unsolved_by_this_attempt', 'turns': '5/5'}

def replay(root, payload):
    results = []
    with tempfile.TemporaryDirectory(prefix='stringy-publication-') as td:
        for optimized in (False, True):
            flags = [sys.executable, '-I', '-S', '-B'] + (['-O'] if optimized else [])
            for script, extra, expected in [
                ('STRINGY_30002042_AUTHOR_BOOTSTRAP.py', ['STRINGY_30002042_AUTHOR_SAFE_FREEZE.zip', 'STRINGY_30002042_AUTHOR_EXTERNAL_MANIFEST.json'], None),
                ('audit/independent_math.py', [], 'audit/MATH_' + ('OPTIMIZED' if optimized else 'NORMAL') + '.json'),
                ('audit/replay_controls.py', ['STRINGY_30002042_AUTHOR_BOOTSTRAP.py', 'STRINGY_30002042_AUTHOR_SAFE_FREEZE.zip', 'STRINGY_30002042_AUTHOR_EXTERNAL_MANIFEST.json'], 'audit/REPLAY_' + ('OPTIMIZED' if optimized else 'NORMAL') + '.json'),
            ]:
                run = subprocess.run(flags + ['-c', payload[script].decode()] + [str(root / x) for x in extra], cwd=td, capture_output=True, text=True, timeout=180)
                need(run.returncode == 0 and run.stderr == '', 'authenticated replay failed: ' + script + ': ' + run.stderr)
                got = parse(run.stdout)
                if expected: need(got == parse(payload[expected]), 'saved replay mismatch: ' + script)
                if 'independent_math' in script: need(got['independent_checks'] == 4795, 'independent check count')
                if 'replay_controls' in script: need((got['positive_runs'], got['negative_runs'], len(got['structure_layer_controls'])) == (6, 36, 14), 'review control counts')
                results.append({'script': script, 'optimized': optimized, 'saved_expected_match': bool(expected), 'result': got})
    return results

def main():
    need(len(sys.argv) in (3, 4) and (len(sys.argv) == 3 or sys.argv[3] == '--replay'), 'usage: publication_bootstrap.py ROOT MANIFEST_SHA256 [--replay]')
    root, payload, result = verify(sys.argv[1], sys.argv[2])
    if len(sys.argv) == 4:
        result['replays'] = replay(root, payload)
        again = verify(root, sys.argv[2])
        need(again[1] == payload, 'post-replay bytes changed')
    print(json.dumps(result, sort_keys=True, indent=2))

if __name__ == '__main__':
    try: main()
    except (ValueError, OSError, TypeError, KeyError, zipfile.BadZipFile, subprocess.TimeoutExpired) as e:
        print('PUBLICATION VERIFICATION FAILED: ' + str(e), file=sys.stderr)
        sys.exit(1)
