#!/usr/bin/env python3
"""Self-only review-family custody, with fifteen exact external science inputs."""
import hashlib
import json
from pathlib import Path
import stat

ROOT = Path(__file__).resolve().parent

def digest(body):
    return hashlib.sha256(body).hexdigest()

def duplicate_free_pairs(items):
    out = {}
    for key,value in items:
        if key in out:
            raise ValueError('duplicate JSON key: '+key)
        out[key] = value
    return out

def load(path):
    return json.loads(path.read_text(), object_pairs_hook=duplicate_free_pairs,
                      parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)))

def identity(path):
    st = path.lstat()
    if not stat.S_ISREG(st.st_mode):
        raise ValueError('regular file required: '+str(path))
    body = path.read_bytes()
    return {'bytes':len(body),'sha256':digest(body),
            'full_mode':format(stat.S_IMODE(st.st_mode),'04o')}

def external_check():
    value = load(ROOT/'EXTERNAL_BINDINGS.json')
    if value['schema'] != 'pr51-modular-geometry-exact-source-bindings/v1':
        raise ValueError('external schema')
    if type(value['science_file_count']) is not int or value['science_file_count'] != 15:
        raise ValueError('external count')
    if len(value['files']) != 15 or len({r['path'] for r in value['files']}) != 15:
        raise ValueError('external membership')
    total = 0
    for row in value['files']:
        if set(row) != {'path','bytes','sha256','full_mode'} or type(row['bytes']) is not int:
            raise ValueError('external row shape')
        if identity(Path(row['path'])) != {k:row[k] for k in ('bytes','sha256','full_mode')}:
            raise ValueError('external bytes/mode changed: '+row['path'])
        total += row['bytes']
    if total != value['science_total_bytes'] or total != 53495:
        raise ValueError('external total')
    return value

def members():
    files = []
    directories = [ROOT]
    for p in sorted(ROOT.rglob('*')):
        st = p.lstat()
        if stat.S_ISREG(st.st_mode):
            files.append(p)
        elif stat.S_ISDIR(st.st_mode):
            directories.append(p)
        else:
            raise ValueError('nonregular member: '+str(p))
    return files,directories

def verify(expected_manifest_sha256):
    mf = ROOT/'SELF_MANIFEST.json'
    if identity(mf)['sha256'] != expected_manifest_sha256:
        raise ValueError('manifest digest')
    value = load(mf)
    if value['schema'] != 'pr51-modular-geometry-adversary-self-only-closure/v1':
        raise ValueError('manifest schema')
    files,dirs = members()
    payload = [p for p in files if p != mf]
    if sorted(str(p.relative_to(ROOT)) for p in payload) != sorted(r['path'] for r in value['files']):
        raise ValueError('file membership')
    if type(value['payload_file_count']) is not int or type(value['self_excluded_count']) is not int:
        raise ValueError('count types')
    if len(payload) != value['payload_file_count'] or value['self_excluded_count'] != 1:
        raise ValueError('file count')
    for row in value['files']:
        if set(row) != {'path','bytes','sha256','full_mode'} or type(row['bytes']) is not int:
            raise ValueError('file row shape')
        if identity(ROOT/row['path']) != {k:row[k] for k in ('bytes','sha256','full_mode')}:
            raise ValueError('file bytes/mode changed: '+row['path'])
        if row['full_mode'] != '0444':
            raise ValueError('payload mode')
    actual_dirs = sorted('.' if p == ROOT else str(p.relative_to(ROOT)) for p in dirs)
    if actual_dirs != sorted(r['path'] for r in value['directories']):
        raise ValueError('directory membership')
    if any(set(r) != {'path','full_mode'} or r['full_mode'] != '0555' for r in value['directories']):
        raise ValueError('directory row shape/mode')
    for p in dirs:
        if stat.S_IMODE(p.lstat().st_mode) != 0o555:
            raise ValueError('directory mode')
    if identity(mf)['full_mode'] != '0444':
        raise ValueError('manifest mode')
    external_check()
    return {'schema':value['schema'],'manifest_sha256':expected_manifest_sha256,
            'payload_file_count':len(payload),'manifest_self_excluded_count':1,
            'directory_count_including_root':len(dirs),'external_science_files':15,
            'status':'PASS_SELF_ONLY_CLOSURE_NO_ACCEPTANCE_AUTHORITY'}
