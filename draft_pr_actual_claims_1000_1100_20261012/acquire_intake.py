"""Pin PR metadata and claim/scope artifacts without running delivered code."""
import base64
import concurrent.futures
import datetime
import hashlib
import json
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent
REPO = 'AlecKriebel/Math'
PREVIOUS = REPO_ROOT / 'draft_pr_claimed_solved_1000_1100_20261012/inventory.json'

def gh(*args):
    return subprocess.check_output(['gh', *args], cwd=REPO_ROOT, text=True)

def content(sha, path):
    present = subprocess.run(['git', 'cat-file', '-e', f'{sha}:{path}'], cwd=REPO_ROOT, capture_output=True)
    if present.returncode == 0:
        return subprocess.check_output(['git', 'show', f'{sha}:{path}'], cwd=REPO_ROOT)
    obj = json.loads(gh('api', f'repos/{REPO}/contents/{path}?ref={sha}'))
    if obj.get('encoding') != 'base64':
        raise ValueError(f'Cannot obtain pinned bytes: {path}')
    return base64.b64decode(obj['content'])

def acquire(old):
    n = old['number']
    target = HERE / 'intake' / f'pr{n}'
    target.mkdir(parents=True, exist_ok=True)
    if (target / 'pr.json').exists():
        p = json.loads((target / 'pr.json').read_text())
    else:
        p = json.loads(gh('pr', 'view', str(n), '--repo', REPO, '--json',
                         'number,title,state,isDraft,headRefName,headRefOid,baseRefName,url,body,files'))
    (target / 'pr.json').write_text(json.dumps(p, indent=2) + '\n')
    root = f'unsolved_math_prioritization/attempts/{old["problem_id"]}/'
    selected = []
    for f in p['files']:
        path = f['path']
        if not path.startswith(root):
            continue
        relative = path[len(root):]
        # Scope and core authored claim documents, not bulky runner receipts.
        if (relative in ['SCOPE.json', 'README.md', 'ACCEPTANCE.md', 'CLAIM.md',
                         'STATUS.json', 'TARGET_STATUS.json', 'REPORT.md', 'PROOF.md', 'PROOF_APPLICATION.md']
                or (relative.startswith('original/') and relative.endswith('.md')
                    and any(x in Path(relative).name.upper() for x in ['README', 'CLAIM', 'PROOF', 'SCOPE', 'RESULT']))):
            data = content(p['headRefOid'], path)
            destination = target / 'artifacts' / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(data)
            selected.append({'repository_path': path, 'local_relative_path': destination.relative_to(HERE).as_posix(),
                             'size': len(data), 'sha256': hashlib.sha256(data).hexdigest()})
    receipt = {k: p[k] for k in ['number', 'title', 'state', 'isDraft', 'headRefOid', 'headRefName', 'url']}
    receipt.update(problem_id=old['problem_id'], artifacts=selected,
                   head_changed_since_status_pass=p['headRefOid'] != old['headRefOid'])
    (target / 'PINS.json').write_text(json.dumps(receipt, indent=2) + '\n')
    return receipt

def main():
    previous = json.loads(PREVIOUS.read_text())['prs']
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        for p in pool.map(acquire, previous):
            results.append(p)
            if len(results) % 20 == 0:
                print(json.dumps({'pinned': len(results), 'total': len(previous)}), flush=True)
    (HERE / 'INTAKE_INDEX.json').write_text(json.dumps({'captured_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'range': [1000, 1100], 'prs': results}, indent=2) + '\n')
    print(json.dumps({'pinned': len(results), 'changed_heads': [p['number'] for p in results if p['head_changed_since_status_pass']]}))

if __name__ == '__main__':
    main()
