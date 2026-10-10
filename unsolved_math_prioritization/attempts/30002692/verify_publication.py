#!/usr/bin/env python3
"""Pinned publication integrity and portable assertion-active diagnostic replay."""
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
    'release': ('pe_boundary_30002692_author_freeze.zip', 16542, 10,
        '861a13e04725c4ba6cfa227fa5a2a8d36e1e16416cec2d9865127f703a6557cb',
        'f15bd36c7ac29f61315054932772b0da76482a3c8119d34b8b645679590da08e',
        'pe-boundary-author-freeze-v1'),
    'audit_release': ('pe_boundary_30002692_independent_audit.zip', 22360, 11,
        '3606628b167a19c03d28bca505790d0541e70f3b4c9e34bc974c7d3e47e99a81',
        'eb05c7f51a58fc9df7ae7782ab18637fd2f3fe5c96c9de91d030fa8198828178',
        'pe-boundary-independent-audit-freeze-v1'),
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


def manifest_entries(raw, self_name, schema='sha256-bytes-v1'):
    obj = read_json(raw)
    require(obj['schema'] == schema, 'manifest schema')
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
    root = Path(root)
    require(root.is_dir() and not root.is_symlink(), 'package directory')
    manifest = root / MANIFEST
    require(manifest.is_file() and not manifest.is_symlink(), 'manifest file')
    raw = manifest.read_bytes()
    require(digest(raw) == expected_manifest, 'external publication manifest anchor')
    entries = manifest_entries(raw, MANIFEST)
    actual, directories = {}, set()
    for path in root.rglob('*'):
        require(not path.is_symlink(), 'symlink prohibited')
        name = path.relative_to(root).as_posix()
        if path.is_dir():
            directories.add(name)
            continue
        require(stat.S_ISREG(path.stat().st_mode), 'nonregular file')
        if name != MANIFEST:
            actual[name] = path
    require(directories == {'release', 'audit_release'}, 'exact directory set')
    require(set(entries) == set(actual), 'publication file set')
    for name, path in actual.items():
        raw = path.read_bytes()
        require(len(raw) == entries[name]['bytes'] and digest(raw) == entries[name]['sha256'], 'publication bytes ' + name)
    for folder, (filename, size, count, archive_sha, manifest_sha, schema) in ANCHORS.items():
        archive = root / filename
        raw = archive.read_bytes()
        require(len(raw) == size and digest(raw) == archive_sha, folder + ' archive anchor')
        with zipfile.ZipFile(archive) as z:
            infos = z.infolist()
            names = [info.filename for info in infos]
            require(len(names) == len(set(names)) == count and z.testzip() is None, folder + ' archive members')
            for info in infos:
                require(not info.is_dir() and PurePosixPath(info.filename).name == info.filename, 'flat archive path')
                require(not stat.S_ISLNK(info.external_attr >> 16), 'archive symlink')
            require(digest(z.read('MANIFEST.json')) == manifest_sha, folder + ' manifest anchor')
            inner = manifest_entries(z.read('MANIFEST.json'), 'MANIFEST.json', schema)
            require(set(names) == set(inner) | {'MANIFEST.json'}, folder + ' member set')
            require({p.name for p in (root / folder).iterdir()} == set(names), folder + ' extraction set')
            for name in names:
                raw = z.read(name)
                require(raw == (root / folder / name).read_bytes(), folder + ' extraction bytes')
                if name in inner:
                    require(len(raw) == inner[name]['bytes'] and digest(raw) == inner[name]['sha256'], folder + ' member bytes')
    b = read_json((root / 'audit_release/INPUT_BINDING.json').read_bytes())
    require(b['author_manifest_sha256'] == ANCHORS['release'][4], 'cross-packet manifest binding')
    require(b['author_archive']['sha256'] == ANCHORS['release'][3] and b['author_archive']['bytes'] == ANCHORS['release'][1], 'cross-packet archive binding')
    p = read_json((root / 'PUBLICATION_STATUS.json').read_bytes())
    require(p['problem_id'] == '30002692' and p['status'] == 'already_solved', 'target disposition')
    require(p['substantive_approaches_used'] == 1 and p['approach_limit'] == 5, 'one approach')
    require(p['publication_assessment'] == 'accepted_for_printed_primary_statement', 'primary-only acceptance')
    require(p['independent_audit'] == 'accepted', 'accepted audit')
    for key in ['novelty_claim', 'new_proof_or_discovery_claim', 'global_openness_claim',
                'aggregator_statement_verified', 'raw_ai_problem_corpora_inspected',
                'unqualified_current_aggregator_status_approved',
                'original_author_release_modified', 'original_audit_release_modified']:
        require(p[key] is False, 'scope non-claim ' + key)
    require(p['bulk_dimension'] == 3 and p['bulk_orientable'] is True and p['bulk_sectional_curvature'] == -1, 'bulk scope')
    require(p['boundary_components'] == 1 and p['boundary_genus'] == 2, 'boundary scope')
    return len(actual) + 1


def replay(root):
    root = Path(root).resolve()
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONOPTIMIZE='0')
    launcher = ('import runpy,sys; '
                'sys.flags.optimize == 0 and __debug__ or sys.exit("assertions disabled"); '
                'sys.argv=sys.argv[1:]; runpy.run_path(sys.argv[0],run_name="__main__")')
    with tempfile.TemporaryDirectory(prefix='pe-boundary-publication-replay-') as tmp:
        copied = Path(tmp) / 'relocated'
        shutil.copytree(root, copied)
        def run(script, *args):
            process = subprocess.run([sys.executable, '-B', '-c', launcher, str(copied / script), *map(str, args)], cwd=tmp, env=env, text=True, capture_output=True)
            require(process.returncode == 0, script + ' failed: ' + process.stderr)
            return process.stdout
        # The same sanitized environment is inherited by every frozen child script.
        result = read_json(run('audit_release/verify_audit.py',
            '--expected-manifest-sha256', ANCHORS['audit_release'][4],
            '--author-directory', copied / 'release',
            '--author-zip', copied / ANCHORS['release'][0]))
        require(result['result'] == 'PASS' and result['original_author_replayed'] is True, 'complete replay')
        require(result['independent_positive_controls'] == 31 and result['independent_mathematical_negatives'] == 10, 'independent controls')
        require(result['full_riemann_components_checked'] == 81, 'curvature components')
        require(len(result['audit_integrity_mutations_rejected']) == 10, 'audit integrity mutations')
        fresh = read_json(run('audit_release/audit_replay.py', copied / 'release', copied / ANCHORS['release'][0]))
        require(fresh['isolated_author_replay']['exact_assertions'] == 32, 'author checks')
        require(len(fresh['isolated_author_replay']['negative_integrity_controls']) == 7, 'author integrity mutations')
        require(len(fresh['independent_integrity_mutations_rejected']) == 10, 'input integrity mutations')
        controls = read_json(run('test_publication_integrity.py'))
        require(controls['status'] == 'PASS' and controls['control_count'] == 16, 'publication mutation controls')
        return {'author_checks':32,'author_integrity_mutations':7,
                'independent_positive_groups':31,'riemann_components':81,'ricci_components':9,
                'independent_math_negatives':10,'input_integrity_mutations':10,
                'audit_integrity_mutations':10,'publication_integrity_mutations':16,
                'relocated_replay':True,'frozen_scripts_assertions_active':True}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('root', type=Path)
    parser.add_argument('expected_manifest_sha256')
    parser.add_argument('--replay', action='store_true')
    args = parser.parse_args()
    result = {'status':'PASS','scope':'known affirmative construction for printed dimension-unrestricted primary statement only',
              'package_files':verify(args.root,args.expected_manifest_sha256),'wrapper_optimized':bool(sys.flags.optimize)}
    if args.replay:
        result['replay'] = replay(args.root)
        verify(args.root,args.expected_manifest_sha256)
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__ == '__main__':
    main()
