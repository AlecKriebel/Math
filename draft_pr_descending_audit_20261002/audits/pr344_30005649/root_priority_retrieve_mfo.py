"""Retrieve native primary question chronology and compare the operative text."""
from pathlib import Path
import datetime, hashlib, json, subprocess, sys
A = Path(__file__).resolve().parent
OUT = A / 'root_priority_private/mfo_retrieval001'
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
    assert before == after and proc.returncode == 0
    return proc.stdout
curl = Path('/usr/bin/curl')
pdftotext = Path('/opt/homebrew/bin/pdftotext').resolve()
sources = [('metadata', 'https://publications.mfo.de/handle/mfo/4128?show=full', 'mfo_full_metadata.html'),
           ('pdf', 'https://publications.mfo.de/bitstream/handle/mfo/4128/OWR_2023_42.pdf?isAllowed=y&sequence=4', 'mfo2023_42.pdf')]
records = {}
for label, url, filename in sources:
    path = OUT / filename
    run(label + '_download', [str(curl), '--fail', '--location', '--silent', '--show-error', '--max-time', '45', '--dump-header', str(OUT / (label + '.headers')), '--output', str(path), url], [curl, Path(__file__)])
    records[label] = {'url': url, 'body': pin(path), 'headers': pin(OUT / (label + '.headers'))}
pdf = OUT / 'mfo2023_42.pdf'
assert pdf.read_bytes().startswith(b'%PDF-')
text = run('extract', [str(pdftotext), '-layout', str(pdf), '-'], [pdf, pdftotext, Path(__file__)])
(OUT / 'mfo2023_42.txt').write_bytes(text)
pages = text.decode().split('\f')
assert len(pages) - 1 == 112
for i in range(99,104):
    (OUT / ('pdf_page_' + str(i+1) + '.txt')).write_text(pages[i])
html = (OUT / 'mfo_full_metadata.html').read_text()
assert 'dc.date.accessioned' in html and 'dc.date.available' in html
assert '2024-03-15T11:42:57Z' in html
assert program == pin(Path(__file__))
rec = {'utc': now(), 'status': 'MFO_NATIVE_METADATA_AND_QUESTION_SOURCE_RETRIEVED',
       'sources': records, 'whole_layout_text': pin(OUT / 'mfo2023_42.txt'),
       'operative_pages_extracted': {str(i): pin(OUT / ('pdf_page_' + str(i) + '.txt')) for i in range(100,105)},
       'observed_accession_and_available_fields': '2024-03-15T11:42:57Z',
       'program': program, 'interpreter': sys.executable, 'version': sys.version,
       'limits': 'Retrieval is not mathematical reading; timestamp fields establish repository metadata, not the earliest possible public circulation.'}
(OUT / 'RETRIEVAL_RECEIPT.json').write_text(json.dumps(rec, indent=2) + '\n')
print(json.dumps(rec, indent=2))
