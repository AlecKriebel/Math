"""Read-only own evidence checks. Never loads candidate/production code."""
from pathlib import Path, PurePosixPath
import hashlib
import json
import os
import re
import stat

F = Path(__file__).absolute().parent
R = F.parents[3]

def need(value, message):
    if not value:
        raise ValueError(message)

def sha(body):
    return hashlib.sha256(body).hexdigest()

def safe(name):
    need(type(name) is str and name and '\\' not in name and '\0' not in name, 'Literal relative path')
    p = PurePosixPath(name)
    need(not p.is_absolute() and p.as_posix() == name and not {'.', '..', '.git', '__pycache__'}.intersection(p.parts), 'Canonical evidence path')
    return name

def raw(path):
    need(path.is_file() and not path.is_symlink() and all(not q.is_symlink() for q in path.parents), 'Regular nonsymlink evidence')
    before = path.stat()
    with path.open('rb') as stream:
        opened = os.fstat(stream.fileno())
        body = stream.read()
        end = os.fstat(stream.fileno())
    after = path.stat()
    identities = [(z.st_dev, z.st_ino, z.st_mode, z.st_size, z.st_mtime_ns, z.st_ctime_ns) for z in [before, opened, end, after]]
    need(all(z == identities[0] for z in identities), 'Evidence changed while read')
    return body

def ref(path):
    body = raw(path)
    return dict(path=safe(path.relative_to(R).as_posix()), bytes=len(body), sha256=sha(body), full_mode=stat.S_IMODE(path.stat().st_mode))

def check(row):
    need(type(row) is dict and set(row) == {'path', 'bytes', 'sha256', 'full_mode'} and type(row['bytes']) is int and row['bytes'] >= 0 and type(row['full_mode']) is int and 0 <= row['full_mode'] <= 0o7777 and type(row['sha256']) is str and re.fullmatch('[0-9a-f]{64}', row['sha256']), 'Typed complete evidence descriptor')
    path = R / safe(row['path'])
    need(ref(path) == row, 'Whole evidence body/fullmode differs')
    return raw(path)

def parse(body):
    def pairs(items):
        result = {}
        for key, value in items:
            need(key not in result, 'Duplicate JSON key')
            result[key] = value
        return result
    return json.loads(body, object_pairs_hook=pairs, parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))

def load(path):
    return parse(raw(path))

def topology(path, names, directories, mode):
    names = sorted(names)
    need(len(names) == len(set(names)), 'Duplicate member')
    want_dirs = {'.'} | {q.as_posix() for name in names for q in PurePosixPath(safe(name)).parents if q.as_posix() != '.'}
    need(set(directories) == want_dirs, 'Full exact directory domain')
    seen_files, seen_dirs = set(), {'.'}
    for item in path.rglob('*'):
        need(not item.is_symlink(), 'Symlink in evidence family')
        relative = item.relative_to(path).as_posix()
        if item.is_file():
            seen_files.add(relative)
            need(stat.S_IMODE(item.stat().st_mode) == mode, 'Exact full evidence member mode')
        elif item.is_dir():
            seen_dirs.add(relative)
        else:
            raise ValueError('Nonregular evidence topology')
    need(seen_files == set(names) and seen_dirs == want_dirs, 'Missing/extra evidence member or empty directory')
    for name in want_dirs:
        q = path / name
        need(not q.is_symlink() and stat.S_IMODE(q.stat().st_mode) == 0o755, 'Nonsymlink full0755 evidence directory')

def check_fixed():
    observation = load(F / 'OBSERVATIONS.json')
    need(observation['schema'] == 'pr48-v6-independent-fixed-source-evidence/v1' and observation['production_executed'] is False, 'Own fixed observation schema')
    rows = observation['direct_fixed_rows']
    need(len(rows) == observation['direct_fixed_rows_count'] and [z['path'] for z in rows] == sorted(set(z['path'] for z in rows)), 'Distinct exact direct evidence rows')
    for row in rows:
        check(row)
    old = parse(check(observation['prior_fixed_ledger']))
    need(old['fixed_rows_count'] == len(old['fixed_rows']) == 295 and len({z['path'] for z in old['fixed_rows']}) == 295, 'Complete in-place historical fixed ledger')
    for row in old['fixed_rows']:
        check(row)
    for family in old['exact_preserved_families']:
        topology(R / safe(family['path']), family['payload_names'], family['directory_names'], family['full_file_mode'])
    outer_dirs = old['additional_genuine_outer_directories'] + [old['additional_genuine_outer_directory']]
    for row in outer_dirs + observation['exact_directory_modes']:
        q = R / safe(row['path'])
        need(q.is_dir() and not q.is_symlink() and all(not a.is_symlink() for a in q.parents) and stat.S_IMODE(q.stat().st_mode) == row['full_mode'], 'Fixed typed directory mode')
    for family in observation['exact_current_families']:
        topology(R / safe(family['path']), family['payload_names'], family['directory_names'], family['full_file_mode'])
    return observation
