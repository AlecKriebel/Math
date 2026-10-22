#!/usr/bin/env python3
"""Manifest custody, source snapshot integrity, and hostile-object controls.
python3 -I -B verify_custody.py --selftest
python3 -I -B verify_custody.py --freeze   # once, after all authored files exist
python3 -I -B verify_custody.py
python3 -I -B verify_custody.py --sources # optional primary-source body re-fetch
"""
from pathlib import Path
import argparse
import datetime
import hashlib
import json
import os
import stat
import tempfile

HERE = Path(__file__).resolve().parent
HEAD = '4a38c3ccc4cac918fb75fd4b97449f3ebd2e0f7f'
MANIFEST = 'MANIFEST.json'


def atomic(path, data):
    fd, temporary = tempfile.mkstemp(prefix='.new-', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(data); stream.flush(); os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.lexists(temporary):
            os.unlink(temporary)


def digest_regular(path):
    if not stat.S_ISREG(path.lstat().st_mode):
        raise ValueError('nonregular object: '+str(path))
    # O_NOFOLLOW closes the ordinary symlink substitution route.
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            raise ValueError('opened object is not regular')
        h = hashlib.sha256()
        with os.fdopen(fd, 'rb', closefd=False) as stream:
            for chunk in iter(lambda: stream.read(65536), b''):
                h.update(chunk)
        return h.hexdigest()
    finally:
        os.close(fd)


def file_set(folder):
    paths = {}
    for path in folder.iterdir():
        if path.name == MANIFEST:
            continue
        paths[path.name] = digest_regular(path)
    return paths


def validate_set(folder, expected):
    if any(Path(name).name != name or name in ('.', '..', MANIFEST) for name in expected):
        raise ValueError('unsafe manifest filename')
    actual = file_set(folder)
    if actual != expected:
        raise ValueError('file set/hash mismatch')
    return True


def selftest():
    outcomes = {}
    with tempfile.TemporaryDirectory(prefix='.custody-controls-', dir=HERE) as name:
        folder = Path(name)
        target = folder/'sample.txt'
        atomic(target, b'original\n')
        expected = file_set(folder)
        outcomes['positive'] = validate_set(folder, expected)
        def reject(label):
            try:
                validate_set(folder, expected)
            except (OSError, ValueError):
                outcomes[label] = True
            else:
                raise AssertionError('mutation accepted: '+label)
        atomic(target, b'altered\n'); reject('modified_content')
        atomic(target, b'original\n')
        target.unlink(); reject('missing_file')
        atomic(target, b'original\n')
        extra=folder/'extra.txt'; atomic(extra,b'extra'); reject('unexpected_file'); extra.unlink()
        link=folder/'link'; link.symlink_to(target); reject('symlink_rejected'); link.unlink()
        fifo=folder/'fifo'; os.mkfifo(fifo); reject('fifo_rejected_without_open'); fifo.unlink()
        directory=folder/'directory'; directory.mkdir(); reject('directory_rejected'); directory.rmdir()
        validate_set(folder, expected)
    return {'status':'PASS','controls':outcomes,'temporary_controls_scope':'Only temporary descendants of this audit folder; all removed.'}


def freeze():
    if (HERE/MANIFEST).exists():
        raise ValueError('manifest already frozen')
    initial=json.loads((HERE/'INITIAL_ASSESSMENT.json').read_text())
    manifest={'format':1,'immutable_head':HEAD,'created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':file_set(HERE),'source_snapshot_sha256':initial['input_sha256'],'exclusion':'Only MANIFEST.json itself is excluded.'}
    atomic(HERE/MANIFEST,(json.dumps(manifest,indent=2,sort_keys=True)+'\n').encode())
    return {'status':'FROZEN','files':len(manifest['files']),'manifest_sha256':digest_regular(HERE/MANIFEST)}


def verify():
    manifest=json.loads((HERE/MANIFEST).read_text())
    if manifest['immutable_head'] != HEAD:
        raise ValueError('incorrect immutable head')
    validate_set(HERE,manifest['files'])
    base=HERE.parent
    for relative, expected in manifest['source_snapshot_sha256'].items():
        resolved=(base/relative).resolve()
        if not resolved.is_relative_to(base):
            raise ValueError('input escaped source snapshot')
        if digest_regular(base/relative) != expected:
            raise ValueError('source snapshot changed: '+relative)
    return {'status':'PASS','authored_files_verified':len(manifest['files']),'source_inputs_verified':len(manifest['source_snapshot_sha256']),'manifest_sha256':digest_regular(HERE/MANIFEST)}


def sources():
    import urllib.request
    custody=json.loads((HERE/'SOURCE_CUSTODY.json').read_text())
    result={}
    for key in ('prz2014','boyle2008'):
        item=custody[key]
        with urllib.request.urlopen(item['url'],timeout=30) as response:
            actual=hashlib.sha256(response.read()).hexdigest()
        if actual != item['body_sha256']:
            raise ValueError('primary response body changed: '+key)
        result[key]=actual
    return {'status':'PASS','response_body_sha256':result,'retention':'Response bodies in memory only.'}


def main():
    p=argparse.ArgumentParser()
    group=p.add_mutually_exclusive_group()
    group.add_argument('--selftest',action='store_true')
    group.add_argument('--freeze',action='store_true')
    group.add_argument('--sources',action='store_true')
    args=p.parse_args()
    result=selftest() if args.selftest else freeze() if args.freeze else sources() if args.sources else verify()
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':
    main()
