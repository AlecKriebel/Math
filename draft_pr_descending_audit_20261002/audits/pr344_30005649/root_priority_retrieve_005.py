"""One-shot native retrieval of the supersingular truncation primary lead."""
from pathlib import Path
import datetime, hashlib, json, subprocess, sys
A = Path(__file__).resolve().parent
OUT = A / 'root_priority_private/primary_retrieval005'
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
url = 'https://arxiv.org/pdf/math/0606777v2'
pdf = OUT / 'nicole_vasiu2007v2.pdf'
headers = OUT / 'nicole_vasiu2007v2.headers'
run('download', [str(curl), '--fail', '--location', '--silent', '--show-error', '--max-time', '45', '--dump-header', str(headers), '--output', str(pdf), url], [curl, Path(__file__)])
assert pdf.read_bytes().startswith(b'%PDF-')
text = run('extract', [str(pdftotext), '-layout', str(pdf), '-'], [pdf, pdftotext, Path(__file__)])
(OUT / 'nicole_vasiu2007v2.txt').write_bytes(text)
assert program == pin(Path(__file__))
rec = {'utc': now(), 'status': 'SUPERSINGULAR_TRUNCATION_PRIMARY_VERSION_RETRIEVED_NOT_YET_READ',
       'url': url, 'pdf': pin(pdf), 'whole_native_layout_text': pin(OUT / 'nicole_vasiu2007v2.txt'),
       'headers': pin(headers), 'program': program, 'interpreter': sys.executable, 'version': sys.version,
       'limits': 'ArXivv2 is a primary author version. Equality to the final2007 journal article has not been established; retrieval does not certify mathematical reading or prior exact counterexample.'}
(OUT / 'RETRIEVAL_RECEIPT.json').write_text(json.dumps(rec, indent=2) + '\n')
print(json.dumps(rec, indent=2))
