#!/usr/bin/env python3
"""Single-use, read-only native Git data audit. No project code is imported."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import stat
import struct
import subprocess
import time
import traceback

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
M = Path('/Users/alec/Documents/Math')
W = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
OUT = P / 'verification/radial-tree-native-semantics-sol-20261117'
STAGE = P / 'verification/radial-tree-stage-sol-20261117'
PREP = P / 'verification/radial-tree-production-preparation-sol-20261117'
RUNTIME = P / 'verification/radial-tree-runtime-sol-20261117'
AUTH_SHA = 'f03e6c345529683595dba38fe6ded458852fcbc506e74d082f8441f4b7922be0'
AUTH = P / 'verification/root-radial-tree-publish-authorization-20261117.json'
PUB = RUNTIME / 'publish' / AUTH_SHA
OLD_INDEX = PUB / 'native-backups/index.before'
PARENT = '96f04aa5544df69daba07a9ed4d6212172e9984a'
SUCCESSOR = '7d5ac8ea5dc8d6cddee457da7a5b40042d36d344'
EXPECTED_TREE = 'c59d0d0a542f20bceb3556b1e936e86b22626434'
OLD_SHA = 'e6285d49b7249ae2c88a1f624ca98c1dcf480424db272c4fe111ca91dbdafb5e'
NEW_SHA = '592a25281b63a357fbe4fe2580e2c9764ba2b4836650d8751ac573ff8117c365'
TREE_SHA = 'f12d2a0b795034ce5cab45ad6fa5da31b4d7ad6f4b22a5999ce27841b41350b3'
PAYLOAD_SHA = '6078bbaef4d39e7b0418bc6ed44ad8f37d2733ec6de4a4e4ba165fe7e665bfcb'
INVALID = {'', 'public', 'public/research',
           'public/research/binary-relation-liveness',
           'public/research/rational-point-undecidability',
           'public/research/focal-distance-period-criterion'}
CHECKS = []
COMMANDS = []
EXTERNAL = set()


def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def require(condition, label):
    if not condition:
        raise AssertionError(label)


def check(label, **evidence):
    CHECKS.append({'UTC': utc(), 'check': label, **evidence})


def write(name, value):
    path = OUT / name
    require(path.parent == OUT, 'output must be a direct owned-lane child')
    require(not path.exists(), 'no output overwrite: ' + name)
    if isinstance(value, bytes):
        path.write_bytes(value)
    else:
        path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')
    path.chmod(0o644)


def mode(value):
    return format(int(value, 8) if isinstance(value, str) else value, '04o')


def file_info(path):
    s = path.lstat()
    require(stat.S_ISREG(s.st_mode), 'regular file required: ' + str(path))
    data = path.read_bytes()
    require(len(data) == s.st_size, 'file changed while reading: ' + str(path))
    return {'bytes': len(data), 'SHA256': sha(data), 'mode': mode(stat.S_IMODE(s.st_mode))}


def profile(root):
    require(stat.S_ISDIR(root.lstat().st_mode), 'directory required: ' + str(root))
    files, dirs, empty = {}, {}, []
    def visit(folder):
        children = sorted(folder.iterdir(), key=lambda p: os.fsencode(p.name))
        if not children:
            empty.append(folder.relative_to(root).as_posix())
        for child in children:
            rel = child.relative_to(root).as_posix()
            s = child.lstat()
            if stat.S_ISDIR(s.st_mode):
                dirs[rel] = mode(stat.S_IMODE(s.st_mode))
                visit(child)
            else:
                require(stat.S_ISREG(s.st_mode), 'symlink/special object in guarded tree: ' + str(child))
                files[rel] = file_info(child)
    visit(root)
    return {'root': str(root), 'root_mode': mode(stat.S_IMODE(root.lstat().st_mode)),
            'files': files, 'directories': dirs, 'empty_directories': empty,
            'regular_files': len(files), 'child_directories': len(dirs)}


def normalized_file(row):
    return {'bytes': row['bytes'], 'SHA256': row['SHA256'], 'mode': mode(row['mode'])}


def canonical_profile(p):
    files = p['files']
    dirs = p['directories']
    if isinstance(files, list):
        files = {r['path']: r for r in files}
    if isinstance(dirs, list):
        dirs = {r['path']: r['mode'] for r in dirs}
    return {'root_mode': mode(p['root_mode']),
            'files': {k: normalized_file(v) for k, v in files.items()},
            'directories': {k: mode(v['mode'] if isinstance(v, dict) else v) for k, v in dirs.items()}}


def load(path):
    return json.loads(path.read_bytes())


def pin(row):
    path = Path(row['path'])
    EXTERNAL.add(path)
    require(file_info(path) == normalized_file(row), 'pinned input changed: ' + str(path))


def native(root):
    git = root / '.git'
    require(git.is_dir() and not git.is_symlink(), 'ordinary native .git directory')
    result = {'root': str(root)}
    for name in ['HEAD', 'index', 'config', 'config.worktree']:
        p = git / name
        result[name] = file_info(p) if p.exists() else None
    head = (git / 'HEAD').read_bytes()
    require(head.startswith(b'ref: refs/heads/') and head.endswith(b'\n'), 'native local symbolic HEAD')
    result['HEAD_raw'] = head.decode('ascii')
    result['local_branch'] = head[5:-1].decode('ascii')
    result['loose_local_heads'] = profile(git / 'refs/heads')
    packed = git / 'packed-refs'
    local = {}
    if packed.exists():
        result['packed_refs_mode'] = file_info(packed)['mode']
        for line in packed.read_bytes().splitlines():
            if line.startswith((b'#', b'^')) or not line:
                continue
            oid, ref = line.split(b' ', 1)
            if ref.startswith(b'refs/heads/'):
                key = ref.decode('ascii')
                require(key not in local, 'duplicate packed local ref')
                require(len(oid) == 40 and int(oid, 16) >= 0, 'packed local oid')
                local[key] = {'OID': oid.decode(), 'raw_line': line.decode('ascii')}
    else:
        result['packed_refs_mode'] = None
    result['packed_local_heads'] = local
    loose = git / result['local_branch']
    result['local_branch_OID'] = loose.read_text().strip() if loose.exists() else local[result['local_branch']]['OID']
    result['excluded'] = ['remote-tracking refs', 'FETCH_HEAD', 'nonlocal packed-ref lines', 'reflogs',
                          'Firebase state outside public', 'global process/remote state']
    return result


def guards():
    return {'UTC': utc(), 'trees': {str(r): profile(r) for r in [W / 'public', STAGE, PREP, RUNTIME]},
            'native': {str(r): native(r) for r in [M, W]},
            'external_inputs': {str(p): file_info(p) for p in sorted(EXTERNAL)}}


def same_guards(a, b):
    return {k: v for k, v in a.items() if k != 'UTC'} == {k: v for k, v in b.items() if k != 'UTC'}


def authenticate_manifest(root, actual, manifest):
    require(mode(manifest['root_mode']) == actual['root_mode'], 'manifest root mode ' + str(root))
    rows = {r['path']: r for r in manifest['files']}
    exclusions = set(manifest.get('exact_terminal_exclusions', []))
    require(set(actual['files']) == set(rows) | exclusions, 'whole manifest file topology ' + str(root))
    for path, row in rows.items():
        if row.get('terminal_control'):
            require(actual['files'][path]['mode'] == mode(row['mode']), 'terminal mode ' + path)
        else:
            require(actual['files'][path] == normalized_file(row), 'manifest file ' + path)
    dirs = {r['path']: mode(r['mode']) for r in manifest['directories']}
    require(actual['directories'] == dirs, 'whole manifest directory topology ' + str(root))


def parse_index(data, label):
    require(data[:4] == b'DIRC' and len(data) >= 32, label + ' header')
    version, count = struct.unpack('!II', data[4:12])
    require(version == 2, label + ' version2')
    require(hashlib.sha1(data[:-20]).digest() == data[-20:], label + ' SHA1 trailer')
    offset, entries = 12, []
    for number in range(count):
        start = offset
        require(offset + 62 <= len(data) - 20, label + ' fixed entry extent')
        values = struct.unpack('!10I20sH', data[offset:offset + 62])
        flags = values[-1]
        require(not flags & 0x4000, label + ' no v3 extended flag in v2')
        nul = data.index(b'\0', offset + 62, len(data) - 20)
        path = data[offset + 62:nul]
        require(path and not path.startswith(b'/') and not path.endswith(b'/'), label + ' relative entry path')
        require(all(part not in (b'', b'.', b'..', b'.git') for part in path.split(b'/')), label + ' canonical entry path')
        require((flags & 0xfff) == min(len(path), 0xfff), label + ' name-length flag')
        offset = start + ((nul + 1 - start + 7) // 8) * 8
        require(data[nul:offset] == b'\0' * (offset - nul), label + ' native zero padding')
        csec, cns, msec, mns, dev, ino, imode, uid, gid, size = values[:10]
        require(cns < 10**9 and mns < 10**9, label + ' native nanoseconds')
        require(imode in (0o100644, 0o100755, 0o120000, 0o160000), label + ' canonical mode')
        entries.append({'path_bytes': path, 'path': os.fsdecode(path), 'stage': (flags >> 12) & 3,
                        'flags': flags, 'assume_valid': bool(flags & 0x8000), 'mode': format(imode, 'o'),
                        'OID': values[10].hex(), 'stat': list(values[:10]), 'raw': data[start:offset],
                        'offset': start, 'bytes': offset - start, 'number': number})
    require([(e['path_bytes'], e['stage']) for e in entries] == sorted((e['path_bytes'], e['stage']) for e in entries), label + ' native record sort')
    require(len({(e['path_bytes'], e['stage']) for e in entries}) == count, label + ' unique records')
    require(all(e['stage'] == 0 for e in entries), label + ' stage0 only')
    entry_end = offset
    extensions = []
    while offset < len(data) - 20:
        require(offset + 8 <= len(data) - 20, label + ' extension header extent')
        sig = data[offset:offset + 4]
        size = struct.unpack('!I', data[offset + 4:offset + 8])[0]
        end = offset + 8 + size
        require(end <= len(data) - 20, label + ' extension payload extent')
        extensions.append({'signature': sig.decode('ascii'), 'payload': data[offset + 8:end], 'raw': data[offset:end]})
        offset = end
    require(offset == len(data) - 20, label + ' complete index extent')
    require(len({e['signature'] for e in extensions}) == len(extensions), label + ' unique extensions')
    return {'version': version, 'count': count, 'entries': entries, 'entry_end': entry_end,
            'extensions': extensions, 'SHA256': sha(data), 'trailer_SHA1': data[-20:].hex()}


def parse_cache(payload):
    nodes = {}
    def read(offset, parent, root=False):
        start = offset
        nul = payload.index(b'\0', offset)
        name = payload[offset:nul]
        require((root and name == b'') or (not root and name and b'/' not in name), 'TREE node component')
        nl = payload.index(b'\n', nul + 1)
        fields = payload[nul + 1:nl].split(b' ')
        require(len(fields) == 2, 'TREE count fields')
        count, children = map(int, fields)
        require(count >= -1 and children >= 0, 'TREE count ranges')
        require(payload[nul + 1:nl] == str(count).encode() + b' ' + str(children).encode(), 'TREE canonical count encoding')
        path = parent + (b'/' if parent else b'') + name if not root else b''
        key = os.fsdecode(path)
        require(key not in nodes, 'TREE unique full path')
        offset = nl + 1
        oid = None
        if count >= 0:
            require(offset + 20 <= len(payload), 'TREE valid OID extent')
            oid = payload[offset:offset + 20].hex()
            offset += 20
        node = {'path': key, 'name': os.fsdecode(name), 'count': count, 'subtree_count': children,
                'OID': oid, 'offset': start, 'header_bytes': offset - start, 'children': []}
        nodes[key] = node
        for unused in range(children):
            offset, child = read(offset, path)
            node['children'].append(child)
        require(len(node['children']) == len(set(node['children'])), 'TREE unique immediate children')
        node['subtree_bytes'] = offset - start
        return offset, key
    end, root = read(0, b'', True)
    require(end == len(payload) and root == '', 'complete TREE recursive payload')
    return nodes


def object_oid(kind, data):
    return hashlib.sha1(kind.encode() + b' ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def build_trees(entries):
    trie = {}
    for entry in entries:
        parts = entry['path_bytes'].split(b'/')
        node = trie
        for part in parts[:-1]:
            require(part not in node or isinstance(node[part], dict), 'index directory/leaf collision')
            node = node.setdefault(part, {})
        require(parts[-1] not in node, 'index duplicate leaf or directory collision')
        node[parts[-1]] = (entry['mode'], entry['OID'])
    trees = {}
    def build(node, path):
        records, count, directories = [], 0, []
        for name, value in node.items():
            if isinstance(value, dict):
                subpath = path + (b'/' if path else b'') + name
                child = build(value, subpath)
                imode, oid = '40000', child['OID']
                count += child['count']
                directories.append(os.fsdecode(subpath))
                sortkey = name + b'/'
            else:
                imode, oid = value
                count += 1
                sortkey = name
            records.append((sortkey, imode.encode() + b' ' + name + b'\0' + bytes.fromhex(oid)))
        data = b''.join(raw for key, raw in sorted(records))
        row = {'path': os.fsdecode(path), 'OID': object_oid('tree', data), 'count': count,
               'directories': sorted(directories), 'immediate_entries': len(records), 'payload': data}
        trees[row['path']] = row
        return row
    build(trie, b'')
    return trees


def git_batch(label, requested):
    require(requested and len(requested) == len(set(requested)), 'bounded distinct Git object requests')
    require(len(requested) <= 20000, 'Git object request bound')
    for oid in requested:
        require(len(oid) == 40 and int(oid, 16) >= 0, 'literal Git object id')
    argv = ['/usr/bin/git', '--no-optional-locks', '--git-dir=' + str(W / '.git'), 'cat-file', '--batch']
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env.update({'GIT_OPTIONAL_LOCKS': '0', 'GIT_NO_REPLACE_OBJECTS': '1', 'GIT_NO_LAZY_FETCH': '1',
                'GIT_TERMINAL_PROMPT': '0', 'GIT_CONFIG_NOSYSTEM': '1', 'GIT_CONFIG_GLOBAL': '/dev/null'})
    stdin = ''.join(oid + '\n' for oid in requested).encode()
    write(label + '.stdin.txt', stdin)
    started = utc()
    tick = time.monotonic()
    run = subprocess.run(argv, input=stdin, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         env=env, cwd=str(OUT), timeout=60, check=False)
    elapsed = time.monotonic() - tick
    write(label + '.stdout.bin', run.stdout)
    write(label + '.stderr.txt', run.stderr)
    receipt = {'argv': argv, 'started_UTC': started, 'finished_UTC': utc(), 'elapsed_seconds': elapsed,
               'exit_code': run.returncode, 'stdin_bytes': len(stdin), 'stdout_bytes': len(run.stdout),
               'stderr_bytes': len(run.stderr), 'requested_objects': len(requested), 'read_only': True}
    COMMANDS.append(receipt)
    write(label + '.execution.json', receipt)
    require(run.returncode == 0, label + ' Git exit status')
    require(run.stderr == b'', label + ' unexpected Git stderr')
    objects, offset = {}, 0
    for expected in requested:
        nl = run.stdout.index(b'\n', offset)
        fields = run.stdout[offset:nl].split(b' ')
        require(len(fields) == 3 and fields[0].decode() == expected, label + ' complete cat-file object header')
        oid, kind, size = fields[0].decode(), fields[1].decode(), int(fields[2])
        require(kind in ('tree', 'blob', 'commit'), label + ' expected Git object type')
        start, end = nl + 1, nl + 1 + size
        require(end < len(run.stdout) and run.stdout[end:end + 1] == b'\n', label + ' object extent')
        data = run.stdout[start:end]
        require(object_oid(kind, data) == oid, label + ' actual object identity')
        objects[oid] = (kind, data)
        offset = end + 1
    require(offset == len(run.stdout), label + ' complete literal Git stream')
    return objects


def commit_fields(data):
    header, message = data.split(b'\n\n', 1)
    result = {'parent': [], 'message': message.decode('utf-8')}
    for line in header.splitlines():
        key, value = line.split(b' ', 1)
        key, value = key.decode('ascii'), value.decode('utf-8')
        if key == 'parent':
            result['parent'].append(value)
        else:
            require(key not in result, 'duplicate commit header')
            result[key] = value
    return result


def decode_tree(data):
    records, offset, order = [], 0, []
    while offset < len(data):
        space = data.index(b' ', offset)
        nul = data.index(b'\0', space + 1)
        imode = data[offset:space].decode('ascii')
        name = data[space + 1:nul]
        require(imode in ('40000', '100644', '100755', '120000', '160000'), 'actual canonical tree mode')
        require(name and b'/' not in name and name not in (b'.', b'..', b'.git'), 'actual tree name')
        require(nul + 21 <= len(data), 'actual tree oid extent')
        oid = data[nul + 1:nul + 21].hex()
        records.append((name, imode, oid))
        order.append(name + (b'/' if imode == '40000' else b''))
        offset = nul + 21
    require(offset == len(data) and order == sorted(order), 'actual tree complete Git sort')
    require(len({r[0] for r in records}) == len(records), 'actual tree unique children')
    return records


def actual_leaves(root_oid, objects):
    leaves, trees = {}, {}
    def walk(oid, path, ancestors):
        require(oid not in ancestors, 'actual recursive tree cycle')
        require(oid in objects and objects[oid][0] == 'tree', 'actual complete tree object available')
        rows = decode_tree(objects[oid][1])
        count, childdirs = 0, []
        for name, imode, target in rows:
            rel = path + (b'/' if path else b'') + name
            key = os.fsdecode(rel)
            if imode == '40000':
                count += walk(target, rel, ancestors | {oid})
                childdirs.append(key)
            else:
                require(key not in leaves, 'actual unique recursive leaf')
                leaves[key] = {'mode': imode, 'OID': target, 'type': 'commit' if imode == '160000' else 'blob'}
                count += 1
        trees[os.fsdecode(path)] = {'OID': oid, 'count': count, 'directories': sorted(childdirs), 'immediate_entries': len(rows)}
        return count
    walk(root_oid, b'', set())
    return leaves, trees


def semantic_map(entries):
    return {e['path']: {'mode': e['mode'], 'OID': e['OID'], 'type': 'commit' if e['mode'] == '160000' else 'blob'} for e in entries}


def record_evidence(entry):
    return {k: v for k, v in entry.items() if k not in ('raw', 'path_bytes')} | {'raw_SHA256': sha(entry['raw'])}


def main():
    require(sha(AUTH.read_bytes()) == AUTH_SHA, 'actual publication authorization pin')
    EXTERNAL.add(AUTH)
    auth = load(AUTH)
    plan = load(PREP / 'PLAN.json')
    pin(auth['bindings']['PLAN'])
    pin(auth['bindings']['helper'])
    pin(auth['installation_SUCCESS'])
    pin(auth['helper_review']['audit_FINAL'])
    for row in plan['controls'].values():
        pin(row)
    require(auth['bindings']['controls'] == plan['controls'], 'authorization binds full exact controls')
    require(sha((PREP / 'OWNED_MANIFEST.json').read_bytes()) == '0f2c1089ba6b8dc8ce12977ea9c7470c733b33b8901e7f1b05228f13eb5cd531', 'preparation manifest pin')
    before = guards()
    write('GUARDS_BEFORE.json', before)
    authenticate_manifest(STAGE, before['trees'][str(STAGE)], load(STAGE / 'OWNED_MANIFEST.json'))
    authenticate_manifest(PREP, before['trees'][str(PREP)], load(PREP / 'OWNED_MANIFEST.json'))
    require((before['trees'][str(STAGE)]['regular_files'], before['trees'][str(STAGE)]['child_directories']) == (804, 380), 'full frozen stage counts')
    require((before['trees'][str(PREP)]['regular_files'], before['trees'][str(PREP)]['child_directories']) == (9, 0), 'full frozen preparation counts')
    check('whole frozen stage and preparation authenticated', stage_files=804, stage_directories=380, preparation_files=9)

    targets = load(STAGE / 'TARGETS.json')
    require(targets['D'] == [] and targets['production_target_count'] == 11, 'literal finite TARGETS dictionary')
    require(len(targets['A']) == 9 and len(targets['M']) == 2 and len(targets['new_directories']) == 4, 'TARGETS counts')
    paths = targets['A'] + targets['M']
    require(len(set(paths)) == 11 and all(not p.startswith('public/') and '..' not in p.split('/') for p in paths), 'TARGETS public-root namespace')
    gitpaths = {'public/' + p for p in paths}
    require(gitpaths == set(plan['scope_paths']) == set(auth['bindings']['scope_paths']), 'actual exact intended Git scope')
    candidate = profile(STAGE / 'candidate/public')
    declared = load(STAGE / 'CANDIDATE_MANIFEST.json')
    current = before['trees'][str(W / 'public')]
    require(canonical_profile(candidate) == canonical_profile(declared), 'complete actual candidate vs frozen candidate manifest')
    require(canonical_profile(current) == canonical_profile(candidate), 'complete installed public vs candidate bytes modes topology')
    require((current['regular_files'], current['child_directories']) == (781, 377), 'full public counts')
    baseline = canonical_profile(load(STAGE / 'GUARDS_BEFORE_V2.json')['public'])
    cand = canonical_profile(candidate)
    require((len(baseline['files']), len(baseline['directories'])) == (772, 373), 'complete original public counts')
    require(set(cand['files']) - set(baseline['files']) == set(targets['A']), 'actual public additions exact9')
    require(set(baseline['files']) - set(cand['files']) == set(), 'no public deletions')
    changed = {p for p in baseline['files'] if baseline['files'][p] != cand['files'][p]}
    require(changed == set(targets['M']), 'actual public replacements exact2')
    require(set(cand['directories']) - set(baseline['directories']) == set(targets['new_directories']), 'actual directory additions exact4')
    require(baseline['root_mode'] == cand['root_mode'] and all(cand['directories'].get(p) == m for p, m in baseline['directories'].items()), 'all old directory modes and topology preserved')
    originals = {'research/index.html': STAGE / 'originals/research-index.html',
                 'research/sitemap.xml': STAGE / 'originals/research-sitemap.xml'}
    require(set(originals) == set(targets['M']), 'actual original replacement buffers cover scope')
    for p in baseline['files']:
        original_path = originals.get(p, STAGE / 'candidate/public' / p)
        require(file_info(original_path) == baseline['files'][p], 'complete actual original public buffer ' + p)
    check('all original/candidate/installed public buffers exact', old_files=772, new_files=781, old_dirs=373, new_dirs=377, additions=targets['A'], replacements=targets['M'])

    native_before = load(PUB / 'native-backups/native-guards.before.json')
    historical = {r['root']: r for r in native_before}
    for root in [M, W]:
        actual, old = before['native'][str(root)], historical[str(root)]
        for field in ['HEAD', 'config', 'packed_local_heads', 'packed_refs_mode', 'local_branch']:
            expected = normalized_file(old[field]) if field in ('HEAD', 'config') else old[field]
            require(actual[field] == expected, 'native historical control preserved ' + str(root) + ' ' + field)
        if root == M:
            require(actual['index'] == normalized_file(old['index']), 'Math native index exact publication backup')
            require(canonical_profile(actual['loose_local_heads']) == canonical_profile(old['loose_local_heads']), 'Math local loose heads exact')
            require(actual['local_branch_OID'] == old['local_branch_OID'], 'Math native main exact')
        else:
            require(actual['local_branch_OID'] == SUCCESSOR and old['local_branch_OID'] == PARENT, 'actual website successor/parent local identity')
            old_loose = canonical_profile(old['loose_local_heads'])
            new_loose = canonical_profile(actual['loose_local_heads'])
            require(set(old_loose['files']) == set(new_loose['files']) == {'master'}, 'only actual master loose local head')
            require(old_loose['root_mode'] == new_loose['root_mode'] and old_loose['directories'] == new_loose['directories'], 'website local ref topology preserved')
            require(old_loose['files']['master']['mode'] == new_loose['files']['master']['mode'] == '0644', 'website native master mode')
            require((W / '.git/refs/heads/master').read_bytes() == (SUCCESSOR + '\n').encode(), 'literal native master buffer')
    require((PUB / 'native-backups/HEAD.before').read_bytes() == (W / '.git/HEAD').read_bytes(), 'native HEAD original buffer exact')
    require((PUB / 'native-backups/config.before').read_bytes() == (W / '.git/config').read_bytes(), 'native config original buffer exact')
    require((PUB / 'native-backups/loose-master.before').read_bytes() == (PARENT + '\n').encode(), 'native original master buffer exact')
    old_data, new_data = OLD_INDEX.read_bytes(), (W / '.git/index').read_bytes()
    require((len(old_data), sha(old_data)) == (9057886, OLD_SHA), 'whole actual original index pin')
    require((len(new_data), sha(new_data)) == (9059206, NEW_SHA), 'whole actual current index pin')
    require((PUB / 'native-successor.index').read_bytes() == new_data, 'installed successor matches actual publication buffer')
    old_index, new_index = parse_index(old_data, 'original'), parse_index(new_data, 'successor')
    require((old_index['count'], new_index['count']) == (58712, 58721), 'all native record counts')
    old_entries = {e['path']: e for e in old_index['entries']}
    new_entries = {e['path']: e for e in new_index['entries']}
    require(set(new_entries) - set(old_entries) == {'public/' + p for p in targets['A']}, 'index exact9 additions')
    require(set(old_entries) - set(new_entries) == set(), 'index no deletions')
    protected = set(old_entries) - gitpaths
    require(len(protected) == 58710, 'protected native record count')
    require(all(old_entries[p]['raw'] == new_entries[p]['raw'] for p in protected), 'every whole protected native record byte exact')
    selected = []
    expected_records = {p: old_entries[p]['raw'] for p in protected}
    for public_path in paths:
        p = 'public/' + public_path
        entry = new_entries[p]
        data = (STAGE / 'candidate/public' / public_path).read_bytes()
        fs = (W / p).lstat()
        require(stat.S_ISREG(fs.st_mode) and stat.S_IMODE(fs.st_mode) == 0o644, 'selected native regular payload mode')
        expected_stat = [fs.st_ctime_ns // 10**9, fs.st_ctime_ns % 10**9,
                         fs.st_mtime_ns // 10**9, fs.st_mtime_ns % 10**9,
                         fs.st_dev, fs.st_ino, 0o100644, fs.st_uid, fs.st_gid, fs.st_size]
        expected_stat = [n & 0xffffffff for n in expected_stat]
        require(entry['stat'] == expected_stat, 'selected complete native stat fields ' + p)
        oid = object_oid('blob', data)
        flags = min(len(os.fsencode(p)), 0xfff)
        raw = struct.pack('!10I20sH', *expected_stat, bytes.fromhex(oid), flags) + os.fsencode(p) + b'\0'
        raw += b'\0' * ((-len(raw)) % 8)
        require(entry['raw'] == raw, 'selected exact native record derivation ' + p)
        require(entry['stage'] == 0 and not entry['assume_valid'] and entry['mode'] == '100644' and entry['OID'] == oid, 'selected native semantic entry ' + p)
        expected_records[p] = raw
        selected.append({'path': p, 'operation': 'A' if public_path in targets['A'] else 'M',
                         'old': record_evidence(old_entries[p]) if p in old_entries else None,
                         'new': record_evidence(entry), 'payload_SHA256': sha(data), 'payload_bytes': len(data), 'native_stat_matches_current_file': True})
    require([e['raw'] for e in old_index['extensions']] == [e['raw'] for e in new_index['extensions']], 'all native extension raw bytes/order preserved')
    require({e['signature'] for e in old_index['extensions']} == {'TREE'}, 'actual complete extension set is known TREE')
    reconstructed = b'DIRC' + struct.pack('!II', 2, len(expected_records))
    reconstructed += b''.join(expected_records[p] for p in sorted(expected_records, key=os.fsencode))
    reconstructed += b''.join(e['raw'] for e in old_index['extensions'])
    reconstructed += hashlib.sha1(reconstructed).digest()
    require(reconstructed == new_data, 'whole successor index independently reconstructed byte exact')
    write('ALL_NATIVE_RECORDS.json', {'old': [record_evidence(e) for e in old_index['entries']],
                                      'new': [record_evidence(e) for e in new_index['entries']],
                                      'protected_whole_records': len(protected), 'selected': selected})
    check('entire original/successor indices independently parsed and successor reconstructed', old_records=58712, new_records=58721, protected_whole_raw_records=58710, selected_records=11, foreign_stages=0)

    extension = old_index['extensions'][0]
    require(len(extension['raw']) == 35878 and sha(extension['raw']) == TREE_SHA, 'whole TREE header/payload pin')
    require(len(extension['payload']) == 35870 and sha(extension['payload']) == PAYLOAD_SHA, 'TREE payload distinct pin')
    cache = parse_cache(extension['payload'])
    invalid = {p for p, row in cache.items() if row['count'] < 0}
    require(len(cache) == 983 and len(cache) - len(invalid) == 977 and invalid == INVALID, 'all983 TREE nodes and six original invalid nodes')
    old_trees, new_trees = build_trees(old_index['entries']), build_trees(new_index['entries'])
    require(new_trees['']['OID'] == EXPECTED_TREE, 'full successor in-memory root tree')
    for p, row in cache.items():
        require(p in old_trees and p in new_trees, 'every existing cache path present in both full indices')
        require(row['subtree_count'] == len(row['children']), 'cache direct subtree cardinality')
        require(set(row['children']) <= set(old_trees[p]['directories']) and set(row['children']) <= set(new_trees[p]['directories']), 'cache children map to actual immediate directories')
        if row['count'] >= 0:
            for trees in [old_trees, new_trees]:
                require(row['count'] == trees[p]['count'] and row['OID'] == trees[p]['OID'], 'every valid cache count/OID independently reconstructed ' + p)
                require(set(row['children']) == set(trees[p]['directories']), 'every valid cache full immediate subtree set ' + p)
        else:
            require(row['count'] == -1 and row['OID'] is None, 'native invalid cache has -1 and no OID')
    check('complete TREE semantics reconstructed from both native indices', nodes=len(cache), valid_nodes=977, invalid_paths=sorted(invalid), old_tree=old_trees['']['OID'], new_tree=new_trees['']['OID'])

    commits = git_batch('GIT_COMMITS', [PARENT, SUCCESSOR])
    require(all(value[0] == 'commit' for value in commits.values()), 'actual commit object types')
    parent_commit = commit_fields(commits[PARENT][1])
    successor_commit = commit_fields(commits[SUCCESSOR][1])
    require(parent_commit['tree'] == old_trees['']['OID'], 'actual complete parent root equals original index tree')
    require(successor_commit['tree'] == new_trees['']['OID'] == EXPECTED_TREE, 'actual successor root equals reconstructed index tree')
    require(successor_commit['parent'] == [PARENT], 'actual exact sole parent')
    date = datetime.datetime.fromisoformat(auth['commit_date'])
    identity = auth['author_name'] + ' <' + auth['author_email'] + '> ' + str(int(date.timestamp())) + ' +0000'
    require(successor_commit['author'] == identity and successor_commit['committer'] == identity, 'actual fixed author/committer identity and timestamp')
    require(successor_commit['message'] == plan['commit_message'] + '\n', 'actual exact commit message')
    require(commits[SUCCESSOR][1] == (PUB / 'commit-object.txt').read_bytes(), 'actual commit payload vs saved literal commit buffer')
    blob_oids = {new_entries['public/' + p]['OID'] for p in paths} | {old_entries['public/' + p]['OID'] for p in targets['M']}
    tree_oids = {r['OID'] for r in old_trees.values()} | {r['OID'] for r in new_trees.values()} | {r['OID'] for r in cache.values() if r['OID']}
    objects = git_batch('GIT_TREES_AND_SELECTED_BLOBS', sorted(tree_oids | blob_oids))
    for trees in [old_trees, new_trees]:
        for p, row in trees.items():
            require(objects[row['OID']] == ('tree', row['payload']), 'actual whole recursive Git tree object vs independent payload ' + p)
    old_leaves, actual_old_trees = actual_leaves(parent_commit['tree'], objects)
    new_leaves, actual_new_trees = actual_leaves(successor_commit['tree'], objects)
    require(old_leaves == semantic_map(old_index['entries']), 'zero foreign original staging vs complete actual parent leaves')
    require(new_leaves == semantic_map(new_index['entries']), 'zero foreign successor staging vs complete actual HEAD leaves')
    require(set(new_leaves) - set(old_leaves) == {'public/' + p for p in targets['A']}, 'actual commit nine additions')
    require(set(old_leaves) - set(new_leaves) == set(), 'actual commit no deletions')
    leaf_changes = {p for p in old_leaves if old_leaves[p] != new_leaves[p]}
    require(leaf_changes == {'public/' + p for p in targets['M']}, 'actual commit two replacements')
    require(all(old_leaves[p] == new_leaves[p] for p in protected), 'all58710 unrelated actual commit leaves preserved')
    for p, row in cache.items():
        if row['count'] >= 0:
            for actual in [actual_old_trees, actual_new_trees]:
                require(actual[p]['OID'] == row['OID'] and actual[p]['count'] == row['count'], 'valid TREE vs actual recursively decoded Git object count/OID')
                require(set(actual[p]['directories']) == set(row['children']), 'valid TREE actual child topology')
    for p in paths:
        require(objects[new_entries['public/' + p]['OID']] == ('blob', (STAGE / 'candidate/public' / p).read_bytes()), 'all eleven actual new Git blob buffers')
    for p in targets['M']:
        require(objects[old_entries['public/' + p]['OID']] == ('blob', originals[p].read_bytes()), 'both actual original replacement Git blobs')
    write('COMPLETE_COMMIT_LEAVES.json', {'parent': old_leaves, 'successor': new_leaves,
                                        'additions': sorted(set(new_leaves) - set(old_leaves)), 'replacements': sorted(leaf_changes),
                                        'foreign_staging_before': [], 'foreign_staging_after': []})
    tree_evidence = {p: row | {'actual_parent': actual_old_trees[p], 'actual_successor': actual_new_trees[p]} for p, row in cache.items()}
    write('COMPLETE_TREE_CACHE.json', {'whole_extension_bytes': len(extension['raw']), 'whole_extension_SHA256': sha(extension['raw']),
                                     'payload_bytes': len(extension['payload']), 'payload_SHA256': sha(extension['payload']),
                                     'nodes': tree_evidence, 'all_parent_trees': actual_old_trees, 'all_successor_trees': actual_new_trees})
    write('COMMIT_IDENTITIES.json', {'parent_OID': PARENT, 'parent': parent_commit, 'successor_OID': SUCCESSOR,
                                    'successor': successor_commit, 'actual_authorization_commit_date': auth['commit_date'],
                                    'actual_parent_observed_not_remote_push_lease': True})
    check('actual complete parent/new Git objects and leaf maps verified', parent_leaves=len(old_leaves), successor_leaves=len(new_leaves),
          protected_leaves=len(protected), additions=9, replacements=2, deletions=0, foreign_staging_before=0, foreign_staging_after=0,
          valid_cache_entries_verified_against_recursive_actual_Git_objects=977, Git_object_reads=len(commits) + len(objects))
    after = guards()
    write('GUARDS_AFTER.json', after)
    require(same_guards(before, after), 'all guarded before/after bytes modes hidden/empty topology and native local controls exact')
    check('all guarded local snapshots preserved', guarded_trees=list(before['trees']), external_inputs=len(EXTERNAL), native_repositories=2)
    result = {'schema': 'independent-native-index-tree-commit-data-audit-v1', 'UTC': utc(), 'status': 'PASS',
              'completion_percent': 100, 'checks': CHECKS, 'read_only_Git_commands': COMMANDS,
              'scope_paths': sorted(gitpaths), 'invalid_cache_paths': sorted(invalid),
              'old_index_SHA256': sha(old_data), 'new_index_SHA256': sha(new_data),
              'whole_successor_native_index_reconstructed_byte_exact': True,
              'full_original_candidate_installed_public_buffers_verified': True,
              'all_native_controls_preserved_during_this_audit': True,
              'follow_up': None, 'action_authority': False,
              'limits': ['Observed local snapshots only; serialized writers are an operational assumption.',
                         'No claim about remote refs, push lease, deployed content, UI, future persistence, or Firebase state outside public.',
                         'Remote-tracking refs, FETCH_HEAD, nonlocal packed refs and reflogs are excluded from the local-control preservation claim.',
                         'No prior auditor or project/helper/source code was executed or imported; this is the single invocation of this independently written data auditor.']}
    write('DATA_AUDIT.json', result)


if __name__ == '__main__':
    started_utc, started_tick = utc(), time.monotonic()
    try:
        main()
    except BaseException as error:
        write('FAILURE.json', {'UTC': utc(), 'started_UTC': started_utc, 'elapsed_seconds': time.monotonic() - started_tick,
                               'status': 'FAIL_STOP_NO_RETRY', 'error_type': type(error).__name__, 'error': str(error),
                               'checks_completed': CHECKS, 'read_only_Git_commands': COMMANDS,
                               'traceback': traceback.format_exc(), 'follow_up': None})
        raise
