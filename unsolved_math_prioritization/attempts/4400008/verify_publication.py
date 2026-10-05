#!/usr/bin/env python3
"""Portable integrity and exact-output replay; not a theorem proof certificate."""
import hashlib
import json
from pathlib import Path, PurePosixPath
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
PINS = {
    'author': ('0d9b8a4ad752b292c4d59b262b08090478df48a303959c2de41d612387f045b6', 8, 56661),
    'independent_audit': ('9e9c5001c3c568a1dad07e7cda8cce9f334d6649273c5b8fcca2cbceb26b85c3', 9, 45526),
}


def need(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        need(key not in result, 'duplicate JSON key: ' + key)
        result[key] = value
    return result


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=unique_object)


def inventory(root, manifest_name):
    manifest = read_json(root / manifest_name)
    expected = {}
    for row in manifest['files']:
        name = row['path']
        p = PurePosixPath(name)
        need(name and not p.is_absolute() and '..' not in p.parts and '\\' not in name
             and name == p.as_posix() and name != manifest_name, 'unsafe manifest path')
        need(name not in expected, 'duplicate manifest path')
        expected[name] = row
    entries = list(root.rglob('*'))
    need(not any(p.is_symlink() for p in entries), 'symlink in packet')
    need(all(p.is_file() or p.is_dir() for p in entries), 'nonregular packet entry')
    actual = {p.relative_to(root).as_posix() for p in entries if p.is_file()}
    need(actual == set(expected) | {manifest_name}, 'strict inventory mismatch')
    for name, row in expected.items():
        data = (root / name).read_bytes()
        need(len(data) == row['bytes'] and sha(data) == row['sha256'], 'content mismatch: ' + name)
    return len(actual), sum((root / name).stat().st_size for name in actual)


def integrity():
    count, total = inventory(ROOT, 'PUBLICATION_MANIFEST.json')
    for folder, (digest, files, size) in PINS.items():
        root = ROOT / folder
        need(sha((root / 'manifest.json').read_bytes()) == digest, 'frozen manifest identity: ' + folder)
        need(inventory(root, 'manifest.json') == (files, size), 'frozen inventory: ' + folder)
    binding = read_json(ROOT / 'independent_audit/binding.json')
    need(binding['manifest_sha256'] == PINS['author'][0], 'audit input manifest binding')
    need((binding['input_file_count'], binding['input_total_bytes']) == PINS['author'][1:], 'audit input dimensions')
    names = [r['path'] for r in binding['input_files']]
    need(len(names) == len(set(names)) == 8, 'audit binding inventory')
    need(set(names) == {p.name for p in (ROOT / 'author').iterdir()}, 'audit input names')
    for row in binding['input_files']:
        data = (ROOT / 'author' / row['path']).read_bytes()
        need(len(data) == row['bytes'] and sha(data) == row['sha256'], 'audit input byte binding')
    verdict = read_json(ROOT / 'independent_audit/results.json')
    need(verdict['verdict'] == 'PASS_AS_UNSOLVED_5_OF_5_DOCUMENTED_APPROACHES', 'audit disposition')
    need(not verdict['full_resolution'] and not verdict['counterexample_to_original_problem']
         and not verdict['novelty_certified'] and not verdict['global_openness_certified'], 'scope guard')
    return count, total


def replay():
    rows = []
    for script, expected, metric, value in [
        ('author/verify.py', 'author/verification.json', 'assertions', 9198),
        ('independent_audit/independent_controls.py', 'independent_audit/independent_results.json', 'assertions', 165565),
        ('independent_audit/negative_controls.py', 'independent_audit/negative_results.json', 'deliberate_faults_rejected', 5),
    ]:
        # Always run original controls normally. -I ignores PYTHONOPTIMIZE,
        # and omission of -O keeps the original negative-control asserts active.
        run = subprocess.run([sys.executable, '-I', '-B', str(ROOT / script)],
                             cwd=ROOT / Path(script).parent, capture_output=True, check=True, timeout=180)
        need(run.stdout == (ROOT / expected).read_bytes(), 'replay output mismatch: ' + script)
        result = json.loads(run.stdout, object_pairs_hook=unique_object)
        need(result[metric] == value, 'control count mismatch')
        rows.append({'script': script, 'byte_exact_output_match': True, metric: value,
                     'output_bytes': len(run.stdout), 'output_sha256': sha(run.stdout)})
    return rows


def main():
    need(sys.argv[1:] in ([], ['--integrity-only']), 'usage: verify_publication.py [--integrity-only]')
    count, _ = integrity()
    result = {'target_id': '4400008', 'result': 'PASS', 'files_verified': count,
              'strict_inventory': True, 'frozen_packets': 2, 'frozen_files': 17,
              'frozen_total_bytes': 102187, 'status': 'unsolved', 'turns': '5/5',
              'theorem_proof': False, 'source_pdfs_retrieved_by_this_script': False}
    if not sys.argv[1:]:
        result['replays'] = replay()
        result['original_controls_run_with_assertions_enabled'] = True
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
