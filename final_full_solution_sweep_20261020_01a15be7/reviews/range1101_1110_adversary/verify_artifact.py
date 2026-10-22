#!/usr/bin/env python3
"""Read-only offline custody/scope checks; no proof, priority or live-state certificate."""
import argparse
import hashlib
import io
import json
import math
from pathlib import Path, PurePosixPath
import re
import stat
import zipfile


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def pairs(items):
    result = {}
    for key, value in items:
        require(key not in result, 'duplicate JSON key')
        result[key] = value
    return result


def reject_constant(value):
    raise RuntimeError('nonfinite JSON constant')


def finite_float(value):
    result = float(value)
    require(math.isfinite(result), 'nonfinite JSON float')
    return result


def parse(data):
    return json.loads(data.decode('utf-8'), object_pairs_hook=pairs,
                      parse_constant=reject_constant, parse_float=finite_float)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def gitsha(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def safe(name):
    require(type(name) is str and name != '', 'empty/nonstring path')
    path = PurePosixPath(name)
    require(str(path) == name and not path.is_absolute() and '..' not in path.parts
            and '\\' not in name, 'unsafe path')
    return path


def read(root, name):
    safe(name)
    path = root / name
    for part in [path, *path.parents]:
        require(not part.is_symlink(), 'symlink input')
    require(path.is_file() and stat.S_ISREG(path.stat().st_mode), 'nonregular input')
    return path.read_bytes()


def pins(root, rows):
    require(type(rows) is list, 'pin-list type')
    names = []
    for row in rows:
        require(type(row) is dict and set(row) == {'path', 'bytes', 'sha256'}, 'pin schema')
        safe(row['path'])
        require(type(row['bytes']) is int and row['bytes'] >= 0, 'pin byte type')
        require(type(row['sha256']) is str and re.fullmatch('[0-9a-f]{64}', row['sha256']), 'pin digest type')
        data = read(root, row['path'])
        require(len(data) == row['bytes'] and sha(data) == row['sha256'], 'changed pin: ' + row['path'])
        names.append(row['path'])
    require(names == sorted(set(names)), 'unsorted/duplicate pins')
    return set(names)


def verify(root, expected):
    require(type(expected) is str and re.fullmatch('[0-9a-f]{64}', expected), 'external digest required')
    wire = read(root, 'OUTPUT_MANIFEST.json')
    require(sha(wire) == expected, 'external manifest anchor')
    require(read(root, 'OUTPUT_MANIFEST.sha256') == (expected + '\n').encode(), 'manifest sidecar')
    m = parse(wire)
    require(set(m) == {'schema_version', 'public_files', 'private_manifest'}, 'public schema')
    require(type(m['schema_version']) is int and m['schema_version'] == 1, 'public schema version')
    public = pins(root, m['public_files'])
    require(public == {'.gitignore', 'REVIEW.md', 'CHECK_RESULTS.json', 'RESEARCH_LOG.md', 'verify_artifact.py'}, 'public membership')
    require(m['private_manifest']['path'] == 'private/PRIVATE_MANIFEST.json', 'private manifest path')
    pins(root, [m['private_manifest']])
    pm = parse(read(root, m['private_manifest']['path']))
    require(set(pm) == {'schema_version', 'files', 'directories'}, 'private schema')
    require(type(pm['schema_version']) is int and pm['schema_version'] == 1, 'private schema version')
    private = pins(root, pm['files'])
    require(all(x.startswith('private/') for x in private), 'private namespace')
    actual_files, actual_dirs = set(), set()
    for p in (root / 'private').rglob('*'):
        require(not p.is_symlink(), 'private symlink')
        name = p.relative_to(root).as_posix()
        if p.is_dir():
            actual_dirs.add(name)
        else:
            read(root, name)
            actual_files.add(name)
    require(actual_files == private | {m['private_manifest']['path']}, 'closed private file inventory')
    require(type(pm['directories']) is list and pm['directories'] == sorted(actual_dirs), 'closed directory inventory')
    require({p.name for p in root.iterdir()} == public | {'OUTPUT_MANIFEST.json', 'OUTPUT_MANIFEST.sha256', 'private'}, 'closed outer inventory')
    droot = 'private/checkpoint/files/'
    state = parse(read(root, droot + 'STATE.json'))
    journal = [parse(x) for x in read(root, droot + 'dispositions.jsonl').splitlines()]
    require(state['last_completely_processed_pr'] == 1110 and state['next_pr'] == 1111, 'frozen cursor')
    require([r['pr'] for r in journal] == list(range(9, 1111)), 'frozen contiguous journal')
    path_count = 0
    for n in range(1101, 1111):
        row = parse(read(root, droot + f'PR{n}_DISPOSITION.json'))
        require(row == next(r for r in journal if r['pr'] == n), 'individual decision/journal')
        scope = parse(read(root, droot + f'PR{n}_PINNED_SCOPE_VERIFICATION.json'))
        require(scope['all_complete_paths_equal'] is True and scope['all_added_rows_equal'] is True and scope['added_queue_rows'] == [], 'frozen scope flags')
        live = parse(read(root, f'private/actual/pr{n}/live_pr.json'))
        cache = parse(read(root, f'private/actual/pr{n}/eligibility_cache.json'))
        require(scope['head'] == live['head']['sha'] == cache['inventory_head_sha'], 'head identity')
        require(scope['base'] == live['base']['sha'] == cache['inventory_base_sha'], 'base identity')
        bc = parse(read(root, f'private/actual/pr{n}/blob_checks.json'))
        require(len(bc) == scope['path_count'] == len(cache['files']), 'complete path count')
        cachemap = {x['filename']: x['sha'] for x in cache['files']}
        require(len(cachemap) == len(bc), 'unique actual paths')
        for item in bc:
            data = read(root, f'private/actual/pr{n}/head/' + item['path'])
            require(gitsha(data) == item['git_blob'] == cachemap[item['path']], 'actual original Git blob')
            require(len(data) == item['bytes'] and sha(data) == item['sha256'], 'actual original data')
            require(not item['path'].endswith('QUEUE.md'), 'unexpected QUEUE')
        path_count += len(bc)
    require(path_count == 83, '83 original files')
    ledger = parse(read(root, 'private/live_ledger.json'))['values']
    require(len(ledger) == 180, 'captured ledger rows')
    for n, record, rownum, expected_count in [(1102,23439582,149,20),(1108,23440119,151,26)]:
        prefix = f'private/publications/pr{n}/'
        z = parse(read(root, prefix + 'provider.json'))
        require(z['state'] == 'done' and z['submitted'] is True, 'captured publication state')
        doi = '10.5281/zenodo.' + str(record)
        require(z['doi'] == doi and doi in ledger[rownum-1][2], 'captured DOI ledger binding')
        require(sum(doi in str(x[2]) for x in ledger if len(x)>2) == 1, 'unique captured DOI row')
        archive_data = None
        for item in z['files']:
            data = read(root, prefix + 'files/' + item['key'])
            require(len(data) == item['size'] and item['checksum'] == 'md5:' + hashlib.md5(data).hexdigest(), 'captured provider payload')
            if item['key'].endswith('.zip'):
                archive_data = data
        require(archive_data is not None, 'archive exists')
        with zipfile.ZipFile(io.BytesIO(archive_data)) as archive:
            names = archive.namelist()
            require(len(names) == len(set(names)) == expected_count and archive.testzip() is None, 'unique CRC closed archive')
            manifest = parse(archive.read('SOURCE_MANIFEST.json'))
            require(set(names) == set(manifest) | {'SOURCE_MANIFEST.json'}, 'closed package manifest')
            for name in names:
                safe(name)
                info = archive.getinfo(name)
                require(not info.is_dir() and stat.S_IFMT(info.external_attr >> 16) in (0,stat.S_IFREG), 'regular archive member')
                data = archive.read(name)
                require(data == read(root, prefix + 'archive/' + name), 'retained archive member')
                if name in manifest:
                    require(len(data) == manifest[name]['bytes'] and sha(data) == manifest[name]['sha256'], 'package manifest pin')
    return {'status':'PASS','reviewed_prs':10,'original_head_files':path_count,
            'public_payload_files':len(public),'private_payload_files':len(private),
            'scope':'Offline captured byte identities, inventory closure and bounded record consistency only; no proof, priority, current-provider-state or global-sweep certificate'}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root',type=Path,default=Path(__file__).resolve().parent)
    ap.add_argument('--expect-manifest-sha256',required=True)
    args = ap.parse_args()
    print(json.dumps(verify(args.root.resolve(),args.expect_manifest_sha256),sort_keys=True))


if __name__ == '__main__':
    main()
