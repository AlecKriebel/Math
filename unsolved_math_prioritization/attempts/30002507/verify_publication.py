#!/usr/bin/env python3
"""Externally anchored byte integrity and finite replay, not a formal proof checker."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import zipfile

sys.dont_write_bytecode = True
MANIFEST = 'PUBLICATION_MANIFEST.json'
ANCHORS = {
    'author/safe/MANIFEST.json': '5f892f30acb55e30ccfcf88932e933c55b76942583bca032bbc8339d95548791',
    'author/DIRICHLET_ZERO_30002507_AUTHOR_FREEZE.zip': 'd3c1884b33f378a1289dcbd6eea175dd0e721964f478a6ceb6186d7990d77b1b',
    'independent_audit/AUDIT_MANIFEST.json': '126d118347c7a95a3b1301b55af9576ae15d756c0b20231deaec90c3b0655255',
}

def require(condition, reason):
    if not condition:
        raise ValueError(reason)

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def unique_keys(pairs):
    out = {}
    for key, value in pairs:
        require(key not in out, 'duplicate JSON key')
        out[key] = value
    return out

def read_json(raw):
    return json.loads(raw, object_pairs_hook=unique_keys)

def entries(raw, self_name):
    obj = read_json(raw)
    require(isinstance(obj['files'], list), 'manifest rows')
    rows = {}
    for row in obj['files']:
        require(set(row) == {'path','bytes','sha256'}, 'manifest row keys')
        name = row['path']
        require(isinstance(name, str) and re.fullmatch(r'[A-Za-z0-9_./-]+', name), 'path characters')
        path = PurePosixPath(name)
        require(not path.is_absolute() and str(path) == name and '..' not in path.parts, 'unsafe path')
        require(name not in rows and name != self_name, 'duplicate or self path')
        require(type(row['bytes']) is int and row['bytes'] >= 0, 'byte count')
        require(isinstance(row['sha256'], str) and re.fullmatch(r'[a-f0-9]{64}', row['sha256']), 'hash format')
        rows[name] = row
    return rows

def compare_file(path, row):
    raw = path.read_bytes()
    require(len(raw) == row['bytes'] and digest(raw) == row['sha256'], 'file bytes ' + str(path.name))

def verify(root, expected_manifest):
    root = Path(root)
    require(root.is_dir() and not root.is_symlink(), 'package directory')
    m = root / MANIFEST
    require(m.is_file() and not m.is_symlink(), 'manifest regular file')
    raw = m.read_bytes()
    require(digest(raw) == expected_manifest, 'external publication manifest anchor')
    listed = entries(raw, MANIFEST)
    expected_dirs = {str(parent) for name in listed for parent in PurePosixPath(name).parents if str(parent) != '.'}
    actual, dirs = {}, set()
    for path in root.rglob('*'):
        require(not path.is_symlink(), 'symlink prohibited')
        name = path.relative_to(root).as_posix()
        if path.is_dir():
            dirs.add(name)
        else:
            require(stat.S_ISREG(path.stat().st_mode), 'nonregular file')
            if name != MANIFEST:
                actual[name] = path
    require(dirs == expected_dirs, 'directory inventory')
    require(set(actual) == set(listed), 'file inventory')
    for name, path in actual.items():
        compare_file(path, listed[name])
    for name, anchor in ANCHORS.items():
        require(digest((root / name).read_bytes()) == anchor, 'frozen anchor ' + name)
    for folder, manifest in [('author/safe','MANIFEST.json'), ('independent_audit','AUDIT_MANIFEST.json')]:
        rows = entries((root / folder / manifest).read_bytes(), manifest)
        require(set(rows) | {manifest} == {p.name for p in (root/folder).iterdir()}, 'inner inventory')
        for name, row in rows.items():
            require(PurePosixPath(name).name == name, 'flat inner path')
            compare_file(root / folder / name, row)
    archive = root / 'author/DIRICHLET_ZERO_30002507_AUTHOR_FREEZE.zip'
    require(archive.stat().st_size == 29837, 'archive size')
    with zipfile.ZipFile(archive) as z:
        safe = root / 'author/safe'
        require(len(z.infolist()) == 18 and set(z.namelist()) == {p.name for p in safe.iterdir()}, 'archive inventory')
        require(z.testzip() is None, 'archive CRC')
        for name in z.namelist():
            require(z.read(name) == (safe/name).read_bytes(), 'archive equality')
    binding = read_json((root/'independent_audit/BINDING.json').read_bytes())
    require(binding['author_manifest_sha256'] == ANCHORS['author/safe/MANIFEST.json'], 'audit author binding')
    require(binding['author_archive_sha256'] == ANCHORS['author/DIRICHLET_ZERO_30002507_AUTHOR_FREEZE.zip'], 'audit archive binding')
    audit = read_json((root/'independent_audit/RESULTS.json').read_bytes())
    require(audit['original_target_status'] == 'unsolved' and audit['author_approaches_used'] == 5, 'audit disposition')
    require(audit['mandatory_mathematical_corrections'] == [], 'audit corrections')
    status = read_json((root/'PUBLICATION_STATUS.json').read_bytes())
    require(status['target_id'] == '30002507' and status['queue_status'] == 'unsolved', 'publication target')
    require(status['turns_used'] == status['turn_limit'] == 5 and status['independent_audit_completed'], 'publication accounting')
    for key in ['full_solution','novelty_claim','global_openness_certified','global_uniqueness_proved','exact_convergence_abscissa_claimed','continuation_substituted_for_convergence','finite_controls_prove_analytic_theorems','exact_website_inspected','raw_statement_inspected','raw_prior_AI_report_inspected']:
        require(status[key] is False, 'scope non-claim ' + key)
    return len(listed) + 1

def replay(root):
    root = Path(root).resolve()
    env = dict(os.environ)
    env.pop('PYTHONOPTIMIZE', None)
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    with tempfile.TemporaryDirectory(prefix='dirichlet-portable-') as tmp:
        copied = Path(tmp)/'relocated'
        shutil.copytree(root, copied)
        results = {}
        for mode, flags in [('normal', []), ('optimized', ['-O'])]:
            def run(script, *args):
                proc = subprocess.run([sys.executable,'-E','-B',*flags,str(copied/script),*map(str,args)], cwd=tmp, env=env, capture_output=True)
                require(proc.returncode == 0, script + ': ' + proc.stderr.decode())
                return proc.stdout
            def matched(script, record, *args):
                raw = run(script, *args)
                require(raw == (copied/record).read_bytes(), 'replay byte equality ' + record)
                return read_json(raw)
            a = matched('author/safe/verify.py','author/safe/CONTROL_RESULTS.json')
            n = matched('author/safe/negative_controls.py','author/safe/NEGATIVE_CONTROL_RESULTS.json')
            m = read_json(run('author/safe/verify_manifest.py','--replay'))
            i = matched('independent_audit/independent_controls.py','independent_audit/INDEPENDENT_CONTROL_RESULTS.json')
            b = read_json(run('independent_audit/verify_frozen_binding.py','--author',copied/'author'))
            bn = matched('independent_audit/verify_frozen_binding.py','independent_audit/INDEPENDENT_NEGATIVE_RESULTS.json','--author',copied/'author','--negative-controls')
            require(a['result'] == n['result'] == m['result'] == i['result'] == b['result'] == bn['result'] == 'PASS', 'suite result')
            require(a['total_predicates'] == 67207 and n['negative_cases'] == 12, 'author counts')
            require(i['total_predicates'] == 192572 and i['negative_control_count'] == 6 and bn['negative_cases'] == 18, 'independent counts')
            results[mode] = {'author_predicates':67207,'author_corruptions':12,'independent_predicates':192572,'independent_math_negative_cases':6,'independent_frozen_binding_corruptions':18,'byte_exact_recorded_results':True}
        require(results['normal'] == results['optimized'], 'mode agreement')
    return {'relocated_package':True,'unrelated_working_directory':True,'direct_normal_and_optimized_children':True,'modes':results}

def main():
    p = argparse.ArgumentParser()
    p.add_argument('root',type=Path)
    p.add_argument('expected_manifest_sha256')
    p.add_argument('--replay',action='store_true')
    args = p.parse_args()
    result = {'result':'PASS','package_files':verify(args.root,args.expected_manifest_sha256),'scope':'Byte integrity and finite controls supplement the written analytic proof; no complete target solution.'}
    if args.replay:
        result['replay'] = replay(args.root)
        verify(args.root,args.expected_manifest_sha256)
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__ == '__main__':
    main()
