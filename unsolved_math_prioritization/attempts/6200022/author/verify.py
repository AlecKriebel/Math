#!/usr/bin/env python3
"""Fail-closed, optimization-safe, CWD-independent integrity and exact replay."""
from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys

FILES = {'README.md', 'RESULT.md', 'RESEARCH_LOG.md', 'PUBLIC_METADATA.json',
         'CHECK_RESULTS.json', 'check_math.py', 'verify.py', 'VERIFY_TESTS.json'}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def no_duplicates(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, 'duplicate JSON key: '+key)
        result[key] = value
    return result


def load(path):
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=no_duplicates)


def main():
    root = Path(__file__).resolve().parent
    require(not Path(__file__).is_symlink(), 'verifier may not be a symlink')
    expected = FILES | {'MANIFEST.json'}
    found = {entry.name for entry in root.iterdir()}
    require(found == expected, 'directory allowlist mismatch')
    for name in expected:
        path = root/name
        require(not path.is_symlink() and path.is_file(), 'non-regular or symlink payload: '+name)
    manifest = load(root/'MANIFEST.json')
    require(set(manifest) == {'schema','problem_id','algorithm','coverage','files'}, 'manifest schema keys')
    require(manifest['schema'] == 1 and type(manifest['schema']) is int, 'manifest version')
    require(manifest['problem_id'] == '6200022', 'manifest target')
    require(manifest['algorithm'] == 'sha256', 'manifest algorithm')
    require(manifest['coverage'] == 'All payload files except MANIFEST.json itself.', 'coverage')
    require(type(manifest['files']) is dict and set(manifest['files']) == FILES, 'manifest file allowlist')
    for name, info in manifest['files'].items():
        require(re.fullmatch(r'[A-Za-z0-9_.-]+',name) is not None, 'unsafe filename')
        require(type(info) is dict and set(info) == {'bytes','sha256'}, 'file entry schema')
        require(type(info['bytes']) is int and info['bytes'] > 0, 'invalid byte count')
        require(type(info['sha256']) is str and re.fullmatch(r'[0-9a-f]{64}',info['sha256']) is not None, 'invalid hash')
        data = (root/name).read_bytes()
        require(len(data) == info['bytes'], 'byte count mismatch: '+name)
        require(hashlib.sha256(data).hexdigest() == info['sha256'], 'hash mismatch: '+name)
    metadata = load(root/'PUBLIC_METADATA.json')
    require(metadata['identity']['id'] == '6200022', 'identity id')
    require(metadata['identity']['problem_number'] == 'AMR-061-0022', 'identity number')
    require(metadata['identity']['complete_record_review_sha256'] ==
            '14935ce8c0a28dc4f82299acb615159f9c02d1373854aaeda75f545db8efb245', 'complete review digest')
    require(metadata['disposition']['classification'] == 'already_solved', 'classification')
    require(metadata['disposition']['novel_solution_claimed'] is False, 'novelty scope')
    cmd = [sys.executable, '-I']
    if sys.flags.optimize:
        cmd.append('-O')
    cmd.append(str(root/'check_math.py'))
    replay = subprocess.run(cmd, check=True, capture_output=True, text=True, cwd='/')
    actual = json.loads(replay.stdout, object_pairs_hook=no_duplicates)
    require(actual == load(root/'CHECK_RESULTS.json'), 'exact result replay mismatch')
    require(actual['status'] == 'pass', 'math check failed')
    print(json.dumps({'status':'pass','problem_id':'6200022','manifest_files':len(FILES),
                      'exact_checks':actual['total_checks'],'optimized':bool(sys.flags.optimize)},sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print('FAIL: '+str(exc), file=sys.stderr)
        sys.exit(1)
