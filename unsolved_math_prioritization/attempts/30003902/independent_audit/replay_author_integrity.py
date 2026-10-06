"""Static author-byte authentication only; does not execute author files or prove mathematics."""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):
    raise SystemExit('REJECT: use -I -S -B')
import hashlib, io, json, stat, zipfile
from pathlib import Path

ARCHIVE_SHA256 = '616c01a36dc02a39e1648e293ca8682b5526910956f636194fcb14d6588392e6'
MANIFEST_SHA256 = 'e250178fe2553c8d5243cdab69f10c438fdc21668a07fbdb67ff6ab92ba731cb'
NAMES = {'APPROACHES.md', 'MANIFEST.json', 'README.md', 'RESULT.md', 'SOURCES.json', 'STATUS.json', 'VERIFICATION_METADATA.json'}

def need(condition, message):
    if not condition:
        raise ValueError('REJECT: ' + message)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def read_regular(path):
    info = path.lstat()
    need(stat.S_ISREG(info.st_mode) and info.st_nlink == 1, 'nonregular or hardlinked file: ' + path.name)
    return path.read_bytes()

def inspect(archive_path, manifest_path, root):
    a = read_regular(archive_path)
    need(len(a) == 12203 and digest(a) == ARCHIVE_SHA256, 'archive anchor')
    m = read_regular(manifest_path)
    need(len(m) == 1544 and digest(m) == MANIFEST_SHA256, 'external manifest anchor')
    manifest = json.loads(m)
    entries = manifest['exact_inventory']
    need(len(entries) == 7 and {x['path'] for x in entries} == NAMES, 'manifest inventory')
    expected = {x['path']: (x['bytes'], x['sha256']) for x in entries}
    payload = {}
    with zipfile.ZipFile(io.BytesIO(a)) as z:
        infos = z.infolist()
        need(len(infos) == 7 and {x.filename for x in infos} == NAMES, 'zip inventory')
        need(z.testzip() is None, 'zip CRC')
        for info in infos:
            need(stat.S_ISREG(info.external_attr >> 16), 'zip member not regular')
            need(not (info.flag_bits & 1), 'encrypted zip member')
            need(info.filename == Path(info.filename).name, 'nonflat zip path')
            data = z.read(info)
            need((len(data), digest(data)) == expected[info.filename], 'zip payload mismatch: ' + info.filename)
            payload[info.filename] = data
    for part in (root, *root.parents):
        need(stat.S_ISDIR(part.lstat().st_mode), 'symlink or non-directory ancestry')
    actual = list(root.iterdir())
    need(len(actual) == 7 and {x.name for x in actual} == NAMES, 'directory exact inventory')
    for p in actual:
        need(read_regular(p) == payload[p.name], 'directory/archive mismatch: ' + p.name)
    inner = json.loads(payload['MANIFEST.json'])
    need(len(inner['files']) == 6 and {x['path'] for x in inner['files']} == NAMES-{'MANIFEST.json'}, 'inner manifest inventory')
    for row in inner['files']:
        need((row['bytes'], row['sha256']) == expected[row['path']], 'inner manifest binding')
    need(not any(x.endswith(('.py','.pyc','.so','.sh')) for x in NAMES), 'author executable')
    return {'problem_id': 30003902, 'status': 'PASS', 'archive_bytes': len(a), 'archive_sha256': digest(a), 'external_manifest_bytes': len(m), 'external_manifest_sha256': digest(m), 'exact_regular_files': 7, 'payload_bytes': sum(map(len,payload.values())), 'archive_directory_inner_external_agree': True, 'author_code_executed': False, 'mathematical_proof_certified_by_hashes': False}

if __name__ == '__main__':
    need(len(sys.argv) == 4, 'expected archive, external manifest, and author directory')
    print(json.dumps(inspect(*(Path(x) for x in sys.argv[1:])), sort_keys=True, indent=2))
