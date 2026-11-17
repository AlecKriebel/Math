"""One passive data-only capture; no project imports, Git, network or helper execution."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import stat

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
M = P.parent
W = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
O = P / 'verification/mink-riesz-k3-production-prepare-sol-20261117'
N = P / 'verification/mink-riesz-k3-production-prepare-v2-sol-20261117'
S = P / 'verification/mink-riesz-k3-stage-sol-20261117'
RUN = P / 'verification/mink-riesz-k3-runtime-sol-20261117'
ADOPTION = P / 'verification/root-mink-riesz-k3-stage-adoption-20261117.json'

def need(value, message):
    if not value:
        raise ValueError(message)

def unique(pairs):
    result = {}
    for key, value in pairs:
        need(key not in result, 'duplicate JSON key')
        result[key] = value
    return result

def raw(path):
    need(path.is_absolute() and all(not item.is_symlink() for item in (path, *path.parents)), 'real absolute data path')
    first = path.lstat()
    need(stat.S_ISREG(first.st_mode), 'ordinary data leaf')
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    try:
        before = os.fstat(fd)
        need((first.st_dev, first.st_ino) == (before.st_dev, before.st_ino), 'held leaf identity')
        blocks = []
        while True:
            block = os.read(fd, 1048576)
            if not block:
                break
            blocks.append(block)
        after = os.fstat(fd)
        fields = ('st_dev', 'st_ino', 'st_size', 'st_mtime_ns', 'st_ctime_ns', 'st_mode')
        need(tuple(getattr(before, key) for key in fields) == tuple(getattr(after, key) for key in fields), 'stable complete data read')
        need((path.lstat().st_dev, path.lstat().st_ino) == (after.st_dev, after.st_ino), 'live held leaf')
        data = b''.join(blocks)
        need(len(data) == before.st_size, 'whole data buffer')
        return data
    finally:
        os.close(fd)

def pin(path):
    data = raw(path)
    return {'bytes': len(data), 'SHA256': hashlib.sha256(data).hexdigest(), 'mode': format(stat.S_IMODE(path.lstat().st_mode), '04o')}

def load(path):
    return json.loads(raw(path), object_pairs_hook=unique)

def snapshot(root):
    need(stat.S_ISDIR(root.lstat().st_mode) and all(not item.is_symlink() for item in (root, *root.parents)), 'real namespace root')
    files, directories = {}, {}
    def walk(directory, relative):
        before = directory.lstat()
        children = sorted(directory.iterdir(), key=lambda item: item.name)
        directories[relative] = {'mode': format(stat.S_IMODE(before.st_mode), '04o'), 'empty': not children}
        for child in children:
            name = child.relative_to(root).as_posix()
            info = child.lstat()
            if stat.S_ISDIR(info.st_mode):
                walk(child, name)
            else:
                need(stat.S_ISREG(info.st_mode), 'no symlink or special object')
                files[name] = pin(child)
        after = directory.lstat()
        fields = ('st_dev', 'st_ino', 'st_mode', 'st_mtime_ns', 'st_ctime_ns')
        need(tuple(getattr(before, key) for key in fields) == tuple(getattr(after, key) for key in fields), 'stable whole namespace enumeration')
    walk(root, '.')
    return {'root': str(root), 'files': files, 'directories': directories, 'regular_files': len(files), 'child_directories': len(directories) - 1}

def native(root):
    directory = root / '.git'
    text = raw(directory / 'HEAD').decode('ascii')
    need(text.startswith('ref: refs/heads/') and text.endswith('\n'), 'native symbolic local branch')
    branch = text[5:-1]
    packed = directory / 'packed-refs'
    lines = raw(packed).decode('ascii').splitlines(keepends=True)
    local = [line for line in lines if not line.startswith(('#', '^')) and ' refs/heads/' in line]
    need(len(local) == len({line.split(' ', 1)[1] for line in local}), 'unique local packed heads')
    leaf = directory / branch
    matches = [line.split(' ', 1)[0] for line in local if line.rstrip('\n').endswith(' ' + branch)]
    resolved = raw(leaf).decode('ascii').strip() if os.path.lexists(leaf) else (matches[0] if len(matches) == 1 else None)
    need(resolved is not None, 'actual native local branch resolution')
    optional = directory / 'config.worktree'
    return {**{name: pin(directory / name) for name in ('HEAD', 'index', 'config')}, 'HEAD_text': text,
            'local_loose_heads': snapshot(directory / 'refs/heads'),
            'packed_local_heads': {'file_mode': format(stat.S_IMODE(packed.lstat().st_mode), '04o'), 'raw_lines': local},
            'resolved_native_HEAD': resolved, 'optional_worktree_config': pin(optional) if os.path.lexists(optional) else None}

need(pin(O / 'FINAL.json') == {'bytes': 11407, 'SHA256': '9ed064c8ce6c6c226acfce9b76bfdc0d7bcc9acd179b08da5f9b310dc66113a1', 'mode': '0644'}, 'exact immutable original FINAL')
need(pin(O / 'OWNED_MANIFEST.json') == {'bytes': 3816, 'SHA256': '59c6c63bd49acbcb691b9c9f624ac0ee8b910483c1b1f4e665e428fdc90f0308', 'mode': '0644'}, 'exact immutable original manifest')
old = snapshot(O)
manifest = load(O / 'OWNED_MANIFEST.json')
expected = {row['path']: {key: row[key] for key in ('bytes', 'SHA256', 'mode')} for row in manifest['payload_files']}
need(len(expected) == len(manifest['payload_files']) == 12, 'unique original twelve payload rows')
expected.update({name: pin(O / name) for name in ('FINAL.json', 'OWNED_MANIFEST.json')})
need(old['files'] == expected and old['directories'] == {'.': {'mode': '0755', 'empty': False}} and (old['regular_files'], old['child_directories']) == (14, 0), 'entire original14/0 bytes/modes/topology unchanged')
baseline = load(O / 'GUARDS_AFTER.json')
current = {'schema': baseline['schema'], 'roots': {name: snapshot(Path(name)) for name in baseline['roots']},
           'controls': {name: pin(Path(name)) for name in baseline['controls']}, 'stage': snapshot(S),
           'public': snapshot(W / 'public'), 'native_M': native(M), 'native_W': native(W),
           'website_configuration': {name: pin(Path(name)) for name in baseline['website_configuration']},
           'website_root_mode': format(stat.S_IMODE(W.lstat().st_mode), '04o'), 'runtime_absent': not os.path.lexists(RUN)}
need(current == baseline, 'all inherited source/private/stage/native/public/configuration custody exact')
adoption = load(ADOPTION)
need(adoption['status'] == 'ACCEPTED_PRIVATE_STAGE_ONLY' and adoption['future_action_authority'] is False, 'actual root private-stage adoption is no action authority')
new_source, old_source = raw(N / 'release_three.py'), raw(O / 'release_three.py')
need(hashlib.sha256(old_source).hexdigest() == '06ce7edaf8edd2dcda4e78ce0e5e259efc1bbb867df00daf2765d155b5c47122', 'original source remains stale and exact')
before = b'stdout_base64=None if opaque else base64.b64encode(result.stdout).decode()'
after = b'stdout_base64=base64.b64encode(result.stdout).decode()'
old_hash = b'7ae4db13a10f9bb03de008fd9f06688bf44b9af54bb5b40c82dd7713d30e6654'
new_hash = b'a039e52df5a04d5e8a6c4dec4709bebb1858f4757efd11c09c9e35c1a67aaf24'
old_root = b'verification/mink-riesz-k3-production-prepare-sol-20261117'
new_root = b'verification/mink-riesz-k3-production-prepare-v2-sol-20261117'
need(all(new_source.count(token) == 1 for token in (new_root, new_hash, after)), 'exact three unique source changes')
need(new_source.replace(new_root, old_root).replace(new_hash, old_hash).replace(after, before) == old_source, 'whole unchanged source correspondence after reversing only three literal edits')
need(raw(N / 'PLAN.json').replace(str(N).encode(), str(O).encode()) == raw(O / 'PLAN.json'), 'PLAN differs only by preparation-root relocation')
need(raw(N / 'TARGETS.json') == raw(O / 'TARGETS.json') == raw(S / 'TARGETS.json'), 'whole target bytes unchanged')
own = snapshot(N)
payload_names = {'release_three.py', 'PLAN.json', 'TARGETS.json', 'SOURCE.diff', 'PLAN.diff', 'REPORT.md', 'READ_LEDGER.json', 'RESEARCH_LOG.md', 'capture_v2_custody.py'}
need(set(own['files']) == payload_names | {'FINAL.json', 'OWNED_MANIFEST.json'} and own['child_directories'] == 0 and own['directories']['.']['mode'] == '0755' and all(row['mode'] == '0644' for row in own['files'].values()), 'exact preterminal source-only namespace')
result = {'schema': 'mink-riesz-k3-production-v2-one-passive-custody-v1', 'UTC': datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'status': 'PASS_PASSIVE_DATA_CUSTODY_AND_NARROW_BYTE_CORRESPONDENCE', 'original_packet': old, 'protected': current,
          'inherited_original_guard': {'path': str(O / 'GUARDS_AFTER.json'), **pin(O / 'GUARDS_AFTER.json')},
          'root_private_stage_adoption': {'path': str(ADOPTION), **pin(ADOPTION)}, 'source_changes_exactly_three': True,
          'PLAN_change_only_preparation_root': True, 'TARGETS_unchanged': True, 'production_helper_executed': False,
          'own_payload_files': [{'path': name, **own['files'][name], 'hidden': False, 'empty': own['files'][name]['bytes'] == 0} for name in sorted(payload_names)]}
data = (json.dumps(result, ensure_ascii=False, indent=2) + '\n').encode()
with (N / 'PROTECTION.json').open('xb') as stream:
    stream.write(data)
os.chmod(N / 'PROTECTION.json', 0o644)
print(json.dumps({'UTC': result['UTC'], 'status': result['status'], 'PROTECTION': {'bytes': len(data), 'SHA256': hashlib.sha256(data).hexdigest(), 'mode': '0644'}, 'own_payload_files': result['own_payload_files'], 'root_private_stage_adoption': result['root_private_stage_adoption'], 'helper': pin(N / 'release_three.py'), 'PLAN': pin(N / 'PLAN.json'), 'old_packet_unchanged': True, 'runtime_absent': current['runtime_absent']}, sort_keys=True))
