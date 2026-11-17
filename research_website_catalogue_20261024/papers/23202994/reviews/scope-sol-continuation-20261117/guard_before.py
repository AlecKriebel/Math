"""Passive full-source and immutable-INITIAL guard, no scientific code execution."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import stat

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
OWN = P / 'papers/23202994/reviews/scope-sol-continuation-20261117'
INITIAL = P / 'papers/23202994/reviews/scope-sol'
SOURCE = P / 'papers/23202994/sources'

def row(path):
    first = path.lstat()
    assert stat.S_ISREG(first.st_mode) and not path.is_symlink()
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    try:
        opened = os.fstat(fd)
        assert (opened.st_dev, opened.st_ino) == (first.st_dev, first.st_ino)
        chunks = []
        while True:
            chunk = os.read(fd, 1048576)
            if not chunk:
                break
            chunks.append(chunk)
        last = os.fstat(fd)
        assert (opened.st_dev, opened.st_ino, opened.st_size, opened.st_mode, opened.st_mtime_ns, opened.st_ctime_ns) == (last.st_dev, last.st_ino, last.st_size, last.st_mode, last.st_mtime_ns, last.st_ctime_ns)
        assert (path.lstat().st_dev, path.lstat().st_ino) == (last.st_dev, last.st_ino)
        raw = b''.join(chunks)
        assert len(raw) == last.st_size
        return {'bytes': len(raw), 'SHA256': hashlib.sha256(raw).hexdigest(), 'mode': format(stat.S_IMODE(last.st_mode), '04o')}
    finally:
        os.close(fd)

def census(root):
    files, directories = {}, {}
    stack = [root]
    while stack:
        here = stack.pop()
        first = here.lstat()
        assert stat.S_ISDIR(first.st_mode) and not here.is_symlink()
        for path in sorted(here.iterdir()):
            rel = path.relative_to(root).as_posix()
            info = path.lstat()
            if stat.S_ISDIR(info.st_mode):
                assert not path.is_symlink()
                directories[rel] = format(stat.S_IMODE(info.st_mode), '04o')
                stack.append(path)
            else:
                files[rel] = row(path)
        last = here.lstat()
        assert (first.st_dev, first.st_ino, first.st_mode, first.st_mtime_ns, first.st_ctime_ns) == (last.st_dev, last.st_ino, last.st_mode, last.st_mtime_ns, last.st_ctime_ns)
    return {'root': str(root), 'root_mode': format(stat.S_IMODE(root.lstat().st_mode), '04o'), 'files': files, 'directories': directories}

source = census(SOURCE)
initial = census(INITIAL)
assert (len(source['files']), len(source['directories'])) == (39, 15)
assert (len(initial['files']), len(initial['directories'])) == (38, 3)
assert initial['files']['INITIAL_SEAL.json']['SHA256'] == '97207fb4f5930c4813e7ba34db85cfca3fc40aee4aad8cf4818398b9dffafa98'
assert initial['files']['INITIAL_MANIFEST.json']['SHA256'] == '0cebbd6721d77149f1137b557da066c829468a028ac1ee391a3c97730e794381'
manifest = json.loads((INITIAL / 'INITIAL_MANIFEST.json').read_bytes())
assert manifest['owned_root'] == str(INITIAL)
assert {r['path'] for r in manifest['files']} == set(initial['files'])
assert {r['path']: r['mode'] for r in manifest['directories']} == initial['directories']
for item in manifest['files']:
    if item.get('terminal_control'):
        assert item['path'] in {'INITIAL_MANIFEST.json', 'INITIAL_SEAL.json'}
    else:
        assert initial['files'][item['path']] == {k: item[k] for k in ('bytes', 'SHA256', 'mode')}
original_source = json.loads((INITIAL / 'SOURCE_GUARDS_AFTER.json').read_bytes())
assert source['files'] == original_source['files'] and source['directories'] == original_source['directories'] and source['root_mode'] == original_source['root_mode']
result = {'schema': 'row190-continuation-full-before-guards-v1', 'UTC': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'source': source, 'immutable_INITIAL': initial, 'source_and_INITIAL_exact': True, 'scientific_code_execution': False}
with (OWN / 'GUARDS_BEFORE.json').open('x') as stream:
    json.dump(result, stream, indent=2)
    stream.write('\n')
print(json.dumps({'source_files_dirs': [39, 15], 'INITIAL_files_dirs': [38, 3], 'all_pins_exact': True}))
