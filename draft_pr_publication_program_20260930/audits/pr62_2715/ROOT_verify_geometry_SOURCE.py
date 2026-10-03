"""ROOT-only readback of the exact dated geometry SOURCE; no family mutation."""
from pathlib import Path
import datetime, hashlib, json, os, stat, sys

A = Path(__file__).resolve().parent
F = A / 'ribbon_knot_geometry_adversary_family'
PIN = '5fd55ccc3a0b9585c12e617c250e81611845dfa049de563c8be2070016e16317'

def need(value, message):
    if not value:
        raise ValueError(message)

def read(path):
    need(not path.is_symlink() and all(not p.is_symlink() for p in path.parents), 'No symlink')
    before = path.stat()
    need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1, 'Regular singly linked body')
    with path.open('rb') as stream:
        opened = os.fstat(stream.fileno())
        body = stream.read()
        end = os.fstat(stream.fileno())
    after = path.stat()
    identity = lambda q: (q.st_dev, q.st_ino, q.st_mode, q.st_size, q.st_mtime_ns, q.st_ctime_ns)
    need(all(identity(q) == identity(before) for q in [opened, end, after]), 'Stable opened body')
    return body, {'path': str(path), 'bytes': len(body), 'sha256': hashlib.sha256(body).hexdigest(),
                  'full_mode_07777': format(stat.S_IMODE(after.st_mode), '04o'), 'nlink': after.st_nlink}

def check(row, dated_mode_change=False):
    body, current = read(Path(row['path']))
    for key in ['path', 'bytes', 'sha256', 'nlink']:
        need(current[key] == row[key], 'Exact body/identity descriptor: ' + key)
    if dated_mode_change:
        need(row['full_mode_07777'] == '0644' and current['full_mode_07777'] == '0444',
             'Only independently authenticated original SOURCE freeze mode transition')
    else:
        need(current['full_mode_07777'] == row['full_mode_07777'], 'Exact full mode')
    return body, current

def main():
    need(sys.argv[1:] == ['--source-only'] and __debug__, 'Explicit ROOT SOURCE readback')
    source_body, source = read(F / 'SOURCE.json')
    need(source['sha256'] == PIN and source['full_mode_07777'] == '0644', 'Exact prepared SOURCE')
    obj = json.loads(source_body)
    need(obj['schema'] == 'pr62-geometry-priority-source-only/v1' and obj['root'] == str(F), 'Literal family')
    paths = set()
    for row in obj['files']:
        rel = Path(row['relative_path'])
        need(not rel.is_absolute() and '..' not in rel.parts and rel.as_posix() not in paths,
             'Distinct safe relative SOURCE path')
        need(Path(row['path']) == F / rel, 'Exact family path')
        paths.add(rel.as_posix())
        check(row)
    actual_files = set()
    actual_dirs = {'.'}
    for p in F.rglob('*'):
        need(not p.is_symlink(), 'No family symlink')
        rel = p.relative_to(F).as_posix()
        if p.is_dir():
            actual_dirs.add(rel)
        else:
            need(p.is_file(), 'No family special object')
            actual_files.add(rel)
    need(actual_files == paths | {'SOURCE.json'} and len(paths) == 21, 'Exact complete SOURCE domain')
    directories = {r['relative_path'] for r in obj['directories']}
    need(actual_dirs == directories and len(directories) == 5, 'Exact directory domain')
    for row in obj['directories']:
        p = F / row['relative_path']
        need(str(p) == row['path'] and format(stat.S_IMODE(p.stat().st_mode), '04o') == row['full_mode_07777'] == '0755', 'Exact directory mode')
    for row in obj['external_original_body_pins']:
        check(row)
    need(len(obj['external_original_body_pins']) == 17, 'All original seventeen body pins')
    _, original_authentication = check(obj['original_authentication_index'], True)
    # The original SOURCE freeze happened after this dated external 0644 descriptor.
    original_source_body, original_source = read(A / 'original_preparation_family/SOURCE.json')
    need(original_source['sha256'] == 'b270b2fb405aca2ee0893e070b8b2b3fa0f72db3b05c4609adf3d5b18840b3e9', 'Root verified original SOURCE')
    original_index = json.loads(original_source_body)
    rows = [r for r in original_index['files'] if r['path'] == 'ORIGINAL_AUTHENTICATION.json']
    need(len(rows) == 1 and rows[0]['sha256'] == original_authentication['sha256'] and rows[0]['bytes'] == original_authentication['bytes'] and rows[0]['full_mode_07777'] == '0444', 'Original SOURCE proves exact freeze/body')
    streams = []
    for name in ['submitted_default', 'independent_default', 'independent_optimized_refusal']:
        body, _ = read(F / 'captures' / name / 'CAPTURE.json')
        capture = json.loads(body)
        for key in ['stdout', 'stderr']:
            raw, current = check(capture[key])
            streams.append({'capture': name, 'stream': key, 'descriptor': current})
            print(name + ' ' + key + ':')
            print(raw.decode('utf-8'))
    need(read(F / 'SOURCE.json')[0] == source_body, 'Source unchanged through complete readback')
    result = {'schema': 'pr62-ROOT-geometry-SOURCE-readback/v1', 'actual_pid': os.getpid(),
              'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'argv': sys.argv,
              'source': source, 'files': len(paths), 'directories': len(directories),
              'original_bodies': 17, 'source_files_and_modes_unchanged': True,
              'dated_external_authentication_mode': '0644 at preparation; exact body independently frozen0444 by original SOURCE',
              'current_original_authentication': original_authentication, 'original_source': original_source,
              'full_streams': streams, 'mathematical_approval_inferred': False}
    output = A / 'ROOT_GEOMETRY_SOURCE_READBACK_20261003.json'
    body = (json.dumps(result, indent=2, sort_keys=True) + '\n').encode()
    with output.open('xb') as stream:
        stream.write(body)
        os.fchmod(stream.fileno(), 0o444)
        stream.flush()
        os.fsync(stream.fileno())
    print(json.dumps({'status': 'PASS_DATED_SOURCE_READBACK_ONLY', 'receipt': read(output)[1]}))

if __name__ == '__main__':
    main()
