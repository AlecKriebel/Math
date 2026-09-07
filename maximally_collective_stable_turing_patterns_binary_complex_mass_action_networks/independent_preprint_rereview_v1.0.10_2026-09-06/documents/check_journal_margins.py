#!/usr/bin/env python3
"""Independent measurements of the actual shipped journal PDF text extents."""
from pathlib import Path
import json
import subprocess
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'source_snapshot'
cases = [
    ('submission/journal/manuscript.pdf', 17, 'independent_verifier/verify_symbolic_certificates.py.'),
    ('submission/journal/manuscript.pdf', 19, '2.80855'),
    ('submission/journal/supplement.pdf', 14, 'independent_verifier/verify_symbolic_certificates.py'),
    ('submission/journal/supplement.pdf', 20, '17)Q'),
]
results = []
for relative, page, needle in cases:
    raw = subprocess.check_output(['pdftotext', '-f', str(page), '-l', str(page),
                                   '-bbox-layout', str(SOURCE/relative), '-'])
    root = ET.fromstring(raw)
    words = [w for w in root.iter() if w.tag.endswith('}word')
             and ''.join(w.itertext()) == needle]
    if not words:
        raise RuntimeError('Missing text witness: '+str((relative, page, needle)))
    word = max(words, key=lambda w: float(w.attrib['xMax']))
    right = float(word.attrib['xMax'])
    # Letter width612bp, declared right margin1.25in=90bp: right text edge522bp.
    if right <= 522+10:
        raise RuntimeError('Material text-area excess not reproduced')
    results.append({'pdf': relative, 'page': page, 'text': needle,
                    'xMax_pdf_points': right, 'configured_right_edge_pdf_points': 522,
                    'rightward_excess_pdf_points': right-522})
out = {'status': 'PASS',
       'scope': 'Four substantial text-width excesses, excluding deliberate line numbers and tiny microtype punctuation protrusions. The fifth actual TeX warning is separately preserved in the clean build logs.',
       'witnesses': results}
(HERE/'ROOT_JOURNAL_MARGIN_CHECK.json').write_text(json.dumps(out, indent=2)+'\n')
print(json.dumps(out, indent=2))
