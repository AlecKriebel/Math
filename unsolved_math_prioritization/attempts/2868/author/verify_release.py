#!/usr/bin/env python3
"""Fail-closed package integrity checks. Does not certify mathematical claims."""
import argparse
import hashlib
import json
import pathlib
import shutil
import sys
import tempfile

FILES = frozenset({
    'README.md', 'REPORT.md', 'ATTEMPT_LOG.md', 'INPUT_VERIFICATION.json',
    'SOURCE_METADATA.json', 'STATUS.json', 'verify_release.py', 'MANIFEST.json',
})

class CheckError(Exception):
    pass

def require(condition, message):
    if not condition:
        raise CheckError(message)

def pairs_unique(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'duplicate JSON key')
        result[key] = value
    return result

def read_json(path):
    try:
        return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=pairs_unique)
    except (OSError, ValueError) as exc:
        raise CheckError('unreadable JSON: ' + path.name) from exc

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def verify(root):
    require(root.is_dir() and not root.is_symlink(), 'invalid package directory')
    entries = list(root.iterdir())
    require({p.name for p in entries} == FILES, 'unexpected or missing package member')
    require(all(p.is_file() and not p.is_symlink() for p in entries), 'nonregular or symlink member')
    manifest = read_json(root / 'MANIFEST.json')
    require(set(manifest) == {'schema_version', 'problem_id', 'files'}, 'manifest schema mismatch')
    require(type(manifest['schema_version']) is int and manifest['schema_version'] == 1, 'schema version mismatch')
    require(type(manifest['problem_id']) is int and manifest['problem_id'] == 2868, 'manifest identity mismatch')
    require(isinstance(manifest['files'], dict), 'file records must be an object')
    require(set(manifest['files']) == FILES - {'MANIFEST.json'}, 'manifest member set mismatch')
    for name, row in manifest['files'].items():
        require('/' not in name and '\\' not in name and name not in {'.', '..'}, 'unsafe member path')
        require(isinstance(row, dict) and set(row) == {'bytes', 'sha256'}, 'member record mismatch')
        require(type(row['bytes']) is int and row['bytes'] >= 0, 'invalid byte count')
        require(isinstance(row['sha256'], str) and len(row['sha256']) == 64 and all(c in '0123456789abcdef' for c in row['sha256']), 'invalid digest')
        path = root / name
        require(path.stat().st_size == row['bytes'] and digest(path) == row['sha256'], 'member integrity mismatch: ' + name)
    status = read_json(root / 'STATUS.json')
    require(type(status['problem_id']) is int and status['problem_id'] == 2868, 'status identity mismatch')
    require(status['problem_number'] == 'KP-3.70' and status['rank'] == 915, 'status target mismatch')
    require(status['status'] == 'stalled_partial', 'unsafe mathematical disposition')
    require(type(status['turns_used']) is int and status['turns_used'] == 3 and status['turn_limit'] == 5, 'turn accounting mismatch')
    for name in ('full_problem_solved', 'full_problem_refuted', 'novelty_claim'):
        require(status[name] is False, 'overclaiming status: ' + name)
    inputs = read_json(root / 'INPUT_VERIFICATION.json')
    require(inputs['problem_id'] == 2868 and inputs['gate'] == 'PASS', 'input gate mismatch')
    require(inputs['statement_sha256'] == 'a2c03a6a84ff58dcf8addd47eb50432b6e2de7edf663d55c47521af103df36d4', 'statement hash mismatch')
    require(inputs['record_report_pair_sha256'] == '975b7dad9094fdaba765311a9d0f3891c4c3bb8f00b0ccab2fa4029b61a7f3fe', 'pair hash mismatch')
    return {'result': 'PASS_PACKAGE_INTEGRITY_ONLY', 'problem_id': 2868,
            'bound_files': len(FILES) - 1, 'mathematical_proof_certified': False,
            'source_pdfs_in_package': False}

def update_member(root, name):
    path = root / 'MANIFEST.json'
    value = read_json(path)
    p = root / name
    value['files'][name] = {'bytes': p.stat().st_size, 'sha256': digest(p)}
    path.write_text(json.dumps(value, indent=2) + '\n')

def self_test(root):
    rejected = []
    modes = ['changed_report', 'missing_metadata', 'unexpected_file', 'rehashed_solved_claim',
             'duplicate_json_key', 'unsafe_manifest_path', 'symlink_member']
    for mode in modes:
        with tempfile.TemporaryDirectory(prefix='knot-surgery-release-') as temp:
            target = pathlib.Path(temp) / 'packet'
            shutil.copytree(root, target)
            if mode == 'changed_report':
                with (target / 'REPORT.md').open('a') as handle:
                    handle.write('altered\n')
            elif mode == 'missing_metadata':
                (target / 'SOURCE_METADATA.json').unlink()
            elif mode == 'unexpected_file':
                (target / 'extra.txt').write_text('unapproved file\n')
            elif mode == 'rehashed_solved_claim':
                path = target / 'STATUS.json'
                value = read_json(path)
                value['full_problem_solved'] = True
                path.write_text(json.dumps(value, indent=2) + '\n')
                update_member(target, 'STATUS.json')
            elif mode == 'duplicate_json_key':
                path = target / 'MANIFEST.json'
                text = path.read_text()
                path.write_text(text.replace('{', '{"schema_version": 1,', 1))
            elif mode == 'unsafe_manifest_path':
                path = target / 'MANIFEST.json'
                value = read_json(path)
                value['files']['../REPORT.md'] = value['files'].pop('REPORT.md')
                path.write_text(json.dumps(value, indent=2) + '\n')
            elif mode == 'symlink_member':
                path = target / 'REPORT.md'
                path.unlink()
                path.symlink_to(root / 'REPORT.md')
            try:
                verify(target)
            except (CheckError, OSError, KeyError, TypeError) as exc:
                rejected.append(mode)
            else:
                raise CheckError('negative control accepted: ' + mode)
    return rejected

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    root = pathlib.Path(__file__).resolve().parent
    try:
        result = verify(root)
        if args.self_test:
            result['rejected_negative_controls'] = self_test(root)
        print(json.dumps(result, sort_keys=True, indent=2))
    except (CheckError, OSError, KeyError, TypeError) as exc:
        print('FAIL: ' + str(exc), file=sys.stderr)
        return 1
    return 0

if __name__ == '__main__':
    sys.exit(main())
