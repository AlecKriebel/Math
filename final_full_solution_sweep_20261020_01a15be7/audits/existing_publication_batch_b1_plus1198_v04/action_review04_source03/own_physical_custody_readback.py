"""Independent full physical reconstruction of the reviewer's own cases.

Read original archives only. Restore exact paths, file/directory modes and
nanosecond mtimes into a fresh review-owned scratch tree; verify, then remove
only that redundant own reconstruction after comparison to retained archives.
"""
from pathlib import Path
import datetime, gzip, hashlib, json, os, shutil, stat
D = Path(__file__).resolve().parent
A = D.parent / 'actor01'
F = A / 'private/focused03'
CAP = 18 * 1024 * 1024
RESERVE = 64 * 1024 * 1024

def need(ok, message):
    if not ok:
        raise RuntimeError(message)

def sha_file(p):
    h = hashlib.sha256()
    with p.open('rb') as f:
        for data in iter(lambda: f.read(65536), b''):
            h.update(data)
    return h.hexdigest()

def save(path, value):
    with path.open('x') as f:
        json.dump(value, f, indent=2)
        f.write('\n')
        f.flush()
        os.fsync(f.fileno())

def main():
    need(not (D/'OWN_PHYSICAL_CUSTODY_READBACK.json').exists(), 'Completed readback must not repeat')
    need(not list((D/'private/active').iterdir()), 'Wait for own parsed controls to finish')
    results = json.loads((D/'RESULTS.json').read_text())
    scratch = D/'private/physical_independent_case'
    need(not scratch.exists(), 'Preserve earlier incomplete scratch')
    counts = {'cases': 0, 'files': 0, 'directories': 0, 'regular_bytes': 0}
    peak = 0
    min_free = 10**30
    receipts = []
    for case in results['results']:
        c = case['custody']
        inventory_path = Path(c['inventory'])
        need(sha_file(inventory_path) == c['inventory_sha256'], 'Original inventory changed')
        inv = json.loads(inventory_path.read_text())
        for e in inv['files'] + inv['directories']:
            rel = Path(e['relative'])
            need(not rel.is_absolute() and '..' not in rel.parts, 'Unsafe archived relative path')
        scratch.mkdir()
        for e in inv['directories']:
            if e['relative'] != '.':
                (scratch/e['relative']).mkdir(parents=True, exist_ok=False)
        for e in inv['files']:
            free = shutil.disk_usage(D).free
            min_free = min(min_free, free)
            need(free >= RESERVE, 'Actual storage reserve below64MiB')
            target = scratch/e['relative']
            h = hashlib.sha256()
            total = 0
            with gzip.open(e['blob'], 'rb') as source, target.open('xb') as out:
                for data in iter(lambda: source.read(65536), b''):
                    out.write(data)
                    h.update(data)
                    total += len(data)
                out.flush()
                os.fsync(out.fileno())
            need(total == e['bytes'] and h.hexdigest() == e['sha256'], 'Decompression mismatch')
            os.chmod(target, e['mode'])
            os.utime(target, ns=(e['mtime_ns'], e['mtime_ns']))
        for e in sorted(inv['directories'], key=lambda x: len(Path(x['relative']).parts), reverse=True):
            target = scratch/e['relative']
            os.chmod(target, e['mode'])
            os.utime(target, ns=(e['mtime_ns'], e['mtime_ns']))
        expected = {e['relative'] for e in inv['files'] + inv['directories']}
        need({str(p.relative_to(scratch)) for p in [scratch, *scratch.rglob('*')]} == expected,
             'Physical reconstructed closure mismatch')
        allocated = sum(p.stat().st_blocks*512 for p in [D, *D.rglob('*')])
        peak = max(peak, allocated)
        need(allocated <= CAP, 'Review18MiB incremental cap exceeded')
        for e in inv['files']:
            p = scratch/e['relative']
            s = p.lstat()
            need(stat.S_ISREG(s.st_mode) and stat.S_IMODE(s.st_mode) == e['mode']
                 and s.st_mtime_ns == e['mtime_ns'] and s.st_size == e['bytes']
                 and sha_file(p) == e['sha256'], 'Physical regular entry mismatch')
        for e in inv['directories']:
            s = (scratch/e['relative']).lstat()
            need(stat.S_ISDIR(s.st_mode) and stat.S_IMODE(s.st_mode) == e['mode']
                 and s.st_mtime_ns == e['mtime_ns'], 'Physical directory metadata mismatch')
        receipts.append({'case': case['name'], 'inventory_sha256': c['inventory_sha256'],
                         'files': len(inv['files']), 'directories': len(inv['directories']),
                         'all_paths_bytes_modes_nsmtimes_physically_verified': True})
        # The old authoritative inventory/archives remain present and unchanged.
        # Only this unique review-owned, fully authenticated duplicate is retired.
        for e in inv['files']:
            (scratch/e['relative']).unlink()
        for e in sorted(inv['directories'], key=lambda x: len(Path(x['relative']).parts), reverse=True):
            (scratch/e['relative']).rmdir()
        counts['cases'] += 1
        counts['files'] += len(inv['files'])
        counts['directories'] += len(inv['directories'])
        counts['regular_bytes'] += sum(e['bytes'] for e in inv['files'])
    report = {'at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'status': 'ALL_INDEPENDENT_CASES_PHYSICALLY_RESTORED_AND_READ_BACK', **counts,
              'peak_review_allocated_bytes_during_restores': peak,
              'minimum_actual_free_bytes': min_free, 'cases_verified': receipts,
              'original_archive_or_input_changes': 0, 'real_service_actions': 0,
              'root_action_accepted': False, 'publication_ready': False}
    save(D/'OWN_PHYSICAL_CUSTODY_READBACK.json', report)
    print(json.dumps({k:v for k,v in report.items() if k != 'cases_verified'}), flush=True)

if __name__ == '__main__':
    main()
