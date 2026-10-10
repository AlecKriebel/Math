#!/usr/bin/env python3
"""Independent binding and adversarial replay of the frozen author packet.

Usage: python3 audit_replay.py AUTHOR_DIRECTORY AUTHOR_ZIP
Requires Python 3 only. Never edits either input. Author code runs only after
matching the pinned manifest and every file fingerprint.
"""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import zipfile

MANIFEST_HASH = 'f15bd36c7ac29f61315054932772b0da76482a3c8119d34b8b645679590da08e'
ZIP_HASH = '861a13e04725c4ba6cfa227fa5a2a8d36e1e16416cec2d9865127f703a6557cb'
ZIP_SIZE = 16542
NAMES = {'EXACT_CHECKS.json', 'MANIFEST.json', 'PRIOR_ATTEMPT_CHECKS.json',
         'PROOF.md', 'README.md', 'RESEARCH_LOG.md', 'SOURCE_VERIFICATION.json',
         'STATUS.json', 'exact_checks.py', 'verify_release.py'}


def require(condition, description):
    if not condition:
        raise ValueError(description)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def verify_directory(root):
    require(root.is_dir() and not root.is_symlink(), 'root must be a directory')
    require({p.name for p in root.iterdir()} == NAMES, 'exact flat inventory')
    require(all(p.is_file() and not p.is_symlink() for p in root.iterdir()),
            'regular nonsymlink files only')
    mb = (root/'MANIFEST.json').read_bytes()
    require(digest(mb) == MANIFEST_HASH, 'pinned author manifest digest')
    manifest = json.loads(mb)
    entries = manifest['files']
    require(len(entries) == 9, 'nine manifest entries')
    require({r['path'] for r in entries} == NAMES-{'MANIFEST.json'}, 'manifest names')
    for row in entries:
        raw = (root/row['path']).read_bytes()
        require(len(raw) == row['bytes'], 'member size')
        require(digest(raw) == row['sha256'], 'member digest')
    status = json.loads((root/'STATUS.json').read_text())
    require(status['problem_id'] == '30002692', 'problem ID')
    require(status['aggregator_statement_verified'] is False, 'aggregator scope')
    require(status['raw_ai_problem_corpora_inspected'] is False, 'corpus scope')
    require(status['novelty_claim'] is False, 'no novelty')
    require(status['substantive_approaches_used'] == 1, 'one approach')
    require(status['independent_audit'] == 'pending', 'immutable author status')
    return manifest


def verify_archive(root, archive):
    require(archive.is_file() and not archive.is_symlink(), 'regular archive')
    raw = archive.read_bytes()
    require(len(raw) == ZIP_SIZE and digest(raw) == ZIP_HASH, 'pinned archive bytes')
    with zipfile.ZipFile(archive) as z:
        names = z.namelist()
        require(len(names) == len(set(names)) == 10, 'unique archive inventory')
        require(set(names) == NAMES, 'archive names')
        require(z.testzip() is None, 'archive CRC')
        for name in names:
            require(z.read(name) == (root/name).read_bytes(), 'archive member equality')


def negative_integrity_controls(root, archive):
    labels = []
    for label in ['delete_proof', 'inject_source_pdf', 'tamper_proof',
                  'tamper_manifest', 'rehash_false_aggregator_claim',
                  'rehash_false_novelty_claim', 'rehash_false_corpus_claim',
                  'rehash_false_approach_count', 'symlink_readme']:
        with tempfile.TemporaryDirectory(prefix='pe-independent-negative-') as d:
            p = Path(d)/'author'
            shutil.copytree(root, p)
            if label == 'delete_proof':
                (p/'PROOF.md').unlink()
            elif label == 'inject_source_pdf':
                (p/'source.pdf').write_bytes(b'negative control, not a source')
            elif label == 'tamper_proof':
                (p/'PROOF.md').write_bytes((p/'PROOF.md').read_bytes()+b'\nmutation\n')
            elif label == 'tamper_manifest':
                (p/'MANIFEST.json').write_bytes((p/'MANIFEST.json').read_bytes()+b'\n')
            elif label == 'symlink_readme':
                (p/'README.md').unlink()
                (p/'README.md').symlink_to(p/'PROOF.md')
            else:
                field = {'rehash_false_aggregator_claim': 'aggregator_statement_verified',
                         'rehash_false_novelty_claim': 'novelty_claim',
                         'rehash_false_corpus_claim': 'raw_ai_problem_corpora_inspected',
                         'rehash_false_approach_count': 'substantive_approaches_used'}[label]
                status = json.loads((p/'STATUS.json').read_text())
                status[field] = 5 if field == 'substantive_approaches_used' else True
                data = (json.dumps(status, sort_keys=True)+'\n').encode()
                (p/'STATUS.json').write_bytes(data)
                manifest = json.loads((p/'MANIFEST.json').read_text())
                for item in manifest['files']:
                    if item['path'] == 'STATUS.json':
                        item.update(bytes=len(data), sha256=digest(data))
                (p/'MANIFEST.json').write_text(json.dumps(manifest)+'\n')
            try:
                verify_directory(p)
            except (ValueError, FileNotFoundError):
                labels.append(label)
            else:
                raise AssertionError('accepted mutation: '+label)
    with tempfile.TemporaryDirectory(prefix='pe-independent-zip-') as d:
        p = Path(d)/'mutated.zip'
        raw = bytearray(archive.read_bytes())
        raw[len(raw)//2] ^= 1
        p.write_bytes(raw)
        try:
            verify_archive(root, p)
        except ValueError:
            labels.append('tamper_archive_byte')
        else:
            raise AssertionError('accepted changed archive')
    return labels


def run(root, archive):
    verify_directory(root)
    verify_archive(root, archive)
    before = {p.name: digest(p.read_bytes()) for p in root.iterdir()}
    with tempfile.TemporaryDirectory(prefix='pe-independent-isolation-') as d:
        copy = Path(d)/'author'
        shutil.copytree(root, copy)
        actual = subprocess.check_output([sys.executable, str(copy/'exact_checks.py')], cwd=copy)
        require(actual == (root/'EXACT_CHECKS.json').read_bytes(), 'byte-identical exact replay')
        author_replay = json.loads(subprocess.check_output(
            [sys.executable, str(copy/'verify_release.py')], cwd=copy))
        require(author_replay['result'] == 'PASS', 'author replay')
        require(author_replay['exact_assertions'] == 32, '32 author checks')
        require(len(author_replay['negative_integrity_controls']) == 7, 'seven author mutations')
    independent_negatives = negative_integrity_controls(root, archive)
    after = {p.name: digest(p.read_bytes()) for p in root.iterdir()}
    require(before == after, 'author files preserved')
    verify_archive(root, archive)
    return {
        'result': 'PASS',
        'author_manifest_sha256': MANIFEST_HASH,
        'author_archive_sha256': ZIP_HASH,
        'author_archive_bytes': ZIP_SIZE,
        'author_manifested_files': 9,
        'author_archive_members': 10,
        'all_archive_members_equal_directory': True,
        'isolated_author_replay': author_replay,
        'independent_integrity_mutations_rejected': independent_negatives,
        'original_inputs_unchanged': True,
        'scope': 'Input integrity and diagnostic replay; independent written geometry remains necessary.'
    }


if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise SystemExit('Usage: audit_replay.py AUTHOR_DIRECTORY AUTHOR_ZIP')
    print(json.dumps(run(Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()),
                     indent=2, sort_keys=True))
