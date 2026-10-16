#!/usr/bin/env python3
"""Fetch primary mathematical references transiently and render selected pages."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import sys
from capture import capture

assert __debug__ and sys.flags.optimize == 0
FAMILY = Path(__file__).resolve().parent
AUDIT = FAMILY.parent
TEMP = FAMILY / 'tmp/pdfs'
TEMP.mkdir(parents=True, exist_ok=False)
rows = json.loads((AUDIT / 'source_snapshot/source_checksums.json').read_bytes())
specifications = {
    'K3-book.pdf': [259, 260],
    'owr-2020-8.pdf': [23, 24, 25],
    'bip.pdf': [1, 9, 10, 14, 16, 17, 18, 22],
    'tsuboi-2012-published.pdf': [1, 2, 3],
    'bhw.pdf': [2, 7, 8],
}
bindings = []
for row in rows:
    name = row['cache_filename']
    pdf = TEMP / name
    tag = name.replace('.pdf', '').replace('-', '_')
    fetch = capture('fetch_' + tag, ['curl', '--location', '--fail', '--silent', '--show-error',
                                      row['url'], '--output', str(pdf)], FAMILY)
    body = pdf.read_bytes()
    assert body.startswith(b'%PDF-')
    digest = hashlib.sha256(body).hexdigest()
    info = capture('pdfinfo_' + tag, ['/opt/homebrew/bin/pdfinfo', str(pdf)], FAMILY)
    text_file = TEMP / (name + '.txt')
    text_capture = capture('text_' + tag, ['/opt/homebrew/bin/pdftotext', '-layout', str(pdf), str(text_file)], FAMILY)
    text = text_file.read_bytes()
    assert len(text) > 1000
    renders = []
    for page in specifications[name]:
        prefix = TEMP / (name + '.page%03d' % page)
        cap = capture('render_' + tag + '_%03d' % page,
                      ['/opt/homebrew/bin/pdftoppm', '-f', str(page), '-l', str(page),
                       '-singlefile', '-scale-to', '1800', '-png', str(pdf), str(prefix)], FAMILY)
        image = prefix.with_suffix(prefix.suffix + '.png')
        assert image.exists()
        pixels = image.read_bytes()
        renders.append({'one_based_pdf_page': page, 'path': str(image), 'bytes': len(pixels),
                        'sha256': hashlib.sha256(pixels).hexdigest(), 'capture': cap,
                        'personally_visually_inspected': False})
    bindings.append({'url': row['url'], 'filename': name, 'bytes': len(body), 'sha256': digest,
                     'historical_bytes': row['bytes'], 'historical_sha256': row['sha256'],
                     'fresh_body_matches_historical_hash': digest == row['sha256'] and len(body) == row['bytes'],
                     'full_fresh_body_read': True, 'full_text_read_bytes': len(text),
                     'text_sha256': hashlib.sha256(text).hexdigest(),
                     'fetch_capture': fetch, 'info_capture': info, 'text_capture': text_capture,
                     'selected_page_renders': renders, 'foreign_body_transient_not_for_publication': True})
result = {'schema': 'pr48-algebra-family-fresh-primary-source-bindings/v1', 'actual_pid': os.getpid(),
          'created_utc': datetime.now(timezone.utc).isoformat(), 'sources': bindings,
          'foreign_bodies_deleted': False, 'math_claims_bound_to_relevant_sections_only': True,
          'entire_papers_adversarially_reverified': False, 'exhaustive_priority_audit': False}
(FAMILY / 'FRESH_PRIMARY_SOURCE_BINDINGS.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'sources': len(bindings), 'all_historical_hashes_match': all(row['fresh_body_matches_historical_hash'] for row in bindings),
                  'selected_page_renders': sum(len(row['selected_page_renders']) for row in bindings)}, indent=2))
