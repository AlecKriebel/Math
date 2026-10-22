"""One authorized, guarded repository-kit publication. Reconcile uncertainty read-only."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import base64
import json
import subprocess
import urllib.request

PUB = Path(__file__).resolve().parent
ROOT = Path('/Users/alec/Documents/Math')
R = PUB.parent / 'preprint'
PY = '/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
KIT = ROOT / 'zenodo_deposit_tool/zenodo.py'
MANIFEST = R / 'deposit.json'
clear = json.loads((R / 'FINAL_CLEARANCE.json').read_text())
assert clear['release_cleared'] and clear['fresh_manuscript_reviews'] >= 2
assert clear['final_frozen_clean_reviews'] >= 1 and not clear['unresolved_mandatory_findings']
assert not clear['unresolved_optional_findings']
assert not (PUB / 'ZENODO_VERIFIED_PUBLICATION.json').exists(), 'Already verified: read-only reconciliation'
assert not (PUB / 'STAGE_ATTEMPT.json').exists(), 'Prior stage attempt: reconcile before another provider action'
for row in clear['submission_files']:
    raw = (R / row['path']).read_bytes()
    assert len(raw) == row['bytes'] and hashlib.sha256(raw).hexdigest() == row['sha256']
metadata = json.loads((R / 'metadata.json').read_text())
assert json.loads(MANIFEST.read_text())['metadata'] == metadata == clear['publication_metadata']
T = PUB / 'private_transport/zenodo'
T.mkdir(parents=True, exist_ok=True)


def preflight_read(label, command):
    result = subprocess.run(command, capture_output=True, text=True, timeout=60)
    (T / (label + '-stdout.json')).write_text(result.stdout)
    (T / (label + '-stderr.txt')).write_text(result.stderr)
    assert result.returncode == 0, label
    return json.loads(result.stdout)


pr = preflight_read('PR-head-preflight', ['/opt/homebrew/Cellar/gh/2.85.0/bin/gh', 'api', 'repos/AlecKriebel/Math/pulls/211'])
assert pr['state'] == 'open' and pr['draft'] and pr['head']['sha'] == '9d7b623203b525386da3d9d91548c79e7445a11c'
q = preflight_read('PR-status-preflight', ['/opt/homebrew/Cellar/gh/2.85.0/bin/gh', 'api',
    'repos/AlecKriebel/Math/contents/unsolved_math_prioritization/QUEUE.md?ref=' + pr['head']['sha']])
qrows = [x for x in base64.b64decode(q['content']).decode().splitlines() if '5100063 / AMR-050-0063' in x]
assert len(qrows) == 1 and qrows[0].split('|')[8].strip() == 'claimed_solved'
sheet = preflight_read('tracker-duplicate-preflight', ['/Users/alec/.nvm/versions/node/v22.16.0/bin/gws',
    'sheets', 'spreadsheets', 'values', 'get', '--params', json.dumps({
        'spreadsheetId': '1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20', 'range': "'Math Puzzles'!A:D"})])
matches = [i for i, row in enumerate(sheet.get('values', []), 1)
           if any('AMR-050-0063' in str(value) or '5100063' in str(value) for value in row)]
assert not matches, 'This problem already appears in the publication tracker: reconcile before creating another deposit'
(PUB / 'PUBLICATION_PREFLIGHT.json').write_text(json.dumps({'utc': datetime.now(timezone.utc).isoformat(),
    'PR': 211, 'head': pr['head']['sha'], 'QUEUE_status': 'claimed_solved',
    'existing_problem_tracker_rows': matches, 'no_existing_case_publication_found': True}, indent=2) + '\n')


def call(label, operation, extra=()):
    r = subprocess.run([PY, str(KIT), operation, str(MANIFEST), *extra], cwd=ROOT,
                       capture_output=True, text=True, timeout=600)
    (T / (label + '-stdout.json')).write_text(r.stdout)
    (T / (label + '-stderr.txt')).write_text(r.stderr)
    if r.returncode:
        raise RuntimeError(label + ' failed: inspect retained tool outcome before any mutation retry')
    return json.loads(r.stdout)


local = call('01-local-check', 'check')
assert local['environment'] == 'production' and len(local['files']) == 2
(PUB / 'STAGE_ATTEMPT.json').write_text(json.dumps({'utc': datetime.now(timezone.utc).isoformat(),
    'operation': 'repository kit stage about to be attempted', 'manifest': str(MANIFEST),
    'frozen_files': clear['submission_files']}, indent=2) + '\n')
stage = call('02-stage', 'stage')
assert stage['state'] == 'ready_to_publish' and stage['files'] == local['files']
(PUB / 'ZENODO_STAGED_VERIFIED.json').write_text(json.dumps(stage, indent=2) + '\n')
inspect = call('03-inspect-before-publication', 'inspect')
assert inspect['id'] == stage['id'] and inspect['files'] == local['files']
assert inspect['state'] != 'published', 'Unexpected pre-existing publication: reconcile without a new POST'
(PUB / 'PUBLISH_ATTEMPT.json').write_text(json.dumps({'utc': datetime.now(timezone.utc).isoformat(),
    'id': stage['id'], 'operation': 'single repository kit publish about to be attempted'}, indent=2) + '\n')
published = call('04-publish', 'publish', ['--confirm-id', str(stage['id'])])
assert published['state'] == 'published' and published['id'] == stage['id']
(PUB / 'ZENODO_TOOL_PUBLICATION_RECEIPT.json').write_text(json.dumps(published, indent=2) + '\n')
verified = call('05-inspect-published', 'inspect', ['--check-doi'])
assert verified['state'] == 'published' and verified['id'] == stage['id']
assert verified['files'] == local['files'] and verified['doi'] == published['doi']
downloads = []
download_error = None
try:
    for row in local['files']:
        url = verified['record_url'] + '/files/' + row['name'] + '?download=1'
        request = urllib.request.Request(url, headers={'User-Agent': 'Math-Research-Publication-Verification/1.0'})
        with urllib.request.urlopen(request, timeout=60) as response:
            raw = response.read()
        assert len(raw) == row['size'] and hashlib.sha256(raw).hexdigest() == row['sha256']
        downloads.append({'file': row['name'], 'bytes': len(raw), 'sha256': row['sha256'], 'actual_public_download_byte_hash_match': True})
except Exception as e:
    download_error = str(e)
receipt = {'utc': datetime.now(timezone.utc).isoformat(), 'submitted': True,
           'metadata_and_files_verified': True, 'id': verified['id'], 'doi': verified['doi'],
           'doi_url': verified['doi_url'], 'record_url': verified['record_url'],
           'metadata': metadata, 'files': local['files'],
           'metadata_normalizations': verified.get('metadata_normalizations', []),
           'doi_resolution': verified.get('doi_resolution'), 'tool_postpublication_readback': verified,
           'additional_actual_public_file_downloads': downloads, 'additional_public_readback_error': download_error,
           'exact_reviewed_frozen_files_published': True, 'single_publish_attempt': True}
(PUB / 'ZENODO_VERIFIED_PUBLICATION.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps({k: v for k, v in receipt.items() if k not in ['metadata', 'tool_postpublication_readback']}, indent=2))
