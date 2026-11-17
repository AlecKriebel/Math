"""Fresh source-only PDF reader. No native program/import or mathematical computation."""
import datetime
import hashlib
import json
import subprocess
import sys
from pathlib import Path

BASE = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
OWN = BASE / 'papers/23204810/reviews/scope-sol/INITIAL'
PDF = BASE / 'papers/23204810/sources/zenodo-files/paper.pdf'
raw = PDF.read_bytes()
assert len(raw) == 73479
assert hashlib.sha256(raw).hexdigest() == 'ae0526dfe7442b63e9c3f4754c324970b0d4e8ccd15d85b6f9585ed3ee45a119'
OUT = OWN / 'pdf-pages'
OUT.mkdir(exist_ok=False)
records = []
commands = [
    ('text', ['/opt/homebrew/bin/pdftotext', '-layout', str(PDF), str(OWN / 'native-paper.txt')]),
    ('rasters', ['/opt/homebrew/bin/pdftoppm', '-f', '1', '-l', '5', '-r', '110', '-png', str(PDF), str(OUT / 'page')])]
for route, argv in commands:
    start = datetime.datetime.now(datetime.timezone.utc).isoformat()
    result = subprocess.run(argv, capture_output=True)
    (OWN / (route + '.stdout.txt')).write_bytes(result.stdout)
    (OWN / (route + '.stderr.txt')).write_bytes(result.stderr)
    records.append({'route': route, 'UTC_start': start,
                    'UTC_end': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    'argv': argv, 'exit_code': result.returncode,
                    'stdout_bytes': len(result.stdout), 'stderr_bytes': len(result.stderr)})
    (OWN / 'PDF_READER_EXECUTION.json').write_text(json.dumps(records, indent=2) + '\n')
    if result.returncode:
        sys.exit(result.returncode)
pages = (OWN / 'native-paper.txt').read_text().split('\f')
if not pages[-1].strip():
    pages.pop()
assert len(pages) == 5
for number, content in enumerate(pages, 1):
    (OUT / ('page-' + str(number) + '.txt')).write_text(content)
assert len(list(OUT.glob('*.png'))) == 5
assert PDF.read_bytes() == raw
files = {p.relative_to(OWN).as_posix(): {'bytes': p.stat().st_size,
         'SHA256': hashlib.sha256(p.read_bytes()).hexdigest()}
         for p in sorted(OUT.iterdir()) if p.is_file()}
receipt = {'UTC': datetime.datetime.now(datetime.timezone.utc).isoformat(),
           'reader_script_invocations': 1, 'native_PDF_unchanged': True,
           'PDF_bytes': len(raw), 'PDF_SHA256': hashlib.sha256(raw).hexdigest(),
           'fresh_text_pages': 5, 'fresh_rasters': 5, 'files': files,
           'scientific_source_old_helper_executions': 0, 'routes': records}
(OWN / 'PDF_READING.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps(receipt))
