"""Passive original-first custody reader; no archived code or source is executed."""
import datetime
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import stat
import zipfile

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
SRC = P / 'papers/23202994/sources'
OWN = P / 'papers/23202994/reviews/scope-sol'

def stamp():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def whole(path):
    before = path.lstat()
    assert stat.S_ISREG(before.st_mode) and not path.is_symlink()
    descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    try:
        opened = os.fstat(descriptor)
        assert (opened.st_dev, opened.st_ino) == (before.st_dev, before.st_ino)
        parts = []
        while True:
            block = os.read(descriptor, 1048576)
            if not block:
                break
            parts.append(block)
        after = os.fstat(descriptor)
        assert (opened.st_dev, opened.st_ino, opened.st_size, opened.st_mtime_ns, opened.st_ctime_ns, opened.st_mode) == (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns, after.st_ctime_ns, after.st_mode)
        assert (path.lstat().st_dev, path.lstat().st_ino) == (after.st_dev, after.st_ino)
        raw = b''.join(parts)
        assert len(raw) == after.st_size
        return raw
    finally:
        os.close(descriptor)

def pin(path):
    raw = whole(path)
    return {'bytes': len(raw), 'SHA256': hashlib.sha256(raw).hexdigest(), 'mode': format(stat.S_IMODE(path.lstat().st_mode), '04o')}

started = stamp()
files, directories = {}, {}
stack = [SRC]
while stack:
    root = stack.pop()
    before = root.lstat()
    assert stat.S_ISDIR(before.st_mode) and not root.is_symlink()
    for path in sorted(root.iterdir()):
        rel = path.relative_to(SRC).as_posix()
        info = path.lstat()
        if stat.S_ISDIR(info.st_mode):
            assert not path.is_symlink()
            directories[rel] = format(stat.S_IMODE(info.st_mode), '04o')
            stack.append(path)
        else:
            files[rel] = pin(path)
    after = root.lstat()
    assert (before.st_dev, before.st_ino, before.st_mode, before.st_mtime_ns, before.st_ctime_ns) == (after.st_dev, after.st_ino, after.st_mode, after.st_mtime_ns, after.st_ctime_ns)
assert (len(files), len(directories)) == (39, 15)
adoption_path = P / 'verification/root-source190191-custody-adoption-20261117.json'
assert pin(adoption_path)['SHA256'] == '9ab699b60b7ac0a9be04db1211f144ccb6db852b573a71a18aa37bb2a4fa707b'
assert files['SOURCE_MANIFEST.json']['SHA256'] == '7a6854f7ebb1caf7a0f26c5cb6014872ee0ce93f03414c3f48d965ff13c9a976'
assert files['SOURCE_FINAL.json']['SHA256'] == 'd90fbadc2f49aa86904695ce60c2042eef4e6850f70d3972b5f48fdb8913c27e'
assert files['zenodo-files/paper.pdf']['bytes'] == 87127 and files['zenodo-files/paper.pdf']['SHA256'] == 'b9e7c887787b911b55f012cc640621fedc282dd71e8c57fa01c1f9db49612d9d'
archives = []
for rel in sorted(name for name in files if name.lower().endswith('.zip')):
    rows, seen = [], set()
    with zipfile.ZipFile(SRC / rel) as archive:
        for item in archive.infolist():
            name = item.orig_filename
            path = PurePosixPath(name)
            assert name and '\0' not in name and '\\' not in name and not path.is_absolute() and '..' not in path.parts and ':' not in path.parts[0]
            assert path.as_posix() == name.rstrip('/') and name not in seen
            seen.add(name)
            kind = stat.S_IFMT(item.external_attr >> 16)
            assert kind in (0, stat.S_IFREG, stat.S_IFDIR) and not item.flag_bits & 1
            rows.append({'name': name, 'is_directory': item.is_dir(), 'bytes': item.file_size, 'compressed_bytes': item.compress_size, 'CRC32': format(item.CRC, '08x'), 'external_mode': format((item.external_attr >> 16) & 0xffff, '06o')})
    assert not any(row['name'].lower().endswith('.pdf') for row in rows)
    archives.append({'path': rel, 'pin': files[rel], 'members': rows, 'all_names_safe': True, 'embedded_PDF_members': 0, 'decompressed_or_executed': False})
result = {'schema': 'source-first-passive-custody39-v1', 'started_UTC': started, 'completed_UTC': stamp(), 'root': str(SRC), 'root_mode': format(stat.S_IMODE(SRC.lstat().st_mode), '04o'), 'files': files, 'directories': directories, 'regular_files': len(files), 'child_directories': len(directories), 'root_source_only_adoption': {'path': str(adoption_path), **pin(adoption_path)}, 'semantic_contents_read_by_this_reader': [], 'opaque_hashes_include_forbidden_support_code_opinion_files_without_semantic_exposure': True, 'archives': archives, 'source_changes': False, 'scientific_code_execution': False, 'network_requests': 0}
with (OWN / 'SOURCE_GUARDS_BEFORE.json').open('x') as stream:
    json.dump(result, stream, indent=2)
    stream.write('\n')
print(json.dumps({'schema': result['schema'], 'files': len(files), 'child_directories': len(directories), 'archives': len(archives), 'source_only': True}))
