"""Freeze the exact original PR40 input without changing shared research state."""
from pathlib import Path
import datetime, hashlib, json, subprocess

ROOT = Path('/Users/alec/Documents/Math')
HERE = Path(__file__).resolve().parent
PREFIX = 'unsolved_math_prioritization/attempts/2814/'
HEAD = '163e34d566d6cbaee3a2a8fdc6394fbb9e49a539'
sha = lambda b: hashlib.sha256(b).hexdigest()

def run(*args):
    return subprocess.check_output(args, cwd=ROOT)

def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    assert not path.exists(), 'Never replace an original snapshot: ' + str(path)
    path.write_bytes(data)

def main():
    assert run('git', 'branch', '--show-current').decode().strip() == 'main'
    main_head = run('git', 'rev-parse', 'HEAD').decode().strip()
    remote = run('gh', 'pr', 'view', '40', '--repo', 'AlecKriebel/Math', '--json',
                 'number,state,isDraft,title,headRefName,headRefOid,baseRefName,files,body')
    metadata = json.loads(remote)
    assert metadata['headRefOid'] == HEAD and metadata['state'] == 'OPEN' and metadata['isDraft']
    assert run('git', 'rev-parse', 'origin/pr40-audit').decode().strip() == HEAD
    base = run('git', 'merge-base', main_head, HEAD).decode().strip()
    diff = run('git', 'diff', base, HEAD)
    changed = run('git', 'diff', '--name-only', base, HEAD).decode().splitlines()
    assert set(changed) == {f['path'] for f in metadata['files']}
    assert len(changed) == 14 and all(p == 'unsolved_math_prioritization/QUEUE.md' or p.startswith(PREFIX) for p in changed)
    save(HERE / 'pr_input/metadata.json', remote + b'\n')
    save(HERE / 'pr_input/diff.patch', diff)
    records = []
    for path in changed:
        if not path.startswith(PREFIX):
            continue
        rel = path[len(PREFIX):]
        data = run('git', 'show', HEAD + ':' + path)
        mode, kind, blob_path = run('git', 'ls-tree', HEAD, path).decode().split(None, 2)
        blob, actual_path = blob_path.split('\t', 1)
        assert kind == 'blob' and mode == '100644' and actual_path.strip() == path
        save(HERE / 'source_snapshot' / rel, data)
        records.append({'path': rel, 'mode': mode, 'git_blob': blob, 'sha256': sha(data), 'size': len(data)})
    assert len(records) == 13
    utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
    manifest = {'created_at': utc, 'pr': 40, 'problem': '2814', 'head': HEAD,
                'base': base, 'main_at_start': main_head, 'changed_paths': changed,
                'diff_bytes': len(diff), 'diff_sha256': sha(diff), 'files': records,
                'scope': 'Exact original13 numeric Git artifacts/14 changed paths. Read-only remote inspection; no branch switch, shared queue/state/history change, or new research turn.'}
    save(HERE / 'snapshot_manifest.json', (json.dumps(manifest, indent=2) + '\n').encode())
    save(HERE / 'RESEARCH_LOG.md', ('# PR40 audit log\n\n' + utc +
         ' — workflow10%: original head/base/14 paths and13 numeric artifacts frozen byte-exact. Mathematical and exact-target audit begins; unresolved partial findings remain hypotheses. No acceptance, paper, DOI, or new substantive research route.\n').encode())
    print(json.dumps({'utc': utc, 'head': HEAD, 'base': base, 'members': len(records), 'diff_bytes': len(diff), 'manifest_sha256': sha((HERE / 'snapshot_manifest.json').read_bytes())}, indent=2))

if __name__ == '__main__':
    main()
