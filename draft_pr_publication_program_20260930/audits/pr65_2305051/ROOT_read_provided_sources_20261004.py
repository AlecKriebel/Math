"""ROOT private primary-source rendering and independent provisional reading record."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import subprocess
import sys

if sys.flags.optimize or not __debug__ or not sys.flags.ignore_environment or not sys.flags.dont_write_bytecode:
    raise RuntimeError('Invoke -E -B without optimization')
A = Path(__file__).resolve().parent
D = Path('/Users/alec/.cache/codex-pr65-priority-20261004/provided_primary_sources_20261004')
F = A / 'ROOT_provided_source_reading_20261004'
F.mkdir(exist_ok=False)
V = D / 'ROOT_private_rendered_pages'
V.mkdir(exist_ok=False)
intake = json.loads((A / 'provided_primary_sources_20261004/INTAKE.json').read_bytes())
sources = intake['sources']
for row in sources:
    body = Path(row['private_frozen_copy']).read_bytes()
    if hashlib.sha256(body).hexdigest() != row['PDF_sha256']:
        raise RuntimeError('Source drift')
first = '''# ROOT independent provided-source first conclusion

The complete extracted Piranian1966 and Duren–Shapiro–Shields1966 bodies and complete HL2019 printed121–122 update were read. Scanned equations still require pixel verification. The three new family first-conclusion messages have arrived, but their complete reports have not been read. This is ROOT's independent provisional reading, not a claim of complete book reading or final priority clearance.

Piranian printed260–261 supplies Kahane's fixed absorbed four-adic (M−1,M+1,M+1,M−1) recursion and excludes finite nonzero ordinary derivatives at every point. The earlier1966 attribution must replace any assertion that the mechanism first appears in1969. DSS printed248–250 connects the affine-periodic primitive to the Herglotz Bloch derivative. Neither of these two complete texts prints Holland's normalized pure-Blaschke Cayley target; their adapter is a deduction, not evidence that the whole statement was previously printed.

HL2019 printed121–122 explicitly calls AAN1999's inner construction explicit. It therefore supersedes the no-progress wording of the retained2018v2; adjacent no-progress wording for5.52 must not be assigned to5.51. AAN1999 Theorem2 printed320,326–327 supplies an interpolating pure Blaschke universal covering of a punctured disc whose omitted set avoids0. Its derivative estimate with a quadratic weight makes the Cayley transform Bloch; because0 is in the image, precomposing a disc automorphism makes B(0)=0 and preserves purity and Bloch control. This exact normalization deduction must be fully checked on primary pixels before final adjudication. A general covering recipe can meet the published historical explicitness standard even without today's finite algebraic recursion. Strong evidence of an already available full historical resolution; no new-solution publication is warranted on a narrower invented definition of explicitness.

No Git/native/PR/publication/tracker/editor mutation. Original proof turns2/5 unchanged. Full primary sources and rendered pixels remain private.
'''
stamp = dt.datetime.now(dt.timezone.utc).isoformat()
(F / 'FIRST_CONCLUSION.md').write_text(first)
(F / 'FIRST_CONCLUSION.receipt.json').write_text(json.dumps({'UTC': stamp, 'actual_controller_pid': os.getpid(), 'sha256': hashlib.sha256((F / 'FIRST_CONCLUSION.md').read_bytes()).hexdigest(), 'scope': 'ROOT provisional primary-text reading; before reading complete new family reports'}, indent=2) + '\n')
processes = []
for name, lo, hi in [('hayman2019.pdf', 5, 5), ('hayman2019.pdf', 127, 128), ('piranian1966.pdf', 1, 8), ('duren1966.pdf', 1, 8)]:
    label = name + '_' + str(lo) + '_' + str(hi)
    argv = ['/opt/homebrew/bin/pdftoppm', '-f', str(lo), '-l', str(hi), '-r', '150', '-png', str(D / name), str(V / label)]
    start = dt.datetime.now(dt.timezone.utc).isoformat()
    child = subprocess.Popen(argv, cwd=V, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = child.communicate()
    (V / (label + '.stdout.bin')).write_bytes(out)
    (V / (label + '.stderr.bin')).write_bytes(err)
    row = {'argv': argv, 'actual_child_pid': child.pid, 'started_utc': start, 'finished_utc': dt.datetime.now(dt.timezone.utc).isoformat(), 'exit_code': child.returncode, 'stdout_bytes': len(out), 'stdout_sha256': hashlib.sha256(out).hexdigest(), 'stderr_bytes': len(err), 'stderr_sha256': hashlib.sha256(err).hexdigest()}
    processes.append(row)
    (F / 'ACTUAL_RENDER_PROCESSES.json').write_text(json.dumps(processes, indent=2) + '\n')
    if child.returncode:
        raise RuntimeError('Primary render failed')
images = [{'private_path': str(p), 'bytes': p.stat().st_size, 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(V.glob('*.png'))]
if len(images) != 19:
    raise RuntimeError('Wrong rendered page count')
(F / 'PRIVATE_RENDER_CUSTODY.json').write_text(json.dumps({'UTC': dt.datetime.now(dt.timezone.utc).isoformat(), 'images': images, 'pixel_inspection_complete': False}, indent=2) + '\n')
print(json.dumps({'status': 'PASS', 'pages_rendered_privately': len(images), 'first_conclusion_saved': True, 'render_processes': processes}, indent=2))
