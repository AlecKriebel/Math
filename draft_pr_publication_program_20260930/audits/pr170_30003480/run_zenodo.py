"""Use the repository kit only after the accepted frozen scientific gate."""
from pathlib import Path
import datetime, hashlib, json, subprocess, sys

A = Path(__file__).resolve().parent
R = Path('/Users/alec/Documents/Math')
PY = '/opt/homebrew/opt/python@3.14/bin/python3.14'

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def save(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')

def main():
    require(len(sys.argv) == 2 and sys.argv[1] in ['stage', 'reconcile', 'draft', 'publish', 'published'], 'Choose one phase')
    phase = sys.argv[1]
    gate = json.loads((A / 'ROOT_PUBLICATION_GATE.json').read_text())
    require(gate['status'] == 'READY_FOR_AUTHORIZED_PUBLICATION', 'Accepted complete-package scientific gate required')
    require(gate['human_authorized_qualified_publication'] and gate['fresh_seal_first_review_clean'], 'Qualified publication and clean fresh review required')
    for name, identity in gate['kit_files'].items():
        data = (R / name).read_bytes()
        require(len(data) == identity['bytes'] and hashlib.sha256(data).hexdigest() == identity['sha256'], 'Authorized kit code changed: ' + name)
    package = A / gate['package']
    for name, pin in gate['files'].items():
        data = (package / name).read_bytes()
        require(len(data) == pin['bytes'] and hashlib.sha256(data).hexdigest() == pin['sha256'], 'Frozen package changed: ' + name)
    manifest = A / gate['deposit_manifest']
    require(hashlib.sha256(manifest.read_bytes()).hexdigest() == gate['deposit_manifest_sha256'], 'Deposit manifest changed')
    require(json.loads(manifest.read_text())['metadata'] == json.loads((package / 'metadata.json').read_text()), 'Metadata is not exact')
    state = R / '.zenodo-state' / (hashlib.sha256(str(manifest).encode()).hexdigest()[:24] + '-production.json')
    journal = A / 'zenodo_operation_journal'
    journal.mkdir(exist_ok=True)
    command = 'stage' if phase == 'stage' else 'publish' if phase == 'publish' else 'inspect'
    require(phase != 'stage', 'The existing draft is already staged; use read-only reconcile, never create a duplicate')
    transport_gate = json.loads((A / 'ROOT_PUBLICATION_TRANSPORT_GATE.json').read_text())
    require(transport_gate['status'] == 'EXACT_HTML_DESCRIPTION_TRANSPORT_GUARD_INDEPENDENTLY_VERIFIED', 'Exact transport guard clearance required')
    guard = A / 'zenodo_exact_description_guard.py'
    guard_bytes = guard.read_bytes()
    require(transport_gate['guard_identity'] == {'bytes': len(guard_bytes), 'sha256': hashlib.sha256(guard_bytes).hexdigest()}, 'Transport guard changed')
    args = [PY, '-E', '-S', '-B', '-P', str(guard), command, str(manifest)]
    expected_id = None
    if phase == 'reconcile':
        expected_id = 23318851
        require(json.loads(state.read_text())['id'] == expected_id, 'Original saved draft ID differs')
    elif phase != 'stage':
        stage = json.loads((A / 'ZENODO_STAGE_READBACK.json').read_text())
        expected_id = stage['id']
        require(json.loads(state.read_text())['id'] == expected_id, 'Saved record ID differs')
    if phase == 'publish':
        draft = json.loads((A / 'ZENODO_DRAFT_READBACK.json').read_text())
        require(draft['id'] == expected_id and draft['state'] == 'ready_to_publish', 'Exact inspected draft required')
        args += ['--confirm-id', str(expected_id)]
    if phase == 'published':
        args += ['--check-doi']
    request_path = journal / (phase + '.REQUEST.json')
    if command in ['stage', 'publish']:
        require(not request_path.exists() or (phase == 'stage' and state.exists()), 'Prior mutation outcome requires read-only reconciliation')
        if not request_path.exists():
            save(request_path, {'UTC': datetime.datetime.now(datetime.UTC).isoformat(), 'phase': phase, 'manifest_sha256': gate['deposit_manifest_sha256'], 'expected_id': expected_id})
    result = subprocess.run(args, cwd=R, capture_output=True, text=True, timeout=300)
    require(result.returncode == 0, result.stderr[:1400])
    value = json.loads(result.stdout)
    require(value['environment'] == 'production' and value['title'] == gate['title'], 'Wrong publication/environment')
    expected_files = {name: {'name': name, 'size': gate['files'][name]['bytes'], 'sha256': gate['files'][name]['sha256']} for name in gate['upload_files']}
    require({item['name']: item for item in value['files']} == expected_files, 'Remote kit verification differs from frozen files')
    if expected_id is not None:
        require(value['id'] == expected_id, 'Wrong deposition ID')
    name = {'stage': 'ZENODO_STAGE_READBACK.json', 'reconcile': 'ZENODO_STAGE_READBACK.json', 'draft': 'ZENODO_DRAFT_READBACK.json', 'publish': 'ZENODO_PUBLICATION_RESPONSE.json', 'published': 'ZENODO_PUBLICATION_READBACK.json'}[phase]
    require(value['state'] == ('published' if phase in ['publish', 'published'] else 'ready_to_publish'), 'Wrong actual remote state')
    if phase in ['publish', 'published']:
        require(value.get('doi') and value.get('doi_url'), 'Confirmed publication needs an assigned DOI')
    save(A / name, value)
    print(json.dumps({key: value.get(key) for key in ['id', 'state', 'title', 'doi', 'doi_url', 'record_url', 'doi_resolution', 'metadata_normalizations']}))

if __name__ == '__main__':
    main()
