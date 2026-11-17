"""Passive source-preparation custody only; never invokes project code or Git."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import stat
import sys

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
M = Path('/Users/alec/Documents/Math')
W = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
N = P / 'verification/mink-riesz-k3-production-prepare-sol-20261117'
S = P / 'verification/mink-riesz-k3-stage-sol-20261117'
RUN = P / 'verification/mink-riesz-k3-runtime-sol-20261117'

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
    info = path.lstat()
    need(stat.S_ISREG(info.st_mode), 'regular data leaf: ' + str(path))
    data = path.read_bytes()
    after = path.lstat()
    need((info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns, info.st_ctime_ns, info.st_mode) ==
         (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns, after.st_ctime_ns, after.st_mode), 'stable data leaf')
    return data

def pin(path):
    data = raw(path)
    return {'bytes': len(data), 'SHA256': hashlib.sha256(data).hexdigest(), 'mode': format(stat.S_IMODE(path.lstat().st_mode), '04o')}

def snapshot(root):
    info = root.lstat()
    need(stat.S_ISDIR(info.st_mode), 'real namespace root')
    files, directories = {}, {}
    def walk(directory, relative):
        children = sorted(directory.iterdir(), key=lambda item: item.name)
        directories[relative] = {'mode': format(stat.S_IMODE(directory.lstat().st_mode), '04o'), 'empty': not children}
        for child in children:
            name = child.relative_to(root).as_posix()
            item = child.lstat()
            if stat.S_ISDIR(item.st_mode):
                walk(child, name)
            else:
                need(stat.S_ISREG(item.st_mode), 'no symlink or special object')
                files[name] = pin(child)
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

need(len(sys.argv) == 2 and sys.argv[1] in ('GUARDS_BEFORE.json', 'GUARDS_AFTER.json'), 'owned guard destination only')
frozen = json.loads(raw(S / 'GUARDS_BEFORE.json'), object_pairs_hook=unique)
need(set(frozen) == {'schema', 'roots', 'controls', 'public', 'native_M', 'native_W'}, 'actual frozen guard schema')
result = {'schema': 'passive-production-source-preparation-custody-v1',
          'roots': {name: snapshot(Path(name)) for name in frozen['roots']},
          'controls': {name: pin(Path(name)) for name in frozen['controls']},
          'stage': snapshot(S), 'public': snapshot(W / 'public'),
          'native_M': native(M), 'native_W': native(W),
          'website_configuration': {str(W / name): pin(W / name) for name in ('.firebaserc', 'firebase.json')},
          'website_root_mode': format(stat.S_IMODE(W.lstat().st_mode), '04o'), 'runtime_absent': not os.path.lexists(RUN)}
need(result['roots'] == frozen['roots'] and result['controls'] == frozen['controls'] and result['public'] == frozen['public'] and
     result['native_M'] == frozen['native_M'] and result['native_W'] == frozen['native_W'] and result['runtime_absent'], 'all frozen protected data/native/public bindings remain exact')
need(result['native_W']['resolved_native_HEAD'] == '217d41c0a9344aed9caacee7aed31d4f23b77e47' and
     result['native_W']['index']['SHA256'] == '25494ed68b5d5612ae64ac01f2897c77b26024a994b66167426203d5620de4b7', 'actual current website baseline')
destination = N / sys.argv[1]
data = (json.dumps(result, ensure_ascii=False, indent=2) + '\n').encode()
with destination.open('xb') as stream:
    stream.write(data)
os.chmod(destination, 0o644)
print(json.dumps({'UTC': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'destination': str(destination), 'bytes': len(data), 'SHA256': hashlib.sha256(data).hexdigest(), 'protected_checks': 'PASS', 'production_helper_executed': False}, sort_keys=True))
