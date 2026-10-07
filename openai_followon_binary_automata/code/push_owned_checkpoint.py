#!/usr/bin/env python3
"""Publish owned project paths on remote main without changing shared checkout/index."""
import argparse, json, os, pathlib, subprocess, tempfile
ROOT = pathlib.Path(__file__).resolve().parents[2]
PREFIX = 'openai_followon_binary_automata/'
def run(args, env=None):
    return subprocess.check_output(args, cwd=ROOT, env=env, text=True).strip()
p = argparse.ArgumentParser()
p.add_argument('message')
p.add_argument('paths', nargs='+')
a = p.parse_args()
for path in a.paths:
    q = pathlib.Path(path)
    if q.is_absolute() or '..' in q.parts or not (path + '/').startswith(PREFIX):
        raise SystemExit('Only owned project paths are permitted')
if run(['git','branch','--show-current']) != 'main':
    raise SystemExit('Shared checkout must remain on main')
for attempt in range(10):
    parent = run(['git','ls-remote','origin','refs/heads/main']).split()[0]
    run(['git','fetch','--no-write-fetch-head','origin',parent])
    with tempfile.TemporaryDirectory(prefix='isolated-index-', dir=ROOT/PREFIX/'tmp') as temp:
        env = os.environ.copy()
        env['GIT_INDEX_FILE'] = str(pathlib.Path(temp)/'index')
        run(['git','read-tree',parent],env)
        run(['git','add','--',*a.paths],env)
        changed = run(['git','diff','--cached','--name-only',parent],env).splitlines()
        if any(not x.startswith(PREFIX) for x in changed):
            raise SystemExit('Unexpected non-owned staged path')
        if not changed:
            print(json.dumps({'status':'already_current','parent':parent})); break
        tree = run(['git','write-tree'],env)
        commit = run(['git','commit-tree',tree,'-p',parent,'-m',a.message],env)
        result = subprocess.run(['git','push','origin',f'{commit}:refs/heads/main'],cwd=ROOT,
                                capture_output=True,text=True)
        if result.returncode == 0:
            receipt = {'status':'pushed','parent':parent,'commit':commit,'paths':changed,
                       'shared_checkout_head':run(['git','rev-parse','HEAD']),
                       'shared_branch':run(['git','branch','--show-current'])}
            print(json.dumps(receipt,indent=2)); break
        if not any(x in result.stderr for x in ['fetch first', 'non-fast-forward', "cannot lock ref 'refs/heads/main'"]):
            raise SystemExit(result.stderr)
else:
    raise SystemExit('Concurrent pushes prevented publication after ten safe retries')
