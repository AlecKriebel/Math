"""Native bounded priority retrieval; retain failures and continue independent leads."""
from pathlib import Path
import datetime, hashlib, json, subprocess, sys
A = Path(__file__).resolve().parent
OUT = A / 'root_priority_private/primary_retrieval003'
ENV = {'PATH': '/opt/homebrew/bin:/usr/bin:/bin', 'LANG': 'C', 'LC_ALL': 'C', 'TZ': 'UTC', 'PYTHONDONTWRITEBYTECODE': '1', 'PYTHONHASHSEED': '0'}
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def pin(p):
    b = p.read_bytes()
    return {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest(), 'mode': p.stat().st_mode & 0o7777}
assert not OUT.exists()
OUT.mkdir()
program = pin(Path(__file__))
def run(label, argv, inputs):
    before = {str(p): pin(p) for p in inputs}
    pre = {'utc': now(), 'argv': argv, 'cwd': str(A), 'environment_exact': ENV, 'program': program, 'inputs_before': before}
    (OUT / (label + '.preexecution.json')).write_text(json.dumps(pre, indent=2) + '\n')
    proc = subprocess.run(argv, cwd=A, env=ENV, capture_output=True)
    (OUT / (label + '.stdout')).write_bytes(proc.stdout)
    (OUT / (label + '.stderr')).write_bytes(proc.stderr)
    after = {str(p): pin(p) for p in inputs}
    rec = dict(pre, completed_utc=now(), exit_status=proc.returncode, stdout=pin(OUT / (label + '.stdout')), stderr=pin(OUT / (label + '.stderr')), inputs_after=after, inputs_stable=before == after)
    (OUT / (label + '.json')).write_text(json.dumps(rec, indent=2) + '\n')
    assert before == after
    return proc
curl = Path('/usr/bin/curl')
pdftotext = Path('/opt/homebrew/bin/pdftotext').resolve()
sources = [
    ('kraft_1975_host_alias', 'https://www.math.upenn.edu/~chai/kraft_omm_alg_p-gruppen_sep1975.pdf'),
    ('chai_kraft_2025_host_alias', 'https://www.math.upenn.edu/~chai/papers_pdf/kraft_v1.pdf'),
    ('muller_yu_2026_v2', 'https://arxiv.org/pdf/2603.12116v2'),
]
results = []
for label, url in sources:
    pdf = OUT / (label + '.pdf')
    headers = OUT / (label + '.headers')
    proc = run(label + '_download', [str(curl), '--fail', '--location', '--silent', '--show-error', '--max-time', '45', '--dump-header', str(headers), '--output', str(pdf), url], [curl, Path(__file__)])
    row = {'label': label, 'url': url, 'download_exit_status': proc.returncode, 'download_receipt': pin(OUT / (label + '_download.json')), 'header_present': headers.exists()}
    if headers.exists(): row['headers'] = pin(headers)
    if proc.returncode or not pdf.exists() or not pdf.read_bytes().startswith(b'%PDF-'):
        row['status'] = 'NOT_RETRIEVED_AS_VERIFIED_PDF'
        results.append(row)
        continue
    proc = run(label + '_extract', [str(pdftotext), '-layout', str(pdf), '-'], [pdf, pdftotext, Path(__file__)])
    row['pdf'] = pin(pdf)
    row['extraction_exit_status'] = proc.returncode
    if proc.returncode:
        row['status'] = 'PDF_RETRIEVED_EXTRACTION_FAILED'
    else:
        text = OUT / (label + '.txt')
        text.write_bytes(proc.stdout)
        row.update(status='PRIMARY_PDF_RETRIEVED_AND_EXTRACTED_NOT_YET_READ', whole_native_layout_text=pin(text), extraction_receipt=pin(OUT / (label + '_extract.json')))
    results.append(row)
assert program == pin(Path(__file__))
rec = {'utc': now(), 'status': 'THREE_BOUNDED_PRIMARY_LEADS_ACTUALLY_ATTEMPTED', 'results': results, 'program': program, 'interpreter': sys.executable, 'version': sys.version, 'reading_scope': 'No mathematical reading certified by retrieval; hostname-alias equivalence and versions require subsequent comparison.'}
(OUT / 'RETRIEVAL_RECEIPT.json').write_text(json.dumps(rec, indent=2) + '\n')
print(json.dumps(rec, indent=2))
