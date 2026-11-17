#!/usr/bin/env python3
"""Fixed actual-release audit: local reads and three read-only Git object commands.
No producer/native imports, Git index/tree writes, network, subprocess retries or filesystem writes.
"""
from pathlib import Path
import hashlib
import json
import os
import stat
import struct
import subprocess

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
W = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
STAGE = P / 'verification/low-exponent-su5-stage-sol-20261116'
PREP = P / 'verification/low-exponent-su5-production-sol-20261116'
PRIOR = P / 'verification/low-exponent-su5-production-audit-sol-20261116'
TX = P / 'verification/low-exponent-su5-runtime-root-20261116/publish/cae5c8a0383144c4b356ed40ba65f1adc06adceff854d806057f139853d94c74'
OPS = P / 'verification/root-low-exponent-su5-production-ops-20261116'
COMMIT = 'b767102567ad89aff909f9f11c0e8b7d72b75c40'
PARENT = '3a6e0709bda08d8c913078b4eaa4e591fed7f3c6'
TREE = '16d2f9a43462df50ca505d07153df115b4e6e8eb'
INDEX = '6e57311ffb524aabe230dec4962ebfa6983085674882606f5b8594aa1d4cee18'
git_trace = []
checks = []

def need(ok, name):
    if not ok:
        raise ValueError(name)
    checks.append(name)

def sha(b):
    return hashlib.sha256(b).hexdigest()

def read(p):
    need(not p.is_symlink() and p.is_file(), 'ordinary file:' + str(p))
    return p.read_bytes()

def pin(p):
    b = read(p)
    return {'bytes': len(b), 'SHA256': sha(b), 'mode': int(stat.S_IMODE(p.stat().st_mode))}

def expect(p, row):
    v = pin(p)
    need(v['bytes'] == row['bytes'] and v['SHA256'] == row.get('SHA256', row.get('sha256'))
         and ('mode' not in row or v['mode'] == (int(row['mode'], 8) if isinstance(row['mode'], str) else row['mode'])), 'exact pin:' + str(p))

def census(root):
    need(root.is_dir() and not root.is_symlink(), 'ordinary root')
    files = {}
    dirs = {'.': int(stat.S_IMODE(root.stat().st_mode))}
    for f in sorted(root.rglob('*')):
        need(not f.is_symlink(), 'no symlink:' + str(f))
        if f.is_dir():
            dirs[f.relative_to(root).as_posix()] = int(stat.S_IMODE(f.stat().st_mode))
        else:
            files[f.relative_to(root).as_posix()] = pin(f)
    return files, dirs

def tables(snapshot):
    return ({r['path']: {'bytes': r['bytes'], 'SHA256': r['sha256'], 'mode': int(r['mode'], 8)} for r in snapshot['files']},
            {r['path']: int(r['mode'], 8) for r in snapshot['directories']})

def index_records(b):
    need(b[:4] == b'DIRC' and struct.unpack('>I', b[4:8])[0] == 2, 'native v2')
    need(hashlib.sha1(b[:-20]).digest() == b[-20:], 'native checksum')
    result = {}; pos = 12
    for unused in range(struct.unpack('>I', b[8:12])[0]):
        start = pos; flags = struct.unpack('>H', b[pos+60:pos+62])[0]
        need(not flags & 0x7000, 'supported stage-zero native record')
        end = b.index(b'\0', start+62); name = b[start+62:end]
        pos = start + ((end+1-start+7)//8)*8
        need(name not in result and not any(b[end+1:pos]), 'unique padded native record')
        result[name] = (b[start:pos], struct.unpack('>I', b[start+24:start+28])[0], b[start+40:start+60])
    extension = b[pos:-20]; ext = []; cursor = 0
    while cursor < len(extension):
        kind = extension[cursor:cursor+4]; n = struct.unpack('>I', extension[cursor+4:cursor+8])[0]
        need(kind == b'TREE' and cursor+8+n <= len(extension), 'only bounded TREE extension')
        ext.append(extension[cursor+8:cursor+8+n]); cursor += 8+n
    need(cursor == len(extension) and len(ext) <= 1, 'whole finite extension region')
    return result, extension, ext

def computed_trees(records):
    root = {}
    for path, (_, mode, oid) in records.items():
        node = root; parts = path.split(b'/')
        for part in parts[:-1]:
            node = node.setdefault(part, {})
        need(parts[-1] not in node, 'no file-directory collision')
        node[parts[-1]] = (mode, oid)
    hashes = {}; counts = {}
    def visit(node, path):
        entries = []; count = 0
        for name, value in node.items():
            if isinstance(value, dict):
                child = path+b'/'+name if path else name
                oid, n = visit(value, child); mode = 0o40000; key = name+b'/'
            else:
                mode, oid = value; n = 1; key = name+b'\0'
                need(mode in (0o100644, 0o100755, 0o120000, 0o160000), 'supported Git leaf mode')
            entries.append((key, format(mode, 'o').encode()+b' '+name+b'\0'+oid)); count += n
        body = b''.join(row for _, row in sorted(entries))
        oid = hashlib.sha1(b'tree '+str(len(body)).encode()+b'\0'+body).digest()
        hashes[path] = oid; counts[path] = count
        return oid, count
    visit(root, b'')
    return hashes, counts

def check_cache(payloads, tree_hashes, counts):
    valid = invalid = 0
    if not payloads:
        return {'valid_nodes': 0, 'invalid_nodes': 0, 'dropped': True}
    b = payloads[0]; pos = 0
    def visit(parent):
        nonlocal pos, valid, invalid
        end = b.index(b'\0', pos); name = b[pos:end]; pos = end+1
        end = b.index(b'\n', pos); n, children = map(int, b[pos:end].split(b' ')); pos = end+1
        path = parent+b'/'+name if parent else name
        need(b'/' not in name and children >= 0 and n >= -1, 'TREE finite path/count record')
        if n >= 0:
            oid = b[pos:pos+20]; pos += 20
            need(path in tree_hashes and oid == tree_hashes[path] and n == counts[path], 'valid cache node equals independently computed tree')
            valid += 1
        else:
            invalid += 1
        for unused in range(children):
            visit(path)
    visit(b'')
    need(pos == len(b), 'whole TREE payload consumed')
    return {'valid_nodes': valid, 'invalid_nodes': invalid, 'dropped': False}

def git(*args):
    allowed = [('cat-file', '-p', COMMIT), ('ls-tree', '-r', '-z', '--full-tree', PARENT), ('ls-tree', '-r', '-z', '--full-tree', COMMIT)]
    need(args in allowed, 'only three fixed read-only object commands')
    env = {k:v for k,v in os.environ.items() if not k.startswith('GIT_')}
    env.update(GIT_OPTIONAL_LOCKS='0', GIT_NO_LAZY_FETCH='1', GIT_NO_REPLACE_OBJECTS='1', GIT_TERMINAL_PROMPT='0')
    cmd = ['git', '--no-optional-locks', '-c', 'core.fsmonitor=false', '-c', 'core.hooksPath=/dev/null', '-c', 'gc.auto=0', '-c', 'maintenance.auto=false', *args]
    r = subprocess.run(cmd, cwd=W, env=env, capture_output=True)
    trace = {'argv': cmd, 'exit': r.returncode, 'stdout_bytes': len(r.stdout), 'stdout_SHA256': sha(r.stdout), 'stderr_bytes': len(r.stderr), 'stderr_literal': r.stderr.decode('utf-8', 'backslashreplace')}
    git_trace.append(trace)
    need(r.returncode == 0, 'read-only Git object command succeeded')
    return r.stdout

def tree_map(raw):
    result = {}
    for entry in raw.rstrip(b'\0').split(b'\0'):
        header, name = entry.split(b'\t', 1); mode, kind, oid = header.split(b' ')
        need(name not in result, 'unique commit tree leaf')
        result[name] = (int(mode, 8), bytes.fromhex(oid.decode()))
    return result

def main():
    expect(TX/'SUCCESS.json', {'bytes': 1153, 'SHA256': '82dc3ce881a910255ce7e49f7148c6644d3c9ea3e837f82c5ce5a20afa6fdfdd'})
    success = json.loads(read(TX/'SUCCESS.json'))
    expect(OPS/'PUBLISH.stdout.json', {'bytes':1202,'SHA256':'e0ff738274d85d517ac054d99297b73eaf9b37b3c2621dcab7a507fe039a96ab'})
    need(json.loads(read(OPS/'PUBLISH.stdout.json')) == success and read(OPS/'PUBLISH.stderr.txt') == b'' and read(OPS/'PUBLISH.exit') == b'0\n', 'actual root stdout-success-emptyerr-exit0')
    need(success['commit'] == COMMIT and success['tree'] == success['native_successor_semantic_tree'] == TREE and success['index_SHA256'] == INDEX, 'actual immutable root handoff')
    expect(PREP/'PLAN.json', {'bytes':6466,'SHA256':'9f2874242ce96320a219c7819b5579c620f4344ad8ee08f7c296e4363129a580'})
    plan = json.loads(read(PREP/'PLAN.json'))
    frozen = [(STAGE, 'aa081369d082b380eabd0722cbc7a5bf3458d123c8f8778dbd2fe43ffbaf74b5', '0f8f75c60d0ba1ec0780e97db5669f192b6a07055f320a426a039c4df9c81d81'),
              (PREP, '7dfe3886d6a96572f0ac5de171c0dd480202c21a9664b04b25fa08ebaa4dda5d', '5c8db9d0fca0d71c5eb03ca3f47d8ebd337a01d6794b135b74e6d072c37eb43b')]
    for root, final_sha, manifest_sha in frozen:
        need(sha(read(root/'FINAL.json')) == final_sha and sha(read(root/'OWNED_MANIFEST.json')) == manifest_sha, 'whole frozen controls')
        manifest = json.loads(read(root/'OWNED_MANIFEST.json'))
        rows = manifest['files']; actual, dirs = census(root)
        need(set(actual) == {r['path'] for r in rows}, 'whole frozen packet membership')
        need(dirs == {r['path']:int(r['mode'], 8) for r in manifest['directories']}, 'whole frozen packet directory modes/topology')
        for row in rows:
            if 'bytes' in row:
                expect(root/row['path'], row)
    targets = set(plan['scope_paths']); target_bytes = {n.encode() for n in targets}
    buffers = {n:read(STAGE/n) for n in targets}
    old = read(TX/'shared-index.before'); current = read(W/'.git/index')
    expect(TX/'shared-index.before', {'bytes':9054454,'SHA256':'71ea221a2bcd9f3919f430d785bbcb940ef2348d9596932778568940fc59d14c'})
    need(sha(current) == INDEX and pin(W/'.git/index')['mode'] == 0o644 and current == read(TX/'native-successor.index'), 'actual current58700 successor whole bytes/mode')
    before, ext0, payload0 = index_records(old); after, ext1, payload1 = index_records(current)
    need(len(before) == 58687 and len(after) == 58700 and set(after) == set(before)|target_bytes, 'exact13 additions to native path set')
    untouched = set(before)-target_bytes
    need(len(untouched) == 58685 and all(before[n] == after[n] for n in untouched), 'all58685 whole raw records incl flags/stats/modes/stage/padding exact')
    protected = b''.join(before[n][0] for n in sorted(untouched))
    need(sha(protected) == '9ec676efa40c447716daf8386b93a3dc63830f8fe8843291210700bacab0a65f', 'independent prepublication protected raw digest')
    hashes0, counts0 = computed_trees(before); hashes1, counts1 = computed_trees(after)
    cache0 = check_cache(payload0, hashes0, counts0); cache1 = check_cache(payload1, hashes1, counts1)
    need(hashes1[b''].hex() == TREE, 'independently computed whole native semantic tree equals published tree')
    need({'bytes':len(ext0),'SHA256':sha(ext0)} == success['TREE_extension_before'] and {'bytes':len(ext1),'SHA256':sha(ext1)} == success['TREE_extension_after'] and (ext0 != ext1) == success['TREE_extension_changed'], 'actual TREE region pins and honest delta')
    commit = git('cat-file', '-p', COMMIT).split(b'\n\n', 1)[0].splitlines()
    need([r[7:].decode() for r in commit if r.startswith(b'parent ')] == [PARENT] and commit[0] == ('tree '+TREE).encode(), 'exact immutable commit tree and sole expected parent')
    old_head = tree_map(git('ls-tree', '-r', '-z', '--full-tree', PARENT)); new_head = tree_map(git('ls-tree', '-r', '-z', '--full-tree', COMMIT))
    oids = {n.encode():hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).digest() for n,b in buffers.items()}
    delta = {n for n in set(old_head)|set(new_head) if old_head.get(n) != new_head.get(n)}
    need(delta == target_bytes and len(target_bytes-set(old_head)) == 13 and len(target_bytes&set(old_head)) == 2, 'exact15commit delta13A2M')
    need(set(new_head) == set(old_head)|target_bytes and all(new_head[n] == v for n,v in old_head.items() if n not in target_bytes), 'every untargeted old HEAD leaf exact')
    need(all(new_head[n] == (0o100644,oid) and after[n][1:] == new_head[n] for n,oid in oids.items()), 'all15commit and native target blobs equal actual adopted buffers')
    foreign = lambda records, head:{n:(records[n][1:] if n in records else None,head.get(n)) for n in (set(records)|set(head))-target_bytes if (records[n][1:] if n in records else None) != head.get(n)}
    foreign0 = foreign(before, old_head); foreign1 = foreign(after, new_head)
    need(foreign0 == foreign1, 'all foreign staging semantics preserved')
    need(read(W/'.git/HEAD') == b'ref: refs/heads/master\n' and read(W/'.git/refs/heads/master').strip() == COMMIT.encode(), 'actual existing master points to immutable published commit')
    baseline = json.loads(read(STAGE/'GUARDS_BEFORE.json')); old_files, old_dirs = tables(baseline['public'])
    expected_files = dict(old_files); expected_files.update({n[7:]: {'bytes':len(b),'SHA256':sha(b),'mode':0o644} for n,b in buffers.items()})
    expected_dirs = dict(old_dirs); expected_dirs.update({n:0o755 for n in plan['new_directories']})
    public = census(W/'public')
    need(public == (expected_files, expected_dirs) and len(expected_files) == 760 and len(expected_dirs) == 369, 'whole760public files/368child dirs exact747old-plus15-overlay')
    need(sum(Path(n).name == '.DS_Store' for n in public[0]) == 17, 'all17DSStore preserved')
    guards = baseline['native_indices'] + baseline['raw_HEAD_ref_config_guards']
    for row in guards:
        if row['path'] not in [str(W/'.git/index'), str(W/'.git/refs/heads/master')]:
            expect(Path(row['path']), row)
    for name in baseline['explicit_absent_paths']:
        need(not os.path.lexists(name), 'original explicit Math metadata absence')
    for row in plan['configuration_guards']:
        expect(Path(row['path']), row)
    custody = json.loads(read(STAGE/'INPUT_CUSTODY.json'))['before']
    for snap in custody['writer_packets']+[custody['original167_packet']]+custody['source_packets']:
        need(census(Path(snap['root'])) == tables(snap), 'whole frozen source/editorial namespace protected')
    need(read(W/'.git/index') == current and census(W/'public') == public, 'current index and complete public baseline unchanged across own audit')
    print(json.dumps({'status':'PASS_ACTUAL_LOCAL_POSTRELEASE_15PATH_AUDIT','commit':COMMIT,'parent':PARENT,'tree':TREE,'native_index':{'bytes':len(current),'SHA256':INDEX,'records':len(after),'mode':'0644','untargeted_whole_raw_records':len(untouched),'protected_raw_SHA256':sha(protected)},'TREE':{'before':success['TREE_extension_before'],'after':success['TREE_extension_after'],'changed':ext0!=ext1,'before_cache_validation':cache0,'after_cache_validation':cache1},'pure_hash_native_semantic_tree':hashes1[b''].hex(),'foreign_staging_difference_count':len(foreign1),'exact_delta':'13A2M','public_files':760,'public_child_dirs':368,'DSStore':17,'Git_object_reads':git_trace,'large_Git_stdout_retained_by_digest_and_immutable_object_ID_not_duplicated':True,'checks_including_file_regularities':len(checks),'own_audit_filesystem_writes':0,'Git_write_or_index_refresh_commands':0,'network_or_remote_lookup':False,'remote_publish_evidence':'Actual root exit0/emptyerr/stdout and runtime SUCCESS bound; no fresh independent remote read','deploy_Sheet_browser_or_live_authority':False},indent=2))

if __name__ == '__main__':
    try:
        main()
    except BaseException:
        print(json.dumps({'partial_readonly_Git_trace':git_trace,'completed_guard_count':len(checks)}))
        raise
