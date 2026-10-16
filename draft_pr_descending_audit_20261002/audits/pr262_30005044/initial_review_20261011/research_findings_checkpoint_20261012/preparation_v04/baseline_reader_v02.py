#!/usr/bin/env python3
"""Independent literal current baselines. Provider access is GET/fetch only.

No working repository metadata, implicit object discovery, or provider mutation.
All output paths are preflighted before private Git initialization or network.
"""
import base64
import datetime as dt
import gzip
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess

ROOT = Path('/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr262_30005044/initial_review_20261011/credited_integration_preparation_20261012')
PROGRAM = ROOT.parents[3]
DRIVER = ROOT / 'reader.git'
OBJECTS = ROOT / 'private_objects'
URL = 'https://github.com/AlecKriebel/Math.git'
REPO = 'AlecKriebel/Math'
MAIN = 'adc6d1441ea42af49a9fe296e52358257c087993'
MAIN_TREE = '26ab7153f7589e1b70e67603c3ae74cd33e480cb'
PARENT = '1de8c8d02861ffd90f91c351fbf603fd39764a5f'
AUTHOR = '6ebe8222a1fabab97ff59885968bd8c8158d5d9f'
ORIGINAL = 'c805fbb48db939b82c59609c0b8be6cdcedd40e7'
TARGET = b'unsolved_math_prioritization/attempts/30005044'
TARGET_TREE = '430f0d154546eaa33c0b7eeb0ad29718b62968c4'
ALTERNATES = [ROOT.parent / 'research_checkpoint_20261012/preparation_family/private_objects',
 PROGRAM / 'audits/pr263_30000170/initial_review_20261011/publication_checkpoint_20261011/private_objects',
 PROGRAM / 'audits/pr263_30000170/initial_review_20261011/integration_preparation/private_objects',
 PROGRAM / 'audits/pr278_30005468/resume_20261011/checkpoint_resume/private_objects',
 PROGRAM / 'audits/pr278_30005468/resume_20261011/reconciliation/private_objects',
 PROGRAM / 'audits/pr278_30005468/resume_20261011/objects.git/objects']

def require(ok, message):
    if not ok: raise ValueError(message)

def literal(path, absent=False):
    path = Path(path)
    require(path.is_absolute() and '..' not in path.parts, 'Nonliteral path')
    for p in reversed([path, *path.parents]):
        if p.exists() or p.is_symlink():
            require(not stat.S_ISLNK(p.lstat().st_mode), 'Symlink before access: ' + str(p))
    require(not absent or not path.exists(), 'Output exists: ' + str(path))
    return path

def guard_store(path):
    literal(path)
    if not path.exists(): return False
    require(path.is_dir(), 'Object store is not directory')
    for name in ('info/alternates', 'info/http-alternates'):
        p = path / name; literal(p)
        require(not p.exists(), 'Implicit/nested alternate rejected: ' + str(p))
    for parent, dirs, files in os.walk(path, followlinks=False):
        for name in dirs + files:
            p = Path(parent) / name
            require(not stat.S_ISLNK(p.lstat().st_mode), 'Store symlink rejected: ' + str(p))
    return True

def oid(kind, body):
    return hashlib.sha1(kind.encode() + b' ' + str(len(body)).encode() + b'\0' + body).hexdigest()

def encode(entries):
    keys = sorted(entries, key=lambda n: n + (b'/' if entries[n][0] == b'40000' else b''))
    return b''.join(entries[n][0] + b' ' + n + b'\0' + bytes.fromhex(entries[n][1]) for n in keys)

def census(entries):
    return b''.join(m + b' ' + h.encode() + b'\t' + p + b'\0' for p, (m, h) in sorted(entries.items()))

def fresh_bytes(name, body):
    p = literal(ROOT / name, absent=True)
    require(p.is_relative_to(ROOT), 'Output outside owned folder')
    with p.open('xb') as f: f.write(body)

def fresh_json(name, value):
    fresh_bytes(name, (json.dumps(value, indent=2) + '\n').encode())

def sanitized(alternates):
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_SYSTEM='/dev/null', GIT_CONFIG_NOSYSTEM='1',
      GIT_NO_LAZY_FETCH='1', GIT_TERMINAL_PROMPT='0', GIT_OPTIONAL_LOCKS='0',
      GIT_ATTR_NOSYSTEM='1', GIT_OBJECT_DIRECTORY=str(OBJECTS),
      GIT_ALTERNATE_OBJECT_DIRECTORIES=os.pathsep.join(map(str, alternates)))
    return env

def inspect_driver():
    literal(DRIVER)
    for rel in ('commondir', 'gitdir', 'worktrees', 'config.worktree', 'objects/info/alternates', 'objects/info/http-alternates'):
        p = literal(DRIVER / rel); require(not p.exists(), 'Implicit driver state rejected')
    for parent, dirs, files in os.walk(DRIVER, followlinks=False):
        for name in dirs + files:
            p = Path(parent) / name
            require(not stat.S_ISLNK(p.lstat().st_mode), 'Driver symlink rejected')
    guard_store(OBJECTS)
    guard_store(DRIVER / 'objects')
    config = literal(DRIVER / 'config').read_text()
    sections = re.findall(r'^\[([^\]]+)\]$', config, flags=re.M)
    require(set(sections) <= {'core', 'remote "' + URL + '"'}, 'Unapproved driver config sections')
    require(not re.search(r'include|worktree|alternates|command|url\s*=|pushurl|fetch\s*=', config, re.I),
            'Unapproved driver config/inclusion')
    for line in config.splitlines():
        s = line.strip()
        if not s or s.startswith('['): continue
        key, val = [v.strip() for v in s.split('=', 1)]
        require((key, val) in {('repositoryformatversion', '0'), ('repositoryformatversion', '1'), ('filemode', 'true'), ('bare', 'true'),
          ('ignorecase', 'true'), ('precomposeunicode', 'true'),
          ('promisor', 'true'), ('partialclonefilter', 'blob:none')}, 'Unknown driver config entry')

def git(env, *args, timeout=60):
    inspect_driver()
    p = subprocess.run(['git', '--no-replace-objects', '-c', 'core.hooksPath=/dev/null',
                        '--git-dir', str(DRIVER), *args], env=env, cwd=ROOT,
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
    require(p.returncode == 0, 'Private Git operation failed: ' + p.stderr.decode(errors='replace'))
    return p.stdout, p.stderr

class Reader:
    def __init__(self, env):
        inspect_driver()
        self.p = subprocess.Popen(['git', '--no-replace-objects', '--git-dir', str(DRIVER),
          'cat-file', '--batch'], env=env, cwd=ROOT, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
          stderr=subprocess.PIPE)
        self.cache = {}

    def get(self, sha):
        require(re.fullmatch('[0-9a-f]{40}', sha), 'Nonliteral object id')
        if sha not in self.cache:
            self.p.stdin.write(sha.encode() + b'\n'); self.p.stdin.flush()
            h = self.p.stdout.readline().split()
            require(len(h) == 3 and h[0].decode() == sha, 'Missing literal object: ' + sha)
            kind = h[1].decode(); body = self.p.stdout.read(int(h[2]))
            require(self.p.stdout.read(1) == b'\n' and oid(kind, body) == sha, 'Raw object identity/framing')
            self.cache[sha] = kind, body
        return self.cache[sha]

    def tree(self, sha):
        kind, body = self.get(sha); require(kind == 'tree', 'Expected tree')
        result = {}; off = 0
        while off < len(body):
            space = body.index(b' ', off); zero = body.index(b'\0', space + 1)
            mode, name = body[off:space], body[space + 1:zero]
            require(mode in (b'40000', b'100644', b'100755', b'120000', b'160000'), 'Invalid tree mode')
            require(name and name not in (b'.', b'..') and b'/' not in name and name not in result, 'Unsafe tree name')
            require(zero + 21 <= len(body), 'Truncated tree')
            result[name] = mode, body[zero + 1:zero + 21].hex(); off = zero + 21
        require(encode(result) == body, 'Noncanonical tree')
        return result

    def walk(self, sha, prefix=b''):
        out = {}
        for name, value in self.tree(sha).items():
            path = prefix + name; out[path] = value
            if value[0] == b'40000': out.update(self.walk(value[1], path + b'/'))
        return out

    def close(self):
        self.p.stdin.close(); require(self.p.wait(timeout=10) == 0, 'Reader failed')

def provider_get(endpoint, name):
    # Explicit GET and endpoint; no gh repository discovery or write operation.
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env.update(GIT_CONFIG_GLOBAL='/dev/null', GIT_CONFIG_SYSTEM='/dev/null', GIT_CONFIG_NOSYSTEM='1')
    p = subprocess.run([shutil.which('gh'), 'api', '--method', 'GET', '--hostname', 'github.com',
      endpoint], cwd=ROOT, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60)
    fresh_bytes('provider/' + name + '.json', p.stdout)
    fresh_bytes('provider/' + name + '.stderr', p.stderr)
    require(p.returncode == 0, 'Provider GET failed')
    return json.loads(p.stdout)

def provider_blob(sha, name):
    j = provider_get('repos/' + REPO + '/git/blobs/' + sha, name)
    require(j['sha'] == sha and j['encoding'] == 'base64', 'Provider blob identity')
    body = base64.b64decode(j['content'], validate=False)
    require(len(body) == j['size'] and oid('blob', body) == sha, 'Provider blob raw hash/size')
    return body

def commit(raw, sha, name):
    kind, body = raw.get(sha); require(kind == 'commit', 'Expected commit')
    fresh_bytes(name + '_COMMIT.raw', body)
    lines = body.split(b'\n\n', 1)[0].splitlines()
    tree = lines[0].removeprefix(b'tree ').decode()
    require(lines[0] == b'tree ' + tree.encode(), 'Commit first line')
    parents = [x[7:].decode() for x in lines if x.startswith(b'parent ')]
    return tree, parents, body

def main():
    literal(ROOT)
    require(Path(__file__).absolute() == ROOT / 'baseline_census.py', 'Wrong script location')
    names = ['reader.git', 'private_objects', 'templates', 'provider', 'original_author_payload',
      'STORE_PREFLIGHT.json', 'OWN_FETCH_RECEIPT.json', 'BASELINE_ACCEPTANCE.json',
      'FULL_RAW_TREE_OBJECT_PINS.json', 'PEER_76_PATH_DELTA.json', 'AUTHOR_PAYLOAD_PINS.json',
      'ORIGINAL_QUEUE.raw', 'CURRENT_AUTHOR_QUEUE.raw', 'MAIN_QUEUE.raw',
      'ORIGINAL_SUBMITTED_QUEUE_ROW.raw', 'ACTOR_METADATA.json', 'BASELINE_CHECKPOINT.md',
      'MAIN_ROOT_TREE.raw', 'AUTHOR_TARGET_TREE.raw']
    for label in ['MAIN', 'PARENT', 'AUTHOR', 'ORIGINAL']:
        names += [label + '_COMMIT.raw', label + '_FULL_RAW_LEAVES.nul.gz',
                  label + '_FULL_RAW_TREES_AND_LEAVES.nul.gz']
    for n in names: literal(ROOT / n, absent=True)
    live = [p for p in ALTERNATES if guard_store(p)]
    fresh_json('STORE_PREFLIGHT.json', {'UTC': dt.datetime.now(dt.timezone.utc).isoformat(),
      'whole_stage_future_output_paths_absent_literal_checked_before_mutation': names,
      'explicit_read_only_object_stores': list(map(str, live)), 'implicit_nested_alternates_rejected': True,
      'primary_git_metadata_reads': 0, 'provider_mutations': 0})
    for name in ['private_objects', 'templates', 'provider', 'original_author_payload']:
        literal(ROOT / name, absent=True).mkdir()
    env = sanitized(live)
    p = subprocess.run(['git', 'init', '--bare', '--initial-branch=main', '--template=' + str(ROOT / 'templates'),
      str(DRIVER)], env=env, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
    require(p.returncode == 0, 'Private driver init failed')
    fetches = []
    for sha in [MAIN, PARENT, AUTHOR, ORIGINAL]:
        out, err = git(env, 'fetch', '--no-tags', '--no-write-fetch-head', '--depth=1', '--filter=blob:none', URL, sha)
        fetches.append({'commit': sha, 'stdout': out.decode(), 'stderr': err.decode()})
    fresh_json('OWN_FETCH_RECEIPT.json', {'UTC': dt.datetime.now(dt.timezone.utc).isoformat(),
      'fetches': fetches, 'remote_provider_read_only': True, 'primary_git_metadata_reads': 0,
      'provider_mutations': 0, 'fetch_head_written': False})
    guard_store(OBJECTS)
    raw = Reader(dict(env, GIT_ALTERNATE_OBJECT_DIRECTORIES=''))
    snapshots = {}; commits = {}
    for name, sha in [('MAIN', MAIN), ('PARENT', PARENT), ('AUTHOR', AUTHOR), ('ORIGINAL', ORIGINAL)]:
        tree, parents, body = commit(raw, sha, name); rows = raw.walk(tree)
        leaves = {p: e for p, e in rows.items() if e[0] != b'40000'}
        view, _ = git(dict(env, GIT_ALTERNATE_OBJECT_DIRECTORIES=''), 'ls-tree', '-r', '-t', '-z', tree)
        check = {}
        for line in view.split(b'\0'):
            if not line: continue
            identity, path = line.split(b'\t', 1); mode, kind, h = identity.split()
            check[path] = (b'40000' if mode == b'040000' else mode, h.decode())
        require(check == rows, 'Independent Git/full raw census disagreement')
        for suffix, data in [('LEAVES', leaves), ('TREES_AND_LEAVES', rows)]:
            fresh_bytes(name + '_FULL_RAW_' + suffix + '.nul.gz', gzip.compress(census(data), mtime=0))
        snapshots[name] = (rows, leaves)
        commits[name] = {'sha': sha, 'tree': tree, 'parents': parents, 'commit_bytes': len(body),
          'commit_sha256': hashlib.sha256(body).hexdigest(), 'leaves': len(leaves),
          'tree_entries': len(rows) - len(leaves), 'raw_leaf_census_sha256': hashlib.sha256(census(leaves)).hexdigest(),
          'raw_all_entry_census_sha256': hashlib.sha256(census(rows)).hexdigest()}
    require(commits['MAIN']['tree'] == MAIN_TREE and commits['MAIN']['parents'] == [PARENT], 'Returned MAIN differs')
    fresh_bytes('MAIN_ROOT_TREE.raw', raw.get(MAIN_TREE)[1])
    main_rows, main_leaves = snapshots['MAIN']; parent_rows, parent_leaves = snapshots['PARENT']
    changes = sorted(p for p in main_leaves.keys() | parent_leaves.keys() if main_leaves.get(p) != parent_leaves.get(p))
    require(len(changes) == 76, 'Peer changed leaf count differs')
    delta = [{'path': p.decode(), 'before': None if p not in parent_leaves else
      {'mode': parent_leaves[p][0].decode(), 'oid': parent_leaves[p][1]},
      'after': None if p not in main_leaves else {'mode': main_leaves[p][0].decode(), 'oid': main_leaves[p][1]}}
      for p in changes]
    fresh_json('PEER_76_PATH_DELTA.json', {'MAIN': MAIN, 'parent': PARENT, 'changed_leaf_count': 76,
      'changes': delta, 'independently_raw_derived': True, 'all76_must_be_preserved_in_prepared_root': True,
      'semantic_foreign_review_performed': False})
    author_rows = snapshots['AUTHOR'][0]; original_rows = snapshots['ORIGINAL'][0]
    require(author_rows[TARGET] == (b'40000', TARGET_TREE), 'Author target subtree differs')
    require(original_rows[TARGET] == author_rows[TARGET], 'Original author target differs from current author')
    payload = {p[len(TARGET) + 1:]: e for p, e in author_rows.items() if p.startswith(TARGET + b'/') and e[0] != b'40000'}
    require(len(payload) == 16, 'Original author payload is not 16 leaves')
    fresh_bytes('AUTHOR_TARGET_TREE.raw', raw.get(TARGET_TREE)[1])
    payload_pins = []
    # Preflight all now-known future provider receipts and payload paths before those GETs.
    receipts = ['MAIN_ref', 'AUTHOR_ref', 'PR262', 'MAIN_git_commit', 'AUTHOR_git_commit', 'ORIGINAL_git_commit']
    receipts += ['original_blob_' + str(i) for i in range(16)] + ['queue_' + x for x in ['MAIN','AUTHOR','ORIGINAL']]
    for name in receipts:
        for suffix in ['.json', '.stderr']: literal(ROOT / 'provider' / (name + suffix), absent=True)
    for rel in payload:
        path = ROOT / 'original_author_payload' / rel.decode(); literal(path, absent=True)
        for parent in path.parents:
            if parent == ROOT / 'original_author_payload': break
            literal(parent)
    for i, (rel, (mode, sha)) in enumerate(sorted(payload.items())):
        require(mode in (b'100644', b'100755'), 'Unexpected authored payload mode')
        body = provider_blob(sha, 'original_blob_' + str(i))
        dest = ROOT / 'original_author_payload' / rel.decode()
        literal(dest.parent); dest.parent.mkdir(parents=True, exist_ok=True)
        fresh_bytes('original_author_payload/' + rel.decode(), body)
        payload_pins.append({'path': rel.decode(), 'mode': mode.decode(), 'oid': sha,
          'bytes': len(body), 'sha256': hashlib.sha256(body).hexdigest()})
    fresh_json('AUTHOR_PAYLOAD_PINS.json', {'target_subtree': TARGET_TREE, 'original_commit': ORIGINAL,
      'current_author_commit': AUTHOR, 'original_and_current_author_subtree_equal': True, 'files': payload_pins})
    for name in ['MAIN', 'AUTHOR', 'ORIGINAL']:
        mode, sha = snapshots[name][0][b'unsolved_math_prioritization/QUEUE.md']
        require(mode == b'100644', 'Queue mode changed')
        body = provider_blob(sha, 'queue_' + name)
        fresh_bytes(('CURRENT_AUTHOR' if name == 'AUTHOR' else name) + '_QUEUE.raw', body)
        if name == 'ORIGINAL':
            matches = [line for line in body.splitlines(keepends=True) if b'| 30005044 / ' in line]
            require(len(matches) == 1, 'Original queue target row ambiguous')
            cells = [x.strip() for x in matches[0].strip().split(b'|')[1:-1]]
            require(cells[7] == b'claimed_solved' and cells[8] == b'1/5', 'Original status/turn eligibility differs')
            fresh_bytes('ORIGINAL_SUBMITTED_QUEUE_ROW.raw', matches[0])
    main_ref = provider_get('repos/' + REPO + '/git/ref/heads/main', 'MAIN_ref')
    author_ref = provider_get('repos/' + REPO + '/git/ref/heads/dot/math-30005044', 'AUTHOR_ref')
    pr = provider_get('repos/' + REPO + '/pulls/262', 'PR262')
    require(main_ref['object']['sha'] == MAIN, 'Live MAIN moved')
    require(author_ref['object']['sha'] == AUTHOR, 'Live author moved')
    require(pr['state'] == 'open' and pr['draft'] is True and not pr['merged'] and pr['merged_at'] is None,
            'PR live state differs')
    require(pr['head']['sha'] == AUTHOR and pr['head']['ref'] == 'dot/math-30005044' and
      pr['head']['repo']['full_name'] == REPO and pr['base']['ref'] == 'main' and
      pr['base']['repo']['full_name'] == REPO, 'PR head/base differs')
    for name, sha in [('MAIN', MAIN), ('AUTHOR', AUTHOR), ('ORIGINAL', ORIGINAL)]:
        j = provider_get('repos/' + REPO + '/git/commits/' + sha, name + '_git_commit')
        require(j['sha'] == sha and j['tree']['sha'] == commits[name]['tree'] and
          [x['sha'] for x in j['parents']] == commits[name]['parents'], 'Provider/raw commit identity differs')
    actor_body = raw.get(MAIN)[1]
    headers = actor_body.split(b'\n\n', 1)[0].splitlines()
    actor = [h.decode() for h in headers if h.startswith((b'author ', b'committer '))]
    require(len(actor) == 2, 'Raw historical actor metadata missing')
    fresh_json('ACTOR_METADATA.json', {'source_literal_historical_commit': MAIN, 'raw_actor_headers': actor,
      'name_email_to_reuse': {'name': 'Alec Kriebel', 'email': 'me@aleckriebel.com'},
      'name_email_headers_verified': all('Alec Kriebel <me@aleckriebel.com>' in x for x in actor),
      'ORCID': 'https://orcid.org/0009-0001-9320-500X',
      'new_commit_date_not_chosen_or_authorized': True})
    trees = [{'oid': h, 'bytes': len(body), 'sha256': hashlib.sha256(body).hexdigest()}
      for h, (kind, body) in sorted(raw.cache.items()) if kind == 'tree']
    fresh_json('FULL_RAW_TREE_OBJECT_PINS.json', {'trees': trees})
    raw.close()
    fresh_json('BASELINE_ACCEPTANCE.json', {'UTC': dt.datetime.now(dt.timezone.utc).isoformat(),
      'literal_commits': commits, 'full_raw_tree_objects_hashed': len(trees),
      'full_raw_censuses_crosschecked': True, 'no_alternates_used_for_final_raw_censuses': True,
      'peer_delta_leaf_count': 76, 'original_author_payload_leaves': 16,
      'PR_reported_base_sha': pr['base']['sha'], 'PR_base_sha_used_as_live_MAIN_authority': False,
      'PR262_open_draft_unmerged': True, 'original_eligibility': 'claimed_solved', 'author_turns': '1/5',
      'added_author_attempt_turns': 0, 'actor_source': MAIN,
      'provider_object_POSTs': 0, 'provider_ref_writes': 0, 'provider_PR_writes': 0,
      'primary_git_metadata_reads': 0, 'primary_git_metadata_writes': 0,
      'case_completion_percent': 55, 'math_source_completion_percent': 100,
      'bounded_priority_completion_percent': 100, 'novel_contribution_clearance_percent': 0,
      'native_integration_preparation_completion_percent': 45, 'actual_native_integration_complete': False})
    fresh_bytes('BASELINE_CHECKPOINT.md', ('# Private native integration baseline checkpoint\n\nUTC: ' +
      dt.datetime.now(dt.timezone.utc).isoformat() + '\n\nMAIN and author raw censuses, all76 peer leaf changes,\n'
      '16 original payload leaves, full original QUEUE row, actor metadata and fresh live PR state verified.\n'
      'Case55%; math/source100%; bounded priority100%; novelty clearance0%; private native preparation45%.\n'
      'Actual integration remains incomplete; zero provider mutation and zero primary Git metadata access.\n').encode())
    print(json.dumps({'MAIN': commits['MAIN'], 'author': commits['AUTHOR'], 'peer_delta': 76,
      'original_payload_leaves': 16, 'provider_writes': 0}, indent=2))

if __name__ == '__main__': main()
