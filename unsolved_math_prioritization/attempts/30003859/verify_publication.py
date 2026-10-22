#!/usr/bin/env python3
"""Closed delivery checks and exact replays; no claim of general rigidity."""
from pathlib import Path, PurePosixPath
import argparse, hashlib, json, os, shutil, stat, subprocess, sys, tempfile, zipfile
ROOT = Path(__file__).absolute().parent
AUTHOR = 'hirzebruch_kummer_30003859'
AUDIT = AUTHOR + '_independent_audit'
ARCHIVES = {
    'HIRZEBRUCH_KUMMER_30003859_AUTHOR_SAFE_FREEZE.zip': AUTHOR,
    'HIRZEBRUCH_KUMMER_30003859_INDEPENDENT_AUDIT_SAFE.zip': AUDIT,
}
PINS = {
    AUTHOR + '/manifest.json': 'e999f3f7d15d19152e106ad898c8f6ec2f36b9f5ca7cedbdb067477accbfa867',
    AUDIT + '/manifest.json': 'b011e6dfee108810ea54ce1a3c8efac57879ec2f22c77cc0164b31d6a88ceb7b',
    'HIRZEBRUCH_KUMMER_30003859_AUTHOR_SAFE_FREEZE.zip': 'e70fb6353ef5a98363dfd3cbe9aa66531a1b45ef92e90bde2c19b4e70cf99bf9',
    'HIRZEBRUCH_KUMMER_30003859_INDEPENDENT_AUDIT_SAFE.zip': '20ca1b872ed1e5241d5e29af233e969e5bc63377dd815b2666280ef89efa82b5',
}

def need(ok, message):
    if not ok:
        raise ValueError(message)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def regular(path):
    need(stat.S_ISREG(path.lstat().st_mode), 'Not a regular file: ' + str(path))
    return path.read_bytes()

def safe_path(name):
    need(isinstance(name, str) and bool(name), 'Missing path')
    p = PurePosixPath(name)
    need(not p.is_absolute() and '..' not in p.parts and '.' not in p.parts and str(p) == name and '\\' not in name, 'Unsafe path')
    return p

def closed(root, manifest='PUBLICATION_MANIFEST.json'):
    need(root.is_dir() and not root.is_symlink(), 'Invalid root')
    rows = json.loads(regular(root / manifest))['files']
    names = [r['path'] for r in rows]
    need(len(names) == len(set(names)), 'Duplicate path')
    for name in names:
        safe_path(name)
        need(name != manifest, 'Manifest self inclusion')
    expected = set(names) | {manifest}
    expected_dirs = {p.as_posix() for s in expected for p in PurePosixPath(s).parents if str(p) != '.'}
    files, dirs = set(), set()
    for p in root.rglob('*'):
        rel, mode = p.relative_to(root).as_posix(), p.lstat().st_mode
        if stat.S_ISREG(mode):
            files.add(rel)
        elif stat.S_ISDIR(mode):
            dirs.add(rel)
        else:
            raise ValueError('Symlink or special member: ' + rel)
    need(files == expected and dirs == expected_dirs, 'Closed file/directory set mismatch')
    for r in rows:
        data = regular(root / r['path'])
        need(len(data) == r['bytes'] and digest(data) == r['sha256'], 'Size/digest mismatch: ' + r['path'])
    return len(files)

def archive_check(root, name, folder):
    names = {p.relative_to(root / folder).as_posix() for p in (root / folder).rglob('*') if p.is_file()}
    seen = set()
    with zipfile.ZipFile(root / name) as z:
        for item in z.infolist():
            safe_path(item.filename)
            need(not item.is_dir() and not stat.S_ISLNK(item.external_attr >> 16) and not (item.flag_bits & 1), 'Unsafe archive member')
            need(item.filename in names and item.filename not in seen, 'Unlisted/duplicate ZIP member')
            seen.add(item.filename)
            need(z.read(item) == regular(root / folder / item.filename), 'Archive/directory mismatch')
    need(seen == names, 'Archive file set mismatch')
    return len(seen)

def check_fast(root):
    count = closed(root)
    for name, pin in PINS.items():
        need(digest(regular(root / name)) == pin, 'Frozen receipt mismatch: ' + name)
    closed(root / AUTHOR, 'manifest.json')
    closed(root / AUDIT, 'manifest.json')
    frozen = sum(archive_check(root, n, f) for n, f in ARCHIVES.items())
    s = json.loads(regular(root / 'PUBLICATION_STATUS.json'))
    expected = {
        'problem_id': '30003859', 'rank': 741, 'status': 'unsolved', 'turns': '5/5',
        'disposition': 'scoped_partial_investigation', 'intended_conjecture': 'unresolved',
        'literal_unrestricted_formulation': 'four-line/Fermat counterexample; outside intended nontrivial-incidence class',
        'eventual_periodicity': 'infinitesimal-rigidity failure only, for each fixed nonpencil arrangement',
        'eventual_rigidity_claim': False, 'local_rigidity_periodicity_claim': False,
        'novelty_claim': False, 'full_quadrangle_reproof_claim': False,
        'review_type': 'independent AI mathematical/code/source audit; not human peer review or formal verification',
        'audit_disposition': 'PASS_SCOPED', 'mandatory_corrections': 0,
        'homogeneous_generators': 'componentwise-minimal elements of H minus {0}',
        'equisingular_condition': 'kernel of the local singularity-deformation map in source Definition 2.1; no abstract-to-equisingular bridge proved',
    }
    for key, value in expected.items():
        need(s.get(key) == value, 'Disposition/scope mismatch: ' + key)
    v = json.loads(regular(root / AUDIT / 'audit_result.json'))
    need(v['disposition'] == 'PASS' and v['mandatory_corrections'] == [] and v['intended_problem_status'] == 'unresolved_in_this_investigation', 'Audit disposition mismatch')
    return {'packet_files': count, 'frozen_files_preserved': frozen, 'archives_preserved': len(ARCHIVES)}

def run(root, relative, opt, *args):
    cmd = [sys.executable] + (['-O'] if opt else []) + [str(root / relative)] + list(args)
    return subprocess.check_output(cmd, cwd=tempfile.gettempdir(), env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'), stderr=subprocess.STDOUT)

def replay(root):
    for opt in (False, True):
        need(run(root, AUTHOR + '/verify.py', opt) == regular(root / AUTHOR / 'expected_results.json'), 'Author output mismatch')
        need(run(root, AUDIT + '/verify_independent.py', opt, '--author-dir', str(root / AUTHOR), '--archive', str(root / 'HIRZEBRUCH_KUMMER_30003859_AUTHOR_SAFE_FREEZE.zip')) == regular(root / AUDIT / 'independent_results.json'), 'Independent output mismatch')
        a = json.loads(run(root, AUTHOR + '/verify_manifest.py', opt, '--selftest'))
        need(a['status'] == 'PASS_AUTHOR_INTEGRITY' and a['rejected_integrity_mutations'] == 6, 'Author integrity controls failed')
        b = json.loads(run(root, AUDIT + '/verify_audit_manifest.py', opt, '--selftest'))
        need(b['status'] == 'PASS_AUDIT_INTEGRITY' and b['rejected_mutations'] == 6, 'Audit integrity controls failed')
    return {'author_replay_byte_equal': True, 'independent_replay_byte_equal': True, 'normal_and_optimized': True, 'historical_integrity_controls': 12}

def reseal(root):
    p = root / 'PUBLICATION_MANIFEST.json'
    m = json.loads(p.read_text())
    for r in m['files']:
        data = regular(root / r['path'])
        r.update(bytes=len(data), sha256=digest(data))
    p.write_text(json.dumps(m, indent=2, sort_keys=True) + '\n')

def selftest(root):
    cases = ['edit_author', 'edit_audit', 'edit_archive', 'missing', 'extra_pdf', 'extra_hidden', 'extra_directory', 'duplicate', 'traversal', 'repin_author']
    cases += ['symlink:' + s for s in ['PUBLICATION_MANIFEST.json', AUTHOR + '/manifest.json', AUDIT + '/manifest.json', AUTHOR + '/PROOFS.md', 'HIRZEBRUCH_KUMMER_30003859_AUTHOR_SAFE_FREEZE.zip']]
    upgrades = {'status': 'claimed_solved', 'turns': '1/5', 'intended_conjecture': 'solved', 'eventual_rigidity_claim': True, 'local_rigidity_periodicity_claim': True, 'novelty_claim': True, 'full_quadrangle_reproof_claim': True, 'review_type': 'human peer review', 'homogeneous_generators': 'minimal elements of H', 'equisingular_condition': 'constant topology'}
    cases += ['scope:' + k for k in upgrades]
    for case in cases:
        with tempfile.TemporaryDirectory() as temp:
            dst = Path(temp) / 'packet'
            shutil.copytree(root, dst)
            if case.startswith('symlink:'):
                name = case.split(':', 1)[1]
                p = dst / name
                p.unlink()
                p.symlink_to(root / name)
            elif case.startswith('scope:'):
                key = case.split(':', 1)[1]
                p = dst / 'PUBLICATION_STATUS.json'
                s = json.loads(p.read_text())
                s[key] = upgrades[key]
                p.write_text(json.dumps(s))
                reseal(dst)
            elif case in ('edit_author', 'edit_audit', 'edit_archive'):
                name = {'edit_author': AUTHOR + '/PROOFS.md', 'edit_audit': AUDIT + '/AUDIT_REPORT.md', 'edit_archive': 'HIRZEBRUCH_KUMMER_30003859_AUTHOR_SAFE_FREEZE.zip'}[case]
                p = dst / name
                p.write_bytes(p.read_bytes() + b'changed')
            elif case == 'missing':
                (dst / AUTHOR / 'PROOFS.md').unlink()
            elif case == 'extra_pdf':
                (dst / 'unexpected.pdf').write_bytes(b'%PDF-1.4')
            elif case == 'extra_hidden':
                (dst / '.private').write_text('excluded')
            elif case == 'extra_directory':
                (dst / 'unexpected_empty').mkdir()
            elif case in ('duplicate', 'traversal'):
                p = dst / 'PUBLICATION_MANIFEST.json'
                m = json.loads(p.read_text())
                if case == 'duplicate':
                    m['files'].append(m['files'][0])
                else:
                    m['files'][0]['path'] = '../outside'
                p.write_text(json.dumps(m))
            elif case == 'repin_author':
                p = dst / AUTHOR / 'PROOFS.md'
                p.write_bytes(p.read_bytes() + b'changed')
                p = dst / AUTHOR / 'manifest.json'
                m = json.loads(p.read_text())
                for r in m['files']:
                    data = regular(dst / AUTHOR / r['path'])
                    r.update(bytes=len(data), sha256=digest(data))
                p.write_text(json.dumps(m))
                reseal(dst)
            try:
                check_fast(dst)
            except (ValueError, KeyError, TypeError, OSError, zipfile.BadZipFile):
                pass
            else:
                raise ValueError('Mutation accepted: ' + case)
    return {'rejected': cases, 'count': len(cases)}

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--selftest', action='store_true')
    p.add_argument('--integrity-only', action='store_true')
    args = p.parse_args()
    result = {'result': 'PASS', 'problem_id': '30003859', 'status': 'unsolved', 'turns': '5/5', 'scope': 'Scoped partials; intended conjecture unresolved; no novelty or full quadrangle reproof claim.'}
    result.update(check_fast(ROOT))
    if not args.integrity_only:
        result.update(replay(ROOT))
    if args.selftest:
        result['delivery_negative_controls'] = selftest(ROOT)
    check_fast(ROOT)
    result['publication_manifest_sha256'] = digest(regular(ROOT / 'PUBLICATION_MANIFEST.json'))
    print(json.dumps(result, indent=2, sort_keys=True))

if __name__ == '__main__':
    main()
