from pathlib import Path
import argparse, datetime, hashlib, json, os

parser = argparse.ArgumentParser()
parser.add_argument('family')
parser.add_argument('manifest_name')
parser.add_argument('expected_manifest_sha256')
args = parser.parse_args()
A = Path(__file__).resolve().parent
D = A / args.family
M = D / args.manifest_name
require = lambda c, m: None if c else (_ for _ in ()).throw(RuntimeError(m))
require(D.resolve().parent == A, 'Family must be an immediate dedicated folder')
body = M.read_bytes()
require(hashlib.sha256(body).hexdigest() == args.expected_manifest_sha256, 'Closed manifest hash differs')
manifest = json.loads(body)
rows = manifest.get('entries', manifest.get('files', manifest.get('payload_files')))
require(isinstance(rows, list), 'Unrecognized manifest entries')
borrowed = manifest.get('borrowed_read_only_inputs', manifest.get('read_only_borrowed_inputs', manifest.get('borrowed_inputs', [])))
pins = []
for is_borrowed, source_rows in [(False, rows), (True, borrowed)]:
    for row in source_rows:
        filename = row.get('path', row.get('file', row.get('borrowed_read_only_path')))
        p = Path(filename) if is_borrowed else D / filename
        require(p.is_file() and not p.is_symlink(), 'Missing or symlinked body: ' + str(p))
        require(is_borrowed or p.resolve().is_relative_to(D), 'Own manifest traversal')
        b = p.read_bytes()
        require(len(b) == row.get('bytes', row.get('size')), 'Size changed: ' + str(p))
        require(hashlib.sha256(b).hexdigest() == row['sha256'], 'Body changed: ' + str(p))
        pins.append({'path': str(p), 'bytes': len(b), 'sha256': row['sha256'], 'borrowed': is_borrowed})
detached = manifest.get('detached_checksum')
exclusions = {args.manifest_name}
if detached:
    require(detached == 'MANIFEST.sha256', 'Unrecognized detached checksum file')
    require((D / detached).read_text().split()[0] == args.expected_manifest_sha256, 'Detached checksum differs')
    exclusions.add(detached)
actual = {str(p.relative_to(D)) for p in D.rglob('*') if p.is_file() and str(p.relative_to(D)) not in exclusions}
listed = {row.get('path', row.get('file')) for row in rows}
require(actual == listed, 'Closed own-file inventory differs')
require(hashlib.sha256((D/'REPORT.md').read_bytes()).hexdigest() == next(r['sha256'] for r in rows if r.get('path',r.get('file'))=='REPORT.md'), 'Report binding differs')
out = A / 'root_priority_evidence_authentication_20261006'
out.mkdir(exist_ok=True)
record = {'schema': 'root-closed-priority-family-authentication/v1',
          'UTC': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'operator_PID': os.getpid(),
          'family': args.family, 'manifest_file': str(M), 'manifest_sha256': args.expected_manifest_sha256,
          'own_files': len(rows), 'borrowed_files': len(borrowed), 'all_closed_bodies_verified': True,
          'full_ROOT_report_read': True, 'ROOT_read_claim_scope': 'Full REPORT.md, VERDICT.json and independent analysis; source read scope separately bounded.',
          'publication_clearance': False, 'pins': pins}
(out / (args.family + '.json')).write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({k:v for k,v in record.items() if k!='pins'}))
