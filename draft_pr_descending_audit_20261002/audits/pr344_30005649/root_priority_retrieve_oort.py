"""Private primary author PostScript retrieval and native safe conversion."""
from pathlib import Path
import datetime, hashlib, json, subprocess, sys
A = Path(__file__).resolve().parent
OUT = A / 'root_priority_private/oort_retrieval001'
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
    assert proc.returncode == 0 and before == after
    return proc.stdout
curl = Path('/usr/bin/curl')
gs = Path('/opt/homebrew/bin/gs').resolve()
pdftotext = Path('/opt/homebrew/bin/pdftotext').resolve()
run('gs_version', [str(gs), '--version'], [gs, Path(__file__)])
url = 'https://webspace.science.uu.nl/~oort0109/A-EO5.Strat.ps'
ps = OUT / 'oort_stratification_author.ps'
headers = OUT / 'oort_stratification_author.headers'
run('download', [str(curl), '--fail', '--location', '--silent', '--show-error', '--max-time', '45', '--dump-header', str(headers), '--output', str(ps), url], [curl, Path(__file__)])
assert ps.read_bytes().startswith(b'%!PS')
pdf = OUT / 'oort_stratification_author_converted.pdf'
run('convert', [str(gs), '-q', '-dSAFER', '-dBATCH', '-dNOPAUSE', '-sDEVICE=pdfwrite', '-sOutputFile=' + str(pdf), str(ps)], [ps, gs, Path(__file__)])
assert pdf.read_bytes().startswith(b'%PDF-')
data = run('extract', [str(pdftotext), '-layout', str(pdf), '-'], [pdf, pdftotext, Path(__file__)])
text = OUT / 'oort_stratification_author.txt'
text.write_bytes(data)
assert program == pin(Path(__file__))
rec = {'utc': now(), 'status': 'PRIMARY_AUTHOR_POSTSCRIPT_RETRIEVED_CONVERTED_EXTRACTED_NOT_YET_READ', 'url': url, 'author_postscript': pin(ps), 'native_converted_pdf': pin(pdf), 'whole_native_layout_text': pin(text), 'headers': pin(headers), 'program': program, 'interpreter': sys.executable, 'version': sys.version, 'version_limit': 'Author-site preprint bytes; equality to final 2001 journal/chapter version not established.'}
(OUT / 'RETRIEVAL_RECEIPT.json').write_text(json.dumps(rec, indent=2) + '\n')
print(json.dumps(rec, indent=2))
