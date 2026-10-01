#!/usr/bin/env python3
"""Read-only frozen-package audit; reruns happen only in an extracted scratch copy.

Run from the package root with its pinned verification/.venv/bin/python.
The only writes are reviews/round2 evidence and tmp/round2 scratch artifacts.
"""
from pathlib import Path
import hashlib
import json
import os
import platform
import shutil
import stat
import subprocess
import sys
import zipfile
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[2]
SCRATCH = ROOT / 'tmp/round2/extracted'
assert SCRATCH.parent == ROOT / 'tmp/round2'
if SCRATCH.exists():
    shutil.rmtree(SCRATCH)
sha = lambda data: hashlib.sha256(data).hexdigest()
expected = {
    'output/pdf/paper.pdf': 'c13dc861e8e5b5c1d980bdd78d14aff8e4b1a130800c4f942b3bedafbc5f6b2a',
    'output/source-and-verification.zip': '0b37678640290c024cd2cb35c9b9620ccdcf2d2076c695f754956794e2558e70',
    'output/zenodo-upload-kit.zip': 'd9f352d8aebf3f1ca4eebc68b1767c322db14554447f20e6e0300b785eb0dd94',
}
out = {'started_utc': datetime.now(timezone.utc).isoformat(), 'frozen': expected}
for name, digest in expected.items():
    assert sha((ROOT / name).read_bytes()) == digest, name
with zipfile.ZipFile(ROOT / 'output/source-and-verification.zip') as z:
    assert z.testzip() is None
    names = z.namelist()
    assert len(names) == len(set(names)) == 78
    for member in z.infolist():
        p = Path(member.filename)
        assert not p.is_absolute() and '..' not in p.parts
        assert not stat.S_ISLNK(member.external_attr >> 16)
        assert not any(part.startswith('.') for part in p.parts)
        assert not any(part in {'__pycache__', 'tmp', 'documents', '.venv'} for part in p.parts)
        assert p.name not in {'web_results_archive.json', 'web_results_archive_addendum.json', 'search_responses.json'}
        assert member.filename == 'verification/source_snapshot/proof.pdf' or p.suffix != '.pdf'
    manifest = json.loads(z.read('PACKAGE_MANIFEST.json'))
    assert set(manifest['files']) == set(names) - {'PACKAGE_MANIFEST.json'}
    for name, entry in manifest['files'].items():
        data = z.read(name)
        assert sha(data) == entry['sha256'] and len(data) == entry['size'], name
        if name != 'api-metadata.json':
            assert (ROOT / name).read_bytes() == data, name
    pdf = (ROOT / 'output/pdf/paper.pdf').read_bytes()
    assert manifest['paper_pdf'] == {'name': 'paper.pdf', 'sha256': sha(pdf), 'size': len(pdf)}
    previous_reviews = [n for n in names if n.startswith('reviews/round1/')]
    assert len(previous_reviews) == 11
    z.extractall(SCRATCH)
    original_archive = {n: z.read(n) for n in names}
out['source_archive'] = {'members': len(names), 'manifest_members': len(manifest['files']),
                         'all_member_hashes_sizes_and_canonical_bytes_match': True,
                         'previous_round_members': previous_reviews,
                         'exclusion_policy_passed': True,
                         'complete_member_list': names}
deposit = json.loads((ROOT / 'zenodo-deposit.json').read_text())
metadata = {'metadata': deposit['metadata']}
assert json.loads(original_archive['api-metadata.json']) == metadata
assert json.loads((ROOT / 'output/api-metadata.json').read_text()) == metadata
with zipfile.ZipFile(ROOT / 'output/zenodo-upload-kit.zip') as z:
    assert z.testzip() is None
    assert set(z.namelist()) == {'SHA256SUMS', 'UPLOAD.md', 'api-metadata.json', 'paper.pdf',
                               'source-and-verification.zip', 'zenodo-deposit.json'}
    assert z.read('paper.pdf') == pdf
    assert z.read('source-and-verification.zip') == (ROOT / 'output/source-and-verification.zip').read_bytes()
    assert json.loads(z.read('api-metadata.json')) == metadata
    kit_deposit = json.loads(z.read('zenodo-deposit.json'))
    assert kit_deposit['metadata'] == deposit['metadata']
    assert kit_deposit['files'] == [{'path': n, 'name': n} for n in ['paper.pdf', 'source-and-verification.zip']]
    sums = z.read('SHA256SUMS')
    assert sums == (ROOT / 'output/SHA256SUMS').read_bytes()
    for line in sums.decode().splitlines():
        digest, name = line.split('  ')
        assert sha(z.read(name)) == digest
out['kit'] = {'all_nested_bytes_metadata_file_paths_and_checksums_match': True}
snap_manifest = json.loads(original_archive['verification/original_snapshot_manifest.json'])
snap_before = {p.name: sha(p.read_bytes()) for p in (SCRATCH / 'verification/source_snapshot').iterdir() if p.is_file()}
assert len(snap_before) == len(snap_manifest['files']) == 16
for entry in snap_manifest['files']:
    archived = original_archive['verification/' + entry['snapshot_path']]
    blob = subprocess.check_output(['git', 'show', snap_manifest['head'] + ':' + entry['repository_path']], cwd=ROOT)
    assert archived == blob and sha(blob) == entry['sha256'], entry['snapshot_path']
out['original_provenance'] = {'head': snap_manifest['head'], 'all_16_files_match_immutable_git_blobs': True}
import sympy, mpmath
assert sympy.__version__ == '1.14.0' and mpmath.__version__ == '1.3.0'
assert sys.flags.optimize == 0
out['environment'] = {'python': platform.python_version(), 'python_implementation': platform.python_implementation(),
                      'platform': platform.platform(), 'sympy': sympy.__version__, 'mpmath': mpmath.__version__,
                      'python_optimization': sys.flags.optimize, 'bytecode_disabled': sys.dont_write_bytecode}
assert (SCRATCH / 'verification/requirements.txt').read_text() == 'sympy==1.14.0\nmpmath==1.3.0\n'
run = subprocess.run([sys.executable, '-B', str(SCRATCH / 'verification/independent_checks.py')],
                     cwd=SCRATCH, capture_output=True)
assert run.returncode == 0 and not run.stderr, run.stderr
(ROOT / 'tmp/round2/independent_rerun.json').write_bytes(run.stdout)
fresh = json.loads(run.stdout)
archived = json.loads(original_archive['verification/independent_results.json'])
for key in ['utc', 'python', 'sympy', 'mpmath']:
    fresh.pop(key); archived.pop(key)
assert fresh == archived
assert (SCRATCH / 'verification/checks_rerun.stdout.json').read_bytes() == original_archive['verification/source_snapshot/checks_output.json']
assert not (SCRATCH / 'verification/checks_rerun.stderr.txt').read_bytes()
snap_after = {p.name: sha(p.read_bytes()) for p in (SCRATCH / 'verification/source_snapshot').iterdir() if p.is_file()}
assert snap_after == snap_before
out['reproduction'] = {'independent_exit': run.returncode, 'stderr_empty': True,
                       'semantic_results_match_archived_except_runtime_timestamp_version_fields': True,
                       'original_child_output_is_byte_identical': True,
                       'all_16_snapshot_files_preserved': True,
                       'independent_stdout_sha256': sha(run.stdout)}
# Restore the scratch reproduction outputs before the deterministic package rebuild.
for n, b in original_archive.items():
    (SCRATCH / n).write_bytes(b)
(SCRATCH / 'output/pdf').mkdir(parents=True, exist_ok=True)
(SCRATCH / 'output/pdf/paper.pdf').write_bytes(pdf)
rebuild = subprocess.run([sys.executable, '-B', str(SCRATCH / 'build_package.py')], cwd=SCRATCH, capture_output=True)
assert rebuild.returncode == 0 and not rebuild.stderr, rebuild.stderr
for name in ['output/source-and-verification.zip', 'output/zenodo-upload-kit.zip']:
    assert sha((SCRATCH / name).read_bytes()) == expected[name], name
out['deterministic_rebuild'] = {'exit': rebuild.returncode, 'stderr_empty': True,
                                'source_and_kit_byte_exact': True}
tracked = subprocess.check_output(['git', 'ls-files', '-z'], cwd=ROOT).decode().split('\0')
assert not any(Path(n).name in {'web_results_archive.json', 'web_results_archive_addendum.json', 'search_responses.json'} for n in tracked)
out['current_git_tree_raw_capture_exclusion'] = True
for name, digest in expected.items():
    assert sha((ROOT / name).read_bytes()) == digest, name
out['canonical_frozen_outputs_preserved'] = True
out['finished_utc'] = datetime.now(timezone.utc).isoformat()
out['status'] = 'all frozen package checks passed'
(ROOT / 'reviews/round2/archive_evidence.json').write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps(out, indent=2))
