"""Shared explicit guards. Standard library; no removable assertions."""
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
import zipfile

sys.dont_write_bytecode = True
ROOT = Path(__file__).absolute().parent.parent

def require(ok, message):
    if not ok:
        raise ValueError(message)

def no_links(path):
    # Inspect the original lexical prefixes before abspath can erase a
    # symlink followed by "..". Ordinary safe sibling "../" paths remain
    # valid. No component is dereferenced through a symlink in this check.
    raw = Path(path)
    if not raw.is_absolute():
        raw = Path.cwd() / raw
    parts = raw.parts
    node = Path(raw.anchor)
    for index, part in enumerate(parts[1:], start=1):
        node = node / part
        if node.is_symlink():
            raise ValueError('symlink component: ' + str(node))
        if index < len(parts) - 1 and node.exists():
            require(node.is_dir(), 'ancestor is not a directory: ' + str(node))
    return Path(os.path.abspath(raw))

def regular(path):
    path = no_links(path)
    require(path.exists() and stat.S_ISREG(path.stat().st_mode), 'not a regular file: ' + str(path))
    return path

def record(path, name=None):
    path = regular(path)
    data = path.read_bytes()
    return {'path': name if name is not None else path.name, 'bytes': len(data),
            'sha256': hashlib.sha256(data).hexdigest()}

def member(name):
    require(isinstance(name, str), 'member path must be text')
    p = Path(name)
    require(name and not p.is_absolute() and p.as_posix() == name and
            all(part not in ('', '.', '..') for part in name.split('/')),
            'unsafe member path: ' + repr(name))
    return regular(ROOT / p)

def load_json(path):
    return json.loads(regular(path).read_text(encoding='utf-8'))

def inventory():
    no_links(ROOT)
    result = []
    for base, dirs, files in os.walk(ROOT, followlinks=False):
        for name in dirs:
            p = no_links(Path(base) / name)
            require(p.is_dir(), 'invalid input directory')
        for name in files:
            result.append(regular(Path(base) / name))
    return sorted(result)

def verify_payload():
    # Preflight the manifest and every member before parsing the self-excluded
    # bootstrap manifest, as well as before hashing payload bytes.
    files = inventory()
    manifest = ROOT / 'MANIFEST.json'
    regular(manifest)
    data = load_json(manifest)
    require(set(data) == {'schema', 'hash_scope', 'records'}, 'manifest keys')
    require(data['schema'] == 1 and isinstance(data['records'], list), 'manifest schema')
    names = [r['path'] for r in data['records']]
    require(len(names) == len(set(names)), 'duplicate manifest paths')
    require('MANIFEST.json' not in names, 'manifest cannot hash itself')
    require(set(names) == {p.relative_to(ROOT).as_posix() for p in files if p != manifest},
            'manifest inventory differs from regular input inventory')
    for r in data['records']:
        require(set(r) == {'path', 'bytes', 'sha256'}, 'manifest record keys')
        require(record(member(r['path']), r['path']) == r, 'payload mismatch: ' + r['path'])
    metadata=load_json(ROOT/'.zenodo.json')
    require(load_json(ROOT/'metadata.json')==metadata, 'bare metadata mismatch')
    require(load_json(ROOT/'metadata_api.json')=={'metadata':metadata}, 'API metadata mismatch')
    custody=load_json(ROOT/'CUSTODY_MAP.json')
    origins=[r['original_path'] for r in custody['copies']]+[r['path'] for r in custody['exclusions']]
    require(len(origins)==len(set(origins))==custody['exact_partition_count'], 'custody partition')
    for row in custody['copies']:
        require(record(member(row['copy_path']),row['original_path'])==
                {'path':row['original_path'],'bytes':row['bytes'],'sha256':row['sha256']},'historical copy changed')
    return data

def fresh_output(path, directory=False):
    """Preflight without writing; existing files of any inode are rejected.

    Reject all lexical/ancestor symlinks before resolving. Refuse outputs in,
    or ancestors of, kit inputs. Existing hardlink aliases are rejected by the
    same no-existing-output contract, including external delivery files.
    """
    p = no_links(path)
    require(not p.exists(), 'output must be absent: ' + str(p))
    r = no_links(ROOT)
    require(p != r and r not in p.parents and p not in r.parents,
            'output overlaps protected kit: ' + str(p))
    # A case-insensitive filesystem can give the same protected directory
    # a differently cased lexical name. Compare physical identity for EVERY
    # existing output ancestor, including ancestors above absent components.
    # This is a static preflight, not a concurrent-filesystem security claim.
    root_stat = r.stat()
    root_identity = (root_stat.st_dev, root_stat.st_ino)
    for parent in p.parents:
        if parent.exists():
            require(parent.is_dir(), 'output ancestor is not a directory')
            parent_stat = parent.stat()
            require((parent_stat.st_dev, parent_stat.st_ino) != root_identity,
                    'output physically overlaps protected kit: ' + str(p))
    return p

def create_output_dir(path):
    p = fresh_output(path, True)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.mkdir(exist_ok=False)
    return p

def write_new(path, data):
    p = fresh_output(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('xb') as stream:
        stream.write(data)

def json_bytes(value):
    return (json.dumps(value, indent=2, sort_keys=True) + '\n').encode()

def binding_check(path=None, required=False):
    default = ROOT.parent / 'DEPOSIT_BINDING.json'
    selected = Path(path) if path is not None else default
    no_links(selected)
    if not selected.exists():
        require(not required and path is None, 'required or explicit binding is absent')
        return {'status': 'ABSENT_ALLOWED', 'strict': False}
    binding = load_json(selected)
    require(set(binding) == {'schema', 'metadata', 'files'}, 'binding keys')
    require(binding['schema'] == 1, 'binding schema')
    metadata = load_json(ROOT / '.zenodo.json')
    require(binding['metadata'] == metadata, 'binding metadata mismatch')
    require(len(binding['files']) == 2, 'binding must select paper and support ZIP')
    folder = regular(selected).parent
    expected = {'paper.pdf', 'pr1094_supportkit_v1.0.zip'}
    require({r['path'] for r in binding['files']} == expected, 'binding asset names')
    for row in binding['files']:
        require(record(folder / row['path'], row['path']) == row, 'binding asset mismatch')
    require((folder/'paper.pdf').read_bytes()==(ROOT/'paper.pdf').read_bytes(),'delivery PDF differs from kit')
    manifest=verify_payload()
    expected_names=sorted(['MANIFEST.json']+[r['path'] for r in manifest['records']])
    with zipfile.ZipFile(folder/'pr1094_supportkit_v1.0.zip') as archive:
        require(archive.namelist()==expected_names,'archive sorted inventory')
        require(archive.testzip() is None,'archive CRC failure')
        for info in archive.infolist():
            require(info.date_time==(1980,1,1,0,0,0) and info.compress_type==zipfile.ZIP_STORED
                    and info.create_system==3 and info.external_attr==0o100644<<16,
                    'archive header differs')
            require(archive.read(info.filename)==member(info.filename).read_bytes(),'archive member differs')
    uploader=folder/'zenodo-deposit.json'
    require(load_json(uploader)=={'metadata':metadata,'files':[
        {'path':'paper.pdf','name':'paper.pdf'},
        {'path':'pr1094_supportkit_v1.0.zip','name':'pr1094_supportkit_v1.0.zip'}]},'native uploader differs')
    return {'status': 'PRESENT_VERIFIED', 'strict': True, 'files': 2}
