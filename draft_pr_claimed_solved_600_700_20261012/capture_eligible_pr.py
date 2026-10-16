#!/usr/bin/env python3
"""Read the live eligibility gate before copying an in-scope PR's target files.

No checkout, index change, branch mutation, PR write, or other-problem read.
Non-claimed statuses receive only a skip receipt; their target files are unread.
"""
import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path
import re
import subprocess

PROGRAM = Path(__file__).resolve().parent
REPO = PROGRAM.parent
IDS = {615: '4200010', 618: '30004609', 623: '30001184',
       628: '30000403', 630: '30000700', 662: '2306086',
       672: '6700060', 681: '30003703'}
FIELDS = 'number,state,isDraft,headRefOid,headRefName,baseRefName,isCrossRepository,title,url'


def git(*args):
    return subprocess.check_output(['git', *args], cwd=REPO)


def metadata(number):
    return json.loads(subprocess.check_output(
        ['gh', 'pr', 'view', str(number), '--repo', 'AlecKriebel/Math',
         '--json', FIELDS], cwd=REPO))


def save_skip(number, data):
    folder = PROGRAM / 'eligibility_rechecks'
    folder.mkdir(exist_ok=True)
    path = folder / f'pr{number}.json'
    if path.exists():
        raise ValueError('Existing skip receipt: inspect before replacing')
    path.write_text(json.dumps(data, indent=2) + '\n')
    return data


def capture(number):
    state = json.loads((PROGRAM / 'PROGRAM_STATE.json').read_text())
    if number not in IDS or state['current_pr'] != number:
        raise ValueError('Only the current preidentified eligible candidate is permitted')
    if git('branch', '--show-current').decode().strip() != 'main':
        raise ValueError('Shared checkout must stay on main')
    meta = metadata(number)
    utc = dt.datetime.now(dt.timezone.utc).isoformat()
    if meta['state'] != 'OPEN' or not meta['isDraft']:
        return save_skip(number, {'utc': utc, 'pr': meta,
                                 'status': 'SKIP_NOT_CURRENT_OPEN_DRAFT',
                                 'target_files_read': False})
    if meta['baseRefName'] != 'main' or meta['isCrossRepository']:
        raise ValueError('Unexpected base or cross-repository candidate: inspect')
    head = meta['headRefOid']
    if not re.fullmatch(r'[0-9a-f]{40}', head):
        raise ValueError('Invalid immutable head')
    if subprocess.run(['git', 'cat-file', '-e', head + '^{commit}'],
                      cwd=REPO, stdout=subprocess.DEVNULL,
                      stderr=subprocess.DEVNULL).returncode:
        subprocess.run(['git', 'fetch', '--no-tags', 'origin', head],
                       cwd=REPO, check=True)
    pid = IDS[number]
    queue = git('show', head + ':unsolved_math_prioritization/QUEUE.md').decode()
    rows = [line for line in queue.splitlines() if f'| {pid} /' in line]
    if len(rows) != 1:
        raise ValueError('Selected queue row missing or ambiguous')
    status = rows[0].split('|')[8].strip()
    if status != 'claimed_solved':
        return save_skip(number, {'utc': utc, 'pr': meta,
                                 'status': 'SKIP_NON_CLAIMED_STATUS',
                                 'queue_status': status, 'queue_row': rows[0],
                                 'target_files_read': False})
    audit = PROGRAM / 'audits' / f'pr{number}_{pid}'
    if (audit / 'SCOPE_AND_SNAPSHOT.json').exists():
        raise ValueError('Existing immutable snapshot: inspect; do not overwrite')
    prefix = f'unsolved_math_prioritization/attempts/{pid}/'
    blobs = {}
    content = {}
    for record in git('ls-tree', '-r', '-z', head, '--', prefix).split(b'\0'):
        if not record:
            continue
        description, raw_path = record.split(b'\t', 1)
        mode, kind, oid = description.split()
        name = raw_path.decode()
        if kind != b'blob' or mode not in (b'100644', b'100755'):
            raise ValueError('Nonregular target entry requires inspection')
        if not name.startswith(prefix) or '..' in Path(name).parts:
            raise ValueError('Target path escapes selected attempt')
        data = git('show', head + ':' + name)
        content[name] = data
        blobs[name] = {'size': len(data),
                       'sha256': hashlib.sha256(data).hexdigest(),
                       'git_blob': oid.decode(), 'git_mode': mode.decode()}
    if not blobs:
        raise ValueError('No selected attempt files')
    latest = metadata(number)
    if latest['headRefOid'] != head or latest['state'] != 'OPEN' or not latest['isDraft']:
        raise ValueError('Live PR changed during capture; no snapshot written')
    audit.mkdir(parents=True, exist_ok=True)
    for name, data in content.items():
        destination = audit / 'native' / name
        if destination.exists():
            raise ValueError('Preexisting target path: inspect before writing')
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data)
    result = {'captured_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
              'pr': latest, 'problem_id': pid, 'queue_row': rows[0],
              'status': status, 'original_head': head,
              'original_blobs': blobs}
    (audit / 'SCOPE_AND_SNAPSHOT.json').write_text(json.dumps(result, indent=2) + '\n')
    (audit / 'RESEARCH_LOG.md').write_text(
        f'# PR{number} research log\n\n{result["captured_utc"]} — '
        f'Live exact claimed_solved gate passed; {len(blobs)} immutable target '
        'files captured. No target claim has been accepted or rejected. '
        f'PR completion estimate 10%; shard {state["completion_estimate_percent"]}%.\n')
    return {'status': 'CAPTURED_CLAIMED_SOLVED_ONLY', 'pr': number,
            'problem_id': pid, 'head': head, 'files': len(blobs), 'audit': str(audit)}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pr', type=int)
    args = parser.parse_args()
    print(json.dumps(capture(args.pr), indent=2))
