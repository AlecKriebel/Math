from pathlib import Path
import datetime, hashlib, json, os
A = Path(__file__).resolve().parent
D = A / 'priority_later_version_followup_20261005'
checks = []
def verify_row(base, row):
    rel = row.get('path', row.get('file'))
    if rel is None:
        raise RuntimeError('manifest path missing')
    f = base / rel
    b = f.read_bytes()
    if len(b) != row['bytes'] or hashlib.sha256(b).hexdigest() != row['sha256']:
        raise RuntimeError('byte pin mismatch: ' + str(f))
    checks.append({'file':str(f.relative_to(A)), 'bytes':len(b), 'sha256':hashlib.sha256(b).hexdigest()})
manifest = json.loads((D / 'CLOSED_MANIFEST.json').read_text())
for row in manifest.get('files', manifest.get('pins', [])):
    verify_row(D, row)
if not checks:
    raise RuntimeError('empty or unrecognized closed manifest')
closure = json.loads((D / 'CLOSURE.json').read_text())
actual_mhash = hashlib.sha256((D / 'CLOSED_MANIFEST.json').read_bytes()).hexdigest()
if actual_mhash != closure['manifest']['sha256'] or closure['manifest_members'] != len(manifest['files']):
    raise RuntimeError('closure does not authenticate manifest')
for key in ['manifest', 'report']:
    verify_row(D, closure[key])
ledger = json.loads((D / 'SOURCE_LEDGER.json').read_text())
for src in ledger['sources']:
    for row in src.get('files', []):
        verify_row(D, row)
for record in sorted((D / 'processes').glob('retrieval_*.json')):
    row = json.loads(record.read_text())
    verify_row(D, row)
    b = (D / row['path']).read_bytes()
    if b.startswith(b'%PDF-') != row['PDF']:
        raise RuntimeError('retrieval PDF classification mismatch')
for record in sorted((D / 'processes').glob('extract_*.json')):
    row = json.loads(record.read_text())
    if row['exit'] != 0:
        raise RuntimeError('extraction failed')
    for f, h in [(Path(row['argv'][2]),row['source_sha256']), (Path(row['argv'][3]),row['extraction_sha256']), (D / 'retrieve_extract.py',row['script_sha256'])]:
        if hashlib.sha256(f.read_bytes()).hexdigest() != h:
            raise RuntimeError('extraction execution pin mismatch: ' + str(f))
for name in ['INPUT_MANIFEST.json', 'VERSION_COMPARISON_INPUTS.json']:
    for row in json.loads((D / name).read_text())['inputs']:
        f = Path(row['path'])
        b = f.read_bytes()
        if len(b) != row['bytes'] or hashlib.sha256(b).hexdigest() != row['sha256']:
            raise RuntimeError('external input changed: ' + str(f))
for row in json.loads((D / 'adversarial_review/artifact_manifest.json').read_text())['files']:
    verify_row(D / 'adversarial_review', {'path':row['path_relative_to_adversarial_review'], 'bytes':row['size_bytes'], 'sha256':row['sha256']})
thesis = A / 'priority_thesis_repository_followup_20261005'
tc = json.loads((thesis / 'CLOSURE.json').read_text())
if tc['manifest_sha256'] != hashlib.sha256((thesis / 'CLOSED_AUTHORED_MANIFEST.json').read_bytes()).hexdigest():
    raise RuntimeError('thesis closure mismatch')
for row in json.loads((thesis / 'CLOSED_AUTHORED_MANIFEST.json').read_text())['pins']:
    verify_row(A, row)
receipt = {'schema':'ROOT-later-priority-closed-integrity/v1', 'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(), 'actual_operator_PID':os.getpid(), 'manifest_sha256':actual_mhash, 'checks':checks, 'integrity_checks':len(checks), 'priority_clearance':False, 'publication_clearance':False, 'source_read_claim':'ROOT read report, ledger, limitations and child report; checks authenticate byte custody, not every source page.'}
(A / 'ROOT_AUTHENTICATED_PRIORITY_LATER_FOLLOWUP_20261005.json').write_text(json.dumps(receipt, indent=2)+'\n')
print(json.dumps({k:v for k,v in receipt.items() if k != 'checks'}))
