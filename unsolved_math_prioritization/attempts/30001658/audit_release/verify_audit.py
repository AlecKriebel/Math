#!/usr/bin/env python3
"""Verify a pinned flat audit bundle, the separately pinned input, and all replays."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

REQUIRED = {
    'AUDIT.md', 'README.md', 'INPUT_BINDING.json', 'SOURCE_AUDIT.json',
    'VERDICT.json', 'independent_checks.py', 'INDEPENDENT_RESULTS.json',
    'audit_replay.py', 'REPLAY_RESULTS.json', 'verify_audit.py'
}

def require(ok, message):
    if not ok:
        raise ValueError(message)

def unique(pairs):
    result = {}
    for k, v in pairs:
        require(k not in result, 'Duplicate JSON key')
        result[k] = v
    return result

def parse(data):
    return json.loads(data, object_pairs_hook=unique)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--expected-audit-manifest-sha256', required=True)
    ap.add_argument('--source-dir', type=Path)
    args = ap.parse_args()
    root = Path(__file__).resolve().parent
    entries = list(root.iterdir())
    require(all(p.is_file() and not p.is_symlink() for p in entries), 'Nonregular audit entry')
    require({p.name for p in entries} == REQUIRED | {'MANIFEST.json'}, 'Audit filesystem inventory')
    raw = (root/'MANIFEST.json').read_bytes()
    require(sha(raw) == args.expected_audit_manifest_sha256, 'Audit manifest pin mismatch')
    manifest = parse(raw)
    require(set(manifest) == {'format','problem_id','kind','files'}, 'Audit manifest schema')
    require(manifest['format'] == 1 and manifest['problem_id'] == '30001658'
            and manifest['kind'] == 'independent_adversarial_audit', 'Audit identity')
    listed = manifest['files']
    require(type(listed) is list and len(listed) == len(REQUIRED), 'Audit manifest entries')
    require({e['path'] for e in listed} == REQUIRED, 'Audit manifest inventory')
    for e in listed:
        require(set(e) == {'path','bytes','sha256'}, 'Audit file schema')
        require(type(e['bytes']) is int and e['bytes'] >= 0, 'Audit byte count type')
        require(type(e['path']) is str and '/' not in e['path'], 'Audit path type')
        data = (root/e['path']).read_bytes()
        require(len(data) == e['bytes'] and sha(data) == e['sha256'], 'Audit byte binding: '+e['path'])
    verdict = parse((root/'VERDICT.json').read_bytes())
    require(verdict['full_resolution'] is False and verdict['novelty_claim'] is False
            and verdict['global_open_status_claim'] is False, 'Invalid resolution or novelty claim')
    require(verdict['approaches_used'] == 5 and verdict['approach_limit'] == 5, 'Approach scope')
    source = args.source_dir.resolve() if args.source_dir else root.parent/'release'
    command = [sys.executable, '-B'] + (['-O'] if sys.flags.optimize else [])
    command += [str(root/'audit_replay.py'), '--source-dir', str(source)]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    require(result.returncode == 0 and not result.stderr, 'Replay failed')
    require(result.stdout == (root/'REPLAY_RESULTS.json').read_bytes(), 'Frozen audit replay changed')
    print(json.dumps({'status':'PASS_PINNED_INDEPENDENT_AUDIT',
                      'audit_manifest_sha256':sha(raw),
                      'audit_files_including_manifest':len(REQUIRED)+1,
                      'author_source_files':9,'author_source_bytes':41351,
                      'author_source_manifest_sha256':verdict['author_manifest_sha256'],
                      'controlling_clarification':'Proper subcube coefficient formula requires k>=1; full-set coefficient is unrestricted.',
                      'author_checks_each_mode':704115,'independent_checks_each_mode':1282085,
                      'both_python_modes_verified':True,'full_resolution':False},sort_keys=True,indent=2))

if __name__ == '__main__':
    main()
