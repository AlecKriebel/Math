"""Prepared exact11 installer. No action without explicit root adoption and --execute.

install: copy11, construct a temporary HEAD-seeded commit, leave shared index/ref/remote unchanged.
publish: additionally require exact root commit approval; update only11 shared-index entries,
CAS-update existing master and perform one guarded non-force exact-ref push. Never deploy.
"""
import sys
sys.dont_write_bytecode = True
import argparse, json, os, re, tempfile
from pathlib import Path
from exact11_lib import P, W, S, O, BASE, STAGE_SEAL, ADOPTION, COMMIT_APPROVAL, need, now, sha, read, obj, pin, safe_rel, namespace, git, parse_index, stage_fences, website_git_state, root_adoption, LOCK_BODY, write_complete, validate_owned_buffer, unlink_owned, publish_buffer, extent, runtime_custody

def save(run, name, value):
    body = json.dumps(value, indent=2, ensure_ascii=False).encode() + b'\n'
    fd = os.open(run / name, os.O_CREAT | os.O_EXCL | os.O_RDWR, 0o600)
    try:
        write_complete(fd, body)
        validate_owned_buffer(run / name, fd, body)
    finally:
        os.close(fd)

def runtime_root():
    return Path(obj(O / 'RUNTIME_CONTRACT.json')['runtime_root'])

def checkpoint(run, phase, adoption_sha, approval_sha=None):
    # During work, partial extents fail pure custody; only these exact completed phases pass.
    contract_body = read(O / 'RUNTIME_CONTRACT.json')
    phase_contract = json.loads(contract_body)['phases'][phase]
    files, directories = extent(run)
    need(set(files) - {'STATE.json'} == set(phase_contract['files'])
         and directories == phase_contract['directories'], 'exact completed runtime phase before sealing')
    rows = {}
    for name in phase_contract['files']:
        body = read(run / name)
        rows[name] = {'bytes': len(body), 'SHA256': sha(body)}
    state = {'schema': 'exact11-durable-runtime-state-v1', 'phase': phase,
             'preparation_final_seal_SHA256': sha(read(O / 'PREPARATION_SEAL.json')),
             'runtime_contract_SHA256': sha(contract_body), 'root_adoption_SHA256': adoption_sha,
             'root_commit_approval_SHA256': approval_sha, 'files': rows, 'directories': directories}
    body = json.dumps(state, indent=2).encode() + b'\n'
    target = run / 'STATE.json'
    if target.exists():
        read(target)  # Stable owned runtime assumption; reject links/nonregular before overwrite.
    fd = os.open(target, os.O_CREAT | os.O_TRUNC | os.O_RDWR | os.O_NOFOLLOW, 0o600)
    try:
        write_complete(fd, body)
        validate_owned_buffer(target, fd, body)
    finally:
        os.close(fd)
    directory = os.open(run, os.O_RDONLY)
    try:
        os.fsync(directory)
    finally:
        os.close(directory)
    return runtime_custody(run, state['preparation_final_seal_SHA256'], contract_body,
                           obj(O / 'HELD_BASELINE_CONTRACT.json'))

def expected_capture(raw, index, state, adoption):
    c = obj(O / 'HELD_BASELINE_CONTRACT.json')['Git']
    need(raw == read(O / 'private/retained-approved-index') and state['index_SHA256'] == c['index_SHA256'] == adoption['index_SHA256'], 'future actual index equals held independent-bound buffer')
    need(state['protected_raw_records_SHA256'] == c['protected_raw_records_SHA256'] == adoption['protected_raw_records_SHA256'], 'all fresh protected raw records')
    need(state['origin_push_URL_SHA256'] == c['origin_push_URL_SHA256'], 'original explicit origin push location')
    for key in ['HEAD_file_SHA256', 'master_file_SHA256', 'local_git_config_SHA256']:
        need(state[key] == c[key], 'original exact Git control bytes ' + key)

def remote_parent(expected):
    urls = git('remote', 'get-url', '--push', '--all', 'origin').splitlines()
    need(len(urls) == 1 and sha(urls[0]) == obj(O / 'HELD_BASELINE_CONTRACT.json')['Git']['origin_push_URL_SHA256'], 'exact push destination')
    need(git('ls-remote', '--refs', urls[0].decode(), 'refs/heads/master').split() == [expected.encode(), b'refs/heads/master'], 'actual push-destination remote parent')

def paths(rows):
    return sorted((('public/' + r['path']).encode() for r in rows))

def approved_entries(commit, rows):
    target = paths(rows)
    records = [r for r in git('ls-tree', '-rz', commit, '--', *[p.decode() for p in target]).split(b'\x00') if r]
    need(len(records) == 11, 'exact11 approved commit-tree payload records')
    mapping = {r.split(b'\t', 1)[1]: r.split(b'\t', 1)[0] for r in records}
    out = []
    for row in rows:
        path = ('public/' + row['path']).encode()
        b = pin(S / 'candidate-a/public' / row['path'], row)
        oid = __import__('hashlib').sha1(b'blob ' + str(len(b)).encode() + b'\x00' + b).hexdigest().encode()
        need(mapping.get(path) == b'100644 blob ' + oid, 'approved commit mode/blob equals exact sealed payload')
        out.append(b'100644 ' + oid + b' 0\t' + path)
    return out

def checked_commit(commit, tree, targets, rows):
    need(re.fullmatch('[0-9a-f]{40}', commit) is not None, 'actual40-character commit')
    lines = git('cat-file', '-p', commit).splitlines()
    need(lines[0] == b'tree ' + tree.encode(), 'exact commit tree')
    need([l for l in lines if l.startswith(b'parent ')] == [b'parent ' + BASE.encode()], 'sole actual checked parent')
    diff = git('diff-tree', '--no-commit-id', '--name-only', '-r', '-z', BASE, commit).split(b'\x00')
    need(sorted((x for x in diff if x)) == targets, 'complete commit changes exact11 only')
    approved_entries(commit, rows)

def install(adoption, adoption_sha):
    (rows, summary) = stage_fences('baseline')
    (raw, index, state) = website_git_state(rows)
    expected_capture(raw, index, state, adoption)
    run = runtime_root()
    need(not run.exists() and not run.is_symlink(), 'Existing runtime state: inspect and never repeat installation')
    run.mkdir()
    (run / 'ROOT_ADOPTION.json').write_bytes(read(ADOPTION))
    save(run, 'PRE_INSTALL.json', {'UTC': now(), 'stage_seal': STAGE_SEAL, 'root_adoption_SHA256': adoption_sha, 'actual_parent': BASE, 'Git': state, 'exact11': rows, 'summary': summary})
    checkpoint(run, 'INSTALL_STARTED', adoption_sha)
    for row in rows:
        rel = safe_rel(row['path'])
        dest = W / 'public' / rel
        parent = W / 'public'
        for part in rel.parts[:-1]:
            parent = parent / part
            if parent.exists():
                need(parent.is_dir() and (not parent.is_symlink()), 'safe exact destination ancestor')
            else:
                parent.mkdir()
        need(not dest.is_symlink(), 'destination is not a link')
        (fd, tmp) = tempfile.mkstemp(prefix='.exact11-install-', dir=dest.parent)
        try:
            with os.fdopen(fd, 'wb') as f:
                f.write(pin(S / 'candidate-a/public' / row['path'], row))
                f.flush()
                os.fsync(f.fileno())
                os.fchmod(f.fileno(), 420)
            if row['action'] == 'add_new_leaf':
                os.link(tmp, dest, follow_symlinks=False)
            else:
                baseline = next((r for r in obj(S / 'WEBSITE_BASELINE.json')['files'] if r['path'] == str(dest)))
                pin(dest, baseline)
                os.replace(tmp, dest)
            pin(dest, row)
        finally:
            if Path(tmp).exists():
                Path(tmp).unlink()
    stage_fences('installed')
    (raw2, index2, state2) = website_git_state(rows)
    expected_capture(raw2, index2, state2, adoption)
    tempindex = run / 'commit.index'
    need(not tempindex.exists(), 'new temporary index namespace')
    git('read-tree', BASE, index=tempindex, mutating=True)
    for row in rows:
        b = pin(S / 'candidate-a/public' / row['path'], row)
        oid = git('hash-object', '--no-filters', '-w', '--stdin', data=b, mutating=True).decode().strip()
        need(oid == __import__('hashlib').sha1(b'blob ' + str(len(b)).encode() + b'\x00' + b).hexdigest(), 'exact unfiltered Git blob')
        git('update-index', '--add', '--cacheinfo', '100644', oid, 'public/' + row['path'], index=tempindex, mutating=True)
    target = paths(rows)
    changed = [x for x in git('diff', '--cached', '--name-only', '-z', BASE, index=tempindex).split(b'\x00') if x]
    need(sorted(changed) == target, 'temporary HEAD index exact11 only')
    git('diff', '--cached', '--check', BASE, '--', *[p.decode() for p in target], index=tempindex)
    tree = git('write-tree', index=tempindex, mutating=True).decode().strip()
    message = adoption['commit_message']
    need(isinstance(message, str) and 0 < len(message) <= 300 and ('\x00' not in message), 'root explicit bounded commit message')
    commit = git('commit-tree', tree, '-p', BASE, data=(message.rstrip('\n') + '\n').encode(), mutating=True).decode().strip()
    checked_commit(commit, tree, target, rows)
    need(git('rev-parse', 'HEAD').decode().strip() == BASE and read(W / '.git/index') == raw, 'shared index/ref unchanged while constructing commit')
    pending = {'UTC': now(), 'status': 'EXACT11_FILES_INSTALLED_COMMIT_PREPARED_NOT_PUBLISHED', 'root_adoption_SHA256': adoption_sha, 'stage_final_seal_SHA256': STAGE_SEAL, 'parent': BASE, 'commit': commit, 'tree': tree, 'gitpaths': [p.decode() for p in target], 'public_counts': [623, 94, 95], 'protected_raw_records_SHA256': state['protected_raw_records_SHA256'], 'shared_index_SHA256_unchanged': state['index_SHA256'], 'origin_push_URL_SHA256': state['origin_push_URL_SHA256'], 'shared_index_changed': False, 'ref_changed': False, 'pushed': False, 'deployed': False, 'root_commit_approval_required': True, 'temporary_index_SHA256': sha(read(tempindex))}
    save(run, 'PENDING_COMMIT.json', pending)
    checkpoint(run, 'INSTALLED', adoption_sha)
    print(json.dumps(pending, indent=2))

def approve_commit(expected_sha, pending, adoption_sha, rows):
    need(re.fullmatch('[0-9a-f]{64}', expected_sha or '') is not None, 'explicit root commit-approval hash required')
    need(COMMIT_APPROVAL.exists(), 'exact root commit approval exists')
    approval_bytes = read(COMMIT_APPROVAL)
    need(sha(approval_bytes) == expected_sha, 'exact root commit approval hash')
    a = json.loads(approval_bytes)
    need(a['schema'] == 'root_five_centers_mixed_face_exact11_commit_approval_v1' and a['authority'] == 'root' and (a['publication_authorized'] is True), 'root exact publication authority')
    need(a['root_adoption_SHA256'] == adoption_sha and a['pending_commit_receipt_SHA256'] == sha(read(runtime_root() / 'PENDING_COMMIT.json')), 'root checked exact pending receipt')
    for key in ['parent', 'commit', 'tree', 'gitpaths', 'protected_raw_records_SHA256']:
        need(a[key] == pending[key], 'root checked commit ' + key)
    checked_commit(pending['commit'], pending['tree'], paths(rows), rows)
    return a

def publish(adoption, adoption_sha, commit_approval_sha):
    run = runtime_root()
    need(run.is_dir() and (not (run / 'PUBLICATION.json').exists()), 'one prepared unreported commit only')
    durable = runtime_custody(run, sha(read(O / 'PREPARATION_SEAL.json')), read(O / 'RUNTIME_CONTRACT.json'), obj(O / 'HELD_BASELINE_CONTRACT.json'))
    need(durable['phase'] == 'INSTALLED', 'only exact completed installed runtime may publish')
    pending = obj(run / 'PENDING_COMMIT.json')
    need(pending['root_adoption_SHA256'] == adoption_sha and pending['parent'] == BASE, 'prepared commit belongs to root adoption')
    (rows, summary) = stage_fences('installed')
    approve_commit(commit_approval_sha, pending, adoption_sha, rows)
    (run / 'ROOT_COMMIT_APPROVAL.json').write_bytes(read(COMMIT_APPROVAL))
    (raw, index, state) = website_git_state(rows)
    expected_capture(raw, index, state, adoption)
    targetset = set(paths(rows))
    alternate = run / 'shared-index.approved'
    need(not alternate.exists(), 'new approved shared-index copy')
    alternate.write_bytes(raw)
    selected = approved_entries(pending['commit'], rows)
    git('update-index', '-z', '--index-info', index=alternate, data=b'\x00'.join(selected) + b'\x00', mutating=True)
    newraw = read(alternate)
    newindex = parse_index(newraw, targetset)
    need(newindex['protected'] == index['protected'], 'every unrelated raw index entry preserved byte for byte')
    need(newindex['count'] == index['count'] + 9 and len(newindex['entries']) == index['count'] + 9, 'only9 new index entries')
    selected_map = {r.split(b'\t', 1)[1]: r.split(b'\t', 1)[0] for r in selected}
    for (path, record, mode, oid) in newindex['entries']:
        if path in targetset:
            need(selected_map[path] == ('%06o' % mode).encode() + b' ' + oid.encode() + b' 0', 'exact approved11 shared index entries')
    lock = W / '.git/index.lock'
    fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_RDWR, 384)
    try:
        write_complete(fd, LOCK_BODY)
        validate_owned_buffer(lock, fd, LOCK_BODY)
        need(read(W / '.git/index') == raw and git('symbolic-ref', 'HEAD').strip() == b'refs/heads/master' and (git('rev-parse', 'HEAD').decode().strip() == BASE), 'exact original index and parent while holding lock')
        for row in rows:
            pin(W / 'public' / row['path'], row)
        remote_parent(BASE)
        save(run, 'PRE_PUBLICATION.json', {'UTC': now(), 'root_adoption_SHA256': adoption_sha, 'root_commit_approval_SHA256': commit_approval_sha, 'parent': BASE, 'commit': pending['commit'], 'old_index_SHA256': sha(raw), 'approved_index_SHA256': sha(newraw), 'protected_raw_records_SHA256': index['protected_raw_records_SHA256'], 'only11_records_may_change': True, 'pre_push_actual_advertised_parent_guard_required': True})
        publish_buffer(newraw, W / '.git/index', lock, fd)
        directory = os.open(W / '.git', os.O_RDONLY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
        git('update-ref', 'refs/heads/master', pending['commit'], BASE, mutating=True)
        push = git('push', '--porcelain', '--no-follow-tags', '--recurse-submodules=no', 'origin', pending['commit'] + ':refs/heads/master', mutating=True, guard_commit=pending['commit'], guard_remote_sha=state['origin_push_URL_SHA256'])
        (run / 'PUSH.stdout').write_bytes(push)
        remote_parent(pending['commit'])
        finalraw = read(W / '.git/index')
        finalindex = parse_index(finalraw, targetset)
        need(finalindex['protected'] == index['protected'], 'all unrelated raw index entries unchanged at completion')
        need(git('rev-parse', 'HEAD').decode().strip() == pending['commit'] and git('symbolic-ref', 'HEAD').strip() == b'refs/heads/master', 'actual final local existing master')
        stage_fences('installed')
        receipt = {'UTC': now(), 'status': 'PASS_EXACT11_INSTALL_ROOT_CHECKED_COMMIT_AND_GUARDED_NONFORCE_PUSH', 'parent': BASE, 'commit': pending['commit'], 'tree': pending['tree'], 'gitpaths': pending['gitpaths'], 'counts': [623, 94, 95], 'protected_record_count': index['protected_record_count'], 'protected_raw_records_SHA256': index['protected_raw_records_SHA256'], 'unrelated_raw_index_entries_unchanged': True, 'unrelated_public_files_unchanged': 612, 'site_configs_and_qualified17_plus405b_core_unchanged': True, 'core_mutations': False, 'deployed': False, 'live_verified': False, 'browser_verified': False, 'native_Sheet_publication_verified': False, 'canonical_url': None, 'AA': None}
        save(run, 'PUBLICATION.json', receipt)
        checkpoint(run, 'PUBLISHED', adoption_sha, commit_approval_sha)
        print(json.dumps(receipt, indent=2))
    finally:
        try:
            unlink_owned(lock, fd)
        finally:
            os.close(fd)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--phase', required=True, choices=['install', 'publish'])
    parser.add_argument('--execute', action='store_true')
    parser.add_argument('--adoption-sha256')
    parser.add_argument('--commit-approval-sha256')
    args = parser.parse_args()
    need(args.execute, 'Preparation only: explicit --execute and root receipts are required')
    adoption = root_adoption(args.adoption_sha256)
    if args.phase == 'install':
        install(adoption, args.adoption_sha256)
    else:
        publish(adoption, args.adoption_sha256, args.commit_approval_sha256)
if __name__ == '__main__':
    main()
