#!/usr/bin/env python3
"""Build the standalone note in a clean project-local temporary directory."""
from pathlib import Path
import hashlib, json, shutil, subprocess, sys, tempfile

project = Path(__file__).resolve().parents[1]
work_root = project/'verification/clean_reproduction'
work_root.mkdir(parents=True, exist_ok=True)
(project/'receipts').mkdir(parents=True, exist_ok=True)
work = Path(tempfile.mkdtemp(prefix='note-', dir=work_root))
shutil.copy2(project/'main.tex', work/'main.tex')
checks = {}
for name in ('verify.py','verify_parameter.py','verify_plane32.py','verify_embedding.py'):
    output = subprocess.run([sys.executable, str(project/'verification'/name)], check=True, text=True, capture_output=True)
    checks[name] = json.loads(output.stdout)
engine = shutil.which('tectonic')
if not engine:
    raise SystemExit('The exported-PDF reproduction needs Tectonic; the native editor compiler is independent of this.')
version = subprocess.check_output([engine,'--version'],text=True).strip()
build = subprocess.run([engine,'main.tex','--keep-logs'],cwd=work,text=True,capture_output=True)
(work/'build.stdout.txt').write_text(build.stdout)
(work/'build.stderr.txt').write_text(build.stderr)
if build.returncode:
    raise SystemExit(build.stderr)
text = subprocess.check_output(['pdftotext',str(work/'main.pdf'),'-'],text=True)
assert '??' not in text
assert 'Alec Kriebel' in text and 'projective' in text and 'cancellation' in text
assert all(token in text for token in ('532','987','503','two-generator','spectral'))
info = subprocess.check_output(['pdfinfo',str(work/'main.pdf')],text=True)
fonts = subprocess.check_output(['pdffonts',str(work/'main.pdf')],text=True)
(work/'pdfinfo.txt').write_text(info)
(work/'pdffonts.txt').write_text(fonts)
shutil.copy2(work/'main.pdf',project/'paper.pdf')
result = {'status':'passed','python':sys.version,'tectonic':version,'clean_directory':str(work.relative_to(project)),'source_sha256':hashlib.sha256((project/'main.tex').read_bytes()).hexdigest(),'pdf_sha256':hashlib.sha256((project/'paper.pdf').read_bytes()).hexdigest(),'checks':checks,'pdf_info':info,'fonts':fonts,'limits':'Compilation and finite supplemental checks do not prove the group existence theorem; see source audits. PDF timestamps may vary across builds.'}
(project/'receipts/clean_reproduction.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('pdf_info','fonts')},indent=2))
