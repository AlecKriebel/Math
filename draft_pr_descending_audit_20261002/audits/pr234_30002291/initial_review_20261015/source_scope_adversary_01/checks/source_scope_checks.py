"""Read-only reproducible provenance and exact scope-anchor checks.

This script does not certify a proof or novelty. Whole primary texts remain
private; its output contains only hashes, page counts and factual booleans.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import re
import subprocess
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
manifest = json.loads((ROOT / 'SOURCE_MANIFEST.json').read_text())
results = []

def check(name, passed, **details):
    results.append(dict(name=name, passed=bool(passed), **details))

def clean(text):
    text = unicodedata.normalize('NFKD', text)
    text = ''.join(c for c in text if not unicodedata.combining(c))
    return ' '.join(text.split())

expected_pages = [38, 36, 53]
for row, pages in zip(manifest['sources'], expected_pages):
    file = ROOT / row['file']
    data = file.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    check('independent_source_hash:' + file.name,
          digest == row['sha256'] and data.startswith(b'%PDF'),
          sha256=digest, bytes=len(data))
    info = subprocess.check_output(['pdfinfo', str(file)], text=True)
    actual_pages = int(re.search(r'^Pages:\s+(\d+)', info, re.M).group(1))
    check('pdf_page_count:' + file.name, actual_pages == pages, pages=actual_pages)

for row in manifest['candidate_inputs']:
    data = Path(row['file']).read_bytes()
    check('frozen_input_unchanged:' + Path(row['file']).name,
          hashlib.sha256(data).hexdigest() == row['sha256'], sha256=row['sha256'])

texts = [clean((ROOT / 'private_reading' / f).read_text()) for f in [
    'owr_2013_09.txt',
    'basse_heinrich_podolskij_1604_02307v2.txt',
    'basse_lachieze_podolskij_1506_06679.txt']]
check('owr_open_ended_request_anchor',
      'pure jump semimartingale driver (given sufficient conditions)' in texts[0])
check('owr_compound_poisson_anchor',
      'Assume that L is a compound Poisson process' in texts[0])
check('bhp_ambient_filtered_model_anchor',
      'filtered probability space' in texts[1] and 'without a Gaussian component' in texts[1])
check('bhp_cadlag_volatility_anchor',
      'cadlag process adapted' in texts[1])
check('bhp_m1_and_j1_warning_anchors',
      'M1' in texts[1] and 'J1' in texts[1] and 'Remark 1.4' in texts[1])
check('blp_original_sigma_field_stability_definition',
      'for all F-measurable random variables U' in texts[2])
check('private_sources_excluded',
      'private_reading/' in (ROOT / '.gitignore').read_text().splitlines())
for name, files in [
    ('owr_controlling_pages', ['owr-09.png', 'owr-10.png', 'owr-11.png']),
    ('bhp_controlling_pages', [f'bhp-{i:02d}.png' for i in range(2, 7)]),
    ('blp_controlling_pages', [f'blp-{i:02d}.png' for i in range(2, 5)])]:
    check('visual_render_artifacts:' + name,
          all((ROOT / 'private_reading' / f).is_file() for f in files), pages=files)

out = dict(checked_utc=datetime.now(timezone.utc).isoformat(),
           purpose='provenance and source-scope anchors only; no mathematical or novelty certification',
           all_passed=all(r['passed'] for r in results), checks=results)
(ROOT / 'checks' / 'PROVENANCE_CHECKS.json').write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps(out, indent=2))
raise SystemExit(0 if out['all_passed'] else 1)
