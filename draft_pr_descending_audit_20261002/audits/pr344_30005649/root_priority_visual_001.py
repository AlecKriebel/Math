"""Native private page rendering; does not certify visual reading."""
from pathlib import Path
import datetime, hashlib, json, subprocess
A = Path(__file__).resolve().parent
OUT = A / 'root_priority_private/primary_visual001'
SRC = A / 'root_priority_private/primary_retrieval001'
ENV = {'PATH': '/opt/homebrew/bin:/usr/bin:/bin', 'LANG': 'C', 'LC_ALL': 'C', 'TZ': 'UTC', 'PYTHONDONTWRITEBYTECODE': '1', 'PYTHONHASHSEED': '0'}
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def pin(p):
    b = p.read_bytes()
    return {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest(), 'mode': p.stat().st_mode & 0o7777}
assert not OUT.exists()
OUT.mkdir()
program = pin(Path(__file__))
binary = Path('/opt/homebrew/bin/pdftoppm').resolve()
results = []
for label, page in [('pries_ulmer_2021', 6), ('pries_ulmer_2021', 7), ('pries_ulmer_2021', 13), ('pries_ulmer_2021', 14), ('hoshi_ramification_2026', 3)]:
    pdf = SRC / (label + '.pdf')
    key = label + '_pdfpage' + str(page)
    before = {str(p): pin(p) for p in [pdf, binary, Path(__file__)]}
    argv = [str(binary), '-f', str(page), '-l', str(page), '-r', '135', '-png', '-singlefile', str(pdf), str(OUT / key)]
    pre = {'utc': now(), 'argv': argv, 'cwd': str(A), 'environment_exact': ENV, 'inputs_before': before}
    (OUT / (key + '.preexecution.json')).write_text(json.dumps(pre, indent=2) + '\n')
    proc = subprocess.run(argv, cwd=A, env=ENV, capture_output=True)
    (OUT / (key + '.stdout')).write_bytes(proc.stdout)
    (OUT / (key + '.stderr')).write_bytes(proc.stderr)
    after = {str(p): pin(p) for p in [pdf, binary, Path(__file__)]}
    rec = dict(pre, completed_utc=now(), exit_status=proc.returncode, stdout=pin(OUT / (key + '.stdout')), stderr=pin(OUT / (key + '.stderr')), inputs_after=after, inputs_stable=before == after)
    (OUT / (key + '.json')).write_text(json.dumps(rec, indent=2) + '\n')
    assert proc.returncode == 0 and before == after
    png = OUT / (key + '.png')
    results.append({'image': str(png), **pin(png), 'receipt': pin(OUT / (key + '.json'))})
assert program == pin(Path(__file__))
rec = {'utc': now(), 'status': 'FIVE_OPERATIVE_PRIMARY_PAGES_NATIVE_RENDERED_NOT_YET_VISUALLY_READ', 'results': results, 'program': program}
(OUT / 'RENDER_RECEIPT.json').write_text(json.dumps(rec, indent=2) + '\n')
print(json.dumps(rec, indent=2))
