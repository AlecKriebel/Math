"""Offline integrity and replay verifier. No external services or third-party files.
Supply the trusted manifest hash from the separate external manifest for pinning.
All checks remain active under Python optimization; original bytes are never edited.
"""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
sys.dont_write_bytecode = True

AUTHOR_MANIFEST_SHA256 = '5189f13df28414cb1438e75782e332f0d1db2a26d193f5b6135e195fb537ce82'
AUTHOR_ARCHIVE_SHA256 = '970e1d0e9eeee5ff0357c91aabba26f6343955e936167280726a05b0ac68ffdd'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def closure(root, expected_manifest=None):
    root = root.resolve()
    raw = (root/'MANIFEST.json').read_bytes()
    if expected_manifest:
        require(digest(raw) == expected_manifest, 'audit manifest pin mismatch')
    data = json.loads(raw)
    entries = data['files']
    names = [row['path'] for row in entries]
    require(len(names) == len(set(names)), 'duplicate manifest member')
    actual = []
    for path in root.rglob('*'):
        require(not path.is_symlink(), 'symlinks are not allowed')
        if path.is_file():
            actual.append(path.relative_to(root).as_posix())
    require(set(actual) == set(names) | {'MANIFEST.json'}, 'missing or extra file in audit tree')
    for row in entries:
        rel = Path(row['path'])
        require(not rel.is_absolute() and '..' not in rel.parts, 'unsafe manifest member')
        b = (root/rel).read_bytes()
        require(len(b) == row['bytes'] and digest(b) == row['sha256'], 'member pin mismatch: '+row['path'])
    manifest_bytes = (root/'author_external_manifest.json').read_bytes()
    require(digest(manifest_bytes) == AUTHOR_MANIFEST_SHA256, 'author manifest pin mismatch')
    author = json.loads(manifest_bytes)
    require(author['archive']['sha256'] == AUTHOR_ARCHIVE_SHA256 and author['archive']['bytes'] == 11900, 'original archive reference mismatch')
    original_names = [p.relative_to(root/'author_original').as_posix() for p in (root/'author_original').rglob('*') if p.is_file()]
    require(set(original_names) == {x['path'] for x in author['files']}, 'author member set mismatch')
    for row in author['files']:
        b = (root/'author_original'/row['path']).read_bytes()
        require(len(b) == row['bytes'] and digest(b) == row['sha256'], 'original author member changed')
    status = json.loads((root/'author_original/status.json').read_text())
    require(status['status'] == 'partial_stalled' and status['approaches_used'] == 3 and status['approach_cap'] == 5, 'status changed')
    require(not status['full_solution'] and not status['asymptotic_improvement'] and not status['novelty_claim'], 'overclaim detected')
    acceptance = json.loads((root/'acceptance_report.json').read_text())
    require(acceptance['full_solution_accepted'] is False and acceptance['original_optimized_validation_accepted'] is False, 'acceptance scope changed')
    return len(entries)


def replay(root):
    results = []
    expected = (root/'author_original/validation_results.json').read_bytes()
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    with tempfile.TemporaryDirectory(prefix='ep642-relocated-') as temp:
        temp = Path(temp)
        for candidate in ['author_original','corrected']:
            for optimized in [False,True]:
                target = temp/(candidate+str(optimized)); target.mkdir()
                shutil.copy2(root/candidate/'validation.py',target/'validation.py')
                command = [sys.executable,'-B']+(['-O'] if optimized else [])+[str(target/'validation.py')]
                cp = subprocess.run(command,cwd=temp,capture_output=True,text=True,env=env,timeout=60)
                require(cp.returncode == 0, 'replay failed: '+candidate)
                require((target/'validation_results.json').read_bytes() == expected, 'replay output mismatch')
                results.append({'candidate':candidate,'optimized':optimized,'output_matches':True,'checks_active':candidate=='corrected' or not optimized})
        for optimized in [False,True]:
            command = [sys.executable,'-B']+(['-O'] if optimized else [])+[str(root/'independent_checks.py'),str(root/'corrected/validation.py')]
            cp = subprocess.run(command,cwd=temp,capture_output=True,text=True,env=env,timeout=60)
            require(cp.returncode == 0, 'independent replay failed')
            outcome = json.loads(cp.stdout)
            require(outcome['passed'] and outcome['all_labeled_graphs_orders_0_through_5'] == 1100, 'independent finite scope mismatch')
            results.append({'candidate':'independent_subset_DP','optimized':optimized,'passed':True})
    return results


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parent)
    parser.add_argument('--expected-manifest-sha256')
    parser.add_argument('--integrity-only',action='store_true')
    args = parser.parse_args()
    root = args.root.resolve()
    count = closure(root,args.expected_manifest_sha256)
    result = {'passed':True,'integrity_members':count,
              'externally_pinned':args.expected_manifest_sha256 is not None,
              'original_archive_reference_sha256':AUTHOR_ARCHIVE_SHA256,
              'scope':'Accepted elementary partial results and hardened finite validation; not a solution.'}
    if not args.integrity_only:
        result['replays'] = replay(root)
    print(json.dumps(result,indent=2))
