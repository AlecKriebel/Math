from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, subprocess
from pypdf import PdfReader
A = Path(__file__).resolve().parent
P = A.parents[1]
D = A / 'root_sources_private/access002'
pdf = D / 'candidate_0.pdf'
sha = lambda b: hashlib.sha256(b).hexdigest()
utc = lambda: datetime.now(timezone.utc).isoformat()
reader = PdfReader(pdf)
assert len(reader.pages) == 59
for i in [0, 49, 50, 51]:
    (D / f'page_{i+1:02}.txt').write_text(reader.pages[i].extract_text() + '\n')
assert 'Problem/Question 17' in (D / 'page_51.txt').read_text()
args = ['pdftoppm', '-f', '51', '-l', '51', '-scale-to', '2000', '-png', str(pdf), str(D / 'operative')]
start = utc()
r = subprocess.run(args, capture_output=True)
for k,b in [('stdout', r.stdout), ('stderr', r.stderr)]:
    (D / f'render.{k}.bin').write_bytes(b)
record = {'utc': utc(), 'source_url': 'https://aimath.org/WWN/qptsurface2/qptsurface2.pdf',
    'resolved_url': 'https://www.aimath.org/WWN/qptsurface2/qptsurface2.pdf',
    'PDF_bytes': len(pdf.read_bytes()), 'PDF_sha256': sha(pdf.read_bytes()), 'pages': 59,
    'original_version': 'Mon Nov22 11:41:01 2004', 'operative_location': 'Question17, printed51/physical PDF51, all four remarks',
    'candidate_mathematical_content_opened': False,
    'access_history': 'First urllib request to bare domain failedHTTP403 before any PDF capture; retained empty source001 namespace. Native captured curl request to www host succeeds200 at08:33:50.786151UTC. No outreach.',
    'render': {'argv': args, 'started_utc': start, 'finished_utc': utc(), 'exit_code': r.returncode,
        'stderr_sha256': sha(r.stderr), 'stdout_sha256': sha(r.stdout)},
    'reading_scope': 'Full operative Question17 and all four remarks; title/version page1 and adjacent contextual pages50/52 retained. Unrelated lecture notes not represented as fully read.',
    'local_primary_body_path': str(pdf), 'public_redistribution_intended': False}
(A / 'ROOT_SOURCE_CAPTURE.json').write_text(json.dumps(record, indent=2) + '\n')
(A / 'RESEARCH_LOG.md').write_text('# PR329 / 20000450 audit\n\n' + utc()
    + ' — Source-first intake: source downloaded200,59 pages, operative Question17/allremarks captured before opening candidate prose/inherited reviews. First bare-host urllib403 retained as access failure. Original claimed_solved is a hypothesis; original1/5 turns preserved; workflow5%, mathematical verification0%. No shared Git mutation.\n')
status = json.loads((P / 'SHARED_GIT_WINDOW_STATUS.json').read_text())
status.update(utc=utc(), descending_active_pr=329, descending_329_workflow_percent=5,
    descending_329_mathematical_verification_percent=0,
    descending_checkpoint_scope='PR329 source-first mathematical audit only; no shared Git mutation or publication clearance.')
(P / 'SHARED_GIT_WINDOW_STATUS.json').write_text(json.dumps(status, indent=2) + '\n')
print(json.dumps(record, indent=2))
print((D / 'page_01.txt').read_text())
print((D / 'page_51.txt').read_text())
