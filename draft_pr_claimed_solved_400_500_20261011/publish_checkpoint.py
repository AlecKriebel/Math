#!/usr/bin/env python3
"""Publish only explicitly listed program files to remote main, without its index."""
import argparse
import base64
import datetime
import hashlib
import json
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPOSITORY_ROOT = ROOT.parent
REPO = 'AlecKriebel/Math'

def api(endpoint, payload=None):
    cmd = ['gh', 'api', f'repos/{REPO}/{endpoint}']
    if payload is not None:
        cmd += ['--method', 'POST' if endpoint != 'git/refs/heads/main' else 'PATCH', '--input', '-']
    p = subprocess.run(cmd, input=None if payload is None else json.dumps(payload), text=True,
                       capture_output=True)
    if p.returncode:
        raise RuntimeError(p.stderr.strip())
    return json.loads(p.stdout)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file-list', type=Path, required=True,
                        help='JSON list of repository-relative files in this program only')
    parser.add_argument('--message', required=True)
    parser.add_argument('--receipt', type=Path, required=True)
    args = parser.parse_args()
    candidate_path = args.receipt.with_suffix('.candidate.json')
    if args.receipt.exists() or candidate_path.exists():
        raise ValueError('checkpoint already attempted; preserve receipts and reconcile with GETs')
    paths = json.loads(args.file_list.read_text())
    if not paths or len(paths) != len(set(paths)):
        raise ValueError('file list must be nonempty and unique')
    entries, hashes, prepared = [], {}, []
    excluded = {'private_sources', 'mutation_fixtures', '.secrets', '.zenodo-state', '__pycache__'}
    for rel in paths:
        unresolved = REPOSITORY_ROOT / rel
        p = unresolved.resolve()
        if not p.is_relative_to(ROOT) or not unresolved.is_file() or unresolved.is_symlink():
            raise ValueError(f'path outside this program or not a regular file: {rel}')
        if (any(part in excluded for part in Path(rel).parts)
                or any(part in excluded for part in p.relative_to(ROOT).parts)
                or p.suffix == '.pyc'):
            raise ValueError(f'excluded working-copy or credential path: {rel}')
        b = p.read_bytes()
        hashes[rel] = hashlib.sha256(b).hexdigest()
        prepared.append((rel, b))
    # Validate the entire selection before creating any remote blob.
    for rel, b in prepared:
        sha = api('git/blobs', {'content': base64.b64encode(b).decode(), 'encoding': 'base64'})['sha']
        entries.append({'path': rel, 'mode': '100644', 'type': 'blob', 'sha': sha})
    # A non-forced main-ref update fails if another writer advanced main after
    # the captured parent; it cannot overwrite that writer's history.
    main_sha = api('git/ref/heads/main')['object']['sha']
    parent = api(f'git/commits/{main_sha}')
    tree = api('git/trees', {'base_tree': parent['tree']['sha'], 'tree': entries})['sha']
    commit = api('git/commits', {'message': args.message, 'tree': tree, 'parents': [main_sha]})['sha']
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    with candidate_path.open('x') as candidate:
        json.dump({'commit_sha': commit, 'parent_main_sha': main_sha,
                   'files_sha256': hashes, 'next_action': 'one nonforce main PATCH'}, candidate, indent=2)
        candidate.write('\n'); candidate.flush(); os.fsync(candidate.fileno())
    api('git/refs/heads/main', {'sha': commit, 'force': False})
    readback = api('git/ref/heads/main')['object']['sha']
    # Read-back main may already have moved forward under concurrent work.
    comparison = api(f'compare/{commit}...{readback}') if readback != commit else None
    if comparison and comparison['status'] not in ('ahead', 'identical'):
        raise RuntimeError('published checkpoint is not an ancestor of remote main')
    receipt = {'published_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
               'parent_main_sha': main_sha, 'commit_sha': commit, 'readback_main_sha': readback,
               'url': f'https://github.com/{REPO}/commit/{commit}', 'files_sha256': hashes,
               'branch': 'main', 'method': 'GitHub Git-data API, non-forced update; shared index untouched'}
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({'checkpoint_commit': commit, 'url': receipt['url'], 'file_count': len(paths)}, indent=2))

if __name__ == '__main__':
    main()
