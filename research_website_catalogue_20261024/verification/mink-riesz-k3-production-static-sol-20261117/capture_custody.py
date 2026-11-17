"""One passive data-only custody reader for an unexecuted production-source review."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import re
import stat
import struct

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
A = P / 'verification/mink-riesz-k3-production-static-sol-20261117'
N = P / 'verification/mink-riesz-k3-production-prepare-sol-20261117'
S = P / 'verification/mink-riesz-k3-stage-sol-20261117'
V = P / 'verification/mink-riesz-k3-stage-audit-html-fragments-sol-20261117'
M = P.parent
W = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
RUN = P / 'verification/mink-riesz-k3-runtime-sol-20261117'

def need(value, reason):
    if not value:
        raise AssertionError(reason)

def utc():
    return datetime.now(timezone.utc).isoformat()

def load(path):
    return json.loads(path.read_text())

def pin(path):
    st = path.lstat()
    need(stat.S_ISREG(st.st_mode), 'ordinary file ' + str(path))
    b = path.read_bytes()
    return {'bytes': len(b), 'SHA256': hashlib.sha256(b).hexdigest(), 'mode': format(stat.S_IMODE(st.st_mode), '04o')}

def snap(root):
    files, dirs, seen = {}, {}, set()
    def walk(path, rel):
        st = path.lstat()
        need(stat.S_ISDIR(st.st_mode) and (st.st_dev, st.st_ino) not in seen, 'ordinary unique directory ' + str(path))
        seen.add((st.st_dev, st.st_ino))
        children = sorted(path.iterdir(), key=lambda p: p.name)
        dirs[rel] = {'mode': format(stat.S_IMODE(st.st_mode), '04o'), 'empty': not children}
        for child in children:
            st = child.lstat()
            r = child.relative_to(root).as_posix()
            if stat.S_ISDIR(st.st_mode):
                walk(child, r)
            else:
                need(stat.S_ISREG(st.st_mode) and (st.st_dev, st.st_ino) not in seen, 'ordinary unique file ' + str(child))
                seen.add((st.st_dev, st.st_ino))
                files[r] = pin(child)
    walk(root, '.')
    return {'root': str(root), 'files': files, 'directories': dirs,
            'regular_files': len(files), 'child_directories': len(dirs) - 1}

def native(root):
    g = root / '.git'
    text = (g / 'HEAD').read_text()
    branch = text.strip().removeprefix('ref: ')
    need(text.startswith('ref: refs/heads/'), 'native symbolic local head')
    packed = g / 'packed-refs'
    lines = [x for x in packed.read_text().splitlines(keepends=True)
             if re.fullmatch(r'[0-9a-f]{40} refs/heads/[^\n]+\n?', x)]
    refs = {x.split()[1]: x.split()[0] for x in lines}
    loose = g / branch
    oid = loose.read_text().strip() if loose.exists() else refs[branch]
    return {'HEAD': pin(g / 'HEAD'), 'index': pin(g / 'index'), 'config': pin(g / 'config'),
            'HEAD_text': text, 'local_loose_heads': snap(g / 'refs/heads'),
            'packed_local_heads': {'file_mode': pin(packed)['mode'], 'raw_lines': lines},
            'resolved_native_HEAD': oid,
            'optional_worktree_config': pin(g / 'config.worktree') if os.path.lexists(g / 'config.worktree') else None}

def capture(expected):
    protected = {'schema': expected['schema'], 'roots': {r: snap(Path(r)) for r in expected['roots']},
        'controls': {r: pin(Path(r)) for r in expected['controls']}, 'stage': snap(S), 'public': snap(W / 'public'),
        'native_M': native(M), 'native_W': native(W),
        'website_configuration': {r: pin(Path(r)) for r in expected['website_configuration']},
        'website_root_mode': format(stat.S_IMODE(W.lstat().st_mode), '04o'),
        'runtime_absent': not os.path.lexists(RUN)}
    return {'protected': protected, 'source_preparation': snap(N), 'successful_stage_audit': snap(V)}

def finite(snapshot, manifest_name, final_name, expected_count):
    root = Path(snapshot['root'])
    d = load(root / manifest_name)
    rows = d['payload_files']
    need((snapshot['regular_files'], snapshot['child_directories']) == (expected_count, 0), 'exact finite packet counts ' + str(root))
    need(len(rows) == len({r['path'] for r in rows}) and
         set(snapshot['files']) == {r['path'] for r in rows} | {manifest_name, final_name}, 'whole finite file namespace ' + str(root))
    for r in rows:
        need(snapshot['files'][r['path']] == {k: r[k] for k in ['bytes', 'SHA256', 'mode']}, 'whole payload pin ' + str(root / r['path']))
    dirs = {r['path']: {'mode': r['mode'], 'empty': r['empty']} for r in d['directories']}
    need(dirs == snapshot['directories'], 'root-inclusive directory mode/empty topology ' + str(root))
    need(not d['other_exclusions'], 'no other finite exclusions ' + str(root))

def raw_index():
    b = (W / '.git/index').read_bytes()
    need(b[:4] == b'DIRC' and struct.unpack('>II', b[4:12]) == (2, 58730), 'actual v2 58730 native records')
    need(hashlib.sha1(b[:-20]).digest() == b[-20:], 'native index complete checksum')
    pos, entries, prior = 12, {}, None
    for unused in range(58730):
        start = pos
        end = b.index(b'\0', start + 62, len(b) - 20)
        name = b[start + 62:end]
        pos = start + ((end - start + 1 + 7) // 8) * 8
        flags = struct.unpack('>H', b[start + 60:start + 62])[0]
        need(name and (prior is None or prior < name) and not flags & 0x7000 and
             flags & 0xFFF == min(len(name), 4095) and not any(b[end + 1:pos]), 'whole raw record order/flags/NUL/padding')
        entries[name] = b[start:pos]
        prior = name
    ext = b[pos:-20]
    need(ext[:4] == b'TREE' and struct.unpack('>I', ext[4:8])[0] == len(ext) - 8, 'sole complete TREE extension')
    payload = ext[8:]
    cursor, valid, invalid, paths = 0, 0, [], set()
    def cache(parent, first=False):
        nonlocal cursor, valid
        end = payload.index(b'\0', cursor)
        name = payload[cursor:end]
        line = payload.index(b'\n', end + 1)
        count, children = map(int, payload[end + 1:line].split())
        cursor = line + 1
        path = b'' if first else parent + (b'/' if parent else b'') + name
        need(path not in paths and count >= -1 and children >= 0, 'unique finite TREE path and counts')
        paths.add(path)
        if count >= 0:
            need(cursor + 20 <= len(payload), 'complete valid TREE OID')
            cursor += 20
            valid += 1
        else:
            invalid.append(path.decode())
        for unused in range(children):
            cache(path)
    cache(b'', True)
    need(cursor == len(payload) and len(paths) == 983 and valid == 977, 'whole TREE 983 nodes/977 valid extent')
    p = load(N / 'PLAN.json')
    need(sorted(invalid) == sorted(p['baseline_invalid_TREE_paths']) and len(invalid) == 6, 'actual six invalid TREE paths')
    def bytepin(x):
        return {'bytes': len(x), 'SHA256': hashlib.sha256(x).hexdigest()}
    need(bytepin(ext) == p['baseline_TREE_whole'] and bytepin(payload) == p['baseline_TREE_payload'], 'actual distinct whole TREE and payload pins')
    targets = set(p['scope_paths'])
    need(len(targets) == 15 and set(entries) & {x.encode() for x in targets} ==
         {x.encode() for x in p['replacement_paths']} and len(set(entries) - {x.encode() for x in targets}) == 58728, 'actual15 targets and58728 raw foreign records')
    return {'native_index': bytepin(b), 'TREE_whole': bytepin(ext), 'TREE_payload': bytepin(payload),
            'records': 58730, 'untargeted_records': 58728, 'TREE_nodes': len(paths), 'TREE_valid': valid,
            'TREE_invalid_paths': invalid, 'semantic_object_execution': False}

def put(name, value):
    path = A / name
    need(path.parent == A and not path.exists(), 'fresh own custody output ' + name)
    path.write_text(json.dumps(value, indent=2) + '\n')

def main():
    need(Path(__file__).resolve() == A / 'capture_custody.py', 'fixed own custody code')
    need(not (A / 'CUSTODY_RESULT.json').exists(), 'one passive custody invocation')
    started = utc()
    g = load(N / 'GUARDS_BEFORE.json')
    before = capture(g)
    need(before['protected'] == g and (N / 'GUARDS_BEFORE.json').read_bytes() == (N / 'GUARDS_AFTER.json').read_bytes(), 'current complete source-preparation guard exact')
    need(before['source_preparation']['files']['release_three.py'] == {'bytes': 93428, 'SHA256': '06ce7edaf8edd2dcda4e78ce0e5e259efc1bbb867df00daf2765d155b5c47122', 'mode': '0644'}, 'external exact unexecuted helper source pin')
    finite(before['source_preparation'], 'OWNED_MANIFEST.json', 'FINAL.json', 14)
    finite(before['successful_stage_audit'], 'MANIFEST.json', 'FINAL.json', 22)
    need(pin(V / 'FINAL.json') == {'bytes': 2315, 'SHA256': 'f8207dd322c76addc52bafa3b5472a268f4d6924fce7ea38bdc64036bc82a4a0', 'mode': '0644'}, 'successful stage audit external FINAL pin')
    need(pin(V / 'MANIFEST.json') == {'bytes': 5405, 'SHA256': '8e46e120ca55158bc9e623bb4348263591ac75d405393ff1b85e1b746092f517', 'mode': '0644'}, 'successful stage audit external manifest pin')
    audit = load(V / 'AFTER.json')
    need(before['protected']['stage'] == audit['stage'], 'entire actual1635/770 stage equals successful audit snapshot')
    plan = load(N / 'PLAN.json')
    targets = load(N / 'TARGETS.json')
    need((N / 'TARGETS.json').read_bytes() == (S / 'TARGETS.json').read_bytes() and
         sorted(targets['Git_relative_targets']) == plan['scope_paths'], 'actual exact source/stage target plans')
    need(len(plan['scope_paths']) == 15 and len(targets['additions_public_relative']) == 13 and
         len(targets['modifications_public_relative']) == 2 and len(plan['new_directories']) == 6, 'actual13A2M/15paths/6dirs')
    index = raw_index()
    put('BEFORE.json', {'UTC': started, 'snapshot': before, 'raw_index_summary': index})
    after = capture(g)
    need(after == before, 'all current source/preparation/stage/audit/native/public/config/modes/topology before-after exact')
    put('AFTER.json', {'UTC': utc(), 'snapshot': after, 'raw_index_summary': raw_index()})
    put('CUSTODY_RESULT.json', {'schema': 'static-source-review-passive-custody-v1', 'UTC_start': started, 'UTC_end': utc(),
        'status': 'CUSTODY_EXACT_HELPER_REMAINS_UNFIT_FOR_EXECUTION', 'helper_or_original_program_execution': False,
        'Git_network_runtime_ignore_or_source_mutation': False, 'runtime_absent': True,
        'preparation_files_childdirs': [14, 0], 'stage_files_childdirs': [1635, 770], 'audit_files_childdirs': [22, 0],
        'raw_index': index, 'complete_before_after_exact': True, 'follow_up': None, 'future_action_authority': False})

if __name__ == '__main__':
    main()
