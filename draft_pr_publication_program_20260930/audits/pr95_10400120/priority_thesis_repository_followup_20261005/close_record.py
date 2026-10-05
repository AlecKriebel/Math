from pathlib import Path
import datetime, hashlib, json, os
D = Path(__file__).resolve().parent
A = D.parent
op = A / 'actual_operations/root_thesis_osaka_retrieval'
actual = json.loads((op / 'execution.json').read_text())
for name in ['stdout', 'stderr']:
    b = (op / actual[name]['path']).read_bytes()
    if len(b) != actual[name]['bytes'] or hashlib.sha256(b).hexdigest() != actual[name]['sha256']:
        raise RuntimeError('actual capture hash mismatch: ' + name)
rows = json.loads((D / 'OSAKA_NATIVE_RETRIEVAL.json').read_text())
if rows != json.loads((op / 'stdout.bin').read_text()) or len(rows) != 3:
    raise RuntimeError('retrieval scope mismatch')
if actual['exit_code'] != 0 or actual['child_PID'] != 32033:
    raise RuntimeError('actual operation mismatch')
for row in rows:
    if row['operator_PID'] != actual['child_PID'] or not row['retrieval_failed'] or row['source_read']:
        raise RuntimeError('invalid unavailable-source claim')
pins = []
files = sorted(D.glob('*')) + sorted(op.glob('*'))
for f in files:
    if not f.is_file() or f.name in ['CLOSED_AUTHORED_MANIFEST.json', 'CLOSURE.json']:
        continue
    b = f.read_bytes()
    pins.append({'file':str(f.relative_to(A)), 'bytes':len(b), 'sha256':hashlib.sha256(b).hexdigest()})
manifest = {'schema':'closed-authored-source-followup/v1', 'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(), 'actual_operator_PID':os.getpid(), 'pins':pins, 'mathematical_computations':0, 'priority_clearance':False, 'primary_source_read_limits':'SOURCE_READ_SCOPES.json', 'retrieval_success_not_inferred_from_process_exit':True}
(D / 'CLOSED_AUTHORED_MANIFEST.json').write_text(json.dumps(manifest, indent=2)+'\n')
mb = (D / 'CLOSED_AUTHORED_MANIFEST.json').read_bytes()
closure = {'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(), 'actual_operator_PID':os.getpid(), 'manifest_sha256':hashlib.sha256(mb).hexdigest(), 'pins_verified':len(pins), 'closed':True, 'priority_clearance':False}
(D / 'CLOSURE.json').write_text(json.dumps(closure, indent=2)+'\n')
print(json.dumps(closure))
