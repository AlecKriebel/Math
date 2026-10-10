#!/usr/bin/env python3
"""Fail-closed publication gate, exact archive binding, and mathematical replay.

Trust this script through its Git commit or a separately verified external hash.
The pinned manifest covers all remaining payloads. Local bytecode directories are
rejected before any package code is run; -B also suppresses bytecode creation.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import tempfile
import zipfile

sys.dont_write_bytecode = True
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
ROOT = Path(__file__).resolve().parent
MANIFEST_SHA = '12222f6b0d5ee4bdfba84ab08a4aa768800176973df089e0427b71a5a6b4a9be'
FILES = ['QUEUE_DELTA.json', 'README.md', 'RESEARCH_LOG.md', 'VERDICT.json', 'archives/ISOLATED_TRANSVERSAL_30001066_AUTHOR_PUBLIC_SAFE_DERIVATIVE.zip', 'archives/ISOLATED_TRANSVERSAL_30001066_PUBLIC_AUDIT_DERIVATIVE.zip', 'audit/ACCEPTANCE.json', 'audit/AUDIT_MANIFEST.json', 'audit/CORPUS_REPLAY.json', 'audit/INDEPENDENT_AUDIT.md', 'audit/PATCH_REPLAY.json', 'audit/README.md', 'audit/RESULTS.json', 'audit/RESULTS_OPTIMIZED_RELOCATED.json', 'audit/SOURCES.json', 'audit/independent_test.py', 'audit/strict_inventory.py', 'audit/verify_audit_package.py', 'audit/verify_corpora.py', 'audit/verify_package_strict.patch', 'author/MANIFEST.json', 'author/README.md', 'author/approach_audit.md', 'author/certificate.json', 'author/proof.md', 'author/results.json', 'author/source_audit.json', 'author/test_verifier.py', 'author/verify.py', 'author/verify_package.py', 'package_mutation_tests.py', 'PUBLICATION_MANIFEST.json', 'verify_publication.py']
ARCHIVES = {'author': {'path': 'archives/ISOLATED_TRANSVERSAL_30001066_AUTHOR_PUBLIC_SAFE_DERIVATIVE.zip', 'bytes': 17217, 'sha256': 'be4dabaf22028561681c76c353bd537d0b240cfd67d52aa7ed9531f435905034'}, 'audit': {'path': 'archives/ISOLATED_TRANSVERSAL_30001066_PUBLIC_AUDIT_DERIVATIVE.zip', 'bytes': 26759, 'sha256': '12b8c6d00a91d8e5244fed83053fa462f403d9d32ba16f6d099e858c972054e6'}}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def unique(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'duplicate JSON key')
        result[key] = value
    return result


def inventory():
    actual = set()
    permitted_dirs = {str(Path(name).parent) for name in FILES if '/' in name}
    for p in ROOT.rglob('*'):
        name = p.relative_to(ROOT).as_posix()
        require(not p.is_symlink(), 'symlink: ' + name)
        if p.is_dir():
            require(name in permitted_dirs, 'unlisted directory: ' + name)
        else:
            require(stat.S_ISREG(p.stat().st_mode), 'special file: ' + name)
            actual.add(name)
    require(actual == set(FILES), 'unexpected or missing publication member')
    raw = (ROOT / 'PUBLICATION_MANIFEST.json').read_bytes()
    require(hashlib.sha256(raw).hexdigest() == MANIFEST_SHA, 'manifest external anchor mismatch')
    m = json.loads(raw, object_pairs_hook=unique)
    require(set(m) == {'schema', 'files'} and m['schema'] == 'isolated-transversal-publication-manifest-v1', 'manifest schema')
    seen = set()
    for row in m['files']:
        require(set(row) == {'path', 'bytes', 'sha256'}, 'manifest row schema')
        n = row['path']
        require(n in FILES and n not in seen and n not in ('PUBLICATION_MANIFEST.json', 'verify_publication.py'), 'manifest path')
        seen.add(n)
        data = (ROOT / n).read_bytes()
        require(type(row['bytes']) is int and len(data) == row['bytes'], 'size: ' + n)
        require(hashlib.sha256(data).hexdigest() == row['sha256'], 'hash: ' + n)
    require(seen == set(FILES) - {'PUBLICATION_MANIFEST.json', 'verify_publication.py'}, 'manifest coverage')
    reports = {}
    for directory, info in ARCHIVES.items():
        archive = ROOT / info['path']
        data = archive.read_bytes()
        require(len(data) == info['bytes'] and hashlib.sha256(data).hexdigest() == info['sha256'], 'archive external anchor')
        expected = {n.split('/', 1)[1] for n in FILES if n.startswith(directory + '/')}
        with zipfile.ZipFile(archive) as z:
            members = z.infolist()
            names = [i.filename for i in members]
            require(len(names) == len(set(names)) and set(names) == expected, 'archive inventory')
            require(not z.comment, 'archive comment')
            for i in members:
                mode = (i.external_attr >> 16) & 0xffff
                require(not i.is_dir() and stat.S_IFMT(mode) in (0, stat.S_IFREG), 'archive member type')
                require(not i.comment and not i.extra and not i.flag_bits & 1, 'archive hidden metadata')
                require(z.read(i.filename) == (ROOT / directory / i.filename).read_bytes(), 'archive/extracted mismatch')
            require(z.testzip() is None, 'archive CRC')
        reports[directory] = {'bytes': len(data), 'sha256': info['sha256'], 'members': len(expected), 'extracted_bytes_match': True}
    return reports


def run(command, cwd, expected=True):
    p = subprocess.run(command, cwd=cwd, env=os.environ, text=True, capture_output=True)
    require((p.returncode == 0) == expected, 'unexpected replay status: ' + p.stdout + p.stderr)
    return p.stdout.strip()


def python(script, args=(), optimized=False, cwd=None, expected=True):
    return run([sys.executable, '-B'] + (['-O'] if optimized else []) + [str(script), *map(str, args)], cwd or ROOT, expected)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--integrity-only', action='store_true')
    args = parser.parse_args()
    archives = inventory()
    author_zip = ROOT / ARCHIVES['author']['path']
    replay = []
    for optimized in (False, True):
        python(ROOT / 'audit/verify_audit_package.py', optimized=optimized)
        python(ROOT / 'audit/strict_inventory.py', ['--archive', author_zip, '--expected-sha256', ARCHIVES['author']['sha256']], optimized)
        python(ROOT / 'audit/strict_inventory.py', ['--directory', ROOT / 'author'], optimized)
    if args.integrity_only:
        print(json.dumps({'status': 'PASS', 'strict_inventory_mandatory': True, 'archives': archives}, sort_keys=True))
        return
    with tempfile.TemporaryDirectory(prefix='isolated-publication-relocated-') as temp:
        temp = Path(temp)
        clean = temp / 'original relocated'
        shutil.copytree(ROOT / 'author', clean)
        for optimized in (False, True):
            for script in ['verify_package.py', 'verify.py', 'test_verifier.py']:
                python(clean / script, optimized=optimized, cwd=temp)
            out = python(ROOT / 'audit/independent_test.py', ['--author-archive', author_zip], optimized, cwd=temp)
            replay.append({'optimized': optimized, 'independent': json.loads(out)})
        derived = temp / 'patched derived'
        shutil.copytree(clean, derived)
        run(['patch', '--batch', '--fuzz=0', '-p1', '-i', str(ROOT / 'audit/verify_package_strict.patch')], derived)
        old = (clean / 'verify_package.py').read_text()
        new = (derived / 'verify_package.py').read_text()
        exemption = "        if '__pycache__' in rel.parts:\n            need(not p.is_symlink(),'symlink in bytecode cache');continue\n"
        require(old.count(exemption) == 1 and new == old.replace(exemption, ''), 'patch changed something besides cache exemption')
        manifest = json.loads((derived / 'MANIFEST.json').read_bytes())
        for row in manifest['files']:
            data = (derived / row['path']).read_bytes()
            row['bytes'] = len(data)
            row['sha256'] = hashlib.sha256(data).hexdigest()
        (derived / 'MANIFEST.json').write_text(json.dumps(manifest, indent=2) + '\n')
        patch_runs = []
        for optimized in (False, True):
            for script in ['verify_package.py', 'verify.py', 'test_verifier.py']:
                python(derived / script, optimized=optimized, cwd=temp)
            for name in ['__pycache__/unexpected.pdf', '__pycache__/verify.cpython-312.pyc', 'unexpected.pdf']:
                p = derived / name
                p.parent.mkdir(exist_ok=True)
                p.write_bytes(b'SYNTHETIC UNLISTED PAYLOAD')
                python(derived / 'verify_package.py', optimized=optimized, cwd=temp, expected=False)
                p.unlink()
                if p.parent != derived:
                    p.parent.rmdir()
                patch_runs.append({'optimized': optimized, 'rejected': name})
            python(derived / 'verify_package.py', optimized=optimized, cwd=temp)
        require(inventory() == archives, 'original publication changed during replay')
    print(json.dumps({'status': 'PASS', 'strict_inventory_mandatory': True, 'problem_id': 30001066,
        'full_source_solved': False, 'turns': '5/5', 'archives': archives,
        'independent_replays': replay, 'actual_patch_rejected_mutations': patch_runs,
        'frozen_archives_unchanged': True}, sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, KeyError, TypeError, zipfile.BadZipFile) as exc:
        raise SystemExit('FAIL: ' + str(exc))
