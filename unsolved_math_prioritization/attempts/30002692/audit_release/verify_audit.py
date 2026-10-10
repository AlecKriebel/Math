#!/usr/bin/env python3
"""Verify audit integrity, conservative scope, fresh diagnostics and mutations."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

FILES = {'AUDIT.md', 'README.md', 'INPUT_BINDING.json', 'SOURCE_AUDIT.json',
         'VERDICT.json', 'INDEPENDENT_RESULTS.json', 'REPLAY_RESULTS.json',
         'independent_checks.py', 'audit_replay.py', 'verify_audit.py'}
AUTHOR_MANIFEST = 'f15bd36c7ac29f61315054932772b0da76482a3c8119d34b8b645679590da08e'
AUTHOR_ZIP = '861a13e04725c4ba6cfa227fa5a2a8d36e1e16416cec2d9865127f703a6557cb'


def require(condition, name):
    if not condition:
        raise ValueError(name)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def verify_integrity(root, expected_manifest=None):
    require({p.name for p in root.iterdir()} == FILES | {'MANIFEST.json'}, 'exact inventory')
    require(all(p.is_file() and not p.is_symlink() for p in root.iterdir()), 'regular files')
    mb = (root/'MANIFEST.json').read_bytes()
    if expected_manifest:
        require(digest(mb) == expected_manifest, 'externally pinned audit manifest')
    m = json.loads(mb)
    require(m['schema'] == 'pe-boundary-independent-audit-freeze-v1', 'manifest schema')
    require(len(m['files']) == len(FILES), 'entry count')
    require({r['path'] for r in m['files']} == FILES, 'manifest inventory')
    for row in m['files']:
        raw = (root/row['path']).read_bytes()
        require(len(raw) == row['bytes'], 'file size: '+row['path'])
        require(digest(raw) == row['sha256'], 'file hash: '+row['path'])
    v = json.loads((root/'VERDICT.json').read_text())
    require(v['problem_id'] == '30002692', 'problem identity')
    require(v['verdict'] == 'APPROVE_FOR_PRINTED_PRIMARY_STATEMENT', 'primary-only verdict')
    require(v['recommended_disposition'] == 'already_solved', 'known construction')
    require(v['novelty_claim'] is False and v['new_proof_or_discovery_claim'] is False, 'no novelty')
    require(v['aggregator_statement_verified'] is False, 'aggregator limitation')
    require(v['raw_ai_problem_corpora_inspected'] is False, 'corpus limitation')
    require(v['unqualified_current_aggregator_status_approved'] is False, 'no scope upgrade')
    require(v['substantive_approaches_used'] == 1 and v['approach_limit'] == 5, 'approach accounting')
    require(v['bulk_dimension'] == 3 and v['boundary_components'] == 1, 'geometric scope')
    require(v['parent_acceptance'] == 'pending', 'audit does not impersonate acceptance')
    b = json.loads((root/'INPUT_BINDING.json').read_text())
    require(b['author_manifest_sha256'] == AUTHOR_MANIFEST, 'author manifest binding')
    require(b['author_archive']['sha256'] == AUTHOR_ZIP and b['author_archive']['bytes'] == 16542,
            'author archive binding')
    s = json.loads((root/'SOURCE_AUDIT.json').read_text())
    require(len(s['sources']) == 3, 'three primary sources')
    require(all(x['source_files_included'] is False for x in s['sources']), 'no source files')
    require(s['aggregator']['statement_equality_verified'] is False, 'source equality scope')
    require(s['raw_ai_problem_corpora_inspected'] is False, 'source corpus scope')


def rehash(root, name):
    m = json.loads((root/'MANIFEST.json').read_text())
    raw = (root/name).read_bytes()
    for row in m['files']:
        if row['path'] == name:
            row.update(bytes=len(raw), sha256=digest(raw))
    (root/'MANIFEST.json').write_text(json.dumps(m)+'\n')


def negatives(root):
    labels = []
    for label in ['changed_proof', 'missing_proof', 'extra_pdf',
                  'coherent_novelty_upgrade', 'coherent_aggregator_upgrade',
                  'coherent_corpus_upgrade', 'coherent_five_approaches',
                  'coherent_false_parent_acceptance', 'coherent_binding_change',
                  'coherent_source_equality_upgrade']:
        with tempfile.TemporaryDirectory(prefix='pe-audit-negative-') as d:
            p = Path(d)/'audit'
            shutil.copytree(root, p)
            if label == 'changed_proof':
                (p/'AUDIT.md').write_bytes((p/'AUDIT.md').read_bytes()+b'\nchanged\n')
            elif label == 'missing_proof':
                (p/'AUDIT.md').unlink()
            elif label == 'extra_pdf':
                (p/'source.pdf').write_bytes(b'negative control only')
            else:
                name = 'VERDICT.json'
                if label == 'coherent_binding_change':
                    name = 'INPUT_BINDING.json'
                elif label == 'coherent_source_equality_upgrade':
                    name = 'SOURCE_AUDIT.json'
                obj = json.loads((p/name).read_text())
                changes = {
                    'coherent_novelty_upgrade': ('novelty_claim', True),
                    'coherent_aggregator_upgrade': ('aggregator_statement_verified', True),
                    'coherent_corpus_upgrade': ('raw_ai_problem_corpora_inspected', True),
                    'coherent_five_approaches': ('substantive_approaches_used', 5),
                    'coherent_false_parent_acceptance': ('parent_acceptance', 'accepted'),
                    'coherent_binding_change': ('author_manifest_sha256', '0'*64),
                }
                if label == 'coherent_source_equality_upgrade':
                    obj['aggregator']['statement_equality_verified'] = True
                else:
                    key, value = changes[label]
                    obj[key] = value
                (p/name).write_text(json.dumps(obj)+'\n')
                rehash(p, name)
            try:
                verify_integrity(p)
            except (ValueError, FileNotFoundError):
                labels.append(label)
            else:
                raise AssertionError('accepted audit mutation: '+label)
    return labels


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--expected-manifest-sha256')
    parser.add_argument('--author-directory', type=Path)
    parser.add_argument('--author-zip', type=Path)
    args = parser.parse_args()
    require(bool(args.author_directory) == bool(args.author_zip), 'supply both author paths')
    root = Path(__file__).resolve().parent
    verify_integrity(root, args.expected_manifest_sha256)
    result = subprocess.check_output([sys.executable, str(root/'independent_checks.py')], cwd=root)
    require(result == (root/'INDEPENDENT_RESULTS.json').read_bytes(), 'fresh independent replay equality')
    fresh = json.loads(result)
    require(fresh['result'] == 'PASS', 'fresh independent replay')
    author_replayed = False
    if args.author_directory:
        output = subprocess.check_output([sys.executable, str(root/'audit_replay.py'),
                                          str(args.author_directory.resolve()),
                                          str(args.author_zip.resolve())], cwd=root)
        require(output == (root/'REPLAY_RESULTS.json').read_bytes(), 'fresh author replay equality')
        author_replayed = True
    print(json.dumps({'result': 'PASS', 'manifested_audit_files': len(FILES),
                      'independent_positive_controls': fresh['independent_positive_controls'],
                      'independent_mathematical_negatives': fresh['independent_negative_controls'],
                      'full_riemann_components_checked': fresh['full_riemann_components_checked'],
                      'audit_integrity_mutations_rejected': negatives(root),
                      'original_author_replayed': author_replayed,
                      'audit_manifest_sha256': digest((root/'MANIFEST.json').read_bytes()),
                      'scope': 'Integrity and exact diagnostics only; the written proof and source-scope judgment remain necessary.'},
                     indent=2, sort_keys=True))
