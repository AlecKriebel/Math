#!/usr/bin/env python3
"""Byte integrity plus assertion-enabled finite replay; not a proof checker."""
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

sys.dont_write_bytecode = True
MANIFEST = 'PUBLICATION_MANIFEST.json'
ANCHORS = {
    'author/MANIFEST.json': '37454929779c07bff92cb3a3db3346560893aa9f43c9f4ee8250573d10caa5eb',
    'independent_audit/MANIFEST.json': '27057cf19816428d385c20594f9214daeb25ff0a95899565a714871f244a1e9f',
    'independent_audit/AUDIT.md': '33398d4ae6b3a3df2b427153ef69d29dc339c32c309a3d2cb99244720f9fc2d9',
}

def require(value, label):
    if not value:
        raise ValueError(label)

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
    require(isinstance(obj['files'], list), 'manifest file list')
    result = {}
    for row in obj['files']:
        name = row['path']
        require(isinstance(name, str) and re.fullmatch(r'[A-Za-z0-9_./-]+', name), 'path characters')
        path = PurePosixPath(name)
        require(not path.is_absolute() and str(path) == name and '..' not in path.parts, 'unsafe path')
        require(name != self_name and name not in result, 'duplicate or self path')
        require(type(row['bytes']) is int and row['bytes'] >= 0, 'byte count')
        require(isinstance(row['sha256'], str) and re.fullmatch(r'[a-f0-9]{64}', row['sha256']), 'hash format')
        result[name] = row
    return result

def verify(root, expected_manifest):
    require(not sys.flags.optimize and __debug__, 'assertions must be enabled; do not use -O or PYTHONOPTIMIZE')
    root = Path(root)
    require(root.is_dir() and not root.is_symlink(), 'package directory')
    manifest = root / MANIFEST
    require(manifest.is_file() and not manifest.is_symlink(), 'manifest file')
    raw = manifest.read_bytes()
    require(digest(raw) == expected_manifest, 'external publication manifest anchor')
    listed = entries(raw, MANIFEST)
    actual = {}
    for path in root.rglob('*'):
        require(not path.is_symlink(), 'symlink prohibited')
        if path.is_dir():
            continue
        require(stat.S_ISREG(path.stat().st_mode), 'nonregular file')
        name = path.relative_to(root).as_posix()
        if name != MANIFEST:
            actual[name] = path
    require(set(listed) == set(actual), 'publication file set')
    for name, path in actual.items():
        raw = path.read_bytes()
        require(len(raw) == listed[name]['bytes'] and digest(raw) == listed[name]['sha256'], 'publication bytes ' + name)
    for name, anchor in ANCHORS.items():
        require(digest((root / name).read_bytes()) == anchor, 'frozen anchor ' + name)
    for folder in ['author', 'independent_audit']:
        inner = entries((root / folder / 'MANIFEST.json').read_bytes(), 'MANIFEST.json')
        require({p.name for p in (root / folder).iterdir()} == set(inner) | {'MANIFEST.json'}, folder + ' frozen file set')
        for name, row in inner.items():
            require(PurePosixPath(name).name == name, 'flat frozen path')
            raw = (root / folder / name).read_bytes()
            require(len(raw) == row['bytes'] and digest(raw) == row['sha256'], folder + ' frozen bytes ' + name)
    binding = read_json((root / 'independent_audit/BINDING.json').read_bytes())
    require(binding['candidate_manifest_sha256'] == ANCHORS['author/MANIFEST.json'], 'candidate binding')
    require(binding['classification_supported'] == 'already_solved', 'audit disposition')
    require(binding['attempt_accounting_supported']['turns_used'] == 1, 'audit attempt count')
    for row in binding['candidate_all_files']:
        require(PurePosixPath(row['path']).name == row['path'], 'binding path')
        raw = (root / 'author' / row['path']).read_bytes()
        require(len(raw) == row['bytes'] and digest(raw) == row['sha256'], 'bound candidate bytes')
    status = read_json((root / 'PUBLICATION_STATUS.json').read_bytes())
    require(status['problem_id'] == '30002468' and status['queue_status'] == 'already_solved', 'status target')
    require(status['turns_used'] == 1 and status['turn_limit'] == 5, 'attempt accounting')
    require(status['credited_prior_negative'] and status['independent_audit_completed'], 'completed prior-result audit')
    for key in ['novelty_claim', 'external_theorem_formally_reproved', 'finite_controls_prove_limit', 'all_p_resolution', 'raw_ai_report_inspected', 'exact_website_inspected']:
        require(status[key] is False, 'scope non-claim ' + key)
    return len(actual) + 1

def replay(root):
    root = Path(root).resolve()
    env = dict(os.environ)
    env.pop('PYTHONOPTIMIZE', None)
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    python = [sys.executable, '-E', '-B']
    probe = subprocess.run(python + ['-c', 'import sys; print(int(__debug__), sys.flags.optimize)'], env=env, text=True, capture_output=True, check=True)
    require(probe.stdout.strip() == '1 0', 'subprocess assertions enabled')
    with tempfile.TemporaryDirectory(prefix='biclique-portable-replay-') as tmp:
        copied = Path(tmp) / 'relocated'
        shutil.copytree(root, copied)
        def run(script, *args):
            process = subprocess.run(python + [str(copied / script), *map(str, args)], cwd=tmp, env=env, text=True, capture_output=True)
            require(process.returncode == 0, script + ': ' + process.stderr)
            return process.stdout
        author_raw = run('author/verify_exact.py')
        audit_raw = run('independent_audit/independent_controls.py')
        require(author_raw.encode() == (copied / 'author/EXACT_RESULTS.json').read_bytes(), 'author exact results byte equality')
        require(audit_raw.encode() == (copied / 'independent_audit/INDEPENDENT_RESULTS.json').read_bytes(), 'independent exact results byte equality')
        author = read_json(run('author/verify_packet.py'))
        audit = read_json(run('independent_audit/verify_audit.py', copied / 'author'))
        require(author['status'] == audit['status'] == 'PASS', 'frozen suite status')
        require(audit['independent_graphs_checked'] == 1100, 'graph check count')
        return {'assertions_enabled': True, 'relocated_byte_identical_results': True,
                'author_payload_files': author['verified_files'], 'independent_graphs_checked': 1100,
                'external_theorem_reproved': False, 'formal_proof_checker': False}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('root', type=Path)
    parser.add_argument('expected_manifest_sha256')
    parser.add_argument('--replay', action='store_true')
    args = parser.parse_args()
    result = {'status': 'PASS', 'package_files': verify(args.root, args.expected_manifest_sha256), 'scope': 'byte integrity and finite controls; credited published theorem plus written asymptotic implication'}
    if args.replay:
        result['replay'] = replay(args.root)
        verify(args.root, args.expected_manifest_sha256)
    print(json.dumps(result, indent=2, sort_keys=True))

if __name__ == '__main__':
    main()
