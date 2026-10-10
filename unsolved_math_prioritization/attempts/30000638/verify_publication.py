#!/usr/bin/env python3
"""Check the complete anchored publication before optionally replaying its code."""
import sys
sys.dont_write_bytecode = True
from pathlib import Path, PurePosixPath
import argparse
import hashlib
import json
import shutil
import stat
import subprocess
import tempfile
import zipfile

def need(value, message):
    if not value:
        raise RuntimeError(message)

def identity(data):
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}

def unique(items):
    out = {}
    for key, value in items:
        need(key not in out, 'duplicate JSON key')
        out[key] = value
    return out

def read_json(path):
    return json.loads(path.read_text(), object_pairs_hook=unique)

def safe(name):
    p = PurePosixPath(name)
    need(name and not p.is_absolute() and '..' not in p.parts and str(p) == name,
         'unsafe relative path')
    return Path(*p.parts)

def inventory(root, names):
    expected_dirs = {str(p) for name in names for p in safe(name).parents if str(p) != '.'}
    actual_files, actual_dirs = set(), set()
    for path in root.rglob('*'):
        need(not path.is_symlink(), 'symlink in publication')
        rel = str(path.relative_to(root))
        if path.is_file():
            actual_files.add(rel)
        elif path.is_dir():
            actual_dirs.add(rel)
        else:
            raise RuntimeError('nonregular inventory member')
    need(actual_files == set(names), 'file inventory mismatch')
    need(actual_dirs == expected_dirs, 'directory inventory mismatch')

def frozen_manifest(root, name):
    m = read_json(root / name)
    inventory(root, set(m['files']) | {name})
    for rel, expected in m['files'].items():
        need(identity((root / safe(rel)).read_bytes()) == expected,
             'frozen manifest mismatch: ' + rel)

def verify(root):
    m = read_json(root / 'PUBLICATION_MANIFEST.json')
    need(m['schema'] == 1 and type(m['schema']) is int, 'manifest schema')
    need(m['gate'] == 'ACCEPT_CORRECTED_PARTIAL' and m['original_question'] == 'UNSOLVED',
         'publication overclaim')
    inventory(root, set(m['files']) | {'PUBLICATION_MANIFEST.json'})
    for rel, expected in m['files'].items():
        need(identity((root / safe(rel)).read_bytes()) == expected,
             'publication hash mismatch: ' + rel)
    provenance = read_json(root / 'PUBLICATION_PROVENANCE.json')
    need(provenance['gate'] == 'ACCEPT_CORRECTED_PARTIAL' and
         provenance['operative_verifier'] == 'corrected/verify.py', 'operative scope')
    count = 0
    for a in provenance['archives']:
        data = (root / safe(a['path'])).read_bytes()
        need(identity(data) == {k: a[k] for k in ('bytes', 'sha256')}, 'archive identity')
        target = root / safe(a['extracted_directory'])
        with zipfile.ZipFile(root / safe(a['path'])) as z:
            members = z.namelist()
            need(z.testzip() is None and len(members) == len(set(members)) == a['member_count'],
                 'archive CRC, duplicate or member count')
            expected = {a['archive_prefix'] + '/' + str(p.relative_to(target))
                        for p in target.rglob('*') if p.is_file()}
            need(set(members) == expected, 'archive member inventory')
            for info in z.infolist():
                rel = safe(info.filename)
                need(rel.parts[0] == a['archive_prefix'] and not info.is_dir() and
                     not stat.S_ISLNK(info.external_attr >> 16), 'unsafe archive entry')
                need(z.read(info.filename) == (target / Path(*rel.parts[1:])).read_bytes(),
                     'extracted archive bytes')
            count += len(members)
    for target in ('author', 'corrected', 'audit/author_freeze', 'audit/corrected'):
        frozen_manifest(root / target, 'MANIFEST.json')
    frozen_manifest(root / 'audit', 'AUDIT_MANIFEST.json')
    files = set(read_json(root / 'author/MANIFEST.json')['files']) | {'MANIFEST.json'}
    changed = sorted(name for name in files
                     if (root / 'author' / name).read_bytes() != (root / 'corrected' / name).read_bytes())
    need(changed == ['MANIFEST.json', 'verify.py'], 'derivative scope')
    for name in files:
        for original, nested in (('author', 'author_freeze'), ('corrected', 'corrected')):
            need((root / original / name).read_bytes() == (root / 'audit' / nested / name).read_bytes(),
                 'audit fixture byte mismatch')
    audit = read_json(root / 'audit/audit_results.json')
    need(audit['audit_status'] == 'ACCEPT_CORRECTED_PARTIAL' and
         audit['frozen_verifier_status'] == 'TWO_REPRODUCED_GAPS' and
         audit['original_question'] == 'UNSOLVED', 'audit scope mismatch')
    return {'status': 'PASS', 'gate': m['gate'], 'original_question': 'UNSOLVED',
            'payload_files': len(m['files']) + 1, 'archive_members': count,
            'derivative_changed_files': changed}

def verify_queue(root, base_path, updated_path):
    d = read_json(root / 'QUEUE_DELTA.json')
    base, updated = base_path.read_bytes(), updated_path.read_bytes()
    need(identity(base) == d['base'] and identity(updated) == d['updated'], 'queue identity')
    x, y = base.splitlines(keepends=True), updated.splitlines(keepends=True)
    hits = [i for i, b in enumerate(x) if b'| 30000638 / OWR-1394-015 |' in b]
    need(len(hits) == 1 and len(x) == len(y), 'queue target or line count')
    i = hits[0]
    need(i + 1 == d['row_line_1_based'] and x[:i] == y[:i] and x[i+1:] == y[i+1:],
         'unrelated queue bytes')
    a, b = x[i].split(b'|'), y[i].split(b'|')
    need(len(a) == len(b) and [j for j in range(len(a)) if a[j] != b[j]] == [8, 9],
         'queue cell scope')
    need(a[8] == b' queued ' and a[9] == b' 0/5 ' and b[8] == b' unsolved ' and b[9] == b' 5/5 ',
         'queue disposition')
    return {'status': 'PASS', 'changed_cells': ['Status', 'Turns'], 'all_other_bytes_preserved': True}

def run(script, flags, cwd, arguments=()):
    p = subprocess.run([sys.executable, *flags, str(script), *arguments],
                       cwd=cwd, capture_output=True, timeout=600)
    need(p.returncode == 0 and not p.stderr, 'replay failed: ' + p.stderr.decode(errors='replace'))
    return json.loads(p.stdout)

def replay(root):
    out = []
    expected_counts = {'author_regression_checks': 72, 'independent_geometry': 37, 'mutation_probes': 52}
    with tempfile.TemporaryDirectory(prefix='symmetric lattice relocated replay ') as temp:
        base = Path(temp)
        copy = base / 'complete packet'
        shutil.copytree(root, copy)
        verify(copy)
        for flags in ([], ['-O']):
            mode = 'optimized' if flags else 'normal'
            result = run(copy / 'corrected/verify.py', flags, base)
            need(result['status'] == 'PASS_PARTIAL' and result['original_question'] == 'UNSOLVED' and
                 result['geometric_cases'] == 37 and result['residue_cases'] == 7 and
                 result['laguerre_identity_checks'] == 20 and result['product_parameter_checks'] == 4900,
                 'corrected result scope')
            audit = run(copy / 'audit/audit.py', flags, base, ['--write-results'])
            need(audit == {'actual_patch_applies_and_runs': True, 'counts': expected_counts,
                           'status': 'ACCEPT_CORRECTED_PARTIAL'}, 'audit replay summary')
            need((copy / 'audit/audit_results.json').read_bytes() ==
                 (root / 'audit/audit_results.json').read_bytes(), 'full audit results differ')
            verify(copy)
            out.append({'mode': mode, 'corrected': result, 'audit': audit,
                        'full_frozen_audit_results_equal': True, 'relocated': True})
    verify(root)
    return out

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--replay', action='store_true')
    ap.add_argument('--queue-base', type=Path)
    ap.add_argument('--queue-updated', type=Path)
    args = ap.parse_args()
    need(bool(args.queue_base) == bool(args.queue_updated), 'supply both queue paths')
    root = Path(__file__).resolve().parent
    result = verify(root)
    if args.queue_base:
        result['queue'] = verify_queue(root, args.queue_base, args.queue_updated)
    if args.replay:
        result['replay'] = replay(root)
    print(json.dumps(result, indent=2, sort_keys=True))

if __name__ == '__main__':
    main()
