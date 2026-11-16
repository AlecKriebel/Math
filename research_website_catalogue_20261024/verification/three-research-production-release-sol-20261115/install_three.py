#!/usr/bin/env python3
"""Default: read-only preflight. --verify-installed: read-only postinstall.

--install requires a separate exact root authorization. It changes only the19
planned website files/three new directories, using exclusive same-filesystem
moves and owned backups. No Git, deployment, browser, network or source imports.
Race checks provide a bounded final snapshot, not hostile-concurrency isolation.
Any failure stops further website mutations and preserves partial-state evidence.
"""
from pathlib import Path
import ctypes, datetime, hashlib, json, os, re, stat, sys
import xml.etree.ElementTree as ET

N = Path(__file__).absolute().parent
W = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
PLAN_SHA = '0f044fb16240e81bf9a315c0da76cdac3b94b0baadba4055990f9c39ebeee668'
NOFOLLOW = os.O_NOFOLLOW
DIRECTORY = os.O_DIRECTORY

def need(ok, reason):
    if not ok: raise ValueError(reason)

def pin(data): return {'bytes': len(data), 'SHA256': hashlib.sha256(data).hexdigest()}
def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def mode(path): return stat.S_IMODE(path.lstat().st_mode)
def identity(info): return [info.st_dev, info.st_ino]
def digest(value): return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()

def safe(path):
    need(path.is_absolute() and '..' not in path.parts, 'absolute canonical path')
    for item in [path, *path.parents]: need(not item.is_symlink(), 'symlink rejected: ' + str(item))

def held(fd):
    before = os.fstat(fd); need(stat.S_ISREG(before.st_mode), 'ordinary held file')
    os.lseek(fd, 0, os.SEEK_SET); chunks = []
    while True:
        block = os.read(fd, 1048576)
        if not block: break
        chunks.append(block)
    after = os.fstat(fd)
    need((before.st_size, before.st_mtime_ns, before.st_ctime_ns) == (after.st_size, after.st_mtime_ns, after.st_ctime_ns), 'held file stable')
    data = b''.join(chunks); need(len(data) == before.st_size, 'whole buffer')
    return data

def read(path):
    safe(path); first = path.lstat(); need(stat.S_ISREG(first.st_mode), 'ordinary file')
    fd = os.open(path, os.O_RDONLY | NOFOLLOW)
    try:
        need(identity(first) == identity(os.fstat(fd)), 'held/path identity')
        data = held(fd); need(identity(path.lstat()) == identity(os.fstat(fd)), 'path still held file')
        return data
    finally: os.close(fd)

def bound(row):
    data = read(Path(row['path'])); need(pin(data) == {key: row[key] for key in ['bytes', 'SHA256']}, 'whole bound input')
    return data

def contract():
    raw = read(N / 'INSTALL_PLAN.json'); need(pin(raw)['SHA256'] == PLAN_SHA, 'exact current plan')
    plan = json.loads(raw); initial = json.loads(bound(plan['initial']))
    need(plan['website_root'] == str(W), 'exact website root')
    need(len(plan['targets']) == 19 and len({row['path'] for row in plan['targets']}) == 19, 'exact19 unique paths')
    need(set(plan['install_order']) == {row['path'] for row in plan['targets']} and len(plan['install_order']) == 19, 'finite install order')
    for row in plan['targets']:
        path = Path(row['path']); need(not path.is_absolute() and '..' not in path.parts and path.as_posix() == row['path'], 'safe exact target')
    bound(initial['stage_FINAL']); bound(initial['stage_owned_manifest'])
    adoption = json.loads(bound(initial['root_private_adoption']))
    need(adoption['private_stage_root_adopted'] is True and adoption['production_install_authority'] is False, 'private adoption is not installation authority')
    base = json.loads(bound(initial['baseline']))
    buffers = {}
    for row in plan['targets']:
        data = read(Path(row['source'])); need(pin(data) == {key: row[key] for key in ['bytes', 'SHA256']}, 'exact adopted candidate target')
        buffers[row['path']] = data
    return plan, initial, base, buffers

def authorization(plan, initial, required=False):
    path = Path(plan['root_authorization_path'])
    if not path.exists():
        need(not required, 'separate root install authorization absent')
        return None
    raw = read(path); value = json.loads(raw)
    need(value['schema'] == 'three-research-install-authorization-v1' and value['status'] == 'ROOT_AUTHORIZED_EXACT19PATH_FILESYSTEM_INSTALL', 'exact separate root authorization')
    for key, expected in [('root_private_adoption', initial['root_private_adoption']), ('release_initial', plan['initial']), ('install_plan', {'path': str(N / 'INSTALL_PLAN.json'), **pin(read(N / 'INSTALL_PLAN.json'))}), ('installer', {'path': str(N / 'install_three.py'), **pin(read(N / 'install_three.py'))})]:
        need(value[key] == expected, 'authorization binds ' + key); bound(value[key])
    need(value['filesystem_install_authorized'] is True, 'explicit filesystem install authority')
    for key in ['Git_mutation_authorized', 'deployment_authorized', 'Sheet_mutation_authorized', 'browser_or_network_authorized']:
        need(value[key] is False, 'no inferred authority: ' + key)
    need(value['canonical_url'] is None and value['AA'] is None and value['follow_up'] is None, 'no live/tracker assignment')
    return raw

def public_state():
    files, directories = {}, []
    def visit(directory):
        safe(directory); before = directory.lstat(); need(stat.S_ISDIR(before.st_mode), 'ordinary directory')
        for path in sorted(directory.iterdir()):
            relative = path.relative_to(W / 'public').as_posix(); kind = path.lstat().st_mode
            if stat.S_ISDIR(kind): directories.append(relative); visit(path)
            elif stat.S_ISREG(kind): files[relative] = pin(read(path))
            else: raise ValueError('special public entry')
        after = directory.lstat(); need((before.st_ino, before.st_mtime_ns, before.st_ctime_ns) == (after.st_ino, after.st_mtime_ns, after.st_ctime_ns), 'stable enumeration')
    visit(W / 'public'); return files, sorted(directories)

def fence(plan, initial, base, buffers, installed=False):
    files, directories = public_state()
    expected = {row['path']: {key: row[key] for key in ['bytes', 'SHA256']} for row in base['public_files']}
    if installed:
        expected.update({name[7:]: pin(data) for name, data in buffers.items() if name.startswith('public/')})
    need(files == expected and len(files) == (647 if installed else 631), 'entire phase-appropriate public namespace/buffers')
    expected_dirs = sorted(set(base['public_directories']) | ({name[7:] for name in plan['new_directories']} if installed else set()))
    need(directories == expected_dirs, 'entire phase-appropriate directory namespace')
    protected_modes = [[row['path'], mode(W / 'public' / row['path'])] for row in base['public_files'] if 'public/' + row['path'] not in initial['three_old_targets']]
    directory_modes = [[rel, mode(W / 'public' / rel)] for rel in ['.', *base['public_directories']]]
    need(digest(protected_modes) == initial['protected_public_file_mode_digest'] and digest(directory_modes) == initial['existing_public_directory_mode_digest'], 'all protected public file/directory modes')
    for row in base['site_and_Git_controls']:
        name = row['relative_path']; data = read(Path(row['path']))
        expected_pin = pin(buffers['firebase.json']) if installed and name == 'firebase.json' else {key: row[key] for key in ['bytes', 'SHA256']}
        need(pin(data) == expected_pin and mode(W / name) == initial['control_modes'][name], 'all original controls/refs and modes')
    need(read(W / '.git/index') == bound(initial['raw_native_index_by_reference']) and mode(W / '.git/index') == 0o600, 'entire58571 native entries/index5f9c0600 unchanged')
    need(not os.path.lexists(W / '.git/index.lock'), 'no current native index lock')
    for row in plan['targets']:
        path = W / row['path']
        if installed: need(pin(read(path)) == pin(buffers[row['path']]) and mode(path) == row['mode'], 'all19 installed target bytes/modes')
        elif row['kind'] == 'new': need(not os.path.lexists(path), 'all16 new leaves absent')
        else:
            old = initial['three_old_targets'][row['path']]; info = path.lstat()
            need(pin(read(path)) == {key: old[key] for key in ['bytes', 'SHA256']} and mode(path) == old['mode'], 'three exact old replacements')
            need([info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns, info.st_ctime_ns] == [old[key] for key in ['device', 'inode', 'size', 'mtime_ns', 'ctime_ns']], 'three old target identities/timestamps')
    if installed:
        for name in plan['new_directories']: need(mode(W / name) == 0o755, 'three new directory modes')
    index = read(W / 'public/research/index.html')
    collection = json.loads(re.search(rb'<script type="application/ld\+json">(.*?)</script>', index, re.S).group(1))
    counts = [len(files), collection['mainEntity']['numberOfItems'], len(ET.fromstring(read(W / 'public/research/sitemap.xml')))]
    need(counts == ([647, 99, 100] if installed else [631, 96, 97]), 'phase counts')
    need(W.stat().st_dev == N.stat().st_dev == initial['observed_device'], 'same filesystem required')
    return counts

def install(plan, initial, base, buffers, auth_raw):
    need(sys.platform == 'darwin', 'Darwin exclusive rename implementation required')
    libc = ctypes.CDLL('/usr/lib/libSystem.B.dylib', use_errno=True)
    rename = libc.renameatx_np
    rename.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_uint]; rename.restype = ctypes.c_int
    # Local SDK sys/stdio.h defines RENAME_EXCL=0x00000004.
    def move(src_fd, src, dst_fd, dst):
        if rename(src_fd, os.fsencode(src), dst_fd, os.fsencode(dst), 4):
            error = ctypes.get_errno(); raise OSError(error, os.strerror(error))
        os.fsync(src_fd); os.fsync(dst_fd)
    transactions = N / 'transactions'; safe(N)
    if not transactions.exists(): transactions.mkdir(mode=0o700)
    safe(transactions)
    transaction = transactions / hashlib.sha256(auth_raw).hexdigest(); transaction.mkdir(mode=0o700)
    staged = transaction / 'staged'; backups = transaction / 'backups'; staged.mkdir(mode=0o700); backups.mkdir(mode=0o700)
    journal = (transaction / 'journal.jsonl').open('xb')
    def event(value):
        journal.write((json.dumps({'UTC': utc(), **value}, sort_keys=True) + '\n').encode()); journal.flush(); os.fsync(journal.fileno())
    root_fd = os.open(W, os.O_RDONLY | DIRECTORY | NOFOLLOW)
    staged_fd = os.open(staged, os.O_RDONLY | DIRECTORY | NOFOLLOW); backup_fd = os.open(backups, os.O_RDONLY | DIRECTORY | NOFOLLOW)
    descriptors = []; published = {}; original_fds = {}; moved_backups = {}; made_dirs = {}
    def recheck(fds, relative):
        need(identity(W.lstat()) == identity(os.fstat(root_fd)), 'live W root immediately before mutation')
        for index, part in enumerate(Path(relative).parts[:-1]):
            need(identity(os.stat(part, dir_fd=fds[index], follow_symlinks=False)) == identity(os.fstat(fds[index + 1])), 'live ancestor immediately before mutation')
    def parents(relative, create=False):
        fds = [os.dup(root_fd)]; chain = []
        try:
            need(identity(W.lstat()) == identity(os.fstat(root_fd)), 'live W root identity')
            for part in Path(relative).parts[:-1]:
                chain.append(part); parent_name = '/'.join(chain)
                if create and parent_name in plan['new_directories'] and parent_name not in made_dirs:
                    need(not os.path.lexists(W / parent_name), 'do not adopt a concurrently created article directory')
                    event({'intent': 'mkdir', 'path': parent_name}); os.mkdir(part, 0o755, dir_fd=fds[-1]); os.fsync(fds[-1])
                    child = os.open(part, os.O_RDONLY | DIRECTORY | NOFOLLOW, dir_fd=fds[-1]); os.fchmod(child, 0o755); os.fsync(child)
                    made_dirs[parent_name] = identity(os.fstat(child))
                    event({'complete': 'mkdir', 'path': parent_name})
                else: child = os.open(part, os.O_RDONLY | DIRECTORY | NOFOLLOW, dir_fd=fds[-1])
                need(identity(os.stat(part, dir_fd=fds[-1], follow_symlinks=False)) == identity(os.fstat(child)), 'live ancestor identity')
                if parent_name in made_dirs: need(identity(os.fstat(child)) == made_dirs[parent_name], 'same created article directory')
                fds.append(child)
            return fds
        except BaseException:
            for fd in reversed(fds): os.close(fd)
            raise
    try:
        event({'status': 'AUTHORIZED_PREFLIGHT_COMPLETE', 'authorization_SHA256': hashlib.sha256(auth_raw).hexdigest(), 'targets': plan['install_order']})
        rows = {row['path']: row for row in plan['targets']}
        for number, relative in enumerate(plan['install_order']):
            row = rows[relative]; temporary = str(number)
            fd = os.open(temporary, os.O_RDWR | os.O_CREAT | os.O_EXCL | NOFOLLOW, row['mode'], dir_fd=staged_fd); descriptors.append(fd)
            data = buffers[relative]; offset = 0
            while offset < len(data):
                written = os.write(fd, data[offset:]); need(written > 0, 'nonzero temporary write'); offset += written
            os.fchmod(fd, row['mode']); os.fsync(fd); need(held(fd) == data, 'complete owned temporary buffer')
            fds = parents(relative, create=True); parent_fd = fds[-1]; leaf = Path(relative).name
            try:
                need(identity(os.stat(temporary, dir_fd=staged_fd, follow_symlinks=False)) == identity(os.fstat(fd)), 'held prepared source identity')
                if row['kind'] == 'replacement':
                    old_fd = os.open(leaf, os.O_RDONLY | NOFOLLOW, dir_fd=parent_fd); descriptors.append(old_fd); original_fds[relative] = old_fd
                    old = initial['three_old_targets'][relative]
                    need(pin(held(old_fd)) == {key: old[key] for key in ['bytes', 'SHA256']} and identity(os.fstat(old_fd)) == [old['device'], old['inode']], 'held original before move')
                    need(stat.S_IMODE(os.fstat(old_fd).st_mode) == old['mode'], 'original mode before move')
                    need(identity(os.stat(leaf, dir_fd=parent_fd, follow_symlinks=False)) == identity(os.fstat(old_fd)), 'live original before parking')
                    recheck(fds, relative)
                    event({'intent': 'park_original', 'path': relative, 'backup': temporary})
                    move(parent_fd, leaf, backup_fd, temporary)
                    need(identity(os.stat(temporary, dir_fd=backup_fd, follow_symlinks=False)) == identity(os.fstat(old_fd)), 'parked original is held original')
                    need(pin(read(backups / temporary)) == {key: old[key] for key in ['bytes', 'SHA256']}, 'whole parked original')
                    moved_backups[relative] = temporary; event({'complete': 'park_original', 'path': relative, 'backup': temporary})
                recheck(fds, relative)
                event({'intent': 'publish_exclusive', 'path': relative, 'prepared': temporary})
                move(staged_fd, temporary, parent_fd, leaf)
                need(identity(os.stat(leaf, dir_fd=parent_fd, follow_symlinks=False)) == identity(os.fstat(fd)) and held(fd) == data, 'published source identity/buffer')
                published[relative] = identity(os.fstat(fd)); event({'complete': 'publish_exclusive', 'path': relative})
            finally:
                for directory_fd in reversed(fds): os.close(directory_fd)
        counts = fence(plan, initial, base, buffers, installed=True)
        for relative, expected in published.items(): need(identity((W / relative).lstat()) == expected, 'all19 final published identities')
        for relative, name in moved_backups.items():
            old = initial['three_old_targets'][relative]
            need(identity((backups / name).lstat()) == identity(os.fstat(original_fds[relative])), 'all3 backup identities')
            need(pin(read(backups / name)) == {key: old[key] for key in ['bytes', 'SHA256']} and mode(backups / name) == old['mode'], 'all3 final backup buffers/modes')
        need(len(moved_backups) == 3 and not list(staged.iterdir()) and len(list(backups.iterdir())) == 3, 'no unresolved temporary/moved entries')
        event({'status': 'FILESYSTEM_INSTALL_VERIFIED_SNAPSHOT', 'counts': counts, 'native_index_entries_unchanged': 58571})
        return {'status': 'FILESYSTEM_INSTALL_VERIFIED_SNAPSHOT', 'transaction': str(transaction), 'counts': counts, 'native_index_entries_unchanged': 58571, 'Git_deploy_Sheet_actions': False}
    except BaseException as error:
        event({'status': 'STOPPED_PARTIAL_OR_UNCERTAIN_STATE_PRESERVED', 'error': repr(error), 'completed_targets': list(published), 'known_backups': moved_backups, 'automatic_rollback': False})
        raise
    finally:
        for fd in descriptors: os.close(fd)
        for fd in [root_fd, staged_fd, backup_fd]: os.close(fd)
        journal.close()

def main():
    need(sys.argv[1:] in [[], ['--install'], ['--verify-installed']], 'finite explicit modes')
    plan, initial, base, buffers = contract()
    installed = sys.argv[1:] == ['--verify-installed']
    counts = fence(plan, initial, base, buffers, installed=installed)
    if sys.argv[1:] == ['--install']:
        raw = authorization(plan, initial, required=True)
        print(json.dumps(install(plan, initial, base, buffers, raw), sort_keys=True))
    else:
        authorized = authorization(plan, initial) is not None
        print(json.dumps({'status': 'POSTINSTALL_READONLY_VERIFIED' if installed else 'READONLY_PLAN_PREFLIGHT_PASS', 'counts': counts, 'target_paths': 19, 'new_leaves': 16, 'replacements': 3, 'current_native_entries_unchanged': 58571, 'future_root_staging_entries': 58587, 'future_protected_original_raw_records': 58568, 'separate_root_install_authorization_present': authorized, 'writes': 0, 'Git_network_deploy_Sheet_browser_actions': False}, sort_keys=True))

if __name__ == '__main__': main()
