"""Fetch primary sources independently before reading the candidate proof or code."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, subprocess, urllib.request
A = Path(__file__).resolve().parent
D = A / 'root_primary_private'
D.mkdir(exist_ok=True)
M = A / 'snapshot/unsolved_math_prioritization/attempts/30004048/SOURCE_MANIFEST.json'
receipts = []
for e in json.loads(M.read_text())['sources']:
    start = datetime.now(timezone.utc).isoformat()
    with urllib.request.urlopen(e['url'], timeout=60) as response:
        b = response.read()
        resolved = response.url
        headers = dict(response.headers.items())
    end = datetime.now(timezone.utc).isoformat()
    p = D / e['file']
    p.write_bytes(b)
    assert len(b) == e['bytes'] and hashlib.sha256(b).hexdigest() == e['sha256']
    cmd = ['pdftotext', '-layout', str(p), str(p.with_suffix('.txt'))]
    z = subprocess.run(cmd, capture_output=True)
    (D / (p.stem + '.extract.stdout')).write_bytes(z.stdout)
    (D / (p.stem + '.extract.stderr')).write_bytes(z.stderr)
    assert z.returncode == 0 and not z.stderr
    receipts.append({**e, 'requested_url': e['url'], 'resolved_url': resolved,
        'start_utc': start, 'end_utc': end, 'response_headers': headers,
        'pdf_path': str(p), 'text_sha256': hashlib.sha256(p.with_suffix('.txt').read_bytes()).hexdigest(),
        'extraction_argv': cmd, 'extraction_exit': z.returncode,
        'extraction_stdout_bytes': len(z.stdout), 'extraction_stderr_bytes': len(z.stderr)})
(A / 'ROOT_PRIMARY_RECEIPTS.json').write_text(json.dumps({
    'utc': datetime.now(timezone.utc).isoformat(),
    'candidate_proof_code_historical_reviews_not_read': True,
    'routing_exposure': 'Original title, filenames, SOURCE_MANIFEST, and queue row containing proposed pair13/27,14/27 and gap1/108. No candidate proof/code/history read. Sibling source-first preliminary messages arrived and are separately disclosed in the root analytical baseline.',
    'sources': receipts}, indent=2) + '\n')
print(json.dumps({'status': 'THREE_COMPLETE_PRIMARY_DOWNLOADS_EXACT',
    'sources': [{k: e[k] for k in ('file', 'bytes', 'sha256')} for e in receipts]}, indent=2))
