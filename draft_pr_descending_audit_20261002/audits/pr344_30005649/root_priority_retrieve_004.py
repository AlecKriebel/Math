"""One-shot primary retrieval of the exact-word historical filtration lead."""
from pathlib import Path
import datetime, hashlib, json, subprocess, sys
A = Path(__file__).resolve().parent
OUT = A / 'root_priority_private/primary_retrieval004'
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
url = 'https://www2.math.upenn.edu/~chai/HObook/current/draft_versions/driver_HObook_20july2020.pdf'
pdf = OUT / 'chai_oort_2020.pdf'
headers = OUT / 'chai_oort_2020.headers'
proc = run('download', [str(curl), '--fail', '--location', '--silent', '--show-error', '--max-time', '45', '--dump-header', str(headers), '--output', str(pdf), url], [curl, Path(__file__)])
result = {'url': url, 'download_exit_status': proc.returncode, 'download_receipt': pin(OUT / 'download.json')}
if headers.exists(): result['headers'] = pin(headers)
if proc.returncode or not pdf.exists() or not pdf.read_bytes().startswith(b'%PDF-'):
    result['status'] = 'NOT_RETRIEVED_AS_VERIFIED_PDF'
else:
    proc = run('extract', [str(pdftotext), '-layout', str(pdf), '-'], [pdf, pdftotext, Path(__file__)])
    result['pdf'] = pin(pdf)
    result['extraction_exit_status'] = proc.returncode
    if proc.returncode:
        result['status'] = 'PDF_RETRIEVED_EXTRACTION_FAILED'
    else:
        text = OUT / 'chai_oort_2020.txt'
        text.write_bytes(proc.stdout)
        result.update(status='PRIMARY_PDF_RETRIEVED_AND_EXTRACTED_NOT_YET_READ', whole_native_layout_text=pin(text), extraction_receipt=pin(OUT / 'extract.json'))
assert program == pin(Path(__file__))
rec = {'utc': now(), 'status': 'EXACT_WORD_FILTRATION_LEAD_ACTUALLY_ATTEMPTED', 'result': result, 'program': program, 'interpreter': sys.executable, 'version': sys.version, 'reading_scope': 'Retrieval certifies no mathematical reading and establishes no prior resolution.'}
(OUT / 'RETRIEVAL_RECEIPT.json').write_text(json.dumps(rec, indent=2) + '\n')
print(json.dumps(rec, indent=2))
