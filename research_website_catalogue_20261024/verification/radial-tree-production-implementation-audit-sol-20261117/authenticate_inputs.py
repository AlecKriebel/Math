"""Single passive data authentication; no project imports, Git or network."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import re
import stat

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
I = P / 'verification/radial-tree-production-initial-sol-20261117'
N = P / 'verification/radial-tree-production-preparation-sol-20261117'
W = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')

def need(ok, message):
    if not ok:
        raise ValueError(message)

def pairs(items):
    result = {}
    for key, value in items:
        need(key not in result, 'Duplicate JSON key')
        result[key] = value
    return result

def readj(path):
    return json.loads(path.read_bytes(), object_pairs_hook=pairs)

def row(path):
    first = path.lstat()
    need(stat.S_ISREG(first.st_mode), 'Ordinary file')
    raw = path.read_bytes()
    last = path.lstat()
    need((first.st_dev, first.st_ino, first.st_size, first.st_mode, first.st_mtime_ns, first.st_ctime_ns) == (last.st_dev, last.st_ino, last.st_size, last.st_mode, last.st_mtime_ns, last.st_ctime_ns), 'Stable data read')
    return {'bytes': len(raw), 'SHA256': hashlib.sha256(raw).hexdigest(), 'mode': format(stat.S_IMODE(first.st_mode), '04o')}

def census(root):
    need(stat.S_ISDIR(root.lstat().st_mode), 'Ordinary root')
    files, dirs = {}, {}
    for parent, childdirs, childfiles in os.walk(root, followlinks=False):
        parent = Path(parent)
        for name in childdirs:
            q = parent / name
            need(stat.S_ISDIR(q.lstat().st_mode), 'No symbolic directory')
            dirs[q.relative_to(root).as_posix()] = format(stat.S_IMODE(q.lstat().st_mode), '04o')
        for name in childfiles:
            q = parent / name
            files[q.relative_to(root).as_posix()] = row(q)
    return {'root': str(root), 'root_mode': format(stat.S_IMODE(root.lstat().st_mode), '04o'), 'files': files, 'directories': dirs}

def native(repo):
    g = repo / '.git'
    loose = census(g / 'refs/heads')
    lines = [x for x in (g / 'packed-refs').read_bytes().decode('ascii').splitlines() if re.fullmatch('[0-9a-f]{40} refs/heads/\\S+', x)]
    refs = {}
    for line in lines:
        oid, name = line.split(' ', 1)
        need(name not in refs, 'Unique packed local head')
        refs[name] = oid
    for name in loose['files']:
        refs['refs/heads/' + name] = (g / 'refs/heads' / name).read_bytes().decode('ascii').strip()
    head = (g / 'HEAD').read_bytes().decode('ascii')
    need(head.startswith('ref: refs/heads/') and head.endswith('\n'), 'Symbolic local HEAD')
    return {'root': str(repo), 'files': {name: row(g / name) for name in ['HEAD', 'index', 'config']}, 'HEAD_raw': head, 'local_branch': head[5:].strip(), 'local_OID': refs[head[5:].strip()], 'loose_local_heads': loose, 'packed_local_head_lines': lines, 'packed_refs_mode': format(stat.S_IMODE((g / 'packed-refs').lstat().st_mode), '04o')}

need(row(I / 'INITIAL_SEAL.json')['SHA256'] == '423a3491c0efca80f7bc11449bd9f0f1297615dd40d79dcce3dd47dec8a75ac0', 'Frozen production INITIAL seal')
im, initial = readj(I / 'INITIAL_MANIFEST.json'), census(I)
need(len(initial['files']) == 8 and not initial['directories'], 'Exact INITIAL8/0')
for item in im['files']:
    if not item.get('terminal_control'):
        need(initial['files'][item['path']] == {key: item[key] for key in ['bytes', 'SHA256', 'mode']}, 'INITIAL payload exact')
need(row(I / 'INITIAL_MANIFEST.json')['SHA256'] == '1ac2e5a43651991b240b4b541344ce7a2a50b7953d8d32c4451e5a3dcf812528', 'Frozen INITIAL manifest pin')
old = readj(I / 'INPUT_BINDINGS.json')
need(row(I / 'INPUT_BINDINGS.json')['SHA256'] == 'b0813466900fd23c61c12c5ae777aa5608640080b1bff0bc964acc0de72eced1', 'Actual full input-binding pin')
current = {}
for name, expected in old['protected_namespaces'].items():
    current[name] = census(Path(name))
    need(current[name] == expected, 'Whole adopted namespace still exact: ' + name)
audit = census(Path(old['independent_audit']['root']))
need(audit == old['independent_audit'], 'Whole adopted stage audit11/0')
baseline_native = {'M': native(P.parent), 'W': native(W)}
need(baseline_native == old['native_controls'], 'Current M/W native controls still exact')
producer = census(N)
need(len(producer['files']) == 9 and not producer['directories'] and producer['root_mode'] == '0755' and all(x['mode'] == '0644' for x in producer['files'].values()), 'Whole producer9/0 and modes')
for name, size, sha in [('FINAL.json', 6784, '82304819f1a6f4ab8b6c20c508f145cf1be4526c10b9647c5544d7b8c226717c'), ('OWNED_MANIFEST.json', 2323, '0f2c1089ba6b8dc8ce12977ea9c7470c733b33b8901e7f1b05228f13eb5cd531'), ('release_two.py', 85894, 'c253cf4b3a20bd2499b752e9cb2fece9019a6a0ba10be16b63ff85b7adf7c56d'), ('PLAN.json', 16114, 'd3ee52565eb3658d51f15aad5e2f930abc38c772ff8c0f1c0e8cc88edf342516')]:
    need(producer['files'][name] == {'bytes': size, 'SHA256': sha, 'mode': '0644'}, 'Exact handed-off producer pin')
manifest, final, plan = readj(N / 'OWNED_MANIFEST.json'), readj(N / 'FINAL.json'), readj(N / 'PLAN.json')
need(final['schema'] == 'radial-tree-production-preparation-FINAL-v1' and final['status'] == 'READY_FOR_STATIC_REVIEW', 'Actual producer FINAL schema/status')
need({x['path'] for x in manifest['files']} == set(producer['files']) and len(manifest['files']) == 9 and manifest['directories'] == [], 'Whole producer manifest path set')
for item in manifest['files']:
    if not item.get('terminal_control'):
        need(producer['files'][item['path']] == {key: item[key] for key in ['bytes', 'SHA256', 'mode']}, 'Every producer payload pin')
need(set(manifest['exact_already_created_terminal_recursive_hash_exclusions']) == {str(N / 'FINAL.json'), str(N / 'OWNED_MANIFEST.json')} and manifest['other_exclusions'] == [], 'Exact finite terminal exclusions')
control_pins = {}
for name, item in plan['controls'].items():
    actual = row(Path(item['path']))
    need(actual == {key: item[key] for key in ['bytes', 'SHA256', 'mode']}, 'Actual control pin: ' + name)
    readj(Path(item['path'])) if not item['path'].endswith(('.py', '.md')) else None
    control_pins[name] = item
need(set(plan['scope_paths']) == set(old['exact_Git_relative_targets_add_public_once']) and len(plan['scope_paths']) == 11, 'Exact independent target projection')
need(plan['baseline_TREE_extension'] == {'bytes': 35878, 'SHA256': 'f12d2a0b795034ce5cab45ad6fa5da31b4d7ad6f4b22a5999ce27841b41350b3'} and plan['baseline_TREE_payload'] == {'bytes': 35870, 'SHA256': '6078bbaef4d39e7b0418bc6ed44ad8f37d2733ec6de4a4e4ba165fe7e665bfcb'}, 'Distinct original whole TREE and payload pins')
runtime_absent = not os.path.lexists(Path(plan['runtime_root']))
need(runtime_absent, 'Fresh prospective runtime remains absent')
need(census(I) == initial and census(N) == producer and census(Path(audit['root'])) == audit and all(census(Path(name)) == value for name, value in current.items()), 'All whole packet/source/public guards exact after passive read')
need({'M': native(P.parent), 'W': native(W)} == baseline_native, 'Whole native controls exact after passive read')
print(json.dumps({'schema': 'independent-radial-tree-production-static-input-authentication-v1', 'UTC': datetime.now(timezone.utc).isoformat(), 'status': 'PASS_INPUT_AUTHENTICATION_ONLY', 'ordinary_passive_invocations': 1, 'INITIAL8': initial, 'producer9': producer, 'stage_audit11': audit, 'protected_namespaces': current, 'native_controls': baseline_native, 'all15_control_pins': control_pins, 'inherited_exact_index_TREE_binding': old['native_index_semantics'], 'runtime_absent': runtime_absent, 'project_import_producer_execution_AST_compile_test_Git_network_or_protected_write': False}, indent=2))
