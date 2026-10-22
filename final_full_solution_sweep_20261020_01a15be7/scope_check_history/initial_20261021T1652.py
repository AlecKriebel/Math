"""Read-only pinned path/added-QUEUE-row binding; never classify or dispose a PR."""
import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path
import subprocess

from advance_clear_exclusions import parse_row
from checkpoint import ensure_commit
from sweep_io import atomic_json

ROOT = Path(__file__).resolve().parent
QUEUE = {'QUEUE.md', 'unsolved_math_prioritization/QUEUE.md'}


def run(args):
    return subprocess.run(args, cwd=ROOT.parent, capture_output=True, check=True).stdout


def check(number):
    inventory = json.loads((ROOT/'rest_inventory.json').read_text())
    pr = next(p for p in inventory['pull_requests'] if p['number'] == number)
    evidence = json.loads((ROOT/f'eligibility/pr{number:04d}.json').read_text())
    if (evidence['pr'] != number or evidence['inventory_head_sha'] != pr['headRefOid']
            or evidence['inventory_base_sha'] != pr['baseRefOid']):
        raise RuntimeError('Inventory/evidence identity mismatch')
    for commit in (pr['baseRefOid'], pr['headRefOid']):
        ensure_commit(commit)
    comparison = pr['baseRefOid']+'...'+pr['headRefOid']
    wire = run(['git', 'diff', '--no-ext-diff', '--no-renames', '--name-only', '-z', comparison])
    paths = wire.decode().rstrip('\0').split('\0') if wire else []
    if len(paths) != len(set(paths)) or set(paths) != set(evidence['changed_paths']):
        raise RuntimeError('Actual pinned complete path set differs from cached inventory')
    rows = []
    blobs = []
    for path in sorted(set(paths) & QUEUE):
        patch = run(['git', 'diff', '--no-ext-diff', '--no-renames', '--unified=0', comparison, '--', path]).decode()
        rows.extend(row for line in patch.splitlines()
                    if line.startswith('+') and not line.startswith('+++')
                    if (row := parse_row(line[1:], path)))
        actual_blob = run(['git', 'rev-parse', pr['headRefOid']+':'+path]).decode().strip()
        old = [q for q in evidence['queue_changes'] if q['path'] == path]
        if len(old) != 1:
            raise RuntimeError('Cached QUEUE scope not unique')
        blobs.append({'path': path, 'actual_head_blob': actual_blob,
                      'cached_blob': old[0]['sha'], 'equal': actual_blob == old[0]['sha'],
                      'actual_pinned_patch_sha256': hashlib.sha256(patch.encode()).hexdigest()})
    key = lambda row: (row['queue_path'], row['source_line'], row['problem_id'], row['status'])
    if sorted(map(key, rows)) != sorted(map(key, evidence['added_queue_rows'])):
        raise RuntimeError('Actual pinned added QUEUE rows differ from cached rows')
    receipt = {
        'timestamp': dt.datetime.now(dt.timezone.utc).isoformat(), 'pr': number,
        'head': pr['headRefOid'], 'base': pr['baseRefOid'], 'comparison': comparison,
        'path_count': len(paths), 'all_complete_paths_equal': True,
        'all_added_rows_equal': True, 'added_queue_rows': rows, 'queue_blobs': blobs,
        'scope': 'Pinned scope only; no live-head, publication, mathematical or priority decision. '
                 'Different cached merged-context QUEUE blobs are disclosed; actual path and added-row equality is required.',
    }
    atomic_json(ROOT/f'PR{number:04d}_PINNED_SCOPE_VERIFICATION.json', receipt)
    return receipt


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pr', type=int)
    print(json.dumps(check(parser.parse_args().pr), indent=2))
