"""One passive fixed-scope data binding; never imports or executes project code."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import re
import stat
import struct
import zlib

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
V = P / 'verification'
W = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
S = V / 'radial-tree-stage-sol-20261117'
A = V / 'radial-tree-stage-implementation-audit-sol-20261117'
I = V / 'radial-tree-stage-audit-sol-20261117'
CHECKS = []

def need(condition, message):
    if not condition:
        raise ValueError(message)

def pairs(items):
    result = {}
    for key, value in items:
        need(key not in result, 'Duplicate JSON key')
        result[key] = value
    return result

def readj(path):
    return json.loads(path.read_bytes(), object_pairs_hook=pairs)

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def mode(value):
    need(type(value) in (str, int), 'Mode type')
    return format(int(value, 8) if isinstance(value, str) else value, '04o')

def row(path):
    first = path.lstat()
    need(stat.S_ISREG(first.st_mode), 'Ordinary input file')
    raw = path.read_bytes()
    last = path.lstat()
    need((first.st_dev, first.st_ino, first.st_size, first.st_mode, first.st_mtime_ns, first.st_ctime_ns) == (last.st_dev, last.st_ino, last.st_size, last.st_mode, last.st_mtime_ns, last.st_ctime_ns), 'Stable full data read')
    return {'bytes': len(raw), 'SHA256': sha(raw), 'mode': mode(stat.S_IMODE(first.st_mode))}

def pin(path):
    return {'path': str(path), **row(path)}

def normalized(snapshot):
    need(set(snapshot) == {'root', 'root_mode', 'files', 'directories'}, 'Mapped snapshot schema')
    files, dirs = {}, {}
    for name, value in snapshot['files'].items():
        q = Path(name)
        need(q.as_posix() == name and not q.is_absolute() and '..' not in q.parts and set(value) == {'bytes', 'SHA256', 'mode'}, 'Complete canonical file row')
        need(type(value['bytes']) is int and value['bytes'] >= 0 and re.fullmatch('[0-9a-f]{64}', value['SHA256']), 'Whole row scalar types')
        files[name] = {**value, 'mode': mode(value['mode'])}
    for name, value in snapshot['directories'].items():
        q = Path(name)
        need(q.as_posix() == name and not q.is_absolute() and '..' not in q.parts and name not in files, 'Canonical directory row')
        dirs[name] = mode(value)
    return {'root': snapshot['root'], 'root_mode': mode(snapshot['root_mode']), 'files': files, 'directories': dirs}

def census(root):
    need(stat.S_ISDIR(root.lstat().st_mode), 'Ordinary root')
    files, dirs = {}, {}
    for parent, childdirs, childfiles in os.walk(root, followlinks=False):
        parent = Path(parent)
        for name in childdirs:
            f = parent / name
            need(stat.S_ISDIR(f.lstat().st_mode), 'No symlink directory')
            dirs[f.relative_to(root).as_posix()] = mode(stat.S_IMODE(f.lstat().st_mode))
        for name in childfiles:
            f = parent / name
            files[f.relative_to(root).as_posix()] = row(f)
    return normalized({'root': str(root), 'root_mode': mode(stat.S_IMODE(root.lstat().st_mode)), 'files': files, 'directories': dirs})

def native(repo):
    g = repo / '.git'
    loose = census(g / 'refs/heads')
    lines = [line for line in (g / 'packed-refs').read_bytes().decode('ascii').splitlines() if re.fullmatch('[0-9a-f]{40} refs/heads/\\S+', line)]
    refs = {}
    for line in lines:
        oid, name = line.split(' ', 1)
        need(name not in refs, 'Unique packed local branch')
        refs[name] = oid
    for name in loose['files']:
        refs['refs/heads/' + name] = (g / 'refs/heads' / name).read_bytes().decode('ascii').strip()
    raw_head = (g / 'HEAD').read_bytes().decode('ascii')
    need(raw_head.startswith('ref: refs/heads/') and raw_head.endswith('\n'), 'Exact local symbolic HEAD')
    return {'root': str(repo), 'files': {name: row(g / name) for name in ['HEAD', 'index', 'config']}, 'HEAD_raw': raw_head, 'local_branch': raw_head[5:].strip(), 'local_OID': refs[raw_head[5:].strip()], 'loose_local_heads': loose, 'packed_local_head_lines': lines, 'packed_refs_mode': mode(stat.S_IMODE((g / 'packed-refs').lstat().st_mode))}

def parse_index(raw, targets):
    need(len(raw) == 9057886 and sha(raw) == 'e6285d49b7249ae2c88a1f624ca98c1dcf480424db272c4fe111ca91dbdafb5e', 'Exact current native index pin')
    need(struct.unpack('>4sII', raw[:12]) == (b'DIRC', 2, 58712) and hashlib.sha1(raw[:-20]).digest() == raw[-20:], 'Complete checksum-valid v2 index')
    pos, records = 12, {}
    for number in range(58712):
        start = pos
        need(pos + 62 <= len(raw) - 20, 'Bounded index record')
        flags = struct.unpack('>H', raw[pos + 60:pos + 62])[0]
        need(not flags & 0x7000, 'Stage-zero v2 entries without extended flags')
        end = raw.index(b'\0', pos + 62, len(raw) - 20)
        name = raw[pos + 62:end]
        pos = start + ((end + 1 - start + 7) // 8) * 8
        need(name and name not in records and (not records or next(reversed(records)) < name) and flags & 0xFFF == min(len(name), 0xFFF) and pos <= len(raw) - 20 and not any(raw[end + 1:pos]), 'Sorted full raw record name/flags/padding')
        records[name] = {'raw': raw[start:pos], 'mode': struct.unpack('>I', raw[start + 24:start + 28])[0], 'OID': raw[start + 40:start + 60]}
    ext_start, extensions, tree_payload = pos, [], None
    while pos < len(raw) - 20:
        need(pos + 8 <= len(raw) - 20, 'Extension header')
        kind, size = raw[pos:pos + 4], struct.unpack('>I', raw[pos + 4:pos + 8])[0]
        need(pos + 8 + size <= len(raw) - 20, 'Complete extension payload')
        whole, payload = raw[pos:pos + 8 + size], raw[pos + 8:pos + 8 + size]
        extensions.append({'signature_hex': kind.hex(), 'whole_bytes': len(whole), 'whole_SHA256': sha(whole), 'payload_bytes': len(payload), 'payload_SHA256': sha(payload)})
        if kind == b'TREE':
            need(tree_payload is None, 'Unique TREE extension')
            tree_payload = payload
        pos += 8 + size
    need(pos == len(raw) - 20 and tree_payload is not None, 'Complete extension extent')
    root = {}
    for name, record in records.items():
        parts, node = name.split(b'/'), root
        need(all(part and part not in (b'.', b'..') for part in parts), 'Canonical raw index components')
        for part in parts[:-1]:
            node = node.setdefault(part, {})
            need(type(node) is dict, 'No index file/directory collision')
        need(parts[-1] not in node, 'Unique native tree leaf')
        node[parts[-1]] = (record['mode'], record['OID'])
    raw_trees = {}
    def tree(node, path):
        entries, leaves = [], 0
        for name, value in node.items():
            if type(value) is dict:
                oid, count = tree(value, path + [name])
                entries.append((name + b'/', b'40000 ' + name + b'\0' + oid))
                leaves += count
            else:
                kind, oid = value
                need(kind in (0o100644, 0o100755, 0o120000, 0o160000), 'Supported raw tree leaf mode')
                entries.append((name + b'\0', format(kind, 'o').encode() + b' ' + name + b'\0' + oid))
                leaves += 1
        body = b''.join(value for key, value in sorted(entries))
        oid = hashlib.sha1(b'tree ' + str(len(body)).encode() + b'\0' + body).digest()
        raw_trees[b'/'.join(path)] = {'OID': oid.hex(), 'entry_count': leaves}
        return oid, leaves
    native_tree, count = tree(root, [])
    tp, cache_rows = 0, []
    def cache(parent):
        nonlocal tp
        start = tp
        end = tree_payload.index(b'\0', tp)
        component = tree_payload[tp:end]
        newline = tree_payload.index(b'\n', end + 1)
        fields = tree_payload[end + 1:newline].split(b' ')
        need(len(fields) == 2, 'TREE count fields')
        entries, children = map(int, fields)
        need(entries >= -1 and children >= 0, 'TREE valid/preinvalidated count state')
        tp = newline + 1
        oid = None
        if entries >= 0:
            need(tp + 20 <= len(tree_payload), 'TREE valid OID extent')
            oid = tree_payload[tp:tp + 20].hex()
            tp += 20
        path = parent + ([component] if component else [])
        full = b'/'.join(path)
        if entries >= 0:
            need(full in raw_trees and raw_trees[full] == {'OID': oid, 'entry_count': entries}, 'Every original valid TREE OID/count matches independent raw-entry tree')
        cache_rows.append({'path_hex': full.hex(), 'entry_count': entries, 'subtree_count': children, 'OID': oid, 'header_and_OID_bytes': tp - start, 'header_and_OID_SHA256': sha(tree_payload[start:tp])})
        for child in range(children):
            cache(path)
    cache([])
    need(tp == len(tree_payload) and len({r['path_hex'] for r in cache_rows}) == len(cache_rows), 'Whole unique cached TREE traversal')
    valid = sum(r['entry_count'] >= 0 for r in cache_rows)
    invalid = [r for r in cache_rows if r['entry_count'] < 0]
    need((valid, len(invalid)) == (977, 6), 'Actual977valid6preexistinginvalidated TREE records')
    target_bytes = {name.encode() for name in targets}
    existing = set(records) & target_bytes
    need(existing == {b'public/research/index.html', b'public/research/sitemap.xml'}, 'Only exact two targets preexist in native index')
    protected = b''.join(value['raw'] for name, value in records.items() if name not in target_bytes)
    need(len(records) - len(existing) == 58710 and count == 58712, 'Protected58710 native records')
    return {'version': 2, 'records': 58712, 'protected_untargeted_whole_raw_records': 58710, 'prospective_records': 58721, 'protected_raw_records_bytes': len(protected), 'protected_raw_records_SHA256': sha(protected), 'whole_extension_region': {'bytes': len(raw[ext_start:-20]), 'SHA256': sha(raw[ext_start:-20])}, 'extensions': extensions, 'TREE_records': cache_rows, 'TREE_valid_records': valid, 'TREE_preexisting_invalidated_records': invalid, 'every_valid_TREE_node_matches_independent_native_raw_entry_tree': True, 'native_semantic_tree_OID': native_tree.hex(), 'index_checksum_SHA1': raw[-20:].hex()}

adoption = V / 'root-radial-tree-stage-adoption-20261117.json'
need(row(adoption)['SHA256'] == 'e3b1e166db8647ac88846024ad5829271f1dd42219a74c0007c7a9c9e24792f6', 'Actual root stage adoption')
accepted = readj(adoption)
need(accepted['status'] == 'ADOPTED_PRIVATE_STAGE_FIDELITY' and accepted['action_authority_from_this_receipt'] is False, 'Preparation adoption only')
old = readj(A / 'DATA_AUDIT.json')['evidence']
need(row(A / 'DATA_AUDIT.json')['SHA256'] == '1d4a484abe12a2997491f516a3a88f33427a1cf847b33b239b3a2b32e0b5fa48', 'Frozen independent full evidence')
expected = {str(S): old['stage804'], str(I): old['INITIAL'], str(W / 'public'): old['current_public772'], **old['private186'], **old['source233']}
current = {}
for name, value in expected.items():
    current[name] = census(Path(name))
    need(current[name] == normalized(value), 'Complete adopted current namespace: ' + name)
audit = census(A)
need((len(audit['files']), len(audit['directories'])) == (11, 0), 'Frozen independent audit11/0')
need(row(A / 'FINAL.json')['SHA256'] == '592daf99dbbdf169e7743d948f65e3a1bed4392f0dff4e8f150e7c65f4a8f5d4' and row(A / 'OWNED_MANIFEST.json')['SHA256'] == '04d6b8d39946df7b6292b2f6681f17790df8f4a7bc52a1695849fe242dec1970', 'Actual adopted audit terminal pins')
am = readj(A / 'OWNED_MANIFEST.json')
need(set(am['exact_terminal_recursive_hash_exclusions']) == {str(A / 'FINAL.json'), str(A / 'OWNED_MANIFEST.json')}, 'Audit exact terminal exclusions')
for value in am['files']:
    if not value.get('terminal_control'):
        need(audit['files'][value['path']] == {key: value[key] for key in ['bytes', 'SHA256', 'mode']}, 'Every frozen audit payload')
targets = readj(S / 'TARGETS.json')
git_targets = ['public/' + name for name in targets['A'] + targets['M']]
need(len(set(git_targets)) == 11 and (len(targets['A']), len(targets['M']), len(targets['new_directories'])) == (9, 2, 4), 'Exact11Gitrelative9A2M4dirs projection')
native_before = {'M': native(P.parent), 'W': native(W)}
for name, value in native_before.items():
    prior = old['native_controls'][name]
    need(value['files'] == {key: {**item, 'mode': mode(item['mode'])} for key, item in prior['files'].items()} and value['HEAD_raw'] == prior['HEAD'] + '\n' and value['local_OID'] == prior['resolved_local_HEAD'] and value['loose_local_heads'] == normalized(prior['local_heads']) and value['packed_local_head_lines'] == prior['packed_local_head_lines'] and value['packed_refs_mode'] == mode(prior['packed_refs_mode']), 'Current native controls match adopted stage-audit baseline')
need(native_before['M']['local_OID'] == 'a4ce3c37dad209339e490d18dcced6c48cf912d2' and native_before['M']['files']['index']['SHA256'] == '91b10d938f7d737226662bbff3b07016dcc0e501376a045811ab4e930c6fbb11', 'Native M distinct from scoped remote')
need(native_before['W']['local_OID'] == '96f04aa5544df69daba07a9ed4d6212172e9984a', 'Current W master parent')
index = parse_index((W / '.git/index').read_bytes(), git_targets)
head_object = W / '.git/objects/96/f04aa5544df69daba07a9ed4d6212172e9984a'
head = {'commit': native_before['W']['local_OID'], 'loose_object_present': head_object.is_file()}
if head['loose_object_present']:
    raw = zlib.decompress(head_object.read_bytes())
    need(hashlib.sha1(raw).hexdigest() == native_before['W']['local_OID'] and raw.startswith(b'commit '), 'Exact native loose HEAD object')
    body = raw.split(b'\0', 1)[1]
    lines = body.split(b'\n\n', 1)[0].splitlines()
    head.update({'body_SHA256': sha(body), 'tree': next(x[5:].decode() for x in lines if x.startswith(b'tree ')), 'author': next(x[7:].decode() for x in lines if x.startswith(b'author ')), 'committer': next(x[10:].decode() for x in lines if x.startswith(b'committer '))})
    head['native_semantic_tree_equals_HEAD_tree'] = index['native_semantic_tree_OID'] == head['tree']
need(native_before == {'M': native(P.parent), 'W': native(W)}, 'Whole native controls unchanged after passive data read')
need(census(A) == audit and all(census(Path(name)) == value for name, value in current.items()), 'Complete protected scopes unchanged after passive read')
for name, expected_hash in [('root-radial-editorial-adoption-20261117.json', '6534222701fac84e060d60b84bf54112165aa796c17af7d0bf548ef23114ca3b'), ('root-designed-tree-editorial-adoption-20261117.json', '76547b8593fe8bc8df5e8c0224421072fac75b464c3704eb733c7b5f3b3687f1')]:
    need(row(V / name)['SHA256'] == expected_hash, 'Original accepted family adoption')
result = {'schema': 'independent-radial-tree-production-passive-binding-v1', 'UTC': datetime.now(timezone.utc).isoformat(), 'status': 'INPUT_BINDINGS_VERIFIED_NO_IMPLEMENTATION_RESULT', 'root_stage_adoption': pin(adoption), 'root_stage_actual_schema': accepted['schema'], 'root_stage_actual_status': accepted['status'], 'stage_family_adoption_pins': [pin(V / name) for name in ['root-radial-editorial-adoption-20261117.json', 'root-designed-tree-editorial-adoption-20261117.json']], 'protected_namespaces': current, 'independent_audit': audit, 'native_controls': native_before, 'native_index_semantics': index, 'native_HEAD_observation': head, 'target_plan_original_public_root_relative': targets, 'exact_Git_relative_targets_add_public_once': git_targets, 'new_preparation_or_implementation_opened': False, 'project_import_Git_network_or_protected_write': False, 'own_passive_invocations': 1}
print(json.dumps(result, indent=2, ensure_ascii=True))
