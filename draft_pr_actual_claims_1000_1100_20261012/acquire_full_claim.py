"""Freeze a candidate's complete problem tree without touching shared main/index."""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent


def call(arguments, text=False):
    return subprocess.run(arguments, cwd=REPO_ROOT, capture_output=True,
                          text=text, check=True).stdout


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pr', type=int)
    args = parser.parse_args()
    records = json.loads((HERE / 'CLAIM_REGISTRY.json').read_text())['records']
    selected = [r for r in records if r['pr'] == args.pr]
    if len(selected) != 1 or selected[0]['classification'] != 'full_resolution_candidate':
        raise RuntimeError('Only an actually classified full-claim candidate may be acquired')
    problem = str(selected[0]['problem_id'])
    destination = HERE / 'audits' / f'pr{args.pr}_{problem}'
    if (destination / 'SUBMITTED_PINS.json').exists():
        raise RuntimeError('Already pinned; inspect existing records instead of resetting them')
    old = json.loads((HERE / 'intake' / f'pr{args.pr}' / 'pr.json').read_text())
    live = json.loads(call(['gh', 'pr', 'view', str(args.pr), '--repo', 'AlecKriebel/Math',
                           '--json', 'number,title,state,isDraft,headRefOid,headRefName,baseRefName,url,body,files'], True))
    if live['headRefOid'] != old['headRefOid'] or live['state'] != 'OPEN' or not live['isDraft']:
        raise RuntimeError('Live head/state differs from frozen draft intake; reconcile before acquisition')
    head = live['headRefOid']
    if subprocess.run(['git', 'cat-file', '-e', head + '^{commit}'],
                      cwd=REPO_ROOT, capture_output=True).returncode:
        call(['git', 'fetch', '--no-write-fetch-head', 'origin', head])
    root = f'unsolved_math_prioritization/attempts/{problem}'
    paths = call(['git', 'ls-tree', '-r', '--name-only', head, '--', root], True).splitlines()
    if not paths:
        raise RuntimeError('No problem tree at pinned head')
    destination.mkdir(parents=True, exist_ok=True)
    rows = []
    for path in paths:
        relative = Path(path).relative_to(root)
        content = call(['git', 'show', head + ':' + path])
        target = destination / 'submitted' / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
        rows.append({'repository_path': path, 'snapshot_path': target.relative_to(destination).as_posix(),
                     'sha256': hashlib.sha256(content).hexdigest(), 'bytes': len(content)})
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    (destination / 'LIVE_PR_CAPTURE.json').write_text(json.dumps(live, indent=2) + '\n')
    (destination / 'SUBMITTED_PINS.json').write_text(json.dumps({
        'pr': args.pr, 'problem_id': int(problem), 'head_oid': head,
        'captured_utc': now, 'files': rows}, indent=2) + '\n')
    with (destination / 'RESEARCH_LOG.md').open('a') as file:
        file.write(f'\n# PR {args.pr} / problem {problem}: full audit\n\n'
                   f'## {now}: exact full acquisition\n\n'
                   f'All {len(rows)} original files acquired from the full problem tree at '
                   f'unchanged live draft head {head}. Shared main/index untouched. '
                   'Fresh mathematical review pending; asserted claims remain hypotheses. '
                   'Best-guess workflow completion: 10%.\n')
    print(json.dumps({'pr': args.pr, 'problem_id': problem, 'files': len(rows), 'head': head}))


if __name__ == '__main__':
    main()
