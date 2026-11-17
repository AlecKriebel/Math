"""Passive final whole-source guard. No archived content is interpreted or run."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import stat

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
SRC = P / 'papers/23202994/sources'
OWN = P / 'papers/23202994/reviews/scope-sol'
before = json.loads((OWN / 'SOURCE_GUARDS_BEFORE.json').read_bytes())
started = datetime.datetime.now(datetime.timezone.utc).isoformat()
files, directories = {}, {}
stack = [SRC]
while stack:
    root = stack.pop()
    initial = root.lstat()
    assert stat.S_ISDIR(initial.st_mode) and not root.is_symlink()
    for path in sorted(root.iterdir()):
        rel = path.relative_to(SRC).as_posix()
        info = path.lstat()
        if stat.S_ISDIR(info.st_mode):
            assert not path.is_symlink()
            directories[rel] = format(stat.S_IMODE(info.st_mode), '04o')
            stack.append(path)
        else:
            assert stat.S_ISREG(info.st_mode) and not path.is_symlink()
            descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
            try:
                opened = os.fstat(descriptor)
                assert (opened.st_dev, opened.st_ino) == (info.st_dev, info.st_ino)
                blocks = []
                while True:
                    block = os.read(descriptor, 1048576)
                    if not block:
                        break
                    blocks.append(block)
                final = os.fstat(descriptor)
                assert (opened.st_dev, opened.st_ino, opened.st_size, opened.st_mtime_ns, opened.st_ctime_ns, opened.st_mode) == (final.st_dev, final.st_ino, final.st_size, final.st_mtime_ns, final.st_ctime_ns, final.st_mode)
                assert (path.lstat().st_dev, path.lstat().st_ino) == (final.st_dev, final.st_ino)
                raw = b''.join(blocks)
                assert len(raw) == final.st_size
                files[rel] = {'bytes': len(raw), 'SHA256': hashlib.sha256(raw).hexdigest(), 'mode': format(stat.S_IMODE(final.st_mode), '04o')}
            finally:
                os.close(descriptor)
    final_root = root.lstat()
    assert (initial.st_dev, initial.st_ino, initial.st_mode, initial.st_mtime_ns, initial.st_ctime_ns) == (final_root.st_dev, final_root.st_ino, final_root.st_mode, final_root.st_mtime_ns, final_root.st_ctime_ns)
assert files == before['files'] and directories == before['directories']
assert format(stat.S_IMODE(SRC.lstat().st_mode), '04o') == before['root_mode']
result = {'schema': 'source-first-passive-final-custody39-v1', 'started_UTC': started, 'completed_UTC': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'root': str(SRC), 'root_mode': before['root_mode'], 'files': files, 'directories': directories, 'regular_files': len(files), 'child_directories': len(directories), 'all_source_bytes_modes_hidden_empty_topology_exact_before_after': True, 'archive_whole_pins_unchanged_from_secure_census': True, 'source_changes': False, 'scientific_code_attempts': 0, 'network_requests': 0}
with (OWN / 'SOURCE_GUARDS_AFTER.json').open('x') as stream:
    json.dump(result, stream, indent=2)
    stream.write('\n')
print(json.dumps({'schema': result['schema'], 'files': len(files), 'child_directories': len(directories), 'whole_before_after_equal': True}))
