"""Read-only verification of the externally anchored closed independent review."""
from pathlib import Path
import argparse, gzip, hashlib, json, stat
D = Path(__file__).resolve().parent

def need(ok, message):
    if not ok:
        raise RuntimeError(message)

def sha_file(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for data in iter(lambda: f.read(65536), b''):
            h.update(data)
    return h.hexdigest()

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--expected-seal-sha256', required=True)
    args = p.parse_args()
    seal_path = D/'CLOSED_DIRECTORY_SEAL.json'
    need(sha_file(seal_path) == args.expected_seal_sha256, 'External seal changed')
    seal = json.loads(seal_path.read_text())
    expected = seal['entries']
    actual = {'.'} | {str(p.relative_to(D)) for p in D.rglob('*')
                      if p != seal_path}
    need(actual == set(expected), 'Closed review inventory changed')
    for rel, e in expected.items():
        path = D if rel == '.' else D/rel
        need(not path.is_symlink(), 'Unexpected symbolic link')
        s = path.lstat()
        need(stat.S_IMODE(s.st_mode) == e['mode'] and s.st_mtime_ns == e['mtime_ns'],
             'Closed metadata changed: '+rel)
        if e['kind'] == 'file':
            need(stat.S_ISREG(s.st_mode) and s.st_size == e['bytes']
                 and sha_file(path) == e['sha256'], 'Closed bytes changed: '+rel)
        else:
            need(stat.S_ISDIR(s.st_mode), 'Closed directory changed')
    pins = json.loads((D/'INPUT_PINS.json').read_text())['inputs']
    for e in pins:
        path = Path(e['path'])
        s = path.stat()
        need(not path.is_symlink() and s.st_size == e['bytes']
             and sha_file(path) == e['sha256'] and stat.S_IMODE(s.st_mode) == e['mode']
             and s.st_mtime_ns == e['mtime_ns'], 'Reviewed original input changed')
    client = json.loads((D/'READ_CLIENT_PIN.json').read_text())
    need(sha_file(Path(client['path'])) == client['sha256'], 'Shared read client changed')
    results = json.loads((D/'RESULTS.json').read_text())
    need(results['status'] == 'PASS_REVIEW_CONTROLS' and results['completed'] == 16,
         'Independent controls incomplete')
    containers = {}
    file_entries = directory_entries = 0
    for case in results['results']:
        receipt = case['custody']
        path = Path(receipt['inventory'])
        need(path.is_relative_to(D/'private/archives')
             and sha_file(path) == receipt['inventory_sha256'], 'Own custody index changed')
        inv = json.loads(path.read_text())
        for e in inv['files']:
            blob = Path(e['blob'])
            need(blob.is_relative_to(D/'private/archives/blobs'), 'Custody body escaped')
            if str(blob) not in containers:
                need(sha_file(blob) == e['blob_sha256'], 'Compressed body changed')
                h = hashlib.sha256()
                size = 0
                with gzip.open(blob, 'rb') as f:
                    for data in iter(lambda: f.read(65536), b''):
                        h.update(data)
                        size += len(data)
                containers[str(blob)] = (size, h.hexdigest())
            need(containers[str(blob)] == (e['bytes'], e['sha256']), 'Decoded body changed')
        file_entries += len(inv['files'])
        directory_entries += len(inv['directories'])
    need(file_entries == 1106 and directory_entries == 142, 'Own custody count changed')
    for filename, cases, files, dirs in [('PHYSICAL_CUSTODY_READBACK.json', 51, 3466, 430),
                                          ('OWN_PHYSICAL_CUSTODY_READBACK.json', 16, 1106, 142)]:
        report = json.loads((D/filename).read_text())
        need(report['cases'] == cases and report['files'] == files
             and report['directories'] == dirs, 'Physical readback receipt changed')
    need(not list((D/'private/active').iterdir()), 'Active own case remains')
    review = json.loads((D/'ACTION_REVIEW.json').read_text())
    need(review['independent_action_review'] is True and review['action_review_accepted'] is True
         and review['root_action_adoption'] is False and review['publication_ready'] is False,
         'Review/authority boundary changed')
    print(json.dumps({'status': 'CLOSED_REVIEW_READBACK_PASS', 'review_files': seal['files'],
                      'review_directories': seal['directories'], 'original_input_pins': len(pins),
                      'own_parser_cases': 16, 'own_verified_gzip_blobs': len(containers),
                      'own_custody_files': file_entries, 'own_custody_directories': directory_entries,
                      'real_actions': 0, 'root_action_accepted': False, 'publication_ready': False},
                     indent=2))

if __name__ == '__main__':
    main()
