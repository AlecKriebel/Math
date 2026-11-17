"""One passive rendering invocation of the pinned MW primary, pages 10--19 only."""
import datetime
import hashlib
import json
import subprocess
import sys
from pathlib import Path

BASE = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
OWN = BASE / 'papers/23411227/reviews/mw-input-challenge-sol-20261117'
PDF = BASE / 'papers/23411227/reviews/root-continuation-20261117/primary/MW-arxiv-2401.13999v2.pdf'
raw = PDF.read_bytes()
assert len(raw) == 538390
assert hashlib.sha256(raw).hexdigest() == '85285e55a256fe342d511f716530ed790801d695bdd5f21090ff9d56039b8049'
out = OWN / 'rasters'
out.mkdir(exist_ok=False)
argv = ['/opt/homebrew/bin/pdftoppm', '-f', '10', '-l', '19', '-r', '110', '-png', str(PDF), str(out / 'MW')]
start = datetime.datetime.now(datetime.timezone.utc).isoformat()
result = subprocess.run(argv, capture_output=True)
(OWN / 'RENDER.stdout.txt').write_bytes(result.stdout)
(OWN / 'RENDER.stderr.txt').write_bytes(result.stderr)
files = {p.name: {'bytes': p.stat().st_size, 'SHA256': hashlib.sha256(p.read_bytes()).hexdigest()}
         for p in sorted(out.iterdir()) if p.is_file()}
receipt = {'UTC_start': start, 'UTC_end': datetime.datetime.now(datetime.timezone.utc).isoformat(),
           'argv': argv, 'invocations': 1, 'exit_code': result.returncode, 'rasters': files,
           'stdout_bytes': len(result.stdout), 'stderr_bytes': len(result.stderr),
           'source_pdf_unchanged': PDF.read_bytes() == raw, 'scientific_executions': 0}
(OWN / 'RENDER.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps(receipt))
sys.exit(result.returncode)
