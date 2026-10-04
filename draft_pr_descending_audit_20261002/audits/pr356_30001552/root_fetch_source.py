"""Cache the official original report and extract the exact source section."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, subprocess
A = Path(__file__).resolve().parent
D = A / 'root_sources_private'
sha = lambda b: hashlib.sha256(b).hexdigest()
utc = lambda: datetime.now(timezone.utc).isoformat()
url = 'https://ems.press/content/serial-article-files/46296'
pdf = D / 'owr2010-37.pdf'
assert not pdf.exists()
args = ['curl', '--fail', '--silent', '--show-error', '--location', '--max-time', '60', url]
start = utc()
r = subprocess.run(args, capture_output=True)
pdf.write_bytes(r.stdout)
(D / 'fetch.stderr').write_bytes(r.stderr)
rec = {'argv': args, 'started_utc': start, 'completed_utc': utc(), 'exit_code': r.returncode,
       'stdout_bytes': len(r.stdout), 'stdout_sha256': sha(r.stdout),
       'stderr_bytes': len(r.stderr), 'stderr_sha256': sha(r.stderr)}
(D / 'fetch.json').write_text(json.dumps(rec, indent=2) + '\n')
assert r.returncode == 0 and r.stdout.startswith(b'%PDF-') and not r.stderr
commands = [['pdfinfo', str(pdf)], ['pdftotext', '-layout', str(pdf), str(D / 'owr2010-37-full.txt')],
            ['pdftotext', '-f', '25', '-l', '28', '-layout', str(pdf), str(D / 'word-periods-under-involution.txt')],
            ['pdftoppm', '-f', '25', '-l', '28', '-scale-to', '1600', '-png', '-singlefile', str(pdf), str(D / 'source-start-page')]]
for i, args in enumerate(commands):
    start = utc()
    r = subprocess.run(args, capture_output=True)
    for name, b in [('stdout', r.stdout), ('stderr', r.stderr)]:
        (D / (str(i) + '.' + name)).write_bytes(b)
    rec = {'argv': args, 'started_utc': start, 'completed_utc': utc(), 'exit_code': r.returncode,
           'stdout_bytes': len(r.stdout), 'stdout_sha256': sha(r.stdout),
           'stderr_bytes': len(r.stderr), 'stderr_sha256': sha(r.stderr)}
    (D / (str(i) + '.json')).write_text(json.dumps(rec, indent=2) + '\n')
    assert r.returncode == 0
(A / 'ROOT_PRIMARY_SOURCE_IDENTITY.json').write_text(json.dumps({'utc': utc(), 'url': url,
    'pdf_path': str(pdf), 'bytes': pdf.stat().st_size, 'sha256': sha(pdf.read_bytes()),
    'source_title': 'Word periods under involution', 'author': 'Dirk Nowotka',
    'joint_work_with': 'Bastian Bischoff', 'printed_pages': [2219, 2220, 2221, 2222],
    'pdf_one_based_pages': [25, 26, 27, 28], 'original_conjecture_page': 2220,
    'source_theorem_and_conjecture_still_require_human_reading_by_root': True}, indent=2) + '\n')
print('Official PDF cached and exact source-section text extracted; no theorem verification inferred from extraction')
