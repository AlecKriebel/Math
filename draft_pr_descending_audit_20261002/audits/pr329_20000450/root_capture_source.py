"""Capture the original source before analytically opening the submitted work."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, subprocess, urllib.request

A = Path(__file__).resolve().parent
P = A.parents[1]
R = P.parent
D = A / 'root_sources_private/source001'
D.mkdir(parents=True, exist_ok=False)
utc = lambda: datetime.now(timezone.utc).isoformat()
sha = lambda b: hashlib.sha256(b).hexdigest()
url = 'https://aimath.org/WWN/qptsurface2/qptsurface2.pdf'
start = utc()
with urllib.request.urlopen(url, timeout=45) as response:
    raw = response.read()
    record = {'url': url, 'resolved_url': response.url,
              'response_status': response.status, 'started_utc': start,
              'finished_utc': utc(), 'headers': dict(response.headers)}
assert raw.startswith(b'%PDF-')
pdf = D / 'qptsurface2.pdf'
pdf.write_bytes(raw)
record.update(bytes=len(raw), sha256=sha(raw), local_path=str(pdf))
(D / 'download.json').write_text(json.dumps(record, indent=2) + '\n')
from pypdf import PdfReader
reader = PdfReader(pdf)
assert len(reader.pages) == 59
selected = [0, 49, 50, 51]
for index in selected:
    body = reader.pages[index].extract_text()
    (D / f'page_{index + 1:02}.txt').write_text(body + '\n')
assert 'Problem/Question 17' in (D / 'page_51.txt').read_text()
r = subprocess.run(['pdftoppm', '-f', '51', '-l', '51', '-scale-to', '2000', '-png', str(pdf), str(D / 'operative')], capture_output=True)
(D / 'render.stdout.bin').write_bytes(r.stdout)
(D / 'render.stderr.bin').write_bytes(r.stderr)
record['render_exit_code'] = r.returncode
record['source_reading_scope'] = 'Full operative Question17 and all four remarks on physical PDF page51; title/version page1 and adjacent contextual pages50/52. Full59-page source retained; unrelated lecture notes not claimed fully read.'
record['candidate_mathematical_content_opened'] = False
(A / 'ROOT_SOURCE_CAPTURE.json').write_text(json.dumps(record, indent=2) + '\n')
(A / 'RESEARCH_LOG.md').write_text('# PR329 / 20000450 audit\n\n'
    + utc() + ' — Began source-first audit of submitted claimed_solved head96395a4f506af6a6045e3cd59afcba2db6b7e2e7, original1/5 turns. Main/index untouched. Exact original claim remains a hypothesis; workflow5%, mathematical verification0%. Original source downloaded and operative question extracted before candidate prose or inherited reviews are opened.\n')
status = json.loads((P / 'SHARED_GIT_WINDOW_STATUS.json').read_text())
status.update(utc=utc(), descending_active_pr=329, descending_329_workflow_percent=5,
    descending_329_mathematical_verification_percent=0,
    descending_checkpoint_scope='PR329 source-first mathematical audit only; no shared Git mutation or publication clearance.')
(P / 'SHARED_GIT_WINDOW_STATUS.json').write_text(json.dumps(status, indent=2) + '\n')
print(json.dumps({'source': record, 'selected_text_files': [str(D / f'page_{i+1:02}.txt') for i in selected]}, indent=2))
